Step by Step Instructions
=========================

These instructions will guide you through the process of setting up your JupyterHub for the first time.

Setting up kubernetes on Google Cloud
---------------------------------------------

1. We’ll be using google cloud in this tutorial, though in the future many more cloud platforms will be supported. You should be able to get free credits for trying out google cloud. However, first you need to connect your credit card to your google cloud account.
2. Go to https://console.cloud.google.com.
3. Click the hamburger in the top left (it has 3 horizontal lines in one button). Go to “Billing” then “Payment Methods”, and make sure you have a credit card linked to the account. (you should also get $300 in credits).
4. Install and initialize the gcloud command-line tools, which send commands to google cloud and lets you do things like create / delete clusters.
   
   - Go to the `gcloud downloads page <https://cloud.google.com/sdk/downloads>`_
     to download/install the gcloud SDK.
   - See the `gcloud documentation <https://cloud.google.com/sdk/>`_ for
     more information on the gcloud SDK.
   - Install ``kubectl``, which is a tool for controlling kubernetes.

         ``gcloud components install kubectl``

5. Create a kubernetes cluster on google cloud, by typing in the following command.

    ``gcloud container clusters create YOUR_CLUSTER --num-nodes=3 --zone=us-central1-b``

  * ``--num-nodes`` specifies how many computers to spin up. The higher the number, the greater the cost.
  * ``--zone`` specifies which computer center to use.  To reduce latency, choose a zone closest to whoever is sending the commands. View available zones via `gcloud compute zones list` .
  * When it’s done initializing your cluster, run ``kubectl get node``. It should list three running nodes.

  .. note::

      This may take several minutes, so create a new shell tab. Then move on to the section “Setting up JupyterHub”. You'll know it's done initializing when ``kubectl get node`` shows your new nodes.

Setting up JupyterHub
---------------------

1. Install helm:

    .. code::

        curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash

2. Create a file called ``config.yaml`` to hold the various customizations describing our JupyterHub installation:

    ``nano config.yaml``

    .. note::

        Remember where you store your ``config.yaml`` file in case you need to use it again or make changes to it. You'll be able to "re-initialize" helm if you make changes in order to modify the kubernetes setup.

3. Run these two commands (they’re the same command but run them twice)::

       openssl rand -hex 32
       openssl rand -hex 32

   Copy the output each time, we’ll use this in the next step.

4. Insert these lines into the file, making sure they do not contain curly quotes or tabs. Substitute each occurrence of RANDOM_STRING_N below with the output of `openssl rand -hex 32` . The strings are tokens that will be used to authenticate your JupyterHub instance (make sure that you keep the quotation marks):

    .. code-block:: bash

        hub:
            # output of first execution of 'openssl rand -hex 32'
            cookieSecret: "RANDOM_STRING_1"
        token:
            # output of second execution of 'openssl rand -hex 32'
            proxy: "RANDOM_STRING_2"

5. Save the file by hitting ``Ctrl-X`` and make sure to answer ‘yes’ when it asks you to save.


Getting it all running
----------------------

1. Run ``helm init`` to prepare the kubernetes cluster for helm installation
2. Tell helm to create the instances you configured with the ``yaml`` file.
   This will spin up JupyterHub:

    .. code::

        helm install https://github.com/jupyterhub/helm-chart/releases/download/v0.1/jupyterhub-0.1.tgz --name=YOUR_CHART --namespace=YOUR_NAMESPACE -f config.yaml

    where:

    1. ``--name`` can be whatever you like. People often name this based off of what this helm config does. So perhaps you might call it `jhub` .
    2. ``--namespace``  is a nifty feature of kubernetes that essentially lets you have multiple sub-deployments using a single helm-chart. People often use this to have both a “live” and a “dev” environment. You can use whatever you like but make it easy to re-type and remember.

    .. note::

        If you get a ``release named <YOUR_CHART> already exists`` error, then you should delete this helm-chart by running ``helm delete --purge <YOUR_CHART>`` . Then reinstall by repeating this step.

3. You can see the pods being created with ``kubectl --namespace=YOUR_NAMESPACE get pod``.
4. Wait for the hub and proxy pod to get to running. Ignore cull errors for now; that will be fixed by https://github.com/data-8/jupyterhub-k8s/issues/143.
5. You can find the IP to use for accessing the JupyterHub with ``kubectl --namespace=<YOUR_NAMESPACE> get svc`` . The external IP for the ‘proxy-public’ service should be accessible in a minute or two.
6. The default authenticator is ‘dummy’ - any username / password will let you in!

Turning it all off
------------------

1. If you want to stop these resources from running, you’ll need to tell google cloud to explicitly turn off the cluster that we have created. This is possible `from the web console <https://console.cloud.google.com>`_ if you click on the hamburger menu (the 3 horizontal lines) in the top left, and then click on the ``Container Engine`` section (see figure). Click on the container you wish to delete and press the “delete” button.

   .. image:: https://lh5.googleusercontent.com/zNIFrF0TmAKVO4RWXXiosPvl33_YdX_hqQJtN8zbSSILjbfEKZ3xCwc3kGkE7xDhIgpxAGQy-n01Ign8UPNSdbSD5qaIYRUOJx4dciHpwK-sduBms-njh7AhPmPk1_N7K51rHfOs
      :height: 200px

   .. note::

      Alternatively, you can run the following command to delete the cluster of your choice.

      ``gcloud container clusters delete YOUR_CLUSTER --zone=YOUR_ZONE``

2. Now your cluster resources should be gone after a few moments - double check this or you will continue to incur charges!
