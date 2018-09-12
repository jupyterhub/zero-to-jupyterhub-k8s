import os
import glob
from tornado.httpclient import AsyncHTTPClient
from kubernetes import client

from z2jh import get_config, get_secret, set_config_if_not_none
from jupyterhub.utils import url_path_join

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
c.JupyterHub.last_activity_interval = 60

# Don't wait at all before redirecting a spawning user to the progress page
c.JupyterHub.tornado_settings = {
    'slow_spawn_timeout': 0,
}

for trait, cfg_key in (
    # Max number of servers that can be spawning at any one time
    ('concurrent_spawn_limit', 'concurrent-spawn-limit'),
    # Max number of consecutive failures before the Hub restarts itself
    # requires jupyterhub 0.9.2
    ('consecutive_failure_limit', 'consecutive-failure-limit'),
    # Max number of servers to be running at one time
    ('active_server_limit', 'active-server-limit'),
):
    set_config_if_not_none(c.JupyterHub, trait, 'hub.' + cfg_key)

c.JupyterHub.ip = os.environ['PROXY_PUBLIC_SERVICE_HOST']
c.JupyterHub.port = int(os.environ['PROXY_PUBLIC_SERVICE_PORT'])

# the hub should listen on all interfaces, so the proxy can access it
c.JupyterHub.hub_ip = '0.0.0.0'

set_config_if_not_none(c.KubeSpawner, 'common_labels', 'kubespawner.common-labels')

c.KubeSpawner.namespace = os.environ.get('POD_NAMESPACE', 'default')


for trait, cfg_key in (
    ('start_timeout', 'start-timeout'),
    ('image_pull_policy', 'image-pull-policy'),
    ('image_pull_secrets', 'image-pull-secret-name'),
    ('events_enabled', 'events'),
    ('extra_labels', 'extra-labels'),
    ('extra_annotations', 'extra-annotations'),
    ('uid', 'uid'),
    ('fs_gid', 'fs-gid'),
    ('service_account', 'service-account-name'),
    ('scheduler_name', 'scheduler-name'),
    ('node_selector', 'node-selector'),
):
    set_config_if_not_none(c.KubeSpawner, trait, 'singleuser.' + cfg_key)

c.KubeSpawner.image_spec = get_config('singleuser.image-spec')
# Configure dynamically provisioning pvc
storage_type = get_config('singleuser.storage.type')
if storage_type == 'dynamic':
    pvc_name_template = get_config('singleuser.storage.dynamic.pvc-name-template')
    c.KubeSpawner.pvc_name_template = pvc_name_template
    volume_name_template = get_config('singleuser.storage.dynamic.volume-name-template')
    c.KubeSpawner.storage_pvc_ensure = True
    set_config_if_not_none(c.KubeSpawner, 'storage_class', 'singleuser.storage.dynamic.storage-class')
    set_config_if_not_none(c.KubeSpawner, 'storage_access_modes', 'singleuser.storage.dynamic.storage-access-modes')
    set_config_if_not_none(c.KubeSpawner, 'storage_capacity', 'singleuser.storage.capacity')

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

set_config_if_not_none(c.KubeSpawner, 'lifecycle_hooks', 'singleuser.lifecycle-hooks')

init_containers = get_config('singleuser.init-containers')
if init_containers:
    c.KubeSpawner.init_containers.extend(init_containers)

extra_containers = get_config('singleuser.extra-containers')
if extra_containers:
    c.KubeSpawner.extra_containers.extend(extra_containers)

# Gives spawned containers access to the API of the hub
# FIXME: KubeSpawner duplicate hub_connect config should be deprecated and removed
c.KubeSpawner.hub_connect_ip = os.environ['HUB_SERVICE_HOST']
c.KubeSpawner.hub_connect_port = int(os.environ['HUB_SERVICE_PORT'])

c.JupyterHub.hub_connect_ip = os.environ['HUB_SERVICE_HOST']
c.JupyterHub.hub_connect_port = int(os.environ['HUB_SERVICE_PORT'])

for trait, cfg_key in (
    ('mem_limit', 'singleuser.memory.limit'),
    ('mem_guarantee', 'singleuser.memory.guarantee'),
    ('cpu_limit', 'singleuser.cpu.limit'),
    ('cpu_guarantee', 'singleuser.cpu.guarantee'),
    ('extra_resource_limits', 'singleuser.extra-resource.limits'),
    ('extra_resource_guarantees', 'singleuser.extra-resource.guarantees'),
):
    set_config_if_not_none(c.KubeSpawner, trait, cfg_key)

# Allow switching authenticators easily
auth_type = get_config('auth.type')
email_domain = 'local'

if auth_type == 'google':
    c.JupyterHub.authenticator_class = 'oauthenticator.GoogleOAuthenticator'
    for trait, cfg_key in (
        ('client_id', 'client-id'),
        ('client_secret', 'client-secret'),
        ('oauth_callback_url', 'callback-url'),
        ('hosted_domain', 'hosted-domain'),
        ('login_service', 'login-service'),
    ):
        set_config_if_not_none(c.GoogleOAuthenticator, trait, 'auth.google.' + cfg_key)
    email_domain = get_config('auth.google.hosted-domain')
elif auth_type == 'github':
    c.JupyterHub.authenticator_class = 'oauthenticator.github.GitHubOAuthenticator'
    for trait, cfg_key in (
        ('client_id', 'client-id'),
        ('client_secret', 'client-secret'),
        ('oauth_callback_url', 'callback-url'),
        ('github_organization_whitelist', 'org_whitelist'),
    ):
        set_config_if_not_none(c.GitHubOAuthenticator, trait, 'auth.github.' + cfg_key)
elif auth_type == 'cilogon':
    c.JupyterHub.authenticator_class = 'oauthenticator.CILogonOAuthenticator'
    for trait, cfg_key in (
        ('client_id', 'client-id'),
        ('client_secret', 'client-secret'),
        ('oauth_callback_url', 'callback-url'),
    ):
        set_config_if_not_none(c.CILogonOAuthenticator, trait, 'auth.cilogon.' + cfg_key)
elif auth_type == 'gitlab':
    c.JupyterHub.authenticator_class = 'oauthenticator.gitlab.GitLabOAuthenticator'
    for trait, cfg_key in (
        ('client_id', 'client-id'),
        ('client_secret', 'client-secret'),
        ('oauth_callback_url', 'callback-url'),
    ):
        set_config_if_not_none(c.GitLabOAuthenticator, trait, 'auth.gitlab.' + cfg_key)
elif auth_type == 'mediawiki':
    c.JupyterHub.authenticator_class = 'oauthenticator.mediawiki.MWOAuthenticator'
    for trait, cfg_key in (
        ('client_id', 'client-id'),
        ('client_secret', 'client-secret'),
        ('oauth_callback_url', 'callback-url'),
        ('index_url', 'index-url'),
    ):
        set_config_if_not_none(c.MWOAuthenticator, trait, 'auth.mediawiki.' + cfg_key)
elif auth_type == 'globus':
    c.JupyterHub.authenticator_class = 'oauthenticator.globus.GlobusOAuthenticator'
    for trait, cfg_key in (
        ('client_id', 'client-id'),
        ('client_secret', 'client-secret'),
        ('oauth_callback_url', 'callback-url'),
        ('identity_provider', 'identity-provider'),
    ):
        set_config_if_not_none(c.GlobusOAuthenticator, trait, 'auth.globus.' + cfg_key)
elif auth_type == 'hmac':
    c.JupyterHub.authenticator_class = 'hmacauthenticator.HMACAuthenticator'
    c.HMACAuthenticator.secret_key = bytes.fromhex(get_config('auth.hmac.secret-key'))
elif auth_type == 'dummy':
    c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'
    set_config_if_not_none(c.DummyAuthenticator, 'password', 'auth.dummy.password')
elif auth_type == 'tmp':
    c.JupyterHub.authenticator_class = 'tmpauthenticator.TmpAuthenticator'
elif auth_type == 'lti':
    c.JupyterHub.authenticator_class = 'ltiauthenticator.LTIAuthenticator'
    set_config_if_not_none(c.LTIAuthenticator, 'consumers', 'auth.lti.consumers')
elif auth_type == 'ldap':
    c.JupyterHub.authenticator_class = 'ldapauthenticator.LDAPAuthenticator'
    c.LDAPAuthenticator.server_address = get_config('auth.ldap.server.address')
    set_config_if_not_none(c.LDAPAuthenticator, 'server_port', 'auth.ldap.server.port')
    set_config_if_not_none(c.LDAPAuthenticator, 'use_ssl', 'auth.ldap.server.ssl')
    set_config_if_not_none(c.LDAPAuthenticator, 'allowed_groups', 'auth.ldap.allowed-groups')
    set_config_if_not_none(c.LDAPAuthenticator, 'bind_dn_template', 'auth.ldap.dn.templates')
    set_config_if_not_none(c.LDAPAuthenticator, 'lookup_dn', 'auth.ldap.dn.lookup')
    set_config_if_not_none(c.LDAPAuthenticator, 'lookup_dn_search_filter', 'auth.ldap.dn.search.filter')
    set_config_if_not_none(c.LDAPAuthenticator, 'lookup_dn_search_user', 'auth.ldap.dn.search.user')
    set_config_if_not_none(c.LDAPAuthenticator, 'lookup_dn_search_password', 'auth.ldap.dn.search.password')
    set_config_if_not_none(c.LDAPAuthenticator, 'lookup_dn_user_dn_attribute', 'auth.ldap.dn.user.dn-attribute')
    set_config_if_not_none(c.LDAPAuthenticator, 'escape_userdn', 'auth.ldap.dn.user.escape')
    set_config_if_not_none(c.LDAPAuthenticator, 'valid_username_regex', 'auth.ldap.dn.user.valid-regex')
    set_config_if_not_none(c.LDAPAuthenticator, 'user_search_base', 'auth.ldap.dn.user.search-base')
    set_config_if_not_none(c.LDAPAuthenticator, 'user_attribute', 'auth.ldap.dn.user.attribute')
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

set_config_if_not_none(c.OAuthenticator, 'scope', 'auth.scopes')

c.Authenticator.enable_auth_state = get_config('auth.state.enabled', False)

c.KubeSpawner.environment.update(get_config('singleuser.extra-env', {}))

# Enable admins to access user servers
c.JupyterHub.admin_access = get_config('auth.admin.access', False)
c.Authenticator.admin_users = get_config('auth.admin.users', [])
c.Authenticator.whitelist = get_config('auth.whitelist.users', [])

set_config_if_not_none(c.JupyterHub, 'base_url', 'hub.base_url')
c.JupyterHub.base_url = get_config('hub.base_url')

c.JupyterHub.services = []

if get_config('cull.enabled', False):
    cull_timeout = get_config('cull.timeout', 3600)
    cull_every = get_config('cull.every', 600)
    cull_concurrency = get_config('cull.concurrency', 10)
    cull_cmd = [
        '/usr/local/bin/cull_idle_servers.py',
        '--timeout=%s' % cull_timeout,
        '--cull-every=%s' % cull_every,
        '--concurrency=%s' % cull_concurrency,
        '--url=http://127.0.0.1:8081' + url_path_join(c.JupyterHub.base_url, 'hub/api'),
    ]

    if get_config('cull.users'):
        cull_cmd.append('--cull-users')

    cull_max_age = get_config('cull.max-age')
    if cull_max_age:
        cull_cmd.append('--max-age=%s' % cull_max_age)

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


set_config_if_not_none(c.JupyterHub, 'db_url', 'hub.db_url')
set_config_if_not_none(c.JupyterHub, 'allow_named_servers', 'hub.allow-named-servers')

set_config_if_not_none(c.Spawner, 'cmd', 'singleuser.cmd')
set_config_if_not_none(c.Spawner, 'default_url', 'singleuser.default-url')

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

    c.KubeSpawner.init_containers.append(ip_block_container)


if get_config('debug.enabled', False):
    c.JupyterHub.log_level = 'DEBUG'
    c.Spawner.debug = True

extra_configs = sorted(glob.glob('/etc/jupyterhub/config/hub.extra-config.*.py'))
for ec in extra_configs:
    load_subconfig(ec)
