JupyterHub on Kubernetes for Data 8
=======

[![Build Status](https://travis-ci.org/data-8/jupyterhub-k8s.svg?branch=master)](https://travis-ci.org/data-8/jupyterhub-k8s)

This repo contains the Kubernetes config, container images, and docs for Data
8's deployment of JupyterHub on Kubernetes. This is a major work in progress
and is not ready for the real world yet.

Getting Started
-------

Clone this repo:

    git clone https://github.com/data-8/jupyterhub-k8s

Set up a Kubernetes cluster using Google Container Engine. Other cloud
providers are not currently supported but will be before release.

Configure [`kubectl`][kubectl] to point to your cluster. This is automatically
done when using `minikube` or the `gcloud` CLI. Verify that

    kubectl cluster-info

Returns output that looks like:

    Kubernetes master is running at https://146.148.80.79

Then, from the project root, run

    kubectl apply -f manifest.yaml

That deploys JupyterHub!

[kubectl]: http://kubernetes.io/docs/user-guide/prereqs/

File / Folder structure
-------

The `manifest.yaml` file in the project root directory contains the entirety of
the Kubenetes configuration for this deployment.

The subdirectories contain the Dockerfiles and scripts for the images used for
this deployment.

All the images for this deployment are pushed to the [data8 Docker Hub][]
organization and are named `data8/jupyterhub-k8s-<name>` where `<name>` is the
name of the containing folder for that image.

[data8 Docker Hub]: http://hub.docker.com/r/data8/

Development
-------

Current work on this project lives in a [ZenHub][] board for this repo. You
must install the browser extension to see the board.

After installing the extension, navigate to [the issue board](#boards) or press
`b`. You'll see a screen that looks something like this:

![screenshot 2016-11-04 13 24 21](https://cloud.githubusercontent.com/assets/2468904/20021193/084bb660-a292-11e6-9720-10746f475746.png)

- **Icebox** contains future tasks that haven't been prioritized.
- **This week** contains tasks that we plan to finish this week.
- **In Progress** contains tasks that someone is currently working on. All of
  these tasks have at least one person assigned to them.
- When the task is complete, we close the related issue.

**Epics** are groups of tasks that correspond to a complete feature. To see
only issues that belong to a specific Epic, you can click / unclick the
"Filter by this epic" button on the Epic.

[ZenHub]: https://www.zenhub.com/

### Workflow

1. As tasks / issues first get created, they land in the **Icebox** pipeline
   and are categorized into an **Epic** if needed.
2. During our weekly planning meetings we'll move tasks from **Icebox** to
   **This Week**.
3. When team members start actively working on a task, they'll assign
   themselves to the task and move it into the **In Progress** pipeline.
4. When team members finish a task, they'll make a Pull Request for the task.
   When the PR gets merged, they'll close the task to take it off the board.
