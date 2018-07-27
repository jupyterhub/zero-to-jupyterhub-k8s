"""
Utility methods for use in jupyterhub_config.py and dynamic subconfigs.

Methods here can be imported by extraConfig in values.yaml
"""
import os
import sys
import yaml

def get_config(key, default=None):
    """
    Find a config item of a given name & return it

    Parses everything as YAML, so lists and dicts are available too
    """
    path = os.path.join('/etc/jupyterhub/config', key)
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
            return data
    except FileNotFoundError:
        return default

def get_secret(key, default=None):
    """Get a secret from /etc/jupyterhub/secret"""
    path = os.path.join('/etc/jupyterhub/secret', key)
    try:
        with open(path) as f:
            return f.read().strip()
    except FileNotFoundError:
        return default

def set_config_if_not_none(cparent, name, key):
    """
    Find a config item of a given name, set the corresponding Jupyter
    configuration item if not None
    """
    data = get_config(key)
    if data is not None:
        setattr(cparent, name, data)
