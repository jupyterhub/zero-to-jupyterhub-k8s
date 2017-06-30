.. _user_experience:

Changing what is available to Users
===================================

There are many options for tweaking what your users see after they log in
to JupyterHub.

User environment
----------------

The user environment is the set of packages, environment variables, &
various files that are present when the user starts their server. You
usually do this by building a **docker image** specifying all the things
you want in it. There are many ways to build and use one - here we'll
talk about the common ones!

.. FIXME: Explain images better!

Using an existing docker image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The simplest way to proceed is to use an existing docker image that someone
else maintains. For example, the Jupyter project maintains `jupyter/docker-stacks <https://github.com/jupyter/docker-stacks/>`_,
ready to use docker images with various popular science tools in them.

For example, the `scipy-notebook <https://hub.docker.com/r/jupyter/scipy-notebook/>`_
image has a bunch of `useful libraries <https://github.com/jupyter/docker-stacks/tree/master/scipy-notebook>`_
pre-installed, and that might satisfy your needs. You can use it by modifying
your config.yaml to point to it and then applying the change.


.. code-block:: yaml

   singleuser:
     image:
       name: jupyter/scipy-notebook
       tag: 8e15d329f1e9


You can then `apply the change <#applying-configuration-changes>`_, which
will also **pre-pull** the image on all the nodes in your cluster. This
could take several minutes, so be patient.

.. note::
   Always use a specific tag, never use `latest`. That might cause multi
   minute delays or failures for users when a new version of the image is released.

Building your own image with ``repo2docker``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`repo2docker <https://github.com/jupyter/repo2docker>`_
lets you quickly convert a GitHub repository into a Docker image that we can use
as a base for your JupyterHub instance. Anything inside the GitHub repository
will exist in a user’s environment when they join your JupyterHub. If you
include a ``requirements.txt`` file in the root level of your of the repository,
repo2docker will ``pip install`` each of these packages into the Docker image to be
built. If you have an ``environment.yaml`` file, it'll use conda and create an
environment based on that specification. If you have a `Dockerfile` it will ignore
everything else and just use the Dockerfile.

Below we’ll cover how to use repo2docker to generate a Docker image and how to
configure JupyterHub to build off of this image.

1. **Download and start Docker.** You can do this by downloading and installing
   Docker at `this link <https://store.docker.com/search?offering=community&platform=desktop%2Cserver&q=&type=edition>`_.
   Once you’ve started Docker, it will show up as a tiny background application.

2. **Install repo2docker**. You can easily do this with ``pip``.

   .. code:: bash

      pip install jupyter-repo2docker


   If that doesn't work due to permissions, try:

   .. code:: bash

      pip install --user jupyter-repo2docker


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

4. **Use repo2docker to build your Docker image.**
   .. code-block:: bash

      jupyter-repo2docker <YOUR-GITHUB-REPOSITORY> --image=gcr.io/<PROJECT-NAME>/<IMAGE-NAME>:<TAG> --no-run

   This tells repo2docker to fetch master of the github repository, and use
   heuristics to build a docker image of it.

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

Setting environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Another way to affect your user's environment is by setting
`environment variables <https://en.wikipedia.org/wiki/Environment_variable>`_.
You can set them up in your Docker image too, but it is sometimes
easier to set them up in your helm chart!

As usual, you would just edit your ``config.yaml`` file and re-apply!

.. code-block:: yaml

   singleuser:
     extraEnv:
       EDITOR: "vim"

This will set the environment variable ``EDITOR`` to the value ``vim``. You
can set any number of static environment variables here as you want.

Users can read the environment variables in their code in various ways.

In python,

.. code-block:: python

   import os
   my_value = os.environ["MY_ENVIRONMENT_VARIABLE"]

Other languages will have their own methods of accessing this.

User resources
--------------

User resources are the CPU / RAM / Storage resources you provide your users.


Setting memory and CPU guarantees / limits for your users
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Storage resources
~~~~~~~~~~~~~~~~~

Each user gets their own, 10Gi disk for storage when they log in. You
can customize this in many ways!

Turning off per-user persistent storage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want users to not have any persistent storage & just want to turn
it off, you can easily do that.

.. code-block:: yaml

   singleuser:
     storage:
       type: none

When you apply this, users will no longer be allocated a persistent $HOME
directory. Currently running users will still have access to theirs until
their server is restarted.

Changing the size of per-user persistent storage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, user home directories are sized to 10Gi each. You can also
easily change this:

.. code-block:: yaml

   singleuser:
      storage:
        capacity: 5Gi

This will make all **new** user's home directories be 5Gi each, instead
of 10Gi. Note that the disks of users who have already logged in will
not change.


Pre-populating ``$HOME`` directory with notebooks
-----------------------------------------------

By default, the contents of ``$HOME`` in the docker image are hidden by
the contents of the per-user persistent volume. If you want to, you can
execute a command before the notebook starts each time and copy the files
you want from your image to the user's home directory.

If you were using the repo2docker method of building an image & wanted
your git repo copied on first use to user's home directory, you can use
the following in your config.yaml.

    .. code-block:: bash

          singleuser:
            lifecycleHooks:
              postStart:
                exec:
                  command: ["/bin/sh", "-c", "test -f $HOME/.copied || cp -Rf /srv/app/src/. $HOME/; touch $HOME/.copied"]


Note that this will only copy the contents of the directory to $HOME *once* -
the first time the user logs in. Further updates will not be reflected. There
is work in progress for making this better.
