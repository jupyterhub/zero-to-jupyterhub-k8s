# Security Considerations

## Role Based Access Control (RBAC)

Kubernetes supports (and often requires) using
[Role Based Access Control (RBAC)](https://kubernetes.io/docs/admin/authorization/rbac/) 
to secure which pods / users can perform what kinds of actions on the cluster.
If RBAC is disabled, all pods are given `root` equivalent permission on the
Kubernetes cluster and all the nodes in it, which is bad!

As of v0.5, the helm chart can natively work with RBAC enabled clusters. We ship
appropriate minimal RBAC rules for the various components we use. If you want to
disable the RBAC rules for whatever reason, you can do so with the following
snippet in your config.yaml:

```yaml
rbac:
   enabled: false
```
