import os
import requests
import pytest
import uuid
import yaml


@pytest.fixture(scope='function')
def request_data():
    basedir = os.path.dirname(os.path.dirname(__file__))
    with open(os.path.join(basedir, 'minikube-config.yaml')) as f:
        y = yaml.load(f)
    token = y['hub']['services']['test']['apiToken']
    return {
        'token': token,
        'hub_url': os.getenv('HUB_API_URL', 'http://localhost:31212/hub/api'),
        'headers': {
            'Authorization': f'token {token}'
        },
        'username': 'testuser',
    }


@pytest.fixture(scope='function')
def jupyter_user(request_data):
    """
    A temporary unique JupyterHub user
    """
    username = 'testuser-' + str(uuid.uuid4())
    r = requests.post(request_data['hub_url'] + '/users/' + username, headers=request_data['headers'])
    assert r.status_code == 201
    yield username
    r = requests.delete(request_data['hub_url'] + '/users/' + username, headers=request_data['headers'])
    assert r.status_code == 204
