(upgrade-3-to-4)=

# Major upgrade: 3.\* to 4.\*

zero-to-jupyterhub 4.0 is a major upgrade that may require some changes to your configuration,
depending on what features you may use.
This mostly comes in the form of some upgraded packages, described below.

See the [changelog](changelog) for details of upgraded packages.

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
If you have no explicitly allowed users, the default is now to allow no users (this was already the default if you were using OAuth).
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

- `{user_server}` combines the username and server name, and is equivalent to `{username}{servername}` in the old escape scheme
- `{pod_name}`, `{pvc_name}`

You can opt in to the kubespawner 6 behavior with:

```yaml
hub:
  config:
    KubeSpawner:
      slug_scheme: escape
```

which _should_ result in no changes for you from previous behavior.

:::{seealso}

- [KubeSpawner changelog](https://jupyterhub-kubespawner.readthedocs.io/en/latest/changelog.html)
- [KubeSpawner docs on templated fields](https://jupyterhub-kubespawner.readthedocs.io/en/latest/templates.html#fields)

:::

## OAuthenticator 17

OAuthenticator is upgraded from 16.3.1 to 17.1.
The main changes are related to using group information from OAuth providers.
If you used or would like to use groups for authentication,
check out the [OAuthenticator changelog](https://oauthenticator.readthedocs.io/en/stable/reference/changelog.html)

## Other package upgrades

- Python is upgraded from 3.11 to 3.12 in the Hub image
- LDAPAuthenticator is upgraded from 1 to 2 ([changelog](https://github.com/jupyterhub/ldapauthenticator/blob/2.0.0/CHANGELOG.md#200---2024-10-18))
- FirstUseAuthenticator is upgraded from 1.0 to 1.1 ([changelog](https://github.com/jupyterhub/firstuseauthenticator/blob/1.1.0/CHANGELOG.md))
- idle culler is upgraded from 1.3.1 to 1.4.0 ([changelog](https://github.com/jupyterhub/jupyterhub-idle-culler/blob/1.4.0/CHANGELOG.md))
