#!/usr/bin/python

import subprocess
import yaml

# The following code is adapted from the legacy scale script:
# scale-pods.py

# MAIN
NAMESPACES = ['datahub', 'prob140', 'stat28']
USERS_PER_NODE = 7
CLUSTER = 'prod'
KUBECTL_CONTEXT = 'gke_data-8_us-central1-a_prod'
POD_THRESHOLD = 0.9
BUMP_INCREMENT = 2


def __get_hub_pod(namespace, prefix=b'hub-deployment'):
    '''Return the name of the hub pod.'''
    cmd = ['kubectl', '--context=' + KUBECTL_CONTEXT,
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


def __get_singleuser_image(namespace, hub_pod):
    '''Return the name:tag of the hub's singleuser image.'''
    cmd = ['kubectl', '--context=' + KUBECTL_CONTEXT,
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


def increaseNewGCloudNode(new_node_number):
    """ONLY FOR CREATING NEW NODES to ensure 
    new _node_number is running

    NOT FOR SCALING DOWN: random behavior 
    expected"""

    # call gcloud command to start new nodes in GCE
    cmd = ['gcloud', '--quiet', 'container', 'clusters', 'resize', CLUSTER,
           '--size', str(new_node_number)]
    print(' '.join(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    buf = p.read()
    p.close()

    # Populate latest singleuser image on all nodes
    for ns in NAMESPACES:
        hub_pod = __get_hub_pod(ns)
        image = __get_singleuser_image(ns, hub_pod)
        if not image:
            continue

        # TODO: Use absolute path is recommended
        cmd = ['./populate.bash', CLUSTER, image]
        print(' '.join(cmd))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
        buf = p.read()
        p.close()
