# Speed and Optimization

This page contains information and guidelines for improving the speed,
stability, and general optimization of your JupyterHub deployment.

## Picking a Scheduler Strategy

Kubernetes offers very flexible ways to determine how it distributes pods on
your nodes. The JupyterHub helm chart supports two common configurations, see
below for a brief description of each.

### Spread

* **Behavior**: This spreads user pods across **as many nodes as possible**.
* **Benefits**: A single node going down will not affect too many users. If you
  do not have explicit memory & cpu limits, this strategy also allows your users
  the most efficient use of RAM & CPU.
* **Drawbacks**: This strategy is less efficient when used with autoscaling.

This is the default strategy. To explicitly specify it, use the following in
your `config.yaml`:

```yaml
singleuser:
  schedulerStrategy: spread
```

### Pack

* **Behavior**: This packs user pods into **as few nodes as possible**.
* **Benefits**: This reduces your resource utilization, which is useful in
  conjunction with autoscalers.
* **Drawbacks**: A single node going down might affect more user pods than using
  a "spread" strategy (depending on the node).

When you use this strategy, you should specify limits and guarantees for memory
and cpu. This will make your users' experience more predictable.

To explicitly specify this strategy, use the following in your `config.yaml`:

```yaml
singleuser:
  schedulerStrategy: pack
```

## Pre-pulling

Pulling a user's images to a node forces a user to wait before the user's server
is started. Sometimes, the wait can be 5 to 10 minutes. **Pre-pulling** the
images on all the nodes can cut this wait time to a few seconds. Let's look at
how pre-pulling works.

### Hook - image pulling before upgrades

With the **pre-pulling hook**, which is enabled by default, the user's container
image is pulled on all nodes whenever a `helm install` or `helm upgrade` is
performed. While this causes `helm install` and `helm upgrade` to take several
minutes as the update is scheduled after the pulling has completed, the users
waiting time will decrease and become more reliable.

With the default helm upgrade settings, a `helm install` or `helm upgrade` will
allow 5 minutes of image pulling before timing out. This wait time is
configurable by passing the `--wait <seconds>` flag to the `helm` commands.

We recommend using pre-pulling. For the rare cases where you have a good reason
to disable it, pre-pulling can be disabled. To disable the pre-pulling during
`helm install` and `helm upgrade`, you can use the following snippet in your
`config.yaml`:


```yaml
prePuller:
  hook:
    enabled: false
```

### Continuous - image pulling for added nodes

Cluster size can change through manual addition of nodes or autoscaling. When a
new node is added to the cluster, the new node does not yet have the user image.
A user using this new node would be forced to wait while the image is pulled
from scratch. Ideally, it would be helpful to pre-pull images when the new node
is added to the cluster.

With the **continuous pre-puller** enabled (disabled by default), the user's
container image will be pre-pulled when a new node is added. New nodes can for
example be added manually or by a cluster autoscaler. The **continuous
pre-puller** uses a
[daemonset](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)
to force kubernetes to pull the user image on all nodes as soon as a node is
present. The continuous pre-puller uses minimal resources on all nodes and
greatly speeds up the user pod start time.

The continuous pre-puller is disabled by default. To enable it, use the
following snippet in your `config.yaml`:

```yaml
prePuller:
  continuous:
    enabled: true
```

### Pre-pulling additional images

By default, the pre-puller only pulls the singleuser image & the networktools
image (if access to cloud metadata is disabled). If you have customizations that
need additional images present on all nodes, you can ask the pre-puller to also
pull an arbitrary number of additional images.

```yaml
prePuller:
  extraImages:
    ubuntu-xenial:
      name: ubuntu
      tag: 16.04
      policy: IfNotPresent
```

This snippet will pre-pull the `ubuntu:16.04` image on all nodes, for example.
You can pre-pull any number of images.
