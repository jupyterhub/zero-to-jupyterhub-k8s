(upgrade-2-to-3)=

# Major upgrade: 2.\* to 3.\*

Z2JH 3 contains some small breaking changes.
This guide will help you upgrade from 2.\* to 3.\*.

The minimum supported version of Kubernetes is 1.24.

## JupyterHub 4 and related hub components

Z2JH 3.0.0 upgrades from JupyterHub from 3 to JupyterHub 4.
There are some minor breaking changes, most notably that XSRF tokens are now used to prevent cross-origin attacks instead of checking the `Referer` header.

The database schema is updated to support new features, but this should not affect existing behaviour.
Z2JH automatically handles the upgrade if you are using sqlite (`hub.db.type = 'sqlite-pvc'`, the default), but it may not be possible to downgrade to older releases after this.
If you use an external database you need to configure [`hub.db.upgrade`](schema_hub.db.upgrade) to `true` when upgrading.

KubeSpawner is upgraded from 4 to 6.
If you set `KubeSpawner.environment` instead of `singleuser.extraEnv` the symbols `{` and `}` are now used for automatic variable expansion. To retain existing behavior, replace `{` and `}` with `{{` and `}}`.

OAuthenticator is upgraded from 15 to 16.
Previously OAuthenticator would allow any authenticated user by default in most cases.
This was changed to improve the default security configuration. to retain existing behaviour set `OAuthenticator.allow_all` to `True`.

There are major changes to how the `authenticate()` method is implemented.
If you are overriding OAuthenticator ensure you [read the changelog for 16](https://github.com/jupyterhub/oauthenticator/blob/16.0.4/docs/source/reference/changelog.md).
