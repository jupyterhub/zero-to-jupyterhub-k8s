.. _setup-jupyterhub:

Setting up JupyterHub
=====================

Now that we have a `Kubernetes cluster <create-k8s-cluster.html>`_ and `Helm
<setup-helm.html>`_ setup, we can proceed by setting up the cloud deployment of
our JupyterHub.

Prepare configuration file
--------------------------

This step prepares a `YAML <https://en.wikipedia.org/wiki/YAML>`_ configuration
file (`config.yaml`) for the generic JupyterHub deployment declared by the Helm
chart. Helm charts contains templates for Kubernetes resources to be installed
in a Kubernetes cluster. This config file will provide values to be used by
these templates.

It's important to save the config file in a safe place. The config file is
needed for future changes to JupyterHub's settings.

For the following steps, use your favorite code editor. We'll use the
`nano <https://en.wikipedia.org/wiki/GNU_nano>`_ editor as an example.

1. Create a file called ``config.yaml``. Using the nano editor, for example,
   entering ``nano config.yaml`` at the terminal will start the editor and
   open the config file.

2. Create a random hex string representing 32 bytes to use as a security token.
   Run this command in a terminal:

   .. code-block:: bash

       openssl rand -hex 32

   Copy the output for use in the next step.

3. Insert these lines into the ``config.yaml`` file. When editing YAML files,
   use straight quotes and spaces and avoid using curly quotes or tabs.
   Substitute ``<RANDOM_STRING>`` below with the output of ``openssl rand -hex
   32`` from step 2.

   .. code-block:: yaml

      proxy:
        secretToken: "<RANDOM_STRING>"

.. Don't put an example here! People will just copy paste that & that's a
   security issue.

4. Save the ``config.yaml`` file.

Install JupyterHub
------------------

1. Let's add the JupyterHub `Helm repository
   <https://jupyterhub.github.io/helm-chart/>`_ to your `helm` configuration so
   you can install the JupyterHub chart from it without a long URL name.

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

      helm upgrade <YOUR-RELEASE-NAME> jupyterhub/jupyterhub \
        --install \
        --namespace <YOUR-NAMESPACE> \
        --version 0.7.0-beta.1 \
        --values config.yaml

   where:

   - ``<YOUR-RELEASE-NAME>`` refers to a `Helm release name
     <https://docs.helm.sh/glossary/#release>`_, an identifier used to
     differentiate chart installations. You need it when you are changing or
     deleting the configuration of this chart installation. If your Kubernetes
     cluster will contain multiple JupyterHubs make sure to differentiate them.
     You can list Helm releases with ``helm list``.
   - ``<YOUR-NAMESPACE>`` refers to a `Kubernetes namespace
     <https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/>`_,
     an identifier used to group Kubernetes resources, in this case all
     Kubernetes resources associated with the JupyterHub chart. You'll need the
     namespace identifier for performing any commands with ``kubectl``.

   We recommend providing the same value (*jh* for example) to
   ``<YOUR-RELEASE-NAME>`` and ``<YOUR-NAMESPACE>`` for now to avoid too much
   confusion, but advanced users of Kubernetes and helm should feel free to use
   different values.

   .. note::
      * This step may take a moment, during which time there will be no output
        to your terminal. JupyterHub is being installed in the background.

      * If you get a ``release named <YOUR-RELEASE-NAME> already exists`` error,
        then you should delete the release by running ``helm delete --purge
        <YOUR-RELEASE-NAME>``. Then reinstall by repeating this step. If it
        persists, also do ``kubectl delete namespace <YOUR-NAMESPACE>`` and try
        again.

      * In general, if something goes *wrong* with the install step, delete the
        Helm release by running ``helm delete --purge <YOUR-RELEASE-NAME>``
        before re-running the install command.

      * If you're pulling from a large Docker image you may get a
        ``Error: timed out waiting for the condition`` error, add a
        ``--timeout=SOME-LARGE-NUMBER-OF-SECONDS`` parameter to the ``helm
        install`` command.

      * The ``--version`` parameter corresponds to the *version of the helm chart*,
        not the version of JupyterHub. Each version of the JupyterHub helm chart
        is paired with a specific version of JupyterHub. E.g., v0.7 of the helm
        chart runs JupyterHub v0.9.2.

3. While Step 2 is running, you can see the pods being created by entering in
   a different terminal:

   .. code-block:: bash

      kubectl --namespace=<YOUR-NAMESPACE> get pod

   .. note::

      We recommend that you `enable autocompletion for kubectl
      <https://kubernetes.io/docs/tasks/tools/install-kubectl/#enabling-shell-autocompletion>`_
      and set a default value for the ``--namespace`` flag:

      .. code-block:: bash

         kubectl config set-context $(kubectl config current-context) --namespace=<YOUR-NAMESPACE>

4. Wait for the *hub* and *proxy* pod to enter the ``Running`` state.

5. Find the IP to use for accessing the JupyterHub with:

   .. code-block:: bash

      kubectl --namespace=<YOUR-NAMESPACE> get svc

   The external IP for the `proxy-public` service should be accessible in a
   minute or two.

   .. note::

      If the IP for ``proxy-public`` is too long to fit into the window, you
      can find the longer version by calling:

      .. code-block:: bash

         kubectl --namespace=<YOUR-NAMESPACE> describe svc proxy-public --output=wide


7. To use JupyterHub, enter the external IP for the `proxy-public` service in
   to a browser. JupyterHub is running with a default *dummy* authenticator so
   entering any username and password combination will let you enter the hub.

Congratulations! Now that you have basic JupyterHub running, you can `extend it
<extending-jupyterhub.html>`_ and `optimize it <optimization.html>`_ in many
ways to meet your needs.

* Configure the login to use the account that makes sense to you (Google, GitHub, etc.).
* Use a suitable pre-built image for the user container or build your own.
* Host it on https://your-domain.com.
* ...
