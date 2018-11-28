.. _create-k8s-cluster:

Setup a Kubernetes Cluster
==========================

Kubernetes' documentation describes the many `ways to set up a cluster
<https://kubernetes.io/docs/setup/pick-right-solution/>`__. We attempt to
provide quick instructions for the most painless and popular ways of setting up
a Kubernetes cluster on various cloud providers and on other infrastructure.

Choose one option and proceed.

.. toctree::
   :titlesonly:

   google/step-zero-gcp
   microsoft/step-zero-azure
   amazon/step-zero-aws
   redhat/step-zero-openshift
   ibm/step-zero-ibm

.. note::

   * During the process of setting up JupyterHub, you'll be creating some
     files for configuration purposes. It may be helpful to create a folder
     for your JuypterHub deployment to keep track of these files.

.. _ways to set up a cluster: https://kubernetes.io/docs/setup/pick-right-solution/
