(google-cloud)=

# Kubernetes on [Google Cloud](https://cloud.google.com/) (GKE)

[Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine/)
(GKE) is the simplest and most common way of setting
up a Kubernetes Cluster. You may be able to receive [free credits](https://cloud.google.com/free/) for trying it out (though note that a
free account [comes with limitations](https://cloud.google.com/free/docs/free-cloud-features#free-tier-usage-limits)).
Either way, you will need to connect your credit card or other payment method to
your google cloud account.

1. Go to [console.cloud.google.com](https://console.cloud.google.com) and log in.

   ```{note}
   Consider [setting a cloud budget](https://cloud.google.com/billing/docs/how-to/budgets)
   for your Google Cloud account in order to make sure you don't accidentally
   spend more than you wish to.
   ```

2. Go to and enable the [Kubernetes Engine API](https://console.cloud.google.com/apis/api/container.googleapis.com/overview).
3. Choose a terminal.

   You can either to use a web based terminal or install and run the required
   command line interfaces on your own computer's terminal. We recommend
   starting out by using the web based terminal. Choose one set of instructions
   below.

   1. **Use a web based terminal:**

      Start _Google Cloud Shell_ from [console.cloud.google.com](https://console.cloud.google.com) by clicking the button shown below.
      You are now in control of a virtual machine with various tools
      preinstalled. If you save something in a user folder they will remain
      available to you if you return at a later stage. Additional documentation
      about Google Cloud shell is available [here](https://cloud.google.com/shell/docs/)

      ```{image} ../../_static/images/google/start_interactive_cli.png
      :align: center
      ```

   2. **Use your own computer's terminal:**

      1. Download and install the `gcloud` command line tool at its [install
         page](https://cloud.google.com/sdk/docs/install). It will help you
         create and communicate with a Kubernetes cluster.
      2. Install `kubectl` (reads _kube control_), it is a tool for controlling
         Kubernetes clusters in general. From your terminal, enter:

         ```
         gcloud components install kubectl
         ```

4. Create a managed Kubernetes cluster and a default node pool.

   Ask Google Cloud to create a managed Kubernetes cluster and a default [node
   pool](https://cloud.google.com/kubernetes-engine/docs/concepts/node-pools)
   to get nodes from. _Nodes_ represents hardware and a _node pool_ will
   keep track of how much of a certain type of hardware that you would like.

   ```
   gcloud container clusters create \
     --machine-type n1-standard-2 \
     --num-nodes 2 \
     --zone <compute zone from the list linked below> \
     --cluster-version latest \
     <CLUSTERNAME>
   ```

   - Replace `<CLUSTERNAME>` with a name that can be used to refer to this cluster
     in the future.
   - `--machine-type` specifies the amount of CPU and RAM in each node within
     this default node pool. There is a [variety of types](https://cloud.google.com/compute/docs/machine-resource) to choose from.
   - `--num-nodes` specifies how many nodes to spin up. You can change this
     later through the cloud console or using the `gcloud` command line tool.
   - `--zone` specifies the data center zone where your cluster will be created.
     You can pick something from [this list](https://cloud.google.com/compute/docs/regions-zones/#available)
     that is not too far away from your users.
   - A region in GCP is a geographical region with at least three zones, where each zone is representing a datacenter with servers etc.
     - A regional cluster creates pods across zones in a region(three by default), distributing Kubernetes resources across multiple zones in the region. This is different from the default cluster, which has all its resources within a single zone(as shown above).
     - A regional cluster has Highly Available (HA) kubernetes api-servers, this allows jupyterhub which uses them to have no downtime during upgrades of kubernetes itself.
     - They also increase control plane uptime to 99.95%.
     - To avoid tripling the number of nodes while still having HA kubernetes, the `--node-locations` flag can be used to specify a single zone to use.

5. To test if your cluster is initialized, run:

   ```
   kubectl get node
   ```

   The response should list two running nodes (or however many nodes you
   set with `--num-nodes` above).

6. Give your account permissions to perform all administrative actions needed.

   ```
   kubectl create clusterrolebinding cluster-admin-binding \
     --clusterrole=cluster-admin \
     --user=<GOOGLE-EMAIL-ACCOUNT>
   ```

   Replace `<GOOGLE-EMAIL-ACCOUNT>` with the exact email of the Google account
   you used to sign up for Google Cloud.

   Did you enter your email correctly? If not, you can run `kubectl delete clusterrolebinding cluster-admin-binding` and do it again.

7. [optional] Create a node pool for users

   This is an optional step, for those who want to separate
   user pods from "core" pods such as the Hub itself and others.
   See {ref}`optimization` for details on using a dedicated user node pool.

   The nodes in this node pool are for the users only. The node pool has
   autoscaling enabled along with a lower and an upper scaling limit. This
   means that the amount of nodes is automatically adjusted along with the
   amount of users scheduled.

   The `n1-standard-2` machine type has 2 CPUs and 7.5 GB of RAM each of which
   about 0.2 CPU will be requested by system pods. It is a suitable choice for a
   free account that has a limit on a total of 8 CPU cores.

   Note that the node pool is _tainted_. Only user pods that are configured
   with a _toleration_ for this taint can schedule on the node pool's nodes.
   This is done in order to ensure the autoscaler will be able to scale down
   when the user pods have stopped.

   ```
   gcloud beta container node-pools create user-pool \
     --machine-type n1-standard-2 \
     --num-nodes 0 \
     --enable-autoscaling \
     --min-nodes 0 \
     --max-nodes 3 \
     --node-labels hub.jupyter.org/node-purpose=user \
     --node-taints hub.jupyter.org_dedicated=user:NoSchedule \
     --zone us-central1-b \
     --cluster <CLUSTERNAME>
   ```

   <!---
   preemptible node recommendation not included
   pending handling of evictions in jupyterhub/kubespawner#223
   -->

   ```{note}
   Consider adding the ``--preemptible`` flag to reduce the cost
   significantly. You can `compare the prices here
   <https://cloud.google.com/compute/docs/machine-types>`_. See
   the `preemptible node documentation
   <https://cloud.google.com/compute/docs/instances/preemptible>`_ for more
   information.
   ```

Congrats. Now that you have your Kubernetes cluster running, it's time to
begin {ref}`setup-helm`.
