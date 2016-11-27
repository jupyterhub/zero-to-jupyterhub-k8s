import os
import sys

sys.path.insert(0, '/srv/oauthenticator')

c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'

# Connect to a proxy running in a different pod
c.JupyterHub.proxy_api_ip = os.environ['PROXY_API_SERVICE_HOST']
c.JupyterHub.proxy_api_port = int(os.environ['PROXY_API_SERVICE_PORT'])
c.JupyterHub.proxy_cmd = '/usr/local/bin/nchp'

c.JupyterHub.ip = os.environ['PROXY_PUBLIC_SERVICE_HOST']
c.JupyterHub.port = int(os.environ['PROXY_PUBLIC_SERVICE_PORT'])

# the hub should listen on all interfaces, so the proxy can access it
c.JupyterHub.hub_ip = '0.0.0.0'

c.KubeSpawner.namespace = os.environ.get('POD_NAMESPACE', 'default')

# Upto 15 minutes, first pulls can be really slow because data8 user image is huge
c.KubeSpawner.start_timeout = 60 * 20

# Our simplest user image! Optimized to just... start, and be small!
c.KubeSpawner.singleuser_image_spec = 'data8/jupyterhub-k8s-user:master'

# Configure dynamically provisioning pvc
c.KubeSpawner.pvc_name_template = 'claim-{username}-{userid}'
c.KubeSpawner.user_storage_class = 'gce-standard-storage'
c.KubeSpawner.user_storage_access_modes = ['ReadWriteOnce']
c.KubeSpawner.user_storage_capacity = '10Gi'

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

# Gives spawned containers access to the API of the hub
c.KubeSpawner.hub_connect_ip = os.environ['HUB_SERVICE_HOST']
c.KubeSpawner.hub_connect_port = int(os.environ['HUB_SERVICE_PORT'])

# Do not use any authentication at all
c.JupyterHub.authenticator_class = 'oauthenticator.GoogleOAuthenticator'
c.GoogleOAuthenticator.client_id = os.environ['GOOGLE_OAUTH_CLIENT_ID']
c.GoogleOAuthenticator.client_secret = os.environ['GOOGLE_OAUTH_CLIENT_SECRET']
c.GoogleOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']
c.GoogleOAuthenticator.hosted_domain = 'berkeley.edu'
c.GoogleOAuthenticator.login_service = 'UC Berkeley'

c.JupyterHub.api_tokens = {
    os.environ['CULL_JHUB_TOKEN']: 'cull',
}

c.Authenticator.admin_users = {'cull'}
