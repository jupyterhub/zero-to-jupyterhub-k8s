# How to Deploy #

## Google Cloud Engine ##

Log into the gcloud console: [console.cloud.google.com](console.cloud.google.com/)

Create a cluster. Go to `Container Engine` > `Container clusters` > `+ Create Cluster`. Fill out the required information and make sure you know how many instances you will need and what the memory and cpu requirements will be.

Go back to your dashboard in the GCP console. Click `Activate Google Cloud Shell` in the upper right-hand corner. It is an icon that looks like a small terminal.

In the new terminal window that popped up, clone the jupyterhub-k8s repository.

```
$ git clone https://github.com/data-8/jupyterhub-k8s.github.com
```

Set the zone.
```
gcloud config set compute/zone <your zone>
```

Get credentials for your cluster
```
gcloud container clusters get-credentials dev
```

Edit the docker-settings.json file. Set the docker repo name corresponding to your cloud provider. Set the image types. You can leave this blank if you are only using the base image. Set the context prefix to whatever you want.

Here is an example:
```
{
    "buildSettings": {
        "dockerRepo": {
            "gcloud": "gcr.io/data-8",
            "azure": "data8-on.azurecr.io/data-8"
        },
        "imageTypes": ",datahub,prob140,stat28"
    },
    "populateSettings": {
        "contextPrefix": "gke_data-8_us-central1-a_"
    }
}
```

Run Build
```
$ ./build.bash <'hub' or 'user' or 'proxy'> <image type>
```

Run the populate command that build.bash spits out and keep track of the image tag that it lists at the end of the populate command string.

Edit the `helm-chart/values.yaml` file where it says `# Must be overridden`. Set the image tags to the tags of the docker images you just built using `./build.bash`. Also make sure to set the correct docker images. You may also adjust some of the other settings in the `values.yaml` file if necessary.

[Install helm](https://github.com/kubernetes/helm/blob/master/docs/install.md)

Run helm
```
helm init

helm --kube-context=<your context prefix><'dev' or 'prod'> install ./helm-chart
```

Later, when you want to change your deployment run:
```
helm list

helm --kube-context=<your context prefix><'dev' or 'prod'> upgrade <release name> ./helm-chart
```

Congragulations! You just deployed your own jupyterhub cluster using kubernetes! :D


