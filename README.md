# Zero to JupyterHub with Kubernetes

[![Documentation build status](https://img.shields.io/readthedocs/zero-to-jupyterhub?logo=read-the-docs)](https://zero-to-jupyterhub.readthedocs.io/en/latest/?badge=latest)
[![GitHub Workflow Status - Test](https://img.shields.io/github/actions/workflow/status/jupyterhub/zero-to-jupyterhub-k8s/test-chart.yaml?logo=github&label=tests)](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/actions)
[![GitHub Workflow Status - Vuln. scan](https://img.shields.io/github/actions/workflow/status/jupyterhub/zero-to-jupyterhub-k8s/vuln-scan.yaml?logo=github&label=Vuln.%20scan)](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/actions)
[![Latest stable release of the Helm chart](https://img.shields.io/badge/dynamic/json.svg?label=stable&url=https://hub.jupyter.org/helm-chart/info.json&query=$.jupyterhub.stable&colorB=orange&logo=helm)](https://jupyterhub.github.io/helm-chart#jupyterhub)
[![Latest pre-release of the Helm chart](https://img.shields.io/badge/dynamic/json.svg?label=pre&url=https://hub.jupyter.org/helm-chart/info.json&query=$.jupyterhub.pre&colorB=orange&logo=helm)](https://jupyterhub.github.io/helm-chart#development-releases-jupyterhub)
[![Latest development release of the Helm chart](https://img.shields.io/badge/dynamic/json.svg?label=dev&url=https://hub.jupyter.org/helm-chart/info.json&query=$.jupyterhub.latest&colorB=orange&logo=helm)](https://jupyterhub.github.io/helm-chart#development-releases-jupyterhub)
<br/>
[![GitHub](https://img.shields.io/badge/issue_tracking-github-blue?logo=github)](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues)
[![Discourse](https://img.shields.io/badge/help_forum-discourse-blue?logo=discourse)](https://discourse.jupyter.org/c/jupyterhub/z2jh-k8s)
[![Gitter](https://img.shields.io/badge/social_chat-gitter-blue?logo=gitter)](https://gitter.im/jupyterhub/jupyterhub)
[![Contribute](https://img.shields.io/badge/I_want_to_contribute!-grey?logo=jupyter)](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/HEAD/CONTRIBUTING.md)

This repo contains a _Helm chart_ for JupyterHub and a guide to use it. Together
they allow you to make a JupyterHub available to a very large group of users
such as the staff and students of a university.

## The guide

The [Zero to JupyterHub with Kubernetes guide](https://z2jh.jupyter.org)
provides user-friendly steps to _deploy_
[JupyterHub](https://github.com/jupyterhub/jupyterhub) on a cloud using
[Kubernetes](https://kubernetes.io/) and [Helm](https://helm.sh/).

The guide is complemented well by the [documentation for JupyterHub](https://jupyterhub.readthedocs.io).

## The Helm chart

The JupyterHub Helm chart lets a user create a reproducible and maintainable
deployment of JupyterHub on a Kubernetes cluster in a cloud environment. The
released charts are made available in our [Helm chart
repository](https://jupyterhub.github.io/helm-chart).

## Notice of Participation in Study

Please note that this repository is participating in a study into sustainability
of open source projects. Data will be gathered about this repository for
approximately the next 12 months, starting from 2021-06-11.

Data collected will include number of contributors, number of PRs, time taken to
close/merge these PRs, and issues closed.

For more information, please visit
[the informational page](https://sustainable-open-science-and-software.github.io/) or download the [participant information sheet](https://sustainable-open-science-and-software.github.io/assets/PIS_sustainable_software.pdf).

## History

Much of the initial groundwork for this documentation is information learned
from the successful use of JupyterHub and Kubernetes at UC Berkeley in their
[Data 8](http://data8.org/) program.

![](docs/source/_static/images/data8_massive_audience.jpg)

## Acknowledgements

Thank you to the following contributors:

- Aaron Culich
- Carol Willing
- Chris Holdgraf
- Erik Sundell
- Ryan Lovett
- Yuvi Panda
- Laurent Goderre

Future contributors are encouraged to add themselves to this README file too.

## Licensing

This repository is dual licensed under the Apache2 (to match the upstream
Kubernetes [charts](https://github.com/helm/charts) repository) and
3-clause BSD (to match the rest of Project Jupyter repositories) licenses. See
the `LICENSE` file for more information!
