.. _getting-started:

Getting started with JupyterHub
===============================

The goal of JupyterHub is to make it easy and straightforward to
create custom computing environments that can be accessed remotely (e.g.,
at a specific URL) by multiple users. Many of these pieces can be a little
confusing, and this website is meant as an assistant to guide you through
the process of setting up your JupyterHub.

These materials are meant to help you connect the following things:

* A cloud provider (Google Cloud, Microsoft Azure, Amazon EC2)
* Kubernetes (to manage resources on the cloud)
* Helm (to configure and control kubernetes)
* Docker (to use containers that standardize computing environments)
* JupyterHub (to manage users and deploy jupyter notebooks)

To get started, we recommend beginning with the first item on our
:ref:`main page <creating-your-jupyterhub>`. If you'd like to know how to expand and
customize your jupyterhub setup, check out :ref:`extending-jupyterhub`.
Finally, for a more extensive description of the tools and services that
JupyterHub utilizes, see our :ref:`tools` page. Also, don't hesitate to reach
out at our `issues page`_ on GitHub.

.. _issues page: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues
