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

1. Start and automatically setup a VM.

   Use the `vagrant up` command to start the VM for the first time, or `vagrant
   resume` to resume a suspended VM.

   ```shell
   vagrant up
   # vagrant resume
   ```

1. Enter the VM and the `~/zero-to-jupyterhub-k8s` folder.

   The `~/zero-to-jupyterhub-k8s` folder in the VM will be the exact same folder
   on your actual machine. Change either and you influence both.

   ```shell
   vagrant ssh
   cd zero-to-jupyterhub-k8s
   ```

1. Do your development.

1. Exit and suspend the VM.

   If you don't worry about using some disk space, suspending the VM with
   `vagrant suspend` is a good option as compared to `halt` or `destroy`
   commands. Suspending the VM will allow you to quickly get back to development
   within the VM later. For more details see a [description about the
   differences](https://www.vagrantup.com/intro/getting-started/teardown.html).

   ```shell
   # exit the VM
   exit

   # suspend the VM
   vagrant suspend
   ```

#### b) Install tools yourself

This is what you need to install and make available on your PATH.

- [docker](https://docs.docker.com/install/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [helm](https://helm.sh/docs/using_helm/#installing-helm)
- [kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
- [kubeval](https://kubeval.instrumenta.dev/installation/)
- Python 3.7+ ([Anaconda.com](https://www.anaconda.com/distribution/), [Python.org](https://www.python.org/downloads/))
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

This repository contains various `Dockerfile`s that are used to build docker
images in use by the Helm chart. To help us build these docker images only when
needed as well as update the Helm chart's [`values.yaml`](jupyterhub/values.yaml)
to use the latest available image, we rely on a command line tool called
[`chartpress`](https://github.com/jupyterhub/chartpress) that is installed as
part of [dev-requirements.txt](dev-requirements.txt).

Chartpress is configured through [chartpress.yaml](chartpress.yaml), and will
only rebuild images if their dependent files in their respective directories or
chartpress.yaml itself has changed.

Now you will be presented with two options as usual, either you a) use the
automated script to install or upgrade the Helm chart, or b) you do it on your
own.

#### a) Automated Helm chart install or upgrade

1. Install or upgrade your local Helm chart.
   
   ```shell
   ./dev upgrade
   ```

#### b) Manual Helm chart install or upgrade

1. Use [`chartpress`](https://github.com/jupyterhub/chartpress) to rebuild
   modified images if needed but also update the chart's
   [values.yaml](jupyterhub/values.yaml) file with the appropriate image tags.

   ```shell
   chartpress
   ```

   > **NOTE:** If you use a kind cluster and have built new images that will
   > only available locally, you must also load them into the kind cluster using
   > the `kind load docker-image <image:tag>` command.

1. Use `helm` to install or upgrade your Helm chart.

   ```shell
   helm upgrade jh-dev ./jupyterhub --install --namespace jh-dev
   ```



### 4: Setup network access

In order for you to access jupyterhub and a spawned user server, you need to be
able to access the Kubernetes service in this Helm chart called proxy-public.
While pods in the cluster can do this easily, your computer isn't a pod in the
cluster. What we can do is to dedicate a port on your computer to go towards the
proxy-public service of the Kubernetes cluster using `kubectl port-forward`.

When you run `kubectl port-forward` you will get a process that keeps running
and you need to open an new terminal window alongside it, unless you detach this
process. The `./dev port-forward` script will detach the process, and respect
the environment two variables, `Z2JH_PORT_FORWARD_ADDRESS` and
`Z2JH_PORT_FORWARD_PORT`, that you can set with the `.env` file.

#### a) Using dev script

```shell
./dev port-forward
```

#### b) Using kubectl directly

```shell
kubectl port-forward --namespace jh-dev service/proxy-public 8080:80
```



### 5: Run tests

To run the available tests, you can a) use the dev script or b) do it yourself
with `pytest`. Using the dev script, you will be presented with useful debugging
information if a test fails, and you will be required to explicitly declare what
Kubernetes cluster to use in the `.env` file. This can help you avoid a mistake
of working with the wrong Kubernetes cluster.

> **NOTE:** If you haven't port-forwarded the `proxy-public` Kubernetes service
> on `localhost` to port `8080` as is the default, you will need to set the
> environment variables `Z2JH_PORT_FORWARD_ADDRESS` and `Z2JH_PORT_FORWARD_PORT`
> respectively. If you run `./dev test`, you need to set them in the `.env`
> file.

#### a) Run tests with the dev script

```shell
./dev test
```

#### b) Run test with pytest directly

```shell
pytest -v --exitfirst ./tests
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

#### kind load docker-image issues

This is an error experienced using docker version 18.06.1-ce, and it has not
reoccurred since upgrading to 19.03.1-ce.

```
$ python3 ci/kind-load-docker-images.py --kind-cluster jh-dev
Error: exit status 1
`kind load docker-image --name jh-dev jupyterhub/k8s-hub:0.8.0_241-4be955c8` exited with status 1
`python3 ci/kind-load-docker-images.py --kind-cluster jh-dev` errored (1)

$ kind load docker-image --name jh-dev jupyterhub/k8s-hub:0.8.0_241-4be955c8
Error: exit status 1

$ kind load docker-image --name jh-dev jupyterhub/k8s-hub:0.8.0_241-4be955c8 --loglevel DEBUG
DEBU[00:46:57] Running: /snap/bin/docker [docker image inspect -f {{ .Id }} jupyterhub/k8s-hub:0.8.0_241-4be955c8]
DEBU[00:46:57] Running: /snap/bin/docker [docker ps -q -a --no-trunc --filter label=io.k8s.sigs.kind.cluster --format {{.Names}}\t{{.Label "io.k8s.sigs.kind.cluster"}}] 
DEBU[00:46:57] Running: /snap/bin/docker [docker ps -q -a --no-trunc --filter label=io.k8s.sigs.kind.cluster --format {{.Names}}\t{{.Label "io.k8s.sigs.kind.cluster"}} --filter label=io.k8s.sigs.kind.cluster=jh-dev] 
DEBU[00:46:57] Running: /snap/bin/docker [docker inspect -f {{index .Config.Labels "io.k8s.sigs.kind.role"}} jh-dev-control-plane]
DEBU[00:46:57] Running: /snap/bin/docker [docker exec --privileged jh-dev-control-plane crictl inspecti jupyterhub/k8s-hub:0.8.0_241-4be955c8]
DEBU[00:46:57] Image: "jupyterhub/k8s-hub:0.8.0_241-4be955c8" with ID "sha256:49a728c14a0f1d8cba40071f7bf2c173d03acd8c04fce828fea6b9dcb9805145" not present on node "jh-dev-control-plane" 
DEBU[00:46:57] Running: /snap/bin/docker [docker save -o /tmp/image-tar149196292/image.tar jupyterhub/k8s-hub:0.8.0_241-4be955c8] 
Error: exit status 1

$ docker save -o /tmp/image-tar149196292/image.tar jupyterhub/k8s-hub:0.8.0_241-4be955c8
failed to save image: unable to validate output path: directory "/tmp/image-tar149196292" does not exist
```

#### Unable to listen on port

Did you get an error like this?

```
Unable to listen on port 8080: Listeners failed to create with the following errors: [Unable to create listener: Error listen tcp4 127.0.0.1:8080: bind: address already in use Unable to create listener: Error listen tcp6 [::1]:8080: bind: address already in use]
```

The key to solving this is understanding it!

We need to shuttle traffic from your computer to your Kubernetes clusters's
Service that in turn shuttle the traffic to the pod of relevance. While doing
so, we can end up with issues like the ones above. They arise because we have
asked for traffic to go to more than one place.

Let's look on how we need traffic to be shuttled!

*Traffic entering your computer should go to your Kubernetes cluster's
Service named `proxy-public`.*

When you run `./dev upgrade`, that in turn runs the `kubectl port-forward`
command to shuttle traffic from port `8080` to the `proxy-public` Kubernetes
Service (port `80`) that we want to communicate with, it is the gate to speak
with the hub and proxy even though it is also possible to speak directly to
the hub.

Consider this example issue. Assume you setup a `kind` Kubernetes cluster on
your local computer, and also let incoming traffic on `8080` go straight ot this
cluster using the `kubectl port-forward` command. What would happen if you start
up a VM with `vagrant up` and, Vagrant was configured in the Vagrantfile to want
traffic coming to your computer on `8080` to go towards it? Then you would have
asked for traffic to go both to the Kubernetes cluster and to your VM. You would
experience an error like the one below.

```
Vagrant cannot forward the specified ports on this VM, since they
would collide with some other application that is already listening
on these ports. The forwarded port to 8080 is already in use
on the host machine.
```

To conclude: you may run into an issue like this if is there is another service
already listening on traffic arriving on a given port you want to use. Then you
would need to either shut the blocking service down or route traffic
differently.



## Helm chart practices

We strive to follow the guidelines provided by
[kubernetes/charts](https://github.com/kubernetes/charts/blob/master/REVIEW_GUIDELINES.md)
and the [Helm chart best practices
guide](https://github.com/kubernetes/helm/tree/master/docs/chart_best_practices).
