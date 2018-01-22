.. _turn-off:

Turning Off JupyterHub and Computational Resources
==================================================

When you are done with your hub, you should delete it so you are no longer
paying money for it. The following sections describe how to delete your
JupyterHub resources on various cloud providers.

Tearing down your JupyterHub entails:

1. Deleting your Kubernetes namespace, which deletes all objects created and managed by Kubernetes
2. Deleting any computational resources you've requested from the cloud provider
3. Running a final check to make sure there aren't any lingering resources that haven't been deleted
   (e.g., storage volumes in some cloud providers)

For all cloud providers
-----------------------

.. _delete-namespace:

Delete the helm namespace
~~~~~~~~~~~~~~~~~~~~~~~~~

The steps in this section must be performed for all cloud providers first,
before doing the cloud provider specific setup.

1. First, delete the helm release. This deletes all resources that were created
   by helm to make your jupyterhub.

  .. code-block:: bash

     helm delete <your-helm-release-name> --purge

2. Next, delete the namespace the hub was installed in. This deletes any disks
   that may have been created to store user's data, and any IP addresses that
   may have been provisioned.

   .. code-block:: bash

      kubectl delete namespace <your-namespace>

Google Cloud Platform
---------------------

1. Perform the steps in :ref:`delete-namespace`. These cloud provider agnostic steps will
   delete the helm chart and delete the hub's namespace. This must be done before proceeding.

2. Delete the kubernetes cluster. You can list all the clusters you have.

   .. code-block:: bash

      gcloud container clusters list

   You can then delete the one you want.

   .. code-block:: bash

      gcloud container clusters delete <CLUSTER-NAME> --zone=<CLUSTER-ZONE>

3. Double check to make sure all the resources are now deleted, since anything you
   have not deleted will cost you money! You can check the `web console <https://console.cloud.google.com>`_
   (make sure you are in the right project and account) to verify that everything
   has been deleted.

   At a minimum, check the following under the Hamburger (left top corner) menu:

   1. Compute Engine -> Disks
   2. Container Engine -> Container Clusters
   3. Container Registry -> Images
   4. Networking -> Network Services -> Load Balancing

   These might take several minutes to clear up, but they shouldn't have anything
   related to your JupyterHub cluster after you have deleted the cluster.

Microsoft Azure AKS
-------------------

1. Perform the steps in :ref:`delete-namespace`. These cloud provider agnostic steps will
   delete the helm chart and delete the hub's namespace. This must be done before proceeding.

2. Delete your resource group. You can list your active resource groups with
   the following command

   .. code-block:: bash

      az aks list --output table

   You can then delete the one you want with the following command

   .. code-block:: bash

      az group delete -n <YOUR-GROUP-NAME>

3. Double check to make sure all the resources are now deleted, since anything you
   have not deleted will cost you money! You can check the `web portal <https://portal.azure.com>`_
   (check the "Resource Groups" page) to verify that everything has been deleted.

   These might take several minutes to clear up, but they shouldn't have anything
   related to your JupyterHub cluster after you have deleted the cluster.

Amazon Web Services (AWS)
-------------------------

1. Perform the steps in :ref:`delete-namespace`. These cloud provider agnostic steps will
   delete the helm chart and delete the hub's namespace. This must be done before proceeding.

2. The easiest way to delete your cloud resources on AWS is to use their
   website. Go to the ``CloudFormation`` page. This should have a list of all
   running AWS stacks that you've created.

   If you followed the JupyterHub guide, there should be two items, both containing the name
   that you chose for this stack. For each item, click the checkbox next to it. Then, click
   ``Actions`` and finally ``Delete Stack``. Answer "yes" to any confirmation dialogues, and
   this should begin the process of deleting your Kubernetes cluster.

.. note::

   Sometimes AWS fails to delete parts of the stack on a first pass. Be sure
   to double-check that your stack has in fact been deleted, and re-perform
   the actions above if needed.
