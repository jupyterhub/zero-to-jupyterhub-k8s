index

creating your kubernetes cluster:
    creating your cluster
        zero-gke

creating your jupyterhub:
    getting started
    setting up helm
    setting up jupyterhub
    turning off jupyterhub and computational resources

customization guide
    extending your jh setup
        applying config changes
    
    customizing user environment
        use an existing docker image
        build a custom docker image with repo2docker
        user jupyterlab by default
        set env variables
        pre-populating users home dir

    user resources
        ser user memory and cpu guarantees/limits
        modifying user storage type and size
        expanding and contracting the size of your cluster

    user storage in jupyterhub
        how can this process break down
        configuration
        torn off per-user persistent storage

    user management
        culling user pods
        admin users
        authenticating users