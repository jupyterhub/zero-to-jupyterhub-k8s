.. _setup-helm:

Setting up Helm
===============

`Helm <https://helm.sh/>`_, the package manager for Kubernetes, is a useful tool
to install, upgrade and manage applications on a Kubernetes cluster. We will be
using Helm to install and manage JupyterHub on our cluster.

Installation
------------

The simplest way to install helm is to run Helm's installer script at a
terminal:

   .. code:: bash

      curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash

`Alternative methods for helm installation <https://github.com/kubernetes/helm/blob/master/docs/install.md>`_
exist if you prefer to install without using the script.

.. _helm-rbac:

Initialization
--------------

After installing helm on your machine, initialize helm on your Kubernetes
cluster. At the terminal, enter:

1. Set up a `ServiceAccount
   <https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/>`_
   for use by ``Tiller``, the server side component of ``helm``.

   .. code-block:: bash

      kubectl --namespace kube-system create serviceaccount tiller

   **Azure AKS**: If you're on Azure AKS, you should now skip directly to step 3.**

2. Give the ``ServiceAccount`` `RBAC
   <https://kubernetes.io/docs/admin/authorization/rbac/>`_ full permissions to
   manage the cluser.

   While most clusters have RBAC enabled and you need this
   line, you **must** skip this step if your kubernetes cluster does not have
   RBAC enabled (for example, if you are using Azure AKS).

   .. code-block:: bash

      kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller

3. Set up Helm on the cluster.

   .. code-block:: bash

      helm init --service-account tiller

This command only needs to run once per Kubernetes cluster.

Verify
------

You can verify that you have the correct version and that it installed
properly by running:

   .. code:: bash

      helm version

It should provide output like:

   .. code-block:: bash

      Client: &version.Version{SemVer:"v2.4.1", GitCommit:"46d9ea82e2c925186e1fc620a8320ce1314cbb02", GitTreeState:"clean"}
      Server: &version.Version{SemVer:"v2.4.1", GitCommit:"46d9ea82e2c925186e1fc620a8320ce1314cbb02", GitTreeState:"clean"}

Make sure you have at least version 2.4.1!

If you receive an error that the Server is unreachable, do another `helm version`
in 15-30 seconds, and it should display the Server version.

Secure Helm
~~~~~~~~~~~

Ensure that `tiller is secure <https://engineering.bitnami.com/articles/helm-security.html>`_ from access inside the cluster:

   .. code:: bash

      kubectl --namespace=kube-system patch deployment tiller-deploy --type=json --patch='[{"op": "add", "path": "/spec/template/spec/containers/0/command", "value": ["/tiller", "--listen=localhost:44134"]}]'

Next Step
---------

Congratulations. Helm is now set up. The next step is to
:ref:`install JupyterHub <setup-jupyterhub>`!
