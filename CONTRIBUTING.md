# Contributing

Welcome dear open source colleague! As this is a [Jupyter](https://jupyter.org)
project please start by looking at the [Jupyter contributor
guide](https://jupyter.readthedocs.io/en/latest/contributing/content-contributor.html),
and follow [Project Jupyter's Code of
Conduct](https://github.com/jupyter/governance/blob/master/conduct/code_of_conduct.md)
to help us sustain a warm and welcoming collaborative environment.

If you don't have [git](https://www.git-scm.com/) already, install it and clone
this repository.

```shell
git clone https://github.com/jupyterhub/zero-to-jupyterhub-k8s
```

# Setting up for documentation development

See [doc/README.md](doc/README.md).

# Setting up for Helm chart development



## 1: Prerequisites

This needs to be installed:

- [docker](https://docs.docker.com/get-docker/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (also [setup tab completion](https://kubernetes.io/docs/tasks/tools/install-kubectl/#enabling-shell-autocompletion))
- [helm](https://helm.sh/docs/intro/install/) (also [setup tab completion](https://helm.sh/docs/helm/helm_completion/))
- Python 3.6+ (install at [Anaconda.com](https://www.anaconda.com/distribution/) or [Python.org](https://www.python.org/downloads/)) and dependencies:
  ```shell
  pip install -r dev-requirements.txt
  pip install -r doc/doc-requirements.txt
  ```

You can check if you have it all like this:

```shell
docker --version
kubectl version --client
helm version
pytest --version
chartpress --version
```

## 2: Setup a Kubernetes cluster

We need a Kubernetes cluster to work against.
If you are using Linux you can either install [k3s](#linux-only-kubernetes-setup-with-k3s) or [k3d](#linux-mac-and-maybe-windows-kubernetes-setup-with-k3d).
For all other operating systems install [k3d](#linux-mac-and-maybe-windows-kubernetes-setup-with-k3d).

### Linux only: Kubernetes setup with k3s

With [k3s](https://github.com/rancher/k3s) we can _quickly_ create a Kubernetes
cluster, and we _don't have to transfer docker images_ built on our computer to
make them available in the Kubernetes cluster.

__Install__

```shell
# Installs a ~50 MB k3s binary, setups and starts a systemctl service called
# k3s which is also enabled to run on startup, provides a k3s-uninstall.sh
# script, disables not needed functionality. You will be asked for sudo rights.
curl -sfL https://get.k3s.io | sh -s - \
    --write-kubeconfig-mode=644 \
    --disable metrics-server \
    --disable traefik \
    --disable local-storage \
    --disable-network-policy \
    --docker

# Ensure kubectl will work with our k3s cluster
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
```

__Start/Stop and Enable/Disable__

With `systemctl` you can `start` and `stop` the service named `k3s` representing
the cluster, as well as `enable` and `disable` the service's automatic startup
with your computer.

At the moment, there is a workaround making us need to run `docker stop` due to [this issue](https://github.com/rancher/k3s/issues/1469) to fully stop.

```shell
sudo systemctl stop k3s
docker stop $(docker container list --quiet --filter "name=k8s_")
```

__Debug__

```shell
# what is the status of the k3s service?
sudo systemctl status k3s

# what logs have the k3s service generated recently?
journalctl -u k3s --since "1 hour ago"

# what containers are running?
docker container list --filter "name=k8s_"
```

__Uninstall__

When k3s was installed with the installation script, an uninstallation script is
made available as well.

At the moment, there is a workaround needed while uninstalling.

```shell
k3s-uninstall.sh
# ... and a temporary workaround of https://github.com/rancher/k3s/issues/1469
docker stop $(docker container list --all --quiet --filter "name=k8s_") | xargs docker rm
```

### Linux, Mac, and possibly Windows: Kubernetes setup with k3d

[k3d](https://github.com/rancher/k3d) encapsulates k3s in containers. It is less
mature than [k3s](https://github.com/rancher/k3s) and will require locally built
docker images to be pushed to a dedicated registry before they can be accessed
by the pods in the Kubernetes cluster, until [this
issue](https://github.com/rancher/k3d/issues/113) is resolved.

__Install__

```shell
k3d create --publish 30443:30443 --publish 32444:32444 --wait 60 \
   --enable-registry --registry-name local.jovyan.org \
   --server-arg --no-deploy=metrics-server \
   --server-arg --no-deploy=traefik \
   --server-arg --no-deploy=local-storage \
   --server-arg --disable-network-policy \
   --server-arg --flannel-backend=none

# For Linux/Mac:
export KUBECONFIG="$(k3d get-kubeconfig --name='k3s-default')"
. ci/common    # provides the setup_calico function
setup_calico

# For Windows:
# These instructions aren't maintained, you need to figure it out yourself =/
```

__About the published ports__
- 30443: This port exposes the `proxy-public` service. It will route to the
         `autohttps` pod for TLS termination, then onwards to the `proxy` pod
         that routes to the `hub` pod or individual user pods depending on paths
         (`/hub` vs `/user`) and how JupyterHub dynamically has configured it.
- 32444: This port exposes the `pebble` service which which accepts two ports,
         and this specific port will route to the `pebble` pod's management API
         where we can access paths like `/roots/0`. For more details about
         Pebble which we use as a local ACME server, see the section below and
         https://github.com/jupyterhub/pebble-helm-chart.

__Stop__

```shell
k3d delete
```

## 3: Install a local ACME server

Testing automatic TLS certificate acquisition with an ACME server like Let's
Encrypt from a local Kubernetes cluster is tricky. First you need a public
domain name registered and pointing to some public IP, and you need traffic to
that IP end up inside your Kubernetes cluster. In our Travis CI setup we must
install a local ACME server instead, and that is also recommended for local
development.

Pebble is a an ACME server like Let's Encrypt solely meant for testing purposes.
For more information, see
[jupyterhub/pebble-helm-chart](https://github.com/jupyterhub/pebble-helm-chart).

__Install Pebble__

```shell
helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
helm repo update
helm upgrade --install pebble jupyterhub/pebble --cleanup-on-fail --values dev-config-pebble.yaml
```

## 4: Build images, update values, install chart

This repository contains various `Dockerfile`s that are used to build docker images
required by the Helm chart. To help us build these docker images only when needed,
and to update the Helm chart's [values.yaml](jupyterhub/values.yaml) file to use
the most recent image, we rely on a command line tool called
[`chartpress`](https://github.com/jupyterhub/chartpress) that is installed as
part of [dev-requirements.txt](dev-requirements.txt).

Chartpress is configured through [chartpress.yaml](chartpress.yaml), and will
only rebuild images if their dependent files in their respective directories or
`chartpress.yaml` itself has changed.

1. Ensure the latest git tags are available locally, as `chartpress` uses them.

   ```shell
   git fetch origin --tags
   ```

1. Use [`chartpress`](https://github.com/jupyterhub/chartpress) to rebuild
   images that need to be rebuilt and update the chart's
   [values.yaml](jupyterhub/values.yaml) file with the appropriate image tags.

   ```shell
   # run this if you are using k3s, or generally when your Kubernetes cluster
   # can make direct use of your locally built images
   chartpress

   # run this if you are using k3d
   chartpress --image-prefix=local.jovyan.org:5000/ --push
   ```

1. Use `helm` to upgrade (or install) your local JupyterHub Helm chart.

   ```shell
   helm upgrade --install jupyterhub ./jupyterhub --cleanup-on-fail --values dev-config.yaml
   ```

   Note that `--cleanup-on-fail` is a very good practice to avoid `<resource
   name> already exist` errors in future upgrades following a failed upgrade.

## 5: Visit the JupyterHub

After all your pods are running and the `autohttps` pod succesfully has acquired
a certificate from the `pebble` pod acting as an ACME server, you should be able
to access https://local.jovyan.org:30443. Your browser will probably require you
to accept the TLS certificate as its signed an untrusted certificate authority.

Note that `local.jovyan.org` and its subdomains are Project Jupyter managed
domains pointing to the localhost IP of `127.0.0.1`, we use them to avoid
needing to add entries to `/etc/hosts`.

## 6: Run tests

The test suite runs outside your Kubernetes cluster.

```shell
pytest -vx ./tests
```

# Debugging

Various things can go wrong while working with the local development
environment, here are some typical issues and what to do about them.

## Basic debugging strategy in Kubernetes

A good debugging strategy is to start with the following steps.

1. Inspect the status of pods with `kubectl get pods`.
2. Inspect events and status of some pod with `kubectl describe pod <name>`.
3. Inspect a pod's container's logs with `kubectl logs ...`. Sometimes you need
   to specify `-c <container name>` or `--all-containers`. And sometimes you may
   want to specify the `--previous` flag to see the logs from the previous
   container run.

## HTTPS errors

Your browser is expected to complain about the TLS certificate when visiting
https://local.jovyan.org:30443 as its signed by an untrusted certificate
authority and shouldn't be trusted unless it is solely for testing purposes.

But if for example Chrome presents `ERR_SSL_PROTOCOL_ERROR` or Firefox presents
`SSL_ERROR_INTERNARROR_ALERT`, then the `autohttps` pod has probably failed to
acquire a TLS certificate from the ACME server.

```shell
# the certificate should be available here
kubectl exec -it deploy/autohttps -c traefik -- cat /etc/acme/acme.json

# these logs should contain "Register..."
kubectl logs deploy/autohttps -c traefik

# these logs should contain "Issued certificate"
kubectl logs deploy/pebble -c pebble
```

If the ACME client library used by Traefik in the autohttps pod attempted to
acquire the certificate from our ACME server (Pebble) before the Kubernetes
cluster's DNS server or Pebble and it's DNS server had started fully, it would
fail to acquire a certificate. For this situation, a restart of the autohttps
pod by `kubectl delete pod -l component=autohttps` will hopefully resolve the
issue. To avoid this in our CI system, we run the `await_dns` and `await_pebble`
scripts in `ci/common` before we install the JupyterHub Helm chart which will
startup the autohttps pod.

## Hub restarts

Have you seen the hub pod get a restart count > 0? JupyterHub 1.1.0 is typically
crashing after 20 seconds if it started up without the configurable proxy pod
available. This harmless error can be confirmed by doing a `kubectl logs
deploy/hub --previous` if you spot a message about a timeout after ~20 seconds in
the logs.

## Network errors

Did you get an error like one of these below?

```shell
# while running apt-get install while building a docker image with chartpress
E: Failed to fetch http://archive.ubuntu.com/ubuntu/pool/main/r/rtmpdump/librtmp1_2.4+20151223.gitfa8646d.1-1_amd64.deb  Could not connect to archive.ubuntu.com:80 (91.189.88.174). - connect (113: No route to host) Could not connect to archive.ubuntu.com:80 (91.189.88.31). - connect (113: No route to host) [IP: 91.189.88.174 80]
# [...]
subprocess.CalledProcessError: Command '['docker', 'build', '-t', 'jupyterhub/k8s-hub:0.9-217f798', 'images/hub', '--build-arg', 'JUPYTERHUB_VERSION=git+https://github.com/jupyterhub/jupyterhub@master']' returned non-zero exit status 100.

# while installing a dependency for our k8s cluster
Unable to connect to the server: dial tcp: lookup docs.projectcalico.org on 127.0.0.53:53: read udp 127.0.0.1:56409->127.0.0.53:53: i/o timeout
```

Network and DNS issues are typically symptoms of unreliable internet. You can
recognize such issues if you get errors like the ones above.

As you may notice, typical keywords associated with network errors are:

- *resolve host*
- *name resolution*
- *timeout*
- *no route to host*
