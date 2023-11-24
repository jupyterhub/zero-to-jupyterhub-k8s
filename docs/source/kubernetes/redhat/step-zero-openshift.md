(redhat-openshift)=

# Kubernetes on Red Hat OpenShift

[OpenShift](https://www.okd.io/) from RedHat is a cluster manager based on Kubernetes.

For running Z2JH on openshift, check out the [z2jh-openshift](https://github.com/gembaadvantage/z2jh-openshift) project. It customizes the provided helm chart with security configuration required by OpenShift, and makes minor alterations to network policies to enable networking with the weave NPC and openshift-dns.

Otherwise for setting up alternative notebook environments, checkout:

- [RedHat OpenShift Data Science](https://www.redhat.com/en/technologies/cloud-computing/openshift/openshift-data-science) or the OpenShift
- [OpenDataHub](https://opendatahub.io/) operator.

## Additional resources about Jupyter on OpenShift

- An excellent series of OpenShift blog posts on Jupyter and OpenShift
  authored by Red Hat developer, Graham Dumpleton, are
  available on the [OpenShift blog](https://cloud.redhat.com/blog/jupyter-openshift-using-openshift-data-analytics).
