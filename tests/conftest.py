import os
import requests
import pytest
import yaml

@pytest.fixture(scope='function')
def delete_user(request_data):
    yield
    r = requests.delete(request_data['hub_url'] + f"/users/{request_data['username']}", headers=request_data['headers'])
    r.raise_for_status()
    print(r.status_code)

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
