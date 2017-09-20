.. _helm-chart-schema:

Helm Chart Schema
-----------------

The `JupyterHub helm chart <https://github.com/jupyterhub/helm-chart>`_
is configurable so that you can customize your
Kubernetes setup however you'd like. You can extend user resources, build
off of different Docker images, manage security and authentication, and more.

Below is a description of the fields that are exposed with the JupyterHub
helm chart. For more detailed information about some specific things you can do
with modifications to the helm chart, see the :ref:`extending-jupyterhub` and
:ref:`user_experience` pages.

.. literalinclude:: ../../jupyterhub/schema.yaml
   :language: yaml
   :linenos:
