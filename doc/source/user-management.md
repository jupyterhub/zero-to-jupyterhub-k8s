# User Management

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


## User Whitelist

JupyterHub can be configured to only allow a specified
[whitelist](http://jupyterhub.readthedocs.io/en/latest/getting-started/authenticators-users-basics.html#create-a-whitelist-of-users) 
of users authenticated by the Authenticator to login, rather than everyone
authenticated by the chosen authenticator. This is especially useful if you are
using an authenticator that uses an authentication service open to the general
public, such as GitHub or Google

You can specify this list of usernames in your `config.yaml`:

```yaml
auth:
  whitelist:
    users:
      - user1
      - user2
```
