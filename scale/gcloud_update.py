#!/usr/bin/python

import subprocess
import yaml
from settings import GCLOUD_INSTANCE_GROUP
from utils import getPods, getPodType, getPodNamespace, getName


def shutdownSpecifiedNode(name):
    """Deletes the specified node by calling the Google Cloud Engine"""
    cmd = ['gcloud', 'compute', 'instance-groups', 'managed', 'delete-instances',
           GCLOUD_INSTANCE_GROUP, '--instances=' + name]
    p = subprocess.Popen(' '.join(cmd), stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    return "Successfully removed node: %s\n" % name if not err else "Unable to remove node"

# The following code is adapted from the legacy scale script:
# scale-pods.py

KUBECTL_CONTEXT_PREFIX = 'gke_data-8_us-central1-a_'


# FIXME: replace kubectl with up to date API calls
def __get_hub_pod(namespace):
    '''Return the name of the hub pod. Return '' if not found.'''
    pods = getPods()
    for each in pods:
        if getPodType(each) == 'hub' and getPodNamespace(each) == namespace:
            return getName(each)
    return ''


# FIXME: replace kubectl with up to date API calls
def __get_singleuser_image(namespace, hub_pod, cluster_name):
    '''Return the name:tag of the hub's singleuser image.'''
    cmd = ['kubectl', '--context=' + KUBECTL_CONTEXT_PREFIX + cluster_name,
           '--namespace=' + namespace, 'get', 'pod', '-o=yaml',
           hub_pod]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    buf = p.read()
    p.close()

    description = yaml.load(buf)
    image = ''
    for env in description['spec']['containers'][0]['env']:
        if env['name'] == 'SINGLEUSER_IMAGE':
            image = env['value']
            break

    return image


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
        image = __get_singleuser_image(ns, hub_pod, cluster_name)
        if not image:
            continue

        # FIXME: Use absolute path is recommended
        # TODO: Use native python scripts to populate
        cmd = ['./populate.bash', cluster_name, image]
        print(' '.join(cmd))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
        buf = p.read()
        p.close()
