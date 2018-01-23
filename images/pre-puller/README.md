# Image Pre-Puller

## What?
A small go program that does the following:

1. Check if the given list of images already exist on all scheduleable nodes.
   If they do, exit!
2. If they don't, create a deamonset (the spec for which is passed in
   as the `daemonset-spec` commandline parameter)
3. Check every 2s if the images are present in all scheduleable nodes.
4. Once image is in all schedulable nodes, kill the daemonset created in (2) and exit

## Why?

This is used as a [helm hook](https://github.com/kubernetes/helm/blob/master/docs/charts_hooks.md)
to wait for the user images to be present on all nodes before we restart the
hub. This cuts down the amount of time it takes for a user server to start,
since the image no longer needs to be pulled. For large images this can cut down
startup time from almost ten minutes to a few seconds.

## Why Go?

The role of this program is to run as a pod whenever the user is running `helm
install` or `helm upgrade` and help pull in larger images. The image that this
program requires to run must be as small as possible - it is unideal to pull in
a multi hundred megabyte image first to check if more images need to be pulled
in. This is particularly bad in the `helm upgrade` case when new images to *not*
need to be pulled in - then we end up pulling in a multi-hundred mb image that
then just exits pretty much immediately.

This gives us a few choices:

1. Bash
2. Go
3. Rust

All these can produce images < 10MB. Originally this was in Bash, but it very
quickly became hard to maintain (since we need to set up TLS and talk to a JSON
HTTP API & munge the resulting JSON). There was very little error handling code,
and extending it was very bad. This made it clear it needed to be in a real
programming language. Go is a little bit more 'mature' now than Rust is, and so
was chosen.
