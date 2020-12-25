Zero to JupyterHub with Kubernetes
==================================

`JupyterHub`_ allows users to interact with a computing environment through a
webpage. As most devices have access to a web browser, JupyterHub makes it is
easy to provide and standardize the computing environment for a group of people
(e.g., for a class of students or an analytics team).

This project will help you set up your own JupyterHub on a cloud/on-prem k8s environment and leverage
its scalable nature to support a large group of users. Thanks to
:term:`Kubernetes`, we are not tied to a specific cloud provider.

.. note::

   This project is under active development so information and tools may
   change. *You can be a part of this change!* If you see anything that is incorrect
   or have any questions, feel free to post on the community `Discourse forum
   <https://discourse.jupyter.org/>`_ or reach out in the `Gitter chat
   <https://gitter.im/jupyterhub/jupyterhub>`_ or create an issue at the `issues
   page`_. If you have tips or deployments that you would like to share, see
   :ref:`resources-and-references`.

This documentation is for Helm chart version |chart_version|, which deploys
JupyterHub version |jupyterhub_version|.

This version of the chart requires Kubernetes version |kube_version| and Helm
>=2.16.

.. note::

   Helm 2 is deprecated since of November 2019, and
   `will receive bugfixes until August 13, 2020 <https://helm.sh/blog/covid-19-extending-helm-v2-bug-fixes>`_.
   So, the Helm references in this documentation are Helm v3.

.. _about-guide:

What To Expect
--------------

This guide will help you deploy and customize your own JupyterHub on a cloud.
While doing this, you will gain valuable experience with:

* **A cloud provider** such as Google Cloud, Microsoft Azure, Amazon EC2, IBM Cloud...
* **Kubernetes** to manage resources on the cloud
* **Helm v3** to configure and control the packaged JupyterHub installation
* **JupyterHub** to give users access to a Jupyter computing environment
* **A terminal interface** on some operating system

It's also possible you end up getting some experience with:

* **Docker** to build customized image for the users
* **Domain registration** to make the hub available at https://your-domain-name.com

.. note::

   For a more elaborate introduction to the tools and services that JupyterHub
   depends upon, see our :ref:`tools` page.

.. _getting-to-zero:

Setup Kubernetes
----------------

This section describes a how to setup a Kubernetes cluster on a selection of cloud providers and environments, as well as initialize Helm, a Kubernetes package manager, to work with it.

.. toctree::
   :maxdepth: 2

   kubernetes/index

.. _creating-your-jupyterhub:

Setup JupyterHub
----------------

This tutorial starts from *Step Zero: Your Kubernetes cluster* and describes the
steps needed for you to create a complete initial JupyterHub deployment.
Please ensure you have a working installation of Kubernetes and Helm before 
proceeding with this section.

.. toctree::
   :maxdepth: 2

   jupyterhub/index

JupyterHub can be configured and customized to fit a variety of deployment
requirements. If you would like to expand JupyterHub, customize its setup,
increase the computational resources available for users, or change
authentication services, this guide will walk you through the steps.
See the :ref:`helm-chart-configuration-reference` for a list of frequently
used configurable helm chart fields.

.. _administrator-guide:

Administrator Guide
-------------------

This section provides information on managing and maintaining a staging or
production deployment of JupyterHub. It has considerations for managing
cloud-based deployments and tips for maintaining your deployment.

.. toctree::
   :maxdepth: 2

   administrator/index

.. _resources-and-references:

Resources
-----------

This section holds all the references and resources that helped make this project what it is today.

.. toctree::
   :maxdepth: 2

   resources/index


Community Resources
********************

This section gives the community a space to provide information on setting
up, managing, and maintaining JupyterHub.

.. important::
   We recognize that Kubernetes has many deployment options. As a project team
   with limited resources to provide end user support, we rely on community
   members to share their collective Kubernetes knowledge and JupyterHub
   experiences.

.. note::
   **Contributing to Z2JH**. If you would like to help improve the Zero to
   JupyterHub guide, please see the `issues page`_ as well as the `contributor guide
   <https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/master/CONTRIBUTING.md>`_.

We hope that you will use this section to share deployments with on a variety
of infrastructure and for different use cases.
There is also a :doc:`community maintained list <resources/community>` of users of this
Guide and the JupyterHub Helm Chart.


Institutional support
**********************

This guide and the associated helm chart would not be possible without the
amazing institutional support from the following
organizations (and the organizations that support them!)

* `UC Berkeley Data Science Division <https://data.berkeley.edu/>`_
* `Berkeley Institute for Data Science <https://bids.berkeley.edu/>`_
* `Cal Poly, San Luis Obispo <https://www.calpoly.edu/>`_
* `Simula Research Institute <https://www.simula.no/>`_


.. _JupyterHub: https://github.com/jupyterhub/jupyterhub
.. _issues page: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues
