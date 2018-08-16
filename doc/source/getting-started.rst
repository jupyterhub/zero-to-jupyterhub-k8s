.. _getting-started:

Getting Started
===============

**JupyterHub** lets you create custom computing environments that users can
access on any device by opening up a browser and accessing a webpage. This guide
will help you deploy and customize your own JupyterHub on a cloud. You will
gain experience with:

* **A cloud provider** such Google Cloud, Microsoft Azure, Amazon EC2...
* **Kubernetes** to manage resources on the cloud
* **Helm** to configure and control the JupyterHub installation
* **JupyterHub** to allow users to access a Jupyter computing environment
* **A terminal interface** on some operating system

And may end up gaining experience with:

* **Docker** and **repo2docker** to build custom computing environments
* **Domain registration** to serve your JupyterHub at https://your-domain-name.com

.. note::

   For a more elaborate introduction to the tools and services that JupyterHub
   depends upon, see our :ref:`tools` page.


Verify JupyterHub dependencies
------------------------------

At this point, you should have completed *Step Zero* and have an operational
Kubernetes cluster made available through a cloud provider/infrastructure. If
not, see :ref:`create-k8s-cluster`.

You will use Helm and the JupyterHub Helm chart for your JupyterHub deployment.
Let's get started by moving on to :ref:`setup-helm`.
