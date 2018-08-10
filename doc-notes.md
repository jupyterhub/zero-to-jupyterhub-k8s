index

creating your kubernetes cluster:
    creating your cluster OK
        zero-gke OK

creating your jupyterhub:
    Getting Started OK
    Setting up Helm OK
    Setting up JupyterHub OK
    Tearing down everything OK

Customization guide
    Customizing your deployment (extending) OK
    
    Customizing the User Environment
        user jupyterlab by default OK
        use an existing docker image OK
        set env variables
        pre-populating users home dir (THINK THROUGH)
        build a custom docker image with repo2docker (RELOCATE!)

    Customizing User Resources
        ser user memory and cpu guarantees/limits
        modifying user storage type and size
        expanding and contracting the size of your cluster

    Customizing User Storage
        how can this process break down
        configuration
        torn off per-user persistent storage

    Customizing User Management
        culling user pods
        admin users
        authenticating users

EDUCATION SECTION?

schema.yaml fix