.. _local-dev:

Step Zero: Kubernetes on your local machine (dev/test)
------------------------------------------------------

It is possible to set up Kubernetes to run entirely on your laptop or desktop computer for testing or development purposes.

You need to choose a way to run Kubernetes. Here are some guides for the different operating systems explaining 
how you might choose from the options available and how to set them up:

* Windows: `choices are MiniKube or Docker Desktop <https://medium.com/containers-101/local-kubernetes-for-windows-minikube-vs-docker-desktop-25a1c6d3b766>`_
* MacOS: `choices are MiniKube or Docker Desktop <https://medium.com/containers-101/local-kubernetes-for-mac-minikube-vs-docker-desktop-f2789b3cad3a>`_
* Linux: `choices are MiniKube or MicroK8s <https://medium.com/containers-101/local-kubernetes-for-linux-minikube-vs-microk8s-1b2acad068d3>`_
 
You should then be able to proceed with the rest of Zero to JupyterHub, but be aware of some issues if using Kubernetes within Docker Desktop:

* You may need to increase the amount of memory available to Docker Engine. This can be done in the Advanced tab 
  of Preferences in the Docker control panel. An appropriate error message should appear if insufficient memory is available.
* The version of Kubernetes that comes with Docker Desktop may be a few versions old, and when you run the ``helm upgrade ...`` 
  command it may say something like ``Error: Chart requires kubernetesVersion: >=1.11.0-0 which is incompatible with Kubernetes v1.10.11``.
  The easiest thing may be to try earliers version numbers of the 
  `Helm Chart from this table <https://github.com/jupyterhub/helm-chart#versions-coupled-to-each-chart-release>`_ until things work, 
  although then be aware that the rest of the Zero to JupyterHub instructions might have been targeting the more recent versions.

Once you have your Kubernetes cluster running, it's time to begin :ref:`creating-your-jupyterhub`.
