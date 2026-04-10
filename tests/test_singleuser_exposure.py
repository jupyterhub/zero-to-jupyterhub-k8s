import asyncio
import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "jupyterhub"
    / "files"
    / "hub"
    / "singleuser_exposure.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("singleuser_exposure", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_spawner():
    return SimpleNamespace(
        name="",
        pod_name="jupyter-alice",
        namespace="ns1",
        port=8888,
        user=SimpleNamespace(name="alice", escaped_name="alice"),
        server=SimpleNamespace(base_url="/user/alice/"),
        common_labels={"app.kubernetes.io/name": "jupyterhub"},
        component_label="singleuser-server",
    )


def make_pod():
    return {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "name": "jupyter-alice",
            "uid": "pod-uid",
        },
    }


class ConfigSection(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as exc:  # pragma: no cover - defensive
            raise AttributeError(name) from exc

    def __setattr__(self, name, value):
        self[name] = value


class ConfigRoot:
    def __init__(self):
        self.KubeSpawner = ConfigSection()


def test_build_loadbalancer_service_patch():
    module = load_module()
    spawner = make_spawner()
    service = {
        "metadata": {
            "name": "jupyter-alice",
            "labels": {"existing": "label"},
            "annotations": {"existing": "annotation"},
        },
        "spec": {
            "type": "ClusterIP",
            "ports": [{"name": "notebook-port", "port": 8888}],
        },
    }
    exposure_config = {
        "enabled": True,
        "type": "loadBalancer",
        "annotations": {"anno": "{service_name}"},
        "labels": {"label": "{username}"},
        "service": {
            "externalTrafficPolicy": "Local",
            "loadBalancerClass": "internal-vip",
        },
    }

    patch = module.build_loadbalancer_service_patch(spawner, service, exposure_config)

    assert patch["spec"]["type"] == "LoadBalancer"
    assert patch["spec"]["externalTrafficPolicy"] == "Local"
    assert patch["spec"]["loadBalancerClass"] == "internal-vip"
    assert patch["metadata"]["labels"]["existing"] == "label"
    assert patch["metadata"]["labels"]["label"] == "alice"
    assert patch["metadata"]["labels"]["hub.jupyter.org/external-access"] == "true"
    assert patch["metadata"]["annotations"]["existing"] == "annotation"
    assert patch["metadata"]["annotations"]["anno"] == "jupyter-alice"
    assert patch["spec"]["ports"][0] == {
        "name": "ssh",
        "port": 22,
        "targetPort": 22,
        "protocol": "TCP",
    }
    assert patch["spec"]["ports"][1]["name"] == "notebook-port"
    assert patch["spec"]["ports"][1]["port"] == 8888


def test_build_loadbalancer_service_patch_uses_custom_ssh_ports():
    module = load_module()
    spawner = make_spawner()
    service = {
        "metadata": {"name": "jupyter-alice"},
        "spec": {"type": "ClusterIP", "ports": [{"name": "notebook-port", "port": 8888}]},
    }
    exposure_config = {
        "enabled": True,
        "type": "loadBalancer",
        "ssh": {"enabled": True, "externalPort": 2222, "containerPort": 10022},
        "service": {},
    }

    patch = module.build_loadbalancer_service_patch(spawner, service, exposure_config)

    assert patch["spec"]["ports"][0] == {
        "name": "ssh",
        "port": 2222,
        "targetPort": 10022,
        "protocol": "TCP",
    }
    assert patch["spec"]["ports"][1]["name"] == "notebook-port"
    assert patch["spec"]["ports"][1]["port"] == 8888


def test_build_clusterip_service_patch_for_route_sets_ssh_port():
    module = load_module()
    spawner = make_spawner()
    service = {
        "metadata": {"name": "jupyter-alice", "labels": {"existing": "label"}},
        "spec": {"type": "ClusterIP", "ports": [{"name": "notebook-port", "port": 8888}]},
    }
    exposure_config = {
        "enabled": True,
        "type": "route",
        "ssh": {"enabled": True, "externalPort": 22, "containerPort": 22},
        "labels": {"label": "{username}"},
    }

    patch = module.build_clusterip_service_patch(spawner, service, exposure_config)

    assert patch["spec"]["type"] == "ClusterIP"
    assert patch["spec"]["ports"][0] == {
        "name": "ssh",
        "port": 22,
        "targetPort": 22,
        "protocol": "TCP",
    }
    assert patch["spec"]["ports"][1]["name"] == "notebook-port"
    assert patch["spec"]["ports"][1]["port"] == 8888
    assert patch["metadata"]["labels"]["label"] == "alice"
    assert patch["metadata"]["labels"]["existing"] == "label"


def test_build_route_manifest_targets_service_and_keeps_stable_name():
    module = load_module()
    spawner = make_spawner()
    pod = make_pod()
    service = {
        "metadata": {"name": "jupyter-alice"},
        "spec": {
            "ports": [
                {
                    "name": "notebook-port",
                    "port": 8888,
                    "targetPort": "notebook-port",
                }
            ]
        },
    }
    exposure_config = {
        "enabled": True,
        "type": "route",
        "hostTemplate": "{service_name}.apps.example.com",
        "annotations": {"anno": "{user_server}"},
        "labels": {"label": "{username}"},
        "route": {
            "wildcardPolicy": "None",
        },
    }

    manifest = module.build_route_manifest(spawner, pod, service, exposure_config)

    assert manifest["metadata"]["name"] == "jupyter-alice"
    assert manifest["metadata"]["annotations"]["anno"] == "alice"
    assert manifest["metadata"]["labels"]["label"] == "alice"
    assert manifest["metadata"]["ownerReferences"][0]["uid"] == "pod-uid"
    assert manifest["spec"]["to"]["name"] == "jupyter-alice"
    assert manifest["spec"]["port"]["targetPort"] == "notebook-port"
    assert manifest["spec"]["host"] == "jupyter-alice.apps.example.com"
    assert "tls" not in manifest["spec"]
    assert manifest["spec"]["wildcardPolicy"] == "None"


def test_build_route_manifest_includes_tls_when_configured():
    module = load_module()
    spawner = make_spawner()
    pod = make_pod()
    service = {
        "metadata": {"name": "jupyter-alice"},
        "spec": {
            "ports": [
                {
                    "name": "notebook-port",
                    "port": 8888,
                    "targetPort": "notebook-port",
                }
            ]
        },
    }
    exposure_config = {
        "enabled": True,
        "type": "route",
        "route": {
            "tls": {"termination": "edge"},
        },
    }

    manifest = module.build_route_manifest(spawner, pod, service, exposure_config)

    assert manifest["spec"]["tls"]["termination"] == "edge"


def test_chain_hooks_runs_existing_before_new():
    module = load_module()
    calls = []

    async def existing(*args, **kwargs):
        calls.append(("existing", args, kwargs))

    async def new(*args, **kwargs):
        calls.append(("new", args, kwargs))

    asyncio.run(module.chain_hooks(existing, new)("spawner", pod="pod"))

    assert [call[0] for call in calls] == ["existing", "new"]


def test_configure_singleuser_exposure_enables_services_and_registers_hooks(
    monkeypatch,
):
    module = load_module()
    applied = []
    cleaned = []

    async def fake_apply(spawner, exposure_config, pod):
        applied.append((spawner.pod_name, exposure_config["type"], pod["metadata"]["uid"]))

    async def fake_cleanup(spawner, exposure_config):
        cleaned.append((spawner.pod_name, exposure_config["type"]))

    monkeypatch.setattr(module, "apply_exposure", fake_apply)
    monkeypatch.setattr(module, "cleanup_exposure", fake_cleanup)

    c = ConfigRoot()

    def get_config(key, default=None):
        if key == "singleuser.exposure":
            return {"enabled": True, "type": "loadBalancer", "service": {}}
        return default

    module.configure_singleuser_exposure(c, get_config)

    assert c.KubeSpawner.services_enabled is True
    assert c.KubeSpawner.after_pod_created_hook is not None
    assert c.KubeSpawner.post_stop_hook is not None

    spawner = make_spawner()
    pod = make_pod()
    asyncio.run(c.KubeSpawner.after_pod_created_hook(spawner, pod))
    asyncio.run(c.KubeSpawner.post_stop_hook(spawner))

    assert applied == [("jupyter-alice", "loadBalancer", "pod-uid")]
    assert cleaned == [("jupyter-alice", "loadBalancer")]


def test_validate_exposure_config_rejects_unknown_type():
    module = load_module()

    with pytest.raises(module.ExposureConfigError):
        module.validate_exposure_config({"enabled": True, "type": "httpRoute"})
