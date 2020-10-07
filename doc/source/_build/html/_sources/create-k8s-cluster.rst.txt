.. _create-k8s-cluster:

Setup Kubernetes
================

Kubernetes' documentation describes the many `ways to set up a cluster`_.
We attempt to provide quick instructions for the most painless and popular ways of setting up
a Kubernetes cluster on various cloud providers and on other infrastructure.

Choose one option and proceed.

.. toctree::
   :titlesonly:

   google/step-zero-gcp
   microsoft/step-zero-azure
   microsoft/step-zero-azure-autoscale
   amazon/step-zero-aws
   amazon/step-zero-aws-eks
   redhat/step-zero-openshift
   ibm/step-zero-ibm
   digital-ocean/step-zero-digital-ocean
   ovh/step-zero-ovh

.. note::

   * During the process of setting up JupyterHub, you'll be creating some
     files for configuration purposes. It may be helpful to create a folder
     for your JuypterHub deployment to keep track of these files.

.. _ways to set up a cluster: https://kubernetes.io/docs/setup/
