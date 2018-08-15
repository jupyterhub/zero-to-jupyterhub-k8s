import os
import requests
import pytest
import time

# Makes heavy use of JupyterHub's API:
# http://petstore.swagger.io/?url=https://raw.githubusercontent.com/jupyterhub/jupyterhub/master/docs/rest-api.yml

def test_api(request_data):
    print("asking for the hub's version")
    r = requests.get(request_data['hub_url'])
    r.raise_for_status()
    print(r.json())
    return r.json()

def test_api_info(request_data):
    print("asking for the hub information")
    r = requests.get(request_data['hub_url'] + '/info', headers=request_data['headers'])
    r.raise_for_status()
    print(r.json())
    return r.json()

def test_api_create_user(request_data):
    print("creating the testuser")
    r = requests.post(request_data['hub_url'] + f"/users/{request_data['username']}", headers=request_data['headers'])
    json = r.json()
    print(json)
    if 'message' in json and json['message'] == 'User testuser already exists':
        print("the testuser already exists, thats okay...")
        test_delete_user(request_data)
        print("creating the testuser")
        r = requests.post(request_data['hub_url'] + f"/users/{request_data['username']}", headers=request_data['headers'])
        print(r.json())

    r.raise_for_status()

def test_api_list_users(request_data):
    print("asking for information")
    r = requests.get(request_data['hub_url'] + '/users', headers=request_data['headers'])
    if r.status_code == 201:
        print(r.json())
    elif r.status_code == 404:
        print("no users found")

def test_api_request_user_spawn(request_data):
    print("asking kubespawner to spawn testusers singleuser-server pod")
    r = requests.post(request_data['hub_url'] + f"/users/{request_data['username']}/server", headers=request_data['headers'])
    print(r.status_code)
    r.raise_for_status()

def test_api_wait_for_user_to_spawn(request_data):
    while True:
        # FIXME: This can fail with 503! Make it robuster than this!
        r = requests.get(request_data['hub_url'] + f"/users/{request_data['username']}", headers=request_data['headers'])
        r.raise_for_status()
        user_model = r.json()
        print(user_model)

        # will be pending while starting,
        # server will be set when ready
        if '' not in user_model['servers']:
            # spawn failed!
            raise RuntimeError("Server never started!")
            
        server_model = user_model['servers']['']
        if server_model['ready']:
            break
        
        print(f"pending {server_model['pending']}'s singleuser-server startup'")
        time.sleep(1)

    print(f"Server running at {server_model['url']}")
    r = requests.get(request_data['hub_url'].partition('/hub/api')[0] + server_model['url'] + "api")
    print(r.status_code)
    r.raise_for_status()

def test_delete_user(request_data):
    # FIXME: This is taking too long in general, 50 seconds for example... Can't
    # we lower the grace period or similar? That may require a kubespawner
    # setting btw, or custom configuration.

    print("deleting the testuser")
    while True:
        r = requests.delete(request_data['hub_url'] + f"/users/{request_data['username']}", headers=request_data['headers'])
        print(r.status_code)
        if r.status_code == 400 and r.json()['message'].find('in the process of stopping'):
            print("the user is in the process of stopping")
        elif r.status_code == 404:
            print("the user to delete was not found")
            break
        elif r.status_code == 204:
            print("the user was deleted and server fully terminated!")
            break
        time.sleep(1)
