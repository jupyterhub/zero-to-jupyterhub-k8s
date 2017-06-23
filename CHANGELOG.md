# Changelog

Releases are now named after famous [Cricket](https://en.wikipedia.org/wiki/Cricket) players.

## v0.4 "Akram": Stability, HTTPS & breaking changes

Released 2017-06-23

This version has a bunch of breaking changes. If you are upgrading from an older 
version that is using any of the features that changed (you probably are!) and 
do not know much about Kubernetes, we recommend just deleting and recreating your
installation!

If you need support, reach out to us on
[gitter](https://gitter.im/jupyterhub/jupyterhub) or open an
[issue](https://github.com/jupyterhub/helm-chart/issues).

### Breaking changes ###

* Names of user pods and dynamically created home directory PVCs no longer include
  the userid in them by default. If you are using dynamic PVCs for home directories
  (which is the default), you will need to manually rename them before upgrading.
  Otherwise, new PVCs will be created, and users might freak out about their home
  directories appearing empty. 
  
  See [this pull request](https://github.com/jupyterhub/kubespawner/pull/56) on
  what needs to change! 

* A [StorageClass](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#storageclasses)
  is no longer created by default. This shouldn't affect most new installs,
  since as of Kubernetes 1.6 most cloud provider installations have a default.
  If you are using an older version of kubernetes, easiest thing to do is upgrade
  to a newer version. If not, you can create a StorageClass manually and everything
  should continue to work.
  
* Setting `token.proxy` no longer works - set `proxy.secretToken` instead.
  If your `config.yaml` contains something that looks like the following:
  
  ```yaml
  token:
      proxy: <some-secret>
  ```
  
  you can / should change that to:
  
  ```yaml
  proxy:
      secretToken: <some-secret>
  ```


### Features ###

* GitHub Authentication is now supported, thanks to [Jason Kuruzovich](https://github.com/jkuruzovich).
* Using an [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) is
  now supported! If your cluster already has Ingress support (with automatic Let's Encrypt support, perhaps),
  you can easily use that now.
* We now add a label to user pods / PVCs with their usernames.
* Support using a static PVC for user homes or for the hub db. This makes this release usable
  with clusters where you only have one NFS share that must be used for the whole hub.
* PostgreSQL is now a supported hub database backend provider.
 
### Other Changes ###

* We now use the official [CHP](http://github.com/jupyterhub/configurable-http-proxy)
  as the proxy, rather than the unofficial [nchp](https://github.com/yuvipanda/jupyterhub-nginx-chp).
  This should be a no-op for the most part. JupyterHub errors might display a
  nicer error page.
* The version of KubeSpawner uses the official kubernetes 
  [python client](https://github.com/kubernetes-incubator/client-python/) rather than
  [pycurl](http://pycurl.io/). This helps with scalability a little.
* The deprecated `createNamespace` parameter no longer works, alongside the
  deprecated `name` parameter. You probably weren't using these anyway - they
  were kept only for backwards compatibility with very early versions.

### Contributors ###

This release made possible by the awesome work of the following contributors (in alphabetical order):

* [Analect](https://github.com/analect)
* [Carol Willing](https://github.com/willingc)
* [Jason Kuruzovich](https://github.com/jkuruzovich)
* [Min RK](https://github.com/minrk/)
* [Yuvi Panda](https://github.com/yuvipanda/)

<3
