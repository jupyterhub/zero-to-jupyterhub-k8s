# Customizing User Management

This section describes management of users and their
permissions on JupyterHub.

(culling-user-pods)=

## Culling user pods

JupyterHub uses the [jupyterhub-idle-culler](github.com/jupyterhub/jupyterhub-idle-culler) to automatically delete any user pods that have no activity
for a period of time. This helps free up computational resources and keeps
costs down if you are using an autoscaling cluster.
When these users navigate back to your JupyterHub, they will
have to start their server again, and the state of their previous session
(variables they've created, any in-memory data, etc)
will be lost. This is known as _culling_.

```{note}
In JupyterHub, "inactivity" is defined as no response from the user's
browser. JupyterHub constantly pings the user's JupyterHub browser session via the JupyterHub API
to check whether it is open. This means that leaving the computer running
with the JupyterHub window open will **not** be treated as inactivity. However, leaving a process or notebook running and closing the web socket (by closing the browser) **will** be treated as inactivity.
```

To disable `jupyterhub-idle-culler`, put the following into `config.yaml`:

```yaml
cull:
  enabled: false
```

By default, JupyterHub will run the culling process every ten minutes
and will cull any user pods that have been inactive for more than one hour.
You can configure this behavior in your `config.yaml` file with the following
fields:

```yaml
cull:
  timeout: <max-idle-seconds-before-user-pod-is-deleted>
  every: <number-of-seconds-this-check-is-done>
```

The above options correspond to flags in the [jupyterhub-idle-culler](github.com/jupyterhub/jupyterhub-idle-culler) package. Full documentation of these and additional flags can be found in the [jupyterhub-idle-culler docs](github.com/jupyterhub/jupyterhub-idle-culler#as-a-standalone-script).

```{note}
While JupyterHub automatically runs the culling process, it is not a
replacement for keeping an eye on your cluster to make sure resources
are being used as expected.
```

```{note}
There is a separate culling service for Jupyter Notebook that provides more fine-grained control over culling behavior for individual notebooks. That culling behavior has not yet been extended to Jupyter Lab [see here](https://github.com/jupyterlab/jupyterlab/issues/6893). However, when running processes in Classic Notebook, these settings, if passed to user pods, can control culling on active processes regardless of web socket connection. See the [Jupyter Notebook Docs](https://jupyter-notebook.readthedocs.io/en/stable/config.html#options) for more info, specifically options: `MappingKernelManager.cull_idle_timeout`, `MappingKernelManager.cull_interval`, `MappingKernelManager.cull_connected`, and `NotebookApp.shutdown_no_activity_timeout`.
```

## Admin Users

JupyterHub has the concept of
[admin users](https://jupyterhub.readthedocs.io/en/latest/getting-started/authenticators-users-basics.html#configure-admins-admin-users)
who have special rights. They can start / stop other user's servers, and
optionally access user's notebooks. They will see a new **Admin** button in
their Control Panel which will take them to an **Admin Panel** where they can
perform all these actions.

You can specify a list of admin users in your `config.yaml`:

```yaml
auth:
  admin:
    users:
      - adminuser1
      - adminuser2
```

By default, admins can access user's notebooks. If you wish to disable this, use
this in your `config.yaml`:

```yaml
auth:
  admin:
    access: false
```

## Authenticating Users

For information on authenticating users in JupyterHub, see
[the Authentication guide](../../administrator/authentication).
