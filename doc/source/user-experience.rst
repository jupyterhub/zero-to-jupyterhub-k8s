.. _user_experience:

Customization of the User Experience
====================================

Users, depending on their work needs, require different libraries, packages,
and files. Often, users wish to **tailor the user environment** to meet
their personal preferences.

Since JupyterHub can serve many different types of users, JupyterHub managers
and administrators must be able to flexibly **allocate user resources**, like
memory or compute. For example, the Hub may be serving power users with large
resource requirements as well as beginning users with more basic resource
needs. The ability to customize the Hub's resources to satisfy both user
groups improves the user experience for all Hub users.


Tailoring the user environment
------------------------------

The **user environment** is the set of packages, environment variables, and
various files that are present when the user logs into JupyterHub. The user may
also see different tools that provide interfaces to perform specialized tasks,
such as RStudio, RISE, JupyterLab, and others.

Usually a :term:`docker image` specifies the different functionality and
things that you wish to provide to users. The following sections will describe
how to use existing docker images, how to create custom images, and how to set
environment variables.

Use an existing docker image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using an existing docker image, that someone else has written and maintained,
is the simplest approach. For example, Project Jupyter maintains the
`jupyter/docker-stacks <https://github.com/jupyter/docker-stacks/>`_ repo,
which contains ready to use docker images. Each image includes a set of
commonly used science and data science libraries and tools.

The `scipy-notebook <https://hub.docker.com/r/jupyter/scipy-notebook/>`_
image, which can be found in the ``docker-stacks`` repo, contains
`useful scientific programming libraries
<https://github.com/jupyter/docker-stacks/tree/master/scipy-notebook>`_
pre-installed. This image may satisfy your needs. If you wish to use an
existing image, such as the ``scipy-notebook`` image, complete these steps:

1. Modify your ``config.yaml`` file to specify the image. For example:

   .. code-block:: yaml

       singleuser:
         image:
           name: jupyter/scipy-notebook
           tag: 8e15d329f1e9

   .. note::

      Always use an explicit ``tag``, such as a specific commit.

      Avoid using ``latest``. Using ``latest`` might cause a several minute
      delay, confusion, or failures for users when a new version of the image
      is released.

2. Apply the changes by following the directions listed in
   `apply the changes`_. These directions will **pre-pull** the image to all
   the nodes in your cluster. This process may take several minutes to
   complete.

Build a custom image with ``repo2docker``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you can't find a pre-existing image that suits your needs, you can
create your own image. The easiest way to do this is with the package
:term:``repo2docker``.

.. note::

   `repo2docker <https://github.com/jupyter/repo2docker>`_ lets you quickly
   convert a GitHub repository into a Docker image that can be used as a base
   for your JupyterHub instance. Anything inside the GitHub repository
   will exist in a user’s environment when they join your JupyterHub:

   - If you include a ``requirements.txt`` file in the root level of the
     repository, ``repo2docker`` will ``pip install`` the specified packages
     into the Docker image to be built.
   - If you have an ``environment.yaml`` file, ``conda`` will create an
     environment based on this file's specification.
   - If you have a ``Dockerfile``, ``repo2docker`` will ignore everything
     else and just use the Dockerfile.

Below we’ll cover how to use ``repo2docker`` to generate a Docker image and
how to configure JupyterHub to build off of this image:

1. **Download and start Docker.** You can do this by
   `downloading and installing Docker`_. Once you’ve started Docker,
   it will show up as a tiny background application.

2. **Install repo2docker** using ``pip``:

   .. code:: bash

      pip install jupyter-repo2docker

   If that command fails due to insufficient permissions, try it with the
   command option, ``user``:

   .. code:: bash

      pip install --user jupyter-repo2docker


3. **Create (or find) a GitHub repository you want to use.** This repo should
   have all materials that you want your users to be able to use. You may want
   to include a `pip`_ ``requirements.txt`` file to list packages, one per
   file line, to install such as when using ``pip install``. Specify the
   versions explicitly so the image is fully reproducible. An example
   ``requirements.txt`` follows:

   .. code-block:: bash

      numpy==1.12.1
      scipy==0.19.0
      matplotlib==2.0

4. **Use repo2docker to build a Docker image.**

   .. code-block:: bash

      jupyter-repo2docker <YOUR-GITHUB-REPOSITORY> --image=gcr.io/<PROJECT-NAME>/<IMAGE-NAME>:<TAG> --no-run

   This tells ``repo2docker`` to fetch ``master`` of the GitHub repository,
   and uses heuristics to build a docker image of it.

  .. note::

     - The project name should match your google cloud project's name.
     - Don’t use underscores in your image name. Other than this, the name can
       be anything memorable. *This bug with underscores will be fixed soon.*
     - The tag should be the first 6 characters of the SHA in the GitHub
       commit desired for building the image since this improves
       reproducibility.

5. **Push the newly-built Docker image to the cloud.** You can either push
   this to Docker Hub, or to the gcloud docker repository. Here we'll
   demonstrate pushing to the gcloud repository:

   .. code-block:: bash

      gcloud docker -- push gcr.io/<project-name>/<image-name>:<tag>

6. **Edit the JupyterHub configuration to build from this image.**
   Edit ``config.yaml`` file to include these lines in it:

   .. code-block:: bash

      singleuser:
        image:
          name: gcr.io/<project-name>/<image-name>
          tag: <tag>

   This step can be done automatically by setting a flag if desired.

7. **Tell helm to update JupyterHub to use this configuration.** Use the
   standard method to `apply the changes`_ to the config.

8. **Restart your notebook if you are already logged in.** If you already have
   a running JupyterHub session, you’ll need to restart it (by stopping and
   starting your session from the control panel in the top right). New users
   won’t have to do this.

   .. note::

      The contents of your GitHub repository might not show up if you have
      enabled `persistent storage <user_storage>`_. Disable persistent storage
      if you want the
      GitHub repository contents to show up.

9. **Enjoy your new computing environment!** You should now have a live
   computing environment built off of the Docker image we’ve created.

Set environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~

Another way to affect your user's environment is by setting values for
:term:`environment variables`. While you can set them up in your Docker image,
it is often easier to set them up in your helm chart.

To set them up in your helm chart, edit your ``config.yaml`` file
and `apply the changes`_. For example, this code snippet will set the
environment variable ``EDITOR`` to the value ``vim``:

.. code-block:: yaml

   singleuser:
     extraEnv:
       EDITOR: "vim"

You can set any number of static environment variables in the ``config.yaml``
file.

Users can read the environment variables in their code in various ways. In
Python, for example, the following code will read in an environment variable:

.. code-block:: python

   import os
   my_value = os.environ["MY_ENVIRONMENT_VARIABLE"]

Other languages will have their own methods of reading these environment
variables.


Allocating and controlling user resources
-----------------------------------------

User resources include the CPU, RAM, and Storage which JupyterHub provides to
users.


Set user memory and CPU guarantees / limits
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

    Remember to `apply the changes`_ after changing your ``config.yaml`` file!

.. _user_storage:

Allocate user storage
~~~~~~~~~~~~~~~~~~~~~

By default, each user receives their own, 10Gi disk for storage when they log in
to JupyterHub. This storage can be turned off or customized as described in these
sections.

Turn off per-user persistent storage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you do not wish for users to have any persistent storage, it can be
turned off. Edit the ``config.yaml`` file and set the storage type to ``none``:

.. code-block:: yaml

   singleuser:
     storage:
       type: none

Next `apply the changes`_. After the changes are applied, new users
will no longer be allocated a persistent ``$HOME`` directory. Any currently
running users will still have access to their storage until their server
is restarted.

Change per-user persistent storage size
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, user home directories are sized to 10Gi each. To change this
value, edit the ``config.yaml`` file:

.. code-block:: yaml

   singleuser:
      storage:
        capacity: 5Gi

This example will make all **new** user's home directories be 5Gi each,
instead of 10Gi.

.. important::

   The disks of "logged in" users will not change or be decreased in
   this example.


Advanced topic: Pre-populating user's ``$HOME`` directory with notebooks
------------------------------------------------------------------------

By default, the contents of ``$HOME`` in the docker image are hidden by
the contents of the per-user persistent volume. If you want to, you can
execute a command before the notebook starts each time and copy the files
you want from your image to the user's home directory.

If you were using the repo2docker method of building an image and wanted
your git repo copied on first use to the user's home directory, you can
use the following in your ``config.yaml`` file:

    .. code-block:: bash

          singleuser:
            lifecycleHooks:
              postStart:
                exec:
                  command: ["/bin/sh", "-c", "test -f $HOME/.copied || cp -Rf /srv/app/src/. $HOME/; touch $HOME/.copied"]

.. note::

   Note that this will only copy the contents of the directory to ``$HOME``
   *once* - the first time the user logs in. Further updates will not be
   reflected. *There is work in progress for improving this behavior.*

.. _apply the changes: #applying-configuration-changes
.. _downloading and installing Docker: https://store.docker.com/search?offering=community&platform=desktop%2Cserver&q=&type=edition
.. _pip: https://pip.readthedocs.io/en/latest/user_guide/#requirements-files