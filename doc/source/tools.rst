Tools for setting up JupyterHub
===============================

`Google Cloud <http://cloud.google.com/>`_

- Google Cloud will provide the computing power that we’ll use. This is a service provided by Google that essentially allows us to use some of their computers. Fortunately, their computers are fancy, with lots of tools for scaling our usage up or down depending on our needs. There are lots of other cloud services out there (such as Microsoft Azure and Amazon EC2) but we’ll focus on Google’s for now.
  - You can access Google Cloud from its web console or via the “gcloud” SDK that you can download to your computer.

`Kubernetes <https://kubernetes.io/>`_

- Kubernetes is a service that runs on cloud infrastructures, and actually does the communicating between computers on the cloud. Basically, a big challenge of cloud computing is that you want to interact with potentially lots of different computers. However, you want a single point-of-contact for controlling them. This is what kubernetes offers, and it’s what JupyterHub will utilize in order to increase the number of computers available if we need it.
  - We will interact with kubernetes via the Google Cloud terminal or the SDK.

**Git and GitHub**

- Git and GitHub are used for managing repositories of code, as well as keeping track of how these repositories change over time. In particular we’ll use a `github repository <https://github.com/data-8/jupyterhub-k8s>`_ that the JupyterHub team has put together which contains a lot of useful configuration files to connect with google cloud and kubernetes. In addition, you’ll probably want to have some code show up on JupyterHub instances once users login, and a good way to do this is by hosting your code on github.
  - We can push / pull repositories from github using our terminal, and then instruct JupyterHub to automatically pull them into a new instance

`Docker <https://docs.docker.com/engine/getstarted/>`_

- Docker is a technology for “containerized” computing environments. This basically means creating a very specific combination of hardware + software that can be easily moved to any computer. It’s useful for standardizing the environment in which development happens. We use this to generate live computing environments that users of a JupyterHub will experience. They’ll all have the same basic set of files + packages.

`Helm <https://github.com/kubernetes/helm/blob/master/docs/charts.md>`_

- Helm is technically a part of kubernetes, but is worth describing here. Basically this is the language that kubernetes uses as “instructions” for building a particular computing architecture in the cloud. We can think of them like recipes for deploying the particular setup that we want.
  - We’ll create a helm file for our setup so that kubernetes knows how to deploy.

**YAML**

- YAML is a generic language for structuring text, that is used in many places. 
