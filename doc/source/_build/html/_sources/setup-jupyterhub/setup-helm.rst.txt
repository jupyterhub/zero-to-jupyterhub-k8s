.. _setup-helm:

Setting up Helm
===============

`Helm <https://helm.sh/>`_, the package manager for Kubernetes, is a useful tool
for: installing, upgrading and managing applications on a Kubernetes cluster.
Helm packages are called *charts*.
We will be installing and managing JupyterHub on our Kubernetes cluster using a Helm chart.

Charts are abstractions describing how to install packages onto a Kubernetes
cluster. When a chart is deployed, it works as a templating engine to populate
multiple `yaml` files for package dependencies with the required variables, and
then runs `kubectl apply` to apply the configuration to the resource and install
the package.


.. note::

   If you previously installed Z2JH using Helm 2, it is worth noting that
   Helm 3 includes several major **breaking changes**. See the
   `Helm 3 FAQ <https://helm.sh/docs/faq/>`_ for more information.

   For **migrating from Helm v2 to v3**, checkout the official
   `Helm guide <https://helm.sh/docs/topics/v2_v3_migration/>`_.

Installation
------------

While several `methods to install Helm
<https://helm.sh/docs/intro/install/>`_ exist, the
simplest way to install Helm is to run Helm's installer script in a terminal:

.. code:: bash

   curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

* The minimum supported version of Helm in Z2JH is `3.2.0`.

* Helm 3 uses the same security mechanisms as other Kubernetes clients such as `kubectl`.


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

Congratulations, Helm is now set up! Let's continue with :ref:`setup-jupyterhub`!

