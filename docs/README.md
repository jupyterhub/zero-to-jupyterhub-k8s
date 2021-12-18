# About the documentation

This documentation is automatically built on each commit [as configured on
ReadTheDocs](https://readthedocs.org/projects/zero-to-jupyterhub/) and
in the `readthedocs.yml` file, and made available on
[z2jh.jupyter.org](https://z2jh.jupyter.org/).

## Local documentation development

```shell
cd docs
pip install -r requirements.txt
```

```
# automatic build and livereload enabled webserver
make devenv

# automatic check of links validity
make linkcheck
```
