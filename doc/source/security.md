# Security

The information in this document focuses primarily on cloud based deployments. For on-premise deployments, additional security work that is specific to your installation method would also be required. Note that your specific installation's security needs might be more or less stringent than what we can offer you here.

Brad Geesamen gave a wonderful talk titled [Hacking and Hardening Kubernetes by Example](https://kccncna17.sched.com/event/CU6z/hacking-and-hardening-kubernetes-clusters-by-example-i-brad-geesaman-symantec) at Kubecon NA 2017. You can [watch the talk](https://www.youtube.com/watch?v=vTgQLzeBfRU) or [read the slides](https://schd.ws/hosted_files/kccncna17/47/Hacking%20and%20Hardening%20Kubernetes%20By%20Example%20v1.pdf). Highly recommended that you do so to understand the security issues you are up against when using Kubernetes to run JupyterHub.

## Reporting a security issue

If you find a security vulnerability in JupyterHub, either a failure of the
code to properly implement the model described here, or a failure of the
model itself, please report it to [security@ipython.org](mailto:security@ipython.org).

If you prefer to encrypt your security reports, you can use
[this PGP public key](https://jupyter-notebook.readthedocs.io/en/stable/_downloads/ipython_security.asc).


## HTTPS

This section describes how to enable HTTPS on your JupyterHub. The easiest way to do so is by using [Let's Encrypt](https://letsencrypt.org/), though we'll also cover how to set up your own HTTPS credentials. For more information
on HTTPS security see the certificates section of [this blog post](https://blog.hartleybrody.com/https-certificates/).

### Set up your domain

1. Buy a domain name from a registrar. Pick whichever one you want.

2. Create an A record from the domain you want to use, pointing to the EXTERNAL-IP of the proxy-public service. The exact way to do this will depend on the DNS provider that you’re using.

3. Wait for the change to propagate. Propagation can take several minutes to several hours. Wait until you can type in the name of the domain you bought and it shows you the JupyterHub landing page.

   It is important that you wait - prematurely going to the next step might cause problems!

### Set up automatic HTTPS

Refer to the Advanced Topics section for Automatic HTTPS with cert-manager and [Let's Encrypt](https://letsencrypt.org/).

### Set up manual HTTPS

If you have your own HTTPS certificates & want to use those instead of the automatically provisioned Let's Encrypt ones, that's also possible. Note that this is considered an advanced option, so we recommend not doing it unless you have good reasons.

1.  Add your domain name & HTTPS certificate info to your `config.yaml`

    ```yaml
    proxy:
      https:
        hosts:
          - <your-domain-name>
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

### Confirm that your domain is running HTTPS

There are many ways to confirm that a domain is running trusted HTTPS
certificates. One options is to use the [Qualys SSL Labs](https://ssllabs.com)
security report generator. Use the following URL structure to test your domain:

    ```
    http://ssllabs.com/ssltest/analyze.html?d=<YOUR-DOMAIN>
    ```
    
## Secure access to Helm

In its default configuration, helm pretty much allows root access to all other
pods running in your cluster. See this [Bitnami Helm security article](https://engineering.bitnami.com/articles/helm-security.html)
for more information. As a consequence, the default allows all users in your cluster to pretty much have root access to your whole cluster!

You can mitigate this by limiting public access to the Tiller API. To do so, use the following command:

```bash
kubectl --namespace=kube-system patch deployment tiller-deploy --type=json --patch='[{"op": "add", "path": "/spec/template/spec/containers/0/command", "value": ["/tiller", "--listen=localhost:44134"]}]'
```

This limit shouldn't affect helm functionality in any form.

## Audit Cloud Metadata server access

Most cloud providers have a static IP you can hit from any of the compute nodes, including the user pod, to get metadata about the cloud. This metadata can contain very sensitive info, and this metadata, in the wrong hands, can allow attackers to take full control of your cluster and cloud resources. It is **critical** to secure the metadata service. We block access to this IP by default (as of v0.6), so you are protected from this!

The slides beginning at [*Slide 38*](https://schd.ws/hosted_files/kccncna17/d8/Hacking%20and%20Hardening%20Kubernetes%20By%20Example%20v2.pdf) provides more information on the dangers presented by this attack.

If you need to enable access to the metadata server for some reason, you can do the following in config.yaml:

```yaml
singleuser:
  cloudMetadata:
    enabled: true
```

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

Kubernetes supports, and often requires, using [Role Based Access Control (RBAC)](https://kubernetes.io/docs/admin/authorization/rbac/)
to secure which pods / users can perform what kinds of actions on the cluster. RBAC rules can be set to provide users with minimal necessary access based on their administrative needs.


It is **critical** to understand that if RBAC is disabled, all pods are given `root` equivalent permission on the Kubernetes cluster and all the nodes in it. This opens up very bad vulnerabilites for your security.

As of the Helm chart v0.5 used with JupyterHub and BinderHub, the helm chart can natively work with RBAC enabled clusters. To provide sensible security defaults, we ship appropriate minimal RBAC rules for the various components we use. We **highly recommend** using these minimal or more restrictive RBAC rules.

If you want to disable the RBAC rules, for whatever reason, you can do so with the following snippet in your `config.yaml`:

```yaml
rbac:
   enabled: false
```

We strongly **discourage disabling** the RBAC rules and remind you that this
action will open up security vulnerabilities. However, some cloud providers
(particularly Azure AKS)
[do not support RBAC](https://github.com/Azure/AKS/issues/67) right now,
and you might have to disable RBAC with this config to run on Azure.

## Kubernetes API Access

Allowing direct user access to the Kubernetes API can be dangerous. It allows
users to grant themselves more privileges, access other users' content without
permission, run (unprofitable) bitcoin mining operations & various other
not-legitimate activities. By default, we do not allow access to the [service
account credentials](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/) needed
to access the kubernetes API from user servers for this reason.

If you want to (carefully!) give access to the Kubernetes API to your users, you
can do so with the following in your `config.yaml`:

```yaml
singleuser:
    serviceAccountName: <service-account-name>
```

You can either manually create a service account for use by your users and
specify the name of that here (recommended) or use `default` to give them access
to the default service account for the namespace. You should ideally also
(manually) set up [RBAC](https://kubernetes.io/docs/admin/authorization/rbac/)
rules for this service account to specify what permissions users will have.

This is a sensitive security issue (similar to writing sudo rules in a
traditional computing environment), so be very careful.

There's ongoing work on making this easier!


## Kubernetes Network Policies

Kubernetes has optional support for [network
policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
which lets you restrict how pods can communicate with each other and the outside
world. This can provide additional security within JupyterHub, and can also be
used to limit network access for users of JupyterHub.

By default, the JupyterHub helm chart **disables** network policies.

### Enabling network policies

**Important**: If you decide to enable network policies, you should be aware
that a Kubernetes cluster may have partial, full, or no support for network
policies. Kubernetes will **silently ignore** policies that aren't supported.
Please use **caution** if enabling network policies and verify the policies
behave as expected, especially if you rely on them to restrict what users can
access.

You can enable network policies in your `config.yaml`:

```yaml
hub:
  networkPolicy:
    enabled: true
proxy:
  networkPolicy:
    enabled: true
singleuser:
  networkPolicy:
    enabled: true
```

The default singleuser policy allows all outbound network traffic, meaning
JupyterHub users are able to connect to all resources inside and outside your
network. To restrict outbound traffic to DNS, HTTP and HTTPS:

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
        protocol: TCP
    - ports:
      - port: 433
        protocol: TCP
```

See the [Kubernetes
documentation](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
for further information on defining policies.
