Debugging Kubernetes
====================

Sometimes your Kubernetes deployment doesn't behave the way you'd expect.
This section provides some tips on debugging and fixing some common problems.

Debugging commands
------------------
In order to debug your Kubernetes deployment, you need to be able to inspect
the state of the pods are being used. The following are a few common commands
for debugging.

.. note::

   You may need to add ``--namespace=<YOUR_NAMESPACE>`` in order for the
   following commands to work.

``kubectl get pod``
^^^^^^^^^^^^^^^^^^^
In order to list all pods in your Kubernetes deployment, use the following
command::

    kubectl get pod

This will output a list of all of the pods being used in the deployment. This
includes two pods for the JupyterHub infrastructure (``hub-deployment`` and
``proxy-deployment``) as well as any user pods that have been created as users
log in.

In particular, investigate the ``STATUS`` column. If a given
pod contains something other than ``Running``, then something may be wrong.

If you suspect something is wrong with a pod, try the following
command.

``kubectl describe pod``
^^^^^^^^^^^^^^^^^^^^^^^^
To see more detail about the state of a specific pod, use the following
command::

    kubectl describe pod <POD_NAME>

This will output several pieces of information, including the logs for recent
activity on this pod.

``kubectl logs``
^^^^^^^^^^^^^^^^
If you only want to see the latest logs for a pod, use the following command::

    kubectl logs <POD_NAME>

This will output a list of the recent events for the pod. Parse these logs
to see if something is generating an error.

Error messages
--------------
