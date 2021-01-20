(uninstall-jupyterhub)=

# Uninstalling JupyterHub

When you are done with your hub, you should delete it so you are no longer
paying money for it. The following sections describe how to delete your
JupyterHub deployment and associated cloud resources on various cloud providers.

Tearing down your JupyterHub entails:

1. Deleting your Kubernetes namespace, which deletes all objects created and
   managed by Kubernetes in it.
2. Deleting any cloud resources you've requested from the cloud provider.
3. Running a final check to make sure there aren't any lingering resources that
   haven't been deleted (e.g., storage volumes in some cloud providers).

## For all cloud providers

(delete-namespace)=

### Delete the helm release

The steps in this section must be performed for all cloud providers first,
before doing the cloud provider specific setup.

1. First, delete the Helm release. This deletes all resources that were created
   by Helm for your JupyterHub deployment.

   ```bash
   helm delete <YOUR-HELM-RELEASE-NAME>
   ```

   `<YOUR-HELM-RELEASE-NAME>` is the name provided to `helm upgrade` when
   initially setting up the hub. If you had forgotten what you used, you
   can run `helm list` to find all the release names in your cluster.
   You can also see the `namespace` value here that will be used in the next step.

2. Next, delete the Kubernetes namespace the hub was installed in. This deletes
   any disks that may have been created to store user's data, and any IP
   addresses that may have been provisioned.

   ```bash
   kubectl delete namespace <YOUR-NAMESPACE>
   ```

## Google Cloud Platform

1. Perform the steps in {ref}`delete-namespace`. These cloud provider agnostic
   steps will delete the Helm release and the Kubernetes namespace. This must be
   done before proceeding.
2. Delete the Kubernetes cluster. You can list all the clusters you have.

   ```
   gcloud container clusters list
   ```

   You can then delete the one you want.

   ```
   gcloud container clusters delete <CLUSTER-NAME> --zone=<CLUSTER-ZONE>
   ```

3. Double check to make sure all the resources are now deleted, since anything you
   have not deleted will cost you money! You can check the [web console](https://console.cloud.google.com)
   (make sure you are in the right project and account) to verify that everything
   has been deleted.

   At a minimum, check the following under the Hamburger (left top corner) menu:

   1. Compute -> Compute Engine -> Disks
   2. Compute -> Kubernetes Engine -> Clusters
   3. Tools -> Container Registry -> Images
   4. Networking -> Network Services -> Load Balancing

   These might take several minutes to clear up, but they shouldn't have anything
   related to your JupyterHub cluster after you have deleted the cluster.

## Microsoft Azure AKS

1. Perform the steps in {ref}`delete-namespace`. These cloud provider agnostic
   steps will delete the Helm release and the Kubernetes namespace. This must be
   done before proceeding.
2. Delete your resource group. You can list your active resource groups with
   the following command

   ```
   az group list --output table
   ```

   You can then delete the one you want with the following command

   ```
   az group delete --name <YOUR-GROUP-NAME>
   ```

   Be careful to delete the correct Resource Group, as doing so will irreversibly
   delete all resources within the group!

3. Double check to make sure all the resources are now deleted, since anything you
   have not deleted will cost you money! You can check the [web portal](https://portal.azure.com)
   (check the "Resource Groups" page) to verify that everything has been deleted.

   These might take several minutes to clear up, but they shouldn't have anything
   related to your JupyterHub cluster after you have deleted the resource group.

## Amazon Web Services (AWS)

1. Perform the steps in {ref}`delete-namespace`. These cloud provider agnostic
   steps will delete the Helm release and the Kubernetes namespace. This must be
   done before proceeding.
2. on CI host:

   ```bash
   kops delete cluster <CLUSTER-NAME> --yes

   # Leave CI host
   exit

   # Terminate CI host
   aws ec2 stop-instances --instance-ids <aws-instance id of CI host>
   aws ec2 terminate-instances --instance-ids <aws-instance id of CI host>
   ```

```{note}
* `<CLUSTER NAME>` should be `<SOME NAME>.k8s.local`.
* Stopping the CI host will still incur disk storage and IP address costs,
  but the host can be restarted at a later date.
* Sometimes AWS fails to delete parts of the stack on a first pass. Be sure
  to double-check that your stack has in fact been deleted, and re-perform
  the actions above if needed.
```
