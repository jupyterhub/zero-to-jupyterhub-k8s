# Upgrading your Helm chart

This page covers best-practices in upgrading your JupyterHub deployment via updates
to the Helm Chart.

Upgrading from one version of the Helm Chart to the
next should be as seamless as possible, and generally shouldn't require major
changes to your deployment. Check the [CHANGELOG](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/master/CHANGELOG.md)
for each release to find out if there are any breaking changes in the newest version.

For additional help, feel free to reach out to us on [gitter](https://gitter.im/jupyterhub/jupyterhub)
or the [mailing list](https://groups.google.com/forum/#!forum/jupyter)!

## Major helm-chart upgrades

These steps are **critical** before performing a major upgrade.

1. Always backup your database!
2. Review the [CHANGELOG](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/master/CHANGELOG.md) for incompatible changes and upgrade instructions.
3. Update your configuration accordingly.
4. User servers may need be stopped prior to the upgrade,
   or restarted after it.
5. If you are planning an upgrade of a critical major installation,
   we recommend you test the upgrade out on a staging cluster first
   before applying it to production.

### v0.5 to v0.6

See the [CHANGELOG](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/master/CHANGELOG.md#06---ellyse-perry---2017-01-29).

### v0.4 to v0.5

Release 0.5 contains a major JupyterHub version bump (from 0.7.2 to 0.8).
Since it is a major upgrade of JupyterHub that changes how authentication is
implemented, user servers must be stopped during the upgrade.
The database schema has also changed, so a database upgrade must be performed.

See the [documentation for v0.5 for the upgrade process](https://zero-to-jupyterhub.readthedocs.io/en/v0.5-doc/upgrading.html)
as well as the [CHANGELOG](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/master/CHANGELOG.md#05---hamid-hassan---2017-12-05)
for this release for more information about changes.

## Subtopics

This section covers upgrade information specific to the following:

- `helm upgrade` command
- Databases
- RBAC (Role Based Access Control)
- Custom Docker images

### `helm upgrade` command

After modifying your `config.yaml` file according to the CHANGELOG, you will need
`<YOUR-HELM-RELEASE-NAME>` to run the upgrade commands. To find `<YOUR-RELEASE-NAME>`, run:

```
helm list
```

Make sure to test the upgrade on a staging environment before doing the upgrade on
a production system!

To run the upgrade:

```
helm upgrade --cleanup-on-fail <YOUR-HELM-RELEASE-NAME> jupyterhub/jupyterhub --version=<RELEASE-VERSION> -f config.yaml
```

For example, to upgrade to v0.6, enter and substituting `<YOUR-HELM-RELEASE-NAME>` and version v0.6:

```
helm upgrade --cleanup-on-fail <YOUR-HELM-RELEASE-NAME> jupyterhub/jupyterhub --version=v0.6 -f config.yaml
```

### Database

This release contains a major JupyterHub version bump (from 0.7.2 to 0.8). If
you are using the default database provider (SQLite), then the required db upgrades
will be performed automatically when you do a `helm upgrade`.

**Default (SQLite)**: The database upgrade will be performed automatically when you
[perform the upgrade](#upgrade-command)

**MySQL / PostgreSQL**: You will execute the following steps, which includes a manual update of your database:

1. Make a full backup of your database, just in case things go bad.
2. Make sure that the database user used by JupyterHub to connect to your database
   can perform schema migrations like adding new tables, altering tables, etc.
3. In your `config.yaml`, add the following config:

   ```yaml
   hub:
     db:
       upgrade: true
   ```
4. Do a [`helm upgrade`](#upgrade-command). This should perform the database upgrade needed.
5. Remove the lines added in step 3, and do another [`helm upgrade`](#upgrade-command).


### [Role based access control](/security.html#use-role-based-access-control-rbac)

[RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) is the user security model
in Kubernetes that gives applications only as much access they need to the kubernetes
API and not more. Prior to this, applications were all running with the equivalent
of root on your Kubernetes cluster. This release adds appropriate roles for the
various components of JupyterHub, for much better ability to secure clusters.

RBAC is turned on by default. But, if your cluster is older than 1.8, or you have RBAC
enforcement turned off, you might want to explicitly disable it. You can do so by adding
the following snippet to your `config.yaml`:

```yaml
rbac:
  enabled: false
```

This is especially true if you get an error like:

```
Error: the server rejected our request for an unknown reason (get clusterrolebindings.rbac.authorization.k8s.io)
```

when doing the upgrade!

### Custom Docker Images: JupyterHub version match

If you are using a custom built image, make sure that the version of the
JupyterHub package installed in it is now 0.8.1. It needs to be 0.8.1 for it to work with
v0.6 of the helm chart.

For example, if you are using `pip` to install JupyterHub in your custom Docker Image,
you would use:

```Dockerfile
RUN pip install --no-cache-dir jupyterhub==0.8.1
```

## JupyterHub versions installed in each Helm Chart

Each Helm Chart is packaged with a specific version of JupyterHub (and
other software as well). See the [Helm Chart repository](https://github.com/jupyterhub/helm-chart#release-notes>) for
information about the versions of relevant software packages.

## Troubleshooting

If the upgrade is failing on a test system or a system that does not serve users, you can try
deleting the helm chart using:

```
helm delete <YOUR-HELM-RELEASE-NAME>
```

`helm list` may be used to find <YOUR-HELM-RELEASE-NAME>.
