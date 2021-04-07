(digital-ocean)=

# Kubernetes on Digital Ocean

You can create a Kubernetes cluster [either through the Digital Ocean website, or using the Digital Ocean command line tools](https://www.digitalocean.com/).

This page describes the commands required to setup a Kubernetes cluster using the command line.
If you prefer to use the Digital Ocean portal see the [Digital Ocean Get Started](https://www.digitalocean.com/products/kubernetes).

1. Prepare your Digital Ocean shell environment.

   1. **Install command-line tools locally**. You'll need at least v1.13.0.

   You can either follow the [installation instructions](https://github.com/digitalocean/doctl/blob/main/README.md) or use the commands below:

   ```
   wget https://github.com/digitalocean/doctl/releases/download/v1.13.0/doctl-1.13.0-linux-amd64.tar.gz
   tar -xvf doctl-1.13.0-linux-amd64.tar.gz
   sudo mv doctl /usr/bin/
   ```

   2. Create an API token on the Digital Ocean portal. Navigate to API then Generate New Token.
   3. Connect your local CLI with your account:

      ```
      doctl auth init
      ```

2. Create your cluster.
   Digital Ocean's use of doctl for kubernetes support is in beta so you'll need to run the following (add it to your `.bashrc` if you want to make this change permanent).

   ```
   export DIGITALOCEAN_ENABLE_BETA=1
   doctl k8s cluster create jupyter-kubernetes --region lon1 --node-pool="name=worker-pool;count=3"
   ```

3. Export your cluster config.
   You can change the default location from $HOME/.kube by setting the KUBECONFIG environment variable.

   ```
   mkdir -p ~/.kube
   doctl k8s cluster kubeconfig show jupyter-kubernetes > ~/.kube/config
   ```

4. Create an ssh key to secure your cluster.

   ```
   ssh-keygen -f ssh-key-<CLUSTER-NAME>
   ```

   It will prompt you to add a password, which you can leave empty if you wish.
   This will create a public key named `ssh-key-<CLUSTER-NAME>.pub` and a private key named
   `ssh-key-<CLUSTER-NAME>`. Make sure both go into the folder we created earlier,
   and keep both of them safe!

   This command will also print out something to your terminal screen. You
   don't need to do anything with this text.

5. Check if your cluster is fully functional

   ```
   kubectl get node
   ```

   The response should list three running nodes and their Kubernetes versions!
   Each node should have the status of `Ready`, note that this may take a
   few moments.

Congrats. Now that you have your Kubernetes cluster running, it's time to
begin {ref}`setup-helm`.
