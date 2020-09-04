.. _setup-jupyterhub:

Setting up JupyterHub
=====================

Now that we have a :doc:`Kubernetes cluster </create-k8s-cluster>` and :doc:`Helm
<setup-helm>` setup, we can proceed by using Helm to install JupyterHub
and related :term:`Kubernetes resources <Kubernetes resource>` using a
:term:`Helm chart`.

Prepare configuration file
--------------------------

In this step we will prepare a `YAML <https://en.wikipedia.org/wiki/YAML>`_
configuration file that we will refer to as `config.yaml`. It will contain the multiple
:term:`Helm values` to be provided to a JupyterHub :term:`Helm chart` developed
specifically together with this guide.

Helm charts contains :term:`templates
<Helm template>` that with provided values will render to :term:`Kubernetes
resources <Kubernetes resource>` to be installed in a Kubernetes cluster. This
config file will provide the values to be used by our Helm chart.

1. Generate a random hex string representing 32 bytes to use as a security
   token. Run this command in a terminal and copy the output:

   .. code-block:: bash

      openssl rand -hex 32

2. Create and start editing a file called ``config.yaml``. In the code snippet
   below we start the widely available `nano editor
   <https://en.wikipedia.org/wiki/GNU_nano>`_, but any editor will do.

   .. code-block:: bash

      nano config.yaml

3. Write the following into the ``config.yaml`` file but instead of writing
   ``<RANDOM-HEX>`` paste the generated hex string you copied in step 1.

   .. code-block:: yaml

      proxy:
        secretToken: "<RANDOM_HEX>"

   .. note::

      It is common practice for Helm and Kubernetes YAML files to indent using
      two spaces.

4. Save the ``config.yaml`` file. In the nano editor this is done by pressing **CTRL+X** or
   **CMD+X** followed by a confirmation to save the changes.

.. Don't put an example here! People will just copy paste that & that's a
   security issue.

Install JupyterHub
------------------

1. Make Helm aware of the `JupyterHub Helm chart repository
   <https://jupyterhub.github.io/helm-chart/>`_ so you can install the
   JupyterHub chart from it without having to use a long URL name.

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

2. Now install the chart configured by your ``config.yaml`` by running this
   command from the directory that contains your ``config.yaml``:

   .. code:: bash

      # Suggested values: advanced users of Kubernetes and Helm should feel
      # free to use different values.
      RELEASE=jhub
      NAMESPACE=jhub

      helm upgrade --cleanup-on-fail \
        --install $RELEASE jupyterhub/jupyterhub \
        --namespace $NAMESPACE \
        --create-namespace \
        --version=0.9.0 \
        --values config.yaml

   where:

   - ``RELEASE`` refers to a `Helm release name
     <https://helm.sh/docs/glossary/#release>`_, an identifier used to
     differentiate chart installations. You need it when you are changing or
     deleting the configuration of this chart installation. If your Kubernetes
     cluster will contain multiple JupyterHubs make sure to differentiate them.
     You can list your Helm releases with ``helm list``.
   - ``NAMESPACE`` refers to a `Kubernetes namespace
     <https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/>`_,
     an identifier used to group Kubernetes resources, in this case all
     Kubernetes resources associated with the JupyterHub chart. You'll need the
     namespace identifier for performing any commands with ``kubectl``.

   .. note::

      * This step may take a moment, during which time there will be no output
        to your terminal. JupyterHub is being installed in the background.

      * If you get a ``release named <YOUR-RELEASE-NAME> already exists`` error,
        then you should delete the release by running ``helm delete
        <YOUR-RELEASE-NAME>``. Then reinstall by repeating this step. If it
        persists, also do ``kubectl delete namespace <YOUR-NAMESPACE>`` and try
        again.

      * In general, if something goes *wrong* with the install step, delete the
        Helm release by running ``helm delete <YOUR-RELEASE-NAME>``
        before re-running the install command.

      * If you're pulling from a large Docker image you may get a
        ``Error: timed out waiting for the condition`` error, add a
        ``--timeout=<NUMBER-OF-MINUTES>m<NUMBER-OF-SECONDS>s`` parameter to the ``helm
        install`` command.

      * The ``--version`` parameter corresponds to the *version of the Helm
        chart*, not the version of JupyterHub. Each version of the JupyterHub
        Helm chart is paired with a specific version of JupyterHub. E.g.,
        ``0.7.0`` of the Helm chart runs JupyterHub ``0.9.2``.
        For a list of which JupyterHub version is installed in each version
        of the Z2JH Helm Chart, see the `Helm Chart repository <https://github.com/jupyterhub/helm-chart#release-notes>`_.

3. While Step 2 is running, you can see the pods being created by entering in
   a different terminal:

   .. code-block:: bash

      kubectl get pod --namespace jhub

   .. note::

      To remain sane we recommend that you `enable autocompletion for kubectl
      <https://kubernetes.io/docs/tasks/tools/install-kubectl/#enabling-shell-autocompletion>`_
      and set a default value for the ``--namespace`` flag:

      .. code-block:: bash

         kubectl config set-context $(kubectl config current-context) --namespace ${NAMESPACE:-jhub}

4. Wait for the *hub* and *proxy* pod to enter the ``Running`` state.

   .. code-block: bash

      NAME                    READY     STATUS    RESTARTS   AGE
      hub-5d4ffd57cf-k68z8    1/1       Running   0          37s
      proxy-7cb9bc4cc-9bdlp   1/1       Running   0          37s

5. Find the IP we can use to access the JupyterHub. Run the following command
   until the ``EXTERNAL-IP`` of the ``proxy-public`` `service
   <https://kubernetes.io/docs/concepts/services-networking/service/>`__ is
   available like in the example output.

   .. code-block:: bash

      kubectl get service --namespace jhub

   .. code-block:: bash

      NAME           TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)        AGE
      hub            ClusterIP      10.51.243.14    <none>          8081/TCP       1m
      proxy-api      ClusterIP      10.51.247.198   <none>          8001/TCP       1m
      proxy-public   LoadBalancer   10.51.248.230   104.196.41.97   80:31916/TCP   1m

   .. note::

      If the IP for ``proxy-public`` is too long to fit into the window, you
      can find the longer version by calling:

      .. code-block:: bash

         kubectl describe service proxy-public --namespace jhub


7. To use JupyterHub, enter the external IP for the `proxy-public` service in
   to a browser. JupyterHub is running with a default *dummy* authenticator so
   entering any username and password combination will let you enter the hub.

Congratulations! Now that you have basic JupyterHub running, you can :ref:`extend it
<extending-jupyterhub>` and :ref:`optimize it <optimization>` in many
ways to meet your needs.

Some examples of customisations are:

* Configure the login to use the account that makes sense to you (Google, GitHub, etc.).
* Use a suitable pre-built image for the user container or build your own.
* Host it on https://your-domain.com.
* ...
