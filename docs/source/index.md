# Zero to JupyterHub with Kubernetes

[JupyterHub](https://github.com/jupyterhub/jupyterhub) allows users to
interact with a computing environment through a webpage. As most devices
have access to a web browser, JupyterHub makes it is easy to provide and
standardize the computing environment for a group of people (e.g., for a
class of students or an analytics team).

This project will help you set up your own JupyterHub on a cloud/on-prem
k8s environment and leverage its scalable nature to support a large
group of users. Thanks to {term}`Kubernetes`,
we are not tied to a specific cloud provider.

```{admonition} Note
This project is under active development so information and tools may
change. *You can be a part of this change!* If you see anything that is
incorrect or have any questions, feel free to post on the community
[Discourse forum](https://discourse.jupyter.org/) or reach out in the
[Gitter chat](https://gitter.im/jupyterhub/jupyterhub) or create an
issue at the [issues
page](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues). If
you have tips or deployments that you would like to share, see the
[Community Resources section](community-resources).
```

This documentation is for Helm chart version {{chart_version}} that deploys
JupyterHub version {{jupyterhub_version}} and other components versioned
in {{requirements}}. The Helm chart requires Kubernetes version >={{kube_version}}
and Helm >={{helm_version}}.

## What To Expect

This guide will help you deploy and customize your own JupyterHub on a
cloud. While doing this, you will gain valuable experience with:

- **A cloud provider** such as Google Cloud, Microsoft Azure, Amazon
  EC2, IBM Cloud\...
- **Kubernetes** to manage resources on the cloud
- **Helm v3** to configure and control the packaged JupyterHub
  installation
- **JupyterHub** to give users access to a Jupyter computing
  environment
- **A terminal interface** on some operating system

It\'s also possible you end up getting some experience with:

- **Docker** to build customized image for the users
- **Domain registration** to make the hub available at
  <https://your-domain-name.com>

```{admonition} Note
For a more elaborate introduction to the tools and services that
JupyterHub depends upon, see our [page about that](tools).
```

## Setup Kubernetes

This section describes a how to setup a Kubernetes cluster on a
selection of cloud providers and environments, as well as initialize
Helm, a Kubernetes package manager, to work with it.

```{toctree}
:maxdepth: 2
kubernetes/index
```

## Setup JupyterHub

This tutorial starts from _Step Zero: Your Kubernetes cluster_ and
describes the steps needed for you to create a complete initial
JupyterHub deployment. Please ensure you have a working installation of
Kubernetes and Helm before proceeding with this section.

```{toctree}
:maxdepth: 2
jupyterhub/index
```

JupyterHub can be configured and customized to fit a variety of
deployment requirements. If you would like to expand JupyterHub,
customize its setup, increase the computational resources available for
users, or change authentication services, this guide will walk you
through the steps. See the [](helm-chart-configuration-reference) for a
list of frequently used configurable helm chart fields.

## Administrator Guide

This section provides information on managing and maintaining a staging
or production deployment of JupyterHub. It has considerations for
managing cloud-based deployments and tips for maintaining your
deployment.

```{toctree}
:maxdepth: 2
administrator/index
```

## Resources

This section holds all the references and resources that helped make
this project what it is today.

```{toctree}
:maxdepth: 2
resources/index
```

### Community Resources

This section gives the community a space to provide information on
setting up, managing, and maintaining JupyterHub.

```{admonition} Note
We recognize that Kubernetes has many deployment options. As a project
team with limited resources to provide end user support, we rely on
community members to share their collective Kubernetes knowledge and
JupyterHub experiences.
```

```{admonition} Contributing
If you would like to help improve this guide or Helm chart, please see the [issues
page](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues) as
well as the [contributor
guide](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/HEAD/CONTRIBUTING.md).
```

We hope that you will use this section to share deployments with on a
variety of infrastructure and for different use cases. There is also a
[community maintained list](community-resources) of users of this Guide and the JupyterHub Helm Chart.

### Institutional support

This guide and the associated helm chart would not be possible without
the amazing institutional support from the following organizations (and
the organizations that support them!)

- [UC Berkeley Data Science Division](https://data.berkeley.edu/)
- [Berkeley Institute for Data Science](https://bids.berkeley.edu/)
- [Cal Poly, San Luis Obispo](https://www.calpoly.edu/)
- [Simula Research Institute](https://www.simula.no/)
- [2i2c](https://2i2c.org)

## Changelog

This section holds describes the changes between versions and how to upgrade
between them.

```{toctree}
:maxdepth: 1
changelog
```
