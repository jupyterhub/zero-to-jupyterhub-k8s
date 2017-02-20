#!/usr/bin/python

"""Primary scale logic"""
from workload import scheduleGoal, getCriticalNodeNames, numPods
from utils import getNodes, getName, getClusterName, getNamespacesName, isUnschedulable
from update_nodes import updateUnschedulable
from gcloud_update import increaseNewGCloudNode, shutdownSpecifiedNode

import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

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


def resizeForNewNodes(newTotalNodes):
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
    allNodes = getNodes()
    logging.info("Scaling on cluster %s" % getClusterName(allNodes[0]))
    nodes = []  # a list of nodes that are NOT critical
    criticalNodeNames = getCriticalNodeNames()
    for each in allNodes:
        if getName(each) not in criticalNodeNames:
            nodes.append(each)
    goal = scheduleGoal()
    logging.info("Total nodes in the cluster: %i" % len(allNodes))
    logging.info("Found %i critical nodes; recommending additional %i nodes for service" % (
        (len(allNodes) - len(nodes),
         goal)
    ))

    updateUnschedulable(len(nodes) - goal, nodes)

    if len(criticalNodeNames) + goal > len(allNodes):
        logging.info("Resize the cluster to %i nodes to satisfy the demand" % (
            len(criticalNodeNames) + goal))
        resizeForNewNodes(len(criticalNodeNames) + goal)

    # CRITICAL NODES SHOULD NOT BE SHUTDOWN
    shutdownEmptyNodes(nodes)

if __name__ == "__main__":
    scale()
