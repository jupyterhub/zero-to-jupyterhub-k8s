Setting up JupyterHub
=====================

Now that we have a `kubernetes cluster <create-k8s-cluster.html>`_ & `helm <setup-helm.html>`_ setup, we can set up a JupyterHub!

Prepare config file
-------------------

We will use a `YAML <https://en.wikipedia.org/wiki/YAML>`_ file to specify the configuration of our JupyterHub. Save this in a safe place - you will need it if you want to change how your JupyterHub behaves.

We'll be assume you are using the `nano <https://en.wikipedia.org/wiki/GNU_nano>`_ editor to edit the config file. Feel free to use any editor you want!

1. Run these two commands (they’re the same command but run them twice)::

       openssl rand -hex 32
       openssl rand -hex 32

   Copy the output each time, we’ll use this in the next step.

2. Create a file called ``config.yaml``::

    nano config.yaml


4. Insert these lines into the file, making sure they do not contain curly quotes or tabs. Substitute each occurrence of RANDOM_STRING_N below with the output of `openssl rand -hex 32` . The strings are tokens that will be used to secure your JupyterHub instance (make sure that you keep the quotation marks):

    .. code-block:: yaml

        hub:
            # output of first execution of 'openssl rand -hex 32'
            cookieSecret: "RANDOM_STRING_1"
        token:
            # output of second execution of 'openssl rand -hex 32'
            proxy: "RANDOM_STRING_2"

5. Save the file by hitting ``Ctrl-X`` and make sure to answer ‘yes’ when it asks you to save.

Install JupyterHub
------------------

1. Tell helm to create the instances you configured with the ``yaml`` file.
   This will spin up JupyterHub:

    .. code::

        helm install https://github.com/jupyterhub/helm-chart/releases/download/v0.1/jupyterhub-0.1.tgz --name=YOUR_RELEASE_NAME --namespace=YOUR_NAMESPACE -f config.yaml

    where:

    1. ``--name`` can be whatever you like. People often base this off what this particular JupyterHub does. For example, if you are deploying for a class named 'data8' you might set this to 'data8-jupyterhub'
    2. ``--namespace``  is a nifty feature of kubernetes that essentially lets you have multiple sub-deployments using a single helm-chart. People often use this to have both a “live” and a “dev” environment. You can use whatever you like but make it easy to re-type and remember.

    .. note::

        If you get a ``release named <YOUR_CHART> already exists`` error, then you should delete this helm-chart by running ``helm delete --purge <YOUR_CHART>`` . Then reinstall by repeating this step.

2. You can see the pods being created with ``kubectl --namespace=YOUR_NAMESPACE get pod``.
3. Wait for the hub and proxy pod to get to running. 
4. You can find the IP to use for accessing the JupyterHub with ``kubectl --namespace=<YOUR_NAMESPACE> get svc`` . The external IP for the ‘proxy-public’ service should be accessible in a minute or two.
5. The default authenticator is ‘dummy’ - any username / password will let you in!

Now that you have a JupyterHub running, you can `extend it <extending-jupyterhub.html>`_ in many ways! You can use a pre-built image for the user container, build your own, configure different authenticators, and more!
