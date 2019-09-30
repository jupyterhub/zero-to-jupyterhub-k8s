# What is this folder about?

We use CircleCI to build documentation previews for PRs, as configured through
[.circleci/config.yml], this allows us to easily preview documentation changes
in a PR in its final form before the PR is merged.

When a PR is merged, the configuration in [readthedocs.yml](readthedocs.yml) will help ReadTheDocs
build the docs and publish to https://z2jh.jupyter.org.
