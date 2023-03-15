(self-hosted-k8s)

# Self-hosted Kubernetes

The Zero to JupyterHub guide assumes you're using a managed Kubernetes service with one of the main cloud platforms.

JupyterHub can be deployed on a self-hosted Kubernetes cluster, but this is not officially supported.
However you may be able to get help, and find examples of other self-hosted deployments, on the [Jupyter community forum](https://discourse.jupyter.org/c/jupyterhub/10).

## Kubernetes cluster requirements

Z2JH assumes your Kubernetes cluster has the following features:

- [Dynamic Volume Provisioning](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/) for persistent storage
- [LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) or [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) for managing external access to JupyterHub

Z2JH assumes you have full administrator access to the cluster.

In many cases you need to consult your Kubernetes provider's documentation to find out how to enable these features.
Please test all these features with a simple deployment before proceeding with the Zero to JupyterHub guide.
Z2JH has several interacting components which makes it much more difficult to debug Kubernetes problems, so you will save a lot of time by verifying your cluster is working correctly first.

It is possible to deploy Z2JH without some features, for example by [disabling persistent storage](schema_singleuser.storage.type) or using [NodePort](schema_proxy.service.type), but this is only suitable for testing.
