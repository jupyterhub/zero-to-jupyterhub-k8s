"""conftest.py has a special meaning to pytest

ref: https://docs.pytest.org/en/latest/writing_plugins.html#conftest-py-plugins
"""

import os
import requests
import uuid

import pytest
import yaml


@pytest.fixture(scope="module")
def request_data():
    basedir = os.path.dirname(os.path.dirname(__file__))
    with open(os.path.join(basedir, "dev-config.yaml")) as f:
        y = yaml.safe_load(f)
    token = y["hub"]["services"]["test"]["apiToken"]
    host = os.environ.get("Z2JH_PORT_FORWARD_ADDRESS", "localhost")
    port = os.environ.get("Z2JH_PORT_FORWARD_PORT", "8080")
    return {
        "token": token,
        "hub_url": f'http://{host}:{port}/hub/api',
        "headers": {"Authorization": f"token {token}"},
        "test_timeout": 300,
        "request_timeout": 60,
    }


class JupyterRequest(object):
    def __init__(self, request_data):
        self.request_data = request_data

    def _setup_kwargs(self, kwargs):
        kwargs["headers"] = kwargs.get("headers", self.request_data["headers"])
        kwargs["timeout"] = kwargs.get("timeout", self.request_data["request_timeout"])

    def delete(self, api, **kwargs):
        self._setup_kwargs(kwargs)
        return requests.delete(self.request_data["hub_url"] + api, **kwargs)

    def get(self, api, **kwargs):
        self._setup_kwargs(kwargs)
        return requests.get(self.request_data["hub_url"] + api, **kwargs)

    def post(self, api, **kwargs):
        self._setup_kwargs(kwargs)
        return requests.post(self.request_data["hub_url"] + api, **kwargs)

    def put(self, api, **kwargs):
        self._setup_kwargs(kwargs)
        return requests.put(self.request_data["hub_url"] + api, **kwargs)


@pytest.fixture(scope="function")
def api_request(request_data):
    return JupyterRequest(request_data)


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
