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


class JupyterRequest(object):
    def __init__(self, request_data):
        self.request_data = request_data

    def delete(self, api, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = self.request_data['headers']
        return requests.delete(self.request_data['hub_url'] + api, **kwargs)

    def get(self, api, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = self.request_data['headers']
        return requests.get(self.request_data['hub_url'] + api, **kwargs)

    def post(self, api, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = self.request_data['headers']
        return requests.post(self.request_data['hub_url'] + api, **kwargs)

    def put(self, api, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = self.request_data['headers']
        return requests.put(self.request_data['hub_url'] + api, **kwargs)


@pytest.fixture(scope='function')
def api_request(request_data):
    return JupyterRequest(request_data)


@pytest.fixture(scope='function')
def jupyter_user(api_request):
    """
    A temporary unique JupyterHub user
    """
    username = 'testuser-' + str(uuid.uuid4())
    r = api_request.post('/users/' + username)
    assert r.status_code == 201
    yield username
    r = api_request.delete('/users/' + username)
    assert r.status_code == 204
