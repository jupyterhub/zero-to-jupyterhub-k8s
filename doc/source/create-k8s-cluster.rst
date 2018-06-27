.. _create-k8s-cluster:

Creating a Kubernetes Cluster
=============================

Kubernetes' documentation describes the many `ways to set up a cluster`_.
Here, we shall provide quick instructions for the most painless and
popular ways of getting setup in various cloud providers and on other
infrastructure:

- :ref:`Google Cloud <google-cloud>`
- :ref:`Microsoft Azure <microsoft-azure>`
- :ref:`Amazon AWS <amazon-aws>`
- :ref:`Red Hat OpenShift <redhat-openshift>`

.. note::

   * During the process of setting up JupyterHub, you'll be creating some
     files for configuration purposes. It may be helpful to create a folder
     for your JuypterHub deployment to keep track of these files.

   * If you are concerned at all about security (you probably should be), see
     the `Kubernetes best-practices guide <http://blog.kubernetes.io/2016/08/security-best-practices-kubernetes-deployment.html>`_
     for information about keeping your Kubernetes infrastructure secure.

.. _ways to set up a cluster: https://kubernetes.io/docs/setup/pick-right-solution/
