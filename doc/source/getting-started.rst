.. _getting-started:

Getting started with JupyterHub
===============================

The goal of **JupyterHub** is to create custom computing environments that
can be accessed remotely (e.g., at a specific URL) by multiple users.

This guide acts as an assistant to guide you through the process of setting
up your JupyterHub deployment. It helps you connect and configure the
following things:

* A **cloud provider** such Google Cloud, Microsoft Azure, Amazon EC2, and
  others
* **Kubernetes** to manage resources on the cloud
* **Helm** to configure and control Kubernetes
* **Docker** to use containers that standardize computing environments
* **JupyterHub** to manage users and deploy Jupyter notebooks

You already are well on your way to understanding what it means (procedurally)
to deploy Jupyterhub. 

For more guidance
-----------------

If you want more guidance, the next step on your journey is to :ref:`create a
Kubernetes cluster on Google Cloud
<google-cloud>`. 

For info on extensions and customization 
----------------------------------------

If you'd like to know how to expand and customize your jupyterhub setup, check
out :ref:`extending-jupyterhub`. 

For more a discussion about software dependencies
-------------------------------------------------

For a more extensive description of the tools and services that JupyterHub
utilizes, see our :ref:`tools` page.

Questions or Suggestions?
=========================

If you have questions or suggestions, please reach out at our `issues page`_
on GitHub.

.. _issues page: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues
