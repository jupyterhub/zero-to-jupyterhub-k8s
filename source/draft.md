# Draft

This tutorial lets you set up a JupyterHub installation on a Kubernetes Cluster (on Google Cloud), using Helm for managing installation & upgrades.

Install and authenticate with the gcloud commandline tools. https://cloud.google.com/sdk/downloads has info on how to.
Create a kubernetes cluster:
gcloud container clusters create my-cluster-name --num-nodes=3 --zone=us-central1-b
Install kubectl and make sure it works:
gcloud components install kubectl
kubectl get node  (should return 3 nodes)
Install helm using https://github.com/kubernetes/helm/blob/master/docs/install.md
Clone our git repository
git  clone https://github.com/data-8/jupyterhub-k8s
Create a file called ‘config.yaml’. This will hold the various customizations we perform for our JupyterHub installation. Make the values initially be:
name: “name-of-your-hub”
hub:
   cookieSecret: “<output-of-openssl rand -hex 32>”
token:
    proxy: “<output-of-openssl rand -hex 32>”
(Note: Make sure these aren’t curly quotes in your file!)
Run `helm init` to prepare the kubernetes cluster for helm installation
Run `helm install helm-chart --name=<name-of-your-hub> --namespace=<name-of-your-hub> -f config.yaml`
You can see the pods being created with `kubectl --namespace=<name-of-your-hub> get pod`. Wait for the hub and proxy pod to get to running (the cull might be in error - ignore it for now, it’ll be fixed when https://github.com/data-8/jupyterhub-k8s/issues/143 is fixed)
You can find the IP to use for accessing the JupyterHub with `kubectl --namespace=<name-of-your-hub> get svc` - the external IP for the ‘proxy-public’ service should be accessible in a minute or two.
The default authenticator is ‘dummy’ - any username / password will let you in! 

We can explore setting other options, such as persistent storage for users, memory / cpu limits, and other authenticators now!

Common errors:

Something like “could not find default credentials. See https://developers.google.com/accounts/docs/application-default-credentials for more information.”
Do gcloud auth application-default login and follow the prompts. The link provided has other options for advanced use cases.

