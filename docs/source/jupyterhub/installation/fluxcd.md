(flux-cd)=

# Installing JupyterHub Using FluxCD

## Why FluxCD for JupyterHub?

Running JupyterHub can often result in significant infrastructure overhead, especially for data science and data engineering teams. Provisioning and managing compute resources, dependencies, and ensuring high availability can be time-consuming and error-prone.

With FluxCD, you can have everything - from configuration to state - maintained in your Git repositories. This means that all configuration changes are version-controlled, providing a single source of truth for your JupyterHub deployment.

FluxCD automates the deployment and management of JupyterHub infrastructure, reducing manual effort and minimizing the risk of misconfigurations. Whether it's scaling resources up or down, FluxCD handles it seamlessly, providing a hassle-free experience for teams.Implementing continuous delivery practices with FluxCD enables automated deployment pipelines for JupyterHub. This ensures faster and more reliable delivery of updates and enhancements to your JupyterHub environment, empowering data science and data engineering teams to focus more on their work and less on infrastructure management.

## Prerequisites and Setting Up FluxCD

Before setting up FluxCD and deploying JupyterHub, ensure you have the following prerequisites:

1. **Access to Your Kubernetes Cluster:**
   Make sure you have access to your Kubernetes cluster, whether it's on EKS, AKS, GKE, or any other Kubernetes distribution.

2. **FluxCLI:**
   Install FluxCLI on your local machine. You can refer to the [official Flux documentation](https://fluxcd.io/flux/get-started/) for installation instructions.

3. **Repositories Setup:**
   Ensure you have repositories set up where you'll maintain the code to be bootstrapped with FluxCD. This could be on GitLab, GitHub or any other version control platform.You can follow the steps outlined in the [FluxCD documentation](https://fluxcd.io/flux/installation/bootstrap/) to set up your repositories with FluxCD.

4. **Repository Structure:**
   Consider how you want to structure your repositories based on your use case and interaction frequency with the infrastructure. For a simple structure, you can have all three required YAML files (Kustomization, HelmRelease, and HelmRepo) under one directory. This straightforward approach simplifies management and organization.If your use case demands more complexity or if you anticipate frequent changes to the infrastructure, you may opt for a more layered or modular structure. This could involve separate directories ( apps, infra, clusters) for different kustomize overlays of your infrastructure, with each repository containing its own set of configuration files and manifests.

   For more guidance on repository structure options, refer to the [FluxCD documentation on repository structure](https://fluxcd.io/flux/guides/repository-structure/).

   ## Install JupyterHub

   For the base installation of JupyterHub, you can refer to the template FluxCD files located in the `jupyterhub/templates/fluxcd/baseinstall` directory of this repository. These template files provide a starting point for deploying JupyterHub using FluxCD.

   **Basic Configuration YAMLs for Installing JupyterHub with FluxCD:**

   1. **HelmRepository YAML:**

   - Defines the Helm chart repository source for JupyterHub.

   ```yaml
   apiVersion: source.toolkit.fluxcd.io/v1beta1
   kind: HelmRepository
   metadata:
     name: jupyterhub
     namespace: flux-system
   spec:
     interval: 1m
     url: "https://jupyterhub.github.io/helm-chart/"
   ```

   **Where:** This YAML defines a HelmRepository named "jupyterhub" in the "flux-system" namespace. It specifies the URL of the Helm chart repository for JupyterHub and sets the interval for checking for updates to 1 minute.

   2. **HelmRelease YAML:**

   - Deploys JupyterHub using the Helm chart obtained from the HelmRepository.

   ```yaml
   apiVersion: helm.toolkit.fluxcd.io/v2beta1
   kind: HelmRelease
   metadata:
     name: jupyterhub
     namespace: flux-system
   spec:
     interval: 5m
     releaseName: jupyterhub
     targetNamespace: jupyter
     chart:
     spec:
       chart: jupyterhub
       version: "X.X.X"
       sourceRef:
       kind: HelmRepository
       name: jupyterhub
       namespace: flux-system
   ```

   **Where:** This YAML defines a HelmRelease named "jupyterhub" in the "flux-system" namespace. It specifies the Helm chart to be deployed, including its version, obtained from the "jupyterhub" HelmRepository. It sets the interval for checking for updates to 5 minutes and deploys JupyterHub to the "jupyter" namespace.

   3. **Kustomization YAML:**

   - Manages the customization of the deployment, including additional configurations or resources.

   ```yaml
   apiVersion: kustomize.config.k8s.io/v1beta1
   kind: Kustomization
   resources:
     - jupyterhub-repo.yaml
     - jupyterhub-release.yaml
   ```

   **Where:** This YAML defines a Kustomization resource that includes the YAML files for the HelmRepository and HelmRelease. It specifies the resources to be managed by Kustomize for generating the final set of Kubernetes resources.

   These YAML files provide the basic configuration for deploying JupyterHub using FluxCD. Customize them as needed for your specific deployment requirements.

   **Push to Git Repository:**
   Once you've configured these YAML files, push them to your Git repository that you have bootstrapped with your Kubernetes cluster. FluxCD will automatically detect and apply changes from the Git repository to your cluster.

   Certainly! Here's the updated section:

   **Post-Deployment Steps:**

   After pushing all YAML files to your Git repository that you have bootstrapped with your Kubernetes cluster, you can check the deployment and access JupyterHub using the following steps:

   1. **Check Pod Status:**
      Monitor the creation of pods by entering the following command in a separate terminal:

   ```bash
   kubectl get pod --namespace <k8s-namespace>
   ```

   _Replace `<k8s-namespace>` with the namespace you used for the deployment._

   2. **Enable kubectl Autocompletion:**
      To remain sane, we recommend enabling autocompletion for kubectl. Follow the kubectl installation instructions for your platform to find the shell autocompletion instructions. Additionally, set a default value for the `--namespace` flag with the following command:

   ```bash
   kubectl config set-context $(kubectl config current-context) --namespace <k8s-namespace>
   ```

   3. **Wait for Pods to Enter Running State:**
      Wait for the hub and proxy pods to enter the Running state. You can use the following command to monitor their status:

   ```bash
   kubectl get pod --namespace <k8s-namespace>
   ```

   _Replace `<k8s-namespace>` with the namespace you used for the deployment._

   Example output:

   ```
   NAME                    READY     STATUS    RESTARTS   AGE
   hub-5d4ffd57cf-k68z8    1/1       Running   0          37s
   proxy-7cb9bc4cc-9bdlp   1/1       Running   0          37s
   ```

   4. **Find External IP:**
      Once the pods are running, find the external IP that you can use to access JupyterHub. Run the following command until the `EXTERNAL-IP` of the `proxy-public` service is available:

   ```bash
   kubectl --namespace <k8s-namespace> get service proxy-public
   ```

   _Replace `<k8s-namespace>` with the namespace you used for the deployment._

   Or, use the short form:

   ```bash
   kubectl --namespace <k8s-namespace> get service proxy-public --output jsonpath='{.status.loadBalancer.ingress[].ip}'
   ```

   5. **Access JupyterHub:**
      To use JupyterHub, enter the external IP for the `proxy-public` service into a browser. JupyterHub is running with a default dummy authenticator, so entering any username and password combination will let you enter the hub.

   Congratulations! Now that you have basic JupyterHub running, you can {ref}`extend it <extending-jupyterhub>` and {ref}`optimize it <optimization>` in many
   ways to meet your needs.
