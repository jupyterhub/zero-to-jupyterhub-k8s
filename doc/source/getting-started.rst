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

Verifying JupyterHub dependencies
---------------------------------

At this point, you should have completed *Step Zero* and have an operational
Kubernetes cluster. You will already have a cloud provider/infrastructure
and kubernetes and docker installed.

If you need to create a Kubernetes cluster, see
:ref:`create-k8s-cluster`.

We also depend on Helm and the JupyterHub Helm chart for your JupyterHub
deployment. We'll deploy them in this section. Let's begin by moving on to
:ref:`setup-helm`.


.. note::

   For a more extensive description of the tools and services that JupyterHub
   depends upon, see our :ref:`tools` page.



