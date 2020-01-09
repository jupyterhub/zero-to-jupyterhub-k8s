#!/usr/bin/env python3
"""
Helper script to run certbot inside a kubernetes cluster.

certbot expects contents of /etc/letsencrypt to be persistent
across runs, so it knows when to renew certificates & when to leave
them alone. This is a problem in Kubernetes, since we try to avoid
having persistent disks unless we must.

This script saves / restores the contents of /etc/letsencrypt into
a Kubernetes secret object, thus letting certbot operate unchanged
without needing any persistent storage.

This script runs as a sidecar to an nginx container that has webroot
set to /usr/shared/nginx/html, and is shared with this container. This
lets us use the webroot challenge with certbot.
"""
import sys
import os
import subprocess
import argparse
import time
import tarfile
import io
import base64
import logging
from kubernetes import client, config

def update_secret(namespace, secret_name, key, value):
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
                metadata=client.V1ObjectMeta(name=secret_name),
                data={}
            )
            resp = v1.create_namespaced_secret(namespace=namespace, body=secret)
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
    Set up root logger to log to stderr
    """
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO, stream=sys.stderr)

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--namespace',
        help='Namespace to operate in'
    )

    argparser.add_argument(
        'action',
        choices=['load', 'watch-save']
    )

    argparser.add_argument(
        'secret_name'
    )

    argparser.add_argument(
        'key',
    )

    argparser.add_argument(
        'path',
    )

    args = argparser.parse_args()

    setup_logging()

    if not args.namespace:
        try:
            with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace") as f:
                args.namespace = f.read().strip()
        except FileNotFoundError:
            print("Can not determine a namespace, must be explicitly set with --namespace", file=sys.stderr)
            sys.exit(1)

    if args.action == 'load':
        value = get_secret_value(args.namespace, args.secret_name, args.key)
        if value:
            with open(args.path, 'wb') as f:
                f.write(value)
                os.fchmod(f.fileno(), 0o600)
    else:
        while True:
            if os.path.exists(args.path):
                with open(args.path, 'rb') as f:
                    update_secret(args.namespace, args.secret_name, args.key, f.read())
            time.sleep(30)

if __name__ == '__main__':
    main()
