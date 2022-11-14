import subprocess
import time

import pytest
import requests


def test_spawn_basic(
    api_request,
    jupyter_user,
    request_data,
    pebble_acme_ca_cert,
    extra_files_test_command,
):
    """
    Tests the hub api's /users/:user/server POST endpoint. A user pod should be
    created with environment variables defined in singleuser.extraEnv,
    singleuser.extraFiles should be mounted, etc.
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
        c = subprocess.run(
            [
                "kubectl",
                "exec",
                pod_name,
                "--",
                "sh",
                "-c",
                "if [ -z $TEST_ENV_FIELDREF_TO_NAMESPACE ]; then exit 1; fi",
            ]
        )
        assert (
            c.returncode == 0
        ), "singleuser.extraEnv didn't lead to a mounted environment variable!"

        # check user pod's extra files
        c = subprocess.run(
            [
                "kubectl",
                "exec",
                pod_name,
                "--",
                "sh",
                "-c",
                extra_files_test_command,
            ]
        )
        assert (
            c.returncode == 0
        ), "The singleuser.extraFiles configuration doesn't seem to have been honored!"
    finally:
        _delete_server(api_request, jupyter_user, request_data["test_timeout"])


@pytest.mark.netpol
def test_spawn_netpol(api_request, jupyter_user, request_data):
    """
    Tests a spawned user pods ability to communicate with allowed and blocked
    internet locations.
    """

    print(
        "asking kubespawner to spawn a server for a test user to test network policies"
    )
    r = api_request.post("/users/" + jupyter_user + "/server")
    assert r.status_code in (201, 202)
    try:
        # check successfull spawn
        server_model = _wait_for_user_to_spawn(
            api_request, jupyter_user, request_data["test_timeout"]
        )
        assert server_model
        pod_name = server_model["state"]["pod_name"]

        c = subprocess.run(
            [
                "kubectl",
                "exec",
                pod_name,
                "--",
                "nslookup",
                "hub",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if c.returncode != 0:
            print(f"Return code: {c.returncode}")
            print("---")
            print(c.stdout)
            raise AssertionError(
                "DNS issue: failed to resolve 'hub' from a singleuser-server"
            )

        c = subprocess.run(
            [
                "kubectl",
                "exec",
                pod_name,
                "--",
                "nslookup",
                "jupyter.org",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if c.returncode != 0:
            print(f"Return code: {c.returncode}")
            print("---")
            print(c.stdout)
            raise AssertionError(
                "DNS issue: failed to resolve 'jupyter.org' from a singleuser-server"
            )

        # The IPs we test against are differentiated by the NetworkPolicy shaped
        # by the dev-config.yaml's singleuser.networkPolicy.egress
        # configuration. If these IPs change, you can use `nslookup jupyter.org`
        # to get new IPs but beware that this response may look different over
        # time at least on our GitHub Action runners. Note that we have
        # explicitly pinned these IPs and explicitly pass the Host header in the
        # web-request in order to avoid test failures following additional IPs
        # are added.
        allowed_jupyter_org_ip = "104.21.25.233"
        blocked_jupyter_org_ip = "172.67.134.225"

        cmd_kubectl_exec = ["kubectl", "exec", pod_name, "--"]
        cmd_python_exec = ["python", "-c"]
        cmd_python_code = "import socket; s = socket.socket(); s.settimeout(3); s.connect(('{ip}', 80)); s.close();"
        cmd_check_allowed_ip = (
            cmd_kubectl_exec
            + cmd_python_exec
            + [cmd_python_code.format(ip=allowed_jupyter_org_ip)]
        )
        cmd_check_blocked_ip = (
            cmd_kubectl_exec
            + cmd_python_exec
            + [cmd_python_code.format(ip=blocked_jupyter_org_ip)]
        )

        # check allowed jupyter.org ip connectivity
        c = subprocess.run(
            cmd_check_allowed_ip,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if c.returncode != 0:
            print(f"Return code: {c.returncode}")
            print("---")
            print(c.stdout)
            raise AssertionError(
                f"Network issue: access to '{allowed_jupyter_org_ip}' was supposed to be allowed"
            )

        # check blocked jupyter.org ip connectivity
        c = subprocess.run(
            cmd_check_blocked_ip,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if c.returncode == 0:
            print(f"Return code: {c.returncode}")
            print("---")
            print(c.stdout)
            raise AssertionError(
                f"Network issue: access to '{blocked_jupyter_org_ip}' was supposed to be denied"
            )

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

        # Note that JupyterHub has a concept of named servers, so the default
        # server is named "", a blank string.
        if "" in user_model["servers"]:
            server_model = user_model["servers"][""]
            if server_model["ready"]:
                return server_model
        else:
            print("Awaiting server info to be part of user_model...")

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
