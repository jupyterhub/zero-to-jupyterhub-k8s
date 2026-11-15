"""Validate the chart's mounted configuration without a Kubernetes cluster."""

import importlib.util
import io
from pathlib import Path
from types import SimpleNamespace

import pytest


@pytest.fixture
def hub_config(monkeypatch):
    path = Path(__file__).resolve().parents[1] / "jupyterhub/files/hub/z2jh.py"
    spec = importlib.util.spec_from_file_location("chart_config", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    files = {}
    monkeypatch.setattr(
        module, "os", SimpleNamespace(path=SimpleNamespace(exists=files.__contains__))
    )
    monkeypatch.setattr(
        module, "open", lambda path: io.StringIO(files[path]), raising=False
    )
    return module, files


@pytest.mark.parametrize("source", ["secret", "existing-secret"])
@pytest.mark.parametrize(
    "content", ["", "# empty file\n", "null", "missing.yaml", "123", "false", "[]"]
)
def test_non_mapping_config_names_the_file(hub_config, source, content):
    module, files = hub_config
    files["/usr/local/etc/jupyterhub/secret/values.yaml"] = (
        "hub:\n  db:\n    type: sqlite-pvc\n"
    )
    path = f"/usr/local/etc/jupyterhub/{source}/values.yaml"
    files[path] = content

    with pytest.raises(ValueError) as exc:
        module.get_config("hub.db.type")
    assert path in str(exc.value)
    assert "YAML mapping" in str(exc.value)
    if content == "missing.yaml":
        assert content not in str(exc.value)


@pytest.mark.parametrize("override", [None, "{}", "hub:\n  db:\n    type: postgres\n"])
def test_mapping_config_merge_and_optional_file(hub_config, override):
    module, files = hub_config
    files["/usr/local/etc/jupyterhub/secret/values.yaml"] = (
        "hub:\n  db:\n    type: sqlite-pvc\n    url: base-url\n"
    )
    if override is not None:
        files["/usr/local/etc/jupyterhub/existing-secret/values.yaml"] = override

    expected = "postgres" if override and "postgres" in override else "sqlite-pvc"
    assert module.get_config("hub.db.type") == expected
    assert module.get_config("hub.db.url") == "base-url"
