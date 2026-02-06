(docker-desktop-k8s)=

# Kubernetes on Docker Desktop (for learning and development only)

```{important}
[Docker Desktop] is a paid product with a [freemium tier](https://en.wikipedia.org/wiki/Freemium) for individual developers.
```

[Docker Desktop] is bundled with a Kubernetes cluster on a single computer that requires activation in the [Docker Desktop]'s settings. [Docker Desktop] is suitable in order to learn about Kubernetes and to develop and test changes, but its not meant to be used for production purposes.

```{important}
The Zero to JupyterHub guide assumes you're using a managed Kubernetes service with one of the main cloud platforms and **[Docker Desktop] is not officially supported**. You may be able to get help on the [Jupyter community forum](https://discourse.jupyter.org/c/jupyterhub/10).
```

## Kubernetes cluster requirements

All the requirements are implemented in [Docker Desktop] >= 4.37.1 that includes Kubernetes >= 1.30.5:

- [Dynamic Volume Provisioning](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/) for persistent storage
- [LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) or [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) for managing external access to JupyterHub

## Docker Desktop installation

Follow the installation steps in the offical [Docker Desktop]'s Manual:

- [Install Docker Desktop on Mac](https://docs.docker.com/desktop/setup/install/mac-install/)
- [Install Docker Desktop on Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Install Docker Desktop on Linux](https://docs.docker.com/desktop/setup/install/linux/)

  If you are on Linux, you might prefer to use minikube following {ref}`minikube-k8s`.

## Kubernetes cluster creation

1. Click in `Settings`.
2. Click in `Kubernetes`.
3. Click in `Enable Kubernetes`.
4. Click in `Apply & restart`.

To test if your cluster is initialized, run:

```bash
kubectl config get-contexts
```

The response should list the cluster `docker-desktop`.

```bash
kubectl get node
```

The response should list one running node.

Congrats. Now that you have your Kubernetes cluster running, it's time to
begin {ref}`setup-helm`.

[Docker Desktop]: https://www.docker.com/products/docker-desktop/
