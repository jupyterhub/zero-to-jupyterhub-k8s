from collections.abc import Mapping

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
