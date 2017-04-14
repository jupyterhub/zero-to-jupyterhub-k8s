Using an existing image
=======================

In your ``config.yaml`` add:

    .. code-block:: yaml
       singleuser:
           image:
              name: berkeleydsep/singleuser-data8
              tag: v0.1


Then you can upgrade your cluster with:

     .. code:: bash
        helm upgrade YOUR_RELEASE_NAME https://github.com/jupyterhub/helm-chart/releases/download/v0.1/jupyterhub-0.1.tgz -f config.yaml

``YOUR_RELEASE_NAME`` is what you provided to ``--name`` when you did the initial `helm install`. If you forgot what name you used, you might be able to find out from ``helm list``
