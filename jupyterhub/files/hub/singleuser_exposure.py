import copy
from collections.abc import Mapping

from jupyterhub.utils import exponential_backoff, maybe_future

try:
    from kubernetes_asyncio import client
    from kubernetes_asyncio.client import ApiException
except ImportError:  # pragma: no cover - local tooling may not have hub deps
    client = None

    class ApiException(Exception):
        def __init__(self, status=None, *args, **kwargs):
            super().__init__(*args)
            self.status = status


RESOURCE_TYPES = {
    "route": {
        "apiVersion": "route.openshift.io/v1",
        "group": "route.openshift.io",
        "version": "v1",
        "plural": "routes",
        "kind": "Route",
    }
}

EXPOSURE_TYPES = {"loadBalancer", "route"}
DEFAULT_SSH_PORT = 22
DEFAULT_SSH_PORT_NAME = "ssh"


class ExposureConfigError(ValueError):
    """Raised when singleuser.exposure is invalid."""


def get_service_name(spawner):
    return spawner.pod_name


def build_template_context(spawner, service_name=None):
    server_name = spawner.name or ""
    user_server = spawner.user.name
    if server_name:
        user_server = f"{user_server}--{server_name}"

    return {
        "username": spawner.user.name,
        "escaped_username": getattr(spawner.user, "escaped_name", spawner.user.name),
        "servername": server_name,
        "service_name": service_name or get_service_name(spawner),
        "pod_name": spawner.pod_name,
        "namespace": spawner.namespace,
        "base_url": spawner.server.base_url,
        "user_server": user_server,
    }


def render_template_string(template, context):
    try:
        return template.format_map(context)
    except KeyError as exc:
        raise ExposureConfigError(
            f"Unknown template field '{exc.args[0]}' in singleuser.exposure"
        ) from exc


def expand_templates(value, context):
    if isinstance(value, str):
        return render_template_string(value, context)
    if isinstance(value, list):
        return [expand_templates(item, context) for item in value]
    if isinstance(value, Mapping):
        return {key: expand_templates(item, context) for key, item in value.items()}
    return value


def validate_exposure_config(exposure_config):
    exposure_type = exposure_config.get("type")
    if exposure_type not in EXPOSURE_TYPES:
        raise ExposureConfigError(
            "singleuser.exposure.type must be one of: "
            + ", ".join(sorted(EXPOSURE_TYPES))
        )


def build_owner_reference(pod):
    return {
        "apiVersion": pod.get("apiVersion", "v1"),
        "kind": pod.get("kind", "Pod"),
        "name": pod["metadata"]["name"],
        "uid": pod["metadata"]["uid"],
        "blockOwnerDeletion": True,
        "controller": False,
    }


def build_resource_metadata(spawner, pod, exposure_config, service_name):
    context = build_template_context(spawner, service_name=service_name)
    labels = dict(getattr(spawner, "common_labels", {}) or {})
    labels.update(
        {
            "app.kubernetes.io/component": getattr(
                spawner, "component_label", "singleuser-server"
            ),
            "component": getattr(spawner, "component_label", "singleuser-server"),
            "hub.jupyter.org/external-access": "true",
        }
    )
    labels.update(expand_templates(exposure_config.get("labels", {}), context))

    metadata = {
        "name": service_name,
        "labels": labels,
        "ownerReferences": [build_owner_reference(pod)],
    }

    annotations = expand_templates(exposure_config.get("annotations", {}), context)
    if annotations:
        metadata["annotations"] = annotations

    return metadata


def get_service_ports(service, exposure_config):
    ssh_config = exposure_config.get("ssh", {})
    if not ssh_config.get("enabled", True):
        return copy.deepcopy(service.get("spec", {}).get("ports", []))

    service_port = ssh_config.get("externalPort")
    if service_port is None:
        service_port = DEFAULT_SSH_PORT

    target_port = ssh_config.get("containerPort")
    if target_port is None:
        target_port = service_port

    ssh_port = {
        "name": DEFAULT_SSH_PORT_NAME,
        "port": service_port,
        "targetPort": target_port,
        "protocol": "TCP",
    }
    existing_ports = copy.deepcopy(service.get("spec", {}).get("ports", []))
    existing_ports = [
        port for port in existing_ports if port.get("name") != DEFAULT_SSH_PORT_NAME
    ]
    return [ssh_port] + existing_ports


def build_service_metadata_patch(spawner, service, exposure_config):
    service_name = service["metadata"]["name"]
    context = build_template_context(spawner, service_name=service_name)

    labels = dict(service["metadata"].get("labels") or {})
    labels["hub.jupyter.org/external-access"] = "true"
    labels.update(expand_templates(exposure_config.get("labels", {}), context))

    annotations = dict(service["metadata"].get("annotations") or {})
    annotations.update(
        expand_templates(exposure_config.get("annotations", {}), context)
    )

    metadata = {"labels": labels}
    if annotations:
        metadata["annotations"] = annotations
    return metadata


def build_loadbalancer_service_patch(spawner, service, exposure_config):
    service_config = exposure_config.get("service", {})
    spec = {"type": "LoadBalancer"}
    for field in (
        "allocateLoadBalancerNodePorts",
        "externalTrafficPolicy",
        "ipFamilies",
        "ipFamilyPolicy",
        "loadBalancerClass",
        "loadBalancerIP",
        "loadBalancerSourceRanges",
    ):
        if service_config.get(field) is not None:
            spec[field] = service_config[field]

    ports = get_service_ports(service, exposure_config)
    if ports:
        spec["ports"] = ports

    return {
        "metadata": build_service_metadata_patch(spawner, service, exposure_config),
        "spec": spec,
    }


def build_clusterip_service_patch(spawner, service, exposure_config):
    spec = {"type": "ClusterIP"}
    ports = get_service_ports(service, exposure_config)
    if ports:
        spec["ports"] = ports

    return {
        "metadata": build_service_metadata_patch(spawner, service, exposure_config),
        "spec": spec,
    }


def get_route_target_port(service):
    service_port = (service.get("spec", {}).get("ports") or [{}])[0]
    return (
        service_port.get("name")
        or service_port.get("targetPort")
        or service_port.get("port")
    )


def build_route_manifest(spawner, pod, service, exposure_config):
    service_name = service["metadata"]["name"]
    context = build_template_context(spawner, service_name=service_name)
    route_config = exposure_config.get("route", {})
    spec = {
        "to": {
            "kind": "Service",
            "name": service_name,
        },
        "port": {
            "targetPort": get_route_target_port(service),
        },
    }

    if exposure_config.get("hostTemplate"):
        spec["host"] = render_template_string(exposure_config["hostTemplate"], context)

    tls_config = {
        key: value
        for key, value in expand_templates(route_config.get("tls", {}), context).items()
        if value is not None
    }
    if tls_config:
        spec["tls"] = tls_config

    if route_config.get("wildcardPolicy") is not None:
        spec["wildcardPolicy"] = route_config["wildcardPolicy"]

    return {
        "apiVersion": RESOURCE_TYPES["route"]["apiVersion"],
        "kind": RESOURCE_TYPES["route"]["kind"],
        "metadata": build_resource_metadata(
            spawner, pod, exposure_config, service_name=service_name
        ),
        "spec": spec,
    }


async def wait_for_service(api, namespace, name):
    async def get_service():
        try:
            return await api.read_namespaced_service(name=name, namespace=namespace)
        except ApiException as exc:
            if exc.status == 404:
                return False
            raise

    service = await exponential_backoff(
        get_service,
        f"Service {namespace}/{name} did not appear",
        timeout=30,
    )
    return service.to_dict()


async def apply_loadbalancer_service(api, spawner, service, exposure_config):
    patch = build_loadbalancer_service_patch(spawner, service, exposure_config)
    response = await api.patch_namespaced_service(
        name=service["metadata"]["name"],
        namespace=spawner.namespace,
        body=patch,
        _content_type="application/merge-patch+json",
    )
    response = response.to_dict()
    spawner.log.info(
        "Ensured LoadBalancer Service %s for %s",
        response["metadata"]["name"],
        spawner.server.base_url,
    )
    return response


async def apply_clusterip_service(api, spawner, service, exposure_config):
    patch = build_clusterip_service_patch(spawner, service, exposure_config)
    response = await api.patch_namespaced_service(
        name=service["metadata"]["name"],
        namespace=spawner.namespace,
        body=patch,
        _content_type="application/merge-patch+json",
    )
    response = response.to_dict()
    spawner.log.info(
        "Ensured ClusterIP Service %s for %s",
        response["metadata"]["name"],
        spawner.server.base_url,
    )
    return response


async def delete_service(api, spawner):
    try:
        await api.delete_namespaced_service(
            name=get_service_name(spawner),
            namespace=spawner.namespace,
            body=client.V1DeleteOptions(),
        )
    except ApiException as exc:
        if exc.status != 404:
            raise
    else:
        spawner.log.info("Deleted Service %s", get_service_name(spawner))


async def apply_route(api, spawner, service, exposure_config, pod):
    manifest = build_route_manifest(spawner, pod, service, exposure_config)
    resource = RESOURCE_TYPES["route"]
    name = manifest["metadata"]["name"]

    try:
        existing = await api.get_namespaced_custom_object(
            group=resource["group"],
            version=resource["version"],
            namespace=spawner.namespace,
            plural=resource["plural"],
            name=name,
        )
    except ApiException as exc:
        if exc.status != 404:
            raise
        response = await api.create_namespaced_custom_object(
            group=resource["group"],
            version=resource["version"],
            namespace=spawner.namespace,
            plural=resource["plural"],
            body=manifest,
        )
    else:
        manifest = copy.deepcopy(manifest)
        manifest["metadata"]["resourceVersion"] = existing["metadata"][
            "resourceVersion"
        ]
        response = await api.replace_namespaced_custom_object(
            group=resource["group"],
            version=resource["version"],
            namespace=spawner.namespace,
            plural=resource["plural"],
            name=name,
            body=manifest,
        )

    host = response.get("spec", {}).get("host") or response.get("status", {}).get(
        "ingress", [{}]
    )[0].get("host", "")
    spawner.log.info(
        "Ensured Route %s for %s%s",
        name,
        host or "<dynamic-host>",
        spawner.server.base_url,
    )


async def delete_route(api, spawner):
    resource = RESOURCE_TYPES["route"]

    try:
        await api.delete_namespaced_custom_object(
            group=resource["group"],
            version=resource["version"],
            namespace=spawner.namespace,
            plural=resource["plural"],
            name=get_service_name(spawner),
            body=client.V1DeleteOptions(),
        )
    except ApiException as exc:
        if exc.status != 404:
            raise
    else:
        spawner.log.info("Deleted Route %s", get_service_name(spawner))


async def apply_exposure(spawner, exposure_config, pod):
    if client is None:  # pragma: no cover - only relevant in hub runtime
        raise ExposureConfigError(
            "kubernetes_asyncio is required to manage singleuser exposure resources"
        )

    validate_exposure_config(exposure_config)

    async with client.ApiClient() as api_client:
        core_api = client.CoreV1Api(api_client)
        service = await wait_for_service(
            core_api, spawner.namespace, get_service_name(spawner)
        )

        if exposure_config["type"] == "loadBalancer":
            await apply_loadbalancer_service(
                core_api, spawner, service, exposure_config
            )
        elif exposure_config["type"] == "route":
            service = await apply_clusterip_service(
                core_api, spawner, service, exposure_config
            )
            custom_api = client.CustomObjectsApi(api_client)
            await apply_route(custom_api, spawner, service, exposure_config, pod)


async def cleanup_exposure(spawner, exposure_config):
    if client is None:  # pragma: no cover - only relevant in hub runtime
        raise ExposureConfigError(
            "kubernetes_asyncio is required to manage singleuser exposure resources"
        )

    async with client.ApiClient() as api_client:
        if exposure_config["type"] == "route":
            custom_api = client.CustomObjectsApi(api_client)
            await delete_route(custom_api, spawner)

        core_api = client.CoreV1Api(api_client)
        await delete_service(core_api, spawner)


def chain_hooks(existing_hook, new_hook):
    if existing_hook is None:
        return new_hook

    async def chained_hook(*args, **kwargs):
        await maybe_future(existing_hook(*args, **kwargs))
        return await maybe_future(new_hook(*args, **kwargs))

    return chained_hook


def configure_singleuser_exposure(c, get_config):
    exposure_config = copy.deepcopy(get_config("singleuser.exposure", {}))
    if not exposure_config.get("enabled"):
        return

    validate_exposure_config(exposure_config)

    c.KubeSpawner.services_enabled = True

    async def after_pod_created(spawner, pod):
        await apply_exposure(spawner, exposure_config, pod)

    async def post_stop(spawner):
        await cleanup_exposure(spawner, exposure_config)

    existing_after_hook = c.KubeSpawner.get("after_pod_created_hook")
    existing_post_stop_hook = c.KubeSpawner.get("post_stop_hook")

    c.KubeSpawner.after_pod_created_hook = chain_hooks(
        existing_after_hook, after_pod_created
    )
    c.KubeSpawner.post_stop_hook = chain_hooks(existing_post_stop_hook, post_stop)
