.. _google-cloud:

Step Zero: Kubernetes on `Google Cloud <https://cloud.google.com/>`_
--------------------------------------------------------------------

`Google Kubernetes Engine <https://cloud.google.com/kubernetes-engine/>`_
(GKE) is the simplest and most common way of setting
up a Kubernetes Cluster. You may be able to receive `free credits
<https://cloud.google.com/free/>`_ for trying it out (though note that a
free account `comes with limitations
<https://cloud.google.com/free/docs/frequently-asked-questions#limitations>`_).
Either way, you will need to connect your credit card or other payment method to
your google cloud account.

1. Go to ``https://console.cloud.google.com`` and log in.

2. Enable the `Kubernetes Engine API <https://console.cloud.google.com/apis/api/container.googleapis.com/overview>`_.

3. Use your preferred command line interface.

   You have two options: a) use the Google Cloud Shell (no installation needed)
   or b) install and use the gcloud command-line tool.
   If you are unsure which to choose, we recommend beginning with option
   "a" and using the Google Cloud Shell. Instructions
   for each are detailed below:

   a. **Use the Google Cloud Shell**. Start the Google Cloud Shell
      by clicking the button shown below. This will start an interactive shell
      session within Google Cloud.

      .. image:: ../_static/images/google/start_interactive_cli.png
         :align: center

      See the `Google Cloud Shell docs <https://cloud.google.com/shell/docs/>`_
      for more information.

   b. **Install and use the gcloud command line tool**.
      This tool sends commands to Google Cloud and lets you do things like create
      and delete clusters.

      - Go to the `gcloud command line tool downloads page <https://cloud.google.com/sdk/downloads>`_
        to **download and install the gcloud command line tool**.
      - See the `gcloud documentation <https://cloud.google.com/pubsub/docs/quickstart-cli>`_ for
        more information on the gcloud command line tool.

4. Install ``kubectl``, which is a tool for controlling kubernetes. From
   the terminal, enter:

     .. code-block:: bash

        gcloud components install kubectl

5. Create a Kubernetes cluster on Google Cloud, by typing the following
   command into either the Google Cloud shell or the gcloud command-line tool:

   .. code-block:: bash

      gcloud container clusters create <YOUR-CLUSTER> \
          --num-nodes=3 \
          --machine-type=n1-standard-2 \
          --zone=us-central1-b

   where:

   * ``--num-nodes`` specifies how many computers to spin up. The higher the
     number, the greater the cost.
   * ``--machine-type`` specifies the amount of CPU and RAM in each node. There
     is a `variety of types <https://cloud.google.com/compute/docs/machine-types>`_
     to choose from. Picking something appropriate here will have a large effect
     on how much you pay - smaller machines restrict the max amount of RAM each
     user can have access to but allow more fine-grained scaling, reducing cost.
     The default (`n1-standard-2`) has 2CPUs and 7.5G of RAM each, and might not
     be a good fit for all use cases!
   * ``--zone`` specifies which data center to use. Pick something that is not
     too far away from your users. You can find a list of them `here <https://cloud.google.com/compute/docs/regions-zones/regions-zones#available>`_.

   .. note::

      Consider `setting a cloud budget <https://cloud.google.com/billing/docs/how-to/budgets>`_
      for your Google Cloud account in order to make sure you don't accidentally
      spend more than you wish to.

6. To test if your cluster is initialized, run:

   .. code-block:: bash

      kubectl get node

   The response should list three running nodes.

7. Give your account super-user permissions, allowing you to perform all
   the actions needed to set up JupyterHub.

   .. code-block:: bash

      kubectl create clusterrolebinding cluster-admin-binding \
          --clusterrole=cluster-admin \
          --user=<YOUR-EMAIL-ADDRESS>

Congrats. Now that you have your Kubernetes cluster running, it's time to
begin :ref:`creating-your-jupyterhub`.
