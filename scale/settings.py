#!/usr/bin/python3

""" Shared settings and constant values across multiple scaling scripts"""

import os

# Legacy scaling settings
USERS_PER_NODE = 7

# New scaling settings #TODO: discuss with BIDS
CAPACITY_PER_NODE = USERS_PER_NODE  # FIXME: should be determined dynamically


class settings:

    env_delimiter = ':'

    def __init__(self):
        """Set default value"""
        self.max_utilization = 0.85
        self.min_utilization = 0.65
        self.optimal_utilization = 0.75
        self.min_nodes = 3
        self.max_nodes = 72
        self.critical_pod_types = ["hub", "proxy"]
        self.critical_namespaces = []
        self.omit_pod_types = ["cull", "statsd"]
        self.omit_namespaces = ["kube-system", "default"]
        self.student_pod_identifier = "jupyter"
        self.load_env()

    def load_env(self):
        """Load settings from os.env"""
        if "MIN_UTILIZATION" in os.environ:
            self.min_utilization = float(os.environ["MIN_UTILIZATION"])
        if "MAX_UTILIZATION" in os.environ:
            self.max_utilization = float(os.environ["MAX_UTILIZATION"])
        if "OPTIMAL_UTILIZATION" in os.environ:
            self.optimal_utilization = float(os.environ["OPTIMAL_UTILIZATION"])
        if "MIN_NODES" in os.environ:
            self.min_nodes = int(os.environ["MIN_NODES"])
        if "MAX_NODES" in os.environ:
            self.max_nodes = int(os.environ["MAX_NODES"])
        if "CRITICAL_POD_TYPES" in os.environ:
            self.critical_pod_types = os.environ[
                "CRITICAL_POD_TYPES"].split(self.env_delimiter)
        if "CRITICAL_NAMESPACES" in os.environ:
            self.critical_namespaces = os.environ[
                "CRITICAL_NAMESPACES"].split(self.env_delimiter)
        if "OMIT_POD_TYPES" in os.environ:
            self.omit_pod_types = os.environ[
                "OMIT_POD_TYPES"].split(self.env_delimiter)
        if "OMIT_NAMESPACES" in os.environ:
            self.omit_namespaces = os.environ[
                "OMIT_NAMESPACES"].split(self.env_delimiter)
        if "STUDENT_POD_IDENTIFIER" in os.environ:
            self.student_pod_identifier = os.environ[
                 "STUDENT_POD_IDENTIFIER"]

