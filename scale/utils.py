#/usr/bin/python3

"""Kubernetes API access functions"""

from kubernetes import client, config
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
