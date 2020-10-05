# Security

The information in this document focuses primarily on cloud based deployments. For on-premise deployments, additional security work that is specific to your installation method would also be required. Note that your specific installation's security needs might be more or less stringent than what we can offer you here.

Brad Geesamen gave a wonderful talk titled [Hacking and Hardening Kubernetes by Example](https://kccncna17.sched.com/event/CU6z/hacking-and-hardening-kubernetes-clusters-by-example-i-brad-geesaman-symantec) at Kubecon NA 2017. You can [watch the talk](https://www.youtube.com/watch?v=vTgQLzeBfRU) or [read the slides](https://github.com/sbueringer/kubecon-slides/blob/master/slides/2017-kubecon-na/Hacking%20and%20Hardening%20Kubernetes%20Clusters%20by%20Example%20%5BI%5D%20-%20Brad%20Geesaman%2C%20Symantec%20-%20Hacking%20and%20Hardening%20Kubernetes%20By%20Example%20v2.pdf). Highly recommended that you do so to understand the security issues you are up against when using Kubernetes to run JupyterHub.

## Reporting a security issue

If you find a security vulnerability in JupyterHub, either a failure of the
code to properly implement the model described here, or a failure of the
model itself, please report it to [security@ipython.org](mailto:security@ipython.org).

If you prefer to encrypt your security reports, you can use
[this PGP public key](https://ipython.org/ipython-doc/2/_downloads/ipython_security.asc).

## HTTPS

This section describes how to enable HTTPS on your JupyterHub. The easiest way to do so is by using [Let's Encrypt](https://letsencrypt.org/), though we'll also cover how to set up your own HTTPS credentials. For more information
on HTTPS security see the certificates section of [this blog post](https://blog.hartleybrody.com/https-certificates/).

### Set up your domain

1. Buy a domain name from a registrar. Pick whichever one you want.

2. Create an A record from the domain you want to use, pointing to the EXTERNAL-IP of the proxy-public service. The exact way to do this will depend on the DNS provider that you’re using.

3. Wait for the change to propagate. Propagation can take several minutes to several hours. Wait until you can type in the name of the domain you bought and it shows you the JupyterHub landing page.

   It is important that you wait - prematurely going to the next step might cause problems!

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

***
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
***

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

2. Apply the config changes by running helm upgrade ....
3. Wait for about a minute, now your hub should be HTTPS enabled!


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
http://ssllabs.com/ssltest/analyze.html?d=<YOUR-DOMAIN>
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

## Use Role Based Access Control (RBAC)

Kubernetes supports, and often requires, using [Role Based Access Control (RBAC)](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
to secure which pods / users can perform what kinds of actions on the cluster. RBAC rules can be set to provide users with minimal necessary access based on their administrative needs.

It is **critical** to understand that if RBAC is disabled, all pods are given `root` equivalent permission on the Kubernetes cluster and all the nodes in it. This opens up very bad vulnerabilites for your security.

As of the Helm chart v0.5 used with JupyterHub and BinderHub, the helm chart can natively work with RBAC enabled clusters. To provide sensible security defaults, we ship appropriate minimal RBAC rules for the various components we use. We **highly recommend** using these minimal or more restrictive RBAC rules.

If you want to disable the RBAC rules, for whatever reason, you can do so with the following snippet in your `config.yaml`:

```yaml
rbac:
  enabled: false
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

The slides beginning at [_Slide
38_](https://schd.ws/hosted_files/kccncna17/d8/Hacking%20and%20Hardening%20Kubernetes%20By%20Example%20v2.pdf)
provides more information on the dangers presented by this attack.

This Helm chart blocks access to this metadata in two ways by default, but you
only need one.

### Block metadata with a NetworkPolicy enforced by a NetworkPolicy controller

If you have _NetworkPolicy controller_ such as Calico in the Kubernetes cluster,
it will enforce the NetworkPolicy resource created by this chart
(`singleuser.networkPolicy.*`) that blocks user access to the metadata server.
We recommend relying on this approach if you you had a NetworkPolicy controller,
and then you can disable the other option.

### Block metadata with a privileged initContainer running `iptables`

If you can't rely on the NetworkPolicy approach to block access to the metadata
server, we suggest relying on this option. When
`singleuser.cloudMetadata.blockWithIptables` is true as it is by default, an
`initContainer` is added to the user pods. It will run with elevated privileges
and use the `iptables` command line tool to block access to the metadata server.

```yaml
# default configuration
singleuser:
  cloudMetadata:
    blockWithIptables: true
    ip: 169.254.169.254
```

## Kubernetes Network Policies

**Important**: When using network policies, you should be aware
that a Kubernetes cluster may have partial, full, or no support for network policies.
Kubernetes will **silently ignore** policies that aren't supported.
Please use **caution** before relying on network policy enforcement
and verify the policies behave as expected,
especially if you rely on them to restrict what users can access.

Kubernetes has optional support for [network
policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
which lets you restrict how pods can communicate with each other and the outside
world. This can provide additional security within JupyterHub, and can also be
used to limit network access for users of JupyterHub.

By default, the JupyterHub helm chart **enables** network policies in 0.10 or later.
They are **disabled** by default in 0.9 and earlier.

The JupyterHub chart has three network policies,
one for each component (hub, proxy, single-user servers),
which can be enabled and configured separately.

### Enabling and disabling network policies

By default, the JupyterHub helm chart **enables** network policies in 0.10 or later.
They are **disabled** by default in 0.9 and earlier.

You can enable or disable enforcement of each network policy in config.yaml:

```yaml
hub:
  networkPolicy:
    enabled: true  # or false to disable
proxy:
  networkPolicy:
    enabled: true
singleuser:
  networkPolicy:
    enabled: true
```

### Granting network access to jupyterhub pods (ingress)

The chart's network policy default behavior ensures that all of the jupyterhub components can talk to each other,
so all of the following connections are allowed:

- proxy ⇨ hub
- proxy ⇨ singleuser
- hub ⇨ proxy api
- hub ⬄ singleuser
- everything ⇨ DNS

and by default do not allow any other pods to talk to the jupyterhub components.

The network policies use label selectors that look like:

```yaml
ingress:
  # allowed pods (hub.jupyter.org/network-access-hub) --> hub
  - from:
      - podSelector:
          matchLabels:
            hub.jupyter.org/network-access-hub: "true"
```

So if you are creating additional pods that want to talk to these,
you can grant them access to jupyterhub components one by one by adding the right labels.
Here is an example set of labels granting access to all jupyterhub components
(i.e. the same behavior as without network policies):

```yaml
metadata:
  name: my-service
  labels:
    hub.jupyter.org/network-access-hub: "true"  # access the hub api
    hub.jupyter.org/network-access-proxy-http: "true"  # access proxy public http endpoint
    hub.jupyter.org/network-access-proxy-api: "true"  # access proxy api
    hub.jupyter.org/network-access-singleuser: "true"  # access single-user servers directly
```

You can also add additional `ingress` rules to each network policy in your `config.yaml`.
See the [Kubernetes documentation](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
for how to define ingress rules.

### Limiting network access from pods (egress)

By default, all of the pods allow all `egress` traffic,
which means that code in each of the pods may make connections to anywhere in the cluster or on the Internet
(unless that would be blocked by the ingress rules of the destination).
This is very permissive.
The default policy for all components allows all outbound (egress) network traffic,
meaning JupyterHub users are able to connect to all resources inside and outside your network.
You can override the `egress` configuration of each policy
to make it more restrictive.
For example, to restrict user outbound traffic to DNS, HTTP, and HTTPS:

```yaml
singleuser:
  networkPolicy:
    enabled: true
    egress:
      - ports:
          - port: 53
            protocol: UDP
      - ports:
          - port: 80
      - ports:
          - port: 443
```

See the [Kubernetes
documentation](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
for further information on defining policies.

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
