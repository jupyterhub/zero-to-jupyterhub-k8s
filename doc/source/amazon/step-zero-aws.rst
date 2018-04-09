.. _amazon-aws:

Step Zero: Kubernetes on Amazon Web Services (AWS)
--------------------------------------------------

AWS does not have native support for Kubernetes, however there are
many organizations that have put together their own solutions and
guides for setting up Kubernetes on AWS.

This guide uses kops to setup a cluster on AWS.  This should be seen as a rough template you will use to
setup and shape your cluster.

Procedure:

1. Create a IAM Role

   This role will be used to give your CI host permission to create and destroy resources on AWS
   
   * AmazonEC2FullAccess 
   * IAMFullAccess 
   * AmazonS3FullAccess 
   * AmazonVPCFullAccess 
   * Route53FullAccess (Optional)
   
2. Create a new instance to use as your CI host.  This node will deal with provisioning and tearing down the cluster.

   This instance can be small (t2.micro for example).
   
   When creating it, assign the IAM role created in step 1.

3. Install kops and kubectl on your CI host

   Follow the instructions here: https://github.com/kubernetes/kops/blob/master/docs/install.md

4. Setup an ssh keypair to use with the cluster

   ``ssh-keygen``

5. Choose a cluster name

   Since we are not using pre-configured DNS we will use the suffix ".k8s.local".  Per the docs, if the DNS name ends in .k8s.local the cluster will use internal hosted DNS.
   
   ``export NAME=<somename>.k8s.local``

6. Create a S3 bucket to store your cluster configuration

   Since we are on AWS we can use a S3 backing store.  It is recommended to enabling versioning on the S3 bucket.
   We don't need to pass this into the KOPS commands.  It is automatically detected by the kops tool as an env variable.
   
   ``export KOPS_STATE_STORE=s3://<your_s3_bucket_name_here>``
   
7. Set the region to deploy in

   ``export REGION=`curl -s http://169.254.169.254/latest/dynamic/instance-identity/document|grep region|awk -F\" '{print $4}'```

8. Set the availability zones for the nodes

   For this guide we will be allowing nodes to be deployed in all AZs::
  
       export ZONES=$(aws ec2 describe-availability-zones --region $REGION | grep ZoneName | awk '{print $2}' | tr -d '"')
       export ZONES=$(echo $ZONES | tr -d " " | rev | cut -c 2- | rev)``

9. Create the cluster

   All sizes measured in GB::

       kops create cluster $NAME \
         --zones $ZONES \
         --authorization RBAC \
         --master-size t2.micro \
         --master-volume-size 10 \
         --node-size t2.medium \
         --node-volume-size 10 \
         --yes

   Future settings to consider::
   
       --vpc
       --bastion (security)
       --master-count (redundancy/HA)
       --master-zones
       --node-count
       --master/node-security-groups (security)
       --ssh-access (security)
       --topology private (security)

10. Wait for the cluster to start-up

    Running the 'kops validate cluster' command will tell us what the current state of setup is.
    If you see "can not get nodes" initially, just be patient as the cluster can't report until a
    few basic services are up and running.
   
    Keep running 'kops validate cluster' until you see "Your cluster $NAME is ready" at the end of the output.
   
    ``time until kops validate cluster; do sleep 15 ; done`` can be used to automate the waiting process.
    
    If at any point you wish to destroy your cluster after this step, run ``kops delete cluster $NAME --yes``

11. Confirm that ``kubectl`` is connected to your Kubernetes cluster.
    Run::

       kubectl get nodes

    you should see a list of two nodes, each beginning with ``ip``.

12. Enable dynamic storage on your Kubernetes cluster.
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

Congrats. Now that you have your Kubernetes cluster running, it's time to
begin :ref:`creating-your-jupyterhub`.
