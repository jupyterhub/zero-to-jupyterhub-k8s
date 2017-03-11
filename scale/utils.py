#/usr/bin/python3

"""Kubernetes API access functions"""

import logging

scale_logger = logging.getLogger("scale")
logging.getLogger("kubernetes").setLevel(logging.WARNING)


def get_pod_host_name(pod):
    """Return the host node name of the pod"""
    # Based on Kubernetes API:
    # https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_podspec
    # ** API is unclear the value of nodeName flag after the pod is scheduled
    return pod.spec.node_name


def get_pod_type(pod):
    """Return the Type of the pod"""
    # TODO: May not be the best approach
    return pod.metadata.name.split('-')[0]


def get_pod_memory_request(pod):
    """Returns the amount of memory requested
    by the node"""
    node_memory_request = 0
    try:
        node_memory_request = \
            int(pod.spec.containers[0].resources.requests['memory'])
    except (KeyError, TypeError):
        pass
    return node_memory_request


def get_node_memory_capacity(node):
    """Converts the specific memory entry 
    of the kubernetes API into the byte capacity"""
    node_mem_in_kibibytes = int(
        node.status.capacity['memory'].replace('Ki', ''))
    node_mem_in_bytes = 1024 * node_mem_in_kibibytes
    return node_mem_in_bytes


def check_list_intersection(list1, list2):
    """Return True if two lists have intersection,
    otherwise False"""
    if list1 is None or list2 is None:
        return False
    return len(set(list1).intersection(set(list2))) != 0


def user_confirm(prompt=None, resp=False):
    """prompts for yes or no response from the user. Returns True for yes and
    False for no.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n: 
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: 
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True

    """

    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s/%s] ' % (prompt, 'Y', 'n')
    else:
        prompt = '%s [%s/%s]  ' % (prompt, 'y', 'N')

    while True:
        ans = input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print('please enter y or n.')
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False
