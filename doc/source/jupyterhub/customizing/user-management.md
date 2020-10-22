# Customizing User Management

This section describes management of users and their
permissions on JupyterHub.

## Culling user pods
JupyterHub will automatically delete any user pods that have no activity
for a period of time. This helps free up computational resources and keeps
costs down if you are using an autoscaling cluster.
When these users navigate back to your JupyterHub, they will
have to start their server again, and the state of their previous session
(variables they've created, any in-memory data, etc)
will be lost. This is known as *culling*.

```{note}
In JupyterHub, "inactivity" is defined as no response from the user's
browser. JupyterHub constantly pings the user's JupyterHub browser session
to check whether it is open. This means that leaving the computer running
with the JupyterHub window open will **not** be treated as inactivity.
```

To disable culling, put the following into `config.yaml`:

```yaml
cull:
  enabled: false
```

By default, JupyterHub will run the culling process every ten minutes
and will cull any user pods that have been inactive for more than one hour.
You can configure this behavior in your ``config.yaml`` file with the following
fields:

```yaml
cull:
  timeout: <max-idle-seconds-before-user-pod-is-deleted>
  every: <number-of-seconds-this-check-is-done>
```

```{note}
While JupyterHub automatically runs the culling process, it is not a
replacement for keeping an eye on your cluster to make sure resources
are being used as expected.
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
[the Authentication guide](../administrator/authentication).
