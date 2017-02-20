#!/usr/bin/python3

import subprocess
from settings import GCLOUD_INSTANCE_GROUP, GCE_ZONE
from utils import get_pods, get_pod_type, get_pod_namespace

import logging


def shutdown_specified_node(name):
    """Deletes the specified node by calling the Google Cloud Engine"""
    cmd = ['gcloud', 'compute', 'instance-groups', 'managed', 'delete-instances',
           GCLOUD_INSTANCE_GROUP, '--instances=' + name]
    p = subprocess.Popen(' '.join(cmd), stdout=subprocess.PIPE)
    output, err = p.communicate()

    # TODO: Jeff pls find a proper way to log the below message
    return "Successfully removed node: %s\n" % name if not err else "Unable to remove node"

# The following code is adapted from the legacy scale script:
# scale-pods.py

KUBECTL_CONTEXT_PREFIX = 'gke_data-8_us-central1-a_'


def __get_hub_pod(namespace):
    '''Return the hub pod. Return None if not found.'''
    pods = get_pods()
    for each in pods:
        if get_pod_type(each) == 'hub' and get_pod_namespace(each) == namespace:
            return each
    return None


def increase_new_gcloud_node(new_node_number, cluster_name):
    """ONLY FOR CREATING NEW NODES to ensure 
    new _node_number is running

    NOT FOR SCALING DOWN: random behavior 
    expected"""

    # call gcloud command to start new nodes in GCE
    # FIXME: Use GCloud API calls instead
    cmd = ['gcloud', '--quiet', 'container', 'clusters', 'resize', cluster_name,
           '--size', str(new_node_number), '--zone', GCE_ZONE]
    print(' '.join(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    buf = p.read()
    p.close()