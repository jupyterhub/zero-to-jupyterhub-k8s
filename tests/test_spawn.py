import os
import subprocess
import time

import pytest
import requests
import yaml

# Makes heavy use of JupyterHub's API:
# http://petstore.swagger.io/?url=https://raw.githubusercontent.com/jupyterhub/jupyterhub/master/docs/rest-api.yml

# load app version of chart
here = os.path.dirname(os.path.abspath(__file__))
chart_yaml = os.path.join(here, os.pardir, "jupyterhub", "Chart.yaml")

with open(chart_yaml) as f:
    chart = yaml.safe_load(f)
    jupyterhub_version = chart["appVersion"]


def test_api(api_request):
    """
    Tests the hub api's root endpoint (/). The hub's version should be returned.

    A typical jupyterhub logging response to this test:
        
        [I 2019-09-25 12:03:12.051 JupyterHub log:174] 200 GET /hub/api (test@127.0.0.1) 9.57ms
    """

    print("asking for the hub's version")
    r = api_request.get("")
    assert r.status_code == 200
    assert r.json().get("version", "version-missing") == jupyterhub_version



def test_api_info(api_request):
    """
    Tests the hub api's /info endpoint. Information about the hub should be
    returned.

    A typical jupyterhub logging response to this test:

        [I 2019-09-25 12:03:12.086 JupyterHub log:174] 200 GET /hub/api/info (test@127.0.0.1) 10.21ms
    """

    print("asking for the hub information")
    r = api_request.get("/info")
    assert r.status_code == 200
    result = r.json()
    assert result["spawner"]["class"] == "kubespawner.spawner.KubeSpawner"


def test_hub_api_create_user_and_get_information_about_user(api_request, jupyter_user):
    """
    Tests the hub api's /users/:user endpoint, both POST and GET.

    A jupyter user is created and commited to the hub database through the
    jupyter_user pytest fixture declared in conftest.py. Due to this, this first
    test to use the jupyter_user fixture is actually testing both the pytest
    fixture that creates the user as well as the ability to get information from
    the hub about the user. The jupyter_user fixture will automatically clean up
    the user from the hub's database when this function exits.

    A typical jupyterhub logging response to this test:

        [I 2019-09-25 12:03:12.126 JupyterHub log:174] 201 POST /hub/api/users/testuser-7c70eb90-035b-4d9f-92a5-482e441e307d (test@127.0.0.1) 20.74ms
        [I 2019-09-25 12:03:12.153 JupyterHub log:174] 200 GET /hub/api/users/testuser-7c70eb90-035b-4d9f-92a5-482e441e307d (test@127.0.0.1) 11.91ms
        [D 2019-09-25 12:03:12.180 JupyterHub user:240] Creating <class 'kubespawner.spawner.KubeSpawner'> for testuser-7c70eb90-035b-4d9f-92a5-482e441e307d:
        [I 2019-09-25 12:03:12.204 JupyterHub reflector:199] watching for pods with label selector='component=singleuser-server' in namespace jh-dev
        [D 2019-09-25 12:03:12.205 JupyterHub reflector:202] Connecting pods watcher
        [I 2019-09-25 12:03:12.229 JupyterHub reflector:199] watching for events with field selector='involvedObject.kind=Pod' in namespace jh-dev
        [D 2019-09-25 12:03:12.229 JupyterHub reflector:202] Connecting events watcher
        [I 2019-09-25 12:03:12.269 JupyterHub log:174] 204 DELETE /hub/api/users/testuser-7c70eb90-035b-4d9f-92a5-482e441e307d (test@127.0.0.1) 98.85ms
    """
    print("create a user, and get information about the user")
    r = api_request.get("/users/" + jupyter_user)
    assert r.status_code == 200
    assert r.json()["name"] == jupyter_user


def test_hub_api_list_users(api_request, jupyter_user):
    """
    Tests the hub api's /users endpoint. Information about users should be
    returned.

    A typical jupyterhub logging response to this test:

        [I 2019-09-25 12:03:12.303 JupyterHub log:174] 201 POST /hub/api/users/testuser-0d2b0fc9-5ac4-4d8c-8d25-c4545665f81f (test@127.0.0.1) 15.53ms
        [I 2019-09-25 12:03:12.331 JupyterHub log:174] 200 GET /hub/api/users (test@127.0.0.1) 10.83ms
        [D 2019-09-25 12:03:12.358 JupyterHub user:240] Creating <class 'kubespawner.spawner.KubeSpawner'> for testuser-0d2b0fc9-5ac4-4d8c-8d25-c4545665f81f:
        [I 2019-09-25 12:03:12.365 JupyterHub log:174] 204 DELETE /hub/api/users/testuser-0d2b0fc9-5ac4-4d8c-8d25-c4545665f81f (test@127.0.0.1) 18.44ms
    """

    print("create a test user, get information about all users, and find the test user")
    r = api_request.get("/users")
    assert r.status_code == 200
    assert any(u["name"] == jupyter_user for u in r.json())


def test_hub_can_talk_to_proxy(api_request, request_data):
    """
    Tests the hub api's /proxy endpoint.

    A typical jupyterhub logging response to this test:

        [I 2019-09-25 12:03:12.395 JupyterHub log:174] 200 GET /hub/api/proxy (test@127.0.0.1) 13.48ms
    """

    endtime = time.time() + request_data["test_timeout"]
    while time.time() < endtime:
        try:
            r = api_request.get("/proxy")
            if r.status_code == 200:
                break
            print(r.json())
        except requests.RequestException as e:
            print(e)
        time.sleep(1)
    assert r.status_code == 200, "Failed to get /proxy"


def test_hub_api_request_user_spawn(api_request, jupyter_user, request_data, pebble_acme_ca_cert):
    """
    Tests the hub api's /users/:user/server POST endpoint. A user pod should be
    created with environment variables defined in singleuser.extraEnv etc.
    """

    print("asking kubespawner to spawn a server for a test user")
    r = api_request.post("/users/" + jupyter_user + "/server")
    assert r.status_code in (201, 202)
    try:
        # check successfull spawn
        server_model = _wait_for_user_to_spawn(
            api_request, jupyter_user, request_data["test_timeout"]
        )
        assert server_model
        r = requests.get(
            request_data["hub_url"].partition("/hub/api")[0]
            + server_model["url"]
            + "api",
            verify=pebble_acme_ca_cert,
        )
        assert r.status_code == 200
        assert "version" in r.json()

        # check user pod's extra environment variable
        pod_name = server_model["state"]["pod_name"]
        c = subprocess.run([
            "kubectl", "exec", pod_name, "--",
            "sh", "-c", "if [ -z $TEST_ENV_FIELDREF_TO_NAMESPACE ]; then exit 1; fi",
        ])
        assert c.returncode == 0, f"singleuser.extraEnv didn't lead to a mounted environment variable!"
    finally:
        _delete_server(api_request, jupyter_user, request_data["test_timeout"])


@pytest.mark.netpol
def test_singleuser_netpol(api_request, jupyter_user, request_data):
    """
    Tests a spawned user pods ability to communicate with allowed and blocked
    internet locations.
    """

    print("asking kubespawner to spawn a server for a test user to test network policies")
    r = api_request.post("/users/" + jupyter_user + "/server")
    assert r.status_code in (201, 202)
    try:
        server_model = _wait_for_user_to_spawn(
            api_request, jupyter_user, request_data["test_timeout"]
        )
        assert server_model
        print(server_model)
        pod_name = server_model["state"]["pod_name"]

        c = subprocess.run([
            "kubectl", "exec", pod_name, "--",
            "nslookup", "hub",
        ])
        assert c.returncode == 0, "DNS issue: failed to resolve 'hub' from a singleuser-server"

        c = subprocess.run([
            "kubectl", "exec", pod_name, "--",
            "nslookup", "jupyter.org",
        ])
        assert c.returncode == 0, "DNS issue: failed to resolve 'jupyter.org' from a singleuser-server"

        # Must match CIDR in singleuser.networkPolicy.egress.
        allowed_url = "http://jupyter.org"
        blocked_url = "http://mybinder.org"

        c = subprocess.run([
            "kubectl", "exec", pod_name, "--",
            "wget", "--quiet", "--tries=3", "--timeout=3", allowed_url,
        ])
        assert c.returncode == 0, f"Network issue: access to '{blocked_url}' was supposed to be allowed"

        c = subprocess.run([
            "kubectl", "exec", pod_name, "--",
            "wget", "--quiet", "--server-response", "-O-", "--tries=3", "--timeout=3", blocked_url,
        ])
        assert c.returncode > 0, f"Network issue: access to '{blocked_url}' was supposed to be denied"

    finally:
        _delete_server(api_request, jupyter_user, request_data["test_timeout"])


def _wait_for_user_to_spawn(api_request, jupyter_user, timeout):
    endtime = time.time() + timeout
    while time.time() < endtime:
        # NOTE: If this request fails with a 503 response from the proxy, the
        #       hub pod has probably crashed by the tests interaction with it.
        r = api_request.get("/users/" + jupyter_user)
        r.raise_for_status()
        user_model = r.json()

        # will be pending while starting,
        # server will be set when ready
        if "" not in user_model["servers"]:
            # spawn failed!
            raise RuntimeError("Server never started!")

        server_model = user_model["servers"][""]
        if server_model["ready"]:
            return server_model

        time.sleep(1)
    return False


def _delete_server(api_request, jupyter_user, timeout):
    # NOTE: If this request fails with a 503 response from the proxy, the hub
    #       pod has probably crashed by the previous tests' interaction with it.
    r = api_request.delete("/users/" + jupyter_user + "/server")
    assert r.status_code in (202, 204)

    endtime = time.time() + timeout
    while time.time() < endtime:
        r = api_request.get("/users/" + jupyter_user)
        r.raise_for_status()
        user_model = r.json()
        if "" not in user_model["servers"]:
            return True
        time.sleep(1)
    return False
