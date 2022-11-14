#!/usr/bin/env python3
"""
Helper script to perform two-way sync of a specific json file to a k8s secret
object.

traefik expects a JSON file (acme.json) to persist across time, to make sure
Let's Encrypt certificates work. In kubernetes, pod restarts clear out the
filesystem, making this hard. We could add a persistent volume to the proxy, but
this is excessive for a single file.

This script can do a 'two way' sync of a given file and a key in a kubernetes
secret object. The file should be in an emptyDir volume in the traefik pod,
which should also have this script running as a sidecar.

## Kubernetes Secret -> File system

This needs to happen only once when the pod starts - we do not support
modifications to the secret by other actors. The 'load' command is used to
specify the secret name, key and path to load it into

## File system -> Kubernetes secret

traefik might write new contents to the acme.json file over time, and we need to
sync it to the kubernetes secret object so it remains available if the pod
restarts.

There is a check that ensures that this sync is only made if we have acquired a
certificate, this is to avoid syncing a temporary state that may lock the pod
into a bad state even after restart. Note that this decision makes this script
specific to the acme.json file, but it can be re-generalized again by providing
a predicate hook to provide a criteria for syncing.

Ideally, we would watch for changes to the file with inotify and update the
secret object as needed. However, for now we just operate in a 30s loop. This is
good enough, since traefik can always re-generate certs if needed.
"""
import argparse
import base64
import json
import logging
import os
import sys
import time

from kubernetes import client, config


def update_secret(namespace, secret_name, labels, key, value):
    """
    Update a secret object's key with the value
    """
    try:
        config.load_kube_config()
    except:
        config.load_incluster_config()

    v1 = client.CoreV1Api()
    try:
        secret = v1.read_namespaced_secret(namespace=namespace, name=secret_name)
    except client.rest.ApiException as e:
        if e.status == 404:
            secret = client.V1Secret(
                metadata=client.V1ObjectMeta(name=secret_name, labels=labels), data={}
            )
            v1.create_namespaced_secret(namespace=namespace, body=secret)
            logging.info(f"Created secret {secret_name} since it does not exist")
        else:
            raise
    # Value should be base64'd string
    new_value = base64.standard_b64encode(value).decode()
    if secret.data is None:
        secret.data = {}
    if new_value != secret.data.get(key):
        secret.data[key] = base64.standard_b64encode(value).decode()
        v1.patch_namespaced_secret(namespace=namespace, name=secret_name, body=secret)
        logging.info(f"Updated secret {secret_name} with new value for key {key}")


def get_secret_value(namespace, secret_name, key):
    try:
        config.load_kube_config()
    except:
        config.load_incluster_config()

    v1 = client.CoreV1Api()
    try:
        secret = v1.read_namespaced_secret(namespace=namespace, name=secret_name)
    except client.rest.ApiException as e:
        if e.status == 404:
            # Secret doesn't exist
            return None
        raise
    if secret.data is None or key not in secret.data:
        return None
    return base64.standard_b64decode(secret.data[key])


def setup_logging():
    """
    Set up root logger
    """
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO
    )


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--namespace", help="Namespace the secret exists in")

    argparser.add_argument("action", choices=["load", "watch-save"])

    argparser.add_argument(
        "secret_name", help="Name of secret to sync with. Will be created if needed."
    )

    argparser.add_argument("key", help="Key in secret object to sync file to")

    argparser.add_argument("path", help="Path in filesystem to sync to")

    argparser.add_argument(
        "--label",
        help="Labels (of form key=value) to add to the k8s secret when it is created",
        action="append",
    )

    args = argparser.parse_args()

    setup_logging()
    logging.info(str.join(" ", sys.argv))

    if not args.namespace:
        try:
            with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace") as f:
                args.namespace = f.read().strip()
        except FileNotFoundError:
            logging.error(
                "Can not determine a namespace, must be explicitly set with --namespace"
            )
            sys.exit(1)

    if args.action == "load":
        value = get_secret_value(args.namespace, args.secret_name, args.key)
        if value:
            with open(args.path, "wb") as f:
                f.write(value)
                os.fchmod(f.fileno(), 0o600)
    elif args.action == "watch-save":
        labels = {}
        for label in args.label:
            l_splits = label.split("=", 1)
            labels[l_splits[0]] = l_splits[1]
        # FIXME: use inotifiy
        while True:
            if not os.path.exists(args.path):
                logging.warning(f"Watched file {args.path} not found")
            else:
                with open(args.path, "rb") as f:
                    file_content = f.read()

                if not file_content:
                    logging.info(f"Watched file {args.path} is currently empty")
                else:
                    file_dict = json.loads(file_content)

                    for cert_resolver in file_dict.values():
                        if cert_resolver.get("Certificates"):
                            update_secret(
                                args.namespace,
                                args.secret_name,
                                labels,
                                args.key,
                                file_content,
                            )
                            break
                    else:
                        logging.info(f"No certificate detected in {args.path}")

            time.sleep(30)


if __name__ == "__main__":
    main()
