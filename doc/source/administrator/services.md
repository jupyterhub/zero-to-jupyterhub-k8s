(services)=

# Services

JupyterHub services (not to be confused with Kubernetes Service objects) are processes that interact with the JupyterHub API.  [nbgrader](https://nbgrader.readthedocs.io/en/stable/configuration/jupyterhub_config.html) and [culling idle Notebooks](https://github.com/jupyterhub/jupyterhub-idle-culler) are examples of production services, and there are minimal examples of "hello world" services in the [Jupyterhub examples repo](https://github.com/jupyterhub/jupyterhub/tree/master/examples).

Services can be run [externally](https://jupyterhub.readthedocs.io/en/stable/getting-started/services-basics.html) from the Hub, meaning they are started and stopped independently of the Hub and must know about things like their Hub authentication token on their own.  Alternatively, a service can be [Hub-managed](https://jupyterhub.readthedocs.io/en/stable/reference/services.html#hub-managed-services), where the Hub starts and stops the process and passes key information to the service via environment variables.

## Hub-managed services in z2jh

A Hub-managed service will run in the same container/pod as the Hub itself.  First, you'll need to install or copy the appropriate files for the service into your Hub image, either by creating a custom image derived from [`jupyterhub/k8s-hub`](https://hub.docker.com/r/jupyterhub/k8s-hub) or the [hub.extraFiles](schema_hub.extraFiles) configuration.  Keep in mind that your Hub container may need to install dependency libraries like flask or fastapi, depending on the service.  In those cases, you'll need a custom image.

In addition to the code for the service, you need to modify the Hub Kubernetes Service object to include [multiple ports](https://kubernetes.io/docs/concepts/services-networking/service/#multi-port-services), and update the Hub Network Policy.  If you want to allow access from all sources, you can use [hub.networkPolicy.allowedIngressPorts](schema_hub.networkPolicy.allowedIngressPorts).  Otherwise if you want to more precisely control access, you can use [hub.networkPolicy.ingress](schema_hub.networkPolicy.ingress).

## Example service

In the following snippet, I'm using a custom image that copies over the application code and installs the dependencies listed in the [fastapi service example](https://github.com/jupyterhub/jupyterhub/tree/master/examples/service-fastapi).  

```
# Dockerfile
# 0.11.1 is latest stable release at the time of this writing
FROM jupyterhub/k8s-hub:0.11.1

COPY ./service-fastapi /usr/src/fastapi
RUN python3 -m pip install -r /usr/src/fastapi/requirements.txt
```


```
# config.yaml

hub:
  image:
    name: myregistry/my-custom-hub-image
    tag: latest

  services:
    fastapi:
      url: http://hub:8181
      command: ["/home/jovyan/.local/bin/uvicorn", "app:app", "--port", "8181", "--host", "0.0.0.0", "--app-dir", "/usr/src/fastapi"]
      oauth_redirect_uri: "https://jupyterhub.mycloud.com/services/fastapi/oauth_callback"
      environment:
        PUBLIC_HOST: "https://jupyterhub.mycloud.com"

  networkPolicy:
    ingress:
      - ports:
        - port: 8181
        from:
          - podSelector:
              matchLabels:
                hub.jupyter.org/network-access-hub: "true"
  
  service:
    ports:
      extraPorts:
        - port: 8181
          targetPort: 8181
          name: fastapi
```          




