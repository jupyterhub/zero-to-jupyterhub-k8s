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
5. Create a virtualenv & install the libraries required for builds to happen:
   ```bash
   python3 -m venv .
   pip install -r dev-requirements.txt
   ```
 6. Now run `build.py` to build the requisite docker images inside minikube:
    ```bash
    ./build.py
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


## Releasing a new version of the Helm Chart

In order to release a new version of the Helm Chart, make sure to perform each
of the following steps:

1. Generate a release document. This should follow the structure of previous
   entries in the [CHANGELOG](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/master/CHANGELOG.md).
2. Double-check that there aren't any un-documented breaking changes.
3. If applicable, include a section in the [CHANGELOG](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/master/CHANGELOG.md)
   that contains upgrade instructions (usually only applicable for major changes to the code).
4. Generate a list of contributors since the latest release. Use the script
  in `tools/contributors.py` to list all contributions (anyone who made a
  commit or a comment)    since the latest release. Update the dates in that
  script, run it, and paste the output into the changelog. For an example,
  see [the v0.5 list of contributors](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/v0.5/CHANGELOG.md#contributors).
5. ...
