index - Zero to JupyterHub with Kubernetes



# Setup a Kubernetes Cluster
- create-k8s-cluster        OK
    - step-zero-gcp         OK
    - step-zero-azure       --
    - step-zero-aws         --
    - step-zero-openshift   --



# Setup JupyterHub
- getting-started           OK Getting Started
- setup-helm                OK Setting up Helm
- setup-jupyterhub          OK Setting up JupyterHub  
- turn-off                  OK Tearing Everything Down



# Customization Guide
- extending-jupyterhub      OK Customizing your Deployment

- user-environment          () Customizing User Environment
    _ use an existing docker image OK --- Position 1
    _ user jupyterlab by default OK --- Position 2
    _ build off existing docker images --- Position 3
    _ set env variables --- Position 4
    _ pre-populating users home dir (THINK THROUGH) --- Position 5
    _ build a custom docker image with repo2docker --- Position last, add disclaimers about limitations

- user-resources            () Customizing User Resources
    _ set user memory and cpu guarantees/limits
    _ modifying user storage type and size
    _ expanding and contracting the size of your cluster

- user-storage              () Customizing User Storage
    _ how can this process break down
    _ configuration
    _ turn off per-user persistent storage

- user-management           () Customizing User Management
    _ culling user pods   
    _ admin users         
    _ authenticating users



# Administrator guide
- architecture              () The JupyterHub Architecture
- debug                     () Debugging Kubernetes
- authentication            () Authentication
- optimization              () Speed and Optimization
- security                  () Security
- upgrading                 () Upgrading your Helm chart
- troubleshooting           () FAQ
- advanced                  () Advanced Topics
- cost                      () Appendix: Projecting deployment costs



# Community section
- additional-resources      () Community-authored documentation
- users-list                () Zero to JupyterHub Gallery of Deployments
- tips                      () Tips and command snippets



# Reference
- reference                 () Configuration Reference
- 

- reference-docs            () Official JupyterHub and Project Jupyter Documentation
    _ JupyterHub
        _ Spawner
        _ Auth
    _ KubeSpawner
    _ nbgitpuller


- tools                     () Tools used in a JupyterHub Deployment
    _ Cloud Computing Providers
    _ Container Technology
    _ Kubernetes
    _ Helm
    _ JupyterHub

- glossary                  OK

EDUCATION SECTION?

schema.yaml fix