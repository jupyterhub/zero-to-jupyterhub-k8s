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
import subprocess
import argparse
import time
import tarfile
import io
import base64
import logging
from kubernetes import client, config

def compress_dir(path):
    """
    Compress directory at 'path' to a tar.gz & return it.

    Paths stored in the tarball are relative to the base directory -
    so /etc/letsencrypt/account/ is stored as account/
    """
    compressed_stream = io.BytesIO()
    with tarfile.open(fileobj=compressed_stream, mode='w:gz') as tf:
        tf.add(path, arcname='.')
    return compressed_stream.getvalue()

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
    return base64.standard_b64decode(secret.data[key])

def setup_logging():
    """
    Set up root logger to log to stderr
    """
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO, stream=sys.stderr)

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        'secret_name',
        help='Name of kubernetes secret to store certificates in'
    )
    argparser.add_argument(
        'email',
        help='Contact email to pass to letsencrypt'
    )
    argparser.add_argument(
        'domains',
        help='List of domains to get certificates for',
        nargs='+'
    )

    argparser.add_argument(
        '--namespace',
        help='Namespace to operate in'
    )

    argparser.add_argument(
        '--test-cert',
        help='Get test certificates from the staging server',
        action='store_true'
    )

    args = argparser.parse_args()

    setup_logging()

    if not args.namespace:
        try:
            with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace") as f:
                args.namespace = f.read().strip()
        except FileNotFoundError:
            print("Can not determin a namespace, must be explicitly set with --namespace", file=sys.stderr)
            sys.exit(1)

    current_dir = get_secret_value(args.namespace, args.secret_name, 'letsencrypt.tar.gz')
    if current_dir:
        with tarfile.open(fileobj=io.BytesIO(current_dir), mode='r:gz') as tf:
            tf.extractall('/etc/letsencrypt')

    certbot_args = [
        'certbot',
        'certonly', '--webroot', '-n', '--agree-tos',
        '-m', args.email,
        '-w', '/usr/share/nginx/html'
    ] + [f'-d={d}' for d in args.domains]

    if args.test_cert:
        certbot_args.append('--test-cert')
        logging.info("Using Let's Encrypt Staging server")

    while True:
        logging.info(f"Calling certbot: {' '.join(certbot_args)}")
        subprocess.check_call(certbot_args)
        letsencrypt_dir = compress_dir('/etc/letsencrypt')
        update_secret(args.namespace, args.secret_name, 'letsencrypt.tar.gz', letsencrypt_dir)
        time.sleep(30)

if __name__ == '__main__':
    main()
