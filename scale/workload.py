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
            "Current memory usage is %f", k8s.get_total_cluster_memory_usage())
        scale_logger.debug(
            "Total memory capacity is %f", k8s.get_total_cluster_memory_capacity())
        return k8s.get_total_cluster_memory_usage() / k8s.get_total_cluster_memory_capacity()
    except ZeroDivisionError:
        return float("inf")


def schedule_goal(k8s):
    """Return the goal number of schedulable nodes IN ADDITION
    TO CRITICAL NODES, given the current situation"""
    scale_logger.info("Current scheduling target: %f ~ %f",
                      k8s.options.min_utilization, k8s.options.max_utilization)
    currentUtilization = get_effective_utilization(k8s)
    scale_logger.info("Current workload is %f", currentUtilization)
    if currentUtilization >= k8s.options.min_utilization and currentUtilization <= k8s.options.max_utilization:
        # leave unchanged
        return k8s.get_num_schedulable()
    else:
        # need to scale down
        requiredNum = k8s.get_total_cluster_memory_usage(
        ) / k8s.options.optimal_utilization / get_node_memory_capacity(k8s.nodes[0])
        if requiredNum < k8s.options.min_nodes - k8s.critical_node_number:
            requiredNum = k8s.options.min_nodes - k8s.critical_node_number
        if requiredNum > k8s.options.max_nodes - k8s.critical_node_number:
            requiredNum = k8s.options.max_nodes - k8s.critical_node_number
        return int(round(requiredNum))
