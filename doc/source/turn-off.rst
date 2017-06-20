.. _turn-off:

Turning Off JupyterHub and Computational Resources
==================================================

When you are done with your hub, you should delete it so you are no longer
paying money for it.

1. First, delete the namespace the hub was installed in. This deletes any disks
   that may have been created to store user's data, and any IP addresses that
   may have been provisioned.

   .. code-block::

      kubectl delete namespace <your-namespace>

2. Next, you should delete the kubernetes cluster. You can list all the clusters
   you have.

   .. code-block::

      gcloud container clusters list

   You can then delete the one you want.

   .. code-block::

      gcloud container clusters delete <CLUSTER-NAME> --zone=<CLUSTER-ZONE>

3. Double check to make sure all the resources are now deleted, since anything you
   have not deleted will cost you money! You can check the `web console <https://console.cloud.google.com>`_
   (make sure you are in the right project and account!) to make sure everything
   has been deleted.
