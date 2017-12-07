# User Management

This section describes management of users and their
permissions on JupyterHub.

## Admin Users

JupyterHub has the concept of
[admin users](http://jupyterhub.readthedocs.io/en/latest/getting-started/authenticators-users-basics.html#configure-admins-admin-users)
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
