import requests
import time


def test_hub_can_talk_to_proxy(api_request, request_data):
    endtime = time.time() + request_data['test_timeout']
    while time.time() < endtime:
        try:
            r = api_request.get('/proxy')
            if r.status_code == 200:
                break
            print(r.json())
        except requests.RequestException as e:
            print(e)
        time.sleep(1)
    assert r.status_code == 200, 'Failed to get /proxy'
