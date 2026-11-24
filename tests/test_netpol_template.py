"""Tests for Helm NetworkPolicy template rendering."""

import os
import subprocess

import yaml

CHART_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, "jupyterhub")
)


def _render_netpol(template, namespace="jupyterhub", set_values=()):
    cmd = [
        "helm",
        "template",
        "test-release",
        CHART_DIR,
        "--namespace",
        namespace,
        "--show-only",
        template,
    ]
    for value in set_values:
        cmd.extend(["--set", value])
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return yaml.safe_load(result.stdout)


def _egress_peer_for_component(netpol, component):
    for rule in netpol["spec"]["egress"]:
        for peer in rule.get("to", []):
            labels = peer.get("podSelector", {}).get("matchLabels", {})
            if labels.get("component") == component:
                return peer
    raise AssertionError(f"No egress rule found for component {component!r}")


def test_singleuser_netpol_default_namespace():
    singleuser = _render_netpol("templates/singleuser/netpol.yaml")
    hub = _render_netpol("templates/hub/netpol.yaml")
    proxy = _render_netpol("templates/proxy/netpol.yaml")

    assert "namespace" not in singleuser["metadata"]
    assert singleuser["spec"]["ingress"][0]["from"] == [
        {
            "podSelector": {
                "matchLabels": {"hub.jupyter.org/network-access-singleuser": "true"}
            }
        }
    ]
    for component in ("hub", "proxy", "autohttps"):
        assert "namespaceSelector" not in _egress_peer_for_component(
            singleuser, component
        )
    assert hub["spec"]["ingress"][0]["from"] == [
        {
            "podSelector": {
                "matchLabels": {"hub.jupyter.org/network-access-hub": "true"}
            }
        }
    ]
    assert "namespaceSelector" not in _egress_peer_for_component(
        hub, "singleuser-server"
    )
    assert "namespaceSelector" not in _egress_peer_for_component(
        proxy, "singleuser-server"
    )


def test_singleuser_netpol_custom_namespace():
    set_values = ("singleuser.networkPolicy.namespace=jupyterhub-users",)
    singleuser = _render_netpol(
        "templates/singleuser/netpol.yaml",
        namespace="jupyterhub",
        set_values=set_values,
    )
    hub = _render_netpol(
        "templates/hub/netpol.yaml",
        namespace="jupyterhub",
        set_values=set_values,
    )
    proxy = _render_netpol(
        "templates/proxy/netpol.yaml",
        namespace="jupyterhub",
        set_values=set_values,
    )

    assert singleuser["metadata"]["namespace"] == "jupyterhub-users"
    assert singleuser["spec"]["ingress"][0]["from"] == [
        {
            "podSelector": {
                "matchLabels": {"hub.jupyter.org/network-access-singleuser": "true"}
            }
        },
        {
            "podSelector": {
                "matchLabels": {"hub.jupyter.org/network-access-singleuser": "true"}
            },
            "namespaceSelector": {
                "matchLabels": {"kubernetes.io/metadata.name": "jupyterhub"}
            },
        },
    ]
    for component in ("hub", "proxy", "autohttps"):
        assert _egress_peer_for_component(singleuser, component)[
            "namespaceSelector"
        ] == {"matchLabels": {"kubernetes.io/metadata.name": "jupyterhub"}}

    assert hub["spec"]["ingress"][0]["from"] == [
        {
            "podSelector": {
                "matchLabels": {"hub.jupyter.org/network-access-hub": "true"}
            }
        },
        {
            "podSelector": {
                "matchLabels": {"hub.jupyter.org/network-access-hub": "true"}
            },
            "namespaceSelector": {
                "matchLabels": {"kubernetes.io/metadata.name": "jupyterhub-users"}
            },
        },
    ]
    assert _egress_peer_for_component(hub, "singleuser-server")[
        "namespaceSelector"
    ] == {"matchLabels": {"kubernetes.io/metadata.name": "jupyterhub-users"}}
    assert "namespaceSelector" not in _egress_peer_for_component(hub, "proxy")

    assert _egress_peer_for_component(proxy, "singleuser-server")[
        "namespaceSelector"
    ] == {"matchLabels": {"kubernetes.io/metadata.name": "jupyterhub-users"}}
    assert "namespaceSelector" not in _egress_peer_for_component(proxy, "hub")


def test_singleuser_netpol_same_namespace():
    set_values = ("singleuser.networkPolicy.namespace=jupyterhub",)
    singleuser = _render_netpol(
        "templates/singleuser/netpol.yaml",
        namespace="jupyterhub",
        set_values=set_values,
    )
    hub = _render_netpol(
        "templates/hub/netpol.yaml",
        namespace="jupyterhub",
        set_values=set_values,
    )
    proxy = _render_netpol(
        "templates/proxy/netpol.yaml",
        namespace="jupyterhub",
        set_values=set_values,
    )

    assert singleuser["metadata"]["namespace"] == "jupyterhub"
    assert singleuser["spec"]["ingress"][0]["from"] == [
        {
            "podSelector": {
                "matchLabels": {"hub.jupyter.org/network-access-singleuser": "true"}
            }
        }
    ]
    for component in ("hub", "proxy", "autohttps"):
        assert "namespaceSelector" not in _egress_peer_for_component(
            singleuser, component
        )
    assert hub["spec"]["ingress"][0]["from"] == [
        {
            "podSelector": {
                "matchLabels": {"hub.jupyter.org/network-access-hub": "true"}
            }
        }
    ]
    assert "namespaceSelector" not in _egress_peer_for_component(
        hub, "singleuser-server"
    )
    assert "namespaceSelector" not in _egress_peer_for_component(
        proxy, "singleuser-server"
    )


def test_singleuser_netpol_custom_namespace_accept_inter_namespace():
    singleuser = _render_netpol(
        "templates/singleuser/netpol.yaml",
        namespace="jupyterhub",
        set_values=(
            "singleuser.networkPolicy.namespace=jupyterhub-users",
            "singleuser.networkPolicy.interNamespaceAccessLabels=accept",
        ),
    )
    hub = _render_netpol(
        "templates/hub/netpol.yaml",
        namespace="jupyterhub",
        set_values=(
            "singleuser.networkPolicy.namespace=jupyterhub-users",
            "hub.networkPolicy.interNamespaceAccessLabels=accept",
        ),
    )

    assert singleuser["metadata"]["namespace"] == "jupyterhub-users"
    assert singleuser["spec"]["ingress"][0]["from"] == [
        {
            "podSelector": {
                "matchLabels": {"hub.jupyter.org/network-access-singleuser": "true"}
            },
            "namespaceSelector": {"matchLabels": {}},
        },
        {
            "namespaceSelector": {
                "matchLabels": {"hub.jupyter.org/network-access-singleuser": "true"}
            }
        },
    ]
    for component in ("hub", "proxy", "autohttps"):
        assert _egress_peer_for_component(singleuser, component)[
            "namespaceSelector"
        ] == {"matchLabels": {"kubernetes.io/metadata.name": "jupyterhub"}}

    assert hub["spec"]["ingress"][0]["from"] == [
        {
            "podSelector": {
                "matchLabels": {"hub.jupyter.org/network-access-hub": "true"}
            },
            "namespaceSelector": {"matchLabels": {}},
        },
        {
            "namespaceSelector": {
                "matchLabels": {"hub.jupyter.org/network-access-hub": "true"}
            }
        },
    ]
    assert _egress_peer_for_component(hub, "singleuser-server")[
        "namespaceSelector"
    ] == {"matchLabels": {"kubernetes.io/metadata.name": "jupyterhub-users"}}
