(baremetal-microk8s)=

# Kubernetes on a Bare Metal Host with MicroK8s

If you have server hardware available and a small enough user base it's possible to use [Canonical's MicroK8s](https://microk8s.io/) in place of a cloud vendor.

```{warning}
With no ability to scale, users will not be able to access their notebooks when memory and CPU resources are exhausted. Read the section on resource planning and set resource limits accordingly.
```

This guide describes how to configure MicroK8s to work with Zero to JupyterHub for Kubernetes.

## Procedure

1. Install MicroK8s as described in the Getting Started section of the [MicroK8s documentation](https://microk8s.io/docs).

   ```{note}
   For production use consider installing MicroK8s on Ubuntu. Other platforms use an Ubuntu VM which reduces the available resources and performance.
   ```

1. Enable the necessary MicroK8s Add ons:

   - [dns](https://microk8s.io/docs/addon-dns)
   - helm3

   ```
   microk8s enable dns
   microk8s enable helm3
   ```

1. Configure networking.

   The Zero to JupyterHub helm chart defaults to using the `LoadBalancer` service type. On cloud vendors this triggers the allocation of a load balancer and IP address. In order for a `LoadBalancer` resource to work in MicroK8s the [MetalLB add on](https://microk8s.io/docs/addon-metallb) has to be enabled.

   MetalLB has two modes: [Layer 2 Mode](https://metallb.universe.tf/concepts/layer2/), the default and recommended mode, and [BGP Mode](https://metallb.universe.tf/concepts/bgp/). In Layer 2 mode, MetalLB needs a range of IP addresses that are on the same network as the host running MicroK8s. If the host has multiple interfaces you can choose addresses from of _any_ of the interfaces. The range you give MetalLB can have as few as one IP address. When a `LoadBalancer` resource is requested MetalLB automatically adds one of its IP addresses to the interface of your host and passes the traffic into your Kubernetes system. This example shows how to enable a pool of addresses from `10.0.0.100` to `10.0.0.200`:

   ```
   microk8s enable metallb:10.0.0.100-10.0.0.200
   ```

   If you give MetalLB a range of IP addresses you can choose one in your JupyterHub configuration. This is particularly important if you need TLS because you will have to setup a DNS entry for your server that has a fixed IP address. Here's an example proxy configuration with a fixed IP address request:

   ```yaml
   ## Example config.yaml
   proxy:
     https:
       enabled: true
       hosts:
         - jupyter.myschool.edu
       letsencrypt:
         contactEmail: me@myschool.edu
     service:
       loadBalancerIP: 10.0.0.150
   ```

1. Configure Storage.

   The JupyterHub chart uses persistent volume claims to allocate storage for notebooks and the hub database. Cloud vendors handle these claims automatically. On MicroK8s you have to enable the [OpenEBS Add-on](https://microk8s.io/docs/addon-openebs) so claims will be bound to storage. OpenEBS uses iSCSI for clustering which isn't necessary on a single host but the service must be enabled before you can enable OpenEBS:

   ```
   sudo systemctl enable iscsid.service
   ```

   Now you can enable OpenEBS:

   ```
   microk8s enable openebs
   ```

   OpenEBS installs a set of `StorageClass` resources but does not mark any of them default. Choose a directory on your host where you want to store data from your cluster. The path can be on the system disk or a separate disk. Create a YAML file called `local-storage-dir.yaml` with the following contents:

   ```yaml
   ## local-storage-dir.yaml
   apiVersion: storage.k8s.io/v1
   kind: StorageClass
   metadata:
     name: local-storage-dir
     annotations:
       storageclass.kubernetes.io/is-default-class: "true"
       openebs.io/cas-type: local
       cas.openebs.io/config: |
         - name: StorageType
           value: hostpath
         - name: BasePath
           value: /path/to/your/storage
   provisioner: openebs.io/local
   reclaimPolicy: Delete
   volumeBindingMode: WaitForFirstConsumer
   ```

   ```{note}
   Replace `/path/to/your/storage` with your desired path.
   ```

   Apply the customized `StorageClass` resource to your cluster:

   ```
   $ microk8s.kubectl apply -f local-storage-dir.yaml
   ```

   With a default storage class installed the Zero to JupyterHub chart doesn't require any customization.

Now you're ready to install JupyterHub!

## Resource Planning

Hardware has to be sized for **peak load**. It's critical to plan for class size, especially if you intend to use JupyterHub in class with all attendees logged in simultaneously. Each running notebook server should be **guaranteed at least** 0.5 cores and 1G of RAM. Setting the limits lower will cause a lot of frustration. When a server exhausts its memory kernels die off and notebooks crash. The Kubernetes system and JupyterHub also consume resources that have to be accounted for. Assuming there are 2 cores and 2 GiB of RAM overhead this formula will tell you how to size a machine for a particular class size:

```{math}
Cores = \left \lceil{2 + CPUGuarantee * ClassSize}\right \rceil

RAM = 2 + RAMGuarantee * ClassSize
```

If you use the default limits in your configuration:

```yaml
## Example config.yaml
singleuser:
  memory:
    guarantee: 1G
  cpu:
    guarantee: 0.5
```

and you have a class of 35 students that means you should have a machine with at least:

```{math}
Cores = \left \lceil{2 + 0.5 * 35}\right \rceil = 20

RAM = 2 + {1 * 35} = 37
```

The default limits are fairly meager. If you intend to have your class doing real work or you expect that they will have many notebooks open simultaneously in JupyterLab you should plan for double the memory and CPU limits:

```{math}
Cores = \left \lceil{2 + 1 * 35}\right \rceil = 37

RAM = 2 + {2 * 35} = 72
```

These numbers are estimates. Disk usage and network bandwidth must also be considered.

## Troubleshooting

1. The JupyterHub `LoadBalancer` resource is stuck in the `Pending` state.

   Verify that you have MetalLB installed correctly and that you gave it IP addresses. This command should show you two running pods. Check the controller pod log for errors:

   ```
   microk8s.kubectl -n metallb-system get all
   ```

1. The hub pod is stuck pending `Pending` state.

   This is probably because the volume claim is unbound. Use this command to check:

   ```
   microk8s.kubectl get pvc
   ```

   If the claim is unbound verify that the storage class you created is correct and set to the default.

   ```
   microk8s.kubectl get sc
   ```

1. Not everyone in my class can start the notebook.

   Kubernetes manages resources carefully. Each notebook server is guaranteed CPU and memory resources and when there are no more to give new servers cannot be scheduled. Read the Resource Planning section and adjust your limits accordingly.
