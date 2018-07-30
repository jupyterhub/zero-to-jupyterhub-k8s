# Speed and Optimization

This page contains information and guidelines for improving the speed,
stability, and general optimization of your JupyterHub deployment.

## Pre-pulling images

If a user is scheduled on a node requesting an image that isn't available, the
user will have to wait. If the image is large, the wait can be 5 to 10 minutes.
This can happen for two reasons.

1. A new image is introduced during a `helm upgrade`

With the `hook-image-puller` puller enabled, images will be pulled to the nodes
before the actual `helm upgrade` thanks to a [Helm
hook](https://docs.helm.sh/developing_charts/#hooks).

```yaml
prePuller:
  hook:
    enabled: false
```

2. A new node was added

CONTINUE FROM HERE ... Cluster size can change through manual addition of nodes or autoscaling. When a
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
