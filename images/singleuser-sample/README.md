# The default user image

This Docker image is the Helm chart's default user image. It contains the
fundamentals only so that it can get pulled quickly. It is based on the
[base-notebook image](https://github.com/jupyter/docker-stacks/blob/master/base-notebook/Dockerfile)
from Project Jupyter's [jupyter/docker-stacks repository](https://github.com/jupyter/docker-stacks)
which also contains many other images suitable for use with the Helm chart. To
help you choose another one see [the docker-stacks documentation on selecting a
user image](http://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html).

For a brief introduction to *Dockerfiles*, *images* and *containers*, see [the
guide's summary about container technology.](https://z2jh.jupyter.org/en/latest/tools.html#container-technology).

## Basic usage

To quickly try out this Docker image on your computer:

```sh
# with the classic UI
docker run  -it  --rm  -p 8888:8888 jupyterhub/k8s-singleuser-sample:0.7.0

# with JupyterLab
docker run  -it  --rm  -p 8888:8888 -e JUPYTER_ENABLE_LAB=true jupyterhub/k8s-singleuser-sample:0.7.0
```

This image available tags can be found [here](https://hub.docker.com/r/jupyterhub/k8s-singleuser-sample/tags/).

## In the base-notebook image
- Ubuntu Linux - v18.04 aka. Bionic
- JupyterHub - required by with Helm chart since KubeSpawner requires it
- [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/) and [JupyterLab-Hub extension](https://jupyterlab.readthedocs.io/en/stable/user/jupyterhub.html) - to activate it over the classical UI by default, see [the guide's instructions](https://z2jh.jupyter.org/en/latest/user-environment.html#use-jupyterlab-by-default).
