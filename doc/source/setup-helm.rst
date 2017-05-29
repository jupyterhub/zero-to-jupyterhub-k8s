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

        helm init

This command only needs to run once per Kubernetes cluster.

Next Step
---------

Congratulations. Helm is now set up. The next step is to
:ref:`install JupyterHub <setup-jupyterhub>`!
