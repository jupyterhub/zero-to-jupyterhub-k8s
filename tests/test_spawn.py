import os
import requests
import pytest
import time

# Makes heavy use of JupyterHub's API:
# http://petstore.swagger.io/?url=https://raw.githubusercontent.com/jupyterhub/jupyterhub/master/docs/rest-api.yml

API_TIMEOUT = 300


def test_api(api_request):
    print("asking for the hub's version")
    r = api_request.get('')
    assert r.status_code == 200
    assert r.json() == {"version": "0.9.4"}


def test_api_info(api_request):
    print("asking for the hub information")
    r = api_request.get('/info')
    assert r.status_code == 200
    result = r.json()
    assert result['spawner']['class'] == 'kubespawner.spawner.KubeSpawner'


def test_api_create_user(api_request, jupyter_user):
    print("creating the testuser")
    # Already created by the jupyter_user fixture
    r = api_request.get('/users/' + jupyter_user)
    assert r.status_code == 200
    assert r.json()['name'] == jupyter_user


def test_api_list_users(api_request, jupyter_user):
    print("asking for information")
    r = api_request.get('/users')
    assert r.status_code == 200
    assert any(u['name'] == jupyter_user for u in r.json())


def test_api_request_user_spawn(api_request, jupyter_user, request_data):
    print("asking kubespawner to spawn testusers singleuser-server pod")
    r = api_request.post('/users/' + jupyter_user + '/server')
    assert r.status_code in (201, 202)
    try:
        server_model = _wait_for_user_to_spawn(api_request, jupyter_user, API_TIMEOUT)
        assert server_model
        r = requests.get(request_data['hub_url'].partition('/hub/api')[0] + server_model['url'] + "api")
        assert r.status_code == 200
        assert 'version' in r.json()
    finally:
        _delete_server(api_request, jupyter_user, API_TIMEOUT)


@pytest.mark.skipif(os.getenv('DISABLE_TEST_NETPOL') == '1',
                    reason="DISABLE_TEST_NETPOL set")
def test_singleuser_netpol(api_request, jupyter_user, request_data):
    print("asking kubespawner to spawn a singleuser-server pod to test network policies")
    r = api_request.post('/users/' + jupyter_user + '/server')
    assert r.status_code in (201, 202)
    try:
        server_model = _wait_for_user_to_spawn(api_request, jupyter_user, API_TIMEOUT)
        assert server_model
        print(server_model)
        pod_name = server_model['state']['pod_name']

        allowed_url = 'http://www.ebi.ac.uk'
        blocked_url = 'http://www.bbc.co.uk'

        c = subprocess.run([
            'kubectl', '--namespace=jupyterhub-test', 'exec', pod_name, '--',
            'wget', '-q', '-t1', '-T5', allowed_url])
        assert c.returncode == 0, "Unable to get allowed domain"

        c = subprocess.run([
            'kubectl', '--namespace=jupyterhub-test', 'exec', pod_name, '--',
            'wget', '-q', '-t1', '-T5', blocked_url])
        assert c.returncode > 0, "Blocked domain was allowed"

    finally:
        _delete_server(api_request, jupyter_user, API_TIMEOUT)


def _wait_for_user_to_spawn(api_request, jupyter_user, timeout):
    t = 0
    while t < timeout:
        # FIXME: This can fail with 503! Make it robuster than this!
        r = api_request.get('/users/' + jupyter_user)
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


def _delete_server(api_request, jupyter_user, timeout):
    r = api_request.delete('/users/' + jupyter_user + '/server')
    assert r.status_code in (202, 204)
    t = 0
    while t < timeout:
        r = api_request.get('/users/' + jupyter_user)
        r.raise_for_status()
        user_model = r.json()
        if '' not in user_model['servers']:
            return True
        time.sleep(1)
    return False
