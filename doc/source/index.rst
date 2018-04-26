Zero to JupyterHub
==================

`JupyterHub`_ is a tool that allows you to quickly utilize cloud computing
infrastructure to manage a hub that enables your users to interact remotely
with a computing environment that you specify. JupyterHub offers a useful way
to standardize the computing environment of a group of people (e.g.,
for a class of students or an analytics team), as well as allowing
people to access the
hub remotely.

This growing collection of information will help you set up your own
JupyterHub instance. It is in an early stage, so the information and
tools may change quickly.

If you have tips or deployments that you would like to share, see
:ref:`community-resources`. If you see anything that is incorrect
or have any questions, feel free to reach out at the `issues page`_.

.. _getting-to-zero:

Getting to Step Zero: your Kubernetes cluster
---------------------------------------------

This section describes a Kubernetes cluster and outlines how to complete *Step Zero: your Kubernetes cluster* for
different cloud providers and infrastructure.

.. toctree::
   :titlesonly:
   :caption: Step Zero: your Kubernetes cluster

   create-k8s-cluster
   google/step-zero-gcp
   microsoft/step-zero-azure
   amazon/step-zero-aws
   redhat/step-zero-openshift

.. _creating-your-jupyterhub:

Creating your JupyterHub
------------------------

This tutorial starts from *Step Zero: your Kubernetes cluster* and describes the
steps needed for you to create a complete initial JupyterHub deployment.
This will use the JupyterHub Helm chart which provides sensible defaults for
an initial deployment.

To begin, go to :ref:`setup-helm`.

.. toctree::
   :maxdepth: 1
   :caption: Creating your JupyterHub

   getting-started
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
See the :ref:`helm-chart-configuration-reference` for a list of frequently
used configurable helm chart fields.

.. toctree::
   :maxdepth: 2
   :caption: Customization Guide

   extending-jupyterhub
   user-environment
   user-resources
   user-storage
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

   architecture
   debug
   authentication
   optimization
   security
   upgrading
   troubleshooting
   advanced
   cost

.. _community-resources:

Resources from the community
----------------------------

This section gives the community a space to provide information on setting
up, managing, and maintaining JupyterHub.

.. important::
   We recognize that Kubernetes has many deployment options. As a project team
   with limited resources to provide end user support, we rely on community
   members to share their collective Kubernetes knowledge and JupyterHub
   experiences.

We hope that you will use this section to share deployments with on a variety
of infrastructure and for different use cases.
There is also a `community maintained list <users-list.html>`_ of users of this
Guide and the JupyterHub Helm Chart.

Please submit a pull request to add to this section. Thanks.

.. toctree::
   :maxdepth: 1
   :caption: Resources from the community

   additional-resources
   users-list

.. _reference:

Reference
---------

.. toctree::
   :maxdepth: 1
   :caption: Reference

   reference
   reference-docs
   tools
   glossary

Institutional support
---------------------

This guide and the associated helm chart would not be possible without the
amazing institutional support from the following
organizations (and the organizations that support them!)

* `UC Berkeley Data Science Division <https://data.berkeley.edu/>`_
* `Berkeley Institute for Data Science <https://bids.berkeley.edu/>`_
* `Cal Poly, San Luis Obispo <https://www.calpoly.edu/>`_
* `Simula Research Institute <https://www.simula.no/>`_


.. _JupyterHub: https://github.com/jupyterhub/jupyterhub
.. _issues page: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues
