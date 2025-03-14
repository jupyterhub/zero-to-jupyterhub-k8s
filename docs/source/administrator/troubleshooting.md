(faq)=

# FAQ

This section contains frequently asked questions about the JupyterHub deployment.
For information on debugging Kubernetes, see {ref}`debug`.

## I thought I had deleted my cloud resources, but they still show up. Why?

You probably deleted the specific nodes, but not the Kubernetes cluster that
was controlling those nodes. Kubernetes is designed to make sure that a
specific set of resources is available at all times. This means that if you
only delete the nodes, but not the Kubernetes instance, then it will detect
the loss of computers and will create two new nodes to compensate.

## How does billing for this work?

JupyterHub isn't handling any of the billing for your usage. That's done
through whatever cloud service you're using. For considerations about
managing cost with JupyterHub, see {ref}`cost`.

## What version of JupyterHub is installed in the Helm Chart?

Each Helm Chart is packaged with a specific version of JupyterHub (and
other software as well). See see the [Helm Chart repository](https://github.com/jupyterhub/helm-chart#release-notes)
for information about the versions of relevant software packages.

## Metrics scraping with prometheus or vmagent

Network policy needs to be modified in order for prometheus or vmagent to be able to reach the metrics endpoint. The recommended way is by setting [interNamespaceAccessLabels=accept](https://z2jh.jupyter.org/en/stable/resources/reference.html#hub-networkpolicy-internamespaceaccesslabels). This makes the hub pod's associated NetworkPolicy accept ingress from pods in other namespaces that have specific access labels.

```yaml
hub:
  networkPolicy:
    interNamespaceAccessLabels: accept
```

And then set [`prometheus.server.podLabels`](https://github.com/prometheus-community/helm-charts/blob/0c7bf42ac2265d13845ffe0c499d16e6b8cdedea/charts/prometheus/values.yaml#L554) to be `hub.jupyter.org/network-access-hub: "true"` to enable prometheus to reach the hub.

Alternatively you can also set an explicit ingress rule to allow the prometheus or vmagent pod to reach the hub pod to scrape metrics.

```yaml
hub:
  networkPolicy:
    ingress:
      - from:
          - namespaceSelector:
              matchLabels:
                # namespace where your prometheus or vmagent is running
                name: <namespace>
          - podSelector:
              matchLabels:
                # a valid selector for the pod that needs to reach jupyterhub
                app.kubernetes.io/instance: vmagent
```
