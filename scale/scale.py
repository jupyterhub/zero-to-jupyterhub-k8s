#!/usr/bin/python

"""Primary scale logic"""
from workload import scheduleGoal, getCriticalNodeNames
from utils import getNodes, getName
from update_nodes import updateUnschedulable
from gcloud_update import increaseNewGCloudNode

SERVICE_PROVIDER = "gcloud"


def shutdownEmptyNodes():
    raise NotImplementedError


def createNewNodes(newTotalNodes):
    """create new nodes to match newTotalNodes required
    only for scaling up, no action taken if newTotalNodes
    is smaller than number of current nodes"""
    if newTotalNodes <= len(getNodes()):
        return
    if SERVICE_PROVIDER == "gcloud":
        increaseNewGCloudNode(newTotalNodes)


def scale():
    """Update the nodes property based on scaling policy
    and create new nodes if necessary"""
    goal = scheduleGoal()
    nodes = []
    criticalNodeNames = getCriticalNodeNames()
    allNodes = getNodes()
    for each in allNodes:
        if getName(each) not in criticalNodeNames:
            nodes.append(each)
    updateUnschedulable(goal, nodes)

    if len(criticalNodeNames) + goal > len(allNodes):
        createNewNodes(len(criticalNodeNames) + goal)

    shutdownEmptyNodes()
