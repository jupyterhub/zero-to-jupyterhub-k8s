(user-environment)=

# Customizing User Environment

This page contains instructions for common ways to enhance the user experience.
For a list of all the configurable Helm chart options, see the
{ref}`helm-chart-configuration-reference`.

The _user environment_ is the set of software packages, environment variables,
and various files that are present when the user logs into JupyterHub. The user
may also see different tools that provide interfaces to perform specialized
tasks, such as JupyterLab, RStudio, RISE and others.

A {term}`Docker image` built from a {term}`Dockerfile` will lay the foundation for
the environment that you will provide for the users. The image will for example
determine what Linux software (curl, vim ...), programming languages (Julia,
Python, R, ...) and development environments (JupyterLab, RStudio, ...) are made
available for use.

To get started customizing the user environment, see the topics below.

(existing-docker-image)=

## Choose and use an existing Docker image

This chart uses a minimal default singleuser image intended for quick tests.
You will need to choose a different image or build your own for real use.

Project Jupyter maintains the [jupyter/docker-stacks repository](https://github.com/jupyter/docker-stacks/), which contains ready to use
Docker images. Each image includes a set of commonly used science and data
science libraries and tools. They also provide excellent documentation on [how
to choose a suitable image](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html).

For example, to use the [datascience-notebook](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-datascience-notebook)
image containing useful tools and libraries for data science, complete these steps:

1. Modify your `config.yaml` file to specify the image. For example:

   ```yaml
   singleuser:
     image:
       # You should replace the "latest" tag with a fixed version from:
       # https://hub.docker.com/r/jupyter/datascience-notebook/tags/
       # Inspect the Dockerfile at:
       # https://github.com/jupyter/docker-stacks/tree/HEAD/datascience-notebook/Dockerfile
       name: jupyter/datascience-notebook
       tag: latest
     # `cmd: null` allows the custom CMD of the Jupyter docker-stacks to be used
     # which performs further customization on startup.
     cmd: null
   ```

   ```{note}
   Container image names cannot be longer than 63 characters.

   Always use an explicit `tag`, such as a specific commit. Avoid using
   `latest` as it might cause a several minute delay, confusion, or
   failures for users when a new version of the image is released.
   ```

2. Apply the changes by following the directions listed in
   {ref}`apply the changes <apply-config-changes>`.

   If you have configured _prePuller.hook.enabled_, all the nodes in your
   cluster will pull the image before the hub is upgraded to let users
   use the image. The image pulling may take several minutes to complete,
   depending on the size of the image.

3. Restart your server from JupyterHub control panel if you are already logged in.

```{note}
If you'd like users to select an environment from **multiple docker images**,
see {ref}`multiple-profiles`.
```

(user-interfaces)=

## Selecting a user interface

[JupyterLab][] is the new user interface for Jupyter,
which is meant to replace the classic notebook user interface (UI).
Users can already interchange `/tree` and `/lab` in the URL to switch between
the classic UI and JupyterLab if both are installed.
Deployments using JupyterHub 1.x and earlier default to the classic UI,
while JupyterHub 2.0 makes JupyterLab the default.

[jupyterlab]: https://jupyterlab.readthedocs.io

To pick a user interface to launch by default for users, two customization items need to be set:

1. the preferred default user interface (UI)
2. the server program to launch

There are two main Jupyter server implementations
(_Most deployments will not see a difference,
but there can be issues for certain server extensions. If unsure, new applications should choose `jupyter_server`._):

1. the modern `jupyter server`,
   which is launched when you use `jupyter lab` or other recent Jupyter applications, and
2. the 'classic' legacy notebook server (`jupyter notebook`)

In general, the default UI is selected in {term}`config.yaml` by

```yaml
singleuser:
  defaultUrl: ...
```

and the default server by:

```yaml
singleuser:
  extraEnv:
    JUPYTERHUB_SINGLEUSER_APP: "..."
```

Specifically, use one of these options to select the modern server:

```yaml
# this is the default with JupyterHub 2.0
singleuser:
  extraEnv:
    JUPYTERHUB_SINGLEUSER_APP: "jupyter_server.serverapp.ServerApp"
```

or the classic notebook server:

```yaml
# the default with JupyterHub 1.x
singleuser:
  extraEnv:
    JUPYTERHUB_SINGLEUSER_APP: "notebook.notebookapp.NotebookApp"
```

You only need the above configuration when it is different from the default.
JupyterHub 2.0 changes the default server from `NotebookApp` to `ServerApp`,
so here we make the choice explicit in each example,
so the same configuration produces the same result with JupyterHub 1.x and 2.x.
That way, your choice will be preserved across upgrades.

(jupyterlab-by-default)=

## Use JupyterLab by default

```{note}
This is the default in JupyterHub 2.0 and Helm chart 2.0.
```

You can choose JupyterLab as the default UI with the following config in your {term}`config.yaml`:

```yaml
singleuser:
  defaultUrl: "/lab"
  extraEnv:
    JUPYTERHUB_SINGLEUSER_APP: "jupyter_server.serverapp.ServerApp"
```

You can also make JupyterLab the default UI _without_ upgrading to the newer server implementation.
This may help users who need to stick to the legacy UI with extensions that may not work on the new server.

```yaml
singleuser:
  defaultUrl: "/lab"
  extraEnv:
    JUPYTERHUB_SINGLEUSER_APP: "notebook.notebookapp.NotebookApp"
```

```{note}
You need the `jupyterlab` package (installable via `pip` or `conda`)
for this to work. All images in the [jupyter/docker-stacks repository](https://github.com/jupyter/docker-stacks/) come pre-installed with it.
```

(classic-by-default)=

### Use classic notebook by default

```{note}
This is the default in JupyterHub 1.x and helm chart 1.x.
```

If you aren't ready to upgrade to JupyterLab,
especially for those who depend on custom notebook extensions without an equivalent in JupyterLab,
you can always stick with the legacy notebook server (`jupyter notebook`):

```yaml
# the default with JupyterHub 1.x
singleuser:
  extraEnv:
    JUPYTERHUB_SINGLEUSER_APP: "notebook.notebookapp.NotebookApp"
```

This will start the exact same server and UI as before.

If you install the `nbclassic` package,
you can also default to the classic UI, running on the new server:
This may be the best way to support users on both classic and new environments.

```yaml
singleuser:
  defaultUrl: /tree/
  extraEnv:
    JUPYTERHUB_SINGLEUSER_APP: "jupyter_server.serverapp.ServerApp"
```

### Alternative interfaces

There are more Jupyter server extensions providing alternate UI choices,
which can be used with JupyterHub.

For example, [retrolab][] is a different notebook interface, built on JupyterLab,
but which may be more comfortable for those coming from the classic Jupyter UI.

[retrolab]: https://blog.jupyter.org/retrolab-a-jupyterlab-distribution-with-a-retro-look-and-feel-8096b8b223d0

To install such an extension:

1. install the package (`pip install retrolab` or `conda install retrolab`) in your user container image
2. configure the default URL, and make sure ServerApp is used:

```yaml
singleuser:
  defaultUrl: /retro/
  extraEnv:
    JUPYTERHUB_SINGLEUSER_APP: "jupyter_server.serverapp.ServerApp"
```

(custom-docker-image)=

## Customize an existing Docker image

If you are missing something in the image that you would like all users to have,
we recommend that you build a new image on top of an existing Docker image from
jupyter/docker-stacks.

Below is an example {term}`Dockerfile` building on top of the _minimal-notebook_
image. This file can be built to a {term}`Docker image`, and pushed to a
{term}`image registry`, and finally configured in {term}`config.yaml` to be used
by the Helm chart.

```Dockerfile
FROM jupyter/minimal-notebook:latest
# Replace `latest` with an image tag from to ensure reproducible builds:
# https://hub.docker.com/r/jupyter/minimal-notebook/tags/
# Inspect the Dockerfile at:
# https://github.com/jupyter/docker-stacks/tree/HEAD/minimal-notebook/Dockerfile

# install additional package...
RUN pip install --no-cache-dir astropy

# set the default command of the image,
# if you want to launch more complex startup than the default `juptyerhub-singleuser`.
# To launch an image's custom CMD instead of the default `jupyterhub-singleuser`
# set `singleuser.cmd: null` in your config.yaml.
```

```{note}
If you are using a private image registry, you may need to setup the image
credentials. See the :ref:`helm-chart-configuration-reference` for more
details on this.
```

(set-env-vars)=

## Set environment variables

One way to affect your user's environment is by setting {term}`environment variables`. While you can set them up in your Docker image if you build it
yourself, it is often easier to configure your Helm chart through values
provided in your {term}`config.yaml`.

To set this up, edit your {term}`config.yaml` and
{ref}`apply the changes <apply-config-changes>`.
For example, this code snippet will set the environment variable `EDITOR` to the
value `vim`:

```yaml
singleuser:
  extraEnv:
    EDITOR: "vim"
```

You can set any number of static environment variables in the
{term}`config.yaml` file.

Users can read the environment variables in their code in various ways. In
Python, for example, the following code reads an environment variable's value:

```python
import os
my_value = os.environ["MY_ENVIRONMENT_VARIABLE"]
```

(add-files-to-home)=

## About user storage and adding files to it

It is important to understand the basics of how user storage is set up. By
default, each user will get 10GB of space on a harddrive that will persist in
between restarts of their server. This harddrive will be mounted to their home
directory. In practice this means that everything a user writes to the home
directory (`/home/jovyan`) will remain, and everything else will be reset in
between server restarts.

A server can be shut down by _culling_. By default, JupyterHub's culling service
is configured to cull a users server that has been inactive for one hour. Note
that JupyterLab will autosave files, and as long as the file was within the
users home directory no work is lost.

```{note}
In Kubernetes, a *PersistantVolume* (PV) represents the harddrive.
KubeSpawner will create a PersistantVolumeClaim that requests a PV from the
cloud. By default, deleting the PVC will cause the cloud to delete the PV.
```

Docker image's $HOME directory will be hidden from the user. To make these
contents visible to the user, you must pre-populate the user's filesystem. To do
so, you would include commands in the `config.yaml` that would be run each
time a user starts their server. The following pattern can be used in
{term}`config.yaml`:

```yaml
singleuser:
  lifecycleHooks:
    postStart:
      exec:
        command: ["cp", "-a", "src", "target"]
```

Each element of the command needs to be a separate item in the list. Note that
this command will be run from the `$HOME` location of the user's running
container, meaning that commands that place files relative to `./` will result
in users seeing those files in their home directory. You can use commands like
`wget` to place files where you like.

A simple way to populate the notebook user's home directory is to add the
required files to the container's `/tmp` directory and then copy them to
`/home/jovyan` using a `postStart` hook. This example shows the use of
multiple commands.

```yaml
singleuser:
  lifecycleHooks:
    postStart:
      exec:
        command:
          - "sh"
          - "-c"
          - >
            cp -r /tmp/foo /home/jovyan;
            cp -r /tmp/bar /home/jovyan
```

Keep in mind that commands will be run **each time** a user starts
their server. For this reason, we recommend using `nbgitpuller` to synchronize
your user folders with a git repository.

(use-nbgitpuller)=

### Using `nbgitpuller` to synchronize a folder

We recommend using the tool [nbgitpuller](https://github.com/jupyterhub/nbgitpuller) to synchronize a folder
in your user's filesystem with a `git` repository whenever a user
starts their server. This synchronization can also be triggered by
letting a user visit a link like
`https://your-domain.com/hub/user-redirect/git-pull?repo=https://github.com/data-8/materials-fa18`
(e.g., as alternative start url).

To use `nbgitpuller`, first make sure that you [install it in your Docker
image](https://github.com/jupyterhub/nbgitpuller#installation). Once this is done,
you'll have access to the `nbgitpuller` CLI from within JupyterHub. You can
run it with a `postStart` hook with the following configuration

```yaml
singleuser:
  lifecycleHooks:
    postStart:
      exec:
        command:
          [
            "gitpuller",
            "https://github.com/data-8/materials-fa17",
            "master",
            "materials-fa",
          ]
```

This will synchronize the master branch of the repository to a folder called
`$HOME/materials-fa` each time a user logs in. See [the nbgitpuller
documentation](https://github.com/jupyterhub/nbgitpuller) for more information on
using this tool.

```{warning}
`nbgitpuller` will attempt to automatically resolve merge conflicts if your
user's repository has changed since the last sync. You should familiarize
yourself with the [nbgitpuller merging behavior](https://github.com/jupyterhub/nbgitpuller#merging-behavior) prior to using the
tool in production.
```

(setup-conda-envs)=

### Allow users to create their own `conda` environments for notebooks

Sometimes you want users to be able to create their own `conda` environments.
By default, any environments created in a JupyterHub session will not persist
across sessions. To resolve this, take the following steps:

1. Ensure the `nb_conda_kernels` package is installed in the root
   environment (e.g., see {ref}`r2d-custom-image`)
2. Configure Anaconda to install user environments to a folder within `$HOME`.

   Create a file called `.condarc` in the home folder for all users, and make
   sure that the following lines are inside:

   ```yaml
   envs_dirs:
     - /home/jovyan/my-conda-envs/
   ```

The text above will cause Anaconda to install new environments to this folder,
which will persist across sessions.

These environments are supposed to be used in notebooks, so a typical use case:

1. Create one with at least a kernel, e.g. for Python it's `conda create -n myenv ipykernel scipy`
2. Now this env should be available in the list of kernels

(multiple-profiles)=

## Using multiple profiles to let users select their environment

You can create configurations for multiple user environments,
and let users select from them once they log in to your JupyterHub. This
is done by creating multiple **profiles**, each of which is attached to a set
of configuration options that override your JupyterHub's default configuration
(specified in your Helm Chart). This can be used to let users choose among many
Docker images, to select the hardware on which they want their jobs to run,
or to configure default interfaces such as Jupyter Lab vs. RStudio.

Each configuration is a set of options for [KubeSpawner](https://github.com/jupyterhub/kubespawner),
which defines how Kubernetes should launch a new user server pod. Any
configuration options passed to the `profileList` configuration will
overwrite the defaults in KubeSpawner (or any configuration you've
added elsewhere in your helm chart).

Profiles are stored under `singleuser.profileList`, and are defined as
a list of profiles with specific configuration options each. Here's an example:

```yaml
singleuser:
  profileList:
    - display_name: "Name to be displayed to users"
      description: "Longer description for users."
      # Configuration unique to this profile
      kubespawner_override:
        your_config: "Your value"
      # Defines the default profile - only use for one profile
      default: true
```

The above configuration will show a screen with information about this profile
displayed when users start a new server.

Here's an example with four profiles that lets users select the environment they
wish to use.

```yaml
singleuser:
  # Defines the default image
  image:
    name: jupyter/minimal-notebook
    tag: 2343e33dec46
  profileList:
    - display_name: "Minimal environment"
      description: "To avoid too much bells and whistles: Python."
      default: true
    - display_name: "Datascience environment"
      description: "If you want the additional bells and whistles: Python, R, and Julia."
      kubespawner_override:
        image: jupyter/datascience-notebook:2343e33dec46
    - display_name: "Spark environment"
      description: "The Jupyter Stacks spark image!"
      kubespawner_override:
        image: jupyter/all-spark-notebook:2343e33dec46
    - display_name: "Learning Data Science"
      description: "Datascience Environment with Sample Notebooks"
      kubespawner_override:
        image: jupyter/datascience-notebook:2343e33dec46
        lifecycle_hooks:
          postStart:
            exec:
              command:
                - "sh"
                - "-c"
                - >
                  gitpuller https://github.com/data-8/materials-fa17 master materials-fa;
```

This allows users to select from four profiles, each with their own
environment (defined by each Docker image in the configuration above).

The "Learning Data Science" environment in the above example overrides the postStart lifecycle hook. Note that when
using `kubespawner_override` the values must be in the format that comply with the [KubeSpawner configuration](https://jupyterhub-kubespawner.readthedocs.io/en/latest/spawner.html).
For instance, when overriding the lifecycle
hooks in `kubespawner_override`, the configuration is for `lifecycle_hooks` (snake_case) rather than `lifecycleHooks` (camelCase) which is
how it is used directly under the `singleuser` configuration section.
[A further explanation for this can be found in this github issue.](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues/1242#issuecomment-484895216)

### User-dependent profile options

It is also possible to configure the profile choices presented to the user depending on the user.
You can do this by defining a custom **pre-spawn hook** that populates the profile list based on user identity.
See [this discourse post](https://discourse.jupyter.org/t/tailoring-spawn-options-and-server-configuration-to-certain-users/8449) for some examples of how this works.

```{note}
You can also **control the HTML used for the profile selection page** by
using the Kubespawner `profile_form_template` configuration. See the
[Kubespawner configuration reference](https://jupyterhub-kubespawner.readthedocs.io/en/latest/spawner.html)
for more information.
```

(set-cmd)=

## Set command to launch

Ultimately, a single-user server should launch the `jupyterhub-singleuser` command.
However, an image may have a custom CMD that does this,
with some preparation steps, or adding additional command-line arguments,
or launching a custom wrapper command, etc.

```{note}
If you have environment preparation at startup in your image,
this is best done in the ENTRYPOINT of the image,
and not in the CMD, so that overriding the command does not skip your preparation.
```

By default, zero-to-jupyterhub will launch the command `jupyterhub-singleuser`.
If you have an image (such as `jupyter/scipy-notebook` and other Jupyter Docker stacks)
that defines a CMD with startup customization and ultimately launches `jupyterhub-singleuser`,
you can chose to launch the image's default CMD instead by setting:

```yaml
singleuser:
  cmd: null
```

Alternately, you can specify an explicit custom command as a string or list of strings:

```yaml
singleuser:
  cmd:
    - /usr/local/bin/custom-command
    - "--flag"
    - "--other-flag"
```

```{note}
Docker has `ENTRYPOINT` and `CMD`,
which k8s calls `command` and `args`.
zero-to-jupyterhub always respects the ENTRYPOINT of the image,
and setting `singleuser.cmd` only overrides the CMD.
```

## Disable specific JupyterLab extensions

Sometimes you want to temporarily disable a JupyterLab extension on a JupyterHub
by default, without having to rebuild your docker image. This can be very
easily done with [`singleuser.extraFiles`](schema_singleuser.extraFiles).
and JupyterLab's [page_config.json](https://jupyterlab.readthedocs.io/en/stable/user/directories.html#labconfig-directories)

JupyterLab's `page_config.json` lets you set page configuration by dropping JSON files
under a `labconfig` directory inside any of the directories listed when you run `jupyter --paths`.
We just use `singleuser.extraFiles` to provide this file!

```yaml
singleuser:
  extraFiles:
    lab-config:
      mountPath: /etc/jupyter/labconfig/page_config.json
      data:
        disabledExtensions:
          jupyterlab-link-share: true
```

This will disable the [link-share](https://github.com/jupyterlab-contrib/jupyterlab-link-share)
labextension, both in JupyterLab and RetroLab. You can find the name of the
extension, as well as its current status, with `jupyter labextension list`.

```
jovyan@jupyter-yuvipanda:~$ jupyter labextension list
JupyterLab v3.2.4
/opt/conda/share/jupyter/labextensions
        jupyterlab-plotly v5.4.0 enabled OK
        jupyter-matplotlib v0.9.0 enabled OK
        jupyterlab-link-share v0.2.4 disabled OK (python, jupyterlab-link-share)
        @jupyter-widgets/jupyterlab-manager v3.0.1 enabled OK (python, jupyterlab_widgets)
        @jupyter-server/resource-usage v0.6.0 enabled OK (python, jupyter-resource-usage)
        @retrolab/lab-extension v0.3.13 enabled OK
```

This is extremely helpful if the same image is being shared across hubs, and
you want some of the hubs to have some of the extensions disabled.
