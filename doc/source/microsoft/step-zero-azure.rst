.. _microsoft-azure:

Step Zero: Kubernetes on Microsoft Azure Kubernetes Service (AKS)
-----------------------------------------------------------------

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


#. Create a resource group. Azure uses the concept of
   **resource groups** to group related resources together.
   We need to create a resource group in a given data center location. We will create
   computational resources *within* this resource group.

   .. code-block:: bash

     az group create \
                   --name=<RESOURCE-GROUP-NAME> \
                   --location=centralus \
                   --output table

   where:

   * ``--name`` specifies the name of your resource group. We recommend using something
     that uniquely identifies this hub. For example, if you are creating a resource group
     for UC Berkeley's 2018 Spring Data100 Course, you may give it a
     ``<RESOURCE-GROUP-NAME>`` of ``ucb_2018sp_data100_hub``.
   * ``--location`` specifies the location of the data center you want your resource to be in.
     In this case, we used the ``centralus`` location. For other options, see the
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
                    --output table

   where:

   * ``--name`` is the name you want to use to refer to your cluster
   * ``--resource-group`` is the ResourceGroup you created in step 4
   * ``--ssh-key-value`` is the ssh public key created in step 7
   * ``--node-count`` is the number of nodes you want in your Kubernetes cluster
   * ``--node-vm-size`` is the size of the nodes you want to use, which varies based on
     what you are using your cluster for and how much RAM/CPU each of your users need.
     There is a `list of all possible node sizes <https://docs.microsoft.com/en-us/azure/cloud-services/cloud-services-sizes-specs>`_
     for you to choose from, but not all might be available in your location.
     If you get an error whilst creating the cluster you can try changing either the region or the node size.
   * This will install the default version of Kubernetes. You can pass ``--kubernetes-version`` to install a different version.

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

   * ``--name`` is the name you gave your cluster in step 7
   * ``--resource-group`` is the ResourceGroup you created in step 4

   This automatically updates your Kubernetes client configuration file.

#. Check if your cluster is fully functional

   .. code-block:: bash

      kubectl get node

   The response should list three running nodes and their Kubernetes versions!
   Each node should have the status of ``Ready``, note that this may take a
   few moments.

.. note::

   If you create the cluster using the Azure Portal you must enable RBAC.
   RBAC is enabled by default when using the command line tools.

Congrats. Now that you have your Kubernetes cluster running, it's time to
begin :ref:`creating-your-jupyterhub`.

.. _Azure resource group: https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-overview#resource-groups
