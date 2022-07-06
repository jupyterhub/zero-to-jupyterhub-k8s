(ibm-cloud)=

# Kubernetes on IBM Cloud

This guide shows how to deploy JupyterHub on the IBM Cloud using their [Kubernetes service](https://cloud.ibm.com/kubernetes/catalog/create)).
It should provide you with enough knowledge to create a cluster, deploy your application using a Docker image and use a custom domain to use the deployed app.

Before you begin:

- Understand the [Kubernetes basics][https://kubernetes.io/docs/tutorials/kubernetes-basics/].
- Install the IBM Cloud Developer Tools
  - Install the [IBM Cloud CLI](https://cloud.ibm.com/docs/cli?topic=cloud-cli-getting-started).
    - `curl -sL https://ibm.biz/idt-installer | bash`
    - Verify your installation
    - `ibmcloud dev help`
    - Connect to the proper IBM API endpoint for your IBM Cloud location. Example:
    - `ibmcloud api https://api.ng.bluemix.net`
    - Log in to IBM Cloud using your IBMid
    - `ibmcloud login`. Use the `--sso` option to log in using your federated ID.
    - Set up your org and space
    - `ibmcloud target --cf`

To follow this guide, you can use a **free** cluster. You can also use a **paid** cluster of type **standard** on IBM Cloud.

Procedure:

1. Create a Kubernetes cluster
   Kubernetes Service delivers powerful tools by combining Docker and Kubernetes technologies, an intuitive user experience, and built-in security and isolation to automate the deployment, operation, scaling, and monitoring of containerized apps in a cluster of computing hosts.

   To set up the Kubernetes cluster:

   1. Create a Kubernetes cluster from the [IBM Cloud catalog](https://cloud.ibm.com/kubernetes/catalog/create)).
   2. When configuring the new cluster, select the **Cluster type** and click **Create Cluster** to provision a Kubernetes cluster.
      2.1 In the case of a free cluster you will see something similar to:

      ```{image} ../../_static/images/ibm/create-free-kubernetes-cluster-ibm-cloud.png
      :align: center
      ```

      2.2 In the case of a paid cluster you will see something similar to:

      ```{image} ../../_static/images/ibm/create-paid-kubernetes-cluster-ibm-cloud.png
      :align: center
      ```

   3. Check the status of your **Cluster** and **Worker Nodes** and wait for them to be **ready**.

   Or, if you prefer, create the cluster using the [IBM Cloud CLI tools](https://cloud.ibm.com/docs/containers?topic=containers-cs_cli_install))

2. Configure kubectl
   [kubectl](https://kubernetes.io/docs/reference/kubectl/) is a CLI tool to interact with a Kubernetes cluster. In this occasion, you will use it to point forward to the created Kubernetes cluster.

   1. Use `ibmcloud login` to log in interactively into the IBM Cloud. Provide the organization (org), location and space under which the cluster is created. You can reconfirm the details by running `ibmcloud target` command.
   2. When the cluster is ready, retrieve the cluster configuration by using the cluster's name:
      ```
      ibmcloud cs cluster-config <clusterName>
      ```
   3. Copy and paste the **export** command to set the KUBECONFIG environment variable as directed. The command should be something similar to:

      ```
      export KUBECONFIG=/Users/user/.bluemix/plugins/container-service/clusters/JupyterHub/kube-config-***-JupyterHub.yml
      ```

      To verify whether the KUBECONFIG environment variable is set correctly or not, run the following command:

      ```
      echo $KUBECONFIG
      ```

   4. Check that the `kubectl` command is correctly configured

      ```
      kubectl cluster-info
      ```

      ```{image} ../../_static/images/ibm/kubectl-cluster-info.png
      :align: center
      ```

Hooray! You have your Kubernetes cluster running; it's time to begin {ref}`setup-helm`.

More info and readings:

- <https://cloud.ibm.com/docs/tutorials?topic=solution-tutorials-scalable-webapp-kubernetes>
- <https://github.com/IBM-Cloud/get-started-python>
