.. _setup-jupyterhub:

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

1. Create a file called ``config.yaml``. 
   .. code-block:: bash

       echo "hub:" >config.yaml
       echo "    cookieSecret: \"$(openssl rand -hex 32)" >> config.yaml
       echo " " >> config.yaml
       echo "proxy:" >> config.yaml
       echo "    secretToken: \"$(openssl rand -hex 32)" >> config.yaml

Install JupyterHub
------------------

1. Let's add the JupyterHub `helm repository <https://github.com/kubernetes/helm/blob/master/docs/chart_repository.md>`_
   to your helm, so you can install JupyterHub from it. This makes it easy to refer to the JupyterHub chart
   without having to use a long URL each time.

   .. code:: bash

      helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
      helm repo update

   This should show output like:

   .. code::

      Hang tight while we grab the latest from your chart repositories...
      ...Skip local chart repository
      ...Successfully got an update from the "stable" chart repository
      ...Successfully got an update from the "jupyterhub" chart repository
      Update Complete. ⎈ Happy Helming!⎈

2. Now you can install the chart! Run this command from the directory that contains the
   ``config.yaml`` file to spin up JupyterHub:

   .. code:: bash

      helm install jupyterhub/jupyterhub \
          --version=v0.4 \
          --name=<YOUR-RELEASE-NAME> \
          --namespace=<YOUR-NAMESPACE> \
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

      If you get a ``release named <YOUR-RELEASE-NAME> already exists`` error, then
      you should delete the release by running
      ``helm delete --purge <YOUR-RELEASE-NAME>``. Then reinstall by repeating this
      step. If it persists, also do ``kubectl delete <YOUR-NAMESPACE>`` and try again.

      If you're pulling from a large Docker image you may get a
      ``Error: timed out waiting for the condition`` error,
      add a ``--timeout=SOME-LARGE-NUMBER``
      parameter to the ``helm install`` command.

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

   .. note::

      If the IP for ``proxy-public`` is too long to fit into the window, you
      can find the longer version by calling::

        kubectl --namespace=<YOUR_NAMESPACE> describe svc proxy-public

5. To use JupyterHub, enter the external IP for the `proxy-public` service in
   to a browser. JupyterHub is running with a default *dummy* authenticator so
   entering any username and password combination will let you enter the hub.

Congratulations! Now that you have JupyterHub running, you can
`extend it <extending-jupyterhub.html>`_ in many ways. You can use a pre-built
image for the user container, build your own image, configure different
authenticators, and more!
