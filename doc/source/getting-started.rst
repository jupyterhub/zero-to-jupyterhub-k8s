.. _getting-started:

Getting started with JupyterHub
===============================

**JupyterHub** lets you create custom computing environments that
can be accessed remotely (e.g., at a specific URL) by multiple users.

This guide acts as an assistant to guide you through the process of setting
up your JupyterHub deployment using Kubernetes. It helps you connect
and configure the following things:

* A **cloud provider** such Google Cloud, Microsoft Azure, Amazon EC2, and
  others
* **Kubernetes** to manage resources on the cloud
* **Helm** to configure and control Kubernetes
* **Docker** to use containers that standardize computing environments
* **JupyterHub** to manage users and deploy Jupyter notebooks

You already are well on your way to understanding what it means (procedurally)
to deploy Jupyterhub.

Dependencies for Deploying a JupyterHub Instance
------------------------------------------------

For a more extensive description of the tools and services that JupyterHub
depends upon, see our :ref:`tools` page.

To begin deploying your JupyterHub on Kubernetes, please move on
to :ref:`create-k8s-cluster`.

.. _issues page: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues
