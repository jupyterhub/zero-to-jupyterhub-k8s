# Upgrading The helm chart

## General upgrade advice

In general, it should be safe to upgrade a minor revision of the chart to
receive bugfixes and improvements. A major chart upgrade (e.g. v0.4 to v0.5)
can be more challenging, but is possible. We still recommend a full fresh
installation if you can, but recognize it is not possible all the time. We've
provided and tested the following upgrade instructions. If you are planning an
upgrade of a critical major installation, we recommend you test it out on a
staging cluster first before applying it to production. Feel free to reach out
to us on [gitter](http://gitter.im/jupyterhub/jupyterhub) or the [mailing
list](https://groups.google.com/forum/#!forum/jupyter) for upgrade help!

General helm-chart upgrade considerations:

1. Always backup your database!
2. Review incompatible changes for your upgrade (most should be on this page)
   and update your configuration accordingly.
3. For major upgrades, user servers may need be stopped prior to the upgrade,
   or restarted after it.

## v0.4 to v0.5

Release 0.5 contains a major JupyterHub version bump (from 0.7.2 to 0.8).
Since it is a major upgrade of JupyterHub that changes how authentication is
implemented, user servers must be stopped during the upgrade.
The database schema has also changed, so a database upgrade must be performed.

### Database upgrade

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


### [Role based access control](http://zero-to-jupyterhub.readthedocs.io/en/latest/security.html#role-based-access-control-rbac)

[RBAC](https://kubernetes.io/docs/admin/authorization/rbac/) is the user security model
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
JupyterHub package installed in it is now 0.8. It needs to be version 0.7.2 for
it to work with v0.4 of the helm chart, and needs to be 0.8 for it to work with
v0.5 of the helm chart.

For example, if you are using pip to install JupyterHub in your custom Docker Image,
you would use:

```Dockerfile
RUN pip install --no-cache-dir jupyterhub==0.8.*
```

### Ingress config incompatibilities

We've made HTTPS [much easier to set up](http://zero-to-jupyterhub.readthedocs.io/en/latest/extending-jupyterhub.html#setting-up-https),
with automated certificates from [Let's Encrypt](https://letsencrypt.org/).
However, this means that some of the keys used to set up your own ingress has
changed.

If you were using config under `ingress` purely to get HTTPS, we recommend
that you delete your entire config section under `ingress` & instead follow
the new [docs](http://zero-to-jupyterhub.readthedocs.io/en/latest/extending-jupyterhub.html#setting-up-https)
on getting HTTPS set up. It's much easier & a lot less error prone than the method recommended on 0.4.

If you were using config under `ingress` for other reasons, you may continue
to do so. The keys under `ingress` have changed, and are now much more in line
with how many other projects use `ingress` in the [official charts repo](https://github.com/kubernetes/charts/).
See [our ingress documentation](http://zero-to-jupyterhub.readthedocs.io/en/latest/advanced.html#ingress)
for more details on how to set up ingress properly. This is the most likely issue if
you are getting an error like the following when upgrading:

```
Ingress.extensions "jupyterhub" is invalid: spec: Invalid value: []extensions.IngressRule(nil): either `backend` or `rules` must be specified
```

### Admin config incompatibility

If you had used the `admin` config section before, you now need to move it under
`auth`. So if you had config like:

```yaml
admin:
   access: true
   users:
    - yuvipanda
```

it should now be:

```yaml
auth:
  admin:
    access: true
    users:
      - yuvipanda
```

### Upgrade command

After modifying your config.yaml file to match, you can run the actual upgrade with
the following helm command:

```
helm upgrade <YOUR-RELEASE-NAME> jupyterhub/jupyterhub --version=v0.5 -f config.yaml
```

This should perform the upgrade! If you have forgotten your release name, you can find
out with `helm list`. Make sure to test the upgrade on a staging environment
before doing the upgrade!
