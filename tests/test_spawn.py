import os
import requests
import pytest
import time

# Makes heavy use of JupyterHub's API:
# http://petstore.swagger.io/?url=https://raw.githubusercontent.com/jupyterhub/jupyterhub/master/docs/rest-api.yml

API_TIMEOUT = 300

def test_api(request_data):
    print("asking for the hub's version")
    r = requests.get(request_data['hub_url'])
    assert r.status_code == 200
    assert r.json() == {"version": "0.9.4"}

def test_api_info(request_data):
    print("asking for the hub information")
    r = requests.get(request_data['hub_url'] + '/info', headers=request_data['headers'])
    assert r.status_code == 200
    result = r.json()
    assert result['spawner']['class'] == 'kubespawner.spawner.KubeSpawner'


def test_api_create_user(jupyter_user, request_data):
    print("creating the testuser")
    # Already created by the jupyter_user fixture
    r = requests.get(request_data['hub_url'] + f"/users/{jupyter_user}", headers=request_data['headers'])
    assert r.status_code == 200
    assert r.json()['name'] == jupyter_user


def test_api_list_users(jupyter_user, request_data):
    print("asking for information")
    r = requests.get(request_data['hub_url'] + '/users', headers=request_data['headers'])
    assert r.status_code == 200
    assert any(u['name'] == jupyter_user for u in r.json())


def test_api_request_user_spawn(jupyter_user, request_data):
    print("asking kubespawner to spawn testusers singleuser-server pod")
    r = requests.post(request_data['hub_url'] + f"/users/{jupyter_user}/server", headers=request_data['headers'])
    assert r.status_code in (201, 202)
    try:
        server_model = _wait_for_user_to_spawn(jupyter_user, request_data, API_TIMEOUT)
        assert server_model
        r = requests.get(request_data['hub_url'].partition('/hub/api')[0] + server_model['url'] + "api")
        assert r.status_code == 200
        assert 'version' in r.json()
    finally:
        _delete_server(jupyter_user, request_data, API_TIMEOUT)


def _wait_for_user_to_spawn(jupyter_user, request_data, timeout):
    t = 0
    while t < timeout:
        # FIXME: This can fail with 503! Make it robuster than this!
        r = requests.get(request_data['hub_url'] + f"/users/{jupyter_user}", headers=request_data['headers'])
        r.raise_for_status()
        user_model = r.json()

        # will be pending while starting,
        # server will be set when ready
        if '' not in user_model['servers']:
            # spawn failed!
            raise RuntimeError("Server never started!")

        server_model = user_model['servers']['']
        if server_model['ready']:
            return server_model

        time.sleep(1)
    return False


def _delete_server(jupyter_user, request_data, timeout):
    r = requests.delete(request_data['hub_url'] + f"/users/{jupyter_user}/server", headers=request_data['headers'])
    assert r.status_code in (202, 204)
    t = 0
    while t < timeout:
        r = requests.get(request_data['hub_url'] + f"/users/{jupyter_user}", headers=request_data['headers'])
        r.raise_for_status()
        user_model = r.json()
        if '' not in user_model['servers']:
            return True
        time.sleep(1)
    return False
