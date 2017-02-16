#!/usr/bin/python
from scale.utils import getNodes, numPods, setUnschedulable, getName
import heapq

def getPriority(node):
    """Return the priority value of a node
    for being blocked; smallest == highest
    priority"""
    return numPods(node)

def blockPods(number, nodes):
    """Attempt to block num pods if possible,
    otherwise, block all the pods"""
    if number > len(nodes):
        number = len(nodes)
    priority = []
    counter = 0
    while counter < len(nodes):
        heapq.heappush(priority, (getPriority(nodes[counter]), counter))
        counter += 1
    counter = 0
    while counter < number:
        _, index = heapq.heappop(priority)
        setUnschedulable(getName(nodes[counter], True))
        counter += 1