# Security

The information in this document focuses primarily on cloud based deployments. For on-premise deployments, additional security work that is specific to your installation method would also be required. Note that your specific installation's security needs might be more or less stringent than what we can offer you here.

Brad Geesamen gave a wonderful talk titled [Hacking and Hardening Kubernetes by Example](https://kccncna17.sched.com/event/CU6z/hacking-and-hardening-kubernetes-clusters-by-example-i-brad-geesaman-symantec) at Kubecon NA 2017. You can [watch the talk](https://www.youtube.com/watch?v=vTgQLzeBfRU) or [read the slides](https://schd.ws/hosted_files/kccncna17/47/Hacking%20and%20Hardening%20Kubernetes%20By%20Example%20v1.pdf). Highly recommended that you do so to understand the security issues you are up against when using Kubernetes to run JupyterHub.

## HTTPS

This section describes how to enable HTTPS on your JupyterHub. The easiest way to do so is by using [Let's Encrypt](https://letsencrypt.org/), though we'll also cover how to set up your own HTTPS credentials. For more information
on HTTPS security see the certificates section of [this blog post](https://blog.hartleybrody.com/https-certificates/).

### Set up your domain

1. Buy a domain name from a registrar. Pick whichever one you want.

2. Create an A record from the domain you want to use, pointing to the EXTERNAL-IP of the proxy-public service. The exact way to do this will depend on the DNS provider that you’re using.

3. Wait for the change to propagate. Propagation can take several minutes to several hours. Wait until you can type in the name of the domain you bought and it shows you the JupyterHub landing page.

   It is important that you wait - prematurely going to the next step might cause problems!

### Set up automatic HTTPS

1. Specify the two bits of information that we need to automatically provision HTTPS certificates - your domain name & a contact email address.

   ```yaml
   proxy:
     https:
       hosts:
         - <your-domain-name>
       letsencrypt:
         contactEmail: <your-email-address>
   ```

2. Apply the config changes by running helm upgrade ....
3. Wait for about a minute, now your hub should be HTTPS enabled!

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

## Secure access to Helm

In its default configuration, helm pretty much allows root access to all other
pods running in your cluster. See this [Bitnami Helm security article](https://engineering.bitnami.com/articles/helm-security.html)
for more information. As a consequence, the default allows all users in your cluster to pretty much have root access to your whole cluster!

You can mitigate this by limiting public access to the Tiller API. To do so, use the following command:

```bash
kubectl --namespace=kube-system patch deployment tiller-deploy --type=json --patch='[{"op": "add", "path": "/spec/template/spec/containers/0/command", "value": ["/tiller", "--listen=localhost:44134"]}]'
```

This limit shouldn't affect helm functionality in any form.

## Audit Cloud Metadata server security

Most cloud providers have a static IP you can hit from any of the compute nodes, including the user pod, to get metadata about the cloud. This metadata can contain very sensitive info, and this metadata, in the wrong hands, can allow attackers to take full control of your cluster and cloud resources. It is **critical** to secure the metadata service.

The slides beginning at [*Slide 38*](https://schd.ws/hosted_files/kccncna17/d8/Hacking%20and%20Hardening%20Kubernetes%20By%20Example%20v2.pdf) provides more information on the dangers presented by this attack.

The easiest way to mitigate it is to add an [iptables](https://en.wikipedia.org/wiki/Iptables) rule in an [init-container](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/). This allows setting up firewall rules specific to the user pod in a secure way that the user can not undo. Here is how you could do it on the most popular clouds:

### Google Cloud / AWS / Azure

In all these clouds you can access the metadata service via the IP `169.254.169.254`. Blocking all outgoing packets to that IP should protect you.

```yaml
singleuser:
    initContainers:
      - name: block-metadata
        image: minrk/tc-init:0.0.4
        # Block access to GCE Metadata Service from user pods
        command: ["iptables", "-A", "OUTPUT", "-p", "tcp", "-d", "169.254.169.254", "-j", "DROP"]
        securityContext:
          runAsUser: 0
          capabilities:
            add: [ "NET_ADMIN" ]
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

We strongly **discourage disabling** the RBAC rules and remind you that this action will open up security vulnerabilities. Proceed with caution!

