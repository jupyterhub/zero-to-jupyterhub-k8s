(helm-chart-configuration-reference)=
# Configuration Reference

The [JupyterHub Helm
chart](https://github.com/jupyterhub/zero-to-jupyterhub-k8s) is configurable by
values in your `config.yaml`. In this way, you can extend user resources, build off
of different Docker images, manage security and authentication, and more.

Below is a description of many *but not all* of the configurable values for the
Helm chart. To see *all* configurable options, inspect their default values
defined [here](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/master/jupyterhub/values.yaml).

For more guided information about some specific things you can do with
modifications to the helm chart, see the {ref}`customization-guide`.
(schema:hub)=
## hub

(schema:hub.cookieSecret)=
### hub.cookieSecret

A 32-byte cryptographically secure randomly generated string used to sign values of
secure cookies set by the hub. If unset, jupyterhub will generate one on startup and
save it in the file `jupyterhub_cookie_secret` in the `/srv/jupyterhub` directory of
the hub container. A value set here will make JupyterHub overwrite any previous file.

You do not need to set this at all if you are using the default configuration for
storing databases - sqlite on a persistent volume (with `hub.db.type` set to the
default `sqlite-pvc`). If you are using an external database, then you must set this
value explicitly - or your users will keep getting logged out each time the hub pod
restarts.

Changing this value will all user logins to be invalidated. If this secret leaks,
*immediately* change it to something else, or user data can be compromised

```sh
# to generate a value, run
openssl rand -hex 32
```


(schema:hub.imagePullPolicy)=
### hub.imagePullPolicy

Set the imagePullPolicy on the hub pod.

See the [Kubernetes docs](https://kubernetes.io/docs/concepts/containers/images/#updating-images)
for more info on what the values mean.


(schema:hub.imagePullSecret)=
### hub.imagePullSecret

Creates an image pull secret for you and makes the hub pod utilize
it, allowing it to pull images from private image registries.

Using this configuration option automates the following steps that
normally is required to pull from private image registries.

```sh
# you won't need to run this manually...
kubectl create secret docker-registry hub-image-credentials \
  --docker-server=<REGISTRY> \
  --docker-username=<USERNAME> \
  --docker-email=<EMAIL> \
  --docker-password=<PASSWORD>
```

```yaml
# you won't need to specify this manually...
spec:
  imagePullSecrets:
    - name: hub-image-credentials
```

To learn the username and password fields to access a gcr.io registry
from a Kubernetes cluster not associated with the same google cloud
credentials, look into [this
guide](http://docs.heptio.com/content/private-registries/pr-gcr.html)
and read the notes about the password.


(schema:hub.imagePullSecret.enabled)=
#### hub.imagePullSecret.enabled

Enable the creation of a Kubernetes Secret containing credentials
to access a image registry. By enabling this, the hub pod will also be configured
to use these credentials when it pulls its container image.


(schema:hub.imagePullSecret.registry)=
#### hub.imagePullSecret.registry

Name of the private registry you want to create a credential set
for. It will default to Docker Hub's image registry.

Examples:
  - https://index.docker.io/v1/
  - quay.io
  - eu.gcr.io
  - alexmorreale.privatereg.net


(schema:hub.imagePullSecret.username)=
#### hub.imagePullSecret.username

Name of the user you want to use to connect to your private
registry. For external gcr.io, you will use the `_json_key`.

Examples:
  - alexmorreale
  - alex@pfc.com
  - _json_key


(schema:hub.imagePullSecret.password)=
#### hub.imagePullSecret.password

Password of the user you want to use to connect to your private
registry.

Examples:
  - plaintextpassword
  - abc123SECRETzyx098

For gcr.io registries the password will be a big JSON blob for a
Google cloud service account, it should look something like below.
              
```yaml
password: |-
  {
    "type": "service_account",
    "project_id": "jupyter-se",
    "private_key_id": "f2ba09118a8d3123b3321bd9a7d6d0d9dc6fdb85",
    ...
  }
```

Learn more in [this
guide](http://docs.heptio.com/content/private-registries/pr-gcr.html).


(schema:hub.image)=
### hub.image

Set custom image name / tag for the hub pod.

Use this to customize which hub image is used. Note that you must use a version of
the hub image that was bundled with this particular version of the helm-chart - using
other images might not work.


(schema:hub.image.name)=
#### hub.image.name

Name of the image, without the tag.

```
# example names
yuvipanda/wikimedia-hub
gcr.io/my-project/my-hub
```


(schema:hub.image.tag)=
#### hub.image.tag

The tag of the image to pull.

This is the value after the `:` in your full image name.

```
# example tags
v1.11.1
zhy270a
```


(schema:hub.image.pullSecrets)=
#### hub.image.pullSecrets

Use an existing kubernetes secret to pull the custom image.

```yaml
# example existing pull secret.
singleuser:
  image:
    pullSecrets:
      - gcr-pull
```


(schema:hub.db)=
### hub.db

(schema:hub.db.type)=
#### hub.db.type

Type of database backend to use for the hub database.

The Hub requires a persistent database to function, and this lets you specify
where it should be stored.

The various options are:

1. **sqlite-pvc**

   Use an `sqlite` database kept on a persistent volume attached to the hub.

   By default, this disk is created by the cloud provider using
   *dynamic provisioning* configured by a [storage
   class](https://kubernetes.io/docs/concepts/storage/storage-classes/).
   You can customize how this disk is created / attached by
   setting various properties under `hub.db.pvc`.

   This is the default setting, and should work well for most cloud provider
   deployments.

2. **sqlite-memory**

   Use an in-memory `sqlite` database. This should only be used for testing,
   since the database is erased whenever the hub pod restarts - causing the hub
   to lose all memory of users who had logged in before.

   When using this for testing, make sure you delete all other objects that the
   hub has created (such as user pods, user PVCs, etc) every time the hub restarts.
   Otherwise you might run into errors about duplicate resources.

3. **mysql**

   Use an externally hosted mysql database.

   You have to specify an sqlalchemy connection string for the mysql database you
   want to connect to in `hub.db.url` if using this option.

   The general format of the connection string is:
   ```
   mysql+pymysql://<db-username>:<db-password>@<db-hostname>:<db-port>/<db-name>
   ```

   The user specified in the connection string must have the rights to create
   tables in the database specified.

   Note that if you use this, you *must* also set `hub.cookieSecret`.

4. **postgres**

   Use an externally hosted postgres database.

   You have to specify an sqlalchemy connection string for the postgres database you
   want to connect to in `hub.db.url` if using this option.

   The general format of the connection string is:
   ```
   postgres+psycopg2://<db-username>:<db-password>@<db-hostname>:<db-port>/<db-name>
   ```

   The user specified in the connection string must have the rights to create
   tables in the database specified.

   Note that if you use this, you *must* also set `hub.cookieSecret`.


(schema:hub.db.pvc)=
#### hub.db.pvc

Customize the Persistent Volume Claim used when `hub.db.type` is `sqlite-pvc`.


(schema:hub.db.pvc.annotations)=
##### hub.db.pvc.annotations

Annotations to apply to the PVC containing the sqlite database.

See [the Kubernetes
documentation](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/)
for more details about annotations.


(schema:hub.db.pvc.selector)=
##### hub.db.pvc.selector

Label selectors to set for the PVC containing the sqlite database.

Useful when you are using a specific PV, and want to bind to
that and only that.

See [the Kubernetes
documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)
for more details about using a label selector for what PV to
bind to.


(schema:hub.db.pvc.storage)=
##### hub.db.pvc.storage

Size of disk to request for the database disk.


(schema:hub.db.url)=
#### hub.db.url

Connection string when `hub.db.type` is mysql or postgres.

See documentation for `hub.db.type` for more details on the format of this property.


(schema:hub.db.password)=
#### hub.db.password

Password for the database when `hub.db.type` is mysql or postgres.


(schema:hub.labels)=
### hub.labels

Extra labels to add to the hub pod.

See the [Kubernetes docs](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)
to learn more about labels.


(schema:hub.initContainers)=
### hub.initContainers

list of initContainers to be run with hub pod. See [Kubernetes Docs](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/)

```yaml
hub:
  initContainers:
    - name: init-myservice
      image: busybox:1.28
      command: ['sh', '-c', 'command1']
    - name: init-mydb
      image: busybox:1.28
      command: ['sh', '-c', 'command2']
```


(schema:hub.extraEnv)=
### hub.extraEnv

Extra environment variables that should be set for the hub pod.

Environment variables are usually used to:
  - Pass parameters to some custom code in `hub.extraConfig`.
  - Configure code running in the hub pod, such as an authenticator or
    spawner.

String literals with `$(ENV_VAR_NAME)` will be expanded by Kubelet which
is a part of Kubernetes.

```yaml
hub:
  extraEnv:
    # basic notation (for literal values only)
    MY_ENV_VARS_NAME1: "my env var value 1"

    # explicit notation (the "name" field takes precedence)
    HUB_NAMESPACE:
      name: HUB_NAMESPACE
      valueFrom:
        fieldRef:
          fieldPath: metadata.namespace

    # implicit notation (the "name" field is implied)
    PREFIXED_HUB_NAMESPACE:
      value: "my-prefix-$(HUB_NAMESPACE)"
    SECRET_VALUE:
      valueFrom:
        secretKeyRef:
          name: my-k8s-secret
          key: password
```

For more information, see the [Kubernetes EnvVar
specification](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/#envvar-v1-core).


(schema:hub.extraConfig)=
### hub.extraConfig

Arbitrary extra python based configuration that should be in `jupyterhub_config.py`.

This is the *escape hatch* - if you want to configure JupyterHub to do something specific
that is not present here as an option, you can write the raw Python to do it here.

extraConfig is a *dict*, so there can be multiple configuration snippets
under different names.
The configuration sections are run in alphabetical order.

Non-exhaustive examples of things you can do here:
  - Subclass authenticator / spawner to do a custom thing
  - Dynamically launch different images for different sets of images
  - Inject an auth token from GitHub authenticator into user pod
  - Anything else you can think of!

Since this is usually a multi-line string, you want to format it using YAML's
[| operator](https://yaml.org/spec/1.2/spec.html#id2795688).

For example:
  ```yaml
  hub:
    extraConfig:
      myConfig.py: |
        c.JupyterHub.something = 'something'
        c.Spawner.somethingelse = 'something else'
  ```

No validation of this python is performed! If you make a mistake here, it will probably
manifest as either the hub pod going into `Error` or `CrashLoopBackoff` states, or in
some special cases, the hub running but... just doing very random things. Be careful!


(schema:hub.uid)=
### hub.uid

The UID the hub process should be running as.
Use this only if you are building your own image & know that a user with this uid exists inside the hub container! Advanced feature, handle with care!
Defaults to 1000, which is the uid of the `jovyan` user that is present in the default hub image.

(schema:hub.fsGid)=
### hub.fsGid

The gid the hub process should be using when touching any volumes mounted.
Use this only if you are building your own image & know that a group with this gid exists inside the hub container! Advanced feature, handle with care!
Defaults to 1000, which is the gid of the `jovyan` user that is present in the default hub image.

(schema:hub.service)=
### hub.service

Object to configure the service the JupyterHub will be exposed on by the Kubernetes server.


(schema:hub.service.type)=
#### hub.service.type

The Kubernetes ServiceType to be used.

The default type is `ClusterIP`.
See the [Kubernetes docs](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types)
to learn more about service types.


(schema:hub.service.ports)=
#### hub.service.ports

Object to configure the ports the hub service will be deployed on.


(schema:hub.service.ports.nodePort)=
##### hub.service.ports.nodePort

The nodePort to deploy the hub service on.


(schema:hub.service.annotations)=
#### hub.service.annotations

Kubernetes annotations to apply to the hub service.


(schema:hub.pdb)=
### hub.pdb

Set the Pod Disruption Budget for the hub pod.

See [the Kubernetes
documentation](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/)
for more details about disruptions.


(schema:hub.pdb.enabled)=
#### hub.pdb.enabled

Whether PodDisruptionBudget is enabled for the hub pod.


(schema:hub.pdb.minAvailable)=
#### hub.pdb.minAvailable

Minimum number of pods to be available during the voluntary disruptions.


(schema:hub.existingSecret)=
### hub.existingSecret

Name of the existing secret in the kubernetes cluster, typically the `hub-secret`.

This secret should represent the structure as otherwise generated by this chart:
  ```yaml
  apiVersion: v1
  data:
    proxy.token: < FILL IN >
    values.yaml: < FILL IN >
  kind: Secret
  metadata:
    name: hub-secret
  ```

NOTE: if you choose to manage the secret yourself, you are in charge of ensuring the
secret having the proper contents.


(schema:proxy)=
## proxy

(schema:proxy.chp)=
### proxy.chp

Configure the configurable-http-proxy (chp) pod managed by jupyterhub to route traffic
both to itself and to user pods.


(schema:proxy.chp.extraEnv)=
#### proxy.chp.extraEnv

Extra environment variables that should be set for the chp pod.

Environment variables are usually used here to:
  - override HUB_SERVICE_PORT or HUB_SERVICE_HOST default values
  - set CONFIGPROXY_SSL_KEY_PASSPHRASE for setting passphrase of SSL keys

String literals with `$(ENV_VAR_NAME)` will be expanded by Kubelet which
is a part of Kubernetes.

```yaml
proxy:
  chp:
    extraEnv:
      # basic notation (for literal values only)
      MY_ENV_VARS_NAME1: "my env var value 1"

      # explicit notation (the "name" field takes precedence)
      CHP_NAMESPACE:
        name: CHP_NAMESPACE
        valueFrom:
          fieldRef:
            fieldPath: metadata.namespace

      # implicit notation (the "name" field is implied)
      PREFIXED_CHP_NAMESPACE:
        value: "my-prefix-$(CHP_NAMESPACE)"
      SECRET_VALUE:
        valueFrom:
          secretKeyRef:
            name: my-k8s-secret
            key: password
```

For more information, see the [Kubernetes EnvVar
specification](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/#envvar-v1-core).


(schema:proxy.secretToken)=
### proxy.secretToken

A 32-byte cryptographically secure randomly generated string used to secure communications
between the hub and the configurable-http-proxy.

```sh
# to generate a value, run
openssl rand -hex 32
```

Changing this value will cause the proxy and hub pods to restart. It is good security
practice to rotate these values over time. If this secret leaks, *immediately* change
it to something else, or user data can be compromised


(schema:proxy.service)=
### proxy.service

Object to configure the service the JupyterHub's proxy will be exposed on by the Kubernetes server.


(schema:proxy.service.type)=
#### proxy.service.type

Default `LoadBalancer`. See `hub.service.type` for supported values.


(schema:proxy.service.labels)=
#### proxy.service.labels

Extra labels to add to the proxy service.

See the [Kubernetes docs](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)
to learn more about labels.


(schema:proxy.service.annotations)=
#### proxy.service.annotations

Annotations to apply to the service that is exposing the proxy.

See [the Kubernetes
documentation](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/)
for more details about annotations.


(schema:proxy.service.nodePorts)=
#### proxy.service.nodePorts

Object to set NodePorts to expose the service on for http and https.

See [the Kubernetes
documentation](https://kubernetes.io/docs/concepts/services-networking/service/#nodeport)
for more details about NodePorts.


(schema:proxy.service.nodePorts.http)=
##### proxy.service.nodePorts.http

The HTTP port the proxy-public service should be exposed on.


(schema:proxy.service.nodePorts.https)=
##### proxy.service.nodePorts.https

The HTTPS port the proxy-public service should be exposed on.


(schema:proxy.service.loadBalancerIP)=
#### proxy.service.loadBalancerIP

The public IP address the proxy-public Kubernetes service should
be exposed on. This entry will end up at the configurable proxy
server that JupyterHub manages, which will direct traffic to user
pods at the `/user` path and the hub pod at the `/hub` path.

Set this if you want to use a fixed external IP address instead of
a dynamically acquired one. This is relevant if you have a domain
name that you want to point to a specific IP and want to ensure it
doesn't change.


(schema:proxy.service.loadBalancerSourceRanges)=
#### proxy.service.loadBalancerSourceRanges

A list of IP CIDR ranges that are allowed to access the load balancer service.
Defaults to allowing everyone to access it.


(schema:proxy.https)=
### proxy.https

Object for customizing the settings for HTTPS used by the JupyterHub's proxy.
For more information on configuring HTTPS for your JupyterHub, see the [HTTPS section in our security guide](/administrator/security.html#https)


(schema:proxy.https.enabled)=
#### proxy.https.enabled

Indicator to set whether HTTPS should be enabled or not on the proxy. Defaults to `true` if the https object is provided.


(schema:proxy.https.type)=
#### proxy.https.type

The type of HTTPS encryption that is used.
Decides on which ports and network policies are used for communication via HTTPS. Setting this to `secret` sets the type to manual HTTPS with a secret that has to be provided in the `https.secret` object.
Defaults to `letsencrypt`.


(schema:proxy.https.letsencrypt)=
#### proxy.https.letsencrypt

(schema:proxy.https.letsencrypt.contactEmail)=
##### proxy.https.letsencrypt.contactEmail

The contact email to be used for automatically provisioned HTTPS certificates by Let's Encrypt. For more information see [Set up automatic HTTPS](/administrator/security.html#set-up-automatic-https).
Required for automatic HTTPS.


(schema:proxy.https.manual)=
#### proxy.https.manual

Object for providing own certificates for manual HTTPS configuration. To be provided when setting `https.type` to `manual`.
See [Set up manual HTTPS](/administrator/security.html#set-up-manual-https)


(schema:proxy.https.manual.key)=
##### proxy.https.manual.key

The RSA private key to be used for HTTPS.
To be provided in the form of

```
key: |
  -----BEGIN RSA PRIVATE KEY-----
  ...
  -----END RSA PRIVATE KEY-----
```


(schema:proxy.https.manual.cert)=
##### proxy.https.manual.cert

The certificate to be used for HTTPS.
To be provided in the form of

```
cert: |
  -----BEGIN CERTIFICATE-----
  ...
  -----END CERTIFICATE-----
```


(schema:proxy.https.secret)=
#### proxy.https.secret

Secret to be provided when setting `https.type` to `secret`.


(schema:proxy.https.secret.name)=
##### proxy.https.secret.name

Name of the secret


(schema:proxy.https.secret.key)=
##### proxy.https.secret.key

Path to the private key to be used for HTTPS.
Example: `'tls.key'`


(schema:proxy.https.secret.crt)=
##### proxy.https.secret.crt

Path to the certificate to be used for HTTPS.
Example: `'tls.crt'`


(schema:proxy.https.hosts)=
#### proxy.https.hosts

You domain in list form.
Required for automatic HTTPS. See [Set up automatic HTTPS](/administrator/security.html#set-up-automatic-https).
To be provided like:
```
hosts:
  - <your-domain-name>
```   


(schema:proxy.pdb)=
### proxy.pdb

Set the Pod Disruption Budget for the proxy pod.

See [the Kubernetes
documentation](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/)
for more details about disruptions.


(schema:proxy.pdb.enabled)=
#### proxy.pdb.enabled

Whether PodDisruptionBudget is enabled for the proxy pod.


(schema:proxy.pdb.minAvailable)=
#### proxy.pdb.minAvailable

Minimum number of pods to be available during the voluntary disruptions.


(schema:proxy.traefik)=
### proxy.traefik

Configure the traefik proxy used to terminate TLS when 'autohttps' is enabled


(schema:proxy.traefik.extraEnv)=
#### proxy.traefik.extraEnv

Extra environment variables that should be set for the traefik pod.

Environment Variables here may be used to configure traefik.

String literals with `$(ENV_VAR_NAME)` will be expanded by Kubelet which
is a part of Kubernetes.

```yaml
proxy:
  traefik:
    extraEnv:
      # basic notation (for literal values only)
      MY_ENV_VARS_NAME1: "my env var value 1"

      # explicit notation (the "name" field takes precedence)
      TRAEFIK_NAMESPACE:
        name: TRAEFIK_NAMESPACE
        valueFrom:
          fieldRef:
            fieldPath: metadata.namespace

      # implicit notation (the "name" field is implied)
      PREFIXED_TRAEFIK_NAMESPACE:
        value: "my-prefix-$(TRAEFIK_NAMESPACE)"
      SECRET_VALUE:
        valueFrom:
          secretKeyRef:
            name: my-k8s-secret
            key: password
```

For more information, see the [Kubernetes EnvVar
specification](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/#envvar-v1-core).


(schema:auth)=
## auth

(schema:auth.state)=
### auth.state

(schema:auth.state.enabled)=
#### auth.state.enabled

Enable persisting auth_state (if available).
See: [the documentation on authenticators](http://jupyterhub.readthedocs.io/en/latest/api/auth.html)


(schema:auth.state.cryptoKey)=
#### auth.state.cryptoKey

auth_state will be encrypted and stored in the Hub’s database. This can include things like authentication tokens, etc. to be passed to Spawners as environment variables.
Encrypting auth_state requires the cryptography package.
It must contain one (or more, separated by ;) 32-byte encryption keys. These can be either base64 or hex-encoded.
The JUPYTERHUB_CRYPT_KEY environment variable for the hub pod is set using this entry.

```sh
# to generate a value, run
openssl rand -hex 32
```

If encryption is unavailable, auth_state cannot be persisted.


(schema:singleuser)=
## singleuser

Options for customizing the environment that is provided to the users after they log in.


(schema:singleuser.podNameTemplate)=
### singleuser.podNameTemplate

Template for the pod name of each user, such as `jupyter-{username}{servername}`.


(schema:singleuser.cpu)=
### singleuser.cpu

Set CPU limits & guarantees that are enforced for each user.
See: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/


(schema:singleuser.cpu.limit)=
#### singleuser.cpu.limit

(schema:singleuser.cpu.guarantee)=
#### singleuser.cpu.guarantee

(schema:singleuser.memory)=
### singleuser.memory

Set Memory limits & guarantees that are enforced for each user.

See the [Kubernetes docs](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
for more info.


(schema:singleuser.memory.limit)=
#### singleuser.memory.limit

(schema:singleuser.memory.guarantee)=
#### singleuser.memory.guarantee

Note that this field is referred to as *requests* by the Kubernetes API.


(schema:singleuser.imagePullSecret)=
### singleuser.imagePullSecret

Creates an image pull secret for you and makes the user pods utilize
it, allowing them to pull images from private image registries.

Using this configuration option automates the following steps that
normally is required to pull from private image registries.

```sh
# you won't need to run this manually...
kubectl create secret docker-registry singleuser-image-credentials \
  --docker-server=<REGISTRY> \
  --docker-username=<USERNAME> \
  --docker-email=<EMAIL> \
  --docker-password=<PASSWORD>
```

```yaml
# you won't need to specify this manually...
spec:
  imagePullSecrets:
    - name: singleuser-image-credentials
```

To learn the username and password fields to access a gcr.io registry
from a Kubernetes cluster not associated with the same google cloud
credentials, look into [this
guide](http://docs.heptio.com/content/private-registries/pr-gcr.html)
and read the notes about the password.


(schema:singleuser.imagePullSecret.enabled)=
#### singleuser.imagePullSecret.enabled

Enable the creation of a Kubernetes Secret containing credentials
to access a image registry. By enabling this, user pods and image
puller pods will also be configured to use these credentials when
they pull their container images.


(schema:singleuser.imagePullSecret.registry)=
#### singleuser.imagePullSecret.registry

Name of the private registry you want to create a credential set
for. It will default to Docker Hub's image registry.

Examples:
  - https://index.docker.io/v1/
  - quay.io
  - eu.gcr.io
  - alexmorreale.privatereg.net


(schema:singleuser.imagePullSecret.username)=
#### singleuser.imagePullSecret.username

Name of the user you want to use to connect to your private
registry. For external gcr.io, you will use the `_json_key`.

Examples:
  - alexmorreale
  - alex@pfc.com
  - _json_key


(schema:singleuser.imagePullSecret.password)=
#### singleuser.imagePullSecret.password

Password of the user you want to use to connect to your private
registry.

Examples:
  - plaintextpassword
  - abc123SECRETzyx098

For gcr.io registries the password will be a big JSON blob for a
Google cloud service account, it should look something like below.
              
```yaml
password: |-
  {
    "type": "service_account",
    "project_id": "jupyter-se",
    "private_key_id": "f2ba09118a8d3123b3321bd9a7d6d0d9dc6fdb85",
    ...
  }
```

Learn more in [this
guide](http://docs.heptio.com/content/private-registries/pr-gcr.html).


(schema:singleuser.image)=
### singleuser.image

Set custom image name / tag used for spawned users.

This image is used to launch the pod for each user.


(schema:singleuser.image.name)=
#### singleuser.image.name

Name of the image, without the tag.

Examples:
  - yuvipanda/wikimedia-hub-user
  - gcr.io/my-project/my-user-image


(schema:singleuser.image.tag)=
#### singleuser.image.tag

The tag of the image to use.

This is the value after the `:` in your full image name.


(schema:singleuser.image.pullPolicy)=
#### singleuser.image.pullPolicy

Set the imagePullPolicy on the singleuser pods that are spun up by the hub.

See the [Kubernetes docs](https://kubernetes.io/docs/concepts/containers/images/#updating-images)
for more info.


(schema:singleuser.image.pullSecrets)=
#### singleuser.image.pullSecrets

Use an existing kubernetes secret to pull the custom image.

```yaml
# example existing pull secret
singleuser:
  image:
    pullSecrets:
      - gcr-pull
```


(schema:singleuser.initContainers)=
### singleuser.initContainers

list of initContainers to be run every singleuser pod. See [Kubernetes Docs](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/)

```yaml
singleuser:
  initContainers:
    - name: init-myservice
      image: busybox:1.28
      command: ['sh', '-c', 'command1']
    - name: init-mydb
      image: busybox:1.28
      command: ['sh', '-c', 'command2']
```


(schema:singleuser.profileList)=
### singleuser.profileList

For more information about the profile list, see [KubeSpawner's
documentation](https://jupyterhub-kubespawner.readthedocs.io/en/latest/spawner.html#kubespawner.KubeSpawner)
as this is simply a passthrough to that configuration.

**NOTE**: The image-pullers are aware of the overrides of images in
`singleuser.profileList` but they won't be if you configure it in
JupyterHub's configuration of '`c.KubeSpawner.profile_list`.

```yaml
singleuser:
  profileList:
    - display_name: "Default: Shared, 8 CPU cores"
      description: "Your code will run on a shared machine with CPU only."
      default: True
    - display_name: "Personal, 4 CPU cores & 26GB RAM, 1 NVIDIA Tesla K80 GPU"
      description: "Your code will run a personal machine with a GPU."
      kubespawner_override:
        extra_resource_limits:
          nvidia.com/gpu: "1"
```


(schema:singleuser.schedulerStrategy)=
### singleuser.schedulerStrategy

Deprecated and no longer does anything. Use the user-scheduler instead
in order to accomplish a good packing of the user pods.


(schema:singleuser.extraEnv)=
### singleuser.extraEnv

Extra environment variables that should be set for the user pods.

String literals with `$(ENV_VAR_NAME)` will be expanded by Kubelet which
is a part of Kubernetes. Note that the user pods will already have
access to a set of environment variables that you can use, like
`JUPYTERHUB_USER` and `JUPYTERHUB_HOST`. For more information about these
inspect [this source
code](https://github.com/jupyterhub/jupyterhub/blob/cc8e7806530466dce8968567d1bbd2b39a7afa26/jupyterhub/spawner.py#L763).

```yaml
singleuser:
  extraEnv:
    # basic notation (for literal values only)
    MY_ENV_VARS_NAME1: "my env var value 1"

    # explicit notation (the "name" field takes precedence)
    USER_NAMESPACE:
      name: USER_NAMESPACE
      valueFrom:
        fieldRef:
          fieldPath: metadata.namespace

    # implicit notation (the "name" field is implied)
    PREFIXED_USER_NAMESPACE:
      value: "my-prefix-$(USER_NAMESPACE)"
    SECRET_VALUE:
      valueFrom:
        secretKeyRef:
          name: my-k8s-secret
          key: password
```

For more information, see the [Kubernetes EnvVar
specification](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/#envvar-v1-core).


(schema:singleuser.extraTolerations)=
### singleuser.extraTolerations

Tolerations allow a pod to be scheduled on nodes with taints. These
are additional tolerations other than the user pods and core pods
default ones `hub.jupyter.org/dedicated=user:NoSchedule` or
`hub.jupyter.org/dedicated=core:NoSchedule`. Note that a duplicate set
of tolerations exist where `/` is replaced with `_` as the Google
cloud does not support the character `/` yet in the toleration.

See the [Kubernetes docs](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)
for more info.

Pass this field an array of
[`Toleration`](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/#toleration-v1-core)
objects.


(schema:singleuser.extraNodeAffinity)=
### singleuser.extraNodeAffinity

Affinities describe where pods prefer or require to be scheduled, they
may prefer or require a node where they are to be scheduled to have a
certain label (node affinity). They may also require to be scheduled
in proximity or with a lack of proximity to another pod (pod affinity
and anti pod affinity).

See the [Kubernetes
docs](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)
for more info.


(schema:singleuser.extraNodeAffinity.required)=
#### singleuser.extraNodeAffinity.required

Pass this field an array of
[`NodeSelectorTerm`](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/#nodeselectorterm-v1-core)
objects.


(schema:singleuser.extraNodeAffinity.preferred)=
#### singleuser.extraNodeAffinity.preferred

Pass this field an array of
[`PreferredSchedulingTerm`](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/#preferredschedulingterm-v1-core)
objects.


(schema:singleuser.extraPodAffinity)=
### singleuser.extraPodAffinity

See the description of `singleuser.extraNodeAffinity`.


(schema:singleuser.extraPodAffinity.required)=
#### singleuser.extraPodAffinity.required

Pass this field an array of
[`PodAffinityTerm`](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/#podaffinityterm-v1-core)
objects.


(schema:singleuser.extraPodAffinity.preferred)=
#### singleuser.extraPodAffinity.preferred

Pass this field an array of
[`WeightedPodAffinityTerm`](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/#weightedpodaffinityterm-v1-core)
objects.


(schema:singleuser.extraPodAntiAffinity)=
### singleuser.extraPodAntiAffinity

See the description of `singleuser.extraNodeAffinity`.


(schema:singleuser.extraPodAntiAffinity.required)=
#### singleuser.extraPodAntiAffinity.required

Pass this field an array of
[`PodAffinityTerm`](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/#podaffinityterm-v1-core)
objects.


(schema:singleuser.extraPodAntiAffinity.preferred)=
#### singleuser.extraPodAntiAffinity.preferred

Pass this field an array of
[`WeightedPodAffinityTerm`](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/#weightedpodaffinityterm-v1-core)
objects.


(schema:scheduling)=
## scheduling

Objects for customizing the scheduling of various pods on the nodes and
related labels.


(schema:scheduling.userScheduler)=
### scheduling.userScheduler

The user scheduler is making sure that user pods are scheduled
tight on nodes, this is useful for autoscaling of user node pools.


(schema:scheduling.userScheduler.enabled)=
#### scheduling.userScheduler.enabled

Enables the user scheduler.


(schema:scheduling.userScheduler.replicas)=
#### scheduling.userScheduler.replicas

You can have multiple schedulers to share the workload or improve
availability on node failure.


(schema:scheduling.userScheduler.image)=
#### scheduling.userScheduler.image

The image containing the [kube-scheduler
binary](https://console.cloud.google.com/gcr/images/google-containers/GLOBAL/kube-scheduler-amd64).


(schema:scheduling.userScheduler.image.name)=
##### scheduling.userScheduler.image.name

(schema:scheduling.userScheduler.image.tag)=
##### scheduling.userScheduler.image.tag

(schema:scheduling.userScheduler.pdb)=
#### scheduling.userScheduler.pdb

Set the Pod Disruption Budget for the user scheduler.

See [the Kubernetes
documentation](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/)
for more details about disruptions.


(schema:scheduling.userScheduler.pdb.enabled)=
##### scheduling.userScheduler.pdb.enabled

Whether PodDisruptionBudget is enabled for the user scheduler.


(schema:scheduling.userScheduler.pdb.minAvailable)=
##### scheduling.userScheduler.pdb.minAvailable

Minimum number of pods to be available during the voluntary disruptions.


(schema:scheduling.podPriority)=
### scheduling.podPriority

Pod Priority is used to allow real users evict placeholder pods that
in turn triggers a scale up by a cluster autoscaler. So, enabling this
option will only make sense if the following conditions are met:

1. Your Kubernetes cluster has at least version 1.11
2. A cluster autoscaler is installed
3. user-placeholer pods is configured to get a priority equal or
   higher than the cluster autoscaler's priority cutoff
4. Normal user pods have a higher priority than the user-placeholder
   pods

Note that if the default priority cutoff if not configured on cluster
autoscaler, it will currently default to 0, and that in the future
this is meant to be lowered. If your cloud provider is installing the
cluster autoscaler for you, they may also configure this specifically.

Recommended settings for a cluster autoscaler...

... with a priority cutoff of -10 (GKE):

```yaml
podPriority:
  enabled: true
  globalDefault: false
  defaultPriority: 0
  userPlaceholderPriority: -10
```

... with a priority cutoff of 0:

```yaml
podPriority:
  enabled: true
  globalDefault: true
  defaultPriority: 10
  userPlaceholderPriority: 0
```


(schema:scheduling.podPriority.enabled)=
#### scheduling.podPriority.enabled

(schema:scheduling.podPriority.globalDefault)=
#### scheduling.podPriority.globalDefault

Warning! This will influence all pods in the cluster.

The priority a pod usually get is 0. But this can be overridden
with a PriorityClass resource if it is declared to be the global
default. This configuration option allows for the creation of such
global default.


(schema:scheduling.podPriority.defaultPriority)=
#### scheduling.podPriority.defaultPriority

The actual value for the default pod priority.


(schema:scheduling.podPriority.userPlaceholderPriority)=
#### scheduling.podPriority.userPlaceholderPriority

The actual value for the user-placeholder pods' priority.


(schema:scheduling.userPlaceholder)=
### scheduling.userPlaceholder

User placeholders simulate users but will thanks to PodPriority be
evicted by the cluster autoscaler if a real user shows up. In this way
placeholders allow you to create a headroom for the real users and
reduce the risk of a user having to wait for a node to be added. Be
sure to use the the continuous image puller as well along with
placeholders, so the images are also available when real users arrive.

To test your setup efficiently, you can adjust the amount of user
placeholders with the following command:
```sh
# Configure to have 3 user placeholders
kubectl scale sts/user-placeholder --replicas=3
```


(schema:scheduling.userPlaceholder.enabled)=
#### scheduling.userPlaceholder.enabled

(schema:scheduling.userPlaceholder.replicas)=
#### scheduling.userPlaceholder.replicas

How many placeholder pods would you like to have?


(schema:scheduling.userPlaceholder.resources)=
#### scheduling.userPlaceholder.resources

Unless specified here, the placeholder pods will request the same
resources specified for the real singleuser pods.


(schema:scheduling.corePods)=
### scheduling.corePods

These settings influence the core pods like the hub, proxy and
user-scheduler pods.


(schema:scheduling.corePods.nodeAffinity)=
#### scheduling.corePods.nodeAffinity

Where should pods be scheduled? Perhaps on nodes with a certain
label is preferred or even required?


(schema:scheduling.corePods.nodeAffinity.matchNodePurpose)=
##### scheduling.corePods.nodeAffinity.matchNodePurpose

Decide if core pods *ignore*, *prefer* or *require* to
schedule on nodes with this label:
```
hub.jupyter.org/node-purpose=core
```


(schema:scheduling.userPods)=
### scheduling.userPods

These settings influence the user pods like the user-placeholder,
user-dummy and actual user pods named like jupyter-someusername.


(schema:scheduling.userPods.nodeAffinity)=
#### scheduling.userPods.nodeAffinity

Where should pods be scheduled? Perhaps on nodes with a certain
label is preferred or even required?


(schema:scheduling.userPods.nodeAffinity.matchNodePurpose)=
##### scheduling.userPods.nodeAffinity.matchNodePurpose

Decide if user pods *ignore*, *prefer* or *require* to
schedule on nodes with this label:
```
hub.jupyter.org/node-purpose=user
```


(schema:ingress)=
## ingress

(schema:ingress.enabled)=
### ingress.enabled

Enable the creation of a Kubernetes Ingress to proxy-public service.

See [Advanced Topics — Zero to JupyterHub with Kubernetes
0.7.0 documentation](/administrator/advanced.html#ingress)
for more details.


(schema:ingress.annotations)=
### ingress.annotations

Annotations to apply to the Ingress.

See [the Kubernetes
documentation](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/)
for more details about annotations.


(schema:ingress.hosts)=
### ingress.hosts

List of hosts to route requests to the proxy.


(schema:ingress.pathSuffix)=
### ingress.pathSuffix

Suffix added to Ingress's routing path pattern.

Specify `*` if your ingress matches path by glob pattern.


(schema:ingress.tls)=
### ingress.tls

TLS configurations for Ingress.

See [the Kubernetes
documentation](https://kubernetes.io/docs/concepts/services-networking/ingress/#tls)
for more details about annotations.


(schema:prePuller)=
## prePuller

(schema:prePuller.annotations)=
### prePuller.annotations

Annotations to apply to the hook and continous image puller pods. One example use case is to
disable istio sidecars which could interfere with the image pulling.


(schema:prePuller.resources)=
### prePuller.resources

These are standard Kubernetes resources with requests and limits for
cpu and memory. They will be used on the containers in the pods
pulling images. These should be set extremely low as the containers
shut down directly or is a pause container that just idles.

They were made configurable as usage of ResourceQuota may require
containers in the namespace to have explicit resources set.


(schema:prePuller.hook)=
### prePuller.hook

See the [*optimization
section*](/administrator/optimization.html#pulling-images-before-users-arrive)
for more details.


(schema:prePuller.hook.enabled)=
#### prePuller.hook.enabled

(schema:prePuller.hook.podSchedulingWaitDuration)=
#### prePuller.hook.podSchedulingWaitDuration

The `hook-image-awaiter` has a criteria to await all the
`hook-image-puller` DaemonSet's pods to both schedule and finish
their image pulling. This flag can be used to relax this criteria
to instead only await the pods that _has already scheduled_ to
finish image pulling after a certain duration.

The value of this is that sometimes the newly created
`hook-image-puller` pods cannot be scheduled because nodes are
full, and then it probably won't make sense to block a `helm
upgrade`.

An infinite duration to wait for pods to schedule can be
represented by `-1`. This was the default behavior of version
0.9.0 and earlier.


(schema:prePuller.continuous)=
### prePuller.continuous

See the [*optimization
section*](/administrator/optimization.html#pulling-images-before-users-arrive)
for more details.

**NOTE**: If used with a Cluster Autoscaler (an autoscaling node
pool), also add user-placeholders and enable pod priority.


(schema:prePuller.continuous.enabled)=
#### prePuller.continuous.enabled

(schema:prePuller.pullProfileListImages)=
### prePuller.pullProfileListImages

The singleuser.profileList configuration can let the user choose an
image through the selection of a profile. This option determines if
those images will be pulled, both by the hook and continuous pullers.

The reason to disable this, is that if you have for example 10 images
which start pulling in order from 1 to 10, a user that arrives and
wants to start a pod with image number 10 will need to wait for all
images to be pulled, and then it may be preferable to just let the
user arriving wait for a single image to be pulled on arrival.


(schema:prePuller.extraImages)=
### prePuller.extraImages

See the [*optimization
section*](/administrator/optimization.html#the-images-that-will-be-pulled)
for more details.

```yaml
prePuller:
  extraImages:
    myExtraImageIWantPulled:
      name: jupyter/all-spark-notebook
      tag: 2343e33dec46
```


(schema:custom)=
## custom

Additional values to pass to the Hub.
JupyterHub will not itself look at these,
but you can read values in your own custom config via `hub.extraConfig`.
For example:

```yaml
custom:
  myHost: "https://example.horse"
hub:
  extraConfig:
    myConfig.py: |
      c.MyAuthenticator.host = get_config("custom.myHost")
```

