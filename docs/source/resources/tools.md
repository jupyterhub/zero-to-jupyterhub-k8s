(tools)=

# Utilized Tools

JupyterHub is meant to connect with many tools in the world of
cloud computing and container technology. This page describes these
tools in greater detail in order to provide some more contextual
information.

## Cloud Computing Providers

This is whatever will run the actual computation. Generally it means a
company, university server, or some other organization that hosts computational
resources that can be accessed remotely. JupyterHub will run on these
computational resources, meaning that users will also be operating on these
resources if they're interacting with your JupyterHub.

They provide the following things:

- Computing
- Disk space
- Networking (both internal and external)
- Creating, resizing, and deleting clusters

Some of these organizations are companies
(e.g., [Google](https://cloud.google.com/)), though JupyterHub
will work fine with university clusters or custom cluster deployments as well.
For these materials, any cluster with Kubernetes installed will work
with JupyterHub.

More information about setting up accounts services with cloud providers
can be found [here](create-k8s-cluster).

## Container Technology

Container technology is essentially the idea of bundling all of the
necessary components to run a piece of software. There are many ways
to do this, but one that we'll focus on is called Docker. Here are
the main concepts of Docker:

### Container Image

Container images contain the dependencies required to run your code.
This includes **everything**, all the way down to the operating
system itself. It also includes things like the filesystem on which
your code runs, which might include data etc. Containers are also
portable, meaning that you can exactly recreate the computational
environment to run your code on almost any machine.

In Docker, images are described as layers, as in layers of dependencies.
For example, say you want to build a container that runs scikit-learn.
This has a dependency on Python, so you have two layers: one for
python, and another that inherits the python layer and adds the extra
piece of scikit-learn. Moreover, that base python layer needs an
operating system to run on, so now you have three layers:
ubuntu -> python -> scikit-learn. You get the idea. The beauty of this
is that it means you can share base layers between images. This
means that if you have many different images that all require
ubuntu, you don't need to have many copies of ubuntu lying around.

Images can be created from many things. If you're using Docker, the basic
way to do this is with a **Dockerfile**.
This is essentially a list of instructions that tells
Docker how to create an image. It might tell Docker which base layers
you want to include in an image, as well as some extra dependencies that
you need in the image. Think of it like a recipe that tells Docker how
to create an image.

### Containers

You can "run" a container image, and it creates a container for you.
A container is a particular instantiation of a container image. This means
that it actually exists on a computer. It is a self-contained
computational environment that is constructed according to the layers
that are inside of the Container Image. However, because it is now
running on the computer, it can do other useful things like talk to other
Docker containers or communicate via the internet.

## Kubernetes

[Kubernetes](https://kubernetes.io/) is a service that runs on cloud
infrastructures. It provides a single point of contact with the machinery
of your cluster deployment, and allows a user to specify the computational
requirements that they need (e.g., how many machines, how many CPUs
per machine, how much RAM). Then, it handles the resources on the cluster and
ensures that these resources are always available. If something goes down,
Kubernetes will try to automatically bring it back up.

Kubernetes can only manage the computing resources that it is
given. This means that it generally can **not** create new resources on its
own (with the exception of disk space).

The following sections describe some objects in Kubernetes that are
most relevant for JupyterHub.

### Processes

Are any program that is running on a machine. For example,
a Jupyter Notebook creates several processes that handle the
execution of code and the display in the browser. This isn't
technically a Kubernetes object, since literally any computer has
processes that run on it, but Kubernetes does keep track of running
processes in order to ensure that they remain running if needed.

### Pods

Pods are essentially a collection of one or more _containers_ that
run together. You can think of them as a way of combining containers
that, as a group, accomplish some goal.

For example, say you want to create a web server that is open to the
world, but you also want authentication so that only a select group
of users can access it. You could use a single pod with two containers.

- One that does the authentication. It would have something like Apache
  specified in its container image, and would be connected to the
  outside world.
- One that receives information from the authentication container, and
  does something fancy with it (maybe it runs a python process).

This is useful because it lets you compartmentalize the components of the
service that you want to run, which makes things easier to manage and
keeps things more stable.

For more information about pods, see the
[Kubernetes documentation about pods](https://kubernetes.io/docs/concepts/workloads/pods/).

### Deployments

A deployment is a collection of pods on Kubernetes. It is how Kubernetes
knows exactly what containers and what machines need to be running at all
times. For example, if you have two pods: one that does the authenticating
described above, and another that manages a database, you can specify both
in a deployment.

Kubernetes will ensure that both pods are active, and if
one goes down then it will try to re-create it. It does this by continually
checking the current state of the pods, and then comparing this with the
original specification of the deployment. If there are differences between
the current state vs. the specification of the deployment, Kubernetes will
attempt to make changes until the current state matches the specification.

For more information about deployments, see the
[Kubernetes documentation about deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).

```{note}
Users don't generally "create" deployments directly, they are
instead generated from a set of instructions that are sent to Kubernetes.
We'll cover this in the section on "Helm".
```

### Service

A service is simply a stable way of referring to a deployment. Kubernetes
is all about intelligently handling dynamic and quickly-changing
computational environments. This means that the VMs running your pods may change,
IP addresses will be different, etc. However you don't want to have to
re-orient yourself every time this happens. A Kubernetes service keeps
track of all these changes on the backend, and provides a single address
to manage your deployment.

For more information about services, see the
[Kubernetes documentation about services](https://kubernetes.io/docs/concepts/services-networking/service/).

### Namespace

Finally, a [namespace](https://kubernetes.io/docs/tasks/administer-cluster/namespaces/)
defines a collection of objects in Kubernetes. It
is generally the most "high-level" of the groups we've discussed thus far.
For example, a namespace could be a single class running with JupyterHub.

For more information about namespaces, see the
[Kubernetes documentation on namespaces](https://kubernetes.io/docs/tasks/administer-cluster/namespaces/).

### Persistent Volume Claim

Persistent Volume Claims are a way to have persistent storage without
being tied down to one specific computer or machine. Kubernetes is
about that flexibility, and that means that we don't want to lock ourselves
into a particular operating system just because our files are already
on it. Persistent Volume Claims help deal with this problem by knowing
how to convert files between disk types (e.g., AWS vs. Google disks).

For more information on Persistent Volume Claims, see the
[Kubernetes documentation on persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/).

## Helm

[Helm](https://helm.sh/) is a way of specifying Kubernetes objects
with a standard template.

### Charts

The way that Helm controls Kubernetes is with templates of structured
information that specify some computational requirements.
These templates are called "charts", or "helm charts". They contain
all of the necessary information for Kubernetes to generate:

- a deployment object
- a service object
- a persistent volume object for a deployment.
- collections of the above components

They can be installed into a namespace, which causes Kubernetes to
begin deploying the objects above into that namespace.

Charts have both names and versions, which means that you can easily
update them and build off of them. There are
[community maintained charts](https://github.com/helm/charts/tree/HEAD/stable)
available, and we use a chart to install and upgrade JupyterHub in
this guide. In our case, the helm chart is a file called `config.yaml`.

### Releases

A release is basically a specific instantiation of a helmchart inserted
into a particular namespace. If you'd like to upgrade your
kubernetes deployment (say, by changing the amount of RAM that each
user should get), then you can change the helm chart, then re-deploy
it to your Kubernetes cluster. This generates a new version of the release.

## JupyterHub

JupyterHub is a way of utilizing the components above in order to
provide computational environments that users can access remotely.
It exists as two Kubernetes deployments, Proxy and Hub, each of which has
one pod. Each deployment accomplishes some task that, together, make up JupyterHub.
Finally, the output of JupyterHub is a user pod, which specifies the
computational environment in which a single user will operate. So
essentially a JupyterHub is a collection of:

- Pods that contain the JupyterHub Machinery
- A bunch of user pods that are constantly being created or destroyed.

Below we'll describe the primary JupyterHub pods.

### Proxy Pod

This is the user-facing pod. It provides the IP address that people will
go to in order to access JupyterHub. When a new users goes to this pod,
it will decide whether to:

- send that user to the Hub pod, which will create a container for that
  user, or
- if that user's container already exists, send them directly to that
  container instead.

Information about the user's identity is stored as a cookie on their
computer. This is how the proxy pod knows whether a user already has
a running container.

### Hub Pod

Receives traffic from the proxy pod. It has 3 main running processes:

1. An authenticator, which can verify a user's account. It also contains a
   process.
2. A "KubeSpawner" that talks to the Kubernetes API and tells it to spawn
   pods for users if one doesn't already exist. KubeSpawner will tell
   Kubernetes to create a pod for a new user, then it will tell the
   Proxy Pod that the user’s pod has been created.
3. An admin panel that has information about who has pods created, and
   what kind of usage exists on the cluster.
