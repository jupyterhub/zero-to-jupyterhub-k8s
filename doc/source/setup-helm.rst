.. _setup-helm:

Setting up Helm
===============

`Helm <https://helm.sh/>`_, the package manager for Kubernetes, is a useful tool
for: installing, upgrading and managing applications on a Kubernetes cluster.
Helm packages are called *charts*. We will be install and manage JupyterHub on
our Kubernetes cluster with a Helm chart.

Helm has two parts: a client (`helm`) and a server (`tiller`). Tiller runs
inside of your Kubernetes cluster as a pod in the kube-system namespace. Tiller
manages *releases* (installations) and *revisions* (versions) of charts deployed
on the cluster. When you run `helm` commands, your local Helm client sends
instructions to `tiller` in the cluster that in turn make the requested changes.

Installation
------------

While several `methods to install Helm
<https://github.com/kubernetes/helm/blob/master/docs/install.md>`_ exists, the
simplest way to install Helm is to run Helm's installer script in a terminal:

.. code:: bash

   curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash

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

   See `our RBAC documentation
   <security.html#use-role-based-access-control-rbac>`_ for more information.

   .. note::

      While most clusters have RBAC enabled and you need this line, you **must**
      skip this step if your Kubernetes cluster does not have RBAC enabled.

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

It should in less then a minute, when `tiller` on the cluster is ready, be able
to provide output like below. Make sure you have at least version 2.9.1 and that
the client (`helm`) and server version (`tiller`) is matching!

.. code-block:: bash

   Client: &version.Version{SemVer:"v2.10.0", GitCommit:"9ad53aac42165a5fadc6c87be0dea6b115f93090", GitTreeState:"clean"}
   Server: &version.Version{SemVer:"v2.10.0", GitCommit:"9ad53aac42165a5fadc6c87be0dea6b115f93090", GitTreeState:"clean"}

.. note::

   If you wish to upgrade the server component of Helm running on the cluster
   (`tiller`):

   .. code-block:: bash

      helm init --upgrade --service-account tiller

Secure Helm
-----------

Ensure that `tiller is secure <https://engineering.bitnami.com/articles/helm-security.html>`_ from access inside the cluster:

.. code:: bash

   kubectl patch deployment tiller-deploy --namespace=kube-system --type=json --patch='[{"op": "add", "path": "/spec/template/spec/containers/0/command", "value": ["/tiller", "--listen=localhost:44134"]}]'

Next Step
---------

Congratulations, Helm is now set up! Let's continue with :ref:`setup-jupyterhub`!
