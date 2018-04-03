.. _redhat-openshift:

Step Zero: Kubernetes on Red Hat OpenShift
------------------------------------------

The easiest and recommended way to deploy JupyterHub on OpenShift
is to follow the Red Hat instructions at the Red Hat GitHub repo
`jupyter-on-openshift/jupyterhub-quickstart <https://github.com/jupyter-on-openshift/jupyterhub-quickstart>`_. 
This repo's README file steps you through the process to get from OpenShift
to a running JupyterHub cluster.

From the `README <https://github.com/jupyter-on-openshift/jupyterhub-quickstart/blob/master/README.md>`_:

::

	This repository aims to provide a much easier way of deploying JupyterHub
	to OpenShift which makes better use of OpenShift specific features,
	including OpenShift templates, and Source-to-Image (S2I) builders. The
	result is a method for deploying JupyterHub to OpenShift which doesn't
	require any special admin privileges to the underlying Kubernetes cluster,
	or OpenShift. As long as a user has the necessary quotas for memory, CPU
	and persistent storage, they can deploy JupyterHub themselves.

1.  Follow the steps in the `README <https://github.com/jupyter-on-openshift/jupyterhub-quickstart/blob/master/README.md>`_.

Congrats. You should now have a running JupyterHub.

Additional resources about Jupyter on OpenShift
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An excellent series of OpenShift blog posts on Jupyter and OpenShift
authored by Red Hat developer, Graham Dumpleton, are 
available on the `OpenShift blog <https://blog.openshift.com/tag/jupyter/>`_.
The first in a series of seven posts begins `here <https://blog.openshift.com/tag/jupyter/>`_.
