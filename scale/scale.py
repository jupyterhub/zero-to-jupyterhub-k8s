#!/usr/bin/python

"""Primary scale logic"""
from workload import scheduleGoal, getCriticalNodeNames
from utils import getNodes, getName
from update_nodes import updateUnschedulable

def shutdownEmptyNodes():
    raise NotImplementedError

def resizeForNewNodes(totalNodes):
    raise NotImplementedError

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
        resizeForNewNodes(len(criticalNodeNames) + goal)
    
    shutdownEmptyNodes()