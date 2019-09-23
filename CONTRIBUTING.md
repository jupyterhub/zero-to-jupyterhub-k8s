# Contributing

Welcome! As a [Jupyter](https://jupyter.org) project, we follow the [Jupyter
contributor
guide](https://jupyter.readthedocs.io/en/latest/contributor/content-contributor.html).

## Local development for a code contribution

### Prepare git

1. Install [git](https://www.git-scm.com/). To verify it is installed, run this
   from a terminal.

   ```bash
   git version
   ```

1. Make a GitHub fork of [this
   repository](https://github.com/jupyterhub/zero-to-jupyterhub-k8s) by creating
   and then logging into your GitHub account and clicking the Fork button.

1. Clone your fork to your local computer.

   ```bash
   git clone http://github.com/<YOUR-GITHUB-USERNAME>/zero-to-jupyterhub-k8s.git
   cd zero-to-jupyterhub-k8s

   # make it easy to reference the projects GitHub repository as "upstream"
   git remote add upstream https://github.com/jupyterhub/zero-to-jupyterhub-k8s

   # make it obvious what you reference by renaming a reference to your
   # personal GitHub repository to "fork"
   git remote rename origin fork
   ```

### Prepare Virtual Machine software

A `Vagrantfile` is a way to prepare a Virtual Machine (VM), and we [have
one](Vagrantfile) to prepare a VM for local development! We can use it to get
a VM up and running, enter it with SSH, develop and run tests, and later shut
down without influencing our system.

1. Install VirtualBox by [downloading and running an
   installer](https://www.virtualbox.org/wiki/Downloads).

1. Install Vagrant by [downloading and running an
   installer](https://www.vagrantup.com/downloads.html).

### Develop and run tests

1. Start a prepared VM and SSH into it.

   ```bash
   ## if you have suspended a VM earlier, use "vagrat resume" instead
   vagrant up

   ## enter a SSH session with the VM
   vagrant ssh
   ```

2. Develop and test within the VM
   
   ```bash
   ## run within the SSH session
   cd zero-to-jupyterhub-k8s
   
   ## initialize some environment variables etc (notice the leading dot)
   . ./dev init

   ## start a k8s cluster
   ./dev start-k8s

   ## install/upgrade the helm chart
   ./dev upgrade

   ## see the results
   # visit http://localhost:8090

   ## make a change
   # ...

   ## run tests
   ./dev test
   ```
  
3. Close the SSH session

   ```bash
   ## exit the SSH session
   exit
   vagrant suspend
   # vagrant halt
   # vagrant destroy
   ```

> **NOTE:** You can also use `vagrant destroy` to reset the VM state entirely,
> but the start-k8s script will reset the k8s cluster if you have the same k8s
> version set as previous so it should be fine to just `halt` and do `up` again
> later.

### Debugging issues

Various things can go wrong while working with the local development
environment, here are some typical issues and what to do about them.

#### Network errors

Did you get an error like one of these below?

```shell
# while installing docker
curl: (6) Could not resolve host: download.docker.com

# while running pip install
Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x7f420fd81080>: Failed to establish a new connection: [Errno -3] Temporary failure in name resolution',)': /simple/chartpress/

# while running apt-get install while building a docker image with chartpress
E: Failed to fetch http://archive.ubuntu.com/ubuntu/pool/main/r/rtmpdump/librtmp1_2.4+20151223.gitfa8646d.1-1_amd64.deb  Could not connect to archive.ubuntu.com:80 (91.189.88.174). - connect (113: No route to host) Could not connect to archive.ubuntu.com:80 (91.189.88.31). - connect (113: No route to host) [IP: 91.189.88.174 80]
# [...]
subprocess.CalledProcessError: Command '['docker', 'build', '-t', 'jupyterhub/k8s-hub:0.9-217f798', 'images/hub', '--build-arg', 'JUPYTERHUB_VERSION=git+https://github.com/jupyterhub/jupyterhub@master']' returned non-zero exit status 100.

# while installing a dependency for our k8s cluster
Unable to connect to the server: dial tcp: lookup docs.projectcalico.org on 127.0.0.53:53: read udp 127.0.0.1:56409->127.0.0.53:53: i/o timeout
```

Network and DNS issues are typically symptoms of unreliable internet (as
experienced by the VirtualMachine). You can recognize such issues if you get
errors like the ones above.

As you may notice, typical keywords associated with network errors are:

- *resolve host*
- *name resolution*
- *timeout*
- *no route to host*

#### Unable to listen on port

Did you get an error like this?

```
Unable to listen on port 8090: Listeners failed to create with the following errors: [Unable to create listener: Error listen tcp4 127.0.0.1:8090: bind: address already in use Unable to create listener: Error listen tcp6 [::1]:8090: bind: address already in use]
```

The key to solving this is understanding it!

We need to shuttle traffic from your computer to your Kubernetes clusters's
Service that in turn shuttle the traffic to the pod of relevance. While doing
so, we can end up with issues like the one above if we end up asking for traffic
to go to more than one place.

Let's look on how we need traffic to be shuttled!

1. *Traffic entering your computer should go to your VM.*

   When you run `vagrant up` your computer will read the
   [Vagrantfile](Vagrantfile) and from that conclude it should shuttle traffic
   incoming to your computer on port `8090` to your VM on port `8080`.

2. *Traffic entering your VM should go to your Kubernetes cluster's Service named `proxy-public`.*

   When you run `./dev upgrade`, that in turn runs the `kubectl port-forward`
   command to shuttle traffic from port `8080` to the `proxy-public` Kubernetes
   Service (port `80`) that we want to communicate with, it is the gate to speak
   with the hub and proxy even though it is also possible to speak directly to
   the hub.

In short, the traffic is routed from computer (8090), to the VM (8080), to the
Kubernetes `proxy-public` Service (80).

The reason you may run into an issue if is there is another service already
listening on traffic arriving on a given port. Then you would need to either
shut it down or route traffic differently.

## Helm chart practices

We strive to follow the guidelines provided by
[kubernetes/charts](https://github.com/kubernetes/charts/blob/master/REVIEW_GUIDELINES.md)
and the [Helm chart best practices
guide](https://github.com/kubernetes/helm/tree/master/docs/chart_best_practices).
