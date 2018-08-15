# Continuous Integration (CI)
Allows you to run tests on your own machine as well as automatically when
submitting a PR to the repo.

```sh
# Downloads binaries, lints and verifies helm templates and their output, sets
# up a minikube cluster, builds chart and images, install chart and runs tests.
ci/run


# Allow you to access the in-repo cluster with kubectl, minikube and helm, as
# they are installed and configured in-repo this is what you need to do.
source ci/0-setup-env

# should return a binary within the repo's bin folder
which kubectl

kubectl get pods

# FIXME: It may be that we need to call source ci/4-setup-cluster-env as well in
# order to access the DOCKER environment variables setup by `eval $(minikube
# docker-env)`, but I'm not confident if that will be important. It probably is
# useful... I suggest we fix this by removing 4-setup-cluster-env but instead
# reinvoking 0-setup-env as a fourth runtime step where we implement that code
# which must be allowed to fail as it will also be called when the cluster isn't
# yet setup.


# Clean up of the in-repo folders .kube/, .minikube/ and .helm/ and deletion of
# the minikube cluster.
ci/cleanup
```

## About the vagrant files
They are currently not up to date and were a previous way to do some CI.
