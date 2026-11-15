"""Check the documented managed service's policies against chart pod labels."""

import re
import subprocess
from pathlib import Path

import yaml


def test_managed_service_example_allows_hub_and_proxy(tmp_path):
    root = Path(__file__).resolve().parents[1]
    documentation = (root / "docs/source/administrator/services.md").read_text()
    example = next(
        block
        for block in re.findall(r"```yaml\n(.*?)```", documentation, re.S)
        if "# config.yaml" in block
    )
    values = tmp_path / "values.yaml"
    values.write_text(example)
    rendered = subprocess.run(
        [
            "helm",
            "template",
            "services-test",
            str(root / "jupyterhub"),
            "--kube-version",
            "1.32.0",
            "--values",
            str(values),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    resources = [r for r in yaml.safe_load_all(rendered.stdout) if r]

    def resource(kind, component):
        return next(
            r
            for r in resources
            if r["kind"] == kind
            and r["metadata"]["labels"]["app.kubernetes.io/component"] == component
        )

    hub_labels = resource("Deployment", "hub")["spec"]["template"]["metadata"]["labels"]
    proxy_labels = resource("Deployment", "proxy")["spec"]["template"]["metadata"][
        "labels"
    ]
    rules = resource("NetworkPolicy", "hub")["spec"]["ingress"]

    def allowed(labels, port):
        for rule in rules:
            if not any(p["port"] == port for p in rule.get("ports", [])):
                continue
            for peer in rule.get("from", []):
                if set(peer) != {"podSelector"}:
                    continue
                selector = peer["podSelector"].get("matchLabels", {})
                if all(labels.get(k) == v for k, v in selector.items()):
                    return True
        return False

    assert allowed(hub_labels, 8181), "Hub cannot check the managed service's health"
    assert allowed(hub_labels, 8081), "Managed service cannot reach the Hub API"
    assert allowed(proxy_labels, 8181), "Proxy cannot reach the managed service"
    assert not allowed({"component": "unrelated"}, 8181)
    assert not allowed(hub_labels, 9999)
