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

c.BuilderHub.debug = True

c.BuilderHub.docker_image_prefix = '%s/%s/' % (get_config('builder.registry.host'), get_config('builder.registry.prefix'))

c.BuilderHub.docker_push_secret = get_config('builder.push-secret')
c.BuilderHub.build_namespace = os.environ['BUILD_NAMESPACE']

c.BuilderHub.builder_image_spec = get_config('builder.builder-image')
c.BuilderHub.hub_redirect_url_template = get_config('hub.public-url') + '/hub/tmplogin?image={image}&default_url={default_url}'
