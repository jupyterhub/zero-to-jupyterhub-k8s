#!/usr/bin/python3

import subprocess
import logging
scale_logger = logging.getLogger("scale")

GCLOUD_INSTANCE_GROUP = 'gke-dev-default-pool-dbd2a02e-grp'
GCE_ZONE = "us-central1-a"


def shutdown_specified_node(name):
    """Deletes the specified node by calling the Google Cloud Engine"""

    cmd = ['gcloud', 'compute', 'instance-groups', 'managed', 'delete-instances',
           GCLOUD_INSTANCE_GROUP, '--instances=' + name]
    p = subprocess.Popen(' '.join(cmd), stdout=subprocess.PIPE)
    output, err = p.communicate()
    if err:
        scale_logger.error("Cannot shutdown node %s" % name)


def increase_new_gcloud_node(new_node_number, cluster_name):
    """ONLY FOR CREATING NEW NODES to ensure 
    new _node_number is running

    NOT FOR SCALING DOWN: random behavior 
    expected"""

    # call gcloud command to start new nodes in GCE
    # FIXME: Use GCloud API calls instead
    scale_logger.info("Resizing the cluster to %i nodes" % new_node_number)
    cmd = ['gcloud', '--quiet', 'container', 'clusters', 'resize', cluster_name,
           '--size', str(new_node_number), '--zone', GCE_ZONE]
    print(' '.join(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    buf = p.read()
    p.close()
