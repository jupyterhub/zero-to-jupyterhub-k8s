import os
import requests
import pytest

@pytest.fixture(scope='function')
def delete_user(request_data):
    yield
    r = requests.delete(request_data['hub_url'] + f"/users/{request_data['username']}", headers=request_data['headers'])
    r.raise_for_status()
    print(r.status_code)
    
@pytest.fixture(scope='function')
def request_data():
    token = '0cc05feaefeeb29179e924ffc6d3886ffacf0d1a28ab225f5c210436ffc5cfd5'
    return {
        'token': token,
        'hub_url': os.environ['HUB_API_URL'],
        'headers': {
            'Authorization': f'token {token}'
        },
        'username': 'testuser',
    }
