Tools used in a JupyterHub Deployment
=====================================

JupyterHub is meant to connect with many tools in the world of
cloud computing and container technology. This page describes these
tools in greater detail in order to provide some more contextual
information.

Cloud Computing Providers
-------------------------

These are the organizations that host the computers on which your
JupyterHub will run. When people access your JupyterHub remotely, they are
creating instances on machines that are managed by these organizations.

They provide the following things:

- Computing
- Disk space
- Networking (both internal and external)
- Creating, resizing, and deleting clusters

Some of these organizations are companies
(e.g., `Google <http://cloud.google.com/>`_), though JupyterHub
will work fine with university clusters or custom cluster deployments as well.
For these materials, any cluster with Kubernetes installed will work
with JupyterHub.

More information about setting up accounts services with cloud providers
can be found `here <create-k8s-cluster.html>`_.

Container Technology
--------------------

Container technology is essentially the idea of bundling all of the
necessary components to run a piece of software. There are many ways
to do this, but one that we'll focus on is called Docker. Here are
the main components of Docker:

Container Image
***************

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

Containers
**********

You can "run" a container image, and it creates a container for you.
A container is a particular instantiation of a container image. This means
that it actually exists on a computer. It is a self-contained
computational environment that is constructed according to the layers
that are inside of the Container Image. However, because it is now
running on the computer, it can do other useful things like talk to other
Docker containers or communicate via the internet. 


Kubernetes
----------

`Kubernetes <https://kubernetes.io/>`_ is a service that runs on cloud infrastructures. It provides a single point of contact with the machinery
of your cluster deployment, and allows a user to specify the computational requirements that they need (e.g., how many machines, how many CPUs
per machine, how much RAM).
Then, it handles the resources on the cluster and ensures that
these resources are always available. If something goes down, kubernetes
will try to automatically bring it back up.
 
Kubernetes can only manage the computing resources that it is
given. This means that it generally can **not** create new resources on its
own (with the exception of disk space).

There are three main types of objects in Kubernetes:

Processes
*********
Are any program that is running on a machine. For example,
a Jupyter Notebook creates several processes that handle the
execution of code and the display in the browser.

Pods
****

Pods are essentially a collection of one or more *containers* that
run together. You can think of them as a way of combining containers
that, as a group, accomplish some goal.

For example, say you want to create a web server that is open to the
world, but you also want authentication so that only a select group
of users can access it. You could use a single pod with two containers.

* One that does the authentication. It would have something like Apache
  specified in its container image, and would be connected to the
  outside world.
* One that receives information from the authentication container, and
  does something fancy with it (maybe it runs a python process).

This is useful because it lets you compatmentalize the components of the
service that you want to run, which makes things easier to manage and
keeps things more stabl.

Deployments
***********

A deployment is a collection of pods on kubernetes. It is how kubernetes
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

**Note**: Users don't generally "create" deployments directly, they are
instead generated from a set of instructions that are sent to Kubernetes.
We'll cover this in the section on "Helm".

Service
*******

A service is simply a stable way of referring to a deployment. Kubernetes
is all about intelligently handling dynamic and quickly-changing
computational environments. This means that the hardware may change,
IP addresses will be different, etc. However you don't want to have to
re-orient yourself every time this happens. A Kubernetes service keeps
track of all these changes on the backend, and provides a single address
to manage your deployment.

Namespace
*********

Finally, a `namespace <https://kubernetes.io/docs/admin/namespaces/>`_
defines a collection of deployments. This will define
the boundaries of hardware that the deployments have to exist within. It
is generally the most "high-level" of the groups we've discussed thus far.
For example, a a namespace could be a single class running with JupyterHub.
It defines all the hardware that is available to students. It also defines
the JupyterHub machinery that glues together all of the student containers,
manages disk space, etc.

Persistent Volume Chain
***********************

Persistent Volume Chains are a way to have persistent storage without
being tied down to one specific computer or machine. Kubernetes is
about that flexibility, and that means that we don't want to lock ourselves
in to a particular operating system just because our files are already
on it. Persistent Volume Chains help deal with this problem by knowing
how to convert files between filesystem types. 


Helm
----

`Helm <https://helm.sh/>`_ is a way of specifying kubernetes objects
with a standard template.

Charts
******

The way that Helm controls kubernetes is with templates of structured
information that specify some computational requirements.
These templates are called "charts", or "helm charts". They contain
all of the necessary information for kubernetes to generate either:

- a deployment object 
- a service object
- a persistent volume object a deployment.

They can be installed into a namespace, which causes kubernetes to
begin deploying the objects above into that namespace.

Charts have both names and versions, which means that you can easily
update them and build off of them. There are
`community maintained charts <https://github.com/kubernetes/charts/tree/master/stable>`_
available, and we use a chart to install and upgrade JupyterHub in
this guide. In our case, the helm chart is a file called ``config.yaml``.


Releases
********

A release is basically a specific instantiation of a helmchart inserted
into a particular namespace. If you'd like to upgrade your
kubernetes deployment (say, by changing the amount of RAM that each
user should get), then you can change the helm chart, then re-deploy
it to your kubernetes cluster. This generates a new release.


JupyterHub
----------

JupyterHub is a way of utilizing the components above in order to
provide computational environments that users can access remotely.
It exists as a kubernetes deployment, which is comprised of multiple
pods. Each pod accomplishes some task that, together, make up JupyterHub.
Finally, the output of JupyterHub is a user pod, which specifies the
computational environment in which a single user will operate. So
essentially a JupyterHub is a collection of:

* Pods that contain the JupyterHub Machiner
* A bunch of user pods that are constantly being created or destroyed.

Below we'll describe the primary JupyterHub pods.

Proxy Pod
*********

This is the user-facing pod. It provides the IP address that people will
go to in order to access JupyterHub. When a new users goes to this pod,
it will decide whether to:

* send that user to the Hub pod, which will create a container for that
  user, or
* if that user's container already exists, send them directly to that
  container instead.

Information about the user's identity is stored as a cookie on their
computer. This is how the proxy pod knows whether a user already has
a running container.

Hub Pod
*******

Receives traffic from the proxy pod. It has 3 main running processes:

1. An authenticator, which can verify a user's account.It also contains a process
2. A "KubeSpawner" that talks to the kubernetes API and tells it to spawn
   pods for users if one doesn't already exist. KubeSpawner will tell
   kubernetes to create a pod for a new user, then it will tell the
   the Proxy Pod that the user’s pod has been created.
3. An admin panel that has information about who has pods created, and
   what kind of usage exists on the cluster.
