# Advanced Topics

This page contains a grab bag of various useful topics that don't have an easy
home elsewhere:

- Ingress
- Arbitrary code in `jupyterhub_config.py`
- Picking a Scheduler Strategy
- ## Pre-pulling Images for Faster Startup

Most people setting up JupyterHubs on popular public clouds
should not have to use any of this information, but it is essential for more
complex installations.

## Ingress

If you are using a Kubernetes Cluster that does not provide public IPs for
services directly, you need to use
an [ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
to get traffic into your JupyterHub. This varies wildly
based on how your cluster was set up, which is why this is in the 'Advanced' section.

You can enable the required `ingress` object with the following in your
`config.yaml`

```yaml
ingress:
    enabled: true
    hosts:
     - <hostname>
```

You can specify multiple hosts that should be routed to the hub by listing them
under `ingress.hosts`.

Note that you need to install and configure an
[Ingress Controller](https://kubernetes.io/docs/concepts/services-networking/ingress/#ingress-controllers)
for the ingress object to work. We recommend the
[nginx ingress](https://github.com/kubernetes/charts/tree/master/stable/nginx-ingress)
controller maintained by the community.

### Automatic HTTPS with kube-lego & Let's Encrypt

The default automatic HTTPS support does not work if you are using an ingress
object. You'd have to set it up yourself.


This uses [kube-lego](https://github.com/jetstack/kube-lego) to automatically
fetch and renew HTTPS certificates
from [Let's Encrypt](https://letsencrypt.org/). This currently only works with
the nginx ingress controller & google cloud's ingress controller.

1. Make sure that DNS is properly set up (varies wildly depending on the ingress
   controller you are using and how your cluster was set up). Accessing
   `<hostname>` from a browser should route traffic to the hub.
2. Install & configure kube-lego using the
   [kube-lego helm-chart](https://github.com/kubernetes/charts/tree/master/stable/kube-lego).
   Remember to change `config.LEGO_EMAIL` and `config.LEGO_URL` at the least.
3. Add an annotation + TLS config to the ingress so kube-lego knows to get certificates for
   it:

   ```yaml
   ingress:
     annotations:
       kubernetes.io/tls-acme: "true"
     tls:
      - hosts:
         - <hostname>
        secretName: kubelego-tls-jupyterhub
   ```

This should provision a certificate, and keep renewing it whenever it gets close
to expiry!

## Arbitrary code in `jupyterhub_config.py`

Sometimes the various options exposed via the helm-chart's `values.yaml` is not
enough, and you need to insert arbitrary extra code / config into
`jupyterhub_config.py`. This is a valuable escape hatch for both prototyping new
features that are not yet present in the helm-chart, and also for
installation-specific customization that is not suited for upstreaming.

There are four properties you can set in your `config.yaml` to do this.

### `hub.extraConfig`

The value specified for `hub.extraConfig` is evaluated as python code at the end
of `jupyterhub_config.py`. You can do anything here since it is arbitrary Python
Code. Some examples of things you can do:

1. Override various methods in the Spawner / Authenticator by subclassing them.
   For example, you can use this to pass authentication credentials for the user
   (such as GitHub OAuth tokens) to the environment. See
   [the JupyterHub docs](http://jupyterhub.readthedocs.io/en/latest/reference/authenticators.html#authentication-state) for
   an example.
2. Specify traitlets that take callables as values, allowing dynamic per-user
   configuration.
3. Set traitlets for JupyterHub / Spawner / Authenticator that are not currently
   supported in the helm chart

Unfortunately, you have to write your python *in* your YAML file. There's no way
to include a file in `config.yaml`.

You can specify `hub.extraConfig` as a raw string (remember to use the `|` for multi-line
YAML strings):

```yaml
hub:
  extraConfig: |
    import time
    c.Spawner.environment += {
       "CURRENT_TIME": str(time.time())
    }
```

You can also specify `hub.extraConfig` as a dictionary, if you want to logically
split your customizations. The code will be evaluated in alphabetical sorted
order of the key.

```yaml
hub:
  extraConfig:
   00-first-config: |
     # some code
   10-second-config: |
     # some other code
```

### `hub.extraConfigMap`

This property takes a dictionary of values that are then made available for code
in `hub.extraConfig` to read using a `z2jh.get_config` function. You can use this to
easily separate your code (which goes in `hub.extraConfig`) from your config
(which should go here).

For example, if you use the following snippet in your config.yaml file:

```yaml
hub:
  extraConfigMap:
    myString: Hello!
    myList:
      - Item1
      - Item2
    myDict:
      key: value
    myLongString: |
      Line1
      Line2
```

In your `hub.extraConfig`,

1. `z2jh.get_config('custom.myString')` will return a string `"Hello!"`
2. `z2jh.get_config('custom.myList')` will return a list `["Item1", "Item2"]`
3. `z2jh.get_config('custom.myDict')` will return a dict `{"key": "value"}`
4. `z2jh.get_config('custom.myLongString')` will return a string `"Line1\nLine2"`
5. `z2jh.get_config('custom.nonExistent')` will return `None` (since you didn't
    specify any value for `nonExistent`)
6. `z2jh.get_config('custom.myDefault', True)` will return `True`, since that is
    specified as the second parameter (default)

You need to have a `import z2jh` at the top of your `extraConfig` for
`z2jh.get_config()` to work.

Note that the keys in `hub.extraConfigMap` must be alpha numeric strings
starting with a character. Dashes and Underscores are not allowed.

### `hub.extraEnv`

This property takes a dictionary that is set as environment variables in the hub
container. You can use this to either pass in additional config to code in your
`hub.extraConfig` or set some hub parameters that are not settable by other means.

### `hub.extraContainers`

A list of extra containers that are bundled alongside the hub container in the
same pod. This is a
[common pattern](http://blog.kubernetes.io/2015/06/the-distributed-system-toolkit-patterns.html) in
kubernetes that as a long list of cool use cases. Some example use cases are:

1. Database Proxies, which are sometimes required for the hub to talk to its
   configured database
   (in [Google Cloud](https://cloud.google.com/sql/docs/mysql/sql-proxy)) for example
2. Servers / other daemons that are used by code in your `hub.customConfig`

The items in this list must be valid kubernetes
[container specifications](https://kubernetes.io/docs/api-reference/v1.8/#container-v1-core).

## Picking a Scheduler Strategy

Kubernetes offers very flexible ways to determine how it distributes pods on
your nodes. The JupyterHub helm chart supports two common configurations, see
below for a brief description of each.

### Spread

* **Behavior**: This spreads user pods across **as many nodes as possible**.
* **Benefits**: A single node going down will not affect too many users. If you do not have explicit memory & cpu
  limits, this strategy also allows your users the most efficient use of RAM & CPU.
* **Drawbacks**: This strategy is less efficient when used with autoscaling.

This is the default strategy. To explicitly specify it, use the following in your
`config.yaml`:

```yaml
singleuser:
   schedulerStrategy: spread
```

### Pack

* **Behavior**: This packs user pods into **as few nodes as possible**.
* **Benefits**: This increases your resource utilization, which is useful in conjunction with autoscalers.
* **Drawbacks**: A single node going down might affect more user pods than using
  a "spread" strategy (depending on the node).

When you use this strategy, you should specify limits and guarantees for memory
and cpu. This will make your users' experience more predictable.

To explicitly specify this strategy, use the following in your `config.yaml`:

```yaml
singleuser:
    schedulerStrategy: pack
```

## Pre-pulling Images for Faster Startup

Pulling and building a user's images forces a user to wait before the user's
server is started. Sometimes, the wait can be 5 to 10 minutes. **Pre-pulling**
the images on all the nodes can cut this wait time to a few seconds. Let's look
at how pre-pulling works.

### Pre-pulling basics

With **pre-pulling**, which is enabled by default, the user's container image
is pulled on all nodes whenever a `helm install` or `helm upgrade` is performed.
While this causes `helm install` and `helm upgrade` to take several minutes,
this time makes the user startup experience faster and more pleasant.

With the default **pre-pulling** setting, a `helm install` or `helm upgrade`
will cause the system to wait for 5 minutes to begin pulling the images before
timing out. This wait time is configurable by passing the `--wait <seconds>`
flag to the `helm` commands.

We recommend using pre-pulling. For the rare cases where you have a good reason
to disable it, pre-pulling can be disabled. To disable the pre-pulling during
`helm install` and `helm upgrade`, you can use the following snippet in
your `config.yaml`:


```yaml
prePuller:
   hook:
     enabled: false
```

This is not recommended unless you have specific good reasons to disable it!

### Pre-Pulling and changes in cluster size

Cluster size can change through manual addition of nodes or autoscaling. When a
new node is added to the cluster, the new node does not yet have the user image.
A user using this new node would be forced to wait while the image is pulled
from scratch. Ideally, it would be helpful to pre-pull images when the new node
is added to the cluster.

By enabling the **continuous pre-puller** (default state is disabled), the user
image will be pre-pulled when adding a new node. When enabled, the
**continuous pre-puller** runs as a [daemonset](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)
to force kubernetes to pull the user image on all nodes as soon as a node is
present. The continuous pre-puller uses minimal resources on all nodes and
greatly speeds up the user pod start time.

The continuous pre-puller is not enabled by default. To enable it, use the
following snippet in your `config.yaml`:

```yaml
prePuller:
  continuous:
    enabled: true
```
