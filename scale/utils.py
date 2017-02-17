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
        print(str(e))
        sys.exit(1)

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

    r = requests.patch(url, json = newNode, headers = patch_header)
    if r.status_code == 200:
        return ""
    else:
        try:
            msg = json.loads(r.text)
            return msg["message"]
        except Exception:
            return "Return type was " + str(r.status)
        
def numPods(node):
    """Return number of pods running on the node,
    return -1 if an error occurred"""
    # TODO: What is there is a permanent pod, e.g.
    # hub / proxy?
    
    try:
        return len(node["status"]["images"])
    except Exception:
        return -1

def getName(node):
    """Return name of a node, return '' if
    an error occurred """
    try:
        return node["metadata"]["name"]
    except Exception:
        return ''
    
def isUnschedulable(node):
    """Return the value of 'Unschedulable' of a node"""
    if "unschedulable" in node["spec"]:
        return node["spec"]["unschedulable"]
    else:
        return False
