.. _amazon-aws:

Kubernetes on Amazon Web Services (AWS)
---------------------------------------

AWS does not have native support for Kubernetes, however there are many
organizations that have put together their own solutions and guides for setting
up Kubernetes on AWS.

This guide uses kops to setup a cluster on AWS.  This should be seen as a rough
template you will use to setup and shape your cluster.

=============
The Procedure
=============

#. Create an IAM Role

   This role will be used to give your CI host permission to create and destroy
   resources on AWS

   * AmazonEC2FullAccess
   * IAMFullAccess
   * AmazonS3FullAccess
   * AmazonVPCFullAccess
   * Route53FullAccess (Optional)

#. Create a new instance to use as your CI host.  This node will deal with
   provisioning and tearing down the cluster.

   This instance can be small (t2.micro for example).

   When creating it, assign the IAM role created in step 1.

   Once created, download ssh keys.

#. SSH to your CI host

#. Install kops and kubectl on your CI host

   * Follow the instructions here: https://github.com/kubernetes/kops/blob/master/docs/install.md

#. Choose a cluster name:

   Since we are not using pre-configured DNS we will use the suffix
   ".k8s.local".  Per the docs, if the DNS name ends in .k8s.local the cluster
   will use internal hosted DNS.

   .. code-block:: console

      export NAME=<somename>.k8s.local

#. Setup an ssh keypair to use with the cluster:

   .. code-block:: console

      ssh-keygen

#. Create an S3 bucket to store your cluster configuration

   Since we are on AWS we can use a S3 backing store.  It is recommended to
   enabling versioning on the S3 bucket. We don't need to pass this into the
   KOPS commands.  It is automatically detected by the kops tool as an env
   variable.

   .. code-block:: console
   
      export KOPS_STATE_STORE=s3://<your_s3_bucket_name_here>

#. Set the region to deploy in:

   .. code-block:: console

      export REGION=`curl -s http://169.254.169.254/latest/dynamic/instance-identity/document|grep region|awk -F\" '{print $4}'`

#. Install the AWS CLI:

   .. code-block:: console

      sudo apt-get update
      sudo apt-get install awscli

#. Set the availability zones for the nodes

   For this guide we will be allowing nodes to be deployed in all AZs:

   .. code-block:: console

      export ZONES=$(aws ec2 describe-availability-zones --region $REGION | grep ZoneName | awk '{print $2}' | tr -d '"')

#. Create the cluster

   For a basic setup run the following (All sizes measured in GB):

   .. code-block:: console

      kops create cluster $NAME \
      --zones "$ZONES" \
      --authorization RBAC \
      --master-size t2.micro \
      --master-volume-size 10 \
      --node-size t2.medium \
      --node-volume-size 10 \
      --yes

   For a more secure setup add the following params to the kops command::

   .. code-block:: console

      --topology private \
      --networking weave \

   This creates a cluster where all of the masters and nodes are in private subnets and don't have external IP addresses.  A mis-configured security group or insecure ssh configuration is less likely to compromise the cluster.
   In order to SSH into your cluster you will need to set up a bastion node.  Make sure you do that step below.
   If you have the default number of elastic IPs (10) you may need to put in a request to AWS support to bump up that limit.  The alternative is reducing the number of zones specified.

   More reading on this subject:
   https://github.com/kubernetes/kops/blob/master/docs/networking.md

   Settings to consider (not covered in this guide):

   .. code-block:: console

      --vpc
        Allows you to use a custom VPC or share a VPC
        https://github.com/kubernetes/kops/blob/master/docs/run_in_existing_vpc.md
      --master-count
        Spawns more masters in one or more VPCs
        This improves redudancy and reduces downtime during cluster upgrades
      --master-zones
        specify zones to run the master in
      --node-count
        Increases the total nodes created (default 2)
      --master/node-security-groups
        Allows you to specify additional security groups to put the masters and nodes in by default
      --ssh-access
        By default SSH access is open to the world (0.0.0.0).
        If you are using a private topology, this is not a problem.
        If you are using a public topology make sure your ssh keys are strong and you keep sshd up to date on your cluster's nodes.


   .. note::

      Consider `setting a cloud budget <https://aws.amazon.com/aws-cost-management/aws-budgets/>`_
      for your AWS account in order to make sure you don't accidentally
      spend more than you wish to.

#. Wait for the cluster to start-up

   Running the ``kops validate cluster`` command will tell us what the current state of setup is.
   If you see "can not get nodes" initially, just be patient as the cluster can't report until a
   few basic services are up and running.

   Keep running ``kops validate cluster`` until you see "Your cluster $NAME is ready" at the end of the output::

   .. code-block:: console

      time until kops validate cluster; do sleep 15; done
      
   can be used to automate the waiting process.

   If at any point you wish to destroy your cluster after this step, run ``kops delete cluster $NAME --yes``


#. Confirm that ``kubectl`` is connected to your Kubernetes cluster.

   Run:

   .. code-block:: console

      kubectl get nodes

   You should see a list of two nodes, each beginning with ``ip``.

   If you want to use kubectl and helm locally (necessary for step #3 in `Setting up Helm <setup-helm#initialization>`_):

   * run the following on CI host: ``kops export kubecfg``
   * copy the contents of ``~/.kube/config`` to the same place on your local system

   If you wish to put the kube config file in a different location, you will need to run:
    
   .. code-block:: console

      export KUBECONFIG=<other kube config location>


#. Configure ssh bastion (Skip this step if you did not go with the **--topology private** option above!)

   Ideally we would simply be passing the ``--bastion`` flag into the kops command above.  However that flag is not functioning as intended at the moment.  https://github.com/kubernetes/kops/issues/2881

   Instead we need to follow this guide: https://github.com/kubernetes/kops/blob/master/docs/examples/kops-tests-private-net-bastion-host.md#adding-a-bastion-host-to-our-cluster

   At this point there are a few public endpoints left open which need to be addressed

   * Bastion ELB security group defaults to access from 0.0.0.0
   * API ELB security group defaults to access from 0.0.0.0


#. Enable dynamic storage on your Kubernetes cluster.

   Create a file, ``storageclass.yml`` on your local computer, and enter
   this text:

   .. code-block:: yaml

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

   .. code-block:: console

      kubectl apply -f storageclass.yml

   This enables `dynamic provisioning
   <https://kubernetes.io/docs/concepts/storage/persistent-volumes/#dynamic>`_ of
   disks, allowing us to automatically assign a disk per user when they log
   in to JupyterHub.

   .. note:

      EC2 instance metadata is data detailing configuring and running the running instance. This data is potentially sensitive and can be seen by anyone with direct access to the instance.
      This metadata is blocked by an init-container by default since they override ``iptables`` used in setting up the instance. Setting up and securing access to this metadata can be done by adding an ``iptables`` rule in an init-container as shown `here <https://zero-to-jupyterhub.readthedocs.io/en/v0.5-doc/security.html>`_ in the cloud metadata security section.


==========
Encryption
==========

There are simple methods for encrypting your Kubernetes cluster. Illustrated here are simple methods for encryption at rest and encryption in transit.

**Encryption at Rest**

Instead of performing step 13 above. Create the following ``storageclass.yml`` file on your local computer:

.. code-block:: yaml

   kind: StorageClass
   apiVersion: storage.k8s.io/v1
   metadata:
     annotations:
       storageclass.beta.kubernetes.io/is-default-class: "true"
     name: gp2
   provisioner: kubernetes.io/aws-ebs
   parameters:
     type: gp2
     encrypted: "true"

The main difference is the addition of the line `encrypted: "true"` and make note that `true` is in double quotes.

Next run these commands:

.. code-block:: console

   kubectl delete storageclass gp2
   kubectl apply -f storageclass.yml

Kubernetes will not allow you to modify storageclass gp2 in order to add the `encrypted` flag so you will have to delete it first.
This will encrypt any dynamic volumes (such as your notebook)created by Kubernetes, it will not encrypt the storage on the Kubernetes nodes themselves.

**Encryption in Transit**

In step 9 above, set up the cluster with weave by including the `--networking weave` flag in the `kops create` command above.
Then perform the following steps:

#. Verify weave is running:

   .. code-block:: console

      kubectl --namespace kube-system get pods

   You should see several pods of the form `weave-net-abcde`

#. Create Kubernetes secret with a private password of sufficient strength. A random 128 bytes is used in this example:

   .. code-block:: console

      openssl rand -hex 128 >weave-passwd
      kubectl create secret -n kube-system generic weave-passwd --from-file=./weave-passwd

   It is important that the secret name and its value (taken from the filename) are the same. If they do not match you may get a `ConfigError`

#. Patch Weave with the password:

   .. code-block:: console

      kubectl patch --namespace=kube-system daemonset/weave-net --type json -p '[ { "op": "add", "path": "/spec/template/spec/containers/0/env/0", "value": { "name": "WEAVE_PASSWORD", "valueFrom": { "secretKeyRef": { "key": "weave-passwd", "name": "weave-passwd" } } } } ]'


   If you want to remove the encryption you can use the following patch:

   .. code-block:: console

      kubectl patch --namespace=kube-system daemonset/weave-net --type json -p '[ { "op": "remove", "path": "/spec/template/spec/containers/0/env/0"} ]'

#. Check to see that the pods are restarted. To expedite the process you can delete the old pods.

#. You can verify encryption is turned on with the following command:

   .. code-block:: console

      kubectl exec -n kube-system weave-net-<pod> -c weave -- /home/weave/weave --local status

   You should see `encryption: enabled`

   If you really want to insure encryption is working, you can listen on port `6783` of any node. If the traffic looks like gibberish, you know it is on.

==============
Shared Storage
==============
A shared volume is supposed to be mounted to multiple user pods, so we cannot use EBS. As an alternative, there's AWS EFS:

#. :ref:`amazon-efs`

#. :ref:`user-storage`

Congrats. Now that you have your Kubernetes cluster running, it's time to
begin :ref:`creating-your-jupyterhub`.
