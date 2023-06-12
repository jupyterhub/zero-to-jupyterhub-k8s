# Customizing User Management

This section describes management of users and their
permissions on JupyterHub.

(culling-user-pods)=

## Culling user pods

When users work with a JupyterHub deployment, will they reliably shut down their
servers manually when finished? Probably not. Due to this, it can be good to
have a system to shut down servers that are inactive after a configurable
duration of inactivity or a maximum amount of time. JupyterHub uses the
[jupyterhub-idle-culler](https://github.com/jupyterhub/jupyterhub-idle-culler)
to do this.

When a user server has been shut down, the user will have to start their server
again on next visit. The in-memory state of their previous session will have
been lost, but opened notebooks are saved regularly into a `.ipynb_checkpoints`
folder and will typically not cause work to be lost.

```{note}
For more details on how the `jupyterhub-idle-culler` works and additional
configurations you may want to set on the user servers, see the [How it works
documentation](https://github.com/jupyterhub/jupyterhub-idle-culler#how-it-works).
```

To disable culling, put the following into `config.yaml`:

```yaml
cull:
  enabled: false
```

The default culling configuration can be inspected in the Helm chart's
[values.yaml](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/HEAD/jupyterhub/values.yaml)
file under `cull`. The Helm chart's configuration corresponds to command-line
flags passed to
[jupyterhub-idle-culler](https://github.com/jupyterhub/jupyterhub-idle-culler).
Full documentation of these and additional flags can be found in
[jupyterhub-idle-culler's
documentation](https://github.com/jupyterhub/jupyterhub-idle-culler#as-a-standalone-script).

To help `jupyterhub-idle-culler` cull user servers, you should consider
configuring the user servers' _kernel manager_ to cull idle kernels that would
otherwise make the user servers report themselves as active which is part of
what `jupyterhub-idle-culler` considers. To do so, you can mount a configuration
file to the user servers via
[`singleuser.extraFiles`](schema_singleuser.extraFiles).

```yaml
singleuser:
  extraFiles:
    # jupyter_notebook_config reference: https://jupyter-notebook.readthedocs.io/en/stable/config.html
    jupyter_notebook_config.json:
      mountPath: /etc/jupyter/jupyter_notebook_config.json
      # data is a YAML structure here but will be rendered to JSON file as our
      # file extension is ".json".
      data:
        MappingKernelManager:
          # cull_idle_timeout: timeout (in seconds) after which an idle kernel is
          # considered ready to be culled
          cull_idle_timeout: 1200 # default: 0

          # cull_interval: the interval (in seconds) on which to check for idle
          # kernels exceeding the cull timeout value
          cull_interval: 120 # default: 300

          # cull_connected: whether to consider culling kernels which have one
          # or more connections
          cull_connected: true # default: false

          # cull_busy: whether to consider culling kernels which are currently
          # busy running some code
          cull_busy: false # default: false
```

```{note}
While JupyterHub automatically runs the culling process, it is not a
replacement for keeping an eye on your cluster to make sure resources
are being used as expected.
```

## Admin Users

JupyterHub has the concept of
[admin users](https://jupyterhub.readthedocs.io/en/stable/tutorial/getting-started/authenticators-users-basics.html#configure-admins-admin-users)
who have special rights. They can start / stop other user's servers, and
optionally access user's notebooks. They will see a new **Admin** button in
their Control Panel which will take them to an **Admin Panel** where they can
perform all these actions.

You can specify a list of admin users in your `config.yaml`:

```yaml
hub:
  config:
    Authenticator:
      admin_users:
        - adminuser1
        - adminuser2
```

By default, admins can access user's notebooks. If you wish to disable this, use
this in your `config.yaml`:

```yaml
hub:
  config:
    JupyterHub:
      admin_access: false
```

## Authenticating Users

For information on authenticating users in JupyterHub, see
[the Authentication guide](../../administrator/authentication.md).
