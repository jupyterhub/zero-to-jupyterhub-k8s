#!/usr/bin/python

""" Shared settings and constant values across multiple scaling scripts"""

# Deprecated constant context values used by Kubernetes
# NAMESPACES = ['datahub', 'prob140', 'stat28']
# CLUSTER = 'prod'
# KUBECTL_CONTEXT = 'gke_data-8_us-central1-a_prod'
GCLOUD_INSTANCE_GROUP = 'gke-dev-default-pool-dbd2a02e-grp'
GCE_ZONE = "us-central1-a"

# Legacy scaling settings
#USERS_PER_NODE = 7
#POD_THRESHOLD = 0.9
#BUMP_INCREMENT = 2

# New scaling settings #TODO: discuss with BIDS
CAPACITY_PER_NODE = USERS_PER_NODE  # FIXME: should be determined dynamically
MIN_UTILIZATION = 0.65
MAX_UTILIZATION = 0.85
OPTIMAL_UTILIZATION = 0.75
MIN_NODES = 3
MAX_NODES = 72

CRITICAL_POD_TYPES = ["hub", "proxy", "statsd"]
CRITICAL_NAMESPACES = []
OMIT_POD_TYPES = ["cull"]
OMIT_NAMESPACES = ["kube-system", "default"]

# API Access Proxy provided by kubectl
# Context switch is determined by the kubectl proxy
# Need a kubectl proxy running at http://API_HOST:API_PORT/
# See https://kubernetes.io/docs/user-guide/kubectl/kubectl_proxy/
API_HOST = "localhost"
API_PORT = "18080"
