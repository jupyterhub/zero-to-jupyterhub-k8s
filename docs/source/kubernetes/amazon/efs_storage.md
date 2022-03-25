---
orphan: true
---

(amazon-efs)=

# Setting up EFS storage on AWS

ElasticFileSystem is distributed file system which speaks the NFS protocol. It is rumored to be a GlusterFS fork behind the scenes at AWS.

Drawbacks:

- Setting permissions on persistent volumes is not nailed down in the Kubernetes spec yet. This adds some complications we will discuss later.
- A crafty user may be able to contact the EFS server directly and read other user's files depending on how the system is setup.

Procedure:

1. Setting up an EFS volume

   Go through the EFS setup wizard in AWS (in the future this part may be scripted). The new EFS volume must be in
   the same VPC as your cluster. This can be changed in the AWS settings after it has been created.

   Next, create a new security group for NFS traffic (target other instances in that group). Add a rule for incoming NFS traffic to the node security group and to the master security group. Change the EFS volume to use that security group.

   To verify that your EFS volume is working correctly, ssh into one of the master nodes and su to root. Next,
   follow the steps on the EFS console page for mounting your NFS volume. The DNS entry may take a few minutes to show up.

   Once the mount succeeds, unmount it and disconnect from the admin node.

2. Configuring Kubernetes to understand your EFS volume

   Create test_efs.yaml:

   ```yaml
   apiVersion: v1
   kind: PersistentVolume
   metadata:
     name: efs-persist
   spec:
     capacity:
       storage: 123Gi
     accessModes:
       - ReadWriteMany
     nfs:
       server: fs-${EFS_ID}.efs.us-east-1.amazonaws.com
       path: "/"
   ```

   Create test_efs_claim.yaml:

   ```yaml
   kind: PersistentVolumeClaim
   apiVersion: v1
   metadata:
     name: efs-persist
   spec:
     storageClassName: ""
     accessModes:
       - ReadWriteMany
     resources:
       requests:
         storage: 11Gi
   ```

   The sizes in these files are misleading. There is no quota enforced with EFS. In the
   future we want to set the efs PersistentVolume size to something ridiculously large
   like 8EiB and the PersistentVolumeClaim to 10GB. As far as we know at the moment, these sizes don't matter.

   A PersistentVolume defines a service which can perform a mount inside of a container. The
   PersistentVolumeClaim is a way of reserving a portion of the PersistentVolume and potentially
   locking access to it.

   The storageClassName setting looks innocuous, but it is incredibly critical. The only non storage
   class PV in the cluster is the one we defined above. In the future we should tag different PV's
   and use tag filters in the PVC instead of relying on a default of "".

   We are going to configure jupyterhub to use the same "static" claim among all of the containers. This
   means that all of our users will be using the same EFS share which should be able to scale as high as we need.

   This part is a little different than the standard guide. We need to create these PV's and PVC's in the
   namespace that our app will live in. Choose a namespace (this will be the same as the namespace you will
   use in the helm install step later on)

   Run these commands to setup your namespace and storage:

   ```
   kubectl create namespace <your namespace>
   kubectl --namespace=<your namespace> apply -f test_efs.yaml
   kubectl --namespace=<your namespace> apply -f test_efs_claim.yaml
   ```

   I don't know if the PV needs to be in the namespace, but the arg does not seem to hurt anything. The PVC must be in the namespace or stuff will break in weird ways.

3. Configuring your application to use EFS as it's backing storage

   We now add the following to config.yaml:

   ```yaml
   singleuser:
     image:
       name: jupyter/base-notebook
       tag: latest
     storage:
       type: "static"
       static:
         pvcName: "efs-persist"
         subPath: "home/{username}"
     extraEnv:
       CHOWN_HOME: "yes"
     uid: 0
     fsGid: 0
     cmd: "start-singleuser.sh"
   ```

   The image setting overrides the default pinned jh base image since it has not yet been updated
   to include the CHOWN_HOME setting.

   type static tells jh not to use a storage class and instead use a PVC defined below.

   pvcName matches the claim name we specified before

   subPath tells where on the supplied storage the mount point should be. In this case it will
   be "$EFS_ROOT/home/{username}"

   It turns out there is a bug in jupyterhub where the default subPath does not work, and setting the
   subPath to "{username}" breaks in the same way.

   The extraEnv section set's environmental variables before trying to start jupyterhub inside of the user's
   container. CHOWN_HOME is needed to force the ownership change of the home directory.

   Kubernetes is still conflicted if a uid and a gid should be passed in to change how the directory is mounted
   inside of the container. What we do for now is auto-chown the directory before jupyterhub has been started.

   The UID/fsGID is necessary to force the container to run the start-singleuser.sh as root. Once
   start-singleuser.sh has properly changed the ownership of the directory, it su's to the jupyterhub user.
