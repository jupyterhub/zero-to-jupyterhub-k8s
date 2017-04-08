# Create a Kubernetes cluster

Enter:

```
gcloud container clusters create my-cluster-name --num-nodes=3 --zone=us-central1-b
```

If you get this error:

```
ERROR: (gcloud.container.clusters.create) ResponseError: code=503, message=Project alert-result-161014 is not fully initialized with the default service accounts. Please try again later.
```

Go to this URL in browser:

`https://console.cloud.google.com/kubernetes/list`
