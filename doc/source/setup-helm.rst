.. _setup-helm:

Setting up Helm
===============

`Helm <https://helm.sh/>`_, the package manager for Kubernetes, is a useful tool
for: installing, upgrading and managing applications on a Kubernetes cluster.
The Helm packages are called *charts*. We will be install and manage JupyterHub
on our kubernetes cluster with a Helm chart.

Helm has two parts: a client (`helm`) and a server (`tiller`). Tiller runs
inside of your Kubernetes cluster as a pod in the kube-system namespace and
manages *releases* (installations) and *revisions* (versions) of charts deployed
on the kubernetes cluster. When you run `helm` commands, your local Helm client
sends instructions to `tiller` in the cluster that in turn make the requested
changes.

Installation
------------

The simplest way to install helm is to run Helm's installer script in a
terminal:

.. code:: bash

   curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash

`Alternative methods for helm installation <https://github.com/kubernetes/helm/blob/master/docs/install.md>`_
exist if you prefer to install without using the script.

.. _helm-rbac:

Initialization
--------------

After installing helm on your machine, initialize Helm on your Kubernetes
cluster:

1. Set up a `ServiceAccount
   <https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/>`_
   for use by `tiller`.

   .. code-block:: bash

      kubectl --namespace kube-system create serviceaccount tiller

2. Give the `ServiceAccount` full permissions to manage the cluster.

   .. code-block:: bash

      kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller

   See the `RBAC documentation
   <security.html#use-role-based-access-control-rbac>`_ for more
   information.

   .. note::

      While most clusters have RBAC enabled and you need this line, you **must**
      skip this step if your kubernetes cluster does not have RBAC enabled.

3. Initialize `helm` and `tiller`.

   .. code-block:: bash

      helm init --service-account tiller

   This command only needs to run once per Kubernetes cluster, it will create a
   `tiller` deployment in the kube-system namespace and setup your local `helm`
   client.

   .. note::
    
      If you wish to install `helm` on another computer, you won't need to setup
      `tiller` again but you still need to initialize `helm`:

      .. code-block:: bash

         helm init --client-only

Verify
------

You can verify that you have the correct version and that it installed properly
by running:

.. code:: bash

   helm version

It should provide output like below. Make sure you have at least version 2.9.1
and that the client (`helm`) and server version (`tiller`) is matching!

.. code-block:: bash

   Client: &version.Version{SemVer:"v2.9.1", GitCommit:"20adb27c7c5868466912eebdf6664e7390ebe710", GitTreeState:"clean"}
   Server: &version.Version{SemVer:"v2.9.1", GitCommit:"20adb27c7c5868466912eebdf6664e7390ebe710", GitTreeState:"clean"}

If you receive an error that the Server is unreachable, do another `helm
version` in 15-30 seconds, and it should display the Server version.

.. note::

   If you wish to upgrade the server component of Helm running on the cluster
   (`tiller`):

   .. code-block:: bash

      helm init --service-account tiller --upgrade

Secure Helm
-----------

Ensure that `tiller is secure <https://engineering.bitnami.com/articles/helm-security.html>`_ from access inside the cluster:

.. code:: bash

   kubectl --namespace=kube-system patch deployment tiller-deploy --type=json --patch='[{"op": "add", "path": "/spec/template/spec/containers/0/command", "value": ["/tiller", "--listen=localhost:44134"]}]'

Next Step
---------

Congratulations. Helm is now set up. The next step is to :ref:`install
JupyterHub <setup-jupyterhub>`!
