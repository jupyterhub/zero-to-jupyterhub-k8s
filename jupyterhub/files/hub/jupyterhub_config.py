import sys

from tornado.httpclient import AsyncHTTPClient
from jupyterhub.utils import url_path_join

# Make sure that modules placed in the same directory as the jupyterhub config are added to the pythonpath
configuration_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, configuration_directory)

from z2jh import get_config, set_config_if_not_none, camelCaseify
import helpers

# Configure JupyterHub to use the curl backend for making HTTP requests,
# rather than the pure-python implementations. The default one starts
# being too slow to make a large number of requests to the proxy API
# at the rate required.
AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

# Connect to the API running under a proxy
c.ConfigurableHTTPProxy.api_url = 'http://{}:{}'.format(os.environ['PROXY_API_SERVICE_HOST'], int(os.environ['PROXY_API_SERVICE_PORT']))
c.ConfigurableHTTPProxy.should_start = False

# basic configuration of JupyterHub
c.JupyterHub = helpers.configure_jupuyterhub(c.JupyterHub)

# configures culling and optional services within the hub
c.JupyterHub.services = helpers.jupuyterhub_services(jupyterhub.get('base_url', '/'))

# configures c.KubeSpawner and c.Spawner, responsible for spawning user containers
c.KubeSpawner = helpers.configure_kube_spawner(c.KubeSpawner)
c.Spawner = helpers.configure_spawner(c.Spawner)

# configure Authentication
c = helpers.configure_authentication(c)

set_config_if_not_none(c.OAuthenticator, 'scope', 'auth.scopes')

set_config_if_not_none(c.Authenticator, 'enable_auth_state', 'auth.state.enabled')

# Enable admins to access user servers
set_config_if_not_none(c.JupyterHub, 'admin_access', 'auth.admin.access')
set_config_if_not_none(c.Authenticator, 'admin_users', 'auth.admin.users')
set_config_if_not_none(c.Authenticator, 'whitelist', 'auth.whitelist.users')

# Configure debug
if get_config('debug.enabled', False):
    c.JupyterHub.log_level = 'DEBUG'
    c.Spawner.debug = True

# execute extra configurations
extra_config = helpers.extra_configurations()

for key, config_py in sorted(extra_config.items()):
    print("Loading extra config: %s" % key)
    exec(config_py)
