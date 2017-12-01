# Changelog

## [Unreleased]

## Releases

Releases are now named after famous [Cricket](https://en.wikipedia.org/wiki/Cricket) players.

## [0.5] - [TBD] - 2017-11-??
/
JupyterHub 0.8, HTTPS & scalability.

### Upgrading from 0.4

#### Database upgrade

This release contains a major JupyterHub version bump (from 0.7.2 to 0.8). If
you are using the default database provider (SQLite), then the required db upgrades
will be performed automatically when you do a `helm upgrade`.

If you are using MySQL / PostgreSQL as your backing database, you must perform a
manual database upgrade before the helm upgrade.

1. Make a full backup of your database, just in case things go bad.
2. Make sure that the database user used by JupyterHub to connect to your database
   can perform schema migrations like adding new tables, altering tables, etc.
3. In your `config.yaml`, add the following config:

   ```yaml
   hub:
     db:
       upgrade: true
   ```
4. Do a `helm upgrade`. This should perform the database upgrade needed.
5. Remove the lines added in step 3, and do another `helm upgrade`.

It is highly recommended that you have a `staging` environment that matches
your production environment & can be used as a testbed for this upgrade. Feel
free to reach out to us on [gitter](https://gitter.im/jupyterhub/jupyterhub) before
your upgrade if you have any questions!

#### Ingress config incompatibilities

We've made HTTPS [much easier to set up](http://zero-to-jupyterhub.readthedocs.io/en/latest/extending-jupyterhub.html#setting-up-https), with automated certificates from
[Let's Encrypt](https://letsencrypt.org/). However, this means
that some of the keys used to set up your own ingress has changed.

If you were using config under `ingress` purely to get HTTPS, we recommend
that you delete your entire config section under `ingress` & instead follow
the new [docs](http://zero-to-jupyterhub.readthedocs.io/en/latest/extending-jupyterhub.html#setting-up-https)
on getting HTTPS set up. It's much easier & a lot less error prone than the method recommended on 0.4.

If you were using config under `ingress` for other reasons, you may continue
to do so. The keys under `ingress` have changed, and are now much more in line
with how many other projects use `ingress` in the [official charts repo](https://github.com/kubernetes/charts/).

#### Custom Docker Images: JupyterHub version match

If you are using a custom built image, make sure that the version of the
JupyterHub package installed in it is now 0.8. It needs to be version 0.7.2 for
it to work with v0.4 of the helm chart, and needs to be 0.8 for it to work with
v0.5 of the helm chart.

For example, if you are using pip to install JupyterHub in your custom Docker Image,
you would use:

```Dockerfile
RUN pip install --no-cache-dir jupyterhub==0.8.*
```

#### Admin config incompatibility

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

### New Features

#### JupyterHub 0.8

JupyterHub 0.8 is full of new features - see [CHANGELOG](https://github.com/jupyterhub/jupyterhub/blob/master/docs/source/changelog.md#080-2017-10-03)
for more details. Specific features made to benefit this chart are:

1. No more 'too many redirects' errors at scale.
2. Lots of performance improvements, we now know we can handle up to 4k active users
3. Concurrent spawn limits (set via `hub.concurrentSpawnLimit`) can be used to limit the concurrent
   number of users who can try to launch on the hub at any given time. This can be
   tuned to avoid crashes when hundreds of users try to launch at the same time. It gives
   them a friendly error message + asks them to try later, rather than spinning forever.
4. Active Server limit (set via `hub.activeServerLimit`) can be used to limit the
   total number of active users that can be using the hub at any given time. This allows
   admins to control the size of their clusters.
5. Memory limits & guarantees (set via `singleuser.memory`) can now contain fractional
   units. So you can say `0.5G` instead of having to use `512M`.

And lots more!

#### Much easier HTTPS

It is our responsibility as software authors to make it very easy for admins to set up
HTTPS for their users. v0.5 makes this much easier than v0.4. You can find the new
instructions [here](http://zero-to-jupyterhub.readthedocs.io/en/latest/extending-jupyterhub.html#setting-up-https) and
they are much simpler!

You can also now use your own HTTPS certificates & keys rather than using Let's Encrypt.

#### More authenticators supported

The following new authentication providers have been added:

1. GitLab
2. CILogon
3. Globus

You can also set up a whitelist of users by adding to the list in `auth.whitelist.users`.

#### Role based access control

[RBAC](https://kubernetes.io/docs/admin/authorization/rbac/) is the user security model
in Kubernetes that gives applications only as much access they need to the kubernetes
API and not more. Prior to this, applications were all running with the equivalent
of root on your Kubernetes cluster. This release adds appropriate roles for the
various components of JupyterHub, for much better ability to secure clusters.

#### Easier customization of `jupyterhub_config.py`

You can always put extra snippets of `jupyterhub_config.py` configuration in
`hub.extraConfig`. Now you can also add extra environment variables to the hub
in `hub.extraEnv` and extra configmap items via `hub.extraConfigMap`. ConfigMap
items can be arbitrary YAML, and you can read them via the `get_config` function in
your `hub.extraConfig`. This makes it cleaner to customize the hub's config in
ways that's not yet possible with config.yaml.

#### Hub Services support

You can also add [external JupyterHub Services](http://jupyterhub.readthedocs.io/en/latest/reference/services.html)
by adding them to `hub.services`. Note that you are still responsible for actually
running the service somewhere (perhaps as a deployment object).

#### More customization options for user server environments

More options have been added under `singleuser` to help you customize the environment
that the user is spawned in. You can change the uid / gid of the user with `singleuser.uid`
and `singleuser.fsGid`, mount extra volumes with `singleuser.storage.extraVolumes` &
`singleuser.storage.extraVolumeMounts` and provide extra environment variables with
`singleuser.extraEnv`.

## [0.4] - [Akram](#akram) - 2017-06-23

Stability, HTTPS & breaking changes.

### Installation and upgrades

We **recommend** that you delete prior versions of the package and install the
latest version. If you are very familiar with Kubernetes, you can upgrade from
an older version, but we still suggest deleting and recreating your
installation.

### Breaking changes

* The **name of a user pod** and a **dynamically created home directory [PVC (PersistentVolumeClaim)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)** no longer include
  the `userid` in them by default. If you are using dynamic PVCs for `home`
  directories (which is the default), you will need to *manually rename* these
  directories before upgrading.
  Otherwise, new PVCs will be created, and users might freak out when viewing the newly created directory and think that their home directory appears empty.

  See [PR #56](https://github.com/jupyterhub/kubespawner/pull/56) on
  what needs to change.

* A **[StorageClass](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#storageclasses)**
  is no longer created by default. This shouldn't affect most new installs,
  since most cloud provider installations have a default (as of Kubernetes 1.6).
  If you are using an older version of Kubernetes, the easiest thing to do is to
  upgrade to a newer version. If not, you can create a StorageClass manually
  and everything should continue to work.

* `token.proxy` is removed. Use **`proxy.secretToken`** instead.
  If your `config.yaml` contains something that looks like the following:

  ```yaml
  token:
      proxy: <some-secret>
  ```

  you should change that to:

  ```yaml
  proxy:
      secretToken: <some-secret>
  ```

### Added

* Added **GitHub Authentication support**, thanks to [Jason Kuruzovich](https://github.com/jkuruzovich).
* Added **[Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) support**!
  If your cluster already has Ingress support (with automatic Let's Encrypt support, perhaps),
  you can easily use that now.
* We now add a **label** to user pods / PVCs with their usernames.
* Support using a **static PVC** for user `home` directories or for the hub database. This makes this release usable
  with clusters where you only have one NFS share that must be used for the whole hub.
* **PostgreSQL** is now a supported hub database backend provider.
* You can set annotations & labels on the **proxy-public service** now.

### Changed

* We now use the official [configurable http proxy](http://github.com/jupyterhub/configurable-http-proxy)
  (CHP) as the proxy, rather than the unofficial
  [nchp](https://github.com/yuvipanda/jupyterhub-nginx-chp). This should be a
  no-op (or require no changes) for the most part. JupyterHub errors might
  display a nicer error page.
* The version of KubeSpawner uses the official Kubernetes
  [python client](https://github.com/kubernetes-incubator/client-python/) rather
  than [pycurl](http://pycurl.io/). This helps with scalability a little.

### Removed

* The deprecated `createNamespace` parameter no longer works, alongside the
  deprecated `name` parameter. You probably weren't using these anyway - they
  were kept only for backwards compatibility with very early versions.

### Contributors

This release made possible by the awesome work of the following contributors
(in alphabetical order):

* [Analect](https://github.com/analect)
* [Carol Willing](https://github.com/willingc)
* [Jason Kuruzovich](https://github.com/jkuruzovich)
* [Min RK](https://github.com/minrk/)
* [Yuvi Panda](https://github.com/yuvipanda/)

<3

### Akram

[Wasim Akram](https://en.wikipedia.org/wiki/Wasim_Akram) (وسیم اکرم) is considered by many to be
the greatest pace bowler of all time and a founder of the fine art of
[reverse swing bowling](https://en.wikipedia.org/wiki/Swing_bowling#Reverse_swing).

## 0.3

### [0.3.1] - 2017-05-19

KubeSpawner updates. [Release note](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/releases/tag/v0.3.1)

### [0.3] - 2017-05-15

Deployer UX fixes. [Release note](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/releases/tag/v0.3)

## [0.2] - 2017-05-01

Minor cleanups and features. [Release note](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/releases/tag/v0.2)

## [0.1] - 2017-04-10

Initial Public Release. [Release note](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/releases/tag/v0.1)

## Support

If you need support, reach out to us on
[gitter](https://gitter.im/jupyterhub/jupyterhub) or open an
[issue](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues).


[Unreleased]: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/compare/v0.4...HEAD
[0.4]: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/compare/v0.3...v0.3.1
[0.3]: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/compare/v0.2...v0.3
[0.2]: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/compare/v0.1...v0.2
[0.1]: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/releases/tag/v0.1
