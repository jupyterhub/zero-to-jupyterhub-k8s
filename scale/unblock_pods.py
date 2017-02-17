#!/usr/bin/python
from utils import numPods, setUnschedulable, getName, isUnschedulable
import heapq

def __getPriority(node):
    """Return the priority value of a node
    to be unblocked (schedulable); biggest
    == highest priority"""
    return -numPods(node)

def unblockPods(number, originNodes):
    """Attempt to unblock num pods if possible,
    otherwise, unblock all the pods; return a
    list of unblocked node names"""
    
    counter = 0
    nodes = []
    for each in originNodes:
        if isUnschedulable(each):
            nodes.append(each)
    if number > len(nodes):
        number = len(nodes)
    
    # number = Number of nodes to be unblocked
    # nodes = A list of unschedulable nodes
    
    priority = []
    while counter < len(nodes):
        heapq.heappush(priority, (__getPriority(nodes[counter]), counter))
        counter += 1
    counter = 0
    unblocked = []
    while counter < number:
        _, index = heapq.heappop(priority)
        setUnschedulable(getName(nodes[index]), False)
        unblocked.append(getName(nodes[index]))
        counter += 1
    return unblocked