.. _helm-chart-schema:

Helm Chart Schema
-----------------

The `JupyterHub helm chart <https://github.com/jupyterhub/zero-to-jupyterhub-k8s>`_
is configurable so that you can customize your
Kubernetes setup however you'd like. You can extend user resources, build
off of different Docker images, manage security and authentication, and more.
You can find [a JSON schema](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/master/jupyterhub/schema.yaml)
with reference documentation detailing all the fields in the repository.

For more detailed information about some specific things you can do
with modifications to the helm chart, see the :ref:`extending-jupyterhub` and
:ref:`user_experience` pages.
