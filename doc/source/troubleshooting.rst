.. _troubleshooting:

Troubleshooting
===============

FAQ
---

**I thought I had deleted my cloud resources, but they still show up. Why?**

You probably deleted the specific nodes, but not the kubernetes cluster that was controlling those nodes. Kubernetes is designed to make sure that a specific set of resources is available at all times. This means that if you only delete the nodes, but not the kubernetes instance, then it will detect the loss of computers and will create two new nodes to compensate.

**How does billing for this work?!**

JupyterHub isn't handling any of the billing for your usage - that's done through
whatever cloud service you're using.

Common error messages
---------------------

* ``could not find default credentials. See https://developers.google.com/accounts/docs/application-default-credentials for more information.``
    * Execute `gcloud auth application-default login` and follow the prompts. The provided link has other options for advanced use cases.
* ``ERROR: (gcloud.container.clusters.create) ResponseError: code=503, message=Project staeiou-5f880 is not fully initialized with the default service accounts. Please try again later.``
    * Go to ‘https://console.cloud.google.com/kubernetes/list’ and click ‘enable’ and follow the prompts

Investigating Issues
--------------------

If you encounter any issues or are interested to see what's happening under the
hood, you can use the following commands.

To see running pods::

  kubectl --namespace=<YOUR-NAMESPACE> get pod

Then ::

  kubectl --namespace=<YOUR-NAMESPACE> logs <pod-name> to see the logs

you can pass -f to the logs command to tail them.

Alternatively, if you're using Google cloud, you can see the logs in the GUI on
`https://console.cloud.google.com`_ there should be 'logging' under the
hamburger menu.
