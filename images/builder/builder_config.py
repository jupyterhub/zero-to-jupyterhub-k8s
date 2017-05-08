import os
import yaml

def get_config(key, default=None):
    """
    Find a config item of a given name & return it

    Parses everything as YAML, so lists and dicts are available too
    """
    path = os.path.join('/etc/builderhub/config', key)
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
            print(key, data)
            return data
    except FileNotFoundError:
        return default

c.BuilderApp.docker_image_prefix = 'gcr.io/data-8/'

c.BuilderApp.docker_push_secret = get_config('builder.push-secret')
c.BuilderApp.build_namespace = os.environ['BUILD_NAMESPACE']

c.BuilderApp.debug = True

c.BuilderApp.hub_redirect_url_template = get_config('hub.public-url') + '/hub/tmplogin?image={image}'
