#!/usr/bin/python

""" Shared settings and constant values across multiple scaling scripts"""

# Constant context values used by Kubernetes
NAMESPACES = ['datahub', 'prob140', 'stat28']
CLUSTER = 'prod'
KUBECTL_CONTEXT = 'gke_data-8_us-central1-a_prod'

# Legacy scaling settings
USERS_PER_NODE = 7
POD_THRESHOLD = 0.9
BUMP_INCREMENT = 2

# New scaling settings #TODO: discuss with BIDS
CAPACITY_PER_NODE = USERS_PER_NODE #FIXME: should be determined dynamically
MIN_UTILIZATION = 0.65
MAX_UTILIZATION = 0.85
OPTIMAL_UTILIZATION = 0.75
MIN_NODES = 3
MAX_NODES = 72

# API Access Proxy provided by kubectl
API_HOST = "localhost"
API_PORT = "18080" 