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
            "Total memory capacity is %f", k8s.get_total_cluster_memory_capacity())
        utilization_percentage = k8s.get_total_cluster_memory_usage() / k8s.get_total_cluster_memory_capacity()
        return utilization_percentage
    except ZeroDivisionError:
        return float("inf")


def schedule_goal(k8s, options):
    """Return the goal number of schedulable nodes IN ADDITION
    TO CRITICAL NODES, given the current situation"""
    scale_logger.info("Current scheduling target: %f ~ %f",
                      k8s.options.min_utilization, k8s.options.max_utilization)

    current_utilization = get_effective_utilization(k8s)
    scale_logger.info("Current workload is %f", current_utilization)

    if current_utilization >= options.min_utilization and current_utilization <= options.max_utilization:
        # leave unchanged
        return k8s.get_num_schedulable()
    else:
        # need to scale down
        requiredNum = k8s.get_total_cluster_memory_usage(
        ) / options.optimal_utilization / get_node_memory_capacity(k8s.nodes[0])

        # TODO: Can this be nonnegative
        min_noncritical_nodes = options.min_nodes - k8s.critical_node_number
        max_noncritical_nodes = options.max_nodes - k8s.critical_node_number
        # Ensure that newClusterSize remains within the bounds of min and max nodes
        newClusterSize = min_noncritical_nodes if requiredNum < min_noncritical_nodes else requiredNum
        newClusterSize = max_noncritical_nodes if requiredNum > max_noncritical_nodes else requiredNum
        return int(round(newClusterSize))
