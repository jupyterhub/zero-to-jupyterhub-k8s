(extending-jupyterhub)=

# Customizing your Deployment

The Helm chart used to install your JupyterHub deployment has a lot of options
for you to tweak. For a semi-complete reference list of the options, see the
{ref}`helm-chart-configuration-reference`.

(apply-config-changes)=

## Applying configuration changes

The general method to modify your Kubernetes deployment is to:

1. Make a change to your `config.yaml`.
2. Run a `helm upgrade`:

   ```
   helm upgrade --cleanup-on-fail \
     <helm-release-name> jupyterhub/jupyterhub \
     --namespace <k8s-namespace> \
     --version=<chart-version> \
     --values config.yaml
   ```

   Note that `helm list` should display `<YOUR_RELEASE_NAME>` if you forgot it.

3. Verify that the _hub_ and _proxy_ pods entered the `Running` state after
   the upgrade completed.

   ```
   NAMESPACE=jhub

   kubectl get pod --namespace $NAMESPACE
   ```

For information about the many things you can customize with changes to your
Helm chart through values provided to its templates through `config.yaml`, see
the {ref}`customization-guide`.
