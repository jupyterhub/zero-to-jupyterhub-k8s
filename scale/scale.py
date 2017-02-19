#!/usr/bin/python

"""Primary scale logic"""
from workload import scheduleGoal, getCriticalNodeNames
from utils import getNodes, getName, setUnschedulable, shutdownSpecifiedNode
from update_nodes import updateUnschedulable
from gcloud_update import increaseNewGCloudNode

SERVICE_PROVIDER = "gcloud"

def shutdownEmptyNodes(nodes=getNodes()):
    """
    1. Check all nodes for if they are empty
    2. If so, first try to remove some node that is unschedulable
    3. Else add to a list of references and set one of those to be unschedulable after
    """
    shutdownCandidates = []
    for each in nodes:
        if numPods(each) == 0:
            if isUnschedulable(each):
                return shutdownSpecifiedNode(each)
            else:
		shutdownCandidates.append(each)

    return setUnschedulable(shutdownCandidates[0])


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
