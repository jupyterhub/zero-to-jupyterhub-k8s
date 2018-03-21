import os
import glob
from tornado.httpclient import AsyncHTTPClient
from kubernetes import client

from z2jh import get_config, get_secret

# Configure JupyterHub to use the curl backend for making HTTP requests,
# rather than the pure-python implementations. The default one starts
# being too slow to make a large number of requests to the proxy API
# at the rate required.
AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'

# Connect to a proxy running in a different pod
c.ConfigurableHTTPProxy.api_url = 'http://{}:{}'.format(os.environ['PROXY_API_SERVICE_HOST'], int(os.environ['PROXY_API_SERVICE_PORT']))
c.ConfigurableHTTPProxy.should_start = False

# Do not shut down user pods when hub is restarted
c.JupyterHub.cleanup_servers = False

# Check that the proxy has routes appropriately setup
# This isn't the best named setting :D
c.JupyterHub.last_activity_interval = 60

# Max number of servers that can be spawning at any one time
c.JupyterHub.concurrent_spawn_limit = get_config('hub.concurrent-spawn-limit')

active_server_limit = get_config('hub.active-server-limit', None)

if active_server_limit is not None:
    c.JupyterHub.active_server_limit = int(active_server_limit)

c.JupyterHub.ip = os.environ['PROXY_PUBLIC_SERVICE_HOST']
c.JupyterHub.port = int(os.environ['PROXY_PUBLIC_SERVICE_PORT'])

# the hub should listen on all interfaces, so the proxy can access it
c.JupyterHub.hub_ip = '0.0.0.0'

c.KubeSpawner.namespace = os.environ.get('POD_NAMESPACE', 'default')

c.KubeSpawner.start_timeout = get_config('singleuser.start-timeout')

# Use env var for this, since we want hub to restart when this changes
c.KubeSpawner.singleuser_image_spec = os.environ['SINGLEUSER_IMAGE']

c.KubeSpawner.singleuser_image_pull_policy = get_config('singleuser.image-pull-policy')

c.KubeSpawner.singleuser_extra_labels = get_config('singleuser.extra-labels', {})

c.KubeSpawner.singleuser_uid = get_config('singleuser.uid')
c.KubeSpawner.singleuser_fs_gid = get_config('singleuser.fs-gid')

service_account_name = get_config('singleuser.service-account-name', None)
if service_account_name:
    c.KubeSpawner.singleuser_service_account = service_account_name

c.KubeSpawner.singleuser_node_selector = get_config('singleuser.node-selector')
# Configure dynamically provisioning pvc
storage_type = get_config('singleuser.storage.type')
if storage_type == 'dynamic':
    pvc_name_template = get_config('singleuser.storage.dynamic.pvc-name-template')
    volume_name_template = get_config('singleuser.storage.dynamic.volume-name-template')
    c.KubeSpawner.pvc_name_template = pvc_name_template
    c.KubeSpawner.user_storage_pvc_ensure = True
    storage_class = get_config('singleuser.storage.dynamic.storage-class', None)
    if storage_class:
        c.KubeSpawner.user_storage_class = storage_class
    c.KubeSpawner.user_storage_access_modes = get_config('singleuser.storage.dynamic.storage-access-modes')
    c.KubeSpawner.user_storage_capacity = get_config('singleuser.storage.capacity')

    # Add volumes to singleuser pods
    c.KubeSpawner.volumes = [
        {
            'name': volume_name_template,
            'persistentVolumeClaim': {
                'claimName': pvc_name_template
            }
        }
    ]
    c.KubeSpawner.volume_mounts = [
        {
            'mountPath': get_config('singleuser.storage.home_mount_path'),
            'name': volume_name_template
        }
    ]
elif storage_type == 'static':
    pvc_claim_name = get_config('singleuser.storage.static.pvc-name')
    c.KubeSpawner.volumes = [{
        'name': 'home',
        'persistentVolumeClaim': {
            'claimName': pvc_claim_name
        }
    }]

    c.KubeSpawner.volume_mounts = [{
        'mountPath': get_config('singleuser.storage.home_mount_path'),
        'name': 'home',
        'subPath': get_config('singleuser.storage.static.sub-path')
    }]

c.KubeSpawner.volumes.extend(get_config('singleuser.storage.extra-volumes', []))
c.KubeSpawner.volume_mounts.extend(get_config('singleuser.storage.extra-volume-mounts', []))

lifecycle_hooks = get_config('singleuser.lifecycle-hooks')
if lifecycle_hooks:
    c.KubeSpawner.singleuser_lifecycle_hooks = lifecycle_hooks

init_containers = get_config('singleuser.init-containers')
if init_containers:
    c.KubeSpawner.singleuser_init_containers.extend(init_containers)

# Gives spawned containers access to the API of the hub
c.KubeSpawner.hub_connect_ip = os.environ['HUB_SERVICE_HOST']
c.KubeSpawner.hub_connect_port = int(os.environ['HUB_SERVICE_PORT'])

c.JupyterHub.hub_connect_ip = os.environ['HUB_SERVICE_HOST']
c.JupyterHub.hub_connect_port = int(os.environ['HUB_SERVICE_PORT'])

c.KubeSpawner.mem_limit = get_config('singleuser.memory.limit')
c.KubeSpawner.mem_guarantee = get_config('singleuser.memory.guarantee')
c.KubeSpawner.cpu_limit = get_config('singleuser.cpu.limit')
c.KubeSpawner.cpu_guarantee = get_config('singleuser.cpu.guarantee')

# Allow switching authenticators easily
auth_type = get_config('auth.type')
email_domain = 'local'

if auth_type == 'google':
    c.JupyterHub.authenticator_class = 'oauthenticator.GoogleOAuthenticator'
    c.GoogleOAuthenticator.client_id = get_config('auth.google.client-id')
    c.GoogleOAuthenticator.client_secret = get_config('auth.google.client-secret')
    c.GoogleOAuthenticator.oauth_callback_url = get_config('auth.google.callback-url')
    c.GoogleOAuthenticator.hosted_domain = get_config('auth.google.hosted-domain')
    c.GoogleOAuthenticator.login_service = get_config('auth.google.login-service')
    email_domain = get_config('auth.google.hosted-domain')
elif auth_type == 'github':
    c.JupyterHub.authenticator_class = 'oauthenticator.GitHubOAuthenticator'
    c.GitHubOAuthenticator.oauth_callback_url = get_config('auth.github.callback-url')
    c.GitHubOAuthenticator.client_id = get_config('auth.github.client-id')
    c.GitHubOAuthenticator.client_secret = get_config('auth.github.client-secret')
    org_whitelist = get_config('auth.github.org_whitelist', [])
    if len(org_whitelist) != 0:
        c.GitHubOAuthenticator.github_organization_whitelist = org_whitelist
elif auth_type == 'cilogon':
    c.JupyterHub.authenticator_class = 'oauthenticator.CILogonOAuthenticator'
    c.CILogonOAuthenticator.oauth_callback_url = get_config('auth.cilogon.callback-url')
    c.CILogonOAuthenticator.client_id = get_config('auth.cilogon.client-id')
    c.CILogonOAuthenticator.client_secret = get_config('auth.cilogon.client-secret')
elif auth_type == 'gitlab':
    c.JupyterHub.authenticator_class = 'oauthenticator.gitlab.GitLabOAuthenticator'
    c.GitLabOAuthenticator.oauth_callback_url = get_config('auth.gitlab.callback-url')
    c.GitLabOAuthenticator.client_id = get_config('auth.gitlab.client-id')
    c.GitLabOAuthenticator.client_secret = get_config('auth.gitlab.client-secret')
elif auth_type == 'mediawiki':
    c.JupyterHub.authenticator_class = 'oauthenticator.mediawiki.MWOAuthenticator'
    c.MWOAuthenticator.client_id = get_config('auth.mediawiki.client-id')
    c.MWOAuthenticator.client_secret = get_config('auth.mediawiki.client-secret')
    c.MWOAuthenticator.index_url = get_config('auth.mediawiki.index-url')
elif auth_type == 'globus':
    c.JupyterHub.authenticator_class = 'oauthenticator.globus.GlobusOAuthenticator'
    c.GlobusOAuthenticator.oauth_callback_url = get_config('auth.globus.callback-url')
    c.GlobusOAuthenticator.client_id = get_config('auth.globus.client-id')
    c.GlobusOAuthenticator.client_secret = get_config('auth.globus.client-secret')
    c.GlobusOAuthenticator.identity_provider = get_config('auth.globus.identity-provider', '')
elif auth_type == 'hmac':
    c.JupyterHub.authenticator_class = 'hmacauthenticator.HMACAuthenticator'
    c.HMACAuthenticator.secret_key = bytes.fromhex(get_config('auth.hmac.secret-key'))
elif auth_type == 'dummy':
    c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'
    c.DummyAuthenticator.password = get_config('auth.dummy.password', None)
elif auth_type == 'tmp':
    c.JupyterHub.authenticator_class = 'tmpauthenticator.TmpAuthenticator'
elif auth_type == 'lti':
    c.JupyterHub.authenticator_class = 'ltiauthenticator.LTIAuthenticator'
    c.LTIAuthenticator.consumers = get_config('auth.lti.consumers')
elif auth_type == 'custom':
    # full_class_name looks like "myauthenticator.MyAuthenticator".
    # To create a docker image with this class availabe, you can just have the
    # following Dockerifle:
    #   FROM jupyterhub/k8s-hub:v0.4
    #   RUN pip3 install myauthenticator
    full_class_name = get_config('auth.custom.class-name')
    c.JupyterHub.authenticator_class = full_class_name
    auth_class_name = full_class_name.rsplit('.', 1)[-1]
    auth_config = c[auth_class_name]
    auth_config.update(get_config('auth.custom.config') or {})
else:
    raise ValueError("Unhandled auth type: %r" % auth_type)

auth_scopes = get_config('auth.scopes')
if auth_scopes:
    c.OAuthenticator.scope = auth_scopes

c.Authenticator.enable_auth_state = get_config('auth.state.enabled', False)

def generate_user_email(spawner):
    """
    Used as the EMAIL environment variable
    """
    return '{username}@{domain}'.format(
        username=spawner.user.name, domain=email_domain
    )

def generate_user_name(spawner):
    """
    Used as GIT_AUTHOR_NAME and GIT_COMMITTER_NAME environment variables
    """
    return spawner.user.name

c.KubeSpawner.environment = {
    'EMAIL': generate_user_email,
    # git requires these committer attributes
    'GIT_AUTHOR_NAME': generate_user_name,
    'GIT_COMMITTER_NAME': generate_user_name
}

c.KubeSpawner.environment.update(get_config('singleuser.extra-env', {}))

# Enable admins to access user servers
c.JupyterHub.admin_access = get_config('auth.admin.access')
c.Authenticator.admin_users = get_config('auth.admin.users', [])
c.Authenticator.whitelist = get_config('auth.whitelist.users', [])

c.JupyterHub.base_url = get_config('hub.base_url')

c.JupyterHub.services = []

if get_config('cull.enabled', False):
    cull_timeout = get_config('cull.timeout')
    cull_every = get_config('cull.every')
    cull_cmd = [
        '/usr/local/bin/cull_idle_servers.py',
        '--timeout=%s' % cull_timeout,
        '--cull-every=%s' % cull_every,
        '--url=http://127.0.0.1:8081' + c.JupyterHub.base_url + 'hub/api'
    ]
    if get_config('cull.users'):
        cull_cmd.append('--cull-users')
    c.JupyterHub.services.append({
        'name': 'cull-idle',
        'admin': True,
        'command': cull_cmd,
    })

for name, service in get_config('hub.services', {}).items():
    api_token = get_secret('services.token.%s' % name)
    # jupyterhub.services is a list of dicts, but
    # in the helm chart it is a dict of dicts for easier merged-config
    service.setdefault('name', name)
    if api_token:
        service['api_token'] = api_token
    c.JupyterHub.services.append(service)


c.JupyterHub.db_url = get_config('hub.db_url')

cmd = get_config('singleuser.cmd', None)
if cmd:
    c.Spawner.cmd = cmd

default_url = get_config('singleuser.default-url', None)
if default_url:
    c.Spawner.default_url = default_url

cloud_metadata = get_config('singleuser.cloud-metadata', {})

if not cloud_metadata.get('enabled', False):
    # Use iptables to block access to cloud metadata by default
    network_tools_image_name = get_config('singleuser.network-tools.image.name')
    network_tools_image_tag = get_config('singleuser.network-tools.image.tag')
    ip_block_container = client.V1Container(
        name="block-cloud-metadata",
        image=f"{network_tools_image_name}:{network_tools_image_tag}",
        command=[
            'iptables',
            '-A', 'OUTPUT',
            '-d', cloud_metadata.get('ip', '169.254.169.254'),
            '-j', 'DROP'
        ],
        security_context=client.V1SecurityContext(
            privileged=True,
            run_as_user=0,
            capabilities=client.V1Capabilities(add=['NET_ADMIN'])
        )
    )

    c.KubeSpawner.singleuser_init_containers.append(ip_block_container)

scheduler_strategy = get_config('singleuser.scheduler-strategy', 'spread')

if scheduler_strategy == 'pack':
    # FIXME: Support setting affinity directly in KubeSpawner
    c.KubeSpawner.singleuser_extra_pod_config = {
        'affinity': {
            'podAffinity': {
                'preferredDuringSchedulingIgnoredDuringExecution': [{
                    'weight': 50,
                    'podAffinityTerm': {
                        'labelSelector': {
                            'matchExpressions': [{
                                'key': 'component',
                                'operator': 'In',
                                'values': ['hub']
                            }]
                        },
                        'topologyKey': 'kubernetes.io/hostname'
                    }
                }, {
                    'weight': 5,
                    'podAffinityTerm': {
                        'labelSelector': {
                            'matchExpressions': [{
                                'key': 'component',
                                'operator': 'In',
                                'values': ['singleuser-server']
                            }]
                        },
                        'topologyKey': 'kubernetes.io/hostname'
                    }
                }],
            }
        }
    }
else:
    # Set default to {} so subconfigs can easily update it
    c.KubeSpawner.singleuser_extra_pod_config = {}

extra_configs = sorted(glob.glob('/etc/jupyterhub/config/hub.extra-config.*.py'))
for ec in extra_configs:
    load_subconfig(ec)
