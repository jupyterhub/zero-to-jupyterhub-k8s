Creating a Kubernetes Cluster
=============================

Kubernetes has `pretty good documentation <https://kubernetes.io/docs/setup/pick-right-solution/>`_ on the very large number of ways you can setup a cluster. Here, we shall provide quick instructions for the most painless & popular ways of getting setup in various cloud providers.


Setting up Kubernetes on `Google Cloud <https://cloud.google.com/>`_
--------------------------------------------------------------------

`Google Container Engine <https://cloud.google.com/container-engine/>`_ (confusingly abbreviated to GKE) is the simplest & most common way of setting up a Kubernetes Cluster. You should be able to get `free credits <https://cloud.google.com/free/>`_ for trying it out. However, first you need to connect your credit card to your google cloud account.

1. Go to https://console.cloud.google.com.
2. Click the hamburger in the top left (it has 3 horizontal lines in one button). Go to “Billing” then “Payment Methods”, and make sure you have a credit card linked to the account. (you should also get $300 in credits).
3. Install and initialize the gcloud command-line tools, which send commands to google cloud and lets you do things like create / delete clusters.
   
   - Go to the `gcloud downloads page <https://cloud.google.com/sdk/downloads>`_
     to download/install the gcloud SDK.
   - See the `gcloud documentation <https://cloud.google.com/sdk/>`_ for
     more information on the gcloud SDK.
   - Install ``kubectl``, which is a tool for controlling kubernetes.

         ``gcloud components install kubectl``

4. Create a kubernetes cluster on google cloud, by typing in the following command.

    ``gcloud container clusters create YOUR_CLUSTER --num-nodes=3 --machine-type=n1-highmem-2 --zone=us-central1-b``

  * ``--num-nodes`` specifies how many computers to spin up. The higher the number, the greater the cost.
  * ``--machine-type`` specifies the amount of CPU and RAM in each node. There is a `large variety <https://cloud.google.com/compute/docs/machine-types>`_  to choose from.
  * ``--zone`` specifies which computer center to use.  To reduce latency, choose a zone closest to whoever is sending the commands. View available zones via `gcloud compute zones list` .
  * When it’s done initializing your cluster, run ``kubectl get node``. It should list three running nodes.

Setting up kubernetes on Microsoft Azure Container Service (ACS)
----------------------------------------------------------------

1. Install and initialize the Azure command-line tools, which send commands to Azure and let you do things like create and delete clusters.

   - Go to the `azure-cli github repo <https://github.com/Azure/azure-cli>`_
     to download/install the program.
   - See the `az documentation <https://docs.microsoft.com/en-us/cli/azure/acs>`_ for more information on using the tool with the Azure Container Service.

2. Authenticate the az tool so that it has access to your Azure account:

    .. code::

        az login

3. Specify a `resource group <https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-overview#resource-groups>_`, and create it if it doesn't already exist:

    .. code-block:: bash

        export RESOURCE_GROUP=YOUR_RESOURCE_GROUP
        export LOCATION=YOUR_LOCATION
        az group create --name=${RESOURCE_GROUP} --location=${LOCATION}

  * ``--name`` specifies your Azure resource group. If this doesn't exist, az will create it for you.
  * ``--location`` specifies which computer center to use.  To reduce latency, choose a zone closest to whoever is sending the commands. View available zones via `az account list-locations`.

5. Install ``kubectl``, a tool for controlling kubernetes:

    .. code::

        az acs kubernetes install-cli

6. Authenticate kubectl:

    .. code::

        az acs kubernetes get-credentials --resource-group=${RESOURCE_GROUP} --name=${CLUSTER_NAME}

7. Create a kubernetes cluster on Azure, by typing in the following commands:

    .. code-block:: bash

        export CLUSTER_NAME=YOUR_CLUSTER_NAME
        export DNS_PREFIX=YOUR_PREFIX
        az acs create --orchestrator-type=kubernetes --resource-group=${RESOURCE_GROUP} --name=${CLUSTER_NAME} --dns-prefix=${DNS_PREFIX}


  * ``--resource-group`` specifies your Azure resource group.
  * ``--name`` is your ACS cluster name.
  * ``--dns-prefix`` is the domain name prefix for the cluster.

  * When it’s done initializing your cluster, run ``kubectl get node``. It should list three running nodes.


Next Step
---------

Now that you have a kubernetes cluster running, it is time to `set up helm <setup-helm.html>`_.
