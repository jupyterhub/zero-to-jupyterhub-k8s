.. _debug:

Debugging
=========

Sometimes your JupyterHub deployment doesn't behave the way you'd expect.
This section provides some tips on debugging and fixing some common problems.

Debugging commands
------------------
In order to debug your JupyterHub deployment, you need to be able to inspect
the state of the resources being used. The following are a few common commands
for debugging.

**Real world scenario:** Let's say you've got a JupyterHub deployed, and a user
tells you that they are experiencing strange behavior. Let's take a look
at our deployment to figure out what is going on.

.. note::

   For our real world scenario, we'll assume that our Kubernetes namespace
   is called ``jhub``. Your namespace may be called something different

``kubectl get pod``
~~~~~~~~~~~~~~~~~~~
To list all pods in your Kubernetes deployment::

    kubectl --namespace=jhub get pod

This will output a list of all pods being used in the deployment.

**Real world scenario:** In our case, we see two pods for the JupyterHub
infrastructure (``hub`` and ``proxy``) as well as one user
pod that was created when somebody logged in to the JupyterHub.

Here's an example of the output::

    $ kubectl --namespace=jhub get pod
    NAME                                READY     STATUS         RESTARTS   AGE
    hub-3311438805-xnfvp     1/1       Running        0          2m
    jupyter-choldgraf                   0/1       ErrImagePull   0          25s
    proxy-1227971824-mn2wd   1/1       Running        0          5h

Here we can see the two JupyterHub pods, as well as a single user pod. Note
that all user pods will begin with ``jupyter-``.

In particular, keep an eye on the ``STATUS`` column. If a given
pod contains something other than ``Running``, then something may be wrong.

In this case, we can see that our user's pod is in the ``ErrImagePull`` state.
This generally means that there's something wrong with the Docker image that
is defined in ``singleuser`` in our helm chart config. Let's dig further...

``kubectl describe pod``
~~~~~~~~~~~~~~~~~~~~~~~~
To see more detail about the state of a specific pod, use the following
command::

    kubectl --namespace=jhub describe pod <POD_NAME>

This will output several pieces of information, including configuration and
settings for the pod. The final section you'll see is a list of recent
events. These can be particularly informative, as often an error will
show up in this section.

**Real world scenario:** In our case, one of the lines in the events page
displays an error::

      $ kubectl --namespace=jhub describe pod jupyter-choldgraf
      ...
      2m            52s             4       kubelet, gke-jhubtest-default-pool-52c36683-jv6r        spec.containers{notebook}       Warning         Failed           Failed to pull image "jupyter/scipy-notebook:v0.4": rpc error: code = 2 desc = Error response from daemon: {"message":"manifest for jupyter/scipy-notebook:v0.4 not found"}
      ...

It seems there is indeed something wrong with the Docker image. Let's confirm
this by getting another view on the events that have transpired in the pod.

``kubectl logs``
~~~~~~~~~~~~~~~~
If you only want to see the latest logs for a pod, use the following command::

    kubectl --namespace=jhub logs <POD_NAME>

This will show you the logs from the pod, which often contain useful
information about what is going wrong. Parse these logs
to see if something is generating an error.

**Real world scenario:** In our case, we get this line back::

    $ kubectl --namespace=jhub logs jupyter-choldgraf
    Error from server (BadRequest): container "notebook" in pod "jupyter-choldgraf" is waiting to start: trying and failing to pull image

Now we are sure that something is wrong with our Dockerfile. Let's check
our ``config.yaml`` file for the section where we specify the user's
Docker image. Here we see our problem::

  singleuser:
    image:
      name: jupyter/scipy-notebook

We haven't specified a ``tag`` for our Docker image! Not specifying a tag
will cause it to default to ``v0.4``, which isn't what we want and is causing
the pod to fail.

To fix this, let's add a tag to our ``config.yaml`` file::

  singleuser:
    image:
      name: jupyter/scipy-notebook
      tag: ae885c0a6226

Then run a helm upgrade::

    helm upgrade --cleanup-on-fail jhub jupyterhub/jupyterhub --version=v0.6 -f config.yaml

where ``jhub`` is the helm release name (substitute the release name that you
chose during setup).

.. note::

   Depending on the size of the Docker image, this may take a while to complete.

Right after you run this command, let's once again list the pods in our
deployment::

  $ kubectl --namespace=jhub get pod
  NAME                                READY     STATUS              RESTARTS   AGE
  hub-2653507799-r7wf8     0/1       ContainerCreating   0          31s
  hub-3311438805-xnfvp     1/1       Terminating         0          14m
  jupyter-choldgraf                   0/1       ImagePullBackOff    0          12m
  proxy-deployment-1227971824-mn2wd   1/1       Running             0          5h

Here we can see one ``hub`` pod being destroyed, and another (based
on the upgraded helm chart) being created. We also see our broken user pod,
which will not be deleted automatically. Let's manually delete it so a newer
working pod can be started.::

    $ kubectl --namespace=jhub delete pod jupyter-choldgraf

Finally, we'll tell our user to log back in to the JupyterHub. Then let's
list our running pods once again::

  $ kubectl --namespace=jhub get pod
  NAME                                READY     STATUS    RESTARTS   AGE
  hub-2653507799-r7wf8     1/1       Running   0          3m
  jupyter-choldgraf                   1/1       Running   0          18s
  proxy-deployment-1227971824-mn2wd   1/1       Running   0          5h

And now we see that we have a running user pod!

Note that many debugging situations are not as straightforward as this one.
It will take some time before you get a feel for the errors that Kubernetes
may throw at you, and how these are tied to your configuration files.

Troubleshooting Examples
------------------------
The following sections contain some case studies that illustrate some of the
more common bugs / gotchas that you may experience using JupyterHub with
Kubernetes.

Hub fails to start
~~~~~~~~~~~~~~~~~~

**Symptom:** following ``kubectl get pod``, the ``hub`` pod is in
``Error`` or ``CrashLoopBackoff`` state, or appears to be running but accessing
the website for the JupyterHub returns an error message in the browser).

**Investigating:** the output of ``kubectl --namespace=jhub logs
hub...`` shows something like::

  File "/usr/local/lib/python3.5/dist-packages/jupyterhub/proxy.py", line 589, in get_all_routes
    resp = yield self.api_request('', client=client)
  tornado.httpclient.HTTPError: HTTP 403: Forbidden

**Diagnosis:** This is likely because the ``hub`` pod cannot
communicate with the proxy pod API, likely because of a problem in the
``secretToken`` that was put in ``config.yaml``.

**Fix:** Follow these steps:

1. Create a secret token::

    openssl rand -hex 32

2. Add the token to ``config.yaml`` like so::

    proxy:
       secretToken: '<output of `openssl rand -hex 32`>'

3. Redeploy the helm chart::

    helm upgrade --cleanup-on-fail jhub jupyterhub/jupyterhub -f config.yaml
