(upgrade-3-to-4)=

# Major upgrade: 3.\* to 4.\*

zero-to-jupyterhub 4.0 is a major upgrade that may require some changes to your configuration,
depending on what features you may use.
This mostly comes in the form of some upgraded packages, described below.

:::{seealso}

- the [general upgrade documentation](upgrading-major-upgrades) for upgrade steps to take every time you do a major chart update
- the [changelog](changelog-4.0) for details of upgraded packages

:::

## JupyterHub 5

zero-to-jupyterhub 4.0 upgrades the JupyterHub version from 4.1.6 to 5.2.1.

:::{seealso}

For more detailed changes in JupyterHub, see JupyterHub's own documentation on upgrading to version 5:

Especially if you use features like per-user subdomains or custom page templates.

- [jupyterhub changelog](https://jupyterhub.readthedocs.io/en/5.2.1/reference/changelog.html)
- [Upgrading to JupyterHub 5](https://jupyterhub.readthedocs.io/en/5.2.1/howto/upgrading-v5.html)

:::

### Allowing users

JupyterHub 5 promotes the `allow_all` and `allow_existing_users` configuration used on OAuthenticator to all other Authenticators.
If you have not explicitly allowed users, the default is to allow no users (this was already the default if you were using OAuth).
If you are using an Authenticator where all users who can successfully authenticate should have access, set:

```yaml
hub:
  config:
    Authenticator:
      allow_all: true
```

to explicitly opt in to this behavior that was previously the default for some authenticators.

## KubeSpawner 7

zero-to-jupyterhub 4.0 upgrades the KubeSpawner version from 6 to 7.
The main relevant change here is the "slug scheme" used to compute names of resources such as pods and PVC (user storage) is changed.

The new scheme is called "safe" and is the default, whereas the old scheme is called "escape".
If you do not have any custom templated fields, it is _unlikely_ that anything should change for you and everything should work.
If, however, you specify custom templated fields such as volume mounts or environment variables,
especially those that have the `{username}` or `{servername}` fields,
those values are likely to change under the new scheme for some usernames.
In particular, there are new fields that should make things easier:

- `{user_server}` combines the username and server name, and is equivalent to `{username}{servername}` in the old escape scheme.
  It is the recommended value when a string should be unique per named server, as opposed to per user.
- `{pod_name}`, `{pvc_name}` are now available to reference the fully resolved names of these objects
  and can be used to avoid duplicating templates.

You can opt in globally to keep the kubespawner 6 behavior with:

```yaml
hub:
  config:
    KubeSpawner:
      slug_scheme: escape
```

which _should_ result in no changes for you from previous behavior.

One user-facing place where a default template may require administrator action is if you are using:

```yaml
singleuser:
  storage:
    type: static
```

The default value for `subPath` is `{username}` which may resolve to a different value for some usernames, which could appear like a 'lost' home directory because the mount path changes.
The data is not lost, but the mount location has changed.
To ensure this value doesn't change, you can use:

```yaml
singleuser:
  storage:
    type: static
    static:
      subPath: "{escaped_username}"
```

which applies the previous 'escape' scheme to the subPath.
Alternatively, you can keep the new scheme, and perform a one-time migration to move files for the affected usernames.

:::{seealso}

- [KubeSpawner changelog](https://jupyterhub-kubespawner.readthedocs.io/en/latest/changelog.html)
- [KubeSpawner docs on templated fields](https://jupyterhub-kubespawner.readthedocs.io/en/latest/templates.html#fields)

:::
