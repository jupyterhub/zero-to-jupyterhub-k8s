# Image-Awaiter

## What is the image-awaiter?

The image awaiter works in conjunction with a daemonset that will schedule pods
that pull images to all nodes. It works by repeatedly checking the daemonset's
pods are ready, and exits when they are.

## Why would one use it?

Because it can delay the hub to be upgraded before the relevant images are made
available, and that can for large images cut down startup time from almost ten
minutes to a few seconds.

## FAQ

### What technical knowledge is needed to understand this?

You need to know about [Kubernetes Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/) and [Kubernetes DaemonSets](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/), about [Helm and helm hooks](https://helm.sh/docs/topics/charts_hooks/),
and about the programming language Go.

### Why is this project in Go? Isn't the Jupyter Infrastructure ecosystem mostly Python?

The size of the image needed to run this image-awaiter needs to be as small as possible in order
to improve `helm upgrade` and `helm install` performance. If the image was large,
all `helm upgrades` might have to wait for the big image to be pulled, even if no
image pulling needs to happen. This makes for a slow user experience.

We <3 python, but the smallest image with the `kubernetes` python library installed
is about 116MB, and the smallest Python image is about 36MB. This Go image is only
about 4MB, which is almost an order of magnitude smaller. This is the primary reason
Go is used.

### Why is the Go Kubernetes library not used here?

It is currently [hard to depend on](https://github.com/kubernetes/client-go/blob/HEAD/INSTALL.md)
in small Go projects. Once that situation changes, we'll simplify our code by switching
to it.
