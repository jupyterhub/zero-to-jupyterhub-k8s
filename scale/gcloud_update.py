#!/usr/bin/python3

import subprocess
from settings import GCLOUD_INSTANCE_GROUP, GCE_ZONE
from utils import get_pods, get_pod_type
import logging
scale_logger = logging.getLogger("scale")


def shutdown_specified_node(name):
    """Deletes the specified node by calling the Google Cloud Engine"""

    cmd = ['gcloud', 'compute', 'instance-groups', 'managed', 'delete-instances',
           GCLOUD_INSTANCE_GROUP, '--instances=' + name]
    p = subprocess.Popen(' '.join(cmd), stdout=subprocess.PIPE)
    output, err = p.communicate()
    if err:
        scale_logger.error("Cannot shutdown node %s" % name)


def __get_hub_pod(namespace):
    '''Return the hub pod. Return None if not found.'''
    pods = get_pods()
    for pod in pods:
        if get_pod_type(pod) == 'hub' and pod.metadata.namespace == namespace:
            return pod
    return None


def increase_new_gcloud_node(new_node_number, cluster_name):
    """ONLY FOR CREATING NEW NODES to ensure 
    new _node_number is running

    NOT FOR SCALING DOWN: random behavior 
    expected"""

    # call gcloud command to start new nodes in GCE
    # FIXME: Use GCloud API calls instead
    scale_logger.info("Resizing the cluster to %i nodes" % new_node_number)
    cmd = ['gcloud', '--quiet', 'container', 'clusters', 'resize', cluster_name,
           '--size', str(new_node_number), '--zone', GCE_ZONE]
    print(' '.join(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    buf = p.read()
    p.close()
