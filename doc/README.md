# About the documentation

This documentation is automatically built on each commit [as configured on
ReadTheDocs](https://readthedocs.org/projects/zero-to-jupyterhub/), and made
available on [z2jh.jupyter.org](https://z2jh.jupyter.org/).

## Intro to the documentation code base

This is not documented properly yet. What should go in this section could be
what the makefile does, what sphinx is/does, environment.yml vs
doc-requirements.txt, make.bat vs Makefile, source/conf.py, use of .rst and .md,
how to use rst in md, what the _templates folder contains and how those are
used.

Additionally, some foundational RST techniques in play could be useful, but
perhaps documented in the team-compass and referenced here.

## Local documentation development

To locally develop the documentation, do something like this and visit
http://localhost:8888. Note that you need to host the content with a webserver
to avoid links failing, and that you need to rebuild with `make html` to update
the documentation. The live-server will ensure to update its content based on
changes though.

```shell
cd doc
pip install live-server -r doc-requirements.txt
make html
live-server build/html
```
