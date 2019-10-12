# Contributing

We are very pleased to have you as a contributor, and we hope you will find your
impact on the projects valuable. Thank you for sharing your interests, ideas,
and skills with us!

This is a [Jupyter](https://jupyter.org) project, so please start out by reading
the first page of the general [Jupyter contributor
guide](https://jupyter.readthedocs.io/en/latest/contributor/content-contributor.html).

## Local development

### 1: Preparations

Before anything else, install [git](https://www.git-scm.com/), clone the
repository, and enter the repository directory.

```
git clone https://github.com/jupyterhub/zero-to-jupyterhub-k8s
cd zero-to-jupyterhub-k8s
```

For local development, you will additional tools and we present you with two
options. Either you, a) start and work from a Virtual Machine that is
automatically prepared for development, or b) install the tools yourself and
work without a Virtual Machine.

#### a) Use a prepared Virtual Machine (VM)

1. Install VirtualBox by [downloading and running an
   installer](https://www.virtualbox.org/wiki/Downloads).

1. Install Vagrant by [downloading and running an
   installer](https://www.vagrantup.com/downloads.html).

1. Start a prepared VM and SSH into it.

   ```shell
   # if you have suspended a VM earlier, use "vagrat resume" instead
   vagrant up

   # enter a SSH session with the VM
   vagrant ssh

   # relocate to the repository folder that is mounted from outside the VM
   # IMPORTANT: changes to this folder will be seen outside your VM
   cd zero-to-jupyterhub-k8s
   ```

1. Do your development.

1. Exit and suspend the VM

   ```shell
   ## exit the SSH session
   exit
   vagrant suspend
   ```

   > **NOTE:** You can also use `vagrant destroy` to reset the VM state entirely.

#### b) Install tools yourself

This is what you need to install and make available on your PATH.

- [docker](https://docs.docker.com/install/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [helm](https://helm.sh/docs/using_helm/#installing-helm)
- [kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
- [kubeval](https://kubeval.instrumenta.dev/installation/)
- Python 3.6+ ([Anaconda.com](https://www.anaconda.com/distribution/), [Python.org](https://www.python.org/downloads/))
- Python dependencies installed
    - `dev-requirements.txt`
    - `doc/doc-requirements.txt`

To verify you got it all right, you should be able to run the following commands
without error.

```
git --version
docker --version
kubectl version --client
helm version --client
kind --version
kubeval --version
pytest --version
chartpress --version
```

### 2: Setup a Kubernetes cluster

You will now need a Kubernetes cluster to work with, and we present you with two
options again. Either you, a) use an automated script that starts and sets up a
Kubernetes cluster for you using [`kind`
(Kubernetes-in-Docker)](https://kind.sigs.k8s.io), or b), you start and setup
your own Kubernetes cluster.


#### a) Automated use of `kind`

```shell
# create and setup a local Kubernetes cluster
./dev kind create
```

> **NOTE:** You can also use the `--recreate` flag to recreate the cluster to
> get a clean slate, or first run `./dev kind delete`.

#### b) Self-managed Kubernetes cluster

- To be compatible with all test that currently are defined, your cluster need
  to have a network policy controller that enforces the network policies.
- To use `./dev upgrade` or `./dev test`, you will note that you need to
  explicitly declare the path of your Kubernetes config and what Kubernetes
  context to use. This is enforced to ensure the script only works on a
  Kubernetes cluster it is intended to work on.

### 3: Install or upgrade your local Helm chart

You have two options as usual to install or upgrade your local Helm chart,
either you a) use the automated script to install or upgrade, or you do it on
your own.

TODO: learn properly about the chartpress --commit-ranger flag.

#### a) Automated Helm chart install or upgrade

1. Install or upgrade your local Helm chart
   
   ```shell
   ./dev upgrade
   ```

1. Visit http://localhost:8080

#### b) Manual Helm chart install or upgrade

1. Use [`chartpress`](https://github.com/jupyterhub/chartpress) to rebuild
   modified images if needed but also update the chart's
   [values.yaml](jupyterhub/values.yaml) file with the appropriate image tags.

   ```shell
   chartpress --commit-range origin/master..HEAD
   ```

   > **NOTE:** If you use a kind cluster and have built new images that will
   > only available locally, you must also load them into the kind cluster using
   > the `kind load docker-image <image:tag>` command.

1. Use `helm` to install or upgrade your Helm chart.

   ```shell
   helm upgrade jh-dev ./jupyterhub --install --namespace jh-dev
   ```

1. Use `kubectl` to open up a network path to your cluster.

   ```shell
   kubectl port-forward --namespace jh-dev service/proxy-public 8080:80
   ```

1. Visit http://localhost:8080

### 4: Run tests

```shell
./dev test
```

## Debugging issues

Various things can go wrong while working with the local development
environment, here are some typical issues and what to do about them.

### Network errors

Did you get an error like one of these below?

```shell
# while installing docker
curl: (6) Could not resolve host: download.docker.com

# while running pip install
Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x7f420fd81080>: Failed to establish a new connection: [Errno -3] Temporary failure in name resolution',)': /simple/chartpress/

# while running apt-get install while building a docker image with chartpress
E: Failed to fetch http://archive.ubuntu.com/ubuntu/pool/main/r/rtmpdump/librtmp1_2.4+20151223.gitfa8646d.1-1_amd64.deb  Could not connect to archive.ubuntu.com:80 (91.189.88.174). - connect (113: No route to host) Could not connect to archive.ubuntu.com:80 (91.189.88.31). - connect (113: No route to host) [IP: 91.189.88.174 80]
# [...]
subprocess.CalledProcessError: Command '['docker', 'build', '-t', 'jupyterhub/k8s-hub:0.9-217f798', 'images/hub', '--build-arg', 'JUPYTERHUB_VERSION=git+https://github.com/jupyterhub/jupyterhub@master']' returned non-zero exit status 100.

# while installing a dependency for our k8s cluster
Unable to connect to the server: dial tcp: lookup docs.projectcalico.org on 127.0.0.53:53: read udp 127.0.0.1:56409->127.0.0.53:53: i/o timeout
```

Network and DNS issues are typically symptoms of unreliable internet (as
experienced by the VirtualMachine). You can recognize such issues if you get
errors like the ones above.

As you may notice, typical keywords associated with network errors are:

- *resolve host*
- *name resolution*
- *timeout*
- *no route to host*

#### Unable to listen on port

Did you get an error like this?

```
Unable to listen on port 8080: Listeners failed to create with the following errors: [Unable to create listener: Error listen tcp4 127.0.0.1:8080: bind: address already in use Unable to create listener: Error listen tcp6 [::1]:8080: bind: address already in use]
```

The key to solving this is understanding it!

We need to shuttle traffic from your computer to your Kubernetes clusters's
Service that in turn shuttle the traffic to the pod of relevance. While doing
so, we can end up with issues like the one above if we end up asking for traffic
to go to more than one place.

Let's look on how we need traffic to be shuttled!

1. *Traffic entering your computer should go to your VM.*

   When you run `vagrant up` your computer will read the
   [Vagrantfile](Vagrantfile) and from that conclude it should shuttle traffic
   incoming to your computer on port `8080` to your VM on port `8080`.

2. *Traffic entering your VM should go to your Kubernetes cluster's Service named `proxy-public`.*

   When you run `./dev upgrade`, that in turn runs the `kubectl port-forward`
   command to shuttle traffic from port `8080` to the `proxy-public` Kubernetes
   Service (port `80`) that we want to communicate with, it is the gate to speak
   with the hub and proxy even though it is also possible to speak directly to
   the hub.

In short, the traffic is routed from computer (8080), to the VM (8080), to the
Kubernetes `proxy-public` Service (80).

The reason you may run into an issue if is there is another service already
listening on traffic arriving on a given port. Then you would need to either
shut it down or route traffic differently.

## Helm chart practices

We strive to follow the guidelines provided by
[kubernetes/charts](https://github.com/kubernetes/charts/blob/master/REVIEW_GUIDELINES.md)
and the [Helm chart best practices
guide](https://github.com/kubernetes/helm/tree/master/docs/chart_best_practices).
