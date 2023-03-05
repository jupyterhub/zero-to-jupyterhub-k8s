(glossary)=

# Glossary

A partial glossary of terms used in this guide. For more complete descriptions
of the components in JupyterHub, see {ref}`tools`. Here we try to keep the
definition as succinct and relevant as possible, and provide links to learn more
details.

<!--
    Additions to the glossary are welcomed. Please add in alphabetical order.
-->

```{glossary}
[admin user](https://jupyterhub.readthedocs.io/en/stable/getting-started/authenticators-users-basics.html?highlight=admin)
    A user who can access the JupyterHub admin panel. They can start/stop user
    pods, and potentially access their notebooks.

[authenticator](https://jupyterhub.readthedocs.io/en/stable/reference/authenticators.html)
    The way in which users are authenticated to log into JupyterHub. There
    are many authenticators available, like GitHub, Google, MediaWiki,
    Dummy (anyone can log in), etc.

`config.yaml`
    The {term}`Helm charts <Helm chart>` templates are rendered with these
    {term}`Helm values` as input. The file is written in the [YAML](https://en.wikipedia.org/wiki/YAML) format. The YAML format is essential
    to grasp if working with Kubernetes and Helm.

container
    A container is a isolated working space which for us gives users the
    tools, libraries, and capabilities to be productive.

culler
    A separate process in the JupyterHub that stops the user pods of users who
    have not been active in a configured interval.

Dockerfile
    A Dockerfile declares how to build a {term}`Docker image`.

Docker image
    A Docker image, built from a {term}`Dockerfile`, allows tools like
    `docker` to create any number of {term}`containers <container>`.

image registry
    A service for storing Docker images so that they can be stored
    and used later.
    The default public registry is at https://hub.docker.com,
    but you can also run your own private image registry.
    Many cloud providers offer private image registry services.

[environment variables](https://en.wikipedia.org/wiki/Environment_variable)
    A set of named values that can affect the way running processes will
    behave on a computer. Some common examples are `PATH`, `HOME`, and
    `EDITOR`.

[Helm chart](https://helm.sh/docs/topics/charts/)
    A Helm chart is a group of {term}`Helm templates <Helm template>` that
    can, given its default values and overrides in provided `yaml` files,
    render to a set of {term}`Kubernetes resources <Kubernetes resource>` that
    can be easily installed to your Kubernetes cluster. In other words a Helm
    chart is like a configurable installation of software and infrastructure
    to exist on a cloud.

[Helm template](https://helm.sh/docs/chart_template_guide/)
    A Helm template (`.yaml` files), can given values, render to a
    {term}`Kubernetes resource`.

[Helm values](https://helm.sh/docs/chart_template_guide/values_files/)
    {term}`Helm charts <Helm chart>` has a set of predefined values
    (`values.yaml`) typically overridden by other values in `config.yaml`. The
    final values are used to generate {term}`Kubernetes resources <Kubernetes
    resource>` from {term}`Helm templates <Helm template>` within a
    {term}`Helm chart`.

Kubernetes
    For our purposes, you can think of Kubernetes as a way to speak to a cloud
    and describe what you would like it to do, in a manner that isn't specific
    for that cloud.

    - [The Illustrated Children's Guide to Kubernetes](https://www.youtube.com/watch?v=4ht22ReBjno)
    - [The official "What is Kubernetes?" text](https://kubernetes.io/docs/concepts/overview/)

Kubernetes API server
    The [Kubernetes API](https://kubernetes.io/docs/concepts/overview/kubernetes-api/) server,
    also referred to as the master, will answer questions and update the
    desired state of the cluster for you. When you use `kubectl` you
    communicate with the API server.

Kubernetes Pod
    *Pods* are the smallest deployable units of computing that can be created
    and managed in Kubernetes. A pod will use a {term}`Docker image` to create
    a container, and most often a controller such as a Deployment will ensure
    there is always X running pods of a kind.

    See the [Kubernetes documentation](https://kubernetes.io/docs/concepts/workloads/pods/) for more
    information.

Kubernetes resource
    A Kubernetes resource can for example be a [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/),
    [Service](https://kubernetes.io/docs/concepts/services-networking/service/) or a
    [Secret](https://kubernetes.io/docs/concepts/configuration/secret/). It
    is something you can request by the {term}`Kubernetes API server` to be
    present in the cluster.

persistent storage
    A filesystem attached to a user pod that allows the user to store
    notebooks and files that persist across multiple logins.

Node Pool
    A *node pool* or *node group* represents a set of nodes of the same kind.
    With cluster autoscaling, a node pool can grow and shrink based on demand
    allowing you to save computational resources.

[repo2docker](https://github.com/jupyterhub/repo2docker)
    A tool which lets you quickly convert a Git repository into a
    {term}`Docker image`.

[spawner](https://jupyterhub.readthedocs.io/en/stable/getting-started/spawners-basics.html)
    A spawner is a separate process created for each active user by
    JupyterHub. They are each responsible for one user. This Helm chart relies
    on [KubeSpawner](https://jupyterhub-kubespawner.readthedocs.io/en/latest/).
```
