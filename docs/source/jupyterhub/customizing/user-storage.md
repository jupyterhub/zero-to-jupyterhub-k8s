(user-storage)=

# Customizing User Storage

For the purposes of this guide, we'll describe "storage" as
a "volume" - a location on a disk where a user's data resides.

Kubernetes handles the creation and allocation of persistent
volumes, under-the-hood it uses the cloud provider's API to
issue the proper commands. To that extent most of our discussion
around volumes will describe Kubernetes objects.

JupyterHub uses Kubernetes to manage user storage. There are two
primary Kubernetes objects involved in allocating
storage to pods:

- A `PersistentVolumeClaim` (`PVC`) specifies what kind of storage is required. Its configuration is specified in your `config.yaml` file.
- A `PersistentVolume` (`PV`) is the actual volume where the user's data resides. It is created by Kubernetes using details in a `PVC`.

As Kubernetes objects, they can be queried
with the standard `kubectl` commands (e.g., `kubectl --namespace=<your-namespace> get pvc`)

In JupyterHub, each user gets their own `PersistentVolumeClaim`
object, representing the data attached to their account.
When a new user starts their JupyterHub server, a
`PersistentVolumeClaim` is created for that user. This claim
tells Kubernetes what kind of storage (e.g., ssd vs. hd) as
well as how much storage is needed. Kubernetes checks to see
whether a `PersistentVolume` object for that user exists (since
this is a new user, none will exist). If no `PV` object exists,
then Kubernetes will use the `PVC` to create a new `PV` object
for the user.

Now that a `PV` exists for the user, Kubernetes next must
attach (or "mount") that `PV` to the user's pod (which runs
user code). Once this is accomplished, the user will have
access to their `PV` within JupyterHub. Note that this all happens
under-the-hood and automatically when a user logs in.

`PersistentVolumeClaim`s and `PersistentVolume`s are not
deleted unless the `PersistentVolumeClaim` is explicitly deleted
by the JupyterHub administrator. When a user shuts down their
server, their user pod is deleted and their volume is
detached from the pod, _but the `PVC` and `PV` objects still exist_.
In the future, when the user logs back in, JupyterHub will
detect that the user has a pre-existing `PVC` and will simply
attach it to their new pod, rather than creating a new `PVC`.

## How can this process break down?

When Kubernetes uses the `PVC` to create a new user `PV`, it
is sending a command to the underlying API of whatever cloud
provider Kubernetes is running on. Occasionally, the request
for a specific `PV` might fail - for example, if your account
has reached the limit in the amount of disk space available.

Another common issue is limits on the number of volumes that
may be simultaneously attached to a node in your cluster. Check
your cloud provider for details on the limits of storage
resources you request.

```{note}
Some cloud providers have a limited number of disks that can be attached to
each node. Since JupyterHub allocates one disk per user for
persistent storage, this limits the number of users that can be running in
a node at any point of time. If you need users to have
persistent storage, and you end up hitting this limit, you must use
*more* nodes in order to accommodate the disk for each user. In this
case, we recommend allocating *fewer* resources per node (e.g. RAM) since
you'll have fewer users packed onto a single node.
```

## Configuration

Most configuration for storage is done at the cluster level and
is not unique to JupyterHub. However, some bits are, and we will
demonstrate here how to configure those.

Note that new `PVC`s for pre-existing users will **not** be
created unless the old ones are destroyed. If you update your
users' `PVC` config via `config.yaml`, then any **new** users will
have the new `PVC` created for them, but **old** users will not.
To force an upgrade of the storage type for old users, you will
need to manually delete their `PVC` (e.g.
`kubectl --namespace=<your-namespace> delete pvc <pvc-name>`).
**This will delete all of the user's data** so we recommend
backing up their filesystem first if you want to retain their data.

After you delete the user's `PVC`, upon their next log-in a new
`PVC` will be created for them according to your updated `PVC`
specification.

### Type of storage provisioned

A [StorageClass](https://kubernetes.io/docs/concepts/storage/storage-classes/) object
is used to determine what kind of `PersistentVolume`s are provisioned for your
users. Most popular cloud providers have a `StorageClass` marked as default. You
can find out your default `StorageClass` by doing:

```bash
kubectl get storageclass
```

and looking for the object with `(default)` next to its name.

To change the kind of `PersistentVolume`s provisioned for your users,

1. Create a new `StorageClass` object following the
   [kubernetes documentation](https://kubernetes.io/docs/concepts/storage/storage-classes/)
2. Specify the name of the `StorageClass` you just created in `config.yaml`
   ```yaml
   singleuser:
     storage:
       dynamic:
         storageClass: <storageclass-name>
   ```
3. Do a `helm upgrade`

Note that this will only affect new users who are logging in. We recommend
you do this before users start heavily using your cluster.

We will provide examples for popular cloud providers here, but will generally
defer to the Kubernetes documentation.

#### Google Cloud

On Google Cloud, the default `StorageClass` will provision
Standard [Google Persistent Disk](https://cloud.google.com/compute/docs/disks/#pdspecs)s.
These run on Hard Disks. For more performance, you may want to use SSDs.
To use SSDs, you can create a new `StorageClass` by first putting the following `yaml` into a new file. We recommend a descriptive name such
as `storageclass.yaml`, which we'll use below:

```yaml
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: jupyterhub-user-ssd
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
allowedTopologies:
  - matchLabelExpressions:
      - key: failure-domain.beta.kubernetes.io/zone
        values:
          - <your-cluster-zone>
```

Replace `<your-cluster-zone>` with the Zone in which you created your cluster (you can find
this with `gcloud container clusters list`).

Next, create this object by running `kubectl apply -f storageclass.yaml`
from the commandline. The [Kubernetes Docs](https://kubernetes.io/docs/concepts/storage/storage-classes#the-storageclass-resource)
have more information on what the various fields mean. The most important field is `parameters.type`,
which specifies the type of storage you wish to use. The two options are:

- `pd-ssd` makes `StorageClass` provision SSDs.
- `pd-standard` will provision non-SSD disks.

Once you have created this `StorageClass`, you can configure your JupyterHub's `PVC`
template with the following in your `config.yaml`:

```yaml
singleuser:
  storage:
    dynamic:
      storageClass: jupyterhub-user-ssd
```

Note that for `storageClass:` we use the name that we specified
above in `metadata.name`.

### Size of storage provisioned

You can set the size of storage requested by JupyterHub in the `PVC` in
your `config.yaml`.

```yaml
singleuser:
  storage:
    capacity: 2Gi
```

This will request a `2Gi` volume per user. The default requests a `10Gi`
volume per user.

We recommend you use the [IEC binary prefixes] (Ki, Mi, Gi, etc) for specifying
how much storage you want. `2Gi` (IEC binary prefix) is `(2 * 1024 * 1024 *
1024)` bytes, while `2G` (SI decimal prefix) is `(2 * 1000 * 1000 * 1000)`
bytes.

[iec binary prefixes]: https://en.wikipedia.org/wiki/Binary_prefix

## Turn off per-user persistent storage

If you do not wish for users to have any persistent storage, it can be
turned off. Edit the `config.yaml` file and set the storage type to
`none`:

```yaml
singleuser:
  storage:
    type: none
```

Next {ref}`apply the changes <apply-config-changes>`.

After the changes are applied, new users will no longer be allocated a
persistent `$HOME` directory. Any currently running users will still have
access to their storage until their server is restarted. You might have to
manually delete current users' `PVCs` with `kubectl` to reclaim any cloud
disks that might have allocated. You can get a current list of `PVC`s with:

```bash
kubectl --namespace=<your-namespace> get pvc
```

You can then delete the `PVCs` you do not want with:

```bash
kubectl --namespace=<your-namespace> delete pvc <pvc-name>
```

Remember that deleting someone's `PVC`s will delete all their data, so do so
with caution!

## Additional storage volumes

If you already have a `PersistentVolume` and `PersistentVolumeClaim` created
outside of JupyterHub you can mount them inside the user pods.
For example, if you have a shared `PersistentVolumeClaim` called
`jupyterhub-shared-volume` you could mount it as `/home/shared` in all user
pods:

```yaml
singleuser:
  storage:
    extraVolumes:
      - name: jupyterhub-shared
        persistentVolumeClaim:
          claimName: jupyterhub-shared-volume
    extraVolumeMounts:
      - name: jupyterhub-shared
        mountPath: /home/shared
```

Note that if you want to mount a volume into multiple pods the volume must
support a suitable [access mode](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes).
