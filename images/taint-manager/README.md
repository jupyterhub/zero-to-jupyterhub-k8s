# In Cluster Taint Manager

To add or remove taint of a node from a in-cluster pod.

## Compile

```
GOOS=linux GOARCH=amd64 go build -o taintmanager taintmanager.go
```

## Development and Debug

The dev/debug environment is setup by `tilt`. To start, run `tilt up`.

## Test

The `test` directory contains YAML files for deploy a pod with required permissions to run taintmanager.
Please change `namespace` field in `clusterrolebinding.yaml` before deploying to a cluster.

After deploying yaml files, run `kubectl cp` to copy compiled binary to the target pod and run the binary inside pod.
