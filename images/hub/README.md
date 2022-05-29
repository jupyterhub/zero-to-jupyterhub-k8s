# About this folder

The Dockerfile in this folder is built by
[chartpress](https://github.com/jupyterhub/chartpress#readme), using the
requirements.txt file. The requirements.txt file is updated based on the
requirements.in file using [`pip-compile`](https://pip-tools.readthedocs.io).

## How to update requirements.txt

Because `pip-compile` resolves `requirements.txt` with the current Python for
the current platform, it should be run on the same Python version and platform
as our Dockerfile.

Note that as of 2022-05-29, `pip-compile` has issues with `pycurl`, but we
workaround them by by omitting the `-slim` part from the image in the command
below.

```shell
# update requirements.txt based on requirements.in
docker run --rm \
    --env=CUSTOM_COMPILE_COMMAND="see README.md" \
    --volume=$PWD:/io \
    --workdir=/io \
    --user=root \
    python:3.9-bullseye \
    sh -c 'pip install pip-tools==6.* && pip-compile --upgrade'
```
