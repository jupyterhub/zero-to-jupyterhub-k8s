#!/usr/bin/python3

"""Primary scale logic"""
from workload import schedule_goal
from update_nodes import update_unschedulable
from gcloud_update import increase_new_gcloud_node, shutdown_specified_node
from settings import settings

import logging
import argparse
from kubernetes_control import k8s_control

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s')

scale_logger = logging.getLogger("scale")

SERVICE_PROVIDER = "gcloud"


def shutdown_empty_nodes(nodes, k8s):
    """
    Search through all nodes and shut down those that are unschedulable
    and devoid of non-critical pods

    CRITICAL NODES SHOULD NEVER BE INCLUDED IN THE INPUT LIST
    """
    for node in nodes:
        if k8s.get_pods_number_on_node(node) == 0 and node.spec.unschedulable:
            scale_logger.info(
                "Shutting down empty node: %s" % node.metadata.name)
            shutdown_specified_node(node.metadata.name)


def resize_for_new_nodes(new_total_nodes, k8s):
    """create new nodes to match new_total_nodes required
    only for scaling up"""
    scale_logger.info("Using service provider: %s" % SERVICE_PROVIDER)
    if SERVICE_PROVIDER == "gcloud":
        increase_new_gcloud_node(
            new_total_nodes, k8s.get_cluster_name())


def scale(options):
    """Update the nodes property based on scaling policy
    and create new nodes if necessary"""
    k8s = k8s_control(options)
    scale_logger.info("Scaling on cluster %s" %
                      k8s.get_cluster_name())
    nodes = []  # a list of nodes that are NOT critical
    criticalNodeNames = k8s.get_critical_node_names()
    for node in k8s.nodes:
        if node.metadata.name not in criticalNodeNames:
            nodes.append(node)
    goal = schedule_goal(k8s)
    scale_logger.info("Total nodes in the cluster: %i" % len(k8s.nodes))
    scale_logger.info("Found %i critical nodes; recommending additional %i nodes for service" % (
        (len(k8s.nodes) - len(nodes),
         goal)
    ))

    update_unschedulable(len(nodes) - goal, nodes, k8s)

    if len(criticalNodeNames) + goal > len(k8s.nodes):
        scale_logger.info("Resize the cluster to %i nodes to satisfy the demand" % (
            len(criticalNodeNames) + goal))
        resize_for_new_nodes(len(criticalNodeNames) + goal, k8s)

    # CRITICAL NODES SHOULD NOT BE SHUTDOWN
    shutdown_empty_nodes(nodes, k8s)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", help="Show verbose output (debug)", action="store_true")

    args = parser.parse_args()
    if args.verbose:
        scale_logger.setLevel(logging.DEBUG)
    else:
        scale_logger.setLevel(logging.INFO)

    options = settings()
    scale(options)
