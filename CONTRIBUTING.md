# Contributing

Welcome! As a [Jupyter](https://jupyter.org) project, we follow the [Jupyter contributor guide](https://jupyter.readthedocs.io/en/latest/contributor/content-contributor.html).

## Local development

We recommend using [minikube](https://github.com/kubernetes/minikube) for local
development.

1. [Download & install minikube](https://github.com/kubernetes/minikube#installation)
2. Start minikube
   ```
   minikube start
   ```
3. Use the docker daemon inside minikube for building:
   ```
   eval $(minikube docker-env)
   ```
4. Clone the zero-to-jupyterhub repo:
   ```
   git clone git@github.com:jupyterhub/zero-to-jupyterhub-k8s.git
   cd zero-to-jupyterhub-k8s
   ```
5. Create a virtualenv & install the library required for builds to happen:
   ```bash
   python3 -m venv .
   pip install ruamel.yaml
   ```
 6. Now run `build.py` to build the requisite docker images inside minikube:
    ```bash
    ./build.py build
    ```

    This will build the docker images inside minikube & modify
    `jupyterhub/values.yaml` with the appropriate values to make the chart
    installable!

7. Install / Upgrade JupyterHub Chart!
   ```bash
   helm upgrade --wait --install --namespace=hub hub jupyterhub/ -f minikube-config.yaml
   ```

   You can easily change the options in `minikube-config.yaml` file to test what
   you want, or create another `config.yaml` file & pass that as an additional
   `-f config.yaml` file to the `helm upgrade` command.

8. Open the URL for your instance of JupyterHub!

   ```bash
   minikube service --namespace=hub proxy-public
   ```

8. Make the changes you want. You need to re-run step 6 if you changed anything
   under `images`, but only step 7 if you changed things only under `jupyterhub`
