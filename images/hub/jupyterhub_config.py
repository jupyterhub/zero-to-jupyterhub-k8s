import os
import glob
from tornado.httpclient import AsyncHTTPClient
from kubernetes import client

from z2jh import get_config, get_secret, set_config_if_not_none
from jupyterhub.utils import url_path_join

# About traitlets
# ------------------------------------------------------------------------------
# In order to understand how this configuration works, it is useful to read the
# traitlets documentation: https://traitlets.readthedocs.io/en/stable/config.html
#
# A Configuration object (traitlets.config.Config) is made available as `c` in
# this file.
#
### Lazy evaluation and default value initialization
# If you would print c.KubeSpawner.common_labels now within this file, you would
# get...
# <traitlets.config.loader.LazyConfigValue object at 0x7f1c53071a20>
#
# But if you would run the following...
# c.KubeSpawner.common_labels.update({'heritage': 'something-new'})
#
# You would be fine, and end up with...
# {'app': 'jupyterhub', 'heritage': 'something-new'}
#
# Where these labels had defaults set in c.KubeSpawner.common_labels but you
# overrode the second labels value.

# Network related
# ------------------------------------------------------------------------------
# Configure JupyterHub to use the curl backend for making HTTP requests,
# rather than the pure-python implementations. The default one starts
# being too slow to make a large number of requests to the proxy API
# at the rate required.
AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

# Connect to a proxy running in a different pod
c.ConfigurableHTTPProxy.api_url = 'http://{}:{}'.format(os.environ['PROXY_API_SERVICE_HOST'], int(os.environ['PROXY_API_SERVICE_PORT']))
c.ConfigurableHTTPProxy.should_start = False

# Hub related
# ------------------------------------------------------------------------------
# Do not shut down user pods when hub is restarted
c.JupyterHub.cleanup_servers = False

# Check that the proxy has routes appropriately setup
c.JupyterHub.last_activity_interval = 60

# Don't wait at all before redirecting a spawning user to the progress page
c.JupyterHub.tornado_settings = {
    'slow_spawn_timeout': 0,
}

# Max number of servers that can be spawning at any one time
c.JupyterHub.concurrent_spawn_limit = int(get_config('hub.concurrent-spawn-limit'))
c.JupyterHub.allow_named_servers = get_config('hub.allow-named-servers')
c.JupyterHub.active_server_limit = int(get_config('hub.active-server-limit'))

c.JupyterHub.base_url = get_config('hub.base-url')
c.JupyterHub.db_url = get_config('hub.db-url')
c.JupyterHub.ip = os.environ['PROXY_PUBLIC_SERVICE_HOST']
c.JupyterHub.port = int(os.environ['PROXY_PUBLIC_SERVICE_PORT'])

# the hub should listen on all interfaces, so the proxy can access it
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = os.environ['HUB_SERVICE_HOST']
c.JupyterHub.hub_connect_port = int(os.environ['HUB_SERVICE_PORT'])

c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'

# Spawner related
# ------------------------------------------------------------------------------
c.Spawner.cmd = get_config('singleuser.cmd')
c.Spawner.default_url = get_config('singleuser.default-url')

# Max number of consecutive failures spawning users before the hub restarts itself
c.Spawner.consecutive_failure_limit = int(get_config('hub.consecutive-failure-limit'))

# Max time that KubeSpawner waits for 'Running' status after user pod creation
# before it considers the spawn to have failed. It should be high to accomodate
# image pulling and node scale up.
c.KubeSpawner.start_timeout = get_config('singleuser.start-timeout')

# Gives spawned containers access to the API of the hub
# FIXME: KubeSpawner duplicate hub_connect config should be deprecated and removed
c.KubeSpawner.hub_connect_ip = os.environ['HUB_SERVICE_HOST']
c.KubeSpawner.hub_connect_port = int(os.environ['HUB_SERVICE_PORT'])
if os.environ.get('POD_NAMESPACE'):
    c.KubeSpawner.namespace = os.environ.get('POD_NAMESPACE')

c.KubeSpawner.environment.update(get_config('singleuser.extra-env', {}))
c.KubeSpawner.common_labels.update(get_config('kubespawner.common-labels', {}))
c.KubeSpawner.extra_labels.update(get_config('singleuser.extra-labels', {}))
c.KubeSpawner.extra_annotations.update(get_config('singleuser.extra-annotations', {}))
c.KubeSpawner.storage_extra_labels.update(get_config('singleuser.storage-extra-labels', {}))

c.KubeSpawner.image_spec = get_config('singleuser.image-spec')
c.KubeSpawner.image_pull_policy = get_config('singleuser.image-pull-policy')
set_config_if_not_none(c.KubeSpawner, 'image_pull_secrets', 'singleuser.image-pull-secret-name')

set_config_if_not_none(c.KubeSpawner, 'mem_limit', 'singleuser.memory.limit')
set_config_if_not_none(c.KubeSpawner, 'mem_guarantee', 'singleuser.memory.guarantee')
set_config_if_not_none(c.KubeSpawner, 'cpu_limit', 'singleuser.cpu.limit')
set_config_if_not_none(c.KubeSpawner, 'cpu_guarantee', 'singleuser.cpu.guarantee')
c.KubeSpawner.extra_resource_limits.update(get_config('singleuser.extra-resource.limits', {}))
c.KubeSpawner.extra_resource_guarantees.update(get_config('singleuser.extra-resource.guarantees', {}))

c.KubeSpawner.uid = get_config('singleuser.uid')
c.KubeSpawner.fs_gid = get_config('singleuser.fs-gid')

c.KubeSpawner.events_enabled = get_config('singleuser.events')
set_config_if_not_none(c.KubeSpawner, 'service_account', 'singleuser.service-account-name')
set_config_if_not_none(c.KubeSpawner, 'scheduler_name', 'singleuser.scheduler-name')
set_config_if_not_none(c.KubeSpawner, 'priority_class_name', 'singleuser.priority-class-name')

c.KubeSpawner.tolerations.extend(get_config('singleuser.tolerations', []))
c.KubeSpawner.node_selector.update(get_config('singleuser.node-selector', {}))
c.KubeSpawner.node_affinity_required.extend(get_config('singleuser.node-affinity-required', []))
c.KubeSpawner.node_affinity_preferred.extend(get_config('singleuser.node-affinity-preferred', []))
c.KubeSpawner.pod_affinity_required.extend(get_config('singleuser.pod-affinity-required', []))
c.KubeSpawner.pod_affinity_preferred.extend(get_config('singleuser.pod-affinity-preferred', []))
c.KubeSpawner.pod_anti_affinity_required.extend(get_config('singleuser.pod-anti-affinity-required', []))
c.KubeSpawner.pod_anti_affinity_preferred.extend(get_config('singleuser.pod-anti-affinity-preferred', []))
c.KubeSpawner.lifecycle_hooks.update(get_config('singleuser.lifecycle-hooks', {}))
c.KubeSpawner.init_containers.extend(get_config('singleuser.init-containers', []))
c.KubeSpawner.extra_containers.extend(get_config('singleuser.extra-containers', []))

# Volume related
# ------------------------------------------------------------------------------
# Configure dynamically provisioning pvc
storage_type = get_config('singleuser.storage.type')
if storage_type == 'dynamic':
    c.KubeSpawner.pvc_name_template = get_config('singleuser.storage.dynamic.pvc-name-template')
    c.KubeSpawner.storage_pvc_ensure = True
    c.KubeSpawner.storage_class = get_config('singleuser.storage.dynamic.storage-class')
    c.KubeSpawner.storage_access_modes = get_config('singleuser.storage.dynamic.storage-access-modes')
    c.KubeSpawner.storage_capacity = get_config('singleuser.storage.capacity')

    # Add volumes to singleuser pods
    c.KubeSpawner.volumes = [{
        'name': get_config('singleuser.storage.dynamic.volume-name-template'),
        'persistentVolumeClaim': {
            'claimName': c.KubeSpawner.pvc_name_template
        }
    }]
    c.KubeSpawner.volume_mounts = [{
        'name': get_config('singleuser.storage.dynamic.volume-name-template'),
        'mountPath': get_config('singleuser.storage.home_mount_path'),
    }]
elif storage_type == 'static':
    c.KubeSpawner.volumes = [{
        'name': 'home',
        'persistentVolumeClaim': {
            'claimName': get_config('singleuser.storage.static.pvc-name'),
        }
    }]

    c.KubeSpawner.volume_mounts = [{
        'name': 'home',
        'mountPath': get_config('singleuser.storage.home_mount_path'),
        'subPath': get_config('singleuser.storage.static.sub-path'),
    }]

c.KubeSpawner.volumes.extend(get_config('singleuser.storage.extra-volumes', []))
c.KubeSpawner.volume_mounts.extend(get_config('singleuser.storage.extra-volume-mounts', []))


# Auth related
# ------------------------------------------------------------------------------
auth_scopes = get_config('auth.scopes')
if auth_scopes:
    c.OAuthenticator.scope = auth_scopes

c.Authenticator.enable_auth_state = get_config('auth.state.enabled')

# Allow switching authenticators easily
auth_type = get_config('auth.type')

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

# Enable admins to access user servers
c.JupyterHub.admin_access = get_config('auth.admin.access')
c.Authenticator.admin_users = get_config('auth.admin.users', [])
c.Authenticator.whitelist = get_config('auth.whitelist.users', [])


# JupyterHub services
# ------------------------------------------------------------------------------

c.JupyterHub.services = []

if get_config('cull.enabled'):
    cull_timeout = get_config('cull.timeout')
    cull_every = get_config('cull.every')
    cull_concurrency = get_config('cull.concurrency')
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


# Security related
# ------------------------------------------------------------------------------
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


# Configuration related
# ------------------------------------------------------------------------------
if get_config('debug.enabled'):
    c.JupyterHub.log_level = 'DEBUG'
    c.Spawner.debug = True

extra_configs = sorted(glob.glob('/etc/jupyterhub/config/hub.extra-config.*.py'))
for ec in extra_configs:
    load_subconfig(ec)
