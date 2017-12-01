# Advanced Topics

This page contains a grab bag of various useful topics that don't have an easy
home elsewhere. Most people setting up JupyterHubs on popular public clouds
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
1. Install & configure kube-lego using the
   [kube-lego helm-chart](https://github.com/kubernetes/charts/tree/master/stable/kube-lego).
   Remember to change `config.LEGO_EMAIL` and `config.LEGO_URL` at the least.
2. Add an annotation + TLS config to the ingress so kube-lego knows to get certificates for
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
