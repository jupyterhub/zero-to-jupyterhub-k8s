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

        self.preemptible_labels = os.environ.get(
            "PREEMPTIBLE_LABELS", "").split(self.env_delimiter)
        self.omit_labels = os.environ.get(
            "OMIT_LABELS", "").split(self.env_delimiter)
        self.omit_namespaces = os.environ.get(
            "OMIT_NAMESPACES", "kube-system").split(self.env_delimiter)
