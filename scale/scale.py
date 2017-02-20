#!/usr/bin/python

"""Primary scale logic"""
from workload import schedule_goal, get_critical_node_names, get_pods_number_on_node
from utils import get_nodes, get_name, get_cluster_name, get_namespaces_name, is_unschedulable
from update_nodes import updateUnschedulable
from gcloud_update import increase_new_gcloud_node, shutdown_specified_node

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)

SERVICE_PROVIDER = "gcloud"


def shutdown_empty_nodes(nodes):
    """
    Search through all nodes and shut down those that are unschedulable
    and devoid of non-critical pods

    CRITICAL NODES SHOULD NEVER BE INCLUDED IN THE INPUT LIST
    """
    for each in nodes:
        if get_pods_number_on_node(each) == 0 and is_unschedulable(each):
            logging.info("Shutting down empty node: %s" % get_name(each))
            shutdown_specified_node(get_name(each))


def resize_for_new_nodes(newTotalNodes):
    """create new nodes to match newTotalNodes required
    only for scaling up, no action taken if newTotalNodes
    is smaller than number of current nodes"""
    if newTotalNodes <= len(get_nodes()):
        return
    logging.info("Using service provider: %s" % SERVICE_PROVIDER)
    if SERVICE_PROVIDER == "gcloud":
        increase_new_gcloud_node(
            newTotalNodes, get_cluster_name(), get_namespaces_name())


def scale():
    """Update the nodes property based on scaling policy
    and create new nodes if necessary"""
    allNodes = get_nodes()
    logging.info("Scaling on cluster %s" % get_cluster_name(allNodes[0]))
    nodes = []  # a list of nodes that are NOT critical
    criticalNodeNames = get_critical_node_names()
    for each in allNodes:
        if get_name(each) not in criticalNodeNames:
            nodes.append(each)
    goal = schedule_goal()
    logging.info("Total nodes in the cluster: %i" % len(allNodes))
    logging.info("Found %i critical nodes; recommending additional %i nodes for service" % (
        (len(allNodes) - len(nodes),
         goal)
    ))

    updateUnschedulable(len(nodes) - goal, nodes)

    if len(criticalNodeNames) + goal > len(allNodes):
        logging.info("Resize the cluster to %i nodes to satisfy the demand" % (
            len(criticalNodeNames) + goal))
        resize_for_new_nodes(len(criticalNodeNames) + goal)

    # CRITICAL NODES SHOULD NOT BE SHUTDOWN
    shutdown_empty_nodes(nodes)

if __name__ == "__main__":
    scale()
