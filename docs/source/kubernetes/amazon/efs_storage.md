---
orphan: true
---

(amazon-efs)=

# Using AWS EFS storage with JupyterHub

ElasticFileSystem is a distributed file system which speaks the NFS protocol. It
is rumored to be a GlusterFS fork behind the scenes at AWS.

Drawbacks:

- Setting permissions on persistent volumes is not nailed down in the Kubernetes
  spec yet. This adds some complications we will discuss later.
- A crafty user may be able to contact the EFS server directly and read other
  user's files depending on how the system is setup.

## Setting up an EFS volume on AWS

Go through the EFS setup wizard in AWS (in the future this part may be
scripted). The new EFS volume must be in the same VPC as your cluster. This can
be changed in the AWS settings after it has been created.

Next, create a new security group for NFS traffic (target other instances in
that group). Add a rule for incoming NFS traffic to the node security group and
to the master security group. Change the EFS volume to use that security group.

To verify that your EFS volume is working correctly, ssh into one of the master
nodes and su to root. Next, follow the steps on the EFS console page for
mounting your NFS volume. The DNS entry may take a few minutes to show up.

Once the mount succeeds, unmount it and disconnect from the admin node.

## Root vs non-root

At this point, the procedure forks depending on which one of two approaches you
want to take. You can run your notebook containers as root or you can use the
[aws-efs-csi-driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver) and
an [Access
Point](https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html) and run
your notebook containers as non-root.

## Root

### Configuring Kubernetes to understand your EFS volume

Create `pv_root.yaml`:

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

Create `pvc_root.yaml`:

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

The sizes in these files are misleading. There is no quota enforced with EFS. In
the future we want to set the efs PersistentVolume size to something
ridiculously large like 8EiB and the PersistentVolumeClaim to 10GB. As far as we
know at the moment, these sizes don't matter.

A PersistentVolume defines a service which can perform a mount inside of a
container. The PersistentVolumeClaim is a way of reserving a portion of the
PersistentVolume and potentially locking access to it.

The storageClassName setting looks innocuous, but it is incredibly critical. The
only non storage class PV in the cluster is the one we defined above. In the
future we should tag different PV's and use tag filters in the PVC instead of
relying on a default of "".

We are going to configure jupyterhub to use the same "static" claim among all of
the containers. This means that all of our users will be using the same EFS
share which should be able to scale as high as we need.

This part is a little different than the standard guide. We need to create these
PV's and PVC's in the namespace that our app will live in. Choose a namespace
(this will be the same as the namespace you will use in the helm install step
later on).

Run these commands to setup your namespace and apply the Persistent and
Persistent Volume Claim to your Kubernetes cluster:

```bash
kubectl create namespace <your namespace>
kubectl --namespace=<your namespace> apply -f pv_root.yaml -f pvc_root.yaml
```

### Configuring JupyterHub to use the EFS PV/PVC (root)

Add the following to
[values.yaml](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/main/jupyterhub/values.yaml#L360)
in the JupyterHub helm chart:

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

The image setting overrides the default pinned JupyterHub base image since it
has not yet been updated to include the CHOWN_HOME setting. This will be fixed
in Z2JH 0.7.

type static tells JupyterHub not to use a Storage Class and instead use a PVC
defined below.

pvcName matches the claim name we specified before.

subPath tells where on the supplied storage the mount point should be. In this
case it will be "$EFS_ROOT/home/{username}"

It turns out there is a bug in jupyterhub where the default subPath does not
work, and setting the subPath to "{username}" breaks in the same way.

The extraEnv section set's environmental variables before trying to start
jupyterhub inside of the user's container. CHOWN_HOME is needed to force the
ownership change of the home directory.

Kubernetes is still conflicted if a uid and a gid should be passed in to change
how the directory is mounted inside of the container. What we do for now is
auto-chown the directory before JupyterHub has been started.

The UID/fsGID is necessary to force the container to run the start-singleuser.sh
as root. Once start-singleuser.sh has properly changed the ownership of the
directory, it su's to the jupyterhub user.

## Non-root

Mounting the EFS volume as your home directory without running the container as
root hinges on leveraging an [Access
Point](https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html) and the
[aws-efs-csi-driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver).
We'll step through setting up both in sequence.

Navigate to the AWS console.

Navigate to the EFS service.

Select your EFS volume.

Navigate to the `Access Points` tab.

Click the `Create access point` button.

Set `User ID` and `Group ID` to `1000`.

Specify any of the optional parameters.

Click the `Create access point` button.

Install
[aws-efs-csi-driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver) to
your Kubernetes cluster.

Create the following [Storage
Class](https://kubernetes.io/docs/concepts/storage/storage-classes/) and call it
`sc.yaml`:

```yaml
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: efs-csi-driver
provisioner: efs.csi.aws.com
```

Create the following [Persistent
Volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) and
call it `pv.yaml`:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: efs-pv
spec:
  capacity:
    storage: 5Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: efs-csi-driver
  mountOptions:
    - tls
  csi:
    driver: efs.csi.aws.com
    volumeHandle: fs-${EFS_ID}.amazonaws.com:/:${ACCESS_POINT_ID}
```

Create the following Persistent Volume Claim and call it `pvc.yaml`:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: efs-pvc
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: efs-csi-driver
  resources:
    requests:
      storage: 5Gi
```

Run these commands to apply the Storage Class, Persistent Volume, and
Persistent Volume Claim to your Kubernetes cluster:

```bash
kubectl create namespace <your namespace>
kubectl apply --namespace=<your namespace> -f sc.yaml -f pv.yaml -f pvc.yaml
```

### Configuring JupyterHub to use the EFS PV/PVC (non-root)

Add the following to
[values.yaml](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/main/jupyterhub/values.yaml#L360)
in the JupyterHub helm chart:

```yaml
singleuser:
  image:
    name: jupyter/base-notebook
    tag: latest
  storage:
    type: "static"
    static:
      pvcName: "efs-persist"
      subPath: "home/jovyan"
  uid: 1000
  fsGid: 1000
  cmd: "start-singleuser.sh"
```

We set the subpath to `/home/jovyan` because now that we're not running as root,
all Linux users will be `jovyan` instead of their JupyterHub specific username.
The update to uid and fsGid is self-explanatory (1000 is the first non-root
user).
