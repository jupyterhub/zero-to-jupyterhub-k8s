#!/usr/bin/python

""" Shared settings and constant values across multiple scaling scripts"""

# Constant context values used by Kubernetes
NAMESPACES = ['datahub', 'prob140', 'stat28']
CLUSTER = 'prod'
KUBECTL_CONTEXT = 'gke_data-8_us-central1-a_prod'

# Scaling settings
USERS_PER_NODE = 7
POD_THRESHOLD = 0.9
BUMP_INCREMENT = 2

# API Access Proxy provided by kubectl
API_HOST = "localhost"
API_PORT = "18080" 