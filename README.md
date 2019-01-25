# Zero to JupyterHub with Kubernetes

[![Build Status](https://travis-ci.org/jupyterhub/zero-to-jupyterhub-k8s.svg?branch=master)](https://travis-ci.org/jupyterhub/zero-to-jupyterhub-k8s)
[![Documentation Status](https://readthedocs.org/projects/zero-to-jupyterhub/badge/?version=stable)](https://zero-to-jupyterhub.readthedocs.io/en/stable/?badge=stable)

This repo contains a *Helm chart* for JupyterHub and a guide to use it. Together
they allow you to make a JupyterHub available to a very large group of users
such as the staff and students of a university.

## The guide

The [Zero to JupyterHub with Kubernetes guide](https://z2jh.jupyter.org)
provides user-friendly steps to _deploy_
[JupyterHub](https://github.com/jupyterhub/jupyterhub) on a cloud using
[Kubernetes](https://kubernetes.io/) and [Helm](https://helm.sh/).

The guide is complemented well by the [documentation for JupyterHub](https://jupyterhub.readthedocs.io).

## The chart

The JupyterHub Helm chart lets a user create a reproducible and maintainable
deployment of JupyterHub on a Kubernetes cluster in a cloud environment. The
released charts are made available in our [Helm chart
repository](https://jupyterhub.github.io/helm-chart).

## History

Much of the initial groundwork for this documentation is information learned
from the successful use of JupyterHub and Kubernetes at UC Berkeley in their
[Data 8](http://data8.org/) program.

![](doc/source/_static/images/data8_audience.jpg)

## Acknowledgements

Thank you to the following contributors:

- Aaron Culich
- Carol Willing
- Chris Holdgraf
- Erik Sundell
- Ryan Lovett
- Yuvi Panda

Future contributors are encouraged to add themselves to this README file too.

## Licensing

This repository is dual licensed under the Apache2 (to match the upstream
Kubernetes [charts](https://github.com/helm/charts) repository) and
3-clause BSD (to match the rest of Project Jupyter repositories) licenses. See
the `LICENSE` file for more information!
