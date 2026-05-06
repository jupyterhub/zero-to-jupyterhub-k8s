# JupyterHub Helm chart

[![Documentation](https://img.shields.io/badge/Documentation-z2jh.jupyter.org-blue?logo=read-the-docs&logoColor=white)](https://z2jh.jupyter.org)
[![GitHub](https://img.shields.io/badge/Source_code-github-blue?logo=github&logoColor=white)](https://github.com/jupyterhub/zero-to-jupyterhub-k8s)
[![Discourse](https://img.shields.io/badge/Help_forum-discourse-blue?logo=discourse&logoColor=white)](https://discourse.jupyter.org/c/jupyterhub/z2jh-k8s)
[![Zulip](https://img.shields.io/badge/zulip-join_chat-blue.svg)](https://jupyter.zulipchat.com/#narrow/channel/469744-jupyterhub)
<br>
[![Latest stable release of the Helm chart](https://img.shields.io/badge/dynamic/json.svg?label=Latest%20stable%20release&url=https://hub.jupyter.org/helm-chart/info.json&query=$.jupyterhub.stable&logo=helm&logoColor=white)](https://jupyterhub.github.io/helm-chart#jupyterhub)
[![Latest pre-release of the Helm chart](https://img.shields.io/badge/dynamic/json.svg?label=Latest%20pre-release&url=https://hub.jupyter.org/helm-chart/info.json&query=$.jupyterhub.pre&logo=helm&logoColor=white)](https://jupyterhub.github.io/helm-chart#development-releases-jupyterhub)
[![Latest development release of the Helm chart](https://img.shields.io/badge/dynamic/json.svg?label=Latest%20dev%20release&url=https://hub.jupyter.org/helm-chart/info.json&query=$.jupyterhub.latest&logo=helm&logoColor=white)](https://jupyterhub.github.io/helm-chart#development-releases-jupyterhub)

The JupyterHub Helm chart is accompanied with an installation guide at [z2jh.jupyter.org](https://z2jh.jupyter.org). Together they enable you to deploy [JupyterHub](https://jupyterhub.readthedocs.io) in a Kubernetes cluster that can make Jupyter environments available to several thousands of simultaneous users.

## Configuration

For detailed configuration options, see the [official documentation](https://z2jh.jupyter.org).

### Namespace Override

The chart supports deploying resources to a custom namespace via `namespaceOverride`:

```yaml
namespaceOverride: my-custom-namespace
```

This is particularly useful for ArgoCD deployments or when using this chart as a subchart. See the [configuration reference](https://z2jh.jupyter.org/en/stable/resources/reference.html) for more details.

## History

Much of the initial groundwork for this documentation is information learned from the successful use of JupyterHub and Kubernetes at UC Berkeley in their [Data 8](http://data8.org/) program.

![](https://raw.githubusercontent.com/jupyterhub/zero-to-jupyterhub-k8s/HEAD/docs/source/_static/images/data8_massive_audience.jpg)
