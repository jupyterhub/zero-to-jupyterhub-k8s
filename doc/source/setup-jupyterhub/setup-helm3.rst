:orphan:

.. _setup-helm3:

Setting up Helm 3 (Preview)
===========================

.. warning::

  Helm 3 is not yet officially supported by Zero to JupyterHub. Upgrades from
  Helm 2 are **not** handled. Helm 3 should only be used for testing new
  clusters. Please report any bugs on the `GitHub issue tracker
  <https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues>`_.

`Helm <https://helm.sh/>`_, the package manager for Kubernetes, is a useful tool
for: installing, upgrading and managing applications on a Kubernetes cluster.
Helm packages are called *charts*.
We will be installing and managing JupyterHub on
our Kubernetes cluster using a Helm chart.

Charts are abstractions describing how to install packages onto a Kubernetes
cluster. When a chart is deployed, it works as a templating engine to populate
multiple `yaml` files for package dependencies with the required variables, and
then runs `kubectl apply` to apply the configuration to the resource and install
the package.

Helm 3 includes several major breaking changes including:

- The Tiller server component is removed. Helm now uses the default Kubernetes
  security mechanisms. This greatly improves security.
- Uses a three way instead of two way strategic merge. This may affect how
  upgrades are merged into an existing deployment.

See the `Helm 3 FAQ <https://helm.sh/docs/faq/>`_ for more information.

Installation
------------

While several `methods to install Helm
<https://helm.sh/docs/intro/install/>`_ exist, the
simplest way to install Helm is to run Helm's installer script in a terminal:

.. code:: bash

   curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

Helm 3 uses the same security mechanisms as other Kubrenetes clients such as
`kubectl`. Since it does not have a separate server process no special steps
are required to secure it.

Verify
------

You can verify that it is installed properly by running:

.. code:: bash

   helm list

You should see an empty list since no Helm charts have been installed:

.. code-block:: bash

   NAME    NAMESPACE       REVISION        UPDATED STATUS  CHART   APP VERSION


Next Step
---------

Helm 3 will not automatically create a namespace for JupyterHub.
If you are using a namespace other than `default` create it now:

.. code:: bash

   kubectl create namespace $NAMESPACE

Now continue with :ref:`setup-jupyterhub`.
