JupyterHub on Kubernetes for Data 8
=======

[![Build Status](https://travis-ci.org/data-8/jupyterhub-k8s.svg?branch=master)](https://travis-ci.org/data-8/jupyterhub-k8s)

This repo contains the Kubernetes config, container images, and docs for Data
8's deployment of JupyterHub on Kubernetes.

Getting Started
-------

### Google Cloud Engine ###

Log into the gcloud console at [console.cloud.google.com](console.cloud.google.com/)

Create a cluster. Go to `Container Engine` > `Container clusters` > `+ Create Cluster`. Fill out the required information and make sure you know how many instances you will need and what the memory and cpu requirements will be.

Go back to your dashboard in the GCP console. Click `Activate Google Cloud Shell` in the upper right-hand corner. It is an icon that looks like a small terminal.

In the new terminal window, clone the jupyterhub-k8s repository.

```
git clone https://github.com/data-8/jupyterhub-k8s
```

Set the zone.
```
gcloud config set compute/zone <your zone>
```

Get credentials for your cluster
```
gcloud container clusters get-credentials <your cluster>
```

Edit the docker-settings.json file. Set the docker repo name corresponding to your cloud provider. Set the image types. You can leave this blank if you are only using the base image. Set the context prefix to whatever you want.

Here is an example:
```
{
    "buildSettings": {
        "dockerRepo": {
            "gcloud": "gcr.io/<your project>",
            "azure": "data8-on.azurecr.io/data-8"
        },
        "imageTypes": ",datahub"
    },
    "populateSettings": {
        "contextPrefix": "gke_<your project>_<your zone>_"
    }
}
```

Run the build script to generate Docker images. `hub` is for the jupyterhub image and `proxy` is for the jupyterhub proxy image. The build script generates more than one singleuser image; `base` is intented to be inherited by all user images and `user {user_type}` is used to specify the variants of `base`.
```
./build.bash [ hub | proxy | base | user {user user_type} ]
```

Then enter the populate.bash commands printed by build.bash. Note the tag of the image that gets populated.

Edit the `helm-chart/values.yaml` file where it says `# Must be overridden`. Set the image tags to the tags of the docker images you just built using `./build.bash`. Also make sure to set the correct docker images. You may also adjust some of the other settings in the `values.yaml` file if necessary.

Install [helm](https://github.com/kubernetes/helm/blob/master/docs/install.md).

Run helm.
```
helm init

helm --kube-context=<your context prefix><your cluster> install ./helm-chart
```

Later, when you want to change your deployment run:
```
helm list

helm --kube-context=<your context prefix><your cluster> upgrade <release name> ./helm-chart
```

Congragulations! You just deployed your own jupyterhub cluster using kubernetes! :D



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

## Cal Blueprint

<a href="http://www.calblueprint.org/">
![bp](https://cloud.githubusercontent.com/assets/2468904/11998649/8a12f970-aa5d-11e5-8dab-7eef0766c793.png "BP Banner")
</a>

This project was worked on in close collaboration with
**[Cal Blueprint](http://www.calblueprint.org/)**.
Cal Blueprint is a student-run UC Berkeley organization devoted to matching
the skills of its members to our desire to see
social good enacted in our community. Each semester, teams of 4-5 students work
closely with a non-profit to bring technological solutions to the problems they
face every day.
