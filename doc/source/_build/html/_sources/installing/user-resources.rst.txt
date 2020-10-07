.. _user-resources:

Customizing User Resources
==========================

.. note::

   For a list of all the Helm chart options you can configure, see the
   :ref:`helm-chart-configuration-reference`.

User resources include the CPU, RAM, and Storage which JupyterHub provides to
users. Most of these can be controlled via modifications to the Helm chart.
For information on deploying your modifications to the JupyterHub deployment,
see :ref:`apply-config-changes`.

Since JupyterHub can serve many different types of users, JupyterHub managers
and administrators must be able to flexibly **allocate user resources**, like
memory or compute. For example, the Hub may be serving power users with large
resource requirements as well as beginning users with more basic resource
needs. The ability to customize the Hub's resources to satisfy both user
groups improves the user experience for all Hub users.


Set user memory and CPU guarantees / limits
-------------------------------------------

Each user on your JupyterHub gets a slice of memory and CPU to use. There are
two ways to specify how much users get to use: resource *guarantees* and
resource *limits*.

A resource *guarantee* means that all users will have *at least* this resource
available at all times, but they may be given more resources if they're
available. For example, if users are *guaranteed* 1G of RAM, users can
technically use more than 1G of RAM if these resources aren't being used by
other users.

A resource *limit* sets a hard limit on the resources available. In the example
above, if there were a 1G memory limit, it would mean that users could use
no more than 1G of RAM, no matter what other resources are being used on the
machines.

By default, each user is *guaranteed* 1G of RAM. All users have *at least* 1G,
but they can technically use more if it is available. You can easily change the
amount of these resources, and whether they are a *guarantee* or a *limit*, by
changing your ``config.yaml`` file. This is done with the following structure.

    .. code-block:: yaml

       singleuser:
         memory:
           limit: 1G
           guarantee: 1G

This sets a memory limit and guarantee of 1G. Kubernetes will make sure that
each user will always have access to 1G of RAM, and requests for more RAM will
fail (your kernel will usually die). You can set the limit to be higher than
the guarantee to allow some users to use larger amounts of RAM for
a very short-term time (e.g. when running a single, short-lived function that
consumes a lot of memory).

Similarly, you can limit CPU as follows:

    .. code-block:: yaml

       singleuser:
         cpu:
           limit: .5
           guarantee: .5

This would limit your users to a maximum of .5 of a CPU (so 1/2 of a CPU core), as well as guarantee them that same amount.

.. note::

   Remember to :ref:`apply the change <apply-config-changes>` after changing your ``config.yaml`` file!

Set user GPU guarantees / limits
--------------------------------

It is possible to allocate GPUs to your user. This is useful for heavier
workloads, such as deep learning, that can take advantage of GPUs.

For example, to create a profile that allocates one NVIDIA GPU:

    .. code-block:: yaml

       singleuser:
        profileList:
          - display_name: "GPU Server"
            description: "Spawns a notebook server with access to a GPU"
            kubespawner_override:
              extra_resource_limits:
                nvidia.com/gpu: "1"

This assumes that at least one of your Kubernetes nodes has compatible GPUs
attached. The method for doing this differs according to your infrastructure
provider. Here are a few links to help you get started:

- `Google Kubernetes Engine (GKE) <https://cloud.google.com/kubernetes-engine/docs/how-to/gpus>`_
- `Amazon Elastic Kubernetes Service (EKS) <https://aws.amazon.com/blogs/compute/running-gpu-accelerated-kubernetes-workloads-on-p3-and-p2-ec2-instances-with-amazon-eks/>`_
- `Azure Kubernetes Service (AKS) <https://cloud.google.com/kubernetes-engine/docs/how-to/gpus>`_

You will also need to deploy the k8s-device-plugin following the instructions `here <https://github.com/NVIDIA/k8s-device-plugin#quick-start>`_.

To check that your GPUs are schedulable by Kubernetes, you can run the following command:

    .. code-block:: none

       kubectl get nodes -o=custom-columns=NAME:.metadata.name,GPUs:.status.capacity.'nvidia\.com/gpu'

Modifying user shared memory size
---------------------------------

It is also beneficial to increase the shared memory (SHM) allocation on pods
running workloads like deep learning. This is required for functions like
PyTorch's DataLoader to run properly.

The following configuration will increase the SHM allocation by mounting a
:code:`tmpfs` (ramdisk) at :code:`/dev/shm`, replacing the default 64MB allocation.

    .. code-block:: yaml

       singleuser:
        storage:
          extraVolumes:
            - name: shm-volume
              emptyDir:
                medium: Memory
          extraVolumeMounts:
            - name: shm-volume
              mountPath: /dev/shm

The volume :code:`shm-volume` will be created when the user's pod is created, 
and destroyed after the pod is destroyed.

Some important notes regarding SHM allocation:

- SHM usage by the pod will count towards its memory limit
- When the memory limit is exceeded, the pod will be evicted

Modifying user storage type and size
------------------------------------

See the :ref:`user-storage` for information on how to modify the type and
size of storage that your users have access to.

Expanding and contracting the size of your cluster
--------------------------------------------------

You can easily scale up or down your cluster's size to meet usage demand or to
save cost when the cluster is not being used. This is particularly useful
when you have predictable spikes in usage. For example, if you are
organizing and running a workshop, resizing a cluster gives you a way
to save cost and prepare JupyterHub before the event. For example:

- **One week before the workshop:** You can create the cluster, set
  everything up, and then resize the cluster to zero nodes to save cost.
- **On the day of the workshop:** You can scale the cluster up to a suitable
  size for the workshop. This workflow also helps you avoid scrambling on
  the workshop day to set up the cluster and JupyterHub.
- **After the workshop:** The cluster can be deleted.

The following sections describe
how to resize the cluster on various cloud platforms.

Google Cloud Platform
~~~~~~~~~~~~~~~~~~~~~
Use the ``resize`` command and
provide a new cluster size (i.e. number of nodes) as a command line option
``--num-nodes``:

.. code-block:: bash

   gcloud container clusters resize \
       <YOUR-CLUSTER-NAME> \
       --num-nodes <NEW-SIZE> \
       --zone <YOUR-CLUSTER-ZONE>

To display the cluster's name, zone, or current size, use the command:

.. code-block:: bash

   gcloud container clusters list

After resizing the cluster, it may take a couple of minutes for the new cluster
size to be reported back as the service is adding or removing nodes. You can
find the true count of currently 'ready' nodes using ``kubectl get node`` to
report the current ``Ready/NotReady`` status of all nodes in the cluster.

Microsoft Azure Platform
~~~~~~~~~~~~~~~~~~~~~~~~
Use the ``scale`` command and
provide a new cluster size (i.e. number of nodes) as a command line option
``--node-count``:

.. code-block:: bash

   az aks scale \
       --name <YOUR-CLUSTER-NAME> \
       --node-count <NEW-SIZE> \
       --resource-group <YOUR-RESOURCE-GROUP>

To display the details of the cluster, use the command:

.. code-block:: bash

   az aks show --name <YOUR-CLUSTER-NAME> --resource-group <YOUR-RESOURCE-GROUP>

It may take some time for the new cluster nodes to be ready.
You can use ``kubectl get node`` to report the current ``Ready/NotReady`` status of all nodes in the cluster.
