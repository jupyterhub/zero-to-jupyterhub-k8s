#!/usr/bin/python
from utils import getNodes, numPods, setUnschedulable, getName, isUnschedulable
import heapq

def getPriority(node):
    """Return the priority value of a node
    for being blocked; smallest == highest
    priority"""
    return numPods(node)

def blockPods(number, nodes):
    """Attempt to block num pods if possible,
    otherwise, block all the pods; return a
    list of blocked node names"""
    
    alreadyBlocked = 0
    counter = 0
    for each in nodes:
        if isUnschedulable(each):
            alreadyBlocked += 1
            nodes.remove(each)
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
        heapq.heappush(priority, (getPriority(nodes[counter]), counter))
        counter += 1
    counter = 0
    blocked = []
    while counter < number:
        _, index = heapq.heappop(priority)
        setUnschedulable(getName(nodes[index]), True)
        blocked.append(getName(nodes[index]))
        counter += 1
    return blocked