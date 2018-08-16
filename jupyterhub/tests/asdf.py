import os
import requests

token = 
hub_url = os.environ['HUB_API_URL']

# create user
headers = {'Authorization': f"token {token}"}

username = 'testuser'
r = requests.post(hub_url + f'/hub/api/users/{username}', headers=headers)
r.raise_for_status()
r.json()

# Start the server

r = requests.post(hub_url + f'/hub/api/users/{username}/server', headers=headers)
r.raise_for_status()
r.status_code

#
import time

while True:
    r = requests.get(hub_url + f'/hub/api/users/{username}', headers=headers)
    r.raise_for_status()
    user_model = r.json()
    user_model
    # will be pending while starting,
    # server will be set when ready
    if '' not in user_model['servers']:
        # spawn failed!
        raise RuntimeError("Server never started!")
        print(user_model)
        
    server_model = user_model['servers']['']
    if server_model['ready']:
        break
    print(f"pending {server_model['pending']}")
    time.sleep(1)

print(f"Server running at {server_model['url']}")

#
# 
r = requests.get(hub_url + server_model['url'] + "api")
r.raise_for_status()
r.json()

#Stop the server

r = requests.delete(hub_url + f'/hub/api/users/{username}/server', headers=headers)
r.raise_for_status()