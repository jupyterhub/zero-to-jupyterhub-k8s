import os
import re
import sys

from binascii import a2b_hex

from tornado.httpclient import AsyncHTTPClient
from kubernetes import client
from jupyterhub.utils import url_path_join

# Make sure that modules placed in the same directory as the jupyterhub config are added to the pythonpath
configuration_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, configuration_directory)

from z2jh import get_config, set_config_if_not_none

def camelCaseify(s):
    """convert snake_case to camelCase

    For the common case where some_value is set from someValue
    so we don't have to specify the name twice.
    """
    return re.sub(r"_([a-z])", lambda m: m.group(1).upper(), s)

# Configure JupyterHub to use the curl backend for making HTTP requests,
# rather than the pure-python implementations. The default one starts
# being too slow to make a large number of requests to the proxy API
# at the rate required.
AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'

# Connect to a proxy running in a different pod. Note that *_SERVICE_*
# environment variables are set by Kubernetes for Services
c.ConfigurableHTTPProxy.api_url = f"http://proxy-api:{os.environ['PROXY_API_SERVICE_PORT']}"
c.ConfigurableHTTPProxy.should_start = False

# Do not shut down user pods when hub is restarted
c.JupyterHub.cleanup_servers = False

# Check that the proxy has routes appropriately setup
c.JupyterHub.last_activity_interval = 60

# Don't wait at all before redirecting a spawning user to the progress page
c.JupyterHub.tornado_settings = {
    'slow_spawn_timeout': 0,
}


# configure the hub db connection
db_type = get_config('hub.db.type')
if db_type == 'sqlite-pvc':
    c.JupyterHub.db_url = "sqlite:///jupyterhub.sqlite"
elif db_type == "sqlite-memory":
    c.JupyterHub.db_url = "sqlite://"
else:
    set_config_if_not_none(c.JupyterHub, "db_url", "hub.db.url")


# c.JupyterHub configuration from Helm chart's configmap
for trait, cfg_key in (
    ('concurrent_spawn_limit', None),
    ('active_server_limit', None),
    ('base_url', None),
    # ('cookie_secret', None),  # requires a Hex -> Byte transformation
    ('allow_named_servers', None),
    ('named_server_limit_per_user', None),
    ('authenticate_prometheus', None),
    ('redirect_to_server', None),
    ('shutdown_on_logout', None),
    ('template_paths', None),
    ('template_vars', None),
):
    if cfg_key is None:
        cfg_key = camelCaseify(trait)
    set_config_if_not_none(c.JupyterHub, trait, 'hub.' + cfg_key)

# a required Hex -> Byte transformation
cookie_secret_hex = get_config("hub.cookieSecret")
if cookie_secret_hex:
    c.JupyterHub.cookie_secret = a2b_hex(cookie_secret_hex)

# hub_bind_url configures what the JupyterHub process within the hub pod's
# container should listen to.
hub_container_port = 8081
c.JupyterHub.hub_bind_url = f'http://:{hub_container_port}'

# hub_connect_url is the URL for connecting to the hub for use by external
# JupyterHub services such as the proxy. Note that *_SERVICE_* environment
# variables are set by Kubernetes for Services.
c.JupyterHub.hub_connect_url = f"http://hub:{os.environ['HUB_SERVICE_PORT']}"

# implement common labels
# this duplicates the jupyterhub.commonLabels helper
common_labels = c.KubeSpawner.common_labels = {}
common_labels['app'] = get_config(
    "nameOverride",
    default=get_config("Chart.Name", "jupyterhub"),
)
common_labels['heritage'] = "jupyterhub"
chart_name = get_config('Chart.Name')
chart_version = get_config('Chart.Version')
if chart_name and chart_version:
    common_labels['chart'] = "{}-{}".format(
        chart_name, chart_version.replace('+', '_'),
    )
release = get_config('Release.Name')
if release:
    common_labels['release'] = release

c.KubeSpawner.namespace = os.environ.get('POD_NAMESPACE', 'default')

# Max number of consecutive failures before the Hub restarts itself
# requires jupyterhub 0.9.2
set_config_if_not_none(
    c.Spawner,
    'consecutive_failure_limit',
    'hub.consecutiveFailureLimit',
)

for trait, cfg_key in (
    ('pod_name_template', None),
    ('start_timeout', None),
    ('image_pull_policy', 'image.pullPolicy'),
    ('image_pull_secrets', 'image.pullSecrets'),
    ('events_enabled', 'events'),
    ('extra_labels', None),
    ('extra_annotations', None),
    ('uid', None),
    ('fs_gid', None),
    ('service_account', 'serviceAccountName'),
    ('storage_extra_labels', 'storage.extraLabels'),
    ('tolerations', 'extraTolerations'),
    ('node_selector', None),
    ('node_affinity_required', 'extraNodeAffinity.required'),
    ('node_affinity_preferred', 'extraNodeAffinity.preferred'),
    ('pod_affinity_required', 'extraPodAffinity.required'),
    ('pod_affinity_preferred', 'extraPodAffinity.preferred'),
    ('pod_anti_affinity_required', 'extraPodAntiAffinity.required'),
    ('pod_anti_affinity_preferred', 'extraPodAntiAffinity.preferred'),
    ('lifecycle_hooks', None),
    ('init_containers', None),
    ('extra_containers', None),
    ('mem_limit', 'memory.limit'),
    ('mem_guarantee', 'memory.guarantee'),
    ('cpu_limit', 'cpu.limit'),
    ('cpu_guarantee', 'cpu.guarantee'),
    ('extra_resource_limits', 'extraResource.limits'),
    ('extra_resource_guarantees', 'extraResource.guarantees'),
    ('environment', 'extraEnv'),
    ('profile_list', None),
    ('extra_pod_config', None),
):
    if cfg_key is None:
        cfg_key = camelCaseify(trait)
    set_config_if_not_none(c.KubeSpawner, trait, 'singleuser.' + cfg_key)

image = get_config("singleuser.image.name")
if image:
    tag = get_config("singleuser.image.tag")
    if tag:
        image = "{}:{}".format(image, tag)

    c.KubeSpawner.image = image

if get_config('singleuser.imagePullSecret.enabled'):
    c.KubeSpawner.image_pull_secrets = 'singleuser-image-credentials'

# scheduling:
if get_config('scheduling.userScheduler.enabled'):
    c.KubeSpawner.scheduler_name = os.environ['HELM_RELEASE_NAME'] + "-user-scheduler"
if get_config('scheduling.podPriority.enabled'):
    c.KubeSpawner.priority_class_name = os.environ['HELM_RELEASE_NAME'] + "-default-priority"

# add node-purpose affinity
match_node_purpose = get_config('scheduling.userPods.nodeAffinity.matchNodePurpose')
if match_node_purpose:
    node_selector = dict(
        matchExpressions=[
            dict(
                key="hub.jupyter.org/node-purpose",
                operator="In",
                values=["user"],
            )
        ],
    )
    if match_node_purpose == 'prefer':
        c.KubeSpawner.node_affinity_preferred.append(
            dict(
                weight=100,
                preference=node_selector,
            ),
        )
    elif match_node_purpose == 'require':
        c.KubeSpawner.node_affinity_required.append(node_selector)
    elif match_node_purpose == 'ignore':
        pass
    else:
        raise ValueError("Unrecognized value for matchNodePurpose: %r" % match_node_purpose)

# add dedicated-node toleration
for key in (
    'hub.jupyter.org/dedicated',
    # workaround GKE not supporting / in initial node taints
    'hub.jupyter.org_dedicated',
):
    c.KubeSpawner.tolerations.append(
        dict(
            key=key,
            operator='Equal',
            value='user',
            effect='NoSchedule',
        )
    )

# Configure dynamically provisioning pvc
storage_type = get_config('singleuser.storage.type')

if storage_type == 'dynamic':
    pvc_name_template = get_config('singleuser.storage.dynamic.pvcNameTemplate')
    c.KubeSpawner.pvc_name_template = pvc_name_template
    volume_name_template = get_config('singleuser.storage.dynamic.volumeNameTemplate')
    c.KubeSpawner.storage_pvc_ensure = True
    set_config_if_not_none(c.KubeSpawner, 'storage_class', 'singleuser.storage.dynamic.storageClass')
    set_config_if_not_none(c.KubeSpawner, 'storage_access_modes', 'singleuser.storage.dynamic.storageAccessModes')
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
            'mountPath': get_config('singleuser.storage.homeMountPath'),
            'name': volume_name_template
        }
    ]
elif storage_type == 'static':
    pvc_claim_name = get_config('singleuser.storage.static.pvcName')
    c.KubeSpawner.volumes = [{
        'name': 'home',
        'persistentVolumeClaim': {
            'claimName': pvc_claim_name
        }
    }]

    c.KubeSpawner.volume_mounts = [{
        'mountPath': get_config('singleuser.storage.homeMountPath'),
        'name': 'home',
        'subPath': get_config('singleuser.storage.static.subPath')
    }]

c.KubeSpawner.volumes.extend(get_config('singleuser.storage.extraVolumes', []))
c.KubeSpawner.volume_mounts.extend(get_config('singleuser.storage.extraVolumeMounts', []))

# Allow switching authenticators easily
auth_type = get_config('auth.type')
email_domain = 'local'

common_oauth_traits = (
        ('client_id', None),
        ('client_secret', None),
        ('oauth_callback_url', 'callbackUrl'),
)

if auth_type == 'google':
    c.JupyterHub.authenticator_class = 'oauthenticator.GoogleOAuthenticator'
    for trait, cfg_key in common_oauth_traits + (
        ('hosted_domain', None),
        ('login_service', None),
    ):
        if cfg_key is None:
            cfg_key = camelCaseify(trait)
        set_config_if_not_none(c.GoogleOAuthenticator, trait, 'auth.google.' + cfg_key)
    email_domain = get_config('auth.google.hostedDomain')
elif auth_type == 'github':
    c.JupyterHub.authenticator_class = 'oauthenticator.github.GitHubOAuthenticator'
    for trait, cfg_key in common_oauth_traits + (
        ('github_organization_whitelist', 'orgWhitelist'),
    ):
        if cfg_key is None:
            cfg_key = camelCaseify(trait)
        set_config_if_not_none(c.GitHubOAuthenticator, trait, 'auth.github.' + cfg_key)
elif auth_type == 'cilogon':
    c.JupyterHub.authenticator_class = 'oauthenticator.CILogonOAuthenticator'
    for trait, cfg_key in common_oauth_traits:
        if cfg_key is None:
            cfg_key = camelCaseify(trait)
        set_config_if_not_none(c.CILogonOAuthenticator, trait, 'auth.cilogon.' + cfg_key)
elif auth_type == 'gitlab':
    c.JupyterHub.authenticator_class = 'oauthenticator.gitlab.GitLabOAuthenticator'
    for trait, cfg_key in common_oauth_traits + (
        ('gitlab_group_whitelist', None),
        ('gitlab_project_id_whitelist', None),
        ('gitlab_url', None),
    ):
        if cfg_key is None:
            cfg_key = camelCaseify(trait)
        set_config_if_not_none(c.GitLabOAuthenticator, trait, 'auth.gitlab.' + cfg_key)
elif auth_type == 'azuread':
    c.JupyterHub.authenticator_class = 'oauthenticator.azuread.AzureAdOAuthenticator'
    for trait, cfg_key in common_oauth_traits + (
        ('tenant_id', None),
        ('username_claim', None),
    ):
        if cfg_key is None:
            cfg_key = camelCaseify(trait)

        set_config_if_not_none(c.AzureAdOAuthenticator, trait, 'auth.azuread.' + cfg_key)
elif auth_type == 'mediawiki':
    c.JupyterHub.authenticator_class = 'oauthenticator.mediawiki.MWOAuthenticator'
    for trait, cfg_key in common_oauth_traits + (
        ('index_url', None),
    ):
        if cfg_key is None:
            cfg_key = camelCaseify(trait)
        set_config_if_not_none(c.MWOAuthenticator, trait, 'auth.mediawiki.' + cfg_key)
elif auth_type == 'globus':
    c.JupyterHub.authenticator_class = 'oauthenticator.globus.GlobusOAuthenticator'
    for trait, cfg_key in common_oauth_traits + (
        ('identity_provider', None),
    ):
        if cfg_key is None:
            cfg_key = camelCaseify(trait)
        set_config_if_not_none(c.GlobusOAuthenticator, trait, 'auth.globus.' + cfg_key)
elif auth_type == 'hmac':
    c.JupyterHub.authenticator_class = 'hmacauthenticator.HMACAuthenticator'
    c.HMACAuthenticator.secret_key = bytes.fromhex(get_config('auth.hmac.secretKey'))
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
    set_config_if_not_none(c.LDAPAuthenticator, 'allowed_groups', 'auth.ldap.allowedGroups')
    set_config_if_not_none(c.LDAPAuthenticator, 'bind_dn_template', 'auth.ldap.dn.templates')
    set_config_if_not_none(c.LDAPAuthenticator, 'lookup_dn', 'auth.ldap.dn.lookup')
    set_config_if_not_none(c.LDAPAuthenticator, 'lookup_dn_search_filter', 'auth.ldap.dn.search.filter')
    set_config_if_not_none(c.LDAPAuthenticator, 'lookup_dn_search_user', 'auth.ldap.dn.search.user')
    set_config_if_not_none(c.LDAPAuthenticator, 'lookup_dn_search_password', 'auth.ldap.dn.search.password')
    set_config_if_not_none(c.LDAPAuthenticator, 'lookup_dn_user_dn_attribute', 'auth.ldap.dn.user.dnAttribute')
    set_config_if_not_none(c.LDAPAuthenticator, 'escape_userdn', 'auth.ldap.dn.user.escape')
    set_config_if_not_none(c.LDAPAuthenticator, 'valid_username_regex', 'auth.ldap.dn.user.validRegex')
    set_config_if_not_none(c.LDAPAuthenticator, 'user_search_base', 'auth.ldap.dn.user.searchBase')
    set_config_if_not_none(c.LDAPAuthenticator, 'user_attribute', 'auth.ldap.dn.user.attribute')
elif auth_type == 'custom':
    # full_class_name looks like "myauthenticator.MyAuthenticator".
    # To create a docker image with this class availabe, you can just have the
    # following Dockerfile:
    #   FROM jupyterhub/k8s-hub:v0.4
    #   RUN pip3 install myauthenticator
    full_class_name = get_config('auth.custom.className')
    c.JupyterHub.authenticator_class = full_class_name
    auth_class_name = full_class_name.rsplit('.', 1)[-1]
    auth_config = c[auth_class_name]
    auth_config.update(get_config('auth.custom.config') or {})
else:
    raise ValueError("Unhandled auth type: %r" % auth_type)

set_config_if_not_none(c.OAuthenticator, 'scope', 'auth.scopes')

set_config_if_not_none(c.Authenticator, 'enable_auth_state', 'auth.state.enabled')

# Enable admins to access user servers
set_config_if_not_none(c.JupyterHub, 'admin_access', 'auth.admin.access')
set_config_if_not_none(c.Authenticator, 'admin_users', 'auth.admin.users')
set_config_if_not_none(c.Authenticator, 'whitelist', 'auth.whitelist.users')

c.JupyterHub.services = []

if get_config('cull.enabled', False):
    cull_cmd = [
        'python3',
        '-m',
        'jupyterhub_idle_culler'
    ]
    base_url = c.JupyterHub.get('base_url', '/')
    cull_cmd.append(
        '--url=http://localhost:8081' + url_path_join(base_url, 'hub/api')
    )

    cull_timeout = get_config('cull.timeout')
    if cull_timeout:
        cull_cmd.append('--timeout=%s' % cull_timeout)

    cull_every = get_config('cull.every')
    if cull_every:
        cull_cmd.append('--cull-every=%s' % cull_every)

    cull_concurrency = get_config('cull.concurrency')
    if cull_concurrency:
        cull_cmd.append('--concurrency=%s' % cull_concurrency)

    if get_config('cull.users'):
        cull_cmd.append('--cull-users')

    if get_config('cull.removeNamedServers'):
        cull_cmd.append('--remove-named-servers')

    cull_max_age = get_config('cull.maxAge')
    if cull_max_age:
        cull_cmd.append('--max-age=%s' % cull_max_age)

    c.JupyterHub.services.append({
        'name': 'cull-idle',
        'admin': True,
        'command': cull_cmd,
    })

for name, service in get_config('hub.services', {}).items():
    # jupyterhub.services is a list of dicts, but
    # in the helm chart it is a dict of dicts for easier merged-config
    service.setdefault('name', name)
    # handle camelCase->snake_case of api_token
    api_token = service.pop('apiToken', None)
    if api_token:
        service['api_token'] = api_token
    c.JupyterHub.services.append(service)


set_config_if_not_none(c.Spawner, 'cmd', 'singleuser.cmd')
set_config_if_not_none(c.Spawner, 'default_url', 'singleuser.defaultUrl')

cloud_metadata = get_config('singleuser.cloudMetadata', {})

if cloud_metadata.get('block') == True or cloud_metadata.get('enabled') == False:
    # Use iptables to block access to cloud metadata by default
    network_tools_image_name = get_config('singleuser.networkTools.image.name')
    network_tools_image_tag = get_config('singleuser.networkTools.image.tag')
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


extra_config = get_config('hub.extraConfig', {})
if isinstance(extra_config, str):
    from textwrap import indent, dedent
    msg = dedent(
    """
    hub.extraConfig should be a dict of strings,
    but found a single string instead.

    extraConfig as a single string is deprecated
    as of the jupyterhub chart version 0.6.

    The keys can be anything identifying the
    block of extra configuration.

    Try this instead:

        hub:
          extraConfig:
            myConfig: |
              {}

    This configuration will still be loaded,
    but you are encouraged to adopt the nested form
    which enables easier merging of multiple extra configurations.
    """
    )
    print(
        msg.format(
            indent(extra_config, ' ' * 10).lstrip()
        ),
        file=sys.stderr
    )
    extra_config = {'deprecated string': extra_config}

for key, config_py in sorted(extra_config.items()):
    print("Loading extra config: %s" % key)
    exec(config_py)
