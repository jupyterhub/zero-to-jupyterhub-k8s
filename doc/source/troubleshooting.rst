.. _troubleshooting:

Troubleshooting
===============

This section contains general troubleshooting tips for your JupyterHub
deployment. For information on debugging Kubernetes, see :ref:`debug`.

FAQ - General
-------------

**I thought I had deleted my cloud resources, but they still show up. Why?**

You probably deleted the specific nodes, but not the kubernetes cluster that
was controlling those nodes. Kubernetes is designed to make sure that a
specific set of resources is available at all times. This means that if you
only delete the nodes, but not the kubernetes instance, then it will detect
the loss of computers and will create two new nodes to compensate.

**How does billing for this work?**

JupyterHub isn't handling any of the billing for your usage. That's done
through whatever cloud service you're using. For considerations about
managing cost with JupyterHub, see :ref:`cost`.

Common error messages
---------------------

Google Cloud
^^^^^^^^^^^^

.. tip::

   In Google Cloud, you can see the logs using the
   `Cloud Console GUI <https://console.cloud.google.com>`_. See the **logging**
   section under the hamburger menu.

1. ``Could not find default credentials. See
   https://developers.google.com/accounts/docs/application-default-credentials
   for more information.``

   Execute ``gcloud auth application-default login`` and follow the prompts.
   The provided link in the error message has additional options for advanced
   use cases.

2. ``ERROR: (gcloud.container.clusters.create) ResponseError: code=503,
   message=Project staeiou-5f880 is not fully initialized with the default
   service accounts. Please try again later.``

   Go to `<https://console.cloud.google.com/kubernetes/list>`_ and click
   'enable' and follow the prompts.
