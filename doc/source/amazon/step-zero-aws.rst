.. _amazon-aws:

Step Zero: Kubernetes on Amazon Web Services (AWS)
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

Congrats. Now that you have your Kubernetes cluster running, it's time to
begin :ref:`creating-your-jupyterhub`.

.. _Heptio guide: https://s3.amazonaws.com/quickstart-reference/heptio/latest/doc/heptio-kubernetes-on-the-aws-cloud.pdf
