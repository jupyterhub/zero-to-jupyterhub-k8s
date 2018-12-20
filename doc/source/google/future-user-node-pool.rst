.. A future step to be added

6. Create a node pool for the users.

   The nodes in this node pool are for the users. The node pool has
   autoscaling enabled along with a lower and an upper scaling limit. This
   means that the amount of nodes is automatically adjusted along with the
   amount of users scheduled.
   
   The `n1-standard-2` machine type has 2 CPUs and 7.5 GB of RAM each of which
   about 0.2 CPU will be requested by system pods. It is a suitable choice for a
   free account that has a limit on a total of 8 CPU cores.

   Note that the node pool is *tainted*. Only user pods that is configured
   with a *toleration* for this taint can schedule on the node pool's nodes.
   This is done in order to ensure the autoscaler will be able to scale down
   when the user pods have stopped.
  
   .. code-block:: bash

      gcloud beta container node-pools create user-pool \
        --machine-type n1-standard-2 \
        --num-nodes 0 \
        --enable-autoscaling \
        --min-nodes 0 \
        --max-nodes 3 \
        --node-labels hub.jupyter.org/node-purpose=user \
        --node-taints hub.jupyter.org_dedicated=user:NoSchedule

   .. note::

      Consider adding the ``--preemptible`` flag to reduce the cost
      significantly. You can `compare the prices here
      <https://cloud.google.com/compute/docs/machine-types>`_. See
      the `preemptible node documentation
      <https://cloud.google.com/compute/docs/instances/preemptible>`_ for more
      information.