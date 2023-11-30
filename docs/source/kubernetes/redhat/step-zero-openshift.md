(redhat-openshift)=

# Kubernetes on Red Hat OpenShift

[OpenShift](https://www.okd.io/) from RedHat is a cluster manager based on Kubernetes.

For running Z2JH on openshift, check out the [z2jh-openshift](https://github.com/gembaadvantage/z2jh-openshift) project. It customizes the containers used by the helm chart with security configuration required by OpenShift, and makes minor alterations to network policies to enable networking with the Weave NPC and the default OpenShift DNS.

For more information please see the [ongoing discourse discussion](https://discourse.jupyter.org/t/zero-to-jupyterhub-and-red-hat-openshift/12656).
