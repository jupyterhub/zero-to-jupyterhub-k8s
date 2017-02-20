JupyterHub Kubernetes Autoscaler
===================================

### Definitions

**Critical Service=** Pods whose names start with `hub, proxy, statsd`

**Omitted Namespace=** Default name space, `kube-system` namespace

**Omitted Service=** Pods whose names start with `cull`

**Workload=**  On a node, number of pods that do not belong to `Critical Service`, do not belong to `Omitted Service`, and do not belong to `Omitted Namespace`

**Capacity=** Defined number of pods that can run on a single node; the value is 0 for nodes running `Critical Service` and nodes marked `Unschedulable`

**Utilization=** On certain nodes, the ratio between the sum of `Workload` and the sum of `Capacity`

### Expected Behavior

When `scale.py` is exected

1. The autoscaler will calculate the **Utilization** of the cluster.
2. If the **Utilization** of the cluster is between a **predefined minimum** and a **predefined maximum**, move the `Unschedulable` flag provided by Kubernetes between nodes, to make them deleted as soon as possible. Otherwise, the autoscaler will add or remove `Unschedulable` flags to approximate a **predefined optimal utilization**; if optimal utilization is not reached, new nodes can be created to meet the goal, to the predefined **maximum number of nodes**.
**2a. Nodes running `critical service` will never be marked unschedulable**.
3. Make sure there are at least **predefined minimum number** of nodes schedulable by removing flags or add new nodes.
4. Shutdown all empty unschedulable nodes

### How to run

0. Read `settings.py` to make sure you like the current settings.
1. Ensure a kubectl proxy **running in the context you want to scale** is listening at `http://API_HOST:API_PORT/`, both values were defined in `settings.py`. By default, it is `http://localhost:18080`. See `https://kubernetes.io/docs/user-guide/kubectl/kubectl_proxy/` for details.
2. Run `scale.py`, a one-time scaling should happen, and the script will quit.

### Requirements

Python 2 or 3, with `requests` installed;

Kubernetes, with `kubectl` added in `$PATH`;

Google Cloud SDK, with `gcloud` added in `$PATH`;

Necessary privilege or credentials.

### Supported Service Providers

Only Google Cloud Platform is supported for booting and shutting down nodes for now.
