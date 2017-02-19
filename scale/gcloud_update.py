#!/usr/bin/python

import subprocess
import yaml

# The following code is adapted from the legacy scale script:
# scale-pods.py

KUBECTL_CONTEXT_PREFIX = 'gke_data-8_us-central1-a_'


def __get_hub_pod(namespace, cluster_name, prefix=b'hub-deployment'):
    '''Return the name of the hub pod.'''
    cmd = ['kubectl', '--context=' + KUBECTL_CONTEXT_PREFIX + cluster_name,
           '--namespace=' + namespace, 'get', 'pods',
           '-o=custom-columns=NAME:.metadata.name']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    line = p.readline()
    while line:
        if line.startswith(prefix):
            return line.strip()
        line = p.readline()
        continue
    p.close()
    return ''


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
    cmd = ['gcloud', '--quiet', 'container', 'clusters', 'resize', cluster_name,
           '--size', str(new_node_number)]
    print(' '.join(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    buf = p.read()
    p.close()

    # Populate latest singleuser image on all nodes
    for ns in namespaces:
        hub_pod = __get_hub_pod(ns, cluster_name)
        image = __get_singleuser_image(ns, hub_pod, cluster_name)
        if not image:
            continue

        # TODO: Use absolute path is recommended
        cmd = ['./populate.bash', cluster_name, image]
        print(' '.join(cmd))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
        buf = p.read()
        p.close()
