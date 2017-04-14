Extending your JupyterHub setup
===============================

This section describes how you can extend your JupyterHub setup beyond the
vanilla configuration. For example, you can expand the hardware requested,
such as memory and cpu limits. You can also use different base docker
images or authenticators to tailor your deployment to your needs.

Scaling your deployment for more users
--------------------------------------

Currently, we don't have a way to automatically scale the number of resources that
are being used according to the number of active users. This means that you should
request a number of nodes that can service all of your potential users at once.
This is done in the initial call to::

    gcloud container clusters create

A good rule of thumb is to put { TODO } users per node.

Extending the helm configuration
--------------------------------

Since the helmchart tells kubernetes what kind of resources to make available,
we can use the helmchart to determine what kind of computing environment users
will experience. We do this by editing the ``config.yaml`` file that the
helmchart uses to build. For a list of configuration options that are possible,
see the link below:

https://github.com/data-8/jupyterhub-k8s/blob/master/helm-chart/values.yaml

Using an existing image
=======================

It's possible to build your jupyterhub deployment off of a pre-existing Docker image.
To do this, you need to find an existing image somewhere (such as DockerHub), and configure
your installation to use it.

For example, UC Berkeley's `Data8 Program <https://hub.docker.com/r/berkeleydsep/singleuser-data8>`_ publishes the image they are using on Dockerhub.
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

Extending your software stack with s2i
--------------------------------------

s2i, also known as `Source to Image`_, lets you
quickly convert a GitHub repository into a Docker image that we can use as a
base for your JupyterHub instance. Anything inside the GitHub repository
will exist in a user’s environment when they join your JupyterHub. If you
include a ``requirements.txt`` file in the root level of your of the repository,
s2i will ``pip install`` each of these packages into the Docker image to be
built. Below we’ll cover how to use s2i to generate a Docker image and how to
configure JupyterHub to build off of this image.

.. note::
       For this section, you’ll need to install s2i and docker.


1. **Download s2i.** This is easily done with homebrew on a mac. For linux and
   Windows it entails a couple of quick commands that you can find in the
   links below:

       - On OSX: ``brew install s2i``
       - On Linux and Windows: `follow these instructions
         <https://github.com/openshift/source-to-image#installation>`_

2. **Download and start Docker.** You can do this by downloading and installing
   Docker at `this link <https://store.docker.com/search?offering=community&platform=desktop%2Cserver&q=&type=edition>`_.
   Once you’ve started Docker, it will show up as a tiny background application.

3. **Create (or find) a GitHub repository you want to use.** This repo should
   have all materials that you want your users to access. In addition you can
   include a ``requirements.txt`` file that has one package per line. These
   packages should be listed in the same way that you’d install them using
   ``pip install``. E.g.:

   .. code-block:: bash

          numpy
          scipy
          matplotlib=2.0

4. **Use s2i to build your Docker image.** `s2i` uses a template in order to
   know how to create the Docker image. We have provided one at the url in the
   commands below. Run this command::

       s2i build <git-repo-url>  yuvipanda/ubuntu1610-python35-venv:v0.1 gcr.io/<project-name>/<name-of-image>:<tag>

   this effectively says *s2i, build `<this repository>` to a Docker image by
   using `<this template>` and call the image `<this>`*

  .. note::
         - The project name should match your google cloud project's name.
         - Don’t use underscores in your image name. Other than this it can be
           anything memorable. This is a bug that will be fixed soon.
         - The tag should be the first 6 characters of the SHA in the GitHub
           commit for the image to build from.

5. **Push our newly-built Docker image to the cloud.** You can either push this
   to Docker Hub, or to the gcloud docker repository. Here we’ll push to the
   gcloud repository::

       gcloud docker -- push gcr.io/<project-name>/<image-name>:<tag>

6.  **Edit the JupyterHub configuration to build from this image.** We do this by editing the ``config.yaml`` file that we originally created to include the jupyter hashes. Edit ``config.yaml`` by including these lines in it:

    .. code-block:: bash

          singleuser:
            image:
              name: gcr.io/<project-name>/<image-name>
             tag: <tag>

7. **Tell helm to update itself using this configuration.** This makes helm
   instruct kubernetes to change the way that it builds your computing
   environment, which is now being pointed to the Docker image we’ve created::

       helm upgrade jhub helm-chart -f config.yaml

8. **Log back into your JupyterHub instance.** If you already have a running JupyterHub session, you’ll need to restart it (by restarting your session from the control panel in the top right). New users won’t have to do this.
9. **Enjoy your new computing environment!** You should now have a live computing environment built off of the Docker image we’ve created.

Authenticating with OAuth2
--------------------------

JupyterHub's `oauthenticator <https://github.com/jupyterhub/oauthenticator>`_ has support for enabling your users to authenticate via a third-party OAuth provider, including GitHub, Google, and CILogon.

Follow the service-specific instructions linked on the `oauthenticator repository <https://github.com/jupyterhub/oauthenticator>`_ to generate your JupyterHub instance's OAuth2 client ID and client secret. Then declare the values in the helm chart (``config.yaml``).

Here are example configurations for two common authentication services. Note that
in each case, you need to get the authentication credential information before
you can configure the helmchart for authentication.

**Google**

.. code-block:: bash

    auth:
      type: google
      google:
        clientId: "yourlongclientidstring.apps.googleusercontent.com"
        clientSecret: "adifferentlongstring"
        callbackUrl: "http://<your_jupyterhub_host>/hub/oauth_callback"
        hostedDomain: "youruniversity.edu"
        loginService: "Your University"

**GitHub**

.. code-block:: bash

      auth:
        type: github
        github:
          clientId: "y0urg1thubc1ient1d"
          clientSecret: "an0ther1ongs3cretstr1ng"
          callbackUrl: "http://<your_jupyterhub_host>/hub/oauth_callback"


.. _Source to Image: https://github.com/openshift/source-to-image
