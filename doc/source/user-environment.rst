.. _user-environment:

Customizing the User Environment
================================

.. note::

   For a list of all the options you can configure with your helm
   chart, see the :ref:`helm-chart-configuration-reference`.

This page contains instructions for a few common ways you can extend the
user experience for your kubernetes deployment.

The **user environment** is the set of packages, environment variables, and
various files that are present when the user logs into JupyterHub. The user may
also see different tools that provide interfaces to perform specialized tasks,
such as RStudio, RISE, JupyterLab, and others.

Usually a :term:`docker image` specifies the functionality and
environment that you wish to provide to users. The following sections will describe
how to use existing Docker images, how to create custom images, and how to set
environment variables.

.. _existing-docker-image:

Use an existing Docker image
----------------------------

.. note::

   The Docker image you are using must have the ``jupyterhub`` package
   installed in order to work. Moreover, the version of ``jupyterhub`` must
   match the version installed by the helm chart that you're using. For example,
   ``v0.5`` of the helm chart uses  ``jupyterhub==0.8``.

.. note::

   You can find the configuration for the default Docker image used in this
   guide `here <https://github.com/jupyterhub/zero-to-jupyterhub-k8s/tree/master/images/singleuser-sample>`_.

Using an existing Docker image, that someone else has written and maintained,
is the simplest approach. For example, Project Jupyter maintains the
`jupyter/docker-stacks <https://github.com/jupyter/docker-stacks/>`_ repo,
which contains ready to use Docker images. Each image includes a set of
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
           tag: c7fb6660d096

   .. note::

      Container image name cannot be longer than 63 characters.

      Always use an explicit ``tag``, such as a specific commit.

      Avoid using ``latest``. Using ``latest`` might cause a several minute
      delay, confusion, or failures for users when a new version of the image
      is released.

2. Apply the changes by following the directions listed in
   `apply the changes`_. These directions will **pre-pull** the image to all
   the nodes in your cluster. This process may take several minutes to
   complete.

.. note::

  Docker images must have the ``jupyterhub`` package installed within them to
  be used in this manner.

Build a custom Docker image with ``repo2docker``
------------------------------------------------

If you can't find a pre-existing image that suits your needs, you can
create your own image. The easiest way to do this is with the package
:term:`repo2docker`.

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
   this to Docker Hub or to the gcloud docker repository. Here we'll
   demonstrate pushing to the gcloud repository:

   .. code-block:: bash

      gcloud docker -- push gcr.io/<project-name>/<image-name>:<tag>

6. **Edit the JupyterHub configuration to build from this image.**
   Edit ``config.yaml`` file to include these lines in it:

   .. code-block:: yaml

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

Use JupyterLab by default
-------------------------

`JupyterLab <https://github.com/jupyterlab/jupyterlab>`_ is the next generation
user interface for Project Jupyter. It can be used with JupyterHub, both as an
optional interface and as a default.

1. Install `JupyterLab <https://github.com/jupyterlab/jupyterlab#installation>`_
   and `JupyterLab Hub extension <https://github.com/jupyterhub/jupyterlab-hub#installation>`_ 
   in your user image, for example in your Dockerfile:

   .. code-block::

      FROM jupyter/base-notebook:27ba57364579

      ...
      ARG JUPYTERLAB_VERSION=0.31.12
      RUN     pip install jupyterlab==$JUPYTERLAB_VERSION \
          &&  jupyter labextension install @jupyterlab/hub-extension
      ...

   "JupyterLab Hub" provides a nice UI for accessing JupyterHub control panel from
   JupyterLab.
   
   Without "JupyterLab Hub", users can always switch to classic Jupyter Notebook by 
   replacing the ``/lab`` in the URL after their server starts with ``/tree``.
   Similarly, you can access JupyterLab even if it is not the default by 
   replacing ``/tree`` in the URL with ``/lab``
2. Enable JupterLab in your Helm value file by adding the following snippet:

   .. code-block:: yaml

      hub:
        extraEnv:
          JUPYTER_ENABLE_LAB: 1
        extraConfig: |
          c.KubeSpawner.cmd = ['jupyter-labhub']

3. If you want users to launch automatically into JupyterLab instead of classic
   notebook, set the following setting in your Helm value file:

   .. code-block:: yaml

      singleuser:
        defaultUrl: "/lab"

   This will put users into JupyterLab when they launch their server.

.. note::

   JupyterLab is in beta, so use with caution!

Set environment variables
-------------------------

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

Pre-populating user's ``$HOME`` directory with files
----------------------------------------------------

When persistent storage is enabled (which is the default), the contents of the
docker image's $HOME directory will be hidden from the user. To make these
contents visible to the user, you must pre-populate the user's
filesystem. To do so, you would include commands in the ``config.yaml`` that would
be run each time a user starts their server. The following pattern can be used
in ``config.yaml``:

.. code-block:: yaml

   singleuser:
     lifecycleHooks:
       postStart:
         exec:
           command: ["your", "command", "here"]

Note that this command will be run from the ``$HOME`` location of the user's
running container, meaning that commands that place files relative to ``./``
will result in users seeing those files in their home directory. You can use
commands like ``wget`` to place files where you like.

However, keep in mind that this command will be run **each time** a user
starts their server. For this reason, we recommend using ``nbgitpuller`` to
synchronize your user folders with a git repository.

Using ``nbgitpuller`` for synchronizing a folder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We recommend using the tool `nbgitpuller <https://github.com/data-8/nbgitpuller>`_
to synchronize a folder in your user's filesystem with a ``git`` repository.

To use ``nbgitpuller``, first make sure that you `install it in your Docker
image <https://github.com/data-8/nbgitpuller#installation>`_.
Once this is done, you'll have access to the ``nbgitpuller`` CLI from within
JupyterHub. You can run it with a ``postStart`` hook with the following configuration

.. code-block:: yaml

   singleuser:
     lifecycleHooks:
       postStart:
         exec:
           command: ["gitpuller", "https://github.com/data-8/materials-fa17", "master", "materials-fa"]

This will synchronize the master branch of the repository to a folder called
``$HOME/materials-fa`` each time a user logs in. See `the nbgitpuller documentation <https://github.com/data-8/nbgitpuller>`_
for more information on using this tool.

.. warning::

   ``nbgitpuller`` will attempt to automatically resolve merge conflicts if
   your user's repository has changed since the last sync. You should familiarize
   yourself with the `nbgitpuller merging behavior <https://github.com/data-8/nbgitpuller#merging-behavior>`_
   prior to using the tool in production.

.. _apply the changes: extending-jupyterhub.html#apply-config-changes
.. _downloading and installing Docker: https://store.docker.com/search?offering=community&platform=desktop%2Cserver&q=&type=edition
.. _pip: https://pip.readthedocs.io/en/latest/user_guide/#requirements-files
