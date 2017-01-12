import os
import sys

c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'

# Connect to a proxy running in a different pod
c.JupyterHub.proxy_api_ip = os.environ['PROXY_API_SERVICE_HOST']
c.JupyterHub.proxy_api_port = int(os.environ['PROXY_API_SERVICE_PORT'])

c.JupyterHub.ip = os.environ['PROXY_PUBLIC_SERVICE_HOST']
c.JupyterHub.port = int(os.environ['PROXY_PUBLIC_SERVICE_PORT'])

# the hub should listen on all interfaces, so the proxy can access it
c.JupyterHub.hub_ip = '0.0.0.0'

c.KubeSpawner.namespace = os.environ.get('POD_NAMESPACE', 'default')

# Upto 15 minutes, first pulls can be really slow because data8 user image is huge
c.KubeSpawner.start_timeout = 60 * 20

# Our simplest user image! Optimized to just... start, and be small!
c.KubeSpawner.singleuser_image_spec = os.environ['SINGLEUSER_IMAGE']

# Configure dynamically provisioning pvc
c.KubeSpawner.pvc_name_template = 'claim-{username}-{userid}'
c.KubeSpawner.user_storage_class = os.environ['SINGLEUSER_STORAGE_CLASS']
c.KubeSpawner.user_storage_access_modes = ['ReadWriteOnce']
c.KubeSpawner.user_storage_capacity = os.environ['SINGLEUSER_STORAGE_CAPACITY']

c.KubeSpawner.singleuser_uid = 1000
c.KubeSpawner.singleuser_fs_gid = 1000

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
        'mountPath': '/home/jovyan',
        'name': 'volume-{username}-{userid}'
    }
]

# Gives spawned containers access to the API of the hub
c.KubeSpawner.hub_connect_ip = os.environ['HUB_SERVICE_HOST']
c.KubeSpawner.hub_connect_port = int(os.environ['HUB_SERVICE_PORT'])

c.KubeSpawner.mem_limit = os.environ.get('SINGLEUSER_MEM_LIMIT', None)
c.KubeSpawner.mem_guarantee = os.environ.get('SINGLEUSER_MEM_GUARANTEE', None)
c.KubeSpawner.cpu_limit = os.environ.get('SINGLEUSER_CPU_LIMIT', None)
c.KubeSpawner.cpu_guarantee = os.environ.get('SINGLEUSER_CPU_GUARANTEE', None)

# Allow switching authenticators from environment variables
auth_type = os.environ['HUB_AUTH_TYPE']

if auth_type == 'google':
    c.JupyterHub.authenticator_class = 'oauthenticator.GoogleOAuthenticator'
    c.GoogleOAuthenticator.client_id = os.environ['GOOGLE_OAUTH_CLIENT_ID']
    c.GoogleOAuthenticator.client_secret = os.environ['GOOGLE_OAUTH_CLIENT_SECRET']
    c.GoogleOAuthenticator.oauth_callback_url = os.environ['GOOGLE_OAUTH_CALLBACK_URL']
    c.GoogleOAuthenticator.hosted_domain = os.environ['GOOGLE_OAUTH_HOSTED_DOMAIN']
    c.GoogleOAuthenticator.login_service = os.environ['GOOGLE_OAUTH_LOGIN_SERVICE']
elif auth_type == 'hmac':
    c.JupyterHub.authenticator_class = 'hmacauthenticator.HMACAuthenticator'
    c.HMACAuthenticator.secret_key = bytes.fromhex(os.environ['HMAC_SECRET_KEY'])

c.JupyterHub.api_tokens = {
    os.environ['CULL_JHUB_TOKEN']: 'cull',
}

# Enable admins to access user servers
c.JupyterHub.admin_access = True

c.Authenticator.admin_users = {'cull'}
