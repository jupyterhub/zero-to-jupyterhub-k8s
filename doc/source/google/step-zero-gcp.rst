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
   
      Start *Google Cloud Shell* from `console.cloud.google.com
      <https://console.cloud.google.com>`_ by clicking the button shown below.
      You are now in control of a virtual machine with various tools
      preinstalled. If you save something in a user folder they will remain
      avaitlableo you if you return at a later stage. Additional documentation
      about Google Cloud shell is available `here
      <https://cloud.google.com/shell/docs/>`__

      .. image:: ../_static/images/google/start_interactive_cli.png
         :align: center

   b. **Use your own computer's terminal:**

      1. Download and install the `gcloud` command line tool at its `downloads
         page <https://cloud.google.com/sdk/downloads>`_. It will help you
         create and communicate with a Kubernetes cluster.

      2. Install ``kubectl`` (reads *kube control*), it is a tool for controlling
         Kubernetes clusters in general. From your terminal, enter:

         .. code-block:: bash

            gcloud components install kubectl

4. Create a managed Kubernetes cluster and a default node pool.

   Ask Google Cloud to create a managed Kubernetes cluster and a default `node
   pool <https://cloud.google.com/kubernetes-engine/docs/concepts/node-pools>`_
   to get nodes from. *Nodes* represents hardware and a *node pools* will
   keep track of how much of a certain type of hardware that you would like.

   .. code-block:: bash

      gcloud beta container clusters create \
        --machine-type n1-standard-2 \
        --num-nodes 2 \
        --zone us-central1-b \
        --cluster-version latest \
        <CLUSTERNAME>
      
   * Replace `<CLUSTERNAME>` with a name that can be used to refer to this cluster
     in the future.

   * ``--machine-type`` specifies the amount of CPU and RAM in each node within
     this default node pool. There is a `variety of types
     <https://cloud.google.com/compute/docs/machine-types>`_ to choose from.
     You can pick something from `this list
     <https://cloud.google.com/compute/docs/regions-zones/regions-zones#available>`_.
     that is not too far away from your users.
   
   * ``--num-nodes`` specifies how many nodes to spin up. You can change this
     later through the cloud console or using the `gcloud` command line tool.

   * ``--zone`` specifies the data center zone where your cluster will be created.


5. To test if your cluster is initialized, run:

   .. code-block:: bash

      kubectl get node

   The response should list one running node.

6. Give your account permissions to perform all administrative actions needed.

   .. code-block:: bash

      kubectl create clusterrolebinding cluster-admin-binding \
        --clusterrole=cluster-admin \
        --user=<GOOGLE-EMAIL-ACCOUNT>
    
   Replace `<GOOGLE-EMAIL-ACCOUNT>` with the exact email of the Google account
   you used to sign up for Google Cloud.

   .. note::
  
      Did you enter your email correctly? If not, you can run `kubectl delete
      clusterrolebinding cluster-admin-binding` and do it again.

Congrats. Now that you have your Kubernetes cluster running, it's time to
begin :ref:`creating-your-jupyterhub`.
