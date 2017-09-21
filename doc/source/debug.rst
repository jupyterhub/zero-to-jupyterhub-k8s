Debugging Kubernetes
====================

Sometimes your Kubernetes deployment doesn't behave the way you'd expect.
This section provides some tips on debugging and fixing some common problems.

Debugging commands
------------------
In order to debug your Kubernetes deployment, you need to be able to inspect
the state of the pods being used. The following are a few common commands
for debugging.

.. note::

   You may need to add ``--namespace=<YOUR_NAMESPACE>`` in order for the
   following commands to work.

**Real world scenario:** Let's say you've got a JupyterHub deployed, and a user
tells you that they are experiencing strange behavior. Let's take a look
at our deployment to figure out what is going on.

.. note::

   For our real world scenario, we'll assume that our Kubernetes namespace
   is called ``jhub``. Your namespace may be called something different

``kubectl get pod``
~~~~~~~~~~~~~~~~~~~
To list all pods in your Kubernetes deployment::

    kubectl get pod

This will output a list of all pods being used in the deployment.

**Real world scenario:** In our case, we see two pods for the JupyterHub
infrastructure (``hub-deployment`` and ``proxy-deployment``) as well as one user
pod that was created when somebody logged in to the JupyterHub.

Here's an example of the output::

    $ kubectl get pod --namespace=jhub
    NAME                                READY     STATUS         RESTARTS   AGE
    hub-deployment-3311438805-xnfvp     1/1       Running        0          2m
    jupyter-choldgraf                   0/1       ErrImagePull   0          25s
    proxy-deployment-1227971824-mn2wd   1/1       Running        0          5h

Here we can see the two JupyterHub pods, as well as a single user pod. Note
that all user pods will begin with ``jupyter-``.

In particular, keep an eye on the ``STATUS`` column. If a given
pod contains something other than ``Running``, then something may be wrong.

In this case, we can see that our user's pod is in the ``ErrImagePull`` state.
This generally means that there's something wrong with the Docker image that
is defined in ``singleuser`` in our helm chart. Let's dig further...

``kubectl describe pod``
~~~~~~~~~~~~~~~~~~~~~~~~
To see more detail about the state of a specific pod, use the following
command::

    kubectl describe pod <POD_NAME>

This will output several pieces of information, including configuration and
settings for the pod. The final section you'll see is a list of recent
events. These can be particularly informative, as often an error will
show up in this section.

**Real world scenario:** In our case, one of the lines in the events page
displays an error::

      $ kubectl describe pod jupyter-choldgraf --namespace=jhub
      ...
      2m            52s             4       kubelet, gke-jhubtest-default-pool-52c36683-jv6r        spec.containers{notebook}       Warning         Failed           Failed to pull image "jupyter/scipy-notebook:v0.4": rpc error: code = 2 desc = Error response from daemon: {"message":"manifest for jupyter/scipy-notebook:v0.4 not found"}
      ...

It seems there is indeed something wrong with the Docker image. Let's confirm
this by getting another view on the events that have transpired in the pod.

``kubectl logs``
~~~~~~~~~~~~~~~~
If you only want to see the latest logs for a pod, use the following command::

    kubectl logs <POD_NAME>

This will output a list of the recent events for the pod. Parse these logs
to see if something is generating an error.

**Real world scenario:** In our case, we get this line back::

    $ kubectl logs jupyter-choldgraf --namespace=jhub
    Error from server (BadRequest): container "notebook" in pod "jupyter-choldgraf" is waiting to start: trying and failing to pull image

Now we are sure that something is wrong with our Docker file. Let's check
our ``config.yaml`` file for the section where we specify the user's
Docker image. Here we see our problem::

  singleuser:
  image:
      name:
          jupyter/scipy-notebook

We haven't specified a ``tag`` for our Docker image! This is required in
JupyterHub and not specifying a tag will cause the image pull to fail.

To fix this, let's add a tag to our ``config.yaml`` file::

  singleuser:
  image:
      name:
          jupyter/scipy-notebook
      tag:
          ae885c0a6226

and run a helm upgrade::

    helm upgrade jhub jupyterhub/jupyterhub --version=v0.4 -f config.yaml

.. note::

   In this case our Kubernetes namespace is called ``jhub``. Yours may be
   different depending on what you chose during setup.

.. note::

   Depending on the size of the Docker image, this may take a while to complete.

Right after you run this command, let's once again list the pods in our
deployment::

  $ kubectl get pod --namespace=jhub
  NAME                                READY     STATUS              RESTARTS   AGE
  hub-deployment-2653507799-r7wf8     0/1       ContainerCreating   0          31s
  hub-deployment-3311438805-xnfvp     1/1       Terminating         0          14m
  jupyter-choldgraf                   0/1       ImagePullBackOff    0          12m
  proxy-deployment-1227971824-mn2wd   1/1       Running             0          5h

Here we can see one ``hub-deployment`` pod being destroyed, and another (based
on the upgraded helm chart) being created. We also see our broken user pod,
which will only be upgraded if it is restarted. To do this, let's delete the
user's pod::

    $ kubectl delete pod jupyter-choldgraf --namespace=jhub

Finally, we'll tell our user to log back in to the JupyterHub. Then let's
list our running pods once again::

  $ kubectl get pod --namespace=jhub
  NAME                                READY     STATUS    RESTARTS   AGE
  hub-deployment-2653507799-r7wf8     1/1       Running   0          3m
  jupyter-choldgraf                   1/1       Running   0          18s
  proxy-deployment-1227971824-mn2wd   1/1       Running   0          5h

And now we see that we have a running user pod!

Note that many debugging situations are not as straightforward as this one.
It will take some time before you get a feel for the errors that Kubernetes
may throw at you, and how these are tied to your configuration files.

Case studies in debugging Kubernetes
------------------------------------
The following sections contain some case studies that illustrate some of the
more common bugs / gotchas that you may experience using JupyterHub with
Kubernetes.

Hub fails to start
~~~~~~~~~~~~~~~~~~

**Symptom:** following ``kubectl get pod``, the ``hub-deployment`` pod is in
``Error`` or ``CrashLoopBackoff`` state, or appears to be running but is
unreachable via the web.

**Investigating:** the output of ``kubectl logs hub-deployment...`` shows something
like::
    File "/usr/local/lib/python3.5/dist-packages/jupyterhub/proxy.py", line 589, in get_all_routes
      resp = yield self.api_request('', client=client)
    tornado.httpclient.HTTPError: HTTP 403: Forbidden

**Diagnosis:** This is likely because the ``hub-deployment`` pod cannot
communicate with the proxy pod API, likely because of a problem in the
``secretToken`` that was put in ``config.yaml``.

**Fix:** Add to ``config.yaml``::

    proxy:
      secretToken: '<output of `openssl rand -hex 32`>'

Then redeploy with ``helm upgrade <my-hub> jupyterhub/jupyterhub -f my-config.yaml``.
