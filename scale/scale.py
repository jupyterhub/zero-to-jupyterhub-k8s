#!/usr/bin/python3

"""Primary scale logic"""

import logging
import argparse

from workload import schedule_goal
from update_nodes import update_unschedulable
from cluster_update import gce_cluster_control
from settings import settings
from utils import user_confirm
from kubernetes_control import k8s_control
from kubernetes_control_test import k8s_control_test

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s')
scale_logger = logging.getLogger("scale")


def shutdown_empty_nodes(nodes, k8s, cluster, test=False):
    """
    Search through all nodes and shut down those that are unschedulable
    and devoid of non-critical pods

    CRITICAL NODES SHOULD NEVER BE INCLUDED IN THE INPUT LIST
    """
    for node in nodes:
        if k8s.get_pods_number_on_node(node) == 0 and node.spec.unschedulable:
            if confirm(("Shutting down empty node: %s" % node.metadata.name)):
                scale_logger.info(
                    "Shutting down empty node: %s", node.metadata.name)
                if not test:
                    cluster.shutdown_specified_node(node.metadata.name)


def shutdown_empty_nodes_test(nodes, k8s, cluster):
    shutdown_empty_nodes(nodes, k8s, cluster, True)


def resize_for_new_nodes(new_total_nodes, k8s, cluster, test=False):
    """create new nodes to match new_total_nodes required
    only for scaling up"""
    if confirm(("Resizing up to: %d nodes" % new_total_nodes)):
        scale_logger.info("Resizing up to: %d nodes", new_total_nodes)
        if not test:
            cluster.add_new_node(new_total_nodes)


def resize_for_new_nodes_test(new_total_nodes, k8s, cluster):
    resize_for_new_nodes(new_total_nodes, k8s, cluster, True)


def scale(options):
    """Update the nodes property based on scaling policy
    and create new nodes if necessary"""

    # ONLY GCE is supported for scaling at this time
    cluster = gce_cluster_control(options)
    if options.test_k8s:
        k8s = k8s_control_test(options)
    else:
        k8s = k8s_control(options)

    scale_logger.info("Scaling on cluster %s", k8s.get_cluster_name())

    nodes = []  # a list of nodes that are NOT critical
    for node in k8s.nodes:
        if node.metadata.name not in k8s.critical_node_names:
            nodes.append(node)

    # goal is the total number of nodes we want in the cluster
    goal = schedule_goal(k8s, options)

    scale_logger.info("Total nodes in the cluster: %i", len(k8s.nodes))
    scale_logger.info(
        "%i nodes are unschedulable at this time", k8s.get_num_schedulable)
    scale_logger.info("Found %i critical nodes",
                      len(k8s.nodes) - len(nodes))
    scale_logger.info("Recommending total %i nodes for service", goal)

    if confirm(("Updating unschedulable flags to ensure %i nodes are unschedulable" % max(len(k8s.nodes) - goal, 0))):
        update_unschedulable(max(len(k8s.nodes) - goal, 0), nodes, k8s)

    if goal > len(k8s.nodes):
        scale_logger.info(
            "Resize the cluster to %i nodes to satisfy the demand", goal)
        if options.test_cloud:
            resize_for_new_nodes_test(goal, k8s, cluster)
        else:
            resize_for_new_nodes(goal, k8s, cluster)
    if options.test_cloud:
        shutdown_empty_nodes_test(nodes, k8s, cluster)
    else:
        # CRITICAL NODES SHOULD NOT BE SHUTDOWN
        shutdown_empty_nodes(nodes, k8s, cluster)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", help="Show verbose output (debug)", action="store_true")
    parser.add_argument(
        "-T", "--test", help="Run the script in TEST mode, log expected behavior, no real action will be taken", action="store_true")
    parser.add_argument(
        "--test-k8s", help="Run the script to test kubernetes actions: log expected commands to kubernetes, no real action on node specs", action="store_true")
    parser.add_argument(
        "--test-cloud", help="Run the script to test cloud actions: log expected commands to the cloud provider, no real action on actual VM pool", action="store_true")
    parser.add_argument(
        "-y", help="Run the script without user interactive confirmation", action="store_true")
    parser.add_argument(
        "-c", "--context", required=True, help="A unique segment in the context name to specify which to use to instantiate Kubernetes")
    parser.add_argument(
        "--context-for-cloud", help="An optional different unique segment in the managed pool name to specify which to use to when resizing cloud managed pools", default="")
    args = parser.parse_args()
    if args.verbose:
        scale_logger.setLevel(logging.DEBUG)
    else:
        scale_logger.setLevel(logging.INFO)

    # Retrieve settings from the environment
    options = settings()

    if args.test:
        scale_logger.warning(
            "Running in test mode, no action will actually be taken")
    else:
        options.test_k8s = False
        options.test_cloud = False
        if args.test_cloud:
            options.test_cloud = True
            scale_logger.warning(
                "Running in test cloud mode, no action on VM pool")
        if args.test_k8s:
            options.test_k8s = True
            scale_logger.warning(
                "Running in test kubernetes mode, no action on node specs")

    if args.y:
        confirm = lambda x, y=False: True
    else:
        confirm = user_confirm

    options.context = args.context
    if args.context_for_cloud != "":
        options.context_cloud = args.context_for_cloud
    else:
        options.context_cloud = options.context

    scale(options)
