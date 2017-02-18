#!/usr/bin/python
from utils import getNodes, numPods, setUnschedulable, getName, isUnschedulable
import heapq

def __getBlockPriority(node):
    """Return the priority value of a node
    for being blocked; smallest == highest
    priority"""
    return numPods(node)

def __updateNodes(nodes, unschedulable):
    """Update given list of nodes with given
    unschedulable property"""
    
    updated = []
    for each in nodes:
        setUnschedulable(getName(each), unschedulable)
        updated.append(getName(each))
    return updated

def updateUnschedulable(number_unschedulable, nodes = getNodes(), f=__getBlockPriority):
    """Attempt to make sure given number of
    nodes are blocked, if possible; 
    return number of nodes newly blocked; negative
    value means the number of nodes unblocked"""
    
    assert number_unschedulable >= 0
    
    schedulableNodes= []
    unschedulableNodes = []
    
    priority = []
    
    # Analyze nodes status and establish blocking priority
    for count in range(len(nodes)):
        if isUnschedulable(nodes[count]):
            unschedulableNodes.append(nodes[count])
        else:
            schedulableNodes.append(nodes[count])
        priority.append((f(nodes[count]), count))
    
    # Attempt to modify property based on priority
    toBlock = []
    toUnBlock = []
    
    heapq.heapify(priority)
    for _ in range(number_unschedulable):
        if len(priority) > 0:
            _, index = heapq.heappop(priority)
            if nodes[index] in schedulableNodes:
                toBlock.append(nodes[index])
        else:
            break
    for _, index in priority:
        if nodes[index] in unschedulableNodes:
            toUnBlock.append(nodes[index])
    
    __updateNodes(toBlock, True)
    __updateNodes(toUnBlock, False)
    
    return len(toBlock) - len(toUnBlock)
    