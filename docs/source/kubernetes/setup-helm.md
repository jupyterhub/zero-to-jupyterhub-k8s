(setup-helm)=

# Setting up `helm`

[`helm`](https://helm.sh/), the package manager for Kubernetes, is a useful
command line tool for: installing, upgrading and managing applications on a
Kubernetes cluster. Helm packages are called _charts_. We will be installing and
managing JupyterHub on our Kubernetes cluster using a Helm chart.

Charts are abstractions describing how to install packages onto a Kubernetes
cluster. When a chart is deployed, it works as a templating engine to populate
multiple `yaml` files for package dependencies with the required variables, and
then runs `kubectl apply` to apply the configuration to the resource and install
the package.

```{note}
If you previously installed Z2JH using Helm 2, it is worth noting that
Helm 3 includes several major **breaking changes**. See the
[Helm 3 FAQ](https://helm.sh/docs/faq/) for more information.

For **migrating from Helm v2 to v3**, checkout the official
[Helm guide](https://helm.sh/docs/topics/v2_v3_migration/).
```

## Installation

For version {{chart_version}} of the Helm chart, `helm` >={{helm_version}} is
required.

While several [methods to install Helm](https://helm.sh/docs/intro/install/) exist, the
simplest way to install Helm is to run Helm's installer script in a terminal:

```
curl https://raw.githubusercontent.com/helm/helm/HEAD/scripts/get-helm-3 | bash
```

## Verify

You can verify that it is installed properly by running:

```
helm version
```

## Next Step

Congratulations, `helm` is now set up! Let's continue with {ref}`setup-jupyterhub`!
