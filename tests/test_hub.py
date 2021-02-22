"""
These tests commonl use JupyterHub's REST API:
http://petstore.swagger.io/?url=https://raw.githubusercontent.com/jupyterhub/jupyterhub/master/docs/rest-api.yml
"""

import os
import re
import subprocess
import time

import pytest
import requests
import yaml


def test_api_root(api_request):
    """
    Tests the hub api's root endpoint (/). The hub's version should be returned.

    A typical jupyterhub logging response to this test:

        [I 2019-09-25 12:03:12.051 JupyterHub log:174] 200 GET /hub/api (test@127.0.0.1) 9.57ms
    """

    # load app version of chart
    here = os.path.dirname(os.path.abspath(__file__))
    chart_yaml = os.path.join(here, os.pardir, "jupyterhub", "Chart.yaml")

    with open(chart_yaml) as f:
        chart = yaml.safe_load(f)
        jupyterhub_version = chart["appVersion"]

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


def test_api_create_and_get_user(api_request, jupyter_user):
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


def test_api_list_users(api_request, jupyter_user):
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


def test_api_proxy_connectivity(api_request, request_data):
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


def test_extra_files(extra_files_test_command):
    """
    Tests the hub.extraFiles configuration. It should have mounted files to the
    hub pod's container with specific file system permissions.
    """
    c = subprocess.run(
        [
            "kubectl",
            "exec",
            "deploy/hub",
            "--",
            "sh",
            "-c",
            extra_files_test_command,
        ]
    )
    assert (
        c.returncode == 0
    ), f"The hub.extraFiles configuration doesn't seem to have been honored!"


def test_load_etc_jupyterhub_d():
    """
    Tests that the extra jupyterhub config file put into
    /usr/local/etc/jupyterhub/jupyterhub_config.d by the hub.extraFiles
    configuration was loaded.
    """
    c = subprocess.run(
        [
            "kubectl",
            "exec",
            "deploy/hub",
            "--",
            "sh",
            "-c",
            "cat /tmp/created-by-extra-files-config.txt | grep -- 'hello world' || exit 1",
        ]
    )
    assert (
        c.returncode == 0
    ), f"The hub.extraFiles configuration should have mounted a config file to /usr/local/etc/jupyterhub/jupyterhub_config.d which should have been loaded to write a dummy file for us!"


def test_load_existing_secret():
    """
    Tests that use of hub.existingSecret works as intended, which mean the
    JupyterHub helm chart should make use of the combined values from a self
    managed k8s Secret and a chart managed k8s Secret. The one exception to this
    rule is CONFIGPROXY_AUTH_TOKEN which is always set using the chart managed
    k8s Secret.

    Required for this test to not error or be skipped:

        1. The chart is configured with a hub.extraConfig entry emitting logs
           that this test looks for in the hub logs. Test error otherwise.
        2. The chart is configured with hub.existingSecret. Skip otherwise.

    For this test to work, we rely on:

        - .github/workflows/test-chart.yaml to pass matrix.local-chart-extra-args
          to the helm install command, and for it to set
          matrix.create-k8s-test-resources on the same GitHub workflow job.
        - ci/test-hub-existing-secret.yaml to define a k8s Secret to create.
        - dev-config.yaml to set hub.services.test-hub-existing-secret.apiToken,
          and for it to set hub.extraConfig to log values on jupyterhub startup.
    """
    c = subprocess.run(
        [
            "kubectl",
            "logs",
            "deploy/hub",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    hub_logs = c.stdout

    if c.returncode != 0:
        print(f"Return code: {c.returncode}")
        print("---")
        print(hub_logs)
        raise AssertionError("Logs from deploy/hub not accessible!")

    # error on missing hub.extraConfig entry
    assert (
        "test_hub_existing_secret" in hub_logs
    ), "Expected specific logs to be emitted as planned from dev-config.yaml!"

    # skip on missing hub.existingSecret or the referenced secret isn't available
    if "hub.existingSecret=None" in hub_logs:
        pytest.skip("hub.existingSecret is None")
    else:
        k8s_secret_exist = False
        match = re.compile(r".*hub.existingSecret=(?P<ref>[\S]*).*", re.DOTALL).match(
            hub_logs
        )
        if match:
            k8s_secret = match.group("ref")
            assert k8s_secret, "This should never be found "
            c = subprocess.run(["kubectl", "get", "secret", k8s_secret])
            if c.returncode != 0:
                pytest.skip(f"k8s Secret '{k8s_secret}' not found")

    # NOTE:  ffff9999 are values from ci/test-hub-existing-secret.yaml that
    #        hub.existingSecret will reference, while aaaa1111-dddd4444 come from
    #        the chart managed k8s Secret.
    #
    # FIXME: It would be good to test use against custom databases, then we
    #        would also test hub.db.password here and that the environment
    #        variables MYSQL_PWD and PGPASSWORD would be setup correctly. But,
    #        configuring that would make the hub fail to startup without an
    #        actual database.
    assert "hub.services.test-hub-existing-secret.apiToken=ffff9999" in hub_logs
    assert "CONFIGPROXY_AUTH_TOKEN=aaaa1111" in hub_logs
    assert "JupyterHub.cookie_secret=ffff9999" in hub_logs
    assert "CryptKeeper.keys=ffff9999" in hub_logs
    assert "singleuser.extraLabels.test-chart-managed-secret=ok" in hub_logs
    assert "singleuser.extraLabels.test-self-managed-secret=ok" in hub_logs
