:orphan:

.. This is a backup of the repo2docker instructions from user-environment.rst

.. _r2d-custom-image:

Build a Docker image with ``repo2docker``
-----------------------------------------

.. note::

   Docker images to be used this way must have the ``jupyterhub`` package of a
   matching version with the Helm chart. This documentation is for Helm chart
   |version|, and it uses JupyterHub version |hub_version|.

If you can't find a pre-existing image that suits your needs, you can create
your own image. An easy way to do this is with the package :term:`repo2docker`.

`repo2docker`_ lets you quickly convert
a Git repository into a Docker image that can be used as a base for your
JupyterHub instance. Anything inside the Git repository will exist in a user’s
environment when they access your JupyterHub.

``repo2docker`` will attempt to figure out what should be pre-installed, and you
can help it out by adding various configuration files to the repository. For
example if you include a ``requirements.txt`` file in the root level of the
repository, ``repo2docker`` will ``pip install`` the specified packages into the
Docker image to be built.

See `repo2docker's documentation
<https://repo2docker.readthedocs.io/en/latest/config_files.html>`_ for more
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

      jupyterhub==0.9.4
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
          tag: "<tag>"

    If the tag is the first several characters of the SHA and they happen to
    all be numerical, you *must* use quotes around the tag as above in order
    for the YAML to be parsed correctly.

7. **Tell helm to update JupyterHub to use this configuration.**

   Use the standard method to :ref:`apply the changes <apply-config-changes>` to the config.

8. **Restart your server if you are already logged in.**
   
   If you already have a running JupyterHub server, you’ll need to restart it
   from the JupyterHub control panel. Within JupyterLab look at the meny named
   "Hub". New users won’t have to do this.

   .. note::

      The contents of your GitHub repository might not show up if you have
      enabled :ref:`persistent storage <user-storage>`. Disable persistent
      storage if you want the Git repository contents to show up.

9. **Enjoy your new computing environment!**
   
   You should now have a live computing environment built off of the Docker
   image we’ve created.


.. REFERENCES USED:

.. _repo2docker: https://github.com/jupyter/repo2docker
.. _downloading and installing Docker: https://docs.docker.com/get-docker/
.. _pip: https://pip.pypa.io/en/latest/user_guide/#requirements-files
