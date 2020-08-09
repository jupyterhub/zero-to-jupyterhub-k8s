import os
import sys

import kubernetes.client

from z2jh import get_config, set_config_if_not_none, camelCaseify


def configure_kube_spawner_volumes(kube_spawner):

    # Configure dynamically provisioning pvc
    storage_type = get_config('singleuser.storage.type')

    if storage_type == 'dynamic':
        pvc_name_template = get_config('singleuser.storage.dynamic.pvcNameTemplate')
        kube_spawner.pvc_name_template = pvc_name_template
        volume_name_template = get_config('singleuser.storage.dynamic.volumeNameTemplate')
        kube_spawner.storage_pvc_ensure = True
        set_config_if_not_none(kube_spawner, 'storage_class', 'singleuser.storage.dynamic.storageClass')
        set_config_if_not_none(kube_spawner, 'storage_access_modes', 'singleuser.storage.dynamic.storageAccessModes')
        set_config_if_not_none(kube_spawner, 'storage_capacity', 'singleuser.storage.capacity')

        # Add volumes to singleuser pods
        volumes = [{
            'name': volume_name_template,
            'persistentVolumeClaim': {
                'claimName': pvc_name_template
            }
        }]
        volume_mounts = [{
            'mountPath': get_config('singleuser.storage.homeMountPath'),
            'name': volume_name_template
        }]
    elif storage_type == 'static':
        volumes = [{
            'name': 'home',
            'persistentVolumeClaim': {
                'claimName': get_config('singleuser.storage.static.pvcName')
            }
        }]

        volume_mounts = [{
            'mountPath': get_config('singleuser.storage.homeMountPath'),
            'name': 'home',
            'subPath': get_config('singleuser.storage.static.subPath')
        }]

    volumes.extend(get_config('singleuser.storage.extraVolumes', []))
    volume_mounts.extend(get_config('singleuser.storage.extraVolumeMounts', []))

    kube_spawner.volumes = volumes
    kube_spawner.volume_mounts = volume_mounts
    return kube_spawner


def configure_kube_spawner_init_containers(kube_spawner):
    cloud_metadata = get_config('singleuser.cloudMetadata', {})

    # default: disabled
    if cloud_metadata.get('enabled', False):
        return kube_spawner

    # Use iptables to block access to cloud metadata
    network_tools_image_name = get_config('singleuser.networkTools.image.name')
    network_tools_image_tag = get_config('singleuser.networkTools.image.tag')
    ip_block_container = kubernetes.client.V1Container(
        name="block-cloud-metadata",
        image=f"{network_tools_image_name}:{network_tools_image_tag}",
        command=[
            'iptables',
            '-A', 'OUTPUT',
            '-d', cloud_metadata.get('ip', '169.254.169.254'),
            '-j', 'DROP'
        ],
        security_context=kubernetes.client.V1SecurityContext(
            privileged=True,
            run_as_user=0,
            capabilities=kubernetes.client.V1Capabilities(add=['NET_ADMIN'])
        )
    )

    kube_spawner.init_containers.append(ip_block_container)
    return kube_spawner


def configure_kube_spawner_metadata(kube_spawner):
    # implement common labels
    # this duplicates the jupyterhub.commonLabels helper
    common_labels = {
        'app': get_config(
            'nameOverride',
            default=get_config('Chart.Name', 'jupyterhub'),
        ),
        'heritage': 'jupyterhub',
    }
    chart_name = get_config('Chart.Name')
    chart_version = get_config('Chart.Version')
    if chart_name and chart_version:
        common_labels['chart'] = "{}-{}".format(
            chart_name, chart_version.replace('+', '_'),
        )
    release = get_config('Release.Name')
    if release:
        common_labels['release'] = release

    kube_spawner.common_labels = common_labels
    kube_spawner.namespace = os.environ.get('POD_NAMESPACE', 'default')
    return kube_spawner


def configure_kube_spawner_basic(kube_spawner):
    # assign everything from the singleuser values to the kube_spawner
    for trait, cfg_key in (
        ('start_timeout', None),
        ('image_pull_policy', 'image.pullPolicy'),
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
        set_config_if_not_none(kube_spawner, trait, 'singleuser.' + cfg_key)

    # add image
    image = get_config("singleuser.image.name")
    if image:
        tag = get_config("singleuser.image.tag")
        if tag:
            image = "{}:{}".format(image, tag)

        kube_spawner.image = image

    # add pull secrets
    if get_config('singleuser.imagePullSecret.enabled'):
        kube_spawner.image_pull_secrets = 'singleuser-image-credentials'

    # scheduling:
    if get_config('scheduling.userScheduler.enabled'):
        kube_spawner.scheduler_name = os.environ['HELM_RELEASE_NAME'] + "-user-scheduler"
    if get_config('scheduling.podPriority.enabled'):
        kube_spawner.priority_class_name = os.environ['HELM_RELEASE_NAME'] + "-default-priority"

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
            kube_spawner.node_affinity_preferred.append(
                dict(
                    weight=100,
                    preference=node_selector,
                ),
            )
        elif match_node_purpose == 'require':
            kube_spawner.node_affinity_required.append(node_selector)
        elif match_node_purpose == 'ignore':
            pass
        else:
            raise ValueError("Unrecognized value for matchNodePurpose: %r" % match_node_purpose)

    return kube_spawner


def configure_kube_spawner(kube_spawner):
    kube_spawner = configure_kube_spawner_metadata(kube_spawner)

    kube_spawner = configure_kube_spawner_basic(kube_spawner)

    # add dedicated-node toleration
    for key in (
        'hub.jupyter.org/dedicated',
        # workaround GKE not supporting / in initial node taints
        'hub.jupyter.org_dedicated',
    ):
        kube_spawner.tolerations.append(
            dict(
                key=key,
                operator='Equal',
                value='user',
                effect='NoSchedule',
            )
        )

    kube_spawner = configure_kube_spawner_volumes(kube_spawner)

    kube_spawner = configure_kube_spawner_init_containers(kube_spawner)

    return kube_spawner


def configure_spawner(spawner):
    # Max number of consecutive failures before the Hub restarts itself
    # requires jupyterhub 0.9.2
    set_config_if_not_none(
        spawner,
        'consecutive_failure_limit',
        'hub.consecutiveFailureLimit',
    )

    set_config_if_not_none(spawner, 'cmd', 'singleuser.cmd')
    set_config_if_not_none(spawner, 'default_url', 'singleuser.defaultUrl')

    return spawner


def configure_authentication(context):
    auth_type = get_config('auth.type')

    common_oauth_traits = (
        ('client_id', None),
        ('client_secret', None),
        ('oauth_callback_url', 'callbackUrl'),
    )

    # this maps a string `auth_type` to two attributes:
    # * `authenticator_class`, the full qualified path of the authenticators' class
    # * `traits`, a tuple of pairs whose first element is the attribute of the authenticators' class and the second element is the name of that attribute on the configmap.
    if auth_type == 'google':
        authenticator_class = 'oauthenticator.GoogleOAuthenticator'
        traits = common_oauth_traits + (
            ('hosted_domain', None),
            ('login_service', None),
        )
    elif auth_type == 'github':
        authenticator_class = 'oauthenticator.github.GitHubOAuthenticator'
        traits = common_oauth_traits + (
            ('github_organization_whitelist', 'orgWhitelist'),
        )
    elif auth_type == 'cilogon':
        authenticator_class = 'oauthenticator.CILogonOAuthenticator'
        traits = common_oauth_traits
    elif auth_type == 'gitlab':
        authenticator_class = 'oauthenticator.gitlab.GitLabOAuthenticator'
        traits = common_oauth_traits + (
            ('gitlab_group_whitelist', None),
            ('gitlab_project_id_whitelist', None),
            ('gitlab_url', None),
        )
    elif auth_type == 'azuread':
        authenticator_class = 'oauthenticator.azuread.AzureAdOAuthenticator'
        traits = common_oauth_traits + (
            ('tenant_id', None),
            ('username_claim', None),
        )
    elif auth_type == 'mediawiki':
        authenticator_class = 'oauthenticator.mediawiki.MWOAuthenticator'
        traits = common_oauth_traits + (
            ('index_url', None),
        )
    elif auth_type == 'globus':
        authenticator_class = 'oauthenticator.globus.GlobusOAuthenticator'
        traits = common_oauth_traits + (
            ('identity_provider', None),
        )
    elif auth_type == 'hmac':
        authenticator_class = 'hmacauthenticator.HMACAuthenticator'
        traits = (
            ('secret_key', None),
        )
    elif auth_type == 'dummy':
        authenticator_class = 'dummyauthenticator.DummyAuthenticator'
        traits = (
            ('password', None)
        )
    elif auth_type == 'tmp':
        authenticator_class = 'tmpauthenticator.TmpAuthenticator'
        traits = tuple()
    elif auth_type == 'lti':
        authenticator_class = 'ltiauthenticator.LTIAuthenticator'
        traits = (
            ('consumers', None),
        )
    elif auth_type == 'ldap':
        authenticator_class = 'ldapauthenticator.LDAPAuthenticator'
        traits = (
            ('server_address', 'server.address'),
            ('server_port', 'server.port'),
            ('use_ssl', 'server.ssl'),
            ('allowed_groups', 'allowedGroups'),
            ('bind_dn_template', 'dn.templates'),
            ('lookup_dn', 'dn.lookup'),
            ('lookup_dn_search_filter', 'dn.search.filter'),
            ('lookup_dn_search_user', 'dn.search.user'),
            ('lookup_dn_search_password', 'dn.search.password'),
            ('lookup_dn_user_dn_attribute', 'dn.user.dnAttribute'),
            ('escape_userdn', 'dn.user.escape'),
            ('valid_username_regex', 'dn.user.validRegex'),
            ('user_search_base', 'dn.user.searchBase'),
            ('user_attribute', 'dn.user.attribute'),
        )
    elif auth_type == 'custom':
        # full_class_name looks like "myauthenticator.MyAuthenticator".
        # To create a docker image with this class availabe, you can just have the
        # following Dockerfile:
        #   FROM jupyterhub/k8s-hub:v0.4
        #   RUN pip3 install myauthenticator
        authenticator_class = get_config('auth.custom.className')
        authenticator_class_name = authenticator_class.rsplit('.', 1)[-1]

        # update all values
        context[authenticator_class_name].update(get_config('auth.custom.config') or {})
        return context
    else:
        raise ValueError("Unhandled auth type: %r" % auth_type)

    # set all attributes of the authenticator
    authenticator_class_name = authenticator_class.rsplit('.', 1)[-1]
    for trait, cfg_key in traits:
        if cfg_key is None:
            cfg_key = camelCaseify(trait)

        data = get_config('auth.{}.{}'.format(prefix, auth_type, cfg_key))
        if data is not None:
            if auth_type == 'hmac' and trait == 'secret_key':
                # hmac requires a custom transformation
                data = bytes.fromhex(data)
            setattr(context[authenticator_class_name], trait, data)

    return context


def _cull_service(base_url):
    cmd = [
        'python3',
        '-m',
        'jupyterhub_idle_culler'
    ]
    cmd.append(
        '--url=http://localhost:8081' + url_path_join(base_url, 'hub/api')
    )

    cull_timeout = get_config('cull.timeout')
    if cull_timeout:
        cmd.append('--timeout=%s' % cull_timeout)

    cull_every = get_config('cull.every')
    if cull_every:
        cmd.append('--cull-every=%s' % cull_every)

    cull_concurrency = get_config('cull.concurrency')
    if cull_concurrency:
        cmd.append('--concurrency=%s' % cull_concurrency)

    if get_config('cull.users'):
        cmd.append('--cull-users')

    if get_config('cull.removeNamedServers'):
        cmd.append('--remove-named-servers')

    cull_max_age = get_config('cull.maxAge')
    if cull_max_age:
        cmd.append('--max-age=%s' % cull_max_age)

    return {
        'name': 'cull-idle',
        'admin': True,
        'command': cmd,
    }


def jupuyterhub_services(base_url):
    services = []

    if get_config('cull.enabled', False):
        services.append(_cull_service(base_url))

    for name, service in get_config('hub.services', {}).items():
        # jupyterhub.services is a list of dicts, but
        # in the helm chart it is a dict of dicts for easier merged-config
        service.setdefault('name', name)
        # handle camelCase->snake_case of api_token
        api_token = service.pop('apiToken', None)
        if api_token:
            service['api_token'] = api_token
        services.append(service)

    return services


def configure_jupuyterhub(jupyterhub):
    jupyterhub.spawner_class = 'kubespawner.KubeSpawner'

    # Do not shut down user pods when hub is restarted
    jupyterhub.cleanup_servers = False

    # Check that the proxy has routes appropriately setup
    jupyterhub.last_activity_interval = 60

    # Don't wait at all before redirecting a spawning user to the progress page
    jupyterhub.tornado_settings = {
        'slow_spawn_timeout': 0,
    }

    # configure the hub db connection
    db_type = get_config('hub.db.type')
    if db_type == 'sqlite-pvc':
        jupyterhub.db_url = "sqlite:///jupyterhub.sqlite"
    elif db_type == "sqlite-memory":
        jupyterhub.db_url = "sqlite://"
    else:
        set_config_if_not_none(jupyterhub, "db_url", "hub.db.url")


    for trait, cfg_key in (
        # Max number of servers that can be spawning at any one time
        ('concurrent_spawn_limit', None),
        # Max number of servers to be running at one time
        ('active_server_limit', None),
        # base url prefix
        ('base_url', None),
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
        set_config_if_not_none(jupyterhub, trait, 'hub.' + cfg_key)

    jupyterhub.ip = os.environ['PROXY_PUBLIC_SERVICE_HOST']
    jupyterhub.port = int(os.environ['PROXY_PUBLIC_SERVICE_PORT'])

    # the hub should listen on all interfaces, so the proxy can access it
    jupyterhub.hub_ip = '0.0.0.0'

    # Gives spawned containers access to the API of the hub
    jupyterhub.hub_connect_ip = os.environ['HUB_SERVICE_HOST']
    jupyterhub.hub_connect_port = int(os.environ['HUB_SERVICE_PORT'])

    return jupyterhub


def extra_configurations():
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

    return extra_config
