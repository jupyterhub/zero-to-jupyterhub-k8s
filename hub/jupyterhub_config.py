import os

c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'

# Use the nginx based proxy, rather than the nodejs one
c.JupyterHub.proxy_cmd = '/usr/local/bin/nchp'
c.JupyterHub.ip = '0.0.0.0'

c.KubeSpawner.namespace = os.environ.get('POD_NAMESPACE', 'default')

c.KubeSpawner.start_timeout = 60 * 5  # Upto 5 minutes, first pulls can be really slow

# Our simplest user image! Optimized to just... start, and be small!
c.KubeSpawner.singleuser_image_spec = 'yuvipanda/simple-singleuser:v1'

# Configure dynamically provisioning pvc
c.KubeSpawner.pvc_name_template = 'claim-{username}-{userid}'
c.KubeSpawner.storage_class = 'gce-standard-storage'
c.KubeSpawner.access_modes = ['ReadWriteOnce']
c.KubeSpawner.storage = '10Gi'

# Add volumes to singleuser pods
c.KubeSpawner.volumes = [
    {
        'name': 'volume-{username}-{userid}',
        'persistentVolumeClaim': {
            'claimName': 'claim-{username}-{userid}'
        }
    }
]
c.KubeSpawner.volume_mounts = [
    {
        'mountPath': '/home',
        'name': 'volume-{username}-{userid}'
    }
]

# The spawned containers need to be able to talk to the hub, ok through the proxy!
c.KubeSpawner.hub_connect_ip = os.environ['HUB_PROXY_SERVICE_HOST']
c.KubeSpawner.hub_connect_port = int(os.environ['HUB_PROXY_SERVICE_PORT'])

# Do not use any authentication at all
c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'

c.JupyterHub.api_tokens = {
    os.environ['CULL_JHUB_TOKEN']: 'cull',
}

c.Authenticator.admin_users = {'cull', 'derrickmar1215'}
