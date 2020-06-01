"""conftest.py has a special meaning to pytest

ref: https://docs.pytest.org/en/latest/writing_plugins.html#conftest-py-plugins
"""

import os
import requests
import uuid
from urllib.parse import urlparse

import pytest
import yaml

def pytest_configure(config):
    """
    A pytest hook, see:
    https://docs.pytest.org/en/2.7.3/plugins.html#_pytest.hookspec.pytest_configure
    """
    # Ignore InsecureRequestWarning associated with https:// web requests
    config.addinivalue_line(
        "filterwarnings", "ignore:Unverified HTTPS request"
    )
    # register our custom markers
    config.addinivalue_line(
        "markers", "netpol: mark test that require network policy enforcement"
    )


@pytest.fixture(scope="module")
def request_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    with open(os.path.join(base_dir, "dev-config.yaml")) as f:
        y = yaml.safe_load(f)
    token = y["hub"]["services"]["test"]["apiToken"]
    hub_url = os.environ.get("HUB_URL", "https://local.jovyan.org:30443")
    return {
        "token": token,
        "hub_url": f'{hub_url.rstrip("/")}/hub/api',
        "headers": {"Authorization": f"token {token}"},
        "test_timeout": 300,
        "request_timeout": 60,
    }


@pytest.fixture(scope="module")
def pebble_acme_ca_cert():
    """
    Acquires Pebble's ephemeral root certificate that when trusted implies trust
    to the ACME client's certificates. We can use the response of this function
    when we make web requests with the requests library.

        requests.get(..., verify=<True|False|path_to_certificate>)
    """
    response = requests.get("https://localhost:32444/roots/0", verify=False)
    if not response.ok:
        return True

    base_dir = os.path.dirname(os.path.dirname(__file__))
    cert_path = os.path.join(base_dir, "ci/ephemeral-pebble-acme-ca.crt")
    with open(cert_path, "w+") as f:
        f.write(response.text)
    return cert_path


class JupyterRequest(object):
    def __init__(self, request_data, pebble_acme_ca_cert):
        self.request_data = request_data
        self.pebble_acme_ca_cert = pebble_acme_ca_cert

    def _setup_kwargs(self, kwargs):
        kwargs["headers"] = kwargs.get("headers", self.request_data["headers"])
        kwargs["timeout"] = kwargs.get("timeout", self.request_data["request_timeout"])

    def delete(self, api, **kwargs):
        self._setup_kwargs(kwargs)
        return requests.delete(self.request_data["hub_url"] + api, verify=self.pebble_acme_ca_cert, **kwargs)

    def get(self, api, **kwargs):
        self._setup_kwargs(kwargs)
        return requests.get(self.request_data["hub_url"] + api, verify=self.pebble_acme_ca_cert, **kwargs)

    def post(self, api, **kwargs):
        self._setup_kwargs(kwargs)
        return requests.post(self.request_data["hub_url"] + api, verify=self.pebble_acme_ca_cert, **kwargs)

    def put(self, api, **kwargs):
        self._setup_kwargs(kwargs)
        return requests.put(self.request_data["hub_url"] + api, verify=self.pebble_acme_ca_cert, **kwargs)


@pytest.fixture(scope="function")
def api_request(request_data, pebble_acme_ca_cert):
    return JupyterRequest(request_data, pebble_acme_ca_cert)


@pytest.fixture(scope="function")
def jupyter_user(api_request):
    """
    A temporary unique JupyterHub user
    """
    username = "testuser-" + str(uuid.uuid4())
    r = api_request.post("/users/" + username)
    assert r.status_code == 201
    yield username
    r = api_request.delete("/users/" + username)
    assert r.status_code == 204
