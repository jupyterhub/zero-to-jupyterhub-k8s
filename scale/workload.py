#!/usr/bin/python3

"""Provide functions to analyze current workload status of the cluster.

All functions in the file should be read-only and cause no side effects."""

from utils import get_nodes, get_pods, \
    get_pod_type, get_pod_host_name
from settings import CAPACITY_PER_NODE
import logging
scale_logger = logging.getLogger("scale")


def get_pods_number_on_node(node, options, pods=None):
    """Return the effective number of noncritical
    pods on the node"""
    if pods == None:
        pods = get_pods()
    result = 0
    for pod in pods:
        if not(pod.metadata.namespace in options.omit_namespaces or
               pod.metadata.namespace in options.critical_namespaces or
               get_pod_type(pod) in options.omit_pod_types or
               get_pod_type(pod) in options.critical_pod_types
               ) and get_pod_host_name(pod) == node.metadata.name:
            result += 1
    return result

def get_critical_node_names(options, pods=None):
    """Return a list of nodes where critical pods
    are running"""
    if pods == None:
        pods = get_pods()
    result = []
    for pod in pods:
        if pod.metadata.namespace in options.critical_namespaces or get_pod_type(pod) in options.critical_pod_types:
            if get_pod_host_name(pod) not in result:
                result.append(get_pod_host_name(pod))
    return result


def get_workload(node, pods=None):
    """Return the workload on the given node"""
    if pods == None:
        pods = get_pods()
    return get_pods_number_on_node(node, pods)


def get_sum_workload(nodes):
    """Return the total workload on
    the given list of nodes"""
    pods = get_pods()
    total = 0
    for node in nodes:
        total += get_workload(node, pods)
    return total


def get_node_memory_capacity(node):
    """Converts the specific memory entry 
    of the kubernetes API into the byte capacity"""
    node_mem_in_kibibytes = int(node.status.capacity['memory'].replace('Ki', ''))
    node_mem_in_bytes = 1024 * node_mem_in_kibibytes
    return node_mem_in_bytes


def get_total_cluster_memory_usage(options, pods=None):
    """Gets the total memory usage of 
    all student pods"""
    if pods == None:
        pods = get_pods()
    student_pods = list(filter(lambda pod: pod.metadata.name.startswith(options.student_pod_identifier), pods))
    total_mem_usage = 0
    for pod in student_pods:
        total_mem_usage += int(pod.spec.containers[0].resrouces.requests['memory'])
    return total_mem_usage


def get_total_cluster_memory_capacity(nodes=None):
    """Returns the total memory capacity of all nodes, as student
    pods can be scheduled on any node that meets its Request criteria"""
    if nodes == None:
        nodes = get_nodes()
    total_mem_capacity = 0
    for node in nodes:
        total_mem_capacity += get_node_memory_capacity(node)
    return total_mem_capacity


def get_capacity(node):
    """Return the workload capacity of the 
    given node"""
    # FIXME: not adjusted to different machine types
    return CAPACITY_PER_NODE


def get_num_schedulable(nodes, criticalNodeNames):
    """Return number of nodes schedulable AND NOT
    IN THE LIST OF CRITICAL NODES"""
    result = 0
    for node in nodes:
        if (not node.spec.unschedulable) and node.metadata.name not in criticalNodeNames:
            result += 1
    return result


def get_num_unschedulable(nodes):
    """Return number of nodes unschedulable

    ASSUMING CRITICAL NODES ARE SCHEDULABLE"""
    result = 0
    for node in nodes:
        if node.spec.unschedulable:
            result += 1
    return result


def get_effective_workload(options, nodes, criticalNodeNames):
    """Return effective workload in the given list of nodes"""
    try:
        return get_total_cluster_memory_usage(options) / get_total_cluster_memory_capacity(nodes)
    except ZeroDivisionError:
        return float("inf")


def schedule_goal(options):
    """Return the goal number of schedulable nodes IN ADDITION
    TO CRITICAL NODES, given the current situation"""
    nodes = get_nodes()
    scale_logger.info("Current scheduling target: %f ~ %f" %
                      (options.min_utilization, options.max_utilization))
    criticalNodeNames = get_critical_node_names(get_pods())
    currentUtilization = get_effective_workload(
        options, nodes, criticalNodeNames) / get_capacity(nodes[0])
    scale_logger.info("Current workload is %f" % currentUtilization)
    if currentUtilization >= options.min_utilization and currentUtilization <= options.max_utilization:
        # leave unchanged
        return get_num_schedulable(nodes, criticalNodeNames)
    else:
        # need to scale down
        requiredNum = get_sum_workload(
            nodes) / options.optimal_utilization / get_capacity(nodes[0])
        if requiredNum < options.min_nodes - len(criticalNodeNames):
            requiredNum = options.min_nodes - len(criticalNodeNames)
        if requiredNum > options.max_nodes - len(criticalNodeNames):
            requiredNum = options.max_nodes - len(criticalNodeNames)
        return int(round(requiredNum))
