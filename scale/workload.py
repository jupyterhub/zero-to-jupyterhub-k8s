#!/usr/bin/python

"""Provide functions to analyze current workload status of the cluster.

All functions in the file should be read-only and cause no side effects."""

from utils import getNodes, isUnschedulable, getPods, getPodNamesapce, \
    getPodType, getPodHostName, getName
from settings import CAPACITY_PER_NODE, MIN_NODES, MAX_NODES, MAX_UTILIZATION, MIN_UTILIZATION, OPTIMAL_UTILIZATION
from settings import OMIT_NAMESPACES, CRITICAL_POD_TYPES, OMIT_POD_TYPES, CRITICAL_NAMESPACES


def numPods(node, pods=getPods()):
    """Return the effective number of noncritical
    pods on the node"""
    result = 0
    for each in pods:
        if not(getPodNamesapce(each) in OMIT_NAMESPACES or
               getPodNamesapce(each) in CRITICAL_NAMESPACES or
               getPodType(each) in OMIT_POD_TYPES or
               getPodType(each) in CRITICAL_POD_TYPES
               ) and getPodHostName(each) == getName(node):
            result += 1
    return result


def getCriticalNodeNames(pods=getPods()):
    """Return a list of nodes where critical pods
    are running"""
    result = []
    for each in pods:
        if getPodNamesapce(each) in CRITICAL_NAMESPACES or getPodType(each) in CRITICAL_POD_TYPES:
            if getPodHostName(each) not in result:
                result.append(getPodHostName(each))
    return result


def getWorkload(node, pods=getPods()):
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


def getNumSchedulable(nodes, criticalNodeNames):
    """Return number of nodes schedulable AND NOT
    IN THE LIST OF CRITICAL NODES"""
    result = 0
    for each in nodes:
        if (not isUnschedulable(each)) and getName(each) not in criticalNodeNames:
            result += 1
    return result


def getNumUnschedulable(nodes):
    """Return number of nodes unschedulable

    ASSUMING CRITICAL NODES ARE SCHEDULABLE"""
    result = 0
    for each in nodes:
        if isUnschedulable(each):
            result += 1
    return result


def getEffectiveWorkload(nodes, criticalNodeNames):
    """Return effective workload in the given list of nodes"""
    try:
        return getSumWorkload(nodes) / getNumSchedulable(nodes, criticalNodeNames)
    except ZeroDivisionError:
        return float("inf")


def scheduleGoal():
    """Return the goal number of schedulable nodes IN ADDITION
    TO CRITICAL NODES, given the current situation"""
    nodes = getNodes()
    criticalNodeNames = getCriticalNodeNames(getPods())
    currentUtilization = getEffectiveWorkload(
        nodes, criticalNodeNames) / getCapacity(nodes[0])
    if currentUtilization >= MIN_UTILIZATION and currentUtilization <= MAX_UTILIZATION:
        # leave unchanged
        return getNumSchedulable(nodes, criticalNodeNames)
    else:
        # need to scale down
        requiredNum = round(
            getSumWorkload(nodes) / OPTIMAL_UTILIZATION / getCapacity(nodes[0]))
        if requiredNum < MIN_NODES - len(criticalNodeNames):
            requiredNum = MIN_NODES - len(criticalNodeNames)
        if requiredNum > MAX_NODES - len(criticalNodeNames):
            requiredNum = MAX_NODES - len(criticalNodeNames)
        return requiredNum
