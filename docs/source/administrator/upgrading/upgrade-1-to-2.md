(upgrade-1-to-2)=

# Major upgrade: 1.\* to 2.\*

Z2JH 2 contains several breaking changes, including some that affect the security of your deployment.
This guide will help you upgrade from 1.\* to 2.\*.

(upgrade-1-2-security-breaking-change)=

## Security: breaking change to `*.networkPolicy.egress`

NetworkPolicy egress rules have been extended with a new property.
If you have configured any of:

- `hub.networkPolicy.egress`
- `proxy.chp.networkPolicy.egress`
- `proxy.traefik.networkPolicy.egress`
- `singleuser.networkPolicy.egress`

you must review your configuration as additional default egress routes have been added.
Previously `*.networkPolicy.egress` controlled all egress but a new property `*.networkPolicy.egressAllowRules` add additional egress rules by default.

If you have configured `*.networkPolicy.egress` for `hub`, `proxy.chp`,
`proxy.traefik` or `singleuser` to restrict the permissions to establish
outbound network connections, then this upgrade is likely to _escalate those
permissions unless you revise your configuration_. The new configuration
`*.networkPolicy.egressAllowRules` are by default granting most of the egress
permissions previously granted by default via the `*.networkPolicy.egress`
configuration, and `*.networkPolicy.egress` are now by default not providing
any permissions.

If you for example had overridden the previously very permissive default value
of `singleuser.networkPolicy.egress` to be less permissive, you should consider
disabling all `singleuser.networkPolicy.egressAllowRules` like this
to not risk escalating the permissions.

```yaml
singleuser:
  networkPolicy:
    egressAllowRules:
      cloudMetadataServer: false
      dnsPortsPrivateIPs: false
      nonPrivateIPs: false
      privateIPs: false
```

For more details, see the documentation on [Kubernetes Network Policies](netpol)
and the configuration reference entries under
[`*.networkPolicy.egress`](schema_hub.networkPolicy.egress) and
[`*.networkPolicy.egressAllowRules`](schema_hub.networkPolicy.egressAllowRules).

## JupyterHub 2 and related hub components

Z2JH 2.0.0 upgrades from JupyterHub 1 directly to JupyterHub 3, and also upgrades all hub components.
If you are using any custom JupyterHub services, addons, API integrations, or extra configuration, you should review the breaking changes in the
major releases of JupyterHub 2 and 3 in the [JupyterHub changelog](https://jupyterhub.readthedocs.io/en/stable/changelog.html).

JupyterHub 2 and 3 updates the database schema, which means a migration takes place when you upgrade JupyterHub.
Z2JH automatically handles the upgrade if you are using sqlite (`hub.db.type = 'sqlite-pvc'`, the default), but it may not be possible to downgrade to older releases after this.
When using sqlite, JupyterHub automatically creates a backup in the `hub-db` volume,
which can be restored manually if you need to downgrade.
If you use an external database you need to configure [`hub.db.upgrade`](schema_hub.db.upgrade) to `true` when upgrading.

JupyterHub 2 adds RBAC for managing permissions in JupyterHub.
The old permissions model of admin/non-admin still works, but we recommend using [RBAC to assign only the required privileges to users or services in future](https://jupyterhub.readthedocs.io/en/stable/rbac/index.html).
Default permissions are mostly unchanged, but a few have:

- Servers' own API tokens have limited permissions by default, which can be expanded by defining the `server` role. The previous behavior was the maximum permission of `inherit`.
- `admin_access` as a concept is removed, so disabling it has no effect. In 2.0, admins by definition can do everything, including access servers. To limit user permissions, assign them to roles which have only the needed permissions.

KubeSpawner has replaced the [`kubernetes`] library with [`kubernetes_asyncio`](https://github.com/tomplus/kubernetes_asyncio).
If you have extended the JupyterHub image and you rely on the kubernetes library you will need to modify your extensions.

See
[Notable dependencies updated](notable-dependencies-200)
for more information on other upgraded hub components.

## JupyterLab and Jupyter Server

The default singleuser server is [JupyterLab](https://jupyterlab.readthedocs.io/), running on [Jupyter server](https://jupyter-server.readthedocs.io/en/latest/).
To switch back to Jupyter Notebook either configure/rebuild your singleuser image to default to notebook, or see [the documentation on user interfaces](user-interfaces)

## KubeSpawner prevents privilege escalation such as sudo by default

By default processes cannot escalate their privileges.
For example, a user cannot use sudo to switch to root.
If you have configured sudo or some other privilege escalation method inside your singleuser image you must set `singleuser.allowPrivilegeEscalation: true`.

```yaml
singleuser:
  allowPrivilegeEscalation: true
```

If you want to add custom arguments to the command, you must specify the full command and any arguments in `singleuser.cmd`, for example:

```yaml
singleuser:
  cmd:
    - jupyterhub-singleuser
    - "--collaborative"
    - "--debug"
```

## Configuration in `jupyterhub_config.d` has a higher priority than `hub.config` [#2457](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/2457)

Previously if `hub.config` was used to configure some JupyterHub traitlets it would override any custom configuration files mounted into `jupyterhub_config.d` in the hub container.
In 2.0.0 all extra customisations (e.g. using `hub.extraConfig` to provide in-line configuration, or `hub.extraFiles` to mount files into `jupyterhub_config.d`) will always take precedence over any Helm chart values.

## User scheduler plugin configuration has changed to match `kubescheduler.config.k8s.io/v1beta3` [#2590](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/2590)

Advanced customisation of the user scheduler using plugins now requires Kubernetes 1.21+, and the configuration must follow `kubescheduler.config.k8s.io/v1beta3`.
Customisation is no longer possible with Kubernetes 1.20.

If you are using the user scheduler without custom plugin configuration you are not affected.

## Kubernetes version 1.20+ is required [#2635](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/2635)

This Helm chart uses Kubernetes resources that are not available in Kubernetes versions prior to 1.20.

## `hub.fsGid` is replaced by `hub.podSecurityContext` [#2720](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/2720)

In previous versions of Z2JH `hub.fsGid` set a supplemental group ID, which is required on some K8s systems to ensure JupyterHub has permissions to read/write files on a volume.
This has been replaced by the more general [`hub.podSecurityContext`](schema_hub.podSecurityContext).
To upgrade set:

```yaml
hub:
  podSecurityContext:
    fsGroup: GROUP-ID
```

## Hub image is based on Debian instead of Ubuntu [#2733](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/2733)

The hub container base image has switched from `ubuntu:20.04` to `python:3.9-slim-bullseye` which is based on `debian:bullseye-slim`.
If you have extended the Z2JH hub image please review the [hub Dockerfile](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/2.0.0/images/hub/Dockerfile).
Note the singleuser image is not affected.

## Disabling RBAC requires setting multiple properties, `rbac.enable` is removed [#2736](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/2736) [#2739](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/2739)

If you previously disabled RBAC using `rbac.enable: False` you should set

```yaml
rbac:
  create: False
hub:
  serviceAccount:
    create: false
proxy:
  traefik:
    serviceAccount:
      create: false
scheduling:
  userScheduler:
    serviceAccount:
      create: false
prePuller:
  hook:
    serviceAccount:
      create: false
```

When you have updated your configuration follow the rest of the [upgrade guide](upgrading-major-upgrades).
