.. _getting-started:

Overview
========

At this point, you should have completed *Step Zero* and have an operational
Kubernetes cluster available. If not, see :ref:`create-k8s-cluster`.

From now on, we will almost exclusively control the cloud through Kubernetes
rather then something that is specific to the cloud provider. What you learn
from now on is therefore also useful with other cloud providers.

The next step is to setup Helm. Helm will allow us to install a package of
things on the cloud. This is relevant to us as there are several parts alongside
the JupyterHub itself to allow it to run on the cloud relating to storage,
network and security.

After setting up Helm, we will use it to install JupyterHub and associated
infrastructure. After this has been done, you can spend time configuring your
deployment of JupyterHub to suit your needs.

Let's get started by moving on to :ref:`setup-helm`.
