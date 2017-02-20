#!/usr/bin/python

import subprocess
from settings import GCLOUD_INSTANCE_GROUP
from utils import getPods, getPodType, getPodNamespace,\
    get_singleuser_image_value

import logging


def shutdownSpecifiedNode(name):
    """Deletes the specified node by calling the Google Cloud Engine"""
    cmd = ['gcloud', 'compute', 'instance-groups', 'managed', 'delete-instances',
           GCLOUD_INSTANCE_GROUP, '--instances=' + name]
    p = subprocess.Popen(' '.join(cmd), stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()

    # TODO: Jeff pls find a proper way to log the below message
    return "Successfully removed node: %s\n" % name if not err else "Unable to remove node"

# The following code is adapted from the legacy scale script:
# scale-pods.py

KUBECTL_CONTEXT_PREFIX = 'gke_data-8_us-central1-a_'


def __get_hub_pod(namespace):
    '''Return the hub pod. Return None if not found.'''
    pods = getPods()
    for each in pods:
        if getPodType(each) == 'hub' and getPodNamespace(each) == namespace:
            return each
    return None


def increaseNewGCloudNode(new_node_number, cluster_name, namespaces):
    """ONLY FOR CREATING NEW NODES to ensure 
    new _node_number is running

    NOT FOR SCALING DOWN: random behavior 
    expected"""

    # call gcloud command to start new nodes in GCE
    # FIXME: Use GCloud API calls instead
    cmd = ['gcloud', '--quiet', 'container', 'clusters', 'resize', cluster_name,
           '--size', str(new_node_number)]
    print(' '.join(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    buf = p.read()
    p.close()

    # Populate latest singleuser image on all nodes
    for ns in namespaces:
        hub_pod = __get_hub_pod(ns)
        image = get_singleuser_image_value(ns, hub_pod, cluster_name)
        if image == '':
            continue

        # FIXME: Use absolute path is recommended
        # TODO: Use native python scripts to populate
        cmd = ['./populate.bash', cluster_name, image]
        print(' '.join(cmd))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
        buf = p.read()
        p.close()
