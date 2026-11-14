"""Check placeholder resource rendering without a running Kubernetes cluster."""

import json
import subprocess
from pathlib import Path

import pytest
import yaml

CHART = Path(__file__).resolve().parents[1] / "jupyterhub"


def render_placeholder(tmp_path, singleuser, resources=None, check=True):
    values = {
        "singleuser": singleuser,
        "scheduling": {"userPlaceholder": {"enabled": True, "replicas": 1}},
    }
    if resources is not None:
        values["scheduling"]["userPlaceholder"]["resources"] = resources
    path = tmp_path / "values.json"
    path.write_text(json.dumps(values))
    return subprocess.run(
        [
            "helm",
            "template",
            "memory-test",
            str(CHART),
            "--kube-version",
            "1.32.0",
            "--values",
            str(path),
            "--show-only",
            "templates/scheduling/user-placeholder/statefulset.yaml",
        ],
        check=check,
        capture_output=True,
        text=True,
    )


@pytest.mark.parametrize(
    "memory,expected",
    [
        ("1800M", 1887436800),
        ("1K", 1024),
        ("1G", 1073741824),
        ("1T", 1099511627776),
        ("1.5M", 1572864),
        ("0.1K", 102),
        (".5G", 536870912),
        ("01.5M", 1572864),
        ("+1.5M", 1572864),
        ("1.M", 1048576),
        ("1_024K", 1048576),
        ("1e-6M", 1),
        (123456, 123456),
        (123.9, 123),
        (None, None),
        (0, None),
        ("0M", None),
        ("1e-400K", None),
    ],
)
def test_placeholder_memory(tmp_path, memory, expected):
    result = render_placeholder(
        tmp_path, {"memory": {"guarantee": memory, "limit": memory}}
    )
    pod = yaml.safe_load(result.stdout)["spec"]["template"]["spec"]
    resources = pod["containers"][0].get("resources", {})
    for key in ("requests", "limits"):
        assert resources.get(key, {}).get("memory") == expected


def test_placeholder_other_resources(tmp_path):
    result = render_placeholder(
        tmp_path,
        {
            "memory": {"guarantee": "0M", "limit": "2G"},
            "cpu": {"guarantee": 0.5, "limit": 2},
            "extraResource": {"guarantees": {"example.com/device": "1"}},
        },
    )
    resources = yaml.safe_load(result.stdout)["spec"]["template"]["spec"]["containers"][
        0
    ]["resources"]
    assert resources == {
        "requests": {"cpu": 0.5, "example.com/device": "1"},
        "limits": {"cpu": 2, "memory": 2147483648},
    }


def test_placeholder_explicit_resources(tmp_path):
    resources = {
        "requests": {"memory": "1800M", "cpu": "100m"},
        "limits": {"memory": "2Gi"},
    }
    result = render_placeholder(
        tmp_path,
        {"memory": {"guarantee": "1800M", "limit": "2G"}},
        resources=resources,
    )
    pod = yaml.safe_load(result.stdout)["spec"]["template"]["spec"]
    assert pod["containers"][0]["resources"] == resources


@pytest.mark.parametrize("memory", ["bogusM", "1717Mi", "NaNM", "1e400M", "1__2M"])
def test_placeholder_invalid_memory(tmp_path, memory):
    result = render_placeholder(
        tmp_path, {"memory": {"guarantee": memory}}, check=False
    )
    assert result.returncode != 0
