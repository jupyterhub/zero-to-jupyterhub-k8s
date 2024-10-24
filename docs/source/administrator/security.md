(security)=

# Security

The information in this document focuses primarily on cloud based deployments. For on-premise deployments, additional security work that is specific to your installation method would also be required. Note that your specific installation's security needs might be more or less stringent than what we can offer you here.

Brad Geesamen gave a wonderful talk titled [Hacking and Hardening Kubernetes by Example](https://kccncna17.sched.com/event/CU6z/hacking-and-hardening-kubernetes-clusters-by-example-i-brad-geesaman-symantec) at Kubecon NA 2017 and you can [watch the talk](https://www.youtube.com/watch?v=vTgQLzeBfRU). Highly recommended that you do so to understand the security issues you are up against when using Kubernetes to run JupyterHub.

## Reporting a security issue

If you find a security vulnerability in JupyterHub, either a failure of the
code to properly implement the model described here, or a failure of the
model itself, please report it to [security@ipython.org](mailto:security@ipython.org).

If you prefer to encrypt your security reports, you can use
[this PGP public key](https://ipython.org/ipython-doc/2/_downloads/ipython_security.asc).

(https)=

## HTTPS

This section describes how to enable HTTPS on your JupyterHub. The easiest way to do so is by using [Let's Encrypt](https://letsencrypt.org/), though we'll also cover how to set up your own HTTPS credentials. For more information
on HTTPS security see the certificates section of [this blog post](https://blog.hartleybrody.com/https-certificates/).

### Set up your domain

1. Buy a domain name from a registrar. Pick whichever one you want.

2. Create an A record from the domain you want to use, pointing to the EXTERNAL-IP of the proxy-public service. The exact way to do this will depend on the DNS provider that you’re using.

3. Wait for the change to propagate. Propagation can take several minutes to several hours. Wait until you can type in the name of the domain you bought and it shows you the JupyterHub landing page.

   It is important that you wait - prematurely going to the next step might cause problems!

(setup-automatic-https)=

### Set up automatic HTTPS

JupyterHub uses [Let's Encrypt](https://letsencrypt.org/) to automatically create
HTTPS certificates for your deployment. This will cause your HTTPS certificate
to automatically renew every few months. To enable this, make the following
changes to your `config.yaml` file:

1. Specify the two bits of information that we need to automatically provision
   HTTPS certificates - your domain name & a contact email address.

   ```yaml
   proxy:
     https:
       enabled: true
       hosts:
         - <your-domain-name>
       letsencrypt:
         contactEmail: <your-email-address>
   ```

2. Apply the config changes by running `helm upgrade ...`
3. Wait for about a minute, now your hub should be HTTPS enabled!

---

**NOTE:**

If the proxy service is of type `LoadBalancer`, which it is by default, then a specific static IP address can be requested (if available) instead of a dynamically acquired one.
Although not essential for HTTPS, using a static IP address is a recommended practice for domain names referencing fixed IPs.
This ensures the same IP address for multiple deployments.
The IP can be provided like:

```yaml
proxy:
  service:
    loadBalancerIP: xxx.xxx.xxx.xxx
```

More info about this can be found on the [Configuration Reference](helm-chart-configuration-reference) page.

---

(setup-manual-https)=

### Set up manual HTTPS

If you have your own HTTPS certificates & want to use those instead of the automatically provisioned Let's Encrypt ones, that's also possible. Note that this is considered an advanced option, so we recommend not doing it unless you have good reasons.

There are two ways to specify your manual certificate, directly in the config.yaml or by creating a [Kubernetes `secret`](https://kubernetes.io/docs/concepts/configuration/secret/).

#### Specify certificate in config.yaml

1.  Add your domain name & HTTPS certificate info to your `config.yaml`

    ```yaml
    proxy:
      https:
        enabled: true
        type: manual
        manual:
          key: |
            -----BEGIN RSA PRIVATE KEY-----
            ...
            -----END RSA PRIVATE KEY-----
          cert: |
            -----BEGIN CERTIFICATE-----
            ...
            -----END CERTIFICATE-----
    ```

2.  Apply the config changes by running helm upgrade ....
3.  Wait for about a minute, now your hub should be HTTPS enabled!

#### Specify certificate through Secret resource

1. Create a `secret` resource with type `kubernetes.io/tls` containing your certificate.

   `kubectl create secret tls example-tls --key="tls.key" --cert="tls.crt"`

2. Add your domain and the name of your `secret` to your config.yaml.

   ```yaml
   proxy:
     https:
       enabled: true
       hosts:
         - <your-domain-name>
       type: secret
       secret:
         name: example-tls
   ```

3. Apply the config changes by running helm upgrade ....
4. Wait for about a minute, now your hub should be HTTPS enabled!

### Off-loading SSL to a Load Balancer

In some environments with a trusted network, you may want to terminate SSL at a
load balancer. If https is enabled, and `proxy.https.type` is set to `offload`,
the HTTP and HTTPS front ends target the HTTP port from JupyterHub.

The HTTPS listener on the load balancer will need to be configured based on the
provider. If you're using AWS and a certificate provided by their certificate
manager, your config.yml might look something like:

```yaml
proxy:
  https:
    enabled: true
    type: offload
  service:
    annotations:
      # Certificate ARN
      service.beta.kubernetes.io/aws-load-balancer-ssl-cert: "arn:aws:acm:us-east-1:1234567891011:certificate/uuid"
      # The protocol to use on the backend, we use TCP since we're using websockets
      service.beta.kubernetes.io/aws-load-balancer-backend-protocol: "tcp"
      # Which ports should use SSL
      service.beta.kubernetes.io/aws-load-balancer-ssl-ports: "https"
      service.beta.kubernetes.io/aws-load-balancer-connection-idle-timeout: "3600"
```

Annotation options will vary by provider.

### Confirm that your domain is running HTTPS

There are many ways to confirm that a domain is running trusted HTTPS
certificates. One options is to use the [Qualys SSL Labs](https://www.ssllabs.com/)
security report generator. Use the following URL structure to test your domain:

```
https://ssllabs.com/ssltest/analyze.html?d=<YOUR-DOMAIN>
```

## Minimal hub image

The default hub image includes some useful debugging tools.
You can use the slim version of image to minimise your exposure to vulnerabilities in those optional tools.

```yaml
hub:
  image:
    # The slim variant excludes a few non-essential packages that are useful
    # when debugging something from the hub pod. To use it, apply this
    # configuration.
    #
    name: quay.io/jupyterhub/k8s-hub-slim
```

```{note}
We are based on Linux Debian as a base image. There are container
scanners that pick up known vulnerabilities in Debian that the Debian security
team has dismissed. For details about this, see [this
comment](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues/2918#issuecomment-1295813128).
```

## Secure access to Helm

Helm 3 supports the security, identity, and authorization features of modern Kubernetes. Helm’s permissions are evaluated using your kubeconfig file. Cluster administrators can restrict user permissions at whatever granularity they see fit.

Read more about organizing cluster access using kubeconfig files in the
[Kubernetes docs](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/).

## Delete the Kubernetes Dashboard

The [Kubernetes Dashboard](https://github.com/kubernetes/dashboard) gets created by default in many installations. Although the Dashboard contains useful information, the Dashboard also poses a security risk. We **recommend** deleting it and not using it for the time being until the Dashboard becomes properly securable.

You can mitigate this by deleting the Kubernetes Dashboard deployment from your cluster. This can be most likely performed with:

```bash
kubectl --namespace=kube-system delete deployment kubernetes-dashboard
```

In older clusters, you might have to do:

```bash
kubectl --namespace=kube-system delete rc kubernetes-dashboard
```

(rbac)=

## Use Role Based Access Control (RBAC)

Kubernetes supports, and often requires, using [Role Based Access Control (RBAC)](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
to secure which pods / users can perform what kinds of actions on the cluster. RBAC rules can be set to provide users with minimal necessary access based on their administrative needs.

It is **critical** to understand that if RBAC is disabled, all pods are given `root` equivalent permission on the Kubernetes cluster and all the nodes in it. This opens up very bad vulnerabilities for your security.

As of the Helm chart v0.5 used with JupyterHub and BinderHub, the helm chart can natively work with RBAC enabled clusters. To provide sensible security defaults, we ship appropriate minimal RBAC rules for the various components we use. We **highly recommend** using these minimal or more restrictive RBAC rules.

If you want to disable the RBAC rules, for whatever reason, you can do so with the following snippet in your `config.yaml`:

```yaml
rbac:
  create: false
```

We strongly **discourage disabling** the RBAC rules and remind you that this
action will open up security vulnerabilities. However, some cloud providers may
not support RBAC in which case you can disable it with this config.

## Kubernetes API Access

Allowing direct user access to the Kubernetes API can be dangerous. It allows
users to grant themselves more privileges, access other users' content without
permission, run (unprofitable) bitcoin mining operations & various other
not-legitimate activities. By default, we do not allow access to the [service
account credentials](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/) needed
to access the Kubernetes API from user servers for this reason.

If you want to (carefully!) give access to the Kubernetes API to your users, you
can do so with the following in your `config.yaml`:

```yaml
singleuser:
  serviceAccountName: <service-account-name>
```

You can either manually create a service account for use by your users and
specify the name of that here (recommended) or use `default` to give them access
to the default service account for the namespace. You should ideally also
(manually) set up [RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
rules for this service account to specify what permissions users will have.

This is a sensitive security issue (similar to writing sudo rules in a
traditional computing environment), so be very careful.

There's ongoing work on making this easier!

## Audit Cloud Metadata server access

Most cloud providers have a static IP that pods can reach to get metadata about
the cloud. This metadata can contain very sensitive info and in the wrong hands
allow attackers to take full control of your cluster and cloud resources. Due to
this, it is **critical** to secure the metadata service from your user pods that
could end up running malicious code without knowing it.

This [presentation, 27 min in and
onwards](https://www.youtube.com/watch?v=vTgQLzeBfRU&t=27m7s), provides more
information on the dangers presented by this attack.

This Helm chart blocks access to this metadata in two ways by default, but you
only need one.

(block-metadata-netpol)=

### Block cloud metadata API with a NetworkPolicy enforced by a NetworkPolicy controller

If you have _NetworkPolicy controller_ such as Calico or Cilium in the
Kubernetes cluster, it will enforce the NetworkPolicy resource created by this
chart (`singleuser.networkPolicy.*`) that by default doesn't allow (and
therefore blocks) user access to the cloud metadata API exposed on a specific IP
(`169.254.169.254`).

```{note}
If you have a NetworkPolicy controller, we recommend relying on it and setting
`singleuser.cloudMetadata.blockWithIptables` to `false`.
```

(block-metadata-iptables)=

### Block cloud metadata API with a privileged initContainer running `iptables`

If you can't rely on the NetworkPolicy approach to block access to the cloud
metadata API, we suggest relying on this option instead. When
`singleuser.cloudMetadata.blockWithIptables` is true as it is by default, an
`initContainer` is added to the user pods. It will run with elevated privileges
and use the `iptables` command line tool to block all network access to the
cloud metadata server.

```yaml
# default configuration
singleuser:
  cloudMetadata:
    blockWithIptables: true
    ip: 169.254.169.254
```

```{versionchanged} 3.0.0
This configuration is not allowed to be configured true at the same time as
[`singleuser.networkPolicy.egressAllowRules.cloudMetadataServer`](schema_singleuser.networkPolicy.egressAllowRules.cloudMetadataServer)
to avoid an ambiguous configuration.
```

(netpol)=

## Kubernetes Network Policies

```{warning}
Your Kubernetes cluster may silently ignore the network rules described in the
NetworkPolicy resources that this Helm chart can create. NetworkPolicy rules are
enforced by an optional NetworkPolicy controller that often isn't setup as part
of setting up a Kubernetes cluster.
```

By default this Helm chart creates four different
[NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
resources describing what incoming/ingress and outgoing/egress connections are
to be allowed for the pods they target.

A critical point to understand is that if a pod's ingress or egress connections
respectively aren't targeted by a NetworkPolicy, they won't be constrained by
them at all. If they are though, only what is explicitly allowed for them will
be accepted. In other words, the act of defining a NetworkPolicy targeting a pod
is what is constraining it, but all the rules in the NetworkPolicy are allow
rules.

### Introduction to the chart's four network policies

The four network policies declare rules for four kinds of pods created by the
Helm chart. Below are some tables describing what the four network policy do to
some extent.

| NetworkPolicy | Associated Helm chart config  | Influenced pods      | Notable software in pods                                             |
| ------------- | ----------------------------- | -------------------- | -------------------------------------------------------------------- |
| `hub`         | `hub.networkPolicy`           | `hub`                | `jupyterhub`, `kubespawner`, `jupyterhub-idle-culler`, Authenticator |
| `proxy`       | `proxy.chp.networkPolicy`     | `proxy`              | `configurable-http-proxy`                                            |
| `autohttps`   | `proxy.traefik.networkPolicy` | `autohttps`          | `traefik`, `lego`                                                    |
| `singleuser`  | `singleuser.networkPolicy`    | `jupyter-<username>` | `jupyter_server`                                                     |

| NetworkPolicy | Always allowed outbound connections (egress) for core functionality                                              |
| ------------- | ---------------------------------------------------------------------------------------------------------------- |
| `hub`         | To `proxy` pod's REST API port (8001), user pods' only port (8888)                                               |
| `proxy`       | To `hub` pod's only port (8081), user pods' only port (8888)                                                     |
| `autohttps`   | To `proxy` pod's http proxy port (8000)                                                                          |
| `singleuser`  | To `hub` pod's only port (8081), `proxy` pod's proxy port (8000), `autohttps` pod's http (8080) and https (8443) |

| NetworkPolicy | Always allowed inbound connections (ingress) for core functionality, ingress is allowed for specific ports from pods with certain labels                                       |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `hub`         | From pods labelled `hub.jupyter.org/network-access-hub=true`                                                                                                                   |
| `proxy`       | From pods labelled `hub.jupyter.org/network-access-proxy-http=true` (http proxy port) or `hub.jupyter.org/network-access-proxy-api=true` (REST API port) in the same namespace |
| `autohttps`   | From pods labelled `hub.jupyter.org/network-access-proxy-http=true` (http(s) proxy ports)                                                                                      |
| `singleuser`  | From pods labelled `hub.jupyter.org/network-access-singleuser=true` (notebook-port)                                                                                            |

````{admonition} Not all functionality summarized above
:class: warning

It has been tricky to document the full behavior of these network policies. For
in depth details, please for now refer to inspecting the Helm chart's templates
and the rendered result given your configuration.

Below are links to the Helm chart's templates.

- [`hub` template](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/HEAD/jupyterhub/templates/hub/netpol.yaml)
- [`proxy` template](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/HEAD/jupyterhub/templates/proxy/netpol.yaml)
- [`autohttps` template](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/HEAD/jupyterhub/templates/proxy/autohttps/netpol.yaml)
- [`singleuser` template](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/HEAD/jupyterhub/templates/singleuser/netpol.yaml)

Below are commands you can use to render the specific template.

```shell
# These four commands renders the four NetworkPolicy resource templates of the
# latest release of the JupyterHub Helm chart, with default values.
#
# You can pass `--values <your config file>` or `--version <version here>` to
# these commands to inspect the rendered NetworkPolicy resources given your
# specific version and configuration.
#
helm template --repo https://jupyterhub.github.io/helm-chart jupyterhub --show-only templates/hub/netpol.yaml
helm template --repo https://jupyterhub.github.io/helm-chart jupyterhub --show-only templates/proxy/netpol.yaml
helm template --repo https://jupyterhub.github.io/helm-chart jupyterhub --show-only templates/proxy/autohttps/netpol.yaml
helm template --repo https://jupyterhub.github.io/helm-chart jupyterhub --show-only templates/singleuser/netpol.yaml
```
````

### Enabling and disabling network policies

NetworkPolicy resources are created by default, and with their creation they
restrict inbound and outbound network connections to those explicitly allowed in
the NetworkPolicy resource. To opt-out of creating NetworkPolicy resources, use
configuration like below.

```yaml
# Example configuration on how to disable the creation of all the Helm chart's
# NetworkPolicy resources.
hub:
  networkPolicy:
    enabled: false
proxy:
  chp:
    networkPolicy:
      enabled: false
  traefik:
    networkPolicy:
      enabled: false
singleuser:
  networkPolicy:
    enabled: false
```

### Allowing additional inbound network connections (ingress)

While you can add allow arbitrary allow rules with the
[`<hub|proxy.chp|proxy.traefik|singleuser>.networkPolicy.ingress`](schema_hub.networkPolicy.ingress)
configuration besides the rules ensuring core functionality, you can also label
the pods you want to be allowed to establish connections to the Helm chart's
various pods.

For example, to access the hub pod from another pod in the same namespace, just
add the label `hub.jupyter.org/network-access-hub: "true"` to the pod that
should be able to establish a connection to the hub pod.

The available access labels are:

- `hub.jupyter.org/network-access-hub: "true"`, access the hub api
- `hub.jupyter.org/network-access-proxy-http: "true"`, access proxy public http endpoint
- `hub.jupyter.org/network-access-proxy-api: "true"`, access proxy api
- `hub.jupyter.org/network-access-singleuser: "true"`, access singleuser servers directly

If you wish to access the pod from another namespace with these labels, then
read about
[`<hub|proxy.chp|proxy.traefik|singleuser>.networkPolicy.interNamespaceAccessLabels`](schema_hub.networkPolicy.interNamespaceAccessLabels).

Finally, the option
[`<hub|proxy.chp|proxy.traefik|singleuser>.networkPolicy.allowedIngressPorts`](schema_hub.networkPolicy.allowedIngressPorts)
enable you to allow incoming connections on certain pods.

### Allowing additional outbound network connections (egress)

While you can add allow arbitrary allow rules with the
[`<hub|proxy.chp|proxy.traefik|singleuser>.networkPolicy.egress`](schema_hub.networkPolicy.egress)
configuration besides the rules ensuring core functionality, you can also toggle
some pre-defined allow rules on or off. They are documented in the configuration
reference under
[`<hub|proxy.chp|proxy.traefik|singleuser>.networkPolicy.egressAllowRules`](schema_hub.networkPolicy.egressAllowRules).

By default, all egress allow rules are enabled for `hub`, `proxy.chp`, and
`proxy.traefik`, but
`singleuser.networkPolicy.egressAllowRules.cloudMetadataServer` and
`singleuser.networkPolicy.egressAllowRules.privateIPs` default to false. In
practice, this can mean no rule allows the user pods to communicate with some
k8s local service with [Private IPv4
addresses](https://en.wikipedia.org/wiki/Private_network#Private_IPv4_addresses).

```{versionchanged} 2.0.0
Before JupyterHub Helm chart 2.0.0 the default configuration was to allow
singleuser pods to establish outbound connections to anything. After 2.0.0
`singleuser.networkPolicy.egressAllowRules.privateIPs=true` must be explicitly
set for this.
```

## Restricting Load Balancer Access

By default any IP address can access your JupyterHub deployment through the load balancer service.
In case you want to restrict which IP addresses are allowed to access the load balancer, you can
specify a list of IP CIDR addresses in your `config.yaml` as follows:

```yaml
proxy:
  service:
    loadBalancerSourceRanges:
      - 111.111.111.111/32
      - 222.222.222.222/32
```

This would restrict the access to only two IP addresses: `111.111.111.111` and `222.222.222.222`.

(jupyterhub_subdomains)=

## Host user servers on a subdomain

You can reduce the chance of cross-origin attacks by giving each user
their own subdomain `<user>.jupyter.example.org`.
This requires setting [`subdomain_host`](schema_hub.config.JupyterHub.subdomain_host), creating a wildcard DNS record `*.jupyter.example.org`, and creating a wildcard SSL certificate.

```yaml
hub:
  config:
    JupyterHub:
      subdomain_host: jupyter.example.org
```

If you are using a Kubernetes ingress this must include hosts
`jupyter.example.org` and `*.jupyter.example.org`.
For example:

```yaml
ingress:
  enabled: true
  hosts:
    - jupyter.example.org
    - "*.jupyter.example.org"
  tls:
    - hosts:
        - jupyter.example.org
        - "*.jupyter.example.org"
      secretName: example-tls
```

where `example-tls` is the name of a Kubernetes secret containing the wildcard certificate and key.

The chart does not support the automatic creation of wildcard HTTPS certificates.
You must obtain a certificate from an external source,
for example by using an ACME client such as [cert-manager with the DNS-01 challenge](https://cert-manager.io/docs/configuration/acme/dns01/),
and ensure the certificate and key are stored in the secret.

See {ref}`jupyterhub:subdomains` in the JupyterHub documentation for more information.
