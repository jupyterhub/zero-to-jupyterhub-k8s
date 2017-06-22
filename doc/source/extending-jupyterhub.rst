.. _extending-jupyterhub:

Extending your JupyterHub setup
===============================

The helm chart used to install JupyterHub has a lot of options for you to tweak.
This page lists some of the most common changes.


Applying configuration changes
------------------------------

The general method is:

1. Make a change to the ``config.yaml``
2. Run a helm upgrade:

     .. code-block:: bash

        helm upgrade <YOUR_RELEASE_NAME> https://github.com/jupyterhub/helm-chart/releases/download/v0.3/jupyterhub-v0.3.tgz -f config.yaml

   Where ``<YOUR_RELEASE_NAME>`` is the parameter you passed to ``--name`` when
   `installing jupyterhub <setup-jupyterhub.html#install-jupyterhub>`_ with
   ``helm install``. If you don't remember it, you can probably find it by doing
   ``helm list``.
3. Wait for the upgrade to finish, and make sure that when you do
   ``kubectl --namespace=<YOUR_NAMESPACE> get pod`` the hub and proxy pods are
   in ``Ready`` state. Your configuration change has been applied!

Using an existing image
-----------------------

It's possible to build your JupyterHub deployment off of a pre-existing Docker
image. To do this, you need to find an existing image somewhere (such as
DockerHub), and configure your installation to use it.

For example, UC Berkeley's `Data8 Program <https://hub.docker.com/r/berkeleydsep/singleuser-data8>`_
publishes the image they are using on Dockerhub. To instruct JupyterHub to use
this image, simply add this to your ``config.yaml`` file:

    .. code-block:: yaml

       singleuser:
           image:
              name: berkeleydsep/singleuser-data8
              tag: v0.1


You can then `apply the change <#applying-configuration-changes>`_ to the
config as usual.


Setting memory and CPU guarantees / limits for your users
---------------------------------------------------------

Each user on your JupyterHub gets a slice of memory and CPU to use. There are
two ways to specify how much users get to use: resource *guarantees* and
resource *limits*.

A resource *guarantee* means that all users will have *at least* this resource
available at all times, but they may be given more resources if they're
available. For example, if users are *guaranteed* 1G of RAM, users can
technically use more than 1G of RAM if these resources aren't being used by
other users.

A resource *limit* sets a hard limit on the resources available. In the example
above, if there were a 1G memory limit, it would mean that users could use
no more than 1G of RAM, no matter what other resources are being used on the
machines.

By default, each user is *guaranteed* 1G of RAM. All users have *at least* 1G,
but they can technically use more if it is available. You can easily change the
amount of these resources, and whether they are a *guarantee* or a *limit*, by
changing your ``config.yaml`` file. This is done with the following structure.

    .. code-block:: yaml

       singleuser:
           memory:
              limit: 1G
              guarantee: 1G

This sets a memory limit and guarantee of 1G. Kubernetes will make sure that
each user will always have access to 1G of RAM, and requests for more RAM will
fail (your kernel will usually die). You can set the limit to be higher than
the guarantee to allow some users to use larger amounts of RAM for
a very short-term time (e.g. when running a single, short-lived function that
consumes a lot of memory).

.. note::
    Remember `apply the changes <#applying-configuraiton-changes>`_ after changing
    your config.yaml file!

Extending your software stack with s2i
--------------------------------------

s2i, also known as `Source to Image <https://github.com/openshift/source-to-image>`_,
lets you quickly convert a GitHub repository into a Docker image that we can use
as a base for your JupyterHub instance. Anything inside the GitHub repository
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
   ``pip install``. You should also specify the versions explicitly so the image is
   fully reproducible. E.g.:

   .. code-block:: bash

          numpy==1.12.1
          scipy==0.19.0
          matplotlib==2.0

4. **Use s2i to build your Docker image.** `s2i` uses a template in order to
   know how to create the Docker image. We have provided one at the url in the
   commands below. Run this command::

       s2i build --exclude "" <git-repo-url>  jupyterhub/singleuser-builder-venv-3.5:v0.1.5 gcr.io/<project-name>/<name-of-image>:<tag>

   this effectively says *s2i, build `<this repository>` to a Docker image by
   using `<this template>` and call the image `<this>`*. The `--exclude ""` ensures
   that all files are included in the container (e.g. `.git` directory).

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

6. **Edit the JupyterHub configuration to build from this image.** We do this
   by editing the ``config.yaml`` file that we originally created to include
   the jupyter hashes. Edit ``config.yaml`` by including these lines in it:

    .. code-block:: bash

          singleuser:
            image:
              name: gcr.io/<project-name>/<image-name>
              tag: <tag>

7. **Tell helm to update JupyterHub to use this configuration.** Using the
   normal method to `apply the change <#applying-configuration-changes>`_ to
   the config.
8. **Restart your notebook if you are already logging in** If you already have
   a running JupyterHub session, you’ll need to restart it (by stopping and
   starting your session from the control panel in the top right). New users
   won’t have to do this.
9. **Enjoy your new computing environment!** You should now have a live
   computing environment built off of the Docker image we’ve created.

   .. note::
      The contents of your GitHub repository might not show up if you have
      enabled persistent storage. Disable persistent storage if you want them
      to show up!

Pre-populating `$HOME` directory with notebooks when using Persistent Volumes
-----------------------------------------------------------------------------

By default, Persistent Volumes are used, so if you would like to include the
contents of the GitHub repository in the `$HOME` directory (e.g. all of the
`*.ipynb` files), then edit ``config.yaml`` include these lines in it:

    .. code-block:: bash

          singleuser:
            lifecycleHooks:
              postStart:
                exec:
                  command: ["/bin/sh", "-c", "test -f $HOME/.copied || cp -Rf /srv/app/src/. $HOME/; touch $HOME/.copied"]


Note that this will only copy the contents of the directory to $HOME *once* -
the first time the user logs in. Further updates will not be reflected. There
is work in progress for making this better.

Authenticating with OAuth2
--------------------------

JupyterHub's `oauthenticator <https://github.com/jupyterhub/oauthenticator>`_
has support for enabling your users to authenticate via a third-party OAuth
provider, including GitHub, Google, and CILogon.

Follow the service-specific instructions linked on the
`oauthenticator repository <https://github.com/jupyterhub/oauthenticator>`_
to generate your JupyterHub instance's OAuth2 client ID and client secret. Then
declare the values in the helm chart (``config.yaml``).

Here are example configurations for two common authentication services. Note
that in each case, you need to get the authentication credential information
before you can configure the helmchart for authentication.

**Google**

For more information see the full example of Google OAuth2 in the next section.

.. code-block:: yaml

    auth:
      type: google
      google:
        clientId: "yourlongclientidstring.apps.googleusercontent.com"
        clientSecret: "adifferentlongstring"
        callbackUrl: "http://<your_jupyterhub_host>/hub/oauth_callback"
        hostedDomain: "youruniversity.edu"
        loginService: "Your University"

**GitHub**

.. code-block:: yaml

      auth:
        type: github
        github:
          clientId: "y0urg1thubc1ient1d"
          clientSecret: "an0ther1ongs3cretstr1ng"
          callbackUrl: "http://<your_jupyterhub_host>/hub/oauth_callback"

Full Example of Google OAuth2
-----------------------------

If your institution is a `G Suite customer <https://gsuite.google.com>`_ that
integrates with Google services such as Gmail, Calendar, and Drive, you can
authenticate users to your JupyterHub using Google for authentication.

.. note::
       Google requires that you specify a fully qualified domain name for your
       hub rather than an IP address.

1. Log in to the `Google API Console <https://console.developers.google.com>`_.

2. Select a project > Create a project... and set 'Project name'. This is a
   short term that is only displayed in the console. If you have already
   created a project you may skip this step.

3. Type "Credentials" in the search field at the top and click to access the
   Credentials API.

4. Click "Create credentials", then "OAuth client ID". Choose
   "Application type" > "Web application".

5. Enter a name for your JupyterHub instance. You can give it a descriptive
   name or set it to be the hub's hostname.

6. Set "Authorized JavaScript origins" to be your hub's URL.

7. Set "Authorized redirect URIs" to be your hub's URL followed by
   "/hub/oauth_callback". For example, http://example.com/hub/oauth_callback.

8. When you click "Create", the console will generate and display a Client ID
   and Client Secret. Save these values.

9. Type "consent screen" in the search field at the top and click to access the
   OAuth consent screen. Here you will customize what your users see when they
   login to your JupyterHub instance for the first time. Click Save when you
   are done.

10. In your helm chart, create a stanza that contains these OAuth fields:

.. code-block:: bash

    auth:
      type: google
      google:
        clientId: "yourlongclientidstring.apps.googleusercontent.com"
        clientSecret: "adifferentlongstring"
        callbackUrl: "http://<your_jupyterhub_host>/hub/oauth_callback"
        hostedDomain: "youruniversity.edu"
        loginService: "Your University"

The 'callbackUrl' key is set to the authorized redirect URI you specified
earlier. Set 'hostedDomain' to your institution's domain name. The value of
'loginService' is a descriptive term for your institution that reminds your
users which account they are using to login.

Expanding and contracting the size of your cluster
--------------------------------------------------

You can easily scale up or down your cluster's size to meet usage demand or to
save cost when the cluster is not being used. Use the ``resize`` command and
provide a new cluster size as a command line option ``--size``:

.. code-block:: bash

   gcloud container clusters resize \
                <YOUR-CLUSTER-NAME> \
                --size <NEW-SIZE> \
                --zone <YOUR-CLUSTER-ZONE>

To display the cluster's name, zone, or current size, use the command
``gcloud container clusters list``.

.. note::

   When organizing and running a workshop, resizing a cluster gives you a way
   to save cost and prepare JupyterHub before the event. For example:

   - **One week before the workshop:** You can create the cluster, set
     everything up, and then resize the cluster to zero nodes to save cost.
   - **On the day of the workshop:** You can scale the cluster up to a suitable
     size for the workshop. This workflow also helps you avoid scrambling on
     the workshop day to set up the cluster and JupyterHub.
   - **After the workshop:** The cluster can be deleted.
