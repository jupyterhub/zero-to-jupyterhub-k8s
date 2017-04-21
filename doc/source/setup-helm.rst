Setting up Helm
===============

`Helm <https://helm.sh/>`_ is a tool to install, upgrade & manage applications on a kubernetes cluster. We will be using it to install & manage JupyterHub on our cluster.

Installation
------------

The simplest way to install helm is to run the following at a terminal

    .. code:: bash

        curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash

If this method of installation scares you, there are `other ways to install <https://github.com/kubernetes/helm/blob/master/docs/install.md>`_ too.


Initialization
--------------

After installing helm on your machine, you need to initialize it on your kubernetes cluster. You can do so with


    .. code:: bash

        helm init

This needs to happen only once per Kubernetes cluster.

Next Step
---------

Now that you have helm set up, next step is to `install JupyterHub <setup-jupyterhub.html>`_!
