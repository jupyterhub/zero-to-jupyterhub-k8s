.. _microsoft-azure:

Step Zero: Kubernetes on Microsoft Azure Kubernetes Service (AKS) with Autoscaling
----------------------------------------------------------------------------------

.. warning::

  These instructions involve part of the Azure command line that are in preview, hence the following documentation to subject to change.

You can create a Kubernetes cluster `either through the Azure portal website, or using the Azure command line tools <https://docs.microsoft.com/en-us/azure/aks/>`_.

This page describes the commands required to setup a Kubernetes cluster using the command line.
If you prefer to use the Azure portal see the `Azure Kubernetes Service quickstart <https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough-portal>`_.


#. Prepare your Azure shell environment. You have two options, one is to use
   the Azure interactive shell, the other is to install the Azure command-line
   tools locally. Instructions for each are below.

   * **Using the Azure interactive shell**. The `Azure Portal <https://portal.azure.com>`_
     contains an interactive shell that you can use to communicate with your
     Kubernetes cluster. To access this shell, go to `portal.azure.com <https://portal.azure.com>`_
     and click on the button below.

     .. image:: ../_static/images/azure/cli_start.png
        :align: center

    .. note::
       * If you get errors like ``could not retrieve token from local cache``,
         try refreshing your browser window.
       * The first time you do this, you'll be asked to create a storage
         account where your shell filesystem will live.

   * **Install command-line tools locally**. You can access the Azure CLI via
     a package that you can install locally.

     To do so, first follow the `installation instructions
     <https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest>`_ in the
     Azure documentation. Then run the following command to connect your local
     CLI with your account:

     .. code-block:: bash

        az login

     You'll need to open a browser and follow the instructions in your terminal
     to log in.


#. Activate the correct subscription. Azure uses the concept
   of **subscriptions** to manage spending. You can
   get a list of subscriptions your account has access to by running:

   .. code-block:: bash

      az account list --refresh --output table

   Pick the subscription you want to use for creating the cluster, and set that
   as your default.
   If you only have one subscription you can ignore this step.

   .. code-block:: bash

      az account set -s <YOUR-CHOSEN-SUBSCRIPTION-NAME>


#. Setup the CLI for Autoscaling features.
   First install the `aks-preview <https://github.com/Azure/azure-cli-extensions/tree/master/src/aks-preview>`_ CLI extension.
   This will grant access to new commands.

   .. code-block:: bash

     az extension add --name aks-preview

   We then need to register the scale set feature.

   .. code-block:: bash

     az feature register --name VMSSPreview --namespace Microsoft.ContainerService

   A VMSS is a `Virtual Machine Scale Set <https://docs.microsoft.com/en-us/azure/virtual-machine-scale-sets/overview>`_, that is to say an autoscalable set of virtual machines.

   The previous command will take a while to register.
   Use the following command to check it's status.

   .. code-block:: bash

     az feature list \
       --output table \
       --query  "[?contains(name, 'Microsoft.ContainerService/VMSSPreview')].{Name:name,State:properties.state}"

   Once the VMSSPreview feature has been registered, refresh the registration with the following command.

   .. code-block:: bash

     az provider register --namespace Microsoft.ContainerService


#. Create a resource group. Azure uses the concept of
   **resource groups** to group related resources together.
   We need to create a resource group in a given data center location. We will create
   computational resources *within* this resource group.

   .. code-block:: bash

     az group create \
                   --name=<RESOURCE-GROUP-NAME> \
                   --location=<LOCATION> \
                   --output table

   where:

   * ``--name`` specifies the name of your resource group. We recommend using something
     that uniquely identifies this hub. For example, if you are creating a resource group
     for UC Berkeley's 2018 Spring Data100 Course, you may give it a
     ``<RESOURCE-GROUP-NAME>`` of ``ucb_2018sp_data100_hub``.
   * ``--location`` specifies the location of the data center you want your resource to be in.
     For options, see the
     `Azure list of locations that support AKS
     <https://docs.microsoft.com/en-us/azure/aks/container-service-quotas#region-availability>`_.
   * ``--output table`` specifies that the output should be in human readable
     format, rather than the default JSON output. We shall use this with most
     commands when executing them by hand.

   .. note::

       Consider `setting a cloud budget <https://docs.microsoft.com/en-us/partner-center/set-an-azure-spending-budget-for-your-customers>`_
       for your Azure account in order to make sure you don't accidentally
       spend more than you wish to.


#. Choose a cluster name.

   In the following steps we'll run commands that ask you to input a cluster
   name. We recommend using something descriptive and short. We'll refer to
   this as ``<CLUSTER-NAME>`` for the remainder of this section.

   The next step will create a few files on your filesystem, so first create
   a folder in which these files will go. We recommend giving it the same
   name as your cluster::

      mkdir <CLUSTER-NAME>
      cd <CLUSTER-NAME>

#. Create an ssh key to secure your cluster.

   .. code-block:: bash

      ssh-keygen -f ssh-key-<CLUSTER-NAME>

   It will prompt you to add a password, which you can leave empty if you wish.
   This will create a public key named ``ssh-key-<CLUSTER-NAME>.pub`` and a private key named
   ``ssh-key-<CLUSTER-NAME>``. Make sure both go into the folder we created earlier,
   and keep both of them safe!

   .. note::

      This command will also print out something to your terminal screen. You
      don't need to do anything with this text.


#. Create an AKS cluster.

   The following command will request a Kubernetes cluster within the resource
   group that we created earlier.

   .. code-block:: bash

      az aks create --name <CLUSTER-NAME> \
                    --resource-group <RESOURCE-GROUP-NAME> \
                    --ssh-key-value ssh-key-<CLUSTER-NAME>.pub \
                    --node-count 3 \
                    --node-vm-size Standard_D2s_v3 \
                    --enable-vmss \
                    --enable-cluster-autoscaler \
                    --min-count 3 \
                    --max-count 6 \
                    --kubernetes-version 1.12.7 \
                    --output table

   where:

   * ``--name`` is the name you want to use to refer to your cluster
   * ``--resource-group`` is the ResourceGroup you created in step 4
   * ``--ssh-key-value`` is the ssh public key created in step 6
   * ``--node-count`` is the number of nodes you want in your Kubernetes cluster
   * ``--node-vm-size`` is the size of the nodes you want to use, which varies based on
     what you are using your cluster for and how much RAM/CPU each of your users need.
     There is a `list of all possible node sizes <https://docs.microsoft.com/en-us/azure/cloud-services/cloud-services-sizes-specs>`_
     for you to choose from, but not all might be available in your location.
     If you get an error whilst creating the cluster you can try changing either the region or the node size.
   * ``--enable-vmss`` deploys the cluster as a scale set.
   * ``--enable-cluster-autoscaler`` installs a `Cluster Autoscaler <https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler>`_ onto the cluster (though counterintuitively, does not enable it!).
   * ``--min-count``/``--max-count`` are the minimum/maximum number of nodes in the cluster at any time.
   * ``--kubernetes-version`` installs a specific version of Kubernetes onto the cluster. To autoscale, we require ``>= v 1.12.4``.

   This should take a few minutes and provide you with a working Kubernetes cluster!


#. If you're using the Azure CLI locally, install `kubectl <https://kubernetes.io/docs/reference/kubectl/overview/>`_, a tool
   for accessing the Kubernetes API from the commandline:

   .. code-block:: bash

      az aks install-cli

   Note: kubectl is already installed in Azure Cloud Shell.


#. Get credentials from Azure for ``kubectl`` to work:

   .. code-block:: bash

      az aks get-credentials \
                   --name <CLUSTER-NAME> \
                   --resource-group <RESOURCE-GROUP-NAME> \
                   --output table

   where:

   * ``--name`` is the name you gave your cluster in step 5
   * ``--resource-group`` is the ResourceGroup you created in step 4

   This automatically updates your Kubernetes client configuration file.


#. Check if your cluster is fully functional

   .. code-block:: bash

      kubectl get node

   The response should list three running nodes and their Kubernetes versions!
   Each node should have the status of ``Ready``, note that this may take a
   few moments.


#. Enabling Autoscaling

   We now move to the Azure Portal to enable autoscaling and set rules to manage the Cluster Autoscaler.

   First we need to register `Microsoft Insights <https://docs.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview>`_ for use on the active subscription.

   .. code-block:: bash

     az provider register --namespace microsoft.insights

   To check the status of the registration, run the following command:

   .. code-block:: bash

     az provider show -n microsoft.insights

   Once the application has been registered, navigate to your active subscription on the `Portal <https://portal.azure.com/>`_.

   Under "Resources", select the VMSS.
   It should be named something like ``aks-nodepool1-<random-str>-vmss``.

   .. image:: ../_static/images/azure/select_vmss.png
      :align: center

   From the left-hand menu, select "Scaling".
   Click the blue "Enable autoscaling" button and an autogenerated form for a scale condition will appear.
   We will add two new rules to this condition:

   * Increase the instance count by 1 when the average CPU usage over 10 minutes is greater than 70%
   * Decrease the instance count by 1 when the average CPU usage over 10 minutes is less than 5%

   .. image:: ../_static/images/azure/scale_condition.png
      :align: center

   Make sure the "Scale based on metric" option is selected and click "+ Add new rule", another autogenerated form will appear.
   This will be pre-filled with the required settings to fulfill our first rule, so save it by clicking "Update" and click "+ Add new rule" again.

   .. image:: ../_static/images/azure/scale_out.png
      :align: center

   The second form needs to be edited for the second rule to decrease the instance count by 1 when the average CPU usage over 10 minutes is less than 5%.
   Save this rule and then save the overall scale condition, the cluster will be updated automatically.

   .. image:: ../_static/images/azure/scale_in.png
      :align: center

   .. note::

     This form can also be used to change ``--node-count``/``--min-count``/``--max-count`` that was set in step 7 by using the "Instance limits" section of the scale condition ("Default", "Minimum" and "Maximum" respectively).

     If you prefer to use the command line, you can run the following:

       .. code-block:: bash

         az aks update \
           --name <CLUSTER-NAME> \
           --resource-group <RESOURCE-GROUP> \
           --update-cluster-autoscaler \
           --min-count <DESIRED-MINIMUM-COUNT> \
           --max-count <DESIRED-MAXIMUM-COUNT> \
           --output table

     **Both** ``--min-count`` and ``--max-count`` must be defined.


.. note::

   If you create the cluster using the Azure Portal you must enable RBAC.
   RBAC is enabled by default when using the command line tools.

Congrats. Now that you have your Kubernetes cluster running, it's time to
begin :ref:`creating-your-jupyterhub`.

.. _Azure resource group: https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-overview#resource-groups
