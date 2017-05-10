Setting up JupyterHub
=====================

Now that we have a `Kubernetes cluster <create-k8s-cluster.html>`_ and
`helm <setup-helm.html>`_ setup, we can begin setting up a JupyterHub.

Prepare configuration file
--------------------------

This step prepares a configuration file (config file). We will use the
`YAML <https://en.wikipedia.org/wiki/YAML>`_ file format to specify
JupyterHub's configuration.

It's important to save the config file in a safe place. The config file is
needed for future changes to JupyterHub's settings.

For the following steps, use your favorite code editor. We'll use the
`nano <https://en.wikipedia.org/wiki/GNU_nano>`_ editor as an example.

1. Create a file called ``config.yaml``. Using the nano editor, for example,
   entering ``nano config.yaml`` at the terminal will start the editor and
   open the config file.

2. Create two random hex strings to use as security tokens. Run these two
   commands (they’re the same command but run them twice) in a terminal:

   .. code-block:: bash

       openssl rand -hex 32
       openssl rand -hex 32

   Copy the output each time, we’ll use these hex strings in the next step.

3. Insert these lines into the ``config.yaml`` file. When editing YAML files,
   use straight quotes and spaces and avoid using curly quotes or tabs.
   Substitute each occurrence of ``RANDOM_STRING_N`` below with the output of
   ``openssl rand -hex 32``. The random hex strings are tokens that will be used
   to secure your JupyterHub instance (make sure that you keep the quotation
   marks):

   .. code-block:: yaml

      hub:
        # output of first execution of 'openssl rand -hex 32'
        cookieSecret: "RANDOM_STRING_1"
      token:
        # output of second execution of 'openssl rand -hex 32'
        proxy: "RANDOM_STRING_2"

   For example:

   .. code-block:: yaml

      hub:
        cookieSecret: "cb0b45df678709c5cc780ed73690898f7ba0659902f996017296143976ffb97c"
      token:
        proxy: "712c4c6c0e78c6c745cfb126f5bbc4b9ba763c78b4bba5797e2eaf508ac99475"

4. Save the ``config.yaml`` file. If using the nano editor, hit ``Ctrl-X`` and
   make sure to answer ‘yes’ when it asks you to save.

Install JupyterHub
------------------

1. Let's use helm to create the instances that you configured with the
   ``config.yaml`` file. Run this command from the directory that contains the
   ``config.yaml`` file to spin up JupyterHub:

   .. code:: bash

      helm install https://github.com/jupyterhub/helm-chart/releases/download/v0.2/jupyterhub-0.2.tgz \
          --name=<YOUR_RELEASE_NAME> \
          --namespace=<YOUR_NAMESPACE> \
          -f config.yaml

   where:

   - ``--name`` is an identifier used by helm to refer to this deployment.
     You need it when you are changing the configuration of this install
     or deleting it. Use something descriptive that you will easily
     remember. For a class called *data8* you might wish set the name to
     **data8-jupyterhub**. In the future you can find out the name by
     using ``helm list``.
   - ``--namespace``  is an identifier
     `used by Kubernetes <https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/>`_
     (among other things) to identify a particular application that might
     be running on a single Kubernetes cluster. You can install many
     applications into the same Kubernetes cluster, and each instance of
     an application is usually separated by being in its own namespace.
     You'll need the namespace identifier for performing any commands
     with ``kubectl``.

   We recommend providing the same value to ``--name`` and ``--namespace``
   for now to avoid too much confusion, but advanced users of Kubernetes and
   helm should feel free to use different values.

   .. note::

      If you get a ``release named <YOUR_CHART> already exists`` error, then
      you should delete this helm-chart by running
      ``helm delete --purge <YOUR_CHART>``. Then reinstall by repeating this
      step.

2. While Step 1 is running, you can see the pods being created by entering in
   a different terminal:

   .. code-block:: bash

      kubectl --namespace=<YOUR_NAMESPACE> get pod

3. Wait for the hub and proxy pod to begin running.

4. You can find the IP to use for accessing the JupyterHub with:

   .. code-block:: bash

      kubectl --namespace=<YOUR_NAMESPACE> get svc

   The external IP for the `proxy-public` service should be accessible in a
   minute or two.

5. To use JupyterHub, enter the external IP for the `proxy-public` service in
   to a browser. JupyterHub is running with a default *dummy* authenticator so
   entering any username and password combination will let you enter the hub.

Congratulations! Now that you have JupyterHub running, you can
`extend it <extending-jupyterhub.html>`_ in many ways. You can use a pre-built
image for the user container, build your own image, configure different
authenticators, and more!

Investigating Issues
====================

If you encounter any issues or are interested to see what's happening under the
hood, you can use the following commands.

To see running pods::

  kubectl --namespace=<YOUR-NAMESPACE> get pod

Then ::

  kubectl --namespace=<YOUR-NAMESPACE> logs <pod-name> to see the logs

you can pass -f to the logs command to tail them.

Alternatively, if you're using Google cloud, you can see the logs in the GUI on
`https://console.cloud.google.com`_ there should be 'logging' under the
hamburger menu.
