# In Cluster Taint Manager

To add or remove taint within a pod. The default mode is to run as a pod in a Kubernetes cluster. It will try to
authenticate to K8S API server with in-cluster config (the service account token mounted inside pod). It also uses
downward API to retrieve the node name where the pod is running on in order to change the taint.

## Compile

```
GOOS=linux GOARCH=amd64 go build -o taintmanager taintmanager.go
```

## Development and Debug

To test outside a cluster, commandline parameter `-kubeconfig` and `-node` can be specified. If `-kubeconfig` is not
specified, taintmanager will try to load the kubeconfig from default path `HOME/.kube/config`

Using default kubeconfig:

```
taintmanager -node f6.workers.ctlt.ubc.ca -remove hub.jupyter.org/imagepulling:NoExecute
```

## Test in Cluster

The `test` directory contains YAML files for deploy a pod with required permissions to run taintmanager.
Please change `namespace` field in `clusterrolebinding.yaml` before deploying to a cluster.

After deploying yaml files, run `kubectl cp` to copy compiled binary to the target pod and run the binary inside pod.
