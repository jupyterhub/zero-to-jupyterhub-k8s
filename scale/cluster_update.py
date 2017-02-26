#!/usr/bin/python3

import subprocess
import logging

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

scale_logger = logging.getLogger("scale")


class cluster_control:

    """Abstracts cluster scaling logic. Currently will
    default and interact with the Data8 cluster using 
    GCE"""

    def __init__(self, options):
        """Needs to be initialized with options as an
        instance of settings"""
        self.options = options
        self.credentials = GoogleCredentials.get_application_default()
        self.compute = discovery.build('compute', 'v1', credentials=self.credentials)
        self.zone = options.zone
        self.group = options.manager
        self.project = options.project


    def shut_down_specified_node(self, name):
        request_body = {
            "instances" : [
                self.get_node_url_from_name(name)
            ]
        }

        scale_logger.debug("Shutting down node: %s", name)

        return self.compute.instanceGroupManagers().deleteInstances(
            instanceGroupManager=self.group,
            project=self.project,
            zone=self.zone,
            body=request_body).execute()


    def add_new_node(self, new_node_number, cluster_name):
        """ONLY FOR CREATING NEW NODES to ensure
        new _node_number is running

        NOT FOR SCALING DOWN: random behavior expected
        TODO: Assert check that new_node_number is larger
        than current cluster size"""
        # call gcloud command to start new nodes in GCE
        # FIXME: Use GCloud API calls instead
        scale_logger.debug("Resizing the cluster to %i nodes", new_node_number)
        cmd = ['gcloud', '--quiet', 'container', 'clusters', 'resize', cluster_name,
               '--size', str(new_node_number), '--zone', GCE_ZONE]
        print(' '.join(cmd))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
        buf = p.read()
        p.close()


    def list_managed_instances(self):
        """Lists the instances a part of the 
        specified cluster group"""
        scale_logger.debug("Gathering group: %s managed instances", self.group)
        result = self.compute.instanceGroupManagers().listManagedInstances(
            instanceGroupmanager=self.group,
            project=self.project,
            zone=self.zone).execute()
        return result['managedInstances']


    def get_node_url_from_name(self, name):
        """Gets the URL associated with the node name
        TODO: Error handling for invalid names"""
        node_url = ''
        instances = self.list_managed_instances()
        for instance_url in instances['instance']:
            if name in instance_url:
                node_url = instance_url
                break
        scale_logger.debug("Node: %s has URL of: %s", name, node_url)
        return node_url