import copy

from jupyterhub.utils import maybe_future
from singleuser_exposure_common import validate_exposure_config
from singleuser_exposure_k8s import apply_exposure, cleanup_exposure


def chain_hooks(existing_hook, new_hook):
    if existing_hook is None:
        return new_hook

    async def chained_hook(*args, **kwargs):
        await maybe_future(existing_hook(*args, **kwargs))
        return await maybe_future(new_hook(*args, **kwargs))

    return chained_hook


def configure_singleuser_exposure(c, get_config):
    exposure_config = copy.deepcopy(get_config("singleuser.exposure", {}))
    if not exposure_config.get("enabled"):
        return

    validate_exposure_config(exposure_config)

    c.KubeSpawner.services_enabled = True

    async def after_pod_created(spawner, pod):
        await apply_exposure(spawner, exposure_config, pod)

    async def post_stop(spawner):
        await cleanup_exposure(spawner, exposure_config)

    existing_after_hook = c.KubeSpawner.get("after_pod_created_hook")
    existing_post_stop_hook = c.KubeSpawner.get("post_stop_hook")

    c.KubeSpawner.after_pod_created_hook = chain_hooks(
        existing_after_hook, after_pod_created
    )
    c.KubeSpawner.post_stop_hook = chain_hooks(existing_post_stop_hook, post_stop)
