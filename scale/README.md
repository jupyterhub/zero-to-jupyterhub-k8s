JupyterHub Kubernetes Autoscaler
===================================

### Settings

Settings for the autoscaler should be loaded through environment variables. They are defined as follows:

`MAX_UTILIZATION`, `MIN_UTILIZATION`, `OPTIMAL_UTILIZATION` refer to the minimum, maximum and optimal utilization rate. They are by default set to 0.85, 0.65, 0.75.

`MIN_NODES`, `MAX_NODES` refer to an additional bound of the number of nodes. They are by default set to 3 and 72.

`PREEMPTIBLE_LABELS` are a list of label keys in Kubernetes. Pods with these label keys are dynamic, expected to be created and deleted when the workload changes. Using `':'` as the delimiter, the list should have such a format: `jupyter:student:notebook`. **Despite the name, in the current version these pods will not be preempted in any case.** This list is by default empty.

`OMIT_LABELS`, `OMIT_NAMESPACES` are lists of label keys and namespace names. Pods with the given label keys or in the given namespaces **will not be taken into account at all** by the autoscaler. Using `':'` as the delimiter, the list should have such a format: `jupyter:student:notebook`. They are by default set to `""` and `"kube-system"`.


### Definitions

**Critical Pods** = Pods that are not omitted or assigned a label indicating that they are "preemptible".

**Workload** =  The sum of memory requests of pods that are not omitted.

**Capacity** = Total memeory of the cluster

**Utilization** = On certain nodes, the ratio between the sum of `Workload` and the sum of `Capacity`

### Expected Behavior

When `scale.py` is exected

1. The autoscaler will calculate the **Utilization** of the cluster.
2. If the **Utilization** of the cluster is between a **predefined minimum** and a **predefined maximum**, move the `Unschedulable` flag provided by Kubernetes between nodes, to make them deleted as soon as possible. Otherwise, the autoscaler will add or remove `Unschedulable` flags to approximate a **predefined optimal utilization**; if optimal utilization is not reached, new nodes can be created to meet the goal, to the predefined **maximum number of nodes**.
**2a. Nodes running `critical pods` will never be marked unschedulable**.
3. Make sure there are at least **predefined minimum number** of nodes schedulable by removing flags or add new nodes.
4. Shutdown all empty and unschedulable nodes

### How to run

0. Read `settings.py` to make sure you like the current settings.
1. Run `scale.py`, a one-time scaling should happen, and the script will quit.

### Requirements

Python 3, with `kubernetes` installed;

Google Cloud client `google-api-python-client`;

Necessary privilege or credentials.

### Supported Service Providers

Only Google Cloud Platform is supported for booting and shutting down nodes for now.
