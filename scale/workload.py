#!/usr/bin/python
from utils import getNodes, numPods, isUnschedulable
from settings import CAPACITY_PER_NODE, MIN_NODES, MAX_NODES, MAX_UTILIZATION, MIN_UTILIZATION, OPTIMAL_UTILIZATION

def getWorkload(node):
    """Return the workload on the given node"""
    return numPods(node)

def getSumWorkload(nodes):
    """Return the total workload on
    the given list of nodes"""
    total = 0
    for each in nodes:
        total += getWorkload(each)
    return total

def getCapacity(node):
    """Return the workload capacity of the 
    given node"""
    # FIXME: not adjusted to different machine types
    return CAPACITY_PER_NODE

def getNumSchedulable(nodes):
    """Return number of nodes schedulable"""
    result = 0
    for each in nodes:
        if not isUnschedulable(each):
            result += 1
    return result

def getNumUnschedulable(nodes):
    """Return number of nodes unschedulable"""
    return len(nodes) - getNumSchedulable(nodes)

def getEffectiveWorkload(nodes):
    """Return effective workload in the given list of nodes"""
    return getSumWorkload(nodes) / getNumSchedulable(nodes)

def scheduleGoal(nodes = getNodes()):
    """Return the goal number of schedulable nodes given
    the current situation"""
    currentUtilization = getEffectiveWorkload(nodes) / getCapacity(nodes[0])
    if currentUtilization >= MIN_UTILIZATION and currentUtilization <= MAX_UTILIZATION:
        # leave unchanged
        return getNumSchedulable(nodes)
    else:
        # need to scale down
        requiredNum = round(getSumWorkload(nodes) / OPTIMAL_UTILIZATION / getCapacity(nodes[0]))
        if requiredNum < MIN_NODES:
            requiredNum = MIN_NODES
        if requiredNum > MAX_NODES:
            requiredNum = MAX_NODES
        return requiredNum