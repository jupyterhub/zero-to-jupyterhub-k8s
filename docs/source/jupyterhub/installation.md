(quick-install)=

# Installing JupyterHub

With a {doc}`Kubernetes cluster </kubernetes/setup-kubernetes>` available
and {doc}`Helm </kubernetes/setup-helm>` installed, we can install JupyterHub
in the Kubernetes cluster using the JupyterHub Helm chart.

## Initialize a Helm chart configuration file

Helm charts' contain {term}`templates <Helm template>` that can be rendered to
the {term}`Kubernetes resources <Kubernetes resource>` to be installed. A user
of a Helm chart can override the chart's default values to influence how the
templates render.

In this step we will initialize a chart configuration file for you to adjust
your installation of JupyterHub. We will name and refer to it as `config.yaml`
going onwards.

```{admonition} Introduction to YAML
If you haven't worked with YAML before, investing some
minutes [learning about it](https://www.youtube.com/watch?v=cdLNKUoMc6c)
will likely be worth your time.
```

As of version 1.0.0, you don't need any configuration to get started so you can
just create a `config.yaml` file with some helpful comments.

```yaml
# This file can update the JupyterHub Helm chart's default configuration values.
#
# For reference see the configuration reference and default values, but make
# sure to refer to the Helm chart version of interest to you!
#
# Introduction to YAML:     https://www.youtube.com/watch?v=cdLNKUoMc6c
# Chart config reference:   https://zero-to-jupyterhub.readthedocs.io/en/stable/resources/reference.html
# Chart default values:     https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/HEAD/jupyterhub/values.yaml
# Available chart versions: https://hub.jupyter.org/helm-chart/
#
```

In case you are working from a terminal and are unsure how to create this file,
can try with `nano config.yaml`.

## Install JupyterHub

1. Make Helm aware of the [JupyterHub Helm chart repository](https://hub.jupyter.org/helm-chart/) so you can install the
   JupyterHub chart from it without having to use a long URL name.

   ```
   helm repo add jupyterhub https://hub.jupyter.org/helm-chart/
   helm repo update
   ```

   This should show output like:

   ```
   Hang tight while we grab the latest from your chart repositories...
   ...Skip local chart repository
   ...Successfully got an update from the "stable" chart repository
   ...Successfully got an update from the "jupyterhub" chart repository
   Update Complete. ⎈ Happy Helming!⎈
   ```

2. Now install the chart configured by your `config.yaml` by running this
   command from the directory that contains your `config.yaml`:

   ```
   helm upgrade --cleanup-on-fail \
     --install <helm-release-name> jupyterhub/jupyterhub \
     --namespace <k8s-namespace> \
     --create-namespace \
     --version=<chart-version> \
     --values config.yaml
   ```

   where:

   - `<helm-release-name>` refers to a [Helm release name](https://helm.sh/docs/glossary/#release), an identifier used to
     differentiate chart installations. You need it when you are changing or
     deleting the configuration of this chart installation. If your Kubernetes
     cluster will contain multiple JupyterHubs make sure to differentiate them.
     You can list your Helm releases with `helm list`.
   - `<k8s-namespace>` refers to a [Kubernetes namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/),
     an identifier used to group Kubernetes resources, in this case all
     Kubernetes resources associated with the JupyterHub chart. You'll need the
     namespace identifier for performing any commands with `kubectl`.
   - This step may take a moment, during which time there will be no output
     to your terminal. JupyterHub is being installed in the background.
   - If you get a `release named <helm-release-name> already exists` error, then
     you should delete the release by running `helm delete <helm-release-name>`.
     Then reinstall by repeating this step. If it persists, also do `kubectl delete namespace <k8s-namespace>` and try again.
   - In general, if something goes _wrong_ with the install step, delete the
     Helm release by running `helm delete <helm-release-name>`
     before re-running the install command.
   - If you're pulling from a large Docker image you may get a
     `Error: timed out waiting for the condition` error, add a
     `--timeout=<number-of-minutes>m` parameter to the `helm` command.
   - The `--version` parameter corresponds to the _version of the Helm
     chart_, not the version of JupyterHub. Each version of the JupyterHub
     Helm chart is paired with a specific version of JupyterHub. E.g.,
     `0.11.1` of the Helm chart runs JupyterHub `1.3.0`.
     For a list of which JupyterHub version is installed in each version
     of the JupyterHub Helm Chart, see the [Helm Chart repository](https://hub.jupyter.org/helm-chart/).

3. While Step 2 is running, you can see the pods being created by entering in
   a different terminal:

   ```
   kubectl get pod --namespace <k8s-namespace>
   ```

   To remain sane we recommend that you enable autocompletion for kubectl
   (follow [the kubectl installation instructions for your platform](https://kubernetes.io/docs/tasks/tools/#kubectl)
   to find the shell autocompletion instructions)

   and set a default value for the `--namespace` flag:

   ```
   kubectl config set-context $(kubectl config current-context) --namespace <k8s-namespace>
   ```

4. Wait for the _hub_ and _proxy_ pod to enter the `Running` state.

   ```
   NAME                    READY     STATUS    RESTARTS   AGE
   hub-5d4ffd57cf-k68z8    1/1       Running   0          37s
   proxy-7cb9bc4cc-9bdlp   1/1       Running   0          37s
   ```

5. Find the IP we can use to access the JupyterHub. Run the following
   command until the `EXTERNAL-IP` of the `proxy-public` [service](https://kubernetes.io/docs/concepts/services-networking/service/)
   is available like in the example output.

   ```
   kubectl --namespace <k8s-namespace> get service proxy-public
   ```

   ```
   NAME           TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)        AGE
   proxy-public   LoadBalancer   10.51.248.230   104.196.41.97   80:31916/TCP   1m
   ```

   Or, use the short form:

   ```
   kubectl --namespace <k8s-namespace> get service proxy-public --output jsonpath='{.status.loadBalancer.ingress[].ip}'
   ```

6. To use JupyterHub, enter the external IP for the `proxy-public` service in
   to a browser. JupyterHub is running with a default _dummy_ authenticator so
   entering any username and password combination will let you enter the hub.

Congratulations! Now that you have basic JupyterHub running, you can {ref}`extend it <extending-jupyterhub>` and {ref}`optimize it <optimization>` in many
ways to meet your needs.

Some examples of customizations are:

- Configure the login to use the account that makes sense to you (Google, GitHub, etc.).
- Use a suitable pre-built image for the user container or build your own.
- Host it on <https://your-domain.com>.
