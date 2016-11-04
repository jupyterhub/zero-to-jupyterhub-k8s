import os

c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'

# Use the nginx based proxy, rather than the nodejs one
c.JupyterHub.proxy_cmd = '/usr/local/bin/nchp'
c.JupyterHub.ip = '0.0.0.0'

c.KubeSpawner.kube_namespace = os.environ.get('POD_NAMESPACE', 'default')
c.KubeSpawner.kube_api_endpoint = 'https://{host}:{port}'.format(
    host=os.environ['KUBERNETES_SERVICE_HOST'],
    port=os.environ['KUBERNETES_SERVICE_PORT']
)
# Disable SSL Auth for now. It's not the end of the world because we
# are inside the cluster, but we should fix this by moving to kubesession
# soon! FIXME
c.KubeSpawner.kube_ca_path = False
c.KubeSpawner.start_timeout = 60 * 5  # Upto 5 minutes, first pulls can be really slow

# Our simplest user image! Optimized to just... start, and be small!
c.KubeSpawner.singleuser_image_spec = 'yuvipanda/simple-singleuser:v1'


# The spawned containers need to be able to talk to the hub, ok through the proxy!
c.KubeSpawner.hub_ip_connect = '{host}:{port}'.format(
    host=os.environ['HUB_PROXY_SERVICE_HOST'],
    port=os.environ['HUB_PROXY_SERVICE_PORT']
)

# Do not use any authentication at all
c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'

c.JupyterHub.api_tokens = {
  os.environ['CULL_JHUB_TOKEN']: 'cull',
}

c.Authenticator.admin_users = {'cull', 'derrickmar1215'}
