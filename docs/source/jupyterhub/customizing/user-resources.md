(user-resources)=

# Customizing User Resources

```{note}
For a list of all the Helm chart options you can configure, see the
{ref}`helm-chart-configuration-reference`.
```

User resources include the CPU, RAM, and Storage which JupyterHub provides to
users. Most of these can be controlled via modifications to the Helm chart.
For information on deploying your modifications to the JupyterHub deployment,
see {ref}`apply-config-changes`.

Since JupyterHub can serve many different types of users, JupyterHub managers
and administrators must be able to flexibly **allocate user resources**, like
memory or compute. For example, the Hub may be serving power users with large
resource requirements as well as beginning users with more basic resource
needs. The ability to customize the Hub's resources to satisfy both user
groups improves the user experience for all Hub users.

(memory-cpu-limits)=

## Set user memory and CPU guarantees / limits

Each user on your JupyterHub gets a slice of memory and CPU to use. There are
two ways to specify how much users get to use: resource _guarantees_ and
resource _limits_.

A resource _guarantee_ means that all users will have _at least_ this resource
available at all times, but they may be given more resources if they're
available. For example, if users are _guaranteed_ 1G of RAM, users can
technically use more than 1G of RAM if these resources aren't being used by
other users.

A resource _limit_ sets a hard limit on the resources available. In the example
above, if there were a 1G memory limit, it would mean that users could use
no more than 1G of RAM, no matter what other resources are being used on the
machines.

By default, each user is _guaranteed_ 1G of RAM. All users have _at least_ 1G,
but they can technically use more if it is available. You can easily change the
amount of these resources, and whether they are a _guarantee_ or a _limit_, by
changing your `config.yaml` file. This is done with the following structure.

```yaml
singleuser:
  memory:
    limit: 1G
    guarantee: 1G
```

This sets a memory limit and guarantee of 1G. Kubernetes will make sure that
each user will always have access to 1G of RAM, and requests for more RAM will
fail (your kernel will usually die). You can set the limit to be higher than
the guarantee to allow some users to use larger amounts of RAM for
a very short-term time (e.g. when running a single, short-lived function that
consumes a lot of memory).

Similarly, you can limit CPU as follows:

```yaml
singleuser:
  cpu:
    limit: .5
    guarantee: .5
```

This would limit your users to a maximum of .5 of a CPU (so 1/2 of a CPU core), as well as guarantee them that same amount.

```{note}
Remember to {ref}`apply the change <apply-config-changes>` after changing your `config.yaml` file!
```

## Set user GPU guarantees / limits

It is possible to allocate GPUs to your user. This is useful for heavier
workloads, such as deep learning, that can take advantage of GPUs.

For example, to create a profile that allocates one NVIDIA GPU:

```yaml
singleuser:
  profileList:
    - display_name: "GPU Server"
      description: "Spawns a notebook server with access to a GPU"
      kubespawner_override:
        extra_resource_limits:
          nvidia.com/gpu: "1"
```

This assumes that at least one of your Kubernetes nodes has compatible GPUs
attached. The method for doing this differs according to your infrastructure
provider. Here are a few links to help you get started:

- [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine/docs/how-to/gpus)
- [Amazon Elastic Kubernetes Service (EKS)](https://aws.amazon.com/blogs/compute/running-gpu-accelerated-kubernetes-workloads-on-p3-and-p2-ec2-instances-with-amazon-eks/)
- [Azure Kubernetes Service (AKS)](https://learn.microsoft.com/en-us/azure/aks/gpu-cluster)

You will also need to deploy the k8s-device-plugin following the instructions [here](https://github.com/NVIDIA/k8s-device-plugin#quick-start).

To check that your GPUs are schedulable by Kubernetes, you can run the following command:

```
kubectl get nodes -o=custom-columns=NAME:.metadata.name,GPUs:.status.capacity.'nvidia\.com/gpu'
```

## Modifying user shared memory size

It is also beneficial to increase the shared memory (SHM) allocation on pods
running workloads like deep learning. This is required for functions like
PyTorch's DataLoader to run properly.

The following configuration will increase the SHM allocation by mounting a
`tmpfs` (ramdisk) at `/dev/shm`, replacing the default 64MB allocation.

```yaml
singleuser:
  storage:
    extraVolumes:
      - name: shm-volume
        emptyDir:
          medium: Memory
    extraVolumeMounts:
      - name: shm-volume
        mountPath: /dev/shm
```

The volume `shm-volume` will be created when the user's pod is created,
and destroyed after the pod is destroyed.

Some important notes regarding SHM allocation:

- SHM usage by the pod will count towards its memory limit
- When the memory limit is exceeded, the pod will be evicted

## Modifying user storage type and size

See the {ref}`user-storage` for information on how to modify the type and
size of storage that your users have access to.

## Expanding and contracting the size of your cluster

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

### Google Cloud Platform

Use the `resize` command and
provide a new cluster size (i.e. number of nodes) as a command line option
`--num-nodes`:

```bash
gcloud container clusters resize \
    <YOUR-CLUSTER-NAME> \
    --num-nodes <NEW-SIZE> \
    --zone <YOUR-CLUSTER-ZONE>
```

To display the cluster's name, zone, or current size, use the command:

```bash
gcloud container clusters list
```

After resizing the cluster, it may take a couple of minutes for the new cluster
size to be reported back as the service is adding or removing nodes. You can
find the true count of currently 'ready' nodes using `kubectl get node` to
report the current `Ready/NotReady` status of all nodes in the cluster.

### Microsoft Azure Platform

Use the `scale` command and
provide a new cluster size (i.e. number of nodes) as a command line option
`--node-count`:

```bash
az aks scale \
    --name <YOUR-CLUSTER-NAME> \
    --node-count <NEW-SIZE> \
    --resource-group <YOUR-RESOURCE-GROUP>
```

To display the details of the cluster, use the command:

```bash
az aks show --name <YOUR-CLUSTER-NAME> --resource-group <YOUR-RESOURCE-GROUP>
```

It may take some time for the new cluster nodes to be ready.
You can use `kubectl get node` to report the current `Ready/NotReady` status of all nodes in the cluster.

### Amazon Web Services Elastic Kubernetes Service (EKS)

AWS EKS is an Amazon service providing an AWS-managed kubernetes control plane and a set of command-line tools, `eksctl`, to create and manager kubernetes clusters. It is but one way to deploy kubernetes with AWS infrastructure, but the following assumes that you have:

1. a kubernetes cluster on deployed on EKS
1. the `eksctl` command line tools [installed](https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html) and configured to point to your EKS cluster.

To scale an existing nodegroup using the `eksctl` command line tools:

```bash
eksctl scale nodegroup \
  -n <NODEGROUP-NAME> \
  --nodes <DESIRED-NUMBER-OF-NODES>\
  --nodes-max <MAX-NUMBER-OF-NODES>\
  --nodes-min <MIN-NUMBER-OF-NODES>\
  --cluster=<YOUR-CLUSTER-NAME>
```

If you have a cluster autoscaler set up, you can also create an autoscaling nodegroup with the `eksctl` command line tool.

```bash
eksctl create nodegroup \
  --cluster <YOUR-CLUSTER-NAME> \
  --name <NODEGROUP-NAME> \
  --node-type <EC2-INSTANCE-TYPE(S)> \
  --nodes-max <MAX-NUMBER-OF-NODES>\
  --nodes-min <MIN-NUMBER-OF-NODES>\
  --ssh-access \
  --ssh-public-key <PATH-TO-KEYPAIR-WITH-EKS-PERMISSIONS> \
  --node-zones <OPTIONALLY-SPECIFY-AVAILABILIYT-ZONE-FOR-NODES> \
  --tags "k8s.io/cluster-autoscaler/node-template/taint/<some-taint-key>=<some-taint-value>:<some-taint-effect>, k8s.io/cluster-autoscaler/node-template/label/<some-node-label-key>=<some-node-label-value>,k8s.io/cluster-autoscaler/<YOUR-CLUSTER-NAME>=true,k8s.io/cluster-autoscaler/enabled=true" \
  --node-labels "<some-node-label-key>=<some-node-label-value>,failure-domain.beta.kubernetes.io/zone=<AVAILABILITY-ZONE>,failure-domain.beta.kubernetes.io/region=<AVAILABILITY-REGION>"
```

The tags `k8s.io/cluster-autoscaler/<YOUR-CLUSTER-NAME>=<any-value-only-key-matters>` and `k8s.io/cluster-autoscaler/enabled=true` must be applied in order for the AWS cluster autoscaler to autoscale the nodegroup.

A `tag` must be added that corresponds to each of the `node-labels` that will be used as a `nodeSelector` when scheduling pods; with `node-labels` of the form `<some-node-label-key>=<some-node-label-value>`, these tags should be of the form `k8s.io/cluster-autoscaler/node-template/label/<some-node-label-key>=<some-node-label-value>`.

Taints can also be applied to the nodes in the nodegroup with tags of the form `k8s.io/cluster-autoscaler/node-template/taint/<some-taint-key>=<some-taint-value>:<some-taint-effect>`

Finally, the AWS region (e.g., `eu-west-1`) and availability zone (e.g., `eu-west-1a`) can be set with `node-labels`: `failure-domain.beta.kubernetes.io/region=<AVAILABILITY-REGION>` and `failure-domain.beta.kubernetes.io/zone=<AVAILABILITY-ZONE>`; and/or the `--node-zones` flag. Setting the availability zone is useful when singleUser pods could get scheduled to nodes in different availability zones; that scenario is problematic when using any `persistentVolume` storage backing that does not support mounting across availability zones (including the default `gp2` storage in AWS EKS). In those cases, the `PV` gets created in the availability zone of the node to which the user's pod is first scheduled and errors occur if in the future the same user pod is scheduled in a different availbility zone. Avoid this by controlling the zone to which `nodegroups` are deployed and/or by specifying an availability zone for the volumes in a custom `StorageClass` referenced in your `values.yaml`.
