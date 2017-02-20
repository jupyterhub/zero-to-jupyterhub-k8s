#/usr/bin/python

"""Kubernetes API access functions"""

import requests
import json
import sys
from settings import API_HOST, API_PORT
import logging

logging.getLogger("requests").setLevel(logging.WARNING)


def generate_url(host, port):
    return "http://" + host + ':' + port + "/api/v1/"


def get_nodes():
    """Return a list of v1.Node dict"""
    r = requests.get(generate_url(API_HOST, API_PORT) +
                     "nodes")
    assert r.status_code == 200
    try:
        nodesList = json.loads(r.text)
        return nodesList['items']
    except Exception as e:
        # FIXME: proper exception handling
        print(str(e))
        sys.exit(1)


def get_pods():
    """Return a list of v1.Pod dict"""
    r = requests.get(generate_url(API_HOST, API_PORT) +
                     "pods")
    assert r.status_code == 200
    try:
        podsList = json.loads(r.text)
        return podsList['items']
    except Exception as e:
        # FIXME: proper exception handling
        print(str(e))
        sys.exit(1)


def get_namespaces_name():
    """Return a list of namespaces in the form of string"""
    r = requests.get(generate_url(API_HOST, API_PORT) +
                     "namespaces")
    assert r.status_code == 200
    result = []
    try:
        namespaces = json.loads(r.text)
        for each in namespaces["items"]:
            result.append(get_name(each))
        return result
    except Exception as e:
        # FIXME: proper exception handling
        print(str(e))
        sys.exit(1)


def get_pod_host_name(pod):
    """Return the host node name of the pod"""
    # Based on Kubernetes API:
    # https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_podspec
    # ** API is unclear the value of nodeName flag after the pod is scheduled
    return pod["spec"]["nodeName"]


def get_cluster_name(node=get_nodes()[0]):
    """Return the (guessed) name of the cluster"""
    nodeName = get_name(node)
    parts = nodeName.split('-')
    assert len(parts) > 2
    return parts[1]


def get_pod_name(pod):
    """Return the name of the pod"""
    return get_name(pod)


def get_node_name(node):
    """Return the name of the node"""
    return get_name(node)


def get_pod_namespace(pod):
    """Return the namespace of the pod"""
    return pod["metadata"]["namespace"]


def get_pod_type(pod):
    """Return the Type of the pod"""
    # TODO: May not be the best approach
    return get_pod_name(pod).split('-')[0]


def set_unschedulable(name, value=True, url=generate_url(API_HOST, API_PORT) + "nodes/"):
    """Set the spec key 'unschedulable'"""
    url += name + '/'
    newNode = {
        "apiVersion": "v1",
        "kind": "Node",
                "metadata": {
                    "name": name
                },
        "spec": {
                    "unschedulable": value
                }
    }

    # PATCH header required by Kubernetes
    patch_header = {"Content-Type": "application/strategic-merge-patch+json"}

    r = requests.patch(url, json=newNode, headers=patch_header)
    if r.status_code == 200:
        return ""
    else:
        try:
            msg = json.loads(r.text)
            return msg["message"]
        except Exception:
            return "Return type was " + str(r.status)


def get_name(resource):
    """ Return name of a node, return '' if
    an error occurred """
    try:
        return resource["metadata"]["name"]
    except Exception:
        return ''


def is_unschedulable(node):
    """Return the value of 'Unschedulable' of a node"""
    if "unschedulable" in node["spec"]:
        return node["spec"]["unschedulable"]
    else:
        return False


def get_singleuser_image_value(hub_pod):
    '''Return the name:tag of the hub's singleuser image. If 
    not found, return ''. '''
    try:
        for env in hub_pod['spec']['containers'][0]['env']:
            if env['name'] == 'SINGLEUSER_IMAGE':
                return env['value']

        return ''
    except Exception:
        return ''
