# Image Image-Awaiter

## What is the image image-awaiter?

The image awaiter is designed to await a set of user-specified images to become
present on all nodes that may have user pods assigned to them. It is a small go
program that repeatedly checks if the given list of images exists on all 
scheduleable nodes and then exits.

## Why would one use it?

This is used as a [helm hook](https://github.com/kubernetes/helm/blob/master/docs/charts_hooks.md)
to wait for user images to be present on all nodes before we restart the
hub. This cuts down the amount of time it takes for a user server to start,
since the image no longer needs to be pulled. For large images this can cut down
startup time from almost ten minutes to a few seconds.

## FAQ

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

It is currently [hard to depend on](https://github.com/kubernetes/client-go/blob/master/INSTALL.md)
in small Go projects. Once that situation changes, we'll simplify our code by switching
to it.
