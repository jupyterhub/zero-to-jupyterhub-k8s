Using an existing image
=======================

It's possible to build your jupyterhub deployment off of a pre-existing Docker image. To do this, you need
to register the image on DockerHub, then grab the organization, user name, and tag for the image.

To instruct JupyterHub to use this image, simply add this to your ``config.yaml`` file:

    .. code-block:: yaml
       singleuser:
           image:
              name: berkeleydsep/singleuser-data8
              tag: v0.1

If you have alreday initialized jupyterhub with the helmchart, you'll need to "upgrade" your helmchart.
This will instruct the cluster to re-implement the instructions in ``config.yaml`` (which in this case
now points to the Docker Hub image).

To upgrade the cluster, run:

     .. code:: bash
        helm upgrade <YOUR_RELEASE_NAME> https://github.com/jupyterhub/helm-chart/releases/download/v0.1/jupyterhub-0.1.tgz -f config.yaml

     .. note::
         ``<YOUR_RELEASE_NAME>`` is what you provided to ``--name`` when you did the initial `helm install`.
         If you forgot what name you used, you might be able to find out by running ``helm list``.
