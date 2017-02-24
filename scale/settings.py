#!/usr/bin/python3

""" Shared settings and constant values across multiple scaling scripts"""

import os


class settings:

    env_delimiter = ':'

    def __init__(self):
        """Set default value"""
        self.max_utilization = float(os.environ.get("MAX_UTILIZATION", 0.85))
        self.min_utilization = float(os.environ.get("MIN_UTILIZATION", 0.65))
        self.optimal_utilization = float(
            os.environ.get("OPTIMAL_UTILIZATION", 0.75))
        self.min_nodes = int(os.environ.get("MIN_NODES", 3))
        self.max_nodes = int(os.environ.get("MAX_NODES", 72))

        # FIXME: Replace with labels
        self.critical_pod_types = os.environ.get(
            "CRITICAL_POD_TYPES", "").split(self.env_delimiter)
        self.critical_namespaces = os.environ.get(
            "CRITICAL_NAMESPACES", "").split(self.env_delimiter)
        self.omit_pod_types = os.environ.get(
            "OMIT_POD_TYPES", "").split(self.env_delimiter)
        self.omit_namespaces = os.environ.get(
            "OMIT_NAMESPACES", "").split(self.env_delimiter)
        self.student_pod_type = os.environ.get(
            "STUDENT_POD_TYPE", "").split(self.env_delimiter)
