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

Initialization
--------------

After installing helm on your machine, initialize helm on your Kubernetes
cluster. At the terminal, enter:

   .. code:: bash

      kubectl --namespace kube-system create sa tiller
      kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
      helm init --service-account tiller

This command only needs to run once per Kubernetes cluster.

Verify
------

You can verify that you have the correct version and that it installed
properly by running:

   .. code:: bash

      helm version

It should provide output like

   .. code-block:: bash

      Client: &version.Version{SemVer:"v2.4.1", GitCommit:"46d9ea82e2c925186e1fc620a8320ce1314cbb02", GitTreeState:"clean"}
      Server: &version.Version{SemVer:"v2.4.1", GitCommit:"46d9ea82e2c925186e1fc620a8320ce1314cbb02", GitTreeState:"clean"}

Make sure you have at least version 2.4.1!

Secure Helm
~~~~~~~~~~~

Ensure that `tiller is secure <https://engineering.bitnami.com/articles/helm-security.html>`_ from access inside the cluster:

   .. code:: bash

      kubectl --namespace=kube-system patch deployment tiller-deploy --type=json --patch='[{"op": "add", "path": "/spec/template/spec/containers/0/command", "value": ["/tiller", "--listen=localhost:44134"]}]'

Next Step
---------

Congratulations. Helm is now set up. The next step is to
:ref:`install JupyterHub <setup-jupyterhub>`!
