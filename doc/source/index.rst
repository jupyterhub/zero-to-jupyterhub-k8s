Zero to JupyterHub
==================

`JupyterHub`_ is a tool that allows you to quickly utilize cloud computing
infrastructure to manage a hub that enables users to interact remotely
with a computing environment that you specify. JupyterHub offers a useful way
to standardize the computing environment of a group of people (e.g.,
for a class of students), as well as allowing people to access the
hub remotely.

This growing collection of information will help you set up your own
JupyterHub instance. It is in an early stage, so the information and
tools may change quickly. If you see anything that is incorrect or have any
questions, feel free to reach out at the `issues page`_.

.. _creating-your-jupyterhub:

**Creating your JupyterHub**

.. toctree::
   :maxdepth: 2

   getting-started
   create-k8s-cluster
   setup-helm
   setup-jupyterhub
   turn-off

**Customization Guide**

JupyterHub can be configured and customized to fit a variety of deployment
requirements. This guide helps outline how to customize and extend a
JupyterHub deployment.

.. toctree::
   :maxdepth: 2

   extending-jupyterhub
   user-experience
   schema
   tools


**Administrator Guide**

This section provides information on managing and maintaining a staging or
production deployment of JupyterHub.

.. toctree::
   :maxdepth: 2

   resource-mgmt
   cost
   backups
   upgrading
   security-considerations
   troubleshooting

**Reference**

.. toctree::
   :maxdepth: 2

   glossary
   additional-resources


**Institutional support**

This guide and the `associated helm chart <https://github.com/jupyterhub/helm-chart>`_
would not be possible without the amazing institutional support from the following
organizations (and the organizations that support them!)

* `UC Berkeley Data Science Division <http://data.berkeley.edu/>`_
* `Berkeley Institute for Data Science <https://bids.berkeley.edu/>`_
* `Cal Poly, San Luis Obispo <http://www.calpoly.edu/>`_
* `Simula Research Institute <https://www.simula.no/>`_

.. _JupyterHub: https://github.com/jupyterhub/jupyterhub
.. _issues page: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues
