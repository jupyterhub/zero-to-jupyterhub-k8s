.. _turn-off:

Turning Off JupyterHub and Computational Resources
==================================================

When you are done with your hub, you should delete it so you are no longer
paying money for it. The following sections describe how to delete your
JupyterHub resources on various cloud providers.

For all cloud providers
-----------------------

The steps in this section must be performed for all cloud providers first,
before doing the cloud provider specific setup.

1. First, delete the helm release. This deletes all resources that were created
   by helm to make your jupyterhub.

  .. code-block:: bash

     helm delete <your-helm-release-name> --purge

2. First, delete the namespace the hub was installed in. This deletes any disks
   that may have been created to store user's data, and any IP addresses that
   may have been provisioned.

   .. code-block:: bash

      kubectl delete namespace <your-namespace>

Google Cloud Engine
-------------------

Make sure you have performed the cloud provider agnostic steps listed above before
doing this!

1. You should delete the kubernetes cluster. You can list all the clusters
   you have.

   .. code-block:: bash

      gcloud container clusters list

   You can then delete the one you want.

   .. code-block:: bash

      gcloud container clusters delete <CLUSTER-NAME> --zone=<CLUSTER-ZONE>

2. Double check to make sure all the resources are now deleted, since anything you
   have not deleted will cost you money! You can check the `web console <https://console.cloud.google.com>`_
   (make sure you are in the right project and account!) to make sure everything
   has been deleted.

   At a minimum, check the following under the Hamburger (left top corner) menu:

   1. Compute Engine -> Disks
   2. Container Engine
   3. Networking -> Load Balancing

   These might take several minutes to clear up, but they shouldn't have anything
   related to your JupyterHub cluster after you have deleted the cluster.

Amazon AWS
----------

Make sure you have performed the cloud provider agnostic steps listed above before
doing this!

The easiest way to delete your cloud resources on AWS is to use their
website. Go to the ``CloudFormation`` page. This should have a list of all
running AWS stacks that you've created.

If you followed the JupyterHub guide,
there should be two items, both containing the name that you chose for this
stack. For each item, click the checkbox next to it. Then, click ``Actions``
and finally ``Delete Stack``. Answer "yes" to any confirmation dialogues, and
this should begin the process of deleting your Kubernetes cluster.

.. note::

   Sometimes AWS fails to delete parts of the stack on a first pass. Be sure
   to double-check that your stack has in fact been deleted, and re-perform
   the actions above if needed.
