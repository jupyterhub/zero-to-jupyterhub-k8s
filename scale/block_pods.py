#!/usr/bin/python
from utils import numPods, setUnschedulable, getName, isUnschedulable
import heapq

def __getPriority(node):
    """Return the priority value of a node
    for being blocked; smallest == highest
    priority"""
    return numPods(node)

def blockPods(number, originNodes):
    """Attempt to make sure given number of
    pods are blocked, if possible, 
    otherwise, block all the pods; 
    return a list of blocked node names"""
    
    alreadyBlocked = 0
    counter = 0
    nodes = []
    for each in originNodes:
        if isUnschedulable(each):
            alreadyBlocked += 1
        else:
            nodes.append(each)
    number -= alreadyBlocked
    if number <= 0:
        return []
    if number > len(nodes):
        number = len(nodes)
    
    # number = Number of nodes to be blocked
    # nodes = A list of schedulable nodes
    # alreadyBlocked = NUmber of nodes already blocked
    
    priority = []
    while counter < len(nodes):
        heapq.heappush(priority, (__getPriority(nodes[counter]), counter))
        counter += 1
    counter = 0
    blocked = []
    while counter < number:
        _, index = heapq.heappop(priority)
        setUnschedulable(getName(nodes[index]), True)
        blocked.append(getName(nodes[index]))
        counter += 1
    return blocked