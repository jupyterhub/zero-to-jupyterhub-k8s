Zero to JupyterHub
==================

`JupyterHub`_ is a tool that allows you to quickly utilize cloud computing
infrastructure to manage a hub that enables users to interact remotely
with a computing environment that you specify. JupyterHub offers a useful way
to standardize the computing environment of a group of people (e.g.,
for a class of students or an analytics team), as well as allowing
people to access the
hub remotely.

This growing collection of information will help you set up your own
JupyterHub instance. It is in an early stage, so the information and
tools may change quickly. If you see anything that is incorrect or have any
questions, feel free to reach out at the `issues page`_.

.. _creating-your-jupyterhub:

Creating your JupyterHub
------------------------

This tutorial starts from "step zero" and walks through how to install
and configure a complete JupyterHub deployment in the cloud. Using Kubernetes
and the JupyterHub Helm chart provides sensible defaults for an initial
deployment.

To get started, go to :ref:`getting-started`.

.. toctree::
   :maxdepth: 2
   :caption: Creating your JupyterHub

   getting-started
   create-k8s-cluster
   setup-helm
   setup-jupyterhub
   turn-off

.. _customization-guide:

Customization Guide
-------------------

JupyterHub can be configured and customized to fit a variety of deployment
requirements. If you would like to expand JupyterHub, customize its setup,
increase the computational resources available for users, or change
authentication services, this guide will walk you through the steps.
See the :ref:`helm-chart-configuration-reference` for a list of frequently used configurable
helm chart fields.

.. toctree::
   :maxdepth: 2
   :caption: Customization Guide

   extending-jupyterhub
   user-environment
   user-resources
   user-management

.. _administrator-guide:

Administrator Guide
-------------------

This section provides information on managing and maintaining a staging or
production deployment of JupyterHub. It has considerations for managing
cloud-based deployments and tips for maintaining your deployment.

.. toctree::
   :maxdepth: 2
   :caption: Administrator Guide

   authentication
   debug
   cost
   security
   troubleshooting
   upgrading
   advanced

.. _reference:

Reference
---------

.. toctree::
   :maxdepth: 1
   :caption: Reference

   reference
   tools
   glossary
   additional-resources

Institutional support
---------------------

This guide and the `associated helm chart <https://github.com/jupyterhub/helm-chart>`_
would not be possible without the amazing institutional support from the following
organizations (and the organizations that support them!)

* `UC Berkeley Data Science Division <http://data.berkeley.edu/>`_
* `Berkeley Institute for Data Science <https://bids.berkeley.edu/>`_
* `Cal Poly, San Luis Obispo <http://www.calpoly.edu/>`_
* `Simula Research Institute <https://www.simula.no/>`_

.. _JupyterHub: https://github.com/jupyterhub/jupyterhub
.. _issues page: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues
