(community-resources)=

# Community Resources

This section gives the community a space to provide information on setting
up, managing, and maintaining JupyterHub.

```{important}
We recognize that Kubernetes has many deployment options. As a project team
with limited resources to provide end user support, we rely on community
members to share their collective Kubernetes knowledge and JupyterHub
experiences.
```

```{note}
**Contributing to Z2JH**. If you would like to help improve the Zero to
JupyterHub guide, please see the [issues page](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues) as well as the [contributor guide](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/HEAD/CONTRIBUTING.md).
```

We hope that you will use this section to share deployments with on a variety
of infrastructure and for different use cases.
There is also a [community maintained list](users-list) of users of this
Guide and the JupyterHub Helm Chart.

Please submit an [issue/pull request](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues) to add to this section. Thanks.

## Tips and Snippets

This is a page to collect a few particularly useful patterns and snippets
that help you interact with your Kubernetes cluster and JupyterHub.
If there's something that you think is generic enough (and not obvious enough)
to be added to this page, please feel free to make a PR!

## `kubectl` autocompletion

Kubernetes has a helper script that allows you to auto-complete commands
and references to objects when using `kubectl`. This lets you
{kbd}`TAB`-complete and saves a lot of time.

Follow [the kubectl installation instructions for your platform](https://kubernetes.io/docs/tasks/tools/#kubectl)
to find the shell autocompletion instructions.

## `helm` autocompletion

Helm also has an auto-completion script that lets you {kbd}`TAB`-complete
your commands when using Helm.

[Here are the instructions to install helm auto-completion](https://helm.sh/docs/helm/helm_completion/).

## Managing `kubectl` contexts

Oftentimes people manage multiple Kubernetes deployments at the same time.
`kubectl` handles this with the idea of "contexts", which specify which
Kubernetes deployment you are referring to when you type `kubectl get XXX`.

To see a list of contexts currently available to you, use the following
command:

```bash
kubectl config get-contexts
```

This will list all of your Kubernetes contexts. You can select a particular
context by entering:

```bash
kubectl config use-context <CONTEXT-NAME>
```

## Specifying a default namespace for a context

If you grow tired of typing `namespace=XXX` each time you type a kubernetes
command, here's a snippet that will allow you set a default namespace for
a given Kubernetes context:

```bash
kubectl config set-context $(kubectl config current-context) \
    --namespace=<YOUR-NAMESPACE>
```

The above command will only apply to the currently active context, and will
allow you to skip the `--namespace=` part of your commands for this context.

## Using labels and selectors with `kubectl`

Sometimes it's useful to select an entire class of Kubernetes objects rather
than referring to them by their name. You can attach an arbitrary set of
labels to a Kubernetes object, and can then refer to those labels when
searching with `kubectl`.

To search based on a label value, use the `-l` or `--selector=` keyword
arguments. For example, JupyterHub creates a specific subset of labels for all
user pods. You can search for all user pods with the following label query:

```bash
kubectl --namespace=<YOUR-NAMESPACE> get pod \
    -l "app.kubernetes.io/component=singleuser-server"
```

For more information, see the [Kubernetes labels and selectors page](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/).

## Asking for a more verbose or structured output

Sometimes the information that's in the default output for `kubectl get <XXX>`
is not enough for your needs, or isn't structured the way you'd like. We
recommend looking into the different Kubernetes output options, which can be
modified like so:

```bash
kubectl --namespace=<NAMESPACE> get pod -o <json|yaml|wide|name...>
```

You can find more information on what kinds of output you can generate at
[the kubectl information page](https://kubernetes.io/docs/reference/kubectl/).
(click and search for the text "Output Options")

This is a community maintained list of organizations / people using the Zero to
JupyterHub guide and Helm chart to maintain their JupyterHub. Send us a Pull
Request to add yourself to this alphabetically sorted list!

- Data Science Education Program's [DataHub](https://github.com/berkeley-dsep-infra/datahub) at University of California, Berkeley
- [MyBinder.org](https://mybinder.org)
- [PAWS](https://www.mediawiki.org/wiki/PAWS) at [Wikimedia Cloud Services](https://www.mediawiki.org/wiki/Wikimedia_Cloud_Services_team)
- A group of universities near Paris (led by a team at CNRS and Polytechnique) deployed [a cross-institutional JupyterHub](https://blog.jupyter.org/how-to-deploy-jupyterhub-with-kubernetes-on-openstack-f8f6120d4b1) for university use.
- [Globus](https://www.globus.org/) runs an [instance of Zero-to-JupyterHub](https://jupyter.demo.globus.org/) to help users learn about Globus REST APIs.

(users-list)=

## Links to community project resources

This page contains links and references to other material in the JupyterHub
ecosystem. It may include other guides, examples of JupyterHub deployments,
or posts from the community.

If you have a suggestion for something to add to this page, please
[open an issue](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues).

- **Automatically deploy a JupyterHub on AWS** from the Space Telescope Software Institute
  - [github repository](https://github.com/spacetelescope/z2jh-aws-ansible)
  - [blog post](https://github.com/spacetelescope/z2jh-aws-ansible)
- **Setup Kubernetes with Terraform**
  - [terraform-deploy repository](https://github.com/pangeo-data/terraform-deploy)
    This repo houses several example Kubernetes cluster deployments on AWS.
  - [Terraform tutorial example](https://github.com/pangeo-data/terraform-deploy/tree/HEAD/aws-examples/minimal-deployment-tutorial)
    This is meant to introduce newcomers to Terraform and show them how to deploy an AWS EKS cluster with it.
  - [Terraform blog post](https://github.com/pangeo-data/terraform-deploy/tree/HEAD/aws-examples/blog-post)
    This example is a more in-depth look at deploying an opinionated kubernetes cluster with
    Terraform. It has a partnered blog post as well, available
    [on Medium](https://medium.com/pangeo/terraform-jupyterhub-aws-34f2b725f4fd).
