Creating a Kubernetes Cluster
=============================

Kubernetes' `documentation <https://kubernetes.io/docs/setup/pick-right-solution/>`_
describes the many ways to set up a cluster. Here, we shall provide quick
instructions for the most painless and popular ways of getting setup in various
cloud providers.


Setting up Kubernetes on `Google Cloud <https://cloud.google.com/>`_
--------------------------------------------------------------------

`Google Container Engine <https://cloud.google.com/container-engine/>`_
(confusingly abbreviated to GKE) is the simplest and most common way of setting
up a Kubernetes Cluster. You may be able to receive `free credits
<https://cloud.google.com/free/>`_ for trying it out. You will need to
connect your credit card or other payment method to your google cloud account.

1. Go to ``https://console.cloud.google.com``.

2. Click the hamburger icon in the top left (the icon has three horizontal lines
   in one button). Go to “Billing” then “Payment Methods”, and make sure you
   have a credit card linked to the account. (You may also receive $300 in trial
   credits.)

3. Install and initialize the **gcloud command-line tools**. These tools send
   commands to Google Cloud and lets you do things like create and delete
   clusters.

   - Go to the `gcloud downloads page <https://cloud.google.com/sdk/downloads>`_
     to **download and install the gcloud SDK**.
   - See the `gcloud documentation <https://cloud.google.com/sdk/>`_ for
     more information on the gcloud SDK.
   - Install ``kubectl``, which is a tool for controlling kubernetes. From
     the terminal, enter:

     .. code-block:: bash

        gcloud components install kubectl

4. Create a Kubernetes cluster on Google Cloud, by typing in the following
   command:

   .. code-block:: bash

      gcloud container clusters create YOUR_CLUSTER --num-nodes=3 --machine-type=n1-highmem-2 --zone=us-central1-b``

   where:

   * ``--num-nodes`` specifies how many computers to spin up. The higher the
     number, the greater the cost.
   * ``--machine-type`` specifies the amount of CPU and RAM in each node. There
     is a `variety of types <https://cloud.google.com/compute/docs/machine-types>`_
     to choose from.
   * ``--zone`` specifies which computer center to use.  To reduce latency,
     choose a zone closest to whoever is sending the commands. View available
     zones via ``gcloud compute zones list`` .

5. To test if your cluster is initialized, run:

   .. code-block:: bash

      kubectl get node

   The response should list three running nodes.


Setting up Kubernetes on Microsoft Azure Container Service (ACS)
----------------------------------------------------------------

1. Install and initialize the **Azure command-line tools**, which send commands
   to Azure and let you do things like create and delete clusters.

   - Go to the `azure-cli github repo <https://github.com/Azure/azure-cli>`_
     to download and install the **azure-cli** tools.
   - See the `az documentation <https://docs.microsoft.com/en-us/cli/azure/acs>`_
     for more information on using the ``az`` tool with the Azure Container
     Service.

2. Authenticate the ``az`` tool so it may access your Azure account:

   .. code-block:: bash

      az login

3. Specify a `resource group <https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-overview#resource-groups>`_,
   and create one if it doesn't already exist:

  .. code-block:: bash

     export RESOURCE_GROUP=YOUR_RESOURCE_GROUP
     export LOCATION=YOUR_LOCATION
     az group create --name=${RESOURCE_GROUP} --location=${LOCATION}

  where:

  * ``--name`` specifies your Azure resource group. If a group doesn't exist,
    az will create it for you.
  * ``--location`` specifies which computer center to use.  To reduce latency,
    choose a zone closest to whoever is sending the commands. View available
    zones via ``az account list-locations``.

5. Install ``kubectl``, a tool for controlling Kubernetes:

   .. code-block:: bash

      az acs kubernetes install-cli

6. Authenticate kubectl:

   .. code-block:: bash

      az acs kubernetes get-credentials --resource-group=${RESOURCE_GROUP} --name=${CLUSTER_NAME}

7. Create a Kubernetes cluster on Azure, by typing in the following commands:

   .. code-block:: bash

      export CLUSTER_NAME=YOUR_CLUSTER_NAME
      export DNS_PREFIX=YOUR_PREFIX
      az acs create --orchestrator-type=kubernetes --resource-group=${RESOURCE_GROUP} --name=${CLUSTER_NAME} --dns-prefix=${DNS_PREFIX}

  where:

  * ``--resource-group`` specifies your Azure resource group.
  * ``--name`` is your ACS cluster name.
  * ``--dns-prefix`` is the domain name prefix for the cluster.

8. To test if your cluster is initialized, run:

   .. code-block:: bash

      kubectl get node

   The response should list three running nodes.


Next Step
---------

Now that you have a Kubernetes cluster running, it is time to
`set up helm <setup-helm.html>`_.
