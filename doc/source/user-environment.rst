.. _user-environment:

Customizing User Environment
============================

.. note::

   For a list of all the Helm chart options you can configure, see the
   :ref:`helm-chart-configuration-reference`.

This page contains instructions for a few common ways you can enhance the user
experience for the users of your JupyterHub deployment.

The *user environment* is the set of software packages, environment variables,
and various files that are present when the user logs into JupyterHub. The user
may also see different tools that provide interfaces to perform specialized
tasks, such as JupyterLab, RStudio, RISE and others.

A :term:`docker image` built from a ``Dockerfile`` will lay the foundation for
the environment that you will provide for the users. The image will for example
determine what Linux software (curl, vim ...), programming languages (Julia,
Python, R, ...) and development environments (JupyterLab, RStudio, ...) are made
available for use.

The following sections will describe how to use JupyterLab by default, find and
use other pre-existing images, how to build custom images, and how to set
environment variables.

.. _jupyterlab-by-default:

Use JupyterLab by default
-------------------------

`JupyterLab <http://jupyterlab.readthedocs.io/en/stable/index.html>`_ is the new
user interface for Jupyter, about to replace the classic user interface (UI).

If you have not customized what user image to use, you will default to use `this
image
<https://github.com/jupyterhub/zero-to-jupyterhub-k8s/tree/master/images/singleuser-sample>`_
that is built on top of the `base-notebook image
<https://github.com/jupyter/docker-stacks/tree/master/base-notebook>`_ residing
the `jupyter/docker-stacks repository
<https://github.com/jupyter/docker-stacks/>`_. All images in the
jupyter/docker-stacks come pre-installed with JupyterLab and the `JupyterLab-Hub
extension <https://github.com/jupyterhub/jupyterlab-hub>`_ but is not set to be
used by default in the Helm chart.

This section will help you configure your Helm chart to use JupyterLab by
default and optionally if you are building your own user image how to install it
yourself along with the JupyterLab-Hub extension.

.. note::

   Users can interchange ``/tree`` and ``/lab`` in the URL to switch between the
   classic UI and JupyterLab.

Configure JupyterLab to be used by default
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To let users default to using JupyterLab with the JupyterLab-Hub extension,
assuming your user image have JupyterLab and the JupyterLab-Hub extension
installed, do the following steps:

.. code-block:: yaml

   singleuser:
     defaultUrl: "/lab"

   hub:
     extraConfig: |
       c.Spawner.cmd = ['jupyter-labhub']

Install JupyterLab in a custom user image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To `install JupyterLab <https://github.com/jupyterlab/jupyterlab#installation>`_
and to `install the JupyterLab Hub extension
<https://github.com/jupyterhub/jupyterlab-hub#installation>`_ manually in a
custom user image you can add the following to your Dockerfile:

.. code-block:: dockerfile

   ...
   ARG JUPYTERLAB_VERSION=0.33.*
   RUN pip install jupyterlab==$JUPYTERLAB_VERSION && \
       jupyter labextension install @jupyterlab/hub-extension
   ...


.. _existing-docker-image:

Choose and use an existing Docker image
---------------------------------------

Project Jupyter maintains the `jupyter/docker-stacks repository
<https://github.com/jupyter/docker-stacks/>`_, which contains ready to use
Docker images. Each image includes a set of commonly used science and data
science libraries and tools. They also provide `excellent documentation on how
to choose a suitable image
<http://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html>`_.

.. note::

   The `Helm chart's default Docker image
   <https://github.com/jupyterhub/zero-to-jupyterhub-k8s/tree/v0.7/images/singleuser-sample>`_
   is built off the ``base-notebook`` image in jupyter/docker-stacks.

If you wish to use an existing image, such as the `scipy-notebook
<http://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-scipy-notebook>`_
image containing useful scientific programming libraries pre-installed, complete
these steps:

1. Modify your ``config.yaml`` file to specify the image. For example:

   .. code-block:: yaml

      singleuser:
        image:
          # Source:
          # https://github.com/jupyter/docker-stacks/tree/master/scipy-notebook
          # Get the latest image tag at:
          # https://hub.docker.com/r/jupyter/scipy-notebook/tags/
          name: jupyter/scipy-notebook
          tag: 7258a5c29859

   .. note::

      Container image names cannot be longer than 63 characters.

      Always use an explicit ``tag``, such as a specific commit. Avoid using
      ``latest``. Using ``latest`` might cause a several minute delay,
      confusion, or failures for users when a new version of the image is
      released.

2. Apply the changes by following the directions listed in
   `apply the changes`_. If you have *prePuller.hook.enabled*, all the nodes in
   your cluster will pull the image before the actual upgrade of the hub starts.
   This process may take several minutes to complete.

.. _r2d-custom-image:

Build a Docker image with ``repo2docker``
-----------------------------------------

.. note::

   Docker images to be used this way must have the ``jupyterhub`` package of a
   matching version with the Helm chart. This documentation is for Helm chart
   ``v0.7``, and it uses JupyterHub version ``0.9.1``.

If you can't find a pre-existing image that suits your needs, you can create
your own image. An easy way to do this is with the package :term:`repo2docker`.

`repo2docker <https://github.com/jupyter/repo2docker>`_ lets you quickly convert
a Git repository into a Docker image that can be used as a base for your
JupyterHub instance. Anything inside the Git repository will exist in a user’s
environment when they access your JupyterHub.

``repo2docker`` will attempt to figure out what should be pre-installed, and you
can help it out by adding various configuration files to the repository. For
example if you include a ``requirements.txt`` file in the root level of the
repository, ``repo2docker`` will ``pip install`` the specified packages into the
Docker image to be built.

See `repo2docker's documentation
<http://repo2docker.readthedocs.io/en/latest/config_files.html>`_ for more
details.

Below we’ll cover how to use ``repo2docker`` to generate a Docker image and how
to configure JupyterHub to build off of this image:

1. **Download and start Docker.**

   You can do this by `downloading and installing Docker`_. Once you’ve started
   Docker, it will show up as a tiny background application.

2. **Install repo2docker** using ``pip``:

   .. code:: bash

      pip install jupyter-repo2docker

   If that command fails due to insufficient permissions, try it with the
   command option, ``user``:

   .. code:: bash

      pip install --user jupyter-repo2docker


3. **Create (or find) a Git repository you want to use.**

   This repo should have all materials that you want your users to be able to
   use. You may want to include a `pip`_ ``requirements.txt`` file to list
   packages, one per file line, to install such as when using ``pip install``.
   Specify the versions explicitly so the image is fully reproducible. An
   example ``requirements.txt`` follows:

   .. code-block:: bash

      jupyterhub==0.9.1
      numpy==1.14.3
      scipy==1.1.0
      matplotlib==2.2.2

4. **Get credentials for a docker repository.**

   The image you will build for your JupyterHub must be made available by being
   published to some container registry. You could for example use `Docker Hub
   <https://hub.docker.com/>`_ or `Google Container Registry
   <https://cloud.google.com/container-registry/>`_.

   In the next step, you need an image reference for you and others to find your
   image with.

   An image reference on Docker Hub:

      .. code-block:: bash

         <dockerhub-username>/<image-name>:<image-tag>

   An image reference on Google Container Registry:

      .. code-block:: bash

         gcr.io/<cloud-project-name>/<image-name>:<image-tag>
        
   .. note::

      - Your image name can be anything memorable.
      - We recommend using the first 7 characters of the SHA in the Git
        commit as this improves reproducibility. You can get these in various
        ways, one of which is like this:
        
        .. code-block:: bash

           git ls-remote <your-git-repository> | grep HEAD | awk '{ print $1 }' | cut -c -7

4. **Use repo2docker to build a Docker image.**

   .. code-block:: bash

      jupyter-repo2docker \
          --no-run \
          --user-name=jovyan \ 
          --image=<your-image-reference> \
          <a-git-repository-url>

   This tells ``repo2docker`` to fetch ``master`` of the Git repository, and
   uses heuristics to build a Docker image of it.

5. **Push the newly-built Docker image to your repository.**

   .. code-block:: bash

      docker push <your-image-reference>

6. **Edit the JupyterHub configuration to build from this image.**
   Edit ``config.yaml`` file to include these lines in it:

   .. code-block:: yaml

      singleuser:
        image:
          name: <your-image-reference>
          tag: <tag>

7. **Tell helm to update JupyterHub to use this configuration.**

   Use the standard method to `apply the changes`_ to the config.

8. **Restart your server if you are already logged in.**
   
   If you already have a running JupyterHub server, you’ll need to restart it
   from the JupyterHub control panel. Within JupyterLab look at the meny named
   "Hub". New users won’t have to do this.

   .. note::

      The contents of your GitHub repository might not show up if you have
      enabled `persistent storage <user-storage.html>`_. Disable persistent
      storage if you want the Git repository contents to show up.

9. **Enjoy your new computing environment!**
   
   You should now have a live computing environment built off of the Docker
   image we’ve created.

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

Adding files to users' home directory
-------------------------------------

When persistent storage is enabled (which is the default), the contents of the
docker image's $HOME directory will be hidden from the user. To make these
contents visible to the user, you must pre-populate the user's filesystem. To do
so, you would include commands in the ``config.yaml`` that would be run each
time a user starts their server. The following pattern can be used in
``config.yaml``:

.. code-block:: yaml

   singleuser:
     lifecycleHooks:
       postStart:
         exec:
           command: ["cp", "-a", "src", "target"]

Each element of the command needs to be a separate item in the list. Note that
this command will be run from the ``$HOME`` location of the user's running
container, meaning that commands that place files relative to ``./`` will result
in users seeing those files in their home directory. You can use commands like
``wget`` to place files where you like.

However, keep in mind that this command will be run **each time** a user starts
their server. For this reason, we recommend using ``nbgitpuller`` to synchronize
your user folders with a git repository.

Using ``nbgitpuller`` to synchronize a folder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We recommend using the tool `nbgitpuller <https://github.com/data-8/nbgitpuller>`_
to synchronize a folder in your user's filesystem with a ``git`` repository.

To use ``nbgitpuller``, first make sure that you `install it in your Docker
image <https://github.com/data-8/nbgitpuller#installation>`_. Once this is done,
you'll have access to the ``nbgitpuller`` CLI from within JupyterHub. You can
run it with a ``postStart`` hook with the following configuration

.. code-block:: yaml

   singleuser:
     lifecycleHooks:
       postStart:
         exec:
           command: ["gitpuller", "https://github.com/data-8/materials-fa17", "master", "materials-fa"]

This will synchronize the master branch of the repository to a folder called
``$HOME/materials-fa`` each time a user logs in. See `the nbgitpuller
documentation <https://github.com/data-8/nbgitpuller>`_ for more information on
using this tool.

.. warning::

   ``nbgitpuller`` will attempt to automatically resolve merge conflicts if your
   user's repository has changed since the last sync. You should familiarize
   yourself with the `nbgitpuller merging behavior
   <https://github.com/data-8/nbgitpuller#merging-behavior>`_ prior to using the
   tool in production.

Allow users to create their own ``conda`` environments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes you want users to be able to create their own ``conda`` environments.
By default, any environments created in a JupyterHub session will not persist
across sessions. To resolve this, take the following steps:

1. Ensure the ``nb_conda_kernels`` package is installed in the root
   environment (e.g., see :ref:`r2d-custom-image`)

2. Configure Anaconda to install user environments to a folder within ``$HOME``.

   Create a file called ``.condarc`` in the home folder for all users, and make
   sure that the following lines are inside:

   .. code-block:: yaml

      envs_dirs:
        - /home/jovyan/my-conda-envs/

  The text above will cause Anaconda to install new environments to this folder,
  which will persist across sessions.

.. _apply the changes: extending-jupyterhub.html#apply-config-changes
.. _downloading and installing Docker: https://www.docker.com/community-edition
.. _pip: https://pip.readthedocs.io/en/latest/user_guide/#requirements-files
