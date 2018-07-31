.. _google-cloud:

Step Zero: Kubernetes on `Google Cloud <https://cloud.google.com/>`_ (GKE)
--------------------------------------------------------------------------

`Google Kubernetes Engine <https://cloud.google.com/kubernetes-engine/>`_
(GKE) is the simplest and most common way of setting
up a Kubernetes Cluster. You may be able to receive `free credits
<https://cloud.google.com/free/>`_ for trying it out (though note that a
free account `comes with limitations
<https://cloud.google.com/free/docs/frequently-asked-questions#limitations>`_).
Either way, you will need to connect your credit card or other payment method to
your google cloud account.

1. Go to `console.cloud.google.com <https://console.cloud.google.com>`_ and log in.

   .. note::

      Consider `setting a cloud budget <https://cloud.google.com/billing/docs/how-to/budgets>`_
      for your Google Cloud account in order to make sure you don't accidentally
      spend more than you wish to.

2. Go to and enable the `Kubernetes Engine API <https://console.cloud.google.com/apis/api/container.googleapis.com/overview>`_.

3. Choose a terminal.

   You can either to use a web based terminal or install and run the required
   command line interfaces on your own computer's terminal. We recommend
   starting out by using the web based terminal. Choose one set of instructions
   below.

   a. **Use a web based terminal:**
   
      Start the Google Cloud Shell by clicking the button shown below. This will
      start an interactive shell session within Google Cloud.

      .. image:: ../_static/images/google/start_interactive_cli.png
         :align: center

      See the `Google Cloud Shell documentation <https://cloud.google.com/shell/docs/>`_
      for more information.

   b. **Use your own computer's terminal:**

      1. Download and install the `gcloud` command line tool at its `downloads
         page <https://cloud.google.com/sdk/downloads>`_. It will help you
         create and communicate with a Kubernetes cluster.

      2. Install ``kubectl`` (reads *kube control*), it is a tool for controlling
         Kubernetes clusters in general. From your terminal, enter:

         .. code-block:: bash

            gcloud components install kubectl

4. Decide and configure to use a specific data center.

   From a terminal, enter:

   .. code-block:: bash

      gcloud config set compute/zone <YOUR-ZONE>
   
   * ``<YOUR-ZONE>`` specifies which data center to use. Pick something `from
     this list <https://cloud.google.com/compute/docs/regions-zones/regions-zones#available>`_.
     that is not too far away from your users and has the hardware you want to
     utilize. Note that only some zones has GPUs.

5. Create a managed Kubernetes cluster and a default node pool.
  
   A single node from the default node pool created below will be responsible
   for running the essential pods of the JupyterHub chart. We recommend choosing
   a cheap machine type like `n1-standard-1` initially and upgrading it at a
   later stage if it is found to be overburdened.

   See the `node pool documentation
   <https://cloud.google.com/kubernetes-engine/docs/concepts/node-pools>`_ for
   more information.

   .. code-block:: bash

      gcloud beta container clusters create <YOUR-CLUSTER-NAME> \
        --machine-type n1-standard-1 \
        --num-nodes 1 \
        --cluster-version latest \
        --node-labels hub.jupyter.org/node-purpose=core
      
   * ``--machine-type`` specifies the amount of CPU and RAM in each node within
     this default node pool. There is a `variety of types
     <https://cloud.google.com/compute/docs/machine-types>`_ to choose from.
   
   * ``--num-nodes`` specifies how many nodes to spin up.     
       
6. Create a node pool for the users.

   The nodes in this node pool are for the users. The node pool has
   autoscaling enabled along with a lower and an upper scaling limit. This
   means that the amount of nodes is automatically adjusted along with the
   amount of users scheduled.
   
   The `n1-standard-2` machine type has 2 CPUs and 7.5 GB of RAM each of which
   about 0.2 CPU will be requested by system pods. It is a suitable choice for a
   free account that has a limit on a total of 8 CPU cores.

   Note that the node pool is *tainted*. Only user pods that is configured
   with a *toleration* for this taint can schedule on the node pool's nodes.
   This is done in order to ensure the autoscaler will be able to scale down
   when the user pods have stopped.
  
   .. code-block:: bash

      gcloud beta container node-pools create user-pool \
        --machine-type n1-standard-2 \
        --num-nodes 0 \
        --enable-autoscaling \
        --min-nodes 0 \
        --max-nodes 3 \
        --node-labels hub.jupyter.org/node-purpose=user \
        --node-taints hub.jupyter.org_dedicated=user:NoSchedule

   .. note::

      Consider adding the ``--preemptible`` flag to reduce the cost
      significantly. You can `compare the prices here
      <https://cloud.google.com/compute/pricing#predefined_machine_types>`_. See
      the `preemptible node documentation
      <https://cloud.google.com/compute/docs/instances/preemptible>`_ for more
      information.

5. To test if your cluster is initialized, run:

   .. code-block:: bash

      kubectl get node

   The response should list one running node.

6. Give your account super-user permissions, allowing you to perform all
   the actions needed to set up JupyterHub.

   .. code-block:: bash

      kubectl create clusterrolebinding cluster-admin-binding \
        --clusterrole=cluster-admin \
        --user=<YOUR-EMAIL-ADDRESS>

Congrats. Now that you have your Kubernetes cluster running, it's time to
begin :ref:`creating-your-jupyterhub`.
