.. _faq:

FAQ
===

This section contains frequently asked questions about the JupyterHub deployment.
For information on debugging Kubernetes, see :ref:`debug`.

I thought I had deleted my cloud resources, but they still show up. Why?
------------------------------------------------------------------------

You probably deleted the specific nodes, but not the kubernetes cluster that
was controlling those nodes. Kubernetes is designed to make sure that a
specific set of resources is available at all times. This means that if you
only delete the nodes, but not the kubernetes instance, then it will detect
the loss of computers and will create two new nodes to compensate.

How does billing for this work?
-------------------------------

JupyterHub isn't handling any of the billing for your usage. That's done
through whatever cloud service you're using. For considerations about
managing cost with JupyterHub, see :ref:`cost`.
