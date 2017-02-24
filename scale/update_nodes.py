#!/usr/bin/python3

"""Execute changes to the Kubernetes cluster"""

import heapq
import logging
scale_logger = logging.getLogger("scale")


def __updateNodes(k8s, nodes, unschedulable):
    """Update given list of nodes with given
    unschedulable property"""

    updated = []
    for node in nodes:
        k8s.set_unschedulable(node.metadata.name, unschedulable)
        updated.append(node.metadata.name)
    return updated


def updateUnschedulable(number_unschedulable, nodes, k8s, calculatePriority=None):
    """Attempt to make sure given number of
    nodes are blocked, if possible; 
    return number of nodes newly blocked; negative
    value means the number of nodes unblocked

    calculatePriority should be a function
    that takes a node and return its priority value
    for being blocked; smallest == highest
    priority; default implementation uses get_pods_number_on_node

    CRITICAL NODES SHOULD NOT BE INCLUDED IN THE INPUT LIST"""

    if number_unschedulable < 0:
        number_unschedulable = 0
    number_unschedulable = int(number_unschedulable)

    scale_logger.info(
        "Updating unschedulable flags to ensure %i nodes are unschedulable" % number_unschedulable)

    if calculatePriority == None:
        # Default implementation based on get_pods_number_on_node
        calculatePriority = lambda node: k8s.get_pods_number_on_node(node)

    schedulableNodes = []
    unschedulableNodes = []

    priority = []

    # Analyze nodes status and establish blocking priority
    for count in range(len(nodes)):
        if nodes[count].spec.unschedulable:
            unschedulableNodes.append(nodes[count])
        else:
            schedulableNodes.append(nodes[count])
        priority.append(
            (calculatePriority(nodes[count]), count))

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

    __updateNodes(k8s, toBlock, True)
    scale_logger.debug("%i nodes newly blocked" % len(toBlock))
    __updateNodes(k8s, toUnBlock, False)
    scale_logger.debug("%i nodes newly unblocked" % len(toUnBlock))

    return len(toBlock) - len(toUnBlock)
