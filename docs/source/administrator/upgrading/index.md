# Upgrading your Helm chart

This page covers best-practices in upgrading your JupyterHub deployment via updates
to the Helm Chart.

```{toctree}
:maxdepth: 1
:caption: Upgrade Guide

upgrade-1-to-2
```

Upgrading from one version of the Helm Chart to the
next should be as seamless as possible, and generally shouldn't require major
changes to your deployment. Check the [CHANGELOG](changelog)
for each release to find out if there are any breaking changes in the newest version.

For additional help, feel free to reach out to us on [gitter](https://gitter.im/jupyterhub/jupyterhub)
or the [Discourse forum](https://discourse.jupyter.org/).

## Major helm-chart upgrades

These steps are **critical** before performing a major upgrade.
Z2JH follows semantic versioning, so major upgrades are indicated by an increase in the first component of the version.

1. Always backup your database!
2. Review the [CHANGELOG](changelog) and [2.0.0 upgrade guide](upgrade-1-to-2) for incompatible changes and upgrade instructions.
3. Update your configuration accordingly.
4. User servers may need be stopped prior to the upgrade,
   or restarted after it.
5. If you are planning an upgrade of a critical major installation,
   we recommend you test the upgrade out on a staging cluster first
   before applying it to production.


(helm-upgrade-command)=

## `helm upgrade` command

After modifying your `config.yaml` file according to the CHANGELOG, you will need
`<helm-release-name>` to run the upgrade commands. To find `<helm-release-name>`, run:

```
helm list --namespace <k8s-namespace>
```

Make sure to test the upgrade on a staging environment before doing the upgrade on
a production system!

To run the upgrade:

```
helm upgrade --cleanup-on-fail <helm-release-name> jupyterhub/jupyterhub --version=<chart-version> --values config.yaml --namespace <k8s-namespace>
```

For example, to upgrade to version `1.1.1` with a helm release name of `jhub` in the k8s namespace of `jhub`:

```
helm upgrade --cleanup-on-fail jhub jupyterhub/jupyterhub --version=1.1.1 --values config.yaml --namespace jhub
```

## Database

Major releases of Z2JH may include a major release of JupyterHub that requires an upgrade of the database schema.
If you are using the default database provider (SQLite), then the required db upgrades
will be performed automatically when you do a `helm upgrade`.

**Default (SQLite)**: The database upgrade will be performed automatically when you
[perform the upgrade](helm-upgrade-command)

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

4. Do a [`helm upgrade`](helm-upgrade-command). This should perform the database upgrade needed.
5. Remove the lines added in step 3, and do another [`helm upgrade`](helm-upgrade-command).

## Custom Docker Images: JupyterHub version match

If you are using a custom built image, make sure that the version of the
JupyterHub package installed in it matches the major version of JupyterHub, current 2.\*.

For example, if you are using `pip` to install JupyterHub in your custom Docker Image,
you would use:

```Dockerfile
RUN pip install --no-cache-dir jupyterhub==2.3.1
```
If you are using conda or mamba:
```Dockerfile
RUN conda install -y jupyterhub-base=2.3.1
```

Update the configuration to use this new image, which is typically done via
`singleuser.image` or as part of `singleuser.profileList`.

## JupyterHub versions installed in each Helm Chart

Each Helm Chart is packaged with a specific version of JupyterHub (and
other software as well). See the [Helm Chart repository](https://jupyterhub.github.io/helm-chart/) for
information about the versions of relevant software packages.

## Troubleshooting

If the upgrade is failing on a test system or a system that does not serve users, you can try
deleting the helm chart using:

```
helm delete <helm-release-name> --namespace <k8s-namespace>
```

`helm list --namespace <k8s-namespace>` may be used to find <helm-release-name>.
