#!/usr/bin/python3

"""Provide functions to analyze current workload status of the cluster.

All functions in the file should be read-only and cause no side effects."""

from utils import get_nodes, is_unschedulable, get_pods, get_pod_namespace, \
    get_pod_type, get_pod_host_name, get_name
from settings import CAPACITY_PER_NODE, MIN_NODES, MAX_NODES, MAX_UTILIZATION, MIN_UTILIZATION, OPTIMAL_UTILIZATION
from settings import OMIT_NAMESPACES, CRITICAL_POD_TYPES, OMIT_POD_TYPES, CRITICAL_NAMESPACES

import logging


def get_pods_number_on_node(node, pods=get_pods()):
    """Return the effective number of noncritical
    pods on the node"""
    result = 0
    for each in pods:
        if not(get_pod_namespace(each) in OMIT_NAMESPACES or
               get_pod_namespace(each) in CRITICAL_NAMESPACES or
               get_pod_type(each) in OMIT_POD_TYPES or
               get_pod_type(each) in CRITICAL_POD_TYPES
               ) and get_pod_host_name(each) == get_name(node):
            result += 1
    return result


def get_critical_node_names(pods=get_pods()):
    """Return a list of nodes where critical pods
    are running"""
    result = []
    for each in pods:
        if get_pod_namespace(each) in CRITICAL_NAMESPACES or get_pod_type(each) in CRITICAL_POD_TYPES:
            if get_pod_host_name(each) not in result:
                result.append(get_pod_host_name(each))
    return result


def get_workload(node, pods=get_pods()):
    """Return the workload on the given node"""
    return get_pods_number_on_node(node, pods)


def get_sum_workload(nodes):
    """Return the total workload on
    the given list of nodes"""
    pods = get_pods()
    total = 0
    for each in nodes:
        total += get_workload(each, pods)
    return total


def get_capacity(node):
    """Return the workload capacity of the 
    given node"""
    # FIXME: not adjusted to different machine types
    return CAPACITY_PER_NODE


def get_num_schedulable(nodes, criticalNodeNames):
    """Return number of nodes schedulable AND NOT
    IN THE LIST OF CRITICAL NODES"""
    result = 0
    for each in nodes:
        if (not is_unschedulable(each)) and get_name(each) not in criticalNodeNames:
            result += 1
    return result


def get_num_unschedulable(nodes):
    """Return number of nodes unschedulable

    ASSUMING CRITICAL NODES ARE SCHEDULABLE"""
    result = 0
    for each in nodes:
        if is_unschedulable(each):
            result += 1
    return result


def get_effective_workload(nodes, criticalNodeNames):
    """Return effective workload in the given list of nodes"""
    try:
        return get_sum_workload(nodes) / get_num_schedulable(nodes, criticalNodeNames)
    except ZeroDivisionError:
        return float("inf")


def schedule_goal():
    """Return the goal number of schedulable nodes IN ADDITION
    TO CRITICAL NODES, given the current situation"""
    nodes = get_nodes()
    logging.info("Current scheduling target: %f ~ %f" %
                 (MIN_UTILIZATION, MAX_UTILIZATION))
    criticalNodeNames = get_critical_node_names(get_pods())
    currentUtilization = get_effective_workload(
        nodes, criticalNodeNames) / get_capacity(nodes[0])
    logging.info("Current workload is %f" % currentUtilization)
    if currentUtilization >= MIN_UTILIZATION and currentUtilization <= MAX_UTILIZATION:
        # leave unchanged
        return get_num_schedulable(nodes, criticalNodeNames)
    else:
        # need to scale down
        requiredNum = get_sum_workload(
            nodes) / OPTIMAL_UTILIZATION / get_capacity(nodes[0])
        if requiredNum < MIN_NODES - len(criticalNodeNames):
            requiredNum = MIN_NODES - len(criticalNodeNames)
        if requiredNum > MAX_NODES - len(criticalNodeNames):
            requiredNum = MAX_NODES - len(criticalNodeNames)
        return int(round(requiredNum))
