# Running a Code Server Notebook from JupyterHub

## What this is

Instead of running a traditional Jupyter Notebook or Jupyter Lab Docker image
via JupyterHub, you can run a Docker image designed to run
[Code Server](https://github.com/cdr/code-server). Code Server is a version
of Visual Server Code that runs inside of a browser. The Code Server project
patches the VS Code codebase (which is already mostly Node.js-based)
such that it can run as a webservice.

## Why this is useful

JupyterHub in Kubernetes can be used to spawn independent Code Server pods
on a per-user basis, so that each user can have their own copy of Visual
Studio Code running inside of a container in a Kubernetes cluster. This can
allow users to develop in their own private environment without having a
a development environment installed on their local machine. Developers can
code exclusively in the cloud, all while using open source software.

## Building

### Building the Code Server Notebook Docker Image

You will need to have a "Code Server Notebook" Docker image with Code Server
installed and and available as a webservice. This Docker image will be used
instead of the Jupyter Lab or Notebook image. You can use an existing Code Server
Docker image, but the following guide assumes that you will be compiling it
from source.

First, you will need to checkout the Code Server codebase and select the
branch you want to build.

```bash
git clone https://github.com/cdr/code-server code-server
git checkout -b 3.4.1 tags/3.4.1
```

Next, you will need to create a Dockerfile alongside of the Git checkout.
(The Dockerfile will use the source code in the code-server directory to perform
the build.)

The below multi-stage build Dockerfile will achieve the following:

- Create a VS Code / Code Server binary as a .dep package
- Install that binary into a runtime Docker container

Dockerfile.notebook

```Dockerfile
FROM node:12 as code-server-builder
# Install build-time OS dependencies
RUN apt-get update && apt-get install -y \
    libxkbfile-dev \
    libsecret-1-dev \
    jq \
    rsync \
    gettext-base \
    dumb-init

# Install Go dependencies - used by packaging script
RUN ARCH="$(uname -m | sed 's/x86_64/amd64/; s/aarch64/arm64/')" && \
    curl -fsSL "https://dl.google.com/go/go1.14.3.linux-$ARCH.tar.gz" | tar -C /usr/local -xz
ENV PATH=/usr/local/go/bin:/root/go/bin:$PATH
ENV GO111MODULE=on
RUN go get mvdan.cc/sh/v3/cmd/shfmt
RUN go get github.com/goreleaser/nfpm/cmd/nfpm

RUN mkdir src
WORKDIR /src
COPY code-server /src/
# Steps to build and package code-server along with vscode
RUN yarn && yarn vscode && yarn build
RUN yarn build:vscode
RUN yarn release && yarn release:standalone && yarn package && mv release-packages /tmp/ && rm -r ./* && mv /tmp/release-packages/ .

# Build the Code Server Notebook image
FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    curl

# install code-server binary
COPY --from=code-server-builder /src/release-packages/code-server*.deb /tmp
RUN dpkg -i /tmp/code-server*$(dpkg --print-architecture).deb && rm /tmp/code-server*.deb

# pre-install some extensions
ENV BUILT_IN_EXTENSIONS_DIR=/usr/local/share/code-server/extensions/

# give the coder user permissions within the container
RUN mkdir -p /etc/sudoers.d
RUN adduser --gecos '' --disabled-password coder && \
  echo "coder ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/nopasswd
RUN ARCH="$(dpkg --print-architecture)" && \
    curl -fsSL "https://github.com/boxboat/fixuid/releases/download/v0.4.1/fixuid-0.4.1-linux-$ARCH.tar.gz" | tar -C /usr/local/bin -xzf - && \
    chown root:root /usr/local/bin/fixuid && \
    chmod 4755 /usr/local/bin/fixuid && \
    mkdir -p /etc/fixuid && \
    printf "user: coder\ngroup: coder\n" > /etc/fixuid/config.yml

# Run code-server on port 8888
CMD ["code-server", \
     "--bind-addr", "0.0.0.0:8888", \
     "--auth", "none", \
     "--extensions-dir", "$BUILT_IN_EXTENSIONS_DIR", \
     "--user-data-dir", "$USER_HOME/.config"]

USER coder
# Port Jupyter Notebooks webservice defaults to
EXPOSE 8888
```

To build the above, you will need to run the following Docker build steps:

 1. First, set some environment variables to name your Docker image.

    ```bash
    export NOTEBOOK_IMAGE_NAME="code-server-notebook"
    export NOTEBOOK_IMAGE_TAG="1.0.0"
    ```

 2. Next, build your docker image.

    If you are using minikube to test this process, you can avoid a Docker
    push/pull by building in minikube's Docker daemon.

    ```bash
    eval $(minikube -p minikube docker-env)
    docker build -f Dockerfile.notebook -t ${NOTEBOOK_IMAGE_NAME}:${NOTEBOOK_IMAGE_TAG} .
    ```

    Otherwise, if not using minikube, you can build and push as normal:

    ```bash
    docker build -f Dockerfile.notebook -t ${NOTEBOOK_IMAGE_NAME}:${NOTEBOOK_IMAGE_TAG} .
    docker push ${NOTEBOOK_IMAGE_NAME}:${NOTEBOOK_IMAGE_TAG}
    ```

### Extending the JupyterHub Docker Image

Dockerfile.hub

Next, we need to use the [Jupyterhub Traefik Proxy](https://github.com/jupyterhub/traefik-proxy) by extending the Docker image for Jupyterhub. We need to install
the python package for the jupyterhub-traefik-proxy.

```Dockerfile
FROM jupyterhub/k8s-hub:0.10.2

USER root
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN python3 -m pip install jupyterhub-traefik-proxy==0.1.6 && \
    python3 -m jupyterhub_traefik_proxy.install --traefik --output=/usr/local/bin
#USER jovyan

```

As before, we need to build the docker image:

 1. Set image env variables

    ```bash
    export HUB_IMAGE_NAME="code-server-hub"
    export HUB_IMAGE_TAG="1.0.0"
    ```

 2. Next, build your docker image.

    If you are using minikube to test this process, you can avoid a Docker
    push/pull by building in minikube's Docker daemon.

    ```bash
    eval $(minikube -p minikube docker-env)
    docker build -f Dockerfile.hub -t ${HUB_IMAGE_NAME}:${HUB_IMAGE_TAG} .
    ```

    Otherwise, if not using minikube, you can build and push as normal:

    ```bash
    docker build -f Dockerfile.hub -t ${HUB_IMAGE_NAME}:${HUB_IMAGE_TAG} .
    docker push ${HUB_IMAGE_NAME}:${HUB_IMAGE_TAG}
    ```

## Deploy the JupyterHub with the Code Server Notebook

Once the Docker images are built, you can deploy JupyterHub with the new
Code Server Notebook image.

This example assumes Minikube, but Minikube is not required for using Code Server
Notebooks.

1. Setup Minikube like normal

    ```bash
    # start minikube
    minikube start
    # enable ingress in minikube so we can access it
    minikube addons enable ingress
    # Set your hosts file entry for minikube so you can browse to the ingress with
    # http://minikube:80
    echo `minikube ip` minikube >> /etc/hosts
    ```

2. Create a `config.yaml` file for use with Helm. Note: you can generate the
   `config.yaml` any way you like, but this bash script is just a helper for
   this example.

    config.sh

    ```bash
    #!/bin/bash
    set -e

    RAND_KEY=`openssl rand -hex 32`
    CONFIGYAML="${CONFIGYAML:-config.yaml}"
    NOTEBOOK_IMAGE_NAME=${NOTEBOOK_IMAGE_NAME:-code-server-notebook}
    NOTEBOOK_IMAGE_TAG=${NOTEBOOK_IMAGE_TAG:-latest}
    HUB_IMAGE_NAME=${HUB_IMAGE_NAME:-code-server-hub}
    HUB_IMAGE_TAG=${HUB_IMAGE_TAG:-latest}

    cat <<EOF > $CONFIGYAML
    proxy:
      secretToken: "$RAND_KEY"

    ingress:
      hosts:
      - minikube
      enabled: true
      annotations:
        kubernetes.io/ingress.class: "nginx"

    singleuser:
      image:
        name: ${NOTEBOOK_IMAGE_NAME}
        tag: ${NOTEBOOK_IMAGE_TAG}
        # Set this when using minikube and we've built using minikube's docker daemon
        # This will save us from having to push/pull to a docker remote
        pullPolicy: Never

    hub:
      image:
        name: ${HUB_IMAGE_NAME}
        tag: ${HUB_IMAGE_TAG}
        # Set this when using minikube and we've built using minikube's docker daemon
        # This will save us from having to push/pull to a docker remote
        pullPolicy: 'Never'
      extraConfig: |
        # set JH to use the TraefikTomlProxy
        #from dss_jupyterhub_traefik import CustomTraefikTomlProxy
        from jupyterhub_traefik_proxy import TraefikTomlProxy
        # configure JupyterHub to use TraefikTomlProxy
        c.JupyterHub.proxy_class = CustomTraefikTomlProxy
        c.TraefikTomlProxy.traefik_api_url = "http://127.0.0.1:8099"
        c.TraefikTomlProxy.traefik_api_username = "admin"
        c.TraefikTomlProxy.traefik_api_password = "${RAND_KEY}"
        # c.TraefikTomlProxy.traefik_log_level = "DEBUG"  # default is INFO

    EOF
    ```

3. Deploy JupyterHub with Helm and the generated `config.yaml`:

    run.sh

    ```bash
    #!/bin/bash
    set -e
    CONFIGYAML="${CONFIGYAML:-config.yaml}"
    HELM_RELEASE="${HELM_RELEASE:-jhub}"
    NAMESPACE="${NAMESPACE:-default}"

    helm upgrade \
      --install $HELM_RELEASE jupyterhub/jupyterhub \
      --namespace $NAMESPACE \
      --version=0.9.0 \
      --values $CONFIGYAML

    ```
