#!/usr/bin/env python
"""script to monitor and cull idle single-user servers

Caveats:

last_activity is not updated with high frequency,
so cull timeout should be greater than the sum of:

- single-user websocket ping interval (default: 30s)
- JupyterHub.last_activity_interval (default: 5 minutes)

Generate an API token and store it in `JPY_API_TOKEN`:

    export JPY_API_TOKEN=`jupyterhub token`
    python cull_idle_servers.py [--timeout=900] [--url=http://127.0.0.1:8081/hub]
"""

import datetime
import json
import os

from dateutil.parser import parse as parse_date

from tornado.gen import coroutine
from tornado.log import app_log
from tornado.httpclient import AsyncHTTPClient, HTTPClient, HTTPRequest
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.options import define, options, parse_command_line

@coroutine
def cull_idle(url, api_token, timeout, async):
    """cull idle single-user servers"""
    auth_header = {
            'Authorization': 'token %s' % api_token
        }
    req = HTTPRequest(url=url + '/api/users',
        headers=auth_header,
    )
    now = datetime.datetime.utcnow()
    cull_limit = now - datetime.timedelta(seconds=timeout)
    client = AsyncHTTPClient()
    resp = yield client.fetch(req)
    users = json.loads(resp.body.decode('utf8', 'replace'))
    blocking_client = HTTPClient()
    futures = []
    req_type = {True:"non-blocking", False:"blocking"}[async]
    for user in users:
        last_activity = parse_date(user['last_activity'])
        if user['server'] and last_activity < cull_limit:
            name = user['name']
            app_log.info("Request %s cull for %s (inactive since %s)", req_type, name, last_activity)
            req = HTTPRequest(url=url + '/api/users/%s/server' % name,
                method='DELETE',
                headers=auth_header,
            )
            if async:
                futures.append((name, client.fetch(req)))
            else:
                try:
                    resp = blocking_client.fetch(req)
                except Exception as e:
                    app_log.info("Could not cull %s", name)
                    app_log.info(str(e))
                else:
                    app_log.info("Culled %s", name)
        else:
            app_log.debug("Not culling %s (active since %s)", user['name'], last_activity)

    for (name, f) in futures:
        try:
            yield f
        except Exception as e:
            app_log.info("Could not cull %s", name)
            app_log.info(str(e))
        else:
            app_log.info("Culled %s", name)

if __name__ == '__main__':
    define('url', default='http://127.0.0.1:8081/hub', help="The JupyterHub API URL")
    define('timeout', default=600, help="The idle timeout (in seconds)")
    define('cull_every', default=0, help="The interval (in seconds) for checking for idle servers to cull")
    define('async', default=False, help="Cull in parallel")

    parse_command_line()
    if not options.cull_every:
        options.cull_every = options.timeout // 2

    api_token = os.environ['JPY_API_TOKEN']

    loop = IOLoop.current()
    cull = lambda : cull_idle(options.url, api_token, options.timeout, options.async)
    # run once before scheduling periodic call
    loop.run_sync(cull)
    # schedule periodic cull
    pc = PeriodicCallback(cull, 1e3 * options.cull_every)
    pc.start()
    try:
        loop.start()
    except KeyboardInterrupt:
        pass

