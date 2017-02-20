#!/usr/bin/python

"""Primary scale logic"""
from workload import scheduleGoal, getCriticalNodeNames, numPods
from utils import getNodes, getName, getClusterName, getNamespacesName, isUnschedulable
from update_nodes import updateUnschedulable
from gcloud_update import increaseNewGCloudNode, shutdownSpecifiedNode

import logging

SERVICE_PROVIDER = "gcloud"


def shutdownEmptyNodes(nodes):
    """
    Search through all nodes and shut down those that are unschedulable
    and devoid of non-critical pods

    CRITICAL NODES SHOULD NEVER BE INCLUDED IN THE INPUT LIST
    """
    for each in nodes:
        if numPods(each) == 0 and isUnschedulable(each):
            logging.info("Shutting down empty node: %s" % getName(each))
            shutdownSpecifiedNode(getName(each))


def createNewNodes(newTotalNodes):
    """create new nodes to match newTotalNodes required
    only for scaling up, no action taken if newTotalNodes
    is smaller than number of current nodes"""
    if newTotalNodes <= len(getNodes()):
        return
    logging.info("Using service provider: %s" % SERVICE_PROVIDER)
    if SERVICE_PROVIDER == "gcloud":
        increaseNewGCloudNode(
            newTotalNodes, getClusterName(), getNamespacesName())


def scale():
    """Update the nodes property based on scaling policy
    and create new nodes if necessary"""
    goal = scheduleGoal()
    nodes = []  # a list of nodes that are NOT critical
    criticalNodeNames = getCriticalNodeNames()
    allNodes = getNodes()
    for each in allNodes:
        if getName(each) not in criticalNodeNames:
            nodes.append(each)
    logging.info("Total nodes in the cluster: %i" % len(allNodes))
    logging.info("Found %i critical nodes; recommending additional %i nodes for service" % (
        (len(allNodes) - len(nodes),
         goal)
    ))

    updateUnschedulable(goal, nodes)

    if len(criticalNodeNames) + goal > len(allNodes):
        logging.info("Creating additional %i nodes to satisfy the demand" % (
            len(criticalNodeNames) + goal))
        createNewNodes(len(criticalNodeNames) + goal)

    # CRITICAL NODES SHOULD NOT BE SHUTDOWN
    shutdownEmptyNodes(nodes)
