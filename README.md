# Zero to JupyterHub with Kubernetes

[![Build Status](https://travis-ci.org/jupyterhub/zero-to-jupyterhub-k8s.svg?branch=master)](https://travis-ci.org/jupyterhub/zero-to-jupyterhub-k8s)
[![Documentation Status](https://readthedocs.org/projects/zero-to-jupyterhub/badge/?version=latest)](http://zero-to-jupyterhub.readthedocs.io/en/latest/?badge=latest)

**This is under active development and subject to change.**

This repo contains resources, such as **Helm charts** and the
[**Zero to JupyterHub Guide**](https://zero-to-jupyterhub.readthedocs.io), which
help you to deploy JupyterHub on Kubernetes.

## Zero to JupyterHub with Kubernetes Guide

The [Zero to JupyterHub Guide](https://zero-to-jupyterhub.readthedocs.io) gives
user-friendly steps to create a new JupyterHub deployment using Kubernetes.

For additional information about JupyterHub, such as a technical overview,
configuration reference, and API reference, please consult the
[JupyterHub project documentation](https://jupyterhub.readthedocs.io) which
contains information that applies to Kubernetes as well as other deployment
methods. The JupyterHub project documentation provides detailed information
about authenticators, spawners, and services.

We hope these two documents help you get up and running with your own
JupyterHub deployment.

## Helm charts

The JupyterHub Helm charts allow a user to create reproducible and
maintainable deployments of JupyterHub with Kubernetes.

## History and inspiration

Much of the intial groundwork for this documentation is information learned from
the successful use of JupyterHub and Kubernetes at UC Berkeley in their
[Data 8](http://data8.org/) program.


### Acknowledgements

Thank you to the following contributors:

- Aaron Culich
- Carol Willing
- Chris Holdgraf
- Erik Sundell
- Ryan Lovett
- Yuvi Panda

Future contributors are encouraged to add themselves to this README file too.

## Licensing

This repository is dual licensed under the Apache2 (to match the upstream kubernetes
[charts](https://github.com/kubernetes/charts) repository) and 3-clause BSD (to
match the rest of Project Jupyter repositories) licenses. See the `LICENSE` file for
more information!
