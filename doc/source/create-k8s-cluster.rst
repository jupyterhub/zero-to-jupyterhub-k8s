.. _create-k8s-cluster:

Creating your Kubernetes Cluster
=============================

Kubernetes' documentation describes the many `ways to set up a cluster`_.
Here, we shall provide quick instructions for the most painless and
popular ways of getting setup in various cloud providers and on other
infrastructure. Choose one option and proceed.

.. toctree::
   :titlesonly:

   google/step-zero-gcp
   microsoft/step-zero-azure
   amazon/step-zero-aws
   redhat/step-zero-openshift

.. _creating-your-jupyterhub:

.. note::

   * During the process of setting up JupyterHub, you'll be creating some
     files for configuration purposes. It may be helpful to create a folder
     for your JuypterHub deployment to keep track of these files.

.. _ways to set up a cluster: https://kubernetes.io/docs/setup/pick-right-solution/
