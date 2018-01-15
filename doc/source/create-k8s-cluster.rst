.. _create-k8s-cluster:

Creating a Kubernetes Cluster
=============================

Kubernetes' documentation describes the many `ways to set up a cluster`_.
Here, we shall provide quick instructions for the most painless and
popular ways of getting setup in various cloud providers:

- :ref:`Google Cloud <google-cloud>`
- :ref:`Microsoft Azure <microsoft-azure>`
- :ref:`Amazon AWS <amazon-aws>`
- Red Hat OpenShift
- Others

.. note::

   * During the process of setting up JupyterHub, you'll be creating some
     files for configuration purposes. It may be helpful to create a folder
     for your JuypterHub deployment to keep track of these files.

   * If you are concerned at all about security (you probably should be), see
     the `Kubernetes best-practices guide <http://blog.kubernetes.io/2016/08/security-best-practices-kubernetes-deployment.html>`_
     for information about keeping your Kubernetes infrastructure secure.

.. _google-cloud:

Setting up Kubernetes on `Google Cloud <https://cloud.google.com/>`_
--------------------------------------------------------------------

`Google Kubernetes Engine <https://cloud.google.com/kubernetes-engine/>`_
(GKE) is the simplest and most common way of setting
up a Kubernetes Cluster. You may be able to receive `free credits
<https://cloud.google.com/free/>`_ for trying it out. You will need to
connect your credit card or other payment method to your google cloud account.

1. Go to ``https://console.cloud.google.com`` and log in.

2. Enable the `Kubernetes Engine API <https://console.cloud.google.com/apis/api/container.googleapis.com/overview>`_.

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

      gcloud container clusters create <YOUR_CLUSTER> \
          --num-nodes=3 \
          --machine-type=n1-standard-2 \
          --zone=us-central1-b \
          --cluster-version=1.8.4-gke.1

   where:

   * ``--num-nodes`` specifies how many computers to spin up. The higher the
     number, the greater the cost.
   * ``--machine-type`` specifies the amount of CPU and RAM in each node. There
     is a `variety of types <https://cloud.google.com/compute/docs/machine-types>`_
     to choose from. Picking something appropriate here will have a large effect
     on how much you pay - smaller machines restrict the max amount of RAM each
     user can have access to but allow more fine-grained scaling, reducing cost.
     The default (`n1-standard-2`) has 2CPUs and 7.5G of RAM each, and might not
     be a good fit for all use cases!
   * ``--zone`` specifies which data center to use. Pick something that is not
     too far away from your users. You can find a list of them `here <https://cloud.google.com/compute/docs/regions-zones/regions-zones#available>`_.
   * ``--cluster-version`` specifies the version of kubernetes we want. Here,
     we specify the minimum that the default configuration will support.

5. To test if your cluster is initialized, run:

   .. code-block:: bash

      kubectl get node

   The response should list three running nodes.

6. Give your account super-user permissions, allowing you to perform all
   the actions needed to set up JupyterHub.

   .. code-block:: bash

      kubectl create clusterrolebinding cluster-admin-binding --clusterrole=cluster-admin --user=<your-email-address>


.. _microsoft-azure:

Setting up Kubernetes on Microsoft Azure Container Service (AKS)
----------------------------------------------------------------

1. `Install <https://docs.microsoft.com/en-us/cli/azure/install-azure-cli>`_ the **Azure command-line tools**.


2. Authenticate the ``az`` tool so it may access your Azure account:

   .. code-block:: bash

      az login


3. Azure uses the concept of **subscriptions** to manage spending. You can
   get a list of subscriptions your account has access to by running:

   .. code-block:: bash

      az account list --refresh -o table

   Pick the subscription you want to use for creating the cluster, and set that
   as your default.

   .. code-block:: bash

      az account set -s <YOUR CHOSEN SUBSCRIPTION>


4. Azure uses the concept of **resource groups** to group related resources together.
   We need to create a resource group in a given data center location to hold all
   the resources for our hub.

   .. code-block:: bash

     az group create --name=<resource-group-name> --location=<datacenter-location> -o table

  where:

  * ``--name`` specifies the name of your resource group. We recommend using something
    that uniquely identifies this hub. For example, if you are creating a resource group
    for UC Berkeley's 2018 Spring Data100 Course, you should call it ucb_2018sp_data100_hub.

  * ``--location`` specifies the location of the data center you want your resource to be in.
    AKS is only available in `a limited set of locations <https://github.com/Azure/AKS/blob/master/preview_regions.md>`_.

5. Enable the cloud APIs required before creating a cluster.

   .. code-block:: bash

      az provider register --name Microsoft.Network --wait
      az provider register --name Microsoft.Compute --wait
      az provider register --name Microsoft.Storage --wait
      az provider register --name Microsoft.ContainerService --wait

6. Create an ssh key to secure your cluster.

   .. code-block:: bash

      ssh-keygen -f ssh-key-<cluster-name>

   Where ``<cluster-name>`` is the name of the cluster you are going to create in the next step.

   This will create a public key named ``ssh-key-<cluster-name>.pub`` and a private key named
   ``ssh-key-<cluster-name>``. Keep both of them safe!

7. Create an AKS cluster!

   .. code-block:: bash

      az aks create --name <cluster-name> \
                    --group <resource-group-name> \
                    --ssh-key-value ssh-key-<cluster-name>.pub \
                    --node-count 3 \
                    --node-vm-size Standard_DS2_v3 \
                    --kubernetes-version 1.8.2

   where:

   * ``--name`` is the name you want to use to refer to your cluster
   * ``--group`` is the ResourceGroup you created in step 4
   * ``--ssh-key-value`` is the ssh public key created in step 6
   * ``--node-count`` is the number of nodes you want in your kubernetes cluster
   * ``--node-vm-size`` is the size of the nodes you want to use, which varies based on
     what you are using your cluster for and how much RAM/CPU each of your users need.
     There is a `list of all possible node sizes <https://docs.microsoft.com/en-us/azure/cloud-services/cloud-services-sizes-specs>`_
     for you to choose from, but not all might be available in your location.
   * ``--kubernetes-version`` is the version of Kubernetes we want to use.


   This should take a few minutes and provide you with a working Kubernetes cluster!

8. Install `kubectl <https://kubernetes.io/docs/reference/kubectl/overview/>`_, a tool
   for accessing the Kubernetes API from the commandline:

   .. code-block:: bash

      az aks install-cli


9. Get credentials from Azure for ``kubectl`` to work:

   .. code-block:: bash

      az aks get-credentials --name <cluster-name> --group <resource-group-name>

  where:

  * ``--name`` is the name you gave your cluster in step 7
  * ``--group`` is the ResourceGroup you created in step 4

10. Check if your cluster is fully functional

   .. code-block:: bash

      kubectl get node

   The response should list three running nodes and their kubernetes versions!

.. note::

   Azure AKS is still in **preview**, and not all features might work as
   intended. In particular,

   1. You have to `not use RBAC <security.html#use-role-based-access-control-rbac>`_, since AKS does not support it
      yet.
   2. TODO: Figure out what's needed for helm?

.. _amazon-aws:

Setting up Kubernetes on Amazon Web Services (AWS)
--------------------------------------------------

AWS does not have native support for Kubernetes, however there are
many organizations that have put together their own solutions and
guides for setting up Kubernetes on AWS.

We like the `Heptio guide`_, and recommend using this for setting up your cluster for clusters
that span short periods of time (a week long workshop, for example). However, if
you are setting up a cluster that would need to run for much longer, we recommend you use
[kops](https://kubernetes.io/docs/getting-started-guides/kops/). It is a bit more complex,
but provides features (such as log collection & cluster upgrades) that are necessary to
run a longer term cluster.

.. note::

   The Heptio deployment of Kubernetes on AWS should not be considered
   production-ready. See `the introduction in the Heptio Kubernetes tutorial <http://docs.heptio.com/content/tutorials/aws-cloudformation-k8s.html>`_
   for information about what to expect.

1. Follow Step 1 of the `Heptio guide`_, called **Prepare your AWS Account**.

   This sets up your Amazon account with the credentials needed to run Kubernetes.

   .. note::

      * Make sure that you keep the file downloaded when you create the SSH
        key. This will be needed later to allow ``kubectl`` to interact with
        your Kubernetes cluster.

      * You may find it helpful to "pin" the services we'll be using to your AWS
        navbar. This makes it easier to navigate in subsequent sessions.
        Click the "pin" icon at the top, then drag ``CloudFormation`` and
        ``EC2`` into your navbar.

2. Deploy a Kubernetes template from Heptio.

   .. note::

      This section largely follows Step 2 of the `Heptio guide`_.

   AWS makes it possible to deploy computational resources in a "stack" using
   templates. Heptio has put together a template for running Kubernetes on AWS.
   Click the button below to select the Heptio template, then follow the
   instructions below.

   .. raw:: html

      <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=Heptio-Kubernetes&templateURL=https://s3.amazonaws.com/quickstart-reference/heptio/latest/templates/kubernetes-cluster-with-new-vpc.template">
      <button style="background-color: rgb(235, 119, 55); border: 1px solid; border-color: black; color: white; padding: 15px 32px; text-align: center; text-decoration: none; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 8px;">Deploy the Heptio Template</button></a>

   You'll be taken to an AWS page with a field already
   chosen under "Choose a template". Simply hit "Next".

   **Enter AWS instance information (page 1)**: On this page you'll tell AWS
   what kind of hardware you need. Fill in the following required fields:

   * ``Stack Name`` can be anything you like.
   * ``Availability Zone`` is related to the location of the AWS
     resources. Choose an AWS location close to your physical location or
     any other desired AWS location.
   * ``Admin Ingress Location`` defines the locations from which you
     can access this cluster as an administrator. Enter ``0.0.0.0/0``
     for the most permissive approach.
   * ``SSH Key`` is a dropdown list of keys attached to your account.
     The one you created in Step 1 should be listed here. This will allow
     you to SSH into the machines if you desire.
   * ``Node Capacity`` defines the number of machines you've got available.
     This will depend on the ``Instance Type`` that you choose. E.g., if you
     want each user to have 2GB and you expect 10 users, choose a combination
     of ``Instance Type`` and ``Node Capacity`` that meets this requirement.
   * ``Instance Type`` defines what kind of machine you're requesting. See
     this `list of instance types with Amazon <https://aws.amazon.com/ec2/instance-types/>`_
     as well as this list of `pricing for each instance type <https://aws.amazon.com/ec2/pricing/on-demand/>`_.
   * ``Disk Size`` corresponds to the hard disk for each node. Note that this is
     different from the disks that users will use for their own notebooks/data.
     This disk should be large enough to contain the size of any Docker
     images you're serving with the JupyterHub.
   * ``Instance Type (Bastion Host)`` corresponds to a computer that allows
     for easy SSH access to your Kubernetes cluster. This does not need to
     be a fancy computer. You may leave these as defaults. For more information
     on the Bastion Host, `see here <http://docs.aws.amazon.com/quickstart/latest/linux-bastion/architecture.html>`_.

   **Enter AWS instance information (page 2)**: On the second page you may leave
   all of these fields as is or customize as you wish. When done, hit ``Next``. Then
   confirm and hit ``Next`` once more.

   AWS will now create the computational resources defined in the Heptio
   template (and according to the options that you chose).

   To see the status of the resources you've requested,
   see the ``CloudFormation`` page. You should see two stacks being created,
   each will have the name you've requested. When they're done creating,
   continue with the guide.

   .. note::

      This often takes 15-20 minutes to finish. You'll know it's done when
      both stacks show the status ``CREATE_COMPLETE``.

3. Ensure that the *latest* version of `kubectl <https://kubernetes.io/docs/user-guide/prereqs/>`_ is
   installed on your machine be following the `install instructions <https://kubernetes.io/docs/user-guide/prereqs>`_.

4. Configure your ``kubectl`` to send instructions to the newly-created
   Kubernetes cluster. To do this, you'll need to copy a security file
   onto your computer. Heptio has pre-configured the command needed to do this.
   To access it, from the ``CloudFormation`` page click on the stack you just
   created (the one without "k8s-stack" in it). Below, there is an "Outputs"
   tab. Click on this, and look for a field called ``GetKubeConfigCommand``.
   Copy / paste that text into your terminal, replacing the ``path/to/myKey.pem``
   with the path to the key you downloaded in Step 1. It looks something like::

     SSH_KEY="<path/to/varMyKey.pem>"; scp -i $SSH_KEY -o
     ProxyCommand="ssh -i \"${SSH_KEY}\" ubuntu@<BastionHostPublicIP> nc
     %h %p" ubuntu@<MasterPrivateIP>:~/kubeconfig ./kubeconfig

5. Tell Kubernetes to use this configuration file. Run::

     export KUBECONFIG=$(pwd)/kubeconfig

6. Confirm that ``kubectl`` is connected to your Kubernetes cluster.
   Run::

      kubectl get nodes

   you should see a list of three nodes, each beginning with ``ip``.

7. Enable dynamic storage on your Kubernetes cluster.
   Create a file, ``storageclass.yml`` on your local computer, and enter
   this text::

       kind: StorageClass
       apiVersion: storage.k8s.io/v1
       metadata:
         annotations:
            storageclass.beta.kubernetes.io/is-default-class: "true"
         name: gp2
       provisioner: kubernetes.io/aws-ebs
       parameters:
         type: gp2

   Next, run this command:

       .. code-block:: bash

          kubectl apply -f storageclass.yml

   This enables `dynamic provisioning
   <https://kubernetes.io/docs/concepts/storage/persistent-volumes/#dynamic>`_ of
   disks, allowing us to automatically assign a disk per user when they log
   in to JupyterHub.


8. Enable legacy authorization mode. This is temporarily required since the newer
   and more secure authorization mode is not out of beta yet.

      .. code-block:: bash

         kubectl create clusterrolebinding permissive-binding \
          --clusterrole=cluster-admin \
          --user=admin \
          --user=kubelet \
          --group=system:serviceaccounts

  This step should hopefully go away soon!

You should now be ready for the next step.

Next Step
---------

Now that you have a Kubernetes cluster running, it is time to
:ref:`set up helm <setup-helm>`.

.. _ways to set up a cluster: https://kubernetes.io/docs/setup/pick-right-solution/
.. _Azure resource group: https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-overview#resource-groups
.. _Heptio guide: https://s3.amazonaws.com/quickstart-reference/heptio/latest/doc/heptio-kubernetes-on-the-aws-cloud.pdf
