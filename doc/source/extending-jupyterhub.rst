.. _extending-jupyterhub:

Extending your JupyterHub setup
===============================

The helm chart used to install JupyterHub has a lot of options for you to tweak.
For a semi-complete list of the changes you can apply via your helm-chart,
see the :ref:`helm-chart-configuration-reference`.

.. _apply-config-changes:

Applying configuration changes
------------------------------

The general method to modify your Kubernetes deployment is to:

1. Make a change to your ``config.yaml``
2. Run a ``helm upgrade``:

     .. code-block:: bash

        helm upgrade <YOUR_RELEASE_NAME> jupyterhub/jupyterhub --version=v0.7 --values config.yaml

   Where ``<YOUR_RELEASE_NAME>`` is the parameter you passed to ``--name`` when
   `installing jupyterhub <setup-jupyterhub.html#install-jupyterhub>`_ with
   ``helm install``. If you don't remember it, you can probably find it by doing
   ``helm list``.
3. Wait for the upgrade to finish, and make sure that when you do
   ``kubectl --namespace=<YOUR_NAMESPACE> get pod`` the hub and proxy pods are
   in ``Ready`` state. Your configuration change has been applied!

For information about the many things you can customize with changes to
your helm chart, see :ref:`user-environment`, :ref:`user-resources`, and
:ref:`helm-chart-configuration-reference`.
