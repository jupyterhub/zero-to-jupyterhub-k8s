# Installing JupyterHub

Installing JupyterHub offers two primary methods: Helm and GitOps tools like FluxCD, ArgoCD. The choice between these methods depends on the specific requirements of your team and deployment scenario. If you're setting up JupyterHub for a limited number of users or for simpler deployments, installing via Helm may be the preferred option. Helm provides a straightforward installation process with minimal configuration. On the other hand, for larger, multi-user teams or complex deployment environments, utilizing GitOps tools such as FluxCD, ArgoCD can significantly streamline infrastructure management. FluxCD automates the deployment and maintenance of JupyterHub, ensuring consistency and reliability through version-controlled manifests. Consider the size of your team and the complexity of your deployment environment when choosing between Helm and GitOps tools for installing JupyterHub.

```{toctree}
:maxdepth: 2
:caption: Installing JupyterHub

installation/helm
installation/fluxcd
```
