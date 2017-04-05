#!/usr/bin/python3

"""Provide functions to analyze current workload status of the cluster.

All functions in the file should be read-only and cause no side effects."""

import logging

from utils import get_node_memory_capacity
scale_logger = logging.getLogger("scale")


def get_effective_utilization(k8s):
    """Return effective workload in the given list of nodes"""
    try:
        scale_logger.debug(
            "Current memory usage is %i", k8s.get_total_cluster_memory_usage())
        scale_logger.debug(
            "Total memory capacity is %i", k8s.get_total_cluster_memory_capacity())
        utilization_percentage = k8s.get_total_cluster_memory_usage(
        ) / k8s.get_total_cluster_memory_capacity()
        return utilization_percentage
    except ZeroDivisionError:
        return float("inf")


def schedule_goal(k8s, options):
    """Return the goal number of schedulable nodes, including nodes running
    critical pods, given the current situation"""
    scale_logger.info("Current scheduling target: %f ~ %f",
                      k8s.options.min_utilization, k8s.options.max_utilization)

    current_utilization = get_effective_utilization(k8s)
    scale_logger.info("Current cluster utilization is %f", current_utilization)

    if current_utilization >= options.min_utilization and current_utilization <= options.max_utilization:
        # leave unchanged
        return len(k8s.nodes) - k8s.get_num_unschedulable
    else:
        # need to scale down or up
        required_num = k8s.get_total_cluster_memory_usage(
        ) / options.optimal_utilization / get_node_memory_capacity(k8s.nodes[0])

        minimum_nodes = options.min_nodes
        maximum_nodes = options.max_nodes
        # Ensure that newClusterSize remains within the bounds of min and max
        # nodes
        newClusterSize = minimum_nodes if required_num < minimum_nodes else required_num
        newClusterSize = maximum_nodes if required_num > maximum_nodes else required_num
        return int(round(newClusterSize))
