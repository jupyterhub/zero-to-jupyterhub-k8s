(minikube-k8s)

# Kubernetes on minikube (for learning and development only)

[minikube] can setup a Kubernetes cluster on a single computer. minikube be suitable in order to learn about Kubernetes and to develop and test changes, but its not meant to be used for production purposes.

```{important}
The Zero to JupyterHub guide assumes you're using a managed Kubernetes service with one of the main cloud platforms and **[minikube] is not officially supported**. You may be able to get help on the [Jupyter community forum](https://discourse.jupyter.org/c/jupyterhub/10).
```

[minikube]: https://minikube.sigs.k8s.io/docs/

## Kubernetes cluster requirements

All the requirements are implemented in minikube >= v1.31.2:

- [Dynamic Volume Provisioning](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/) for persistent storage
- [LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) or [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) for managing external access to JupyterHub

## minikube installation

Follow the installation steps in the [minikube's "Get Started!" page](https://minikube.sigs.k8s.io/docs/start/).

## Kubernetes cluster creation

From a terminal, run

```bash
minikube start \
--kubernetes-version stable \
--nodes 2 \
--cpus 2 \
--memory 2000 \
--cni calico
```

To test if your cluster is initialized, run:

```bash
kubectl get node
```

The response should list two running nodes (or however many nodes you set with ``--nodes` above).

Congrats. Now that you have your Kubernetes cluster running, it's time to
begin {ref}`setup-helm`.
