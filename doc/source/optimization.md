# Optimizations

This page contains information and guidelines for improving the speed,
stability, and general optimization of your JupyterHub deployment.

To summarize, for a good autoscaling experience, we recommend you:
- Enable the continuous image puller, to prepare added nodes for arriving users
- Enable pod priority and add user placeholders, to scale up nodes ahead of real user arrivals
- Enable the user scheduler, to pack users tight on some nodes and let others become empty and scaled down
- Use a node pool dedicated to user pods, to avoid getting other pods on them that blocks scale down

A reasonable final configuration could look something like this:

```yaml
scheduling:
  userScheduler:
    enabled: true
  podPriority:
    enabled: true
  userPlaceholder:
    enabled: true
    replicas: 4
  userPods:
    nodeAffinity:
      matchNodePurpose: require

prePuller:
  continuous:
    enabled: true

cull:
  enabled: true
  timeout: 7200
  every: 300
```

## Pulling images before user arrives

If a user pod is scheduled on a node requesting a Docker image that isn't
available, the user will have to wait for it. If the image is large, the wait
can be 5 to 10 minutes. This commonly occur in two situations:

1. A new image is introduced (`helm upgrade`)

    With the *hook-image-puller* enabled (the default), the user images being
    introduced will be pulled to the nodes before hub pod is updated to utilize
    the new image. The name hook-image-puller is a technical name referring to
    how a [Helm hook](https://docs.helm.sh/developing_charts/#hooks) is used to
    accomplish this, a more informative name would had been
    *pre-upgrade-image-puller*.

    The hook-image-puller is enabled by default. To disable it, use the
    following snippet in your `config.yaml`:

    ```yaml
    prePuller:
      hook:
        enabled: false
    ```

2. A node is added (Cluster Autoscaler)

    The amount of nodes in a Kubernetes cluster can increase, either by manually
    scaling up the cluster size or by a cluster autoscaler. As new nodes will
    come fresh without any images on their disks, a user pod arriving to this
    node will be forced to wait while the image is pulled.

    With the *continuous-image-puller* enabled (disabled by default), the user's
    container image will be pulled when a new node is added. New nodes can for
    example be added manually or by a cluster autoscaler. The continuous
    image-puller uses a
    [daemonset](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)
    to force Kubernetes to pull the user image on all nodes as soon as a node is
    present.

    The continuous-image-puller is disabled by default. To enable it, use the
    following snippet in your `config.yaml`:

    ```yaml
    prePuller:
      continuous:
        # NOTE: if used with a Cluster Autoscaler, also add user-placeholders
        enabled: true
    ```

    It is important to realize that if the continuous-image-puller together with
    a Cluster Autoscaler (CA) won't guarantee a reduced wait time for users. It
    only helps if the CA scales up before real users arrive, but the CA will
    generally fail to do so. This is because it will only add a node if one or
    more pods won't fit on the current nodes but would fit more if a node is
    added, but at that point users are already waiting. To scale up nodes ahead
    of time we can use *user-placeholders*.

### Configuring the pulled images

The hook-image-puller and the continuous-image-puller has various sources to
know what images it should pull. These sources are all found in the values
provided with the Helm chart (that can be overridden with `config.yaml`) under
the following paths:

#### Relevant image sources
- `singleuser.image`
- `singleuser.profileList[].kubespawner_override.image`
- `singleuser.extraContainers[].image`
- `prePuller.extraImages[].someName`

#### Additional sources
- `singleuser.networkTools.image`
- `prePuller.pause.image`

For example, with the following configuration, three images would be pulled by
the image pullers.

```yaml
singleuser:
  image:
    name: jupyter/minimal-notebook
    tag: 2343e33dec46

prePuller:
  extraImages:
    ubuntu-xenial:
      name: ubuntu
      tag: 16.04
    myOtherImageIWantPulled:
      name: jupyter/datascience-notebook
      tag: 2343e33dec46
```

## Efficient Cluster Autoscaling

A [*Cluster
Autoscaler*](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler)
(CA) will help you add and remove nodes from the cluster. But the CA needs some
help to function well. Without help, it will both fail scale up before users
arrive and scale down nodes aggressively enough without disrupting users.

### Scaling up in time (user placeholders)

A *Cluster Autoscaler* (CA) will add nodes when pods don't fit on available
nodes but would fit if another node is added. But, this may lead to a long
waiting time for the pod, and as a pod can represent a user, it can lead to a
long waiting time for a user. There is now options to combat this.

With Kubernetes 1.11+ (that requires Helm 2.11+), [Pod Priority and
Preemption](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/)
was introduced. This allows pods with higher priority to preempt / evict pods
with lower priority if that would help the higher priority pod fit on a node.

This priority mechanism allows us to add dummy users or *user-placeholders* with
low priority that can take up resources until a real user with (higher priority)
requires it. At this time, the lower priority pod will get preempted to make
room for the high priority pod. This now evicted user-placeholder will now be
able to signal to the CA that it needs to scale up.

The user placeholders will have the same resources requests as the default user.
This means that if you have three user placeholders running, real users will
only need to wait for a scale up if more than three users arrive in an interval
of time less than it takes to make a node ready for use.

To use three user placeholders for example, that can do their job thanks to pod
priority, add the following configuration:


```yaml
scheduling:
  podPriority:
    enabled: true
  userPlaceholder:
    replicas: 3
```

For further discussion about user placeholders, see [@MinRK's excellent
post](https://discourse.jupyter.org/t/planning-placeholders-with-jupyterhub-helm-chart-0-8-tested-on-mybinder-org/213)
about it where he analyzed its introduction on mybinder.org.

IMPORTANT: Further settings may be required for successful use of the pod priority depending on how your cluster autoscaler is configured. This is know to work on GKE, but we don't know how it works on other cloud providers or kubernetes installation. See the [configuration reference](reference.html#scheduling-podpriority) for more details.

### Scaling down efficiently

Scaling up is the easy part, scaling down is harder. To scale down a node,
[certain technical
criteria](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md#what-types-of-pods-can-prevent-ca-from-removing-a-node)
needs to be met. The central one is that the node to be scaled down must be free
of pods that isn't allowed to be disrupted. Pods that are not allowed to be
disrupted are for example real user pods, various system pods, and some
JupyterHub pods (without a permissive
[PodDisruptionBudget](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/)).
Consider for example that you add a lot of users during the daytime. New nodes
are added by the CA. Some system pod ends up on the new nodes along with the
user pods for some reason. At night when the
[*culler*](user-management.html#culling-user-pods) has removed many inactive
pods by some nodes was free from users but there was still a single system pod
stopping the CA from removing it.

To avoid these scale down failures, we recommend using a *dedicated node pool*
for the user pods. To accomplish this, we can use [*taints and
tolerations*](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/).
If we add a taint to all the nodes in the node pool, and a toleration on the
user pods to tolerate being scheduled on a tainted node, we have practically
dedicated the node pool to be used by user pods.

#### Using a user dedicated node pool

To make users schedule on a dedicated node for them, you need to do the following:

1. Setup a node pool (with autoscaling), a certain label, and a certain taint.

    How you do this will depend on the cloud provider, also note that cloud
    providers often have their own labels separate from kubernetes labels. This
    needs to be a kubernetes label.

    ```
    # label=value
    hub.jupyter.org/node-purpose=user
    
    # taint=value:effect (you may need to replace '/' with '_')
    hub.jupyter.org/dedicated=user:NoSchedule
    ```    

2. Make user pods require to be scheduled on the node pool setup above

    If you don't require the user pods to schedule on their dedicated node, you
    may fill up the nodes where the other software runs. This can cause a `helm
    upgrade` command to fail because you may have run out of resources for
    non-user pods that cannot schedule on the autoscaling node pool as they need
    during a rolling update for example.

    The default setting is to make user pods *prefer* schedule on nodes with the
    `hub.jupyter.org/node-purpose=user` label, but you can also make it
    *require* to do so using the configuration below.

    ```yaml
    scheduling:
      userPods:
        nodeAffinity:
          matchNodePurpose: require
    ```

NOTE: If you end up not using a dedicated node pool for users and want to scale
down efficiently, you will need to learn about PodDisruptionBudget and to quite
a bit more of work to avoid ending up with almost empty nodes not scaling down.

#### Using resources efficiently (the user scheduler)

If you have users coming online and others being culled by inactivity, but on
average you are needing less and less nodes. How will you free up a node so it
can be scaled down?

This is what the user scheduler can do for you. It will schedule users to the
most utilized node, allowing the underutilized nodes to free up. To see this in
action, look at the following graph showing the amount of users on five
different nodes from the mybinder.org deployment. Five nodes were running, but
only about three were really needed.

[![](_static/images/user_scheduler.png)](_static/images/user_scheduler.png)

To enable the user scheduler:

```yaml
scheduling:
  userScheduler:
    enabled: true
```
