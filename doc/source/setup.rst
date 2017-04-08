Step by Step Instructions
-------------------------
These instructions will guide you through the process of setting up your jupyterhub for the first time.

Install cloud computing services + kubernetes
=============================================

1. We’ll be using google cloud in this tutorial, though in the future many more cloud platforms will be supported. You should be able to get free credits for trying out google cloud. However, first you need to connect your credit card to your google cloud account.
2. Go to https://console.cloud.google.com.
3. Click the hamburger in the top left (it has 3 horizontal lines in one button). Go to “Billing” then “Payment Methods”, and make sure you have a credit card linked to the account. (you should also get $300 in credits).

  .. image:: https://lh6.googleusercontent.com/K6RuUG7kt-DJH5aELuHSwLQM8oTj4qwmktVcR4EFqqHfL7s0szGH7I1SnXUQArIo-yRe7xI8cPlUwxfUyLs_evC5dPcPBJiSh0LxLI_RbO-Yad_7ZrQcVcQfNEAGKCO5En_MtmQU

4. Click the terminal button at the top right of the page (see figure) to open an interactive terminal in the browser. Alternatively install and initialize the gcloud command-line tools, which send commands to google cloud.
    * If you installed gcloud on your own device, then install kubectl as well. It is a tool for controlling kubernetes. kubectl comes preinstalled in the Google Cloud Shell.
    ``gcloud components install kubectl``
5. Create a kubernetes cluster on google cloud, by typing in the following command. 
  **Note**: This may take several minutes, so create a new tab by clicking the `+` button in the console frame. Then move on to “Setting up JupyterHub”.

    ``gcloud container clusters create YOUR_CLUSTER --num-nodes=3 --zone=us-central1-b``

  * ``--num-nodes`` specifies how many computers to spin up. The higher the number, the greater the cost.
  * ``--zone`` specifies which computer center to use.  To reduce latency, choose a zone closest to whoever is sending the commands. View available zones via `gcloud compute zones list` .
  * When it’s done initializing your cluster, run `kubectl get node`. It should list three running nodes.

Setting up JupyterHub
=====================

1. Install helm in the same terminal window where you execute gcloud and kubectl:
    ``curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash`` 
2. Clone our git repository:
    ``git clone` `https://github.com/data-8/jupyterhub-k8s``
3. Go into the folder that was just created via `cd jupyterhub-k8s` .
4. Create a file called ``config.yaml`` to hold the various customizations describing our JupyterHub installation:
    ``nano config.yaml``
5. Run these two commands (they’re the same command but run them twice)
      ``openssl rand -hex 32``
      ``openssl rand -hex 32``
    Copy the output each time, we’ll use this in the next step.
6. Insert these lines into the file, making sure they do not contain curly quotes or tabs. Substitute each occurrence of RANDOM_STRING_N below with the output of `openssl rand -hex 32` . The strings are tokens that will be used to authenticate your jupyterhub instance (make sure that you keep the quotation marks):

    .. code-block:: bash

        hub:
            # output of first execution of 'openssl rand -hex 32'
            cookieSecret: "RANDOM_STRING_1"
        token:
            # output of second execution of 'openssl rand -hex 32'
            proxy: "RANDOM_STRING_2"

7. Save the file by hitting `Ctrl-X` and make sure to answer ‘yes’ when it asks you to save.


Getting it all running
======================

1. Run ``helm init`` to prepare the kubernetes cluster for helm installation
2. Tell helm to create the instances you configured with the ``yaml`` file. This will spin up JupyterHub.
    ``helm install helm-chart --name=YOUR_CHART --namespace=YOUR_NAMESPACE -f config.yaml``
  1. ``--name`` can be whatever you like. People often name this based off of what this helm config does. So perhaps you might call it `jhub` .
  2. ``--namespace``  is a nifty feature of kubernetes that essentially lets you have multiple sub-deployments using a single helm-chart. People often use this to have both a “live” and a “dev” environment. You can use whatever you like but make it easy to re-type and remember.
  3. If you get a ``release named <YOUR_CHART> already exists`` error, then you should delete this helm-chart by running ``helm delete --purge <YOUR_CHART>`` . Then reinstall by repeating this step.
3. You can see the pods being created with ``kubectl --namespace=YOUR``_NAMESPACE` `get pod``.
4. Wait for the hub and proxy pod to get to running. Ignore cull errors for now; that will be fixed by https://github.com/data-8/jupyterhub-k8s/issues/143.
5. You can find the IP to use for accessing the JupyterHub with ``kubectl --namespace=<YOUR_NAMESPACE>`` ``get svc`` . The external IP for the ‘proxy-public’ service should be accessible in a minute or two.
6. The default authenticator is ‘dummy’ - any username / password will let you in! 

    .. image:: https://lh5.googleusercontent.com/zNIFrF0TmAKVO4RWXXiosPvl33_YdX_hqQJtN8zbSSILjbfEKZ3xCwc3kGkE7xDhIgpxAGQy-n01Ign8UPNSdbSD5qaIYRUOJx4dciHpwK-sduBms-njh7AhPmPk1_N7K51rHfOs
        :height: 200px
        :float: right

Turning it all off
==================

1. If you want to stop these resources from running, you’ll need to tell google cloud to explicitly turn off the cluster that we have created. This is possible from the web console if you click on the hamburger menu (the 3 horizontal lines) in the top left, and then click on the `Container Engine` section (see figure). Click on the container you wish to delete and press the “delete” button.
2. Alternatively, you can run the following command to delete the cluster of your choice.
    ``gcloud container clusters delete YOUR_CLUSTER --zone=YOUR_ZONE``
3. Now your cluster resources should be gone after a few moments - double check this or you will continue to incur charges!
