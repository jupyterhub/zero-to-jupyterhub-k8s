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
requirements. This guide helps outline how to customize and extend a JupyterHub
deployment.

.. toctree::
   :maxdepth: 2

   extending-jupyterhub
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



.. _JupyterHub: https://github.com/jupyterhub/jupyterhub
.. _issues page: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues
