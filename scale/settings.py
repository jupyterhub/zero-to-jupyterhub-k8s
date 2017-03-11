#!/usr/bin/python3

""" Shared settings and constant values across multiple scaling scripts"""

import os
import logging
import sys


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

        # TODO: Get rid of these default values specific to Data8
        self.zone = os.environ.get("ZONE", "us-central1-a")
        self.project = os.environ.get("PROJECT", "92948014362")

        self.preemptible_labels = os.environ.get(
            "PREEMPTIBLE_LABELS", "").split(self.env_delimiter)
        self.omit_labels = os.environ.get(
            "OMIT_LABELS", "").split(self.env_delimiter)
        self.omit_namespaces = os.environ.get(
            "OMIT_NAMESPACES", "kube-system").split(self.env_delimiter)

        self.test_cloud = True
        self.test_k8s = True
        self.yes = False

        self.context = ""
        self.context_cloud = ""

        # only used for debugging
        self.default_context = os.environ.get("DEFAULT_CONTEXT", "dev")
