#!/usr/bin/python

"""Kubernetes API access functions"""

import requests
import json
import sys
from settings import API_HOST, API_PORT


def generateUrl(host, port):
    return "http://" + host + ':' + port + "/api/v1/"


def getNodes():
    """Return a list of v1.Node dict"""
    r = requests.get(generateUrl(API_HOST, API_PORT) +
                     "nodes")
    assert r.status_code == 200
    try:
        nodesList = json.loads(r.text)
        return nodesList['items']
    except Exception as e:
        # FIXME: proper exception handling
        print(str(e))
        sys.exit(1)


def getPods():
    """Return a list of v1.Pod dict"""
    r = requests.get(generateUrl(API_HOST, API_PORT) +
                     "pods")
    assert r.status_code == 200
    try:
        podsList = json.loads(r.text)
        return podsList['items']
    except Exception as e:
        # FIXME: proper exception handling
        print(str(e))
        sys.exit(1)


def getPodHostName(pod):
    """Return the host node name of the pod"""
    # Based on Kubernetes API:
    # https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_podspec
    # ** API is unclear the value of nodeName flag after the pod is scheduled
    return pod["spec"]["nodeName"]


def getPodName(pod):
    """Return the name of the pod"""
    return getName(pod)


def getNodeName(node):
    """Return the name of the node"""
    return getName(node)


def getPodNamesapce(pod):
    """Return the namespace of the pod"""
    return pod["metadata"]["namespace"]


def getPodType(pod):
    """Return the Type of the pod"""
    # TODO: May not be the best approach
    return getPodName(pod).split('-')[0]


def setUnschedulable(name, value=True, url=generateUrl(API_HOST, API_PORT) + "nodes/"):
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


def getName(resource):
    """Return name of a node, return '' if
    an error occurred """
    try:
        return resource["metadata"]["name"]
    except Exception:
        return ''


def isUnschedulable(node):
    """Return the value of 'Unschedulable' of a node"""
    if "unschedulable" in node["spec"]:
        return node["spec"]["unschedulable"]
    else:
        return False
