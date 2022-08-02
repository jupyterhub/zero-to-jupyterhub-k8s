(create-k8s-cluster)=

# Setup Kubernetes

Kubernetes' documentation describes the many [ways to set up a cluster][ways to set up a cluster].
We attempt to provide quick instructions for the most painless and popular ways of setting up
a Kubernetes cluster on various cloud providers and on other infrastructure.

Choose one option and proceed.

```{toctree}
:titlesonly:

google/step-zero-gcp
microsoft/step-zero-azure
amazon/step-zero-aws
amazon/step-zero-aws-eks
redhat/step-zero-openshift
ibm/step-zero-ibm
digital-ocean/step-zero-digital-ocean
ovh/step-zero-ovh
other-infrastructure/step-zero-microk8s
```

```{note}
During the process of setting up JupyterHub, you'll be creating some
files for configuration purposes. It may be helpful to create a folder
for your JuypterHub deployment to keep track of these files.
```

[ways to set up a cluster]: https://kubernetes.io/docs/setup/
