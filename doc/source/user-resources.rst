.. _user-resources:

User Resources
==============

.. note::

   For a list of all the options you can configure with your helm
   chart, see the :ref:`helm-chart-configuration-reference`.

User resources include the CPU, RAM, and Storage which JupyterHub provides to
users. Most of these can be controlled via modifications to the Helm Chart.
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
``--size``:

.. code-block:: bash

   gcloud container clusters resize \
                <YOUR-CLUSTER-NAME> \
                --size <NEW-SIZE> \
                --zone <YOUR-CLUSTER-ZONE>

To display the cluster's name, zone, or current size, use the command:

.. code-block:: bash

   gcloud container clusters list

After resizing the cluster, it may take a couple of minutes for the new cluster
size to be reported back as the service is adding or removing nodes. You can
find the true count of currently 'ready' nodes using ``kubectl get node`` to
report the current ``Ready/NotReady`` status of all nodes in the cluster.
