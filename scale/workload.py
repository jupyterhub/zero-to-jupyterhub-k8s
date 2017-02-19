#!/usr/bin/python
from utils import getNodes, isUnschedulable, getPods, getPodNamesapce,\
    getPodType, getPodHostName, getName
from settings import CAPACITY_PER_NODE, MIN_NODES, MAX_NODES, MAX_UTILIZATION, MIN_UTILIZATION, OPTIMAL_UTILIZATION
from settings import OMIT_NAMESPACES, CRITICAL_POD_TYPES, OMIT_POD_TYPES, CRITICAL_NAMESPACES

def numPods(node, pods = getPods()):
    """Return the effective number of pods on
    the node"""
    result = 0
    for each in pods:
        if not(getPodNamesapce(each) in OMIT_NAMESPACES or getPodType(pods) in OMIT_POD_TYPES) and getPodHostName(each) == getName(node):
            result += 1
    return result
    
def getCriticalNodeNames(pods = getPods()):
    """Return a list of nodes where critical pods
    are running"""
    result = []
    for each in pods:
        if getPodNamesapce(each) in CRITICAL_NAMESPACES or getPodType(pods) in CRITICAL_POD_TYPES:
            if getPodHostName(each) not in result:
                result.append(getPodHostName(each))
    return result

def getWorkload(node, pods = getPods()):
    """Return the workload on the given node"""
    return numPods(node, pods)

def getSumWorkload(nodes):
    """Return the total workload on
    the given list of nodes"""
    pods = getPods()
    total = 0
    for each in nodes:
        total += getWorkload(each, pods)
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