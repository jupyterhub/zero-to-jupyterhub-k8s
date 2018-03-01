# Contributing

Welcome! As a [Jupyter](https://jupyter.org) project, we follow the [Jupyter contributor guide](https://jupyter.readthedocs.io/en/latest/contributor/content-contributor.html).

## Local development

We recommend using [minikube](https://github.com/kubernetes/minikube) for local
development.

1. [Download & install minikube](https://github.com/kubernetes/minikube#installation)

   For MacOS, you may find installing from https://github.com/kubernetes/minikube/releases
   may be more stable than using Homebrew.

2. Start minikube
   ```
   minikube start
   ```
3. Use the docker daemon inside minikube for building:
   ```
   eval $(minikube docker-env)
   ```
4. Clone the zero-to-jupyterhub repo:
   ```
   git clone git@github.com:jupyterhub/zero-to-jupyterhub-k8s.git
   cd zero-to-jupyterhub-k8s
   ```
5. Create a virtualenv & install the libraries required for builds to happen:
   ```bash
   python3 -m venv .
   pip install -r dev-requirements.txt
   ```
 6. Now run `chartpress` to build the requisite docker images inside minikube:
    ```bash
    chartpress
    ```

    This will build the docker images inside minikube & modify
    `jupyterhub/values.yaml` with the appropriate values to make the chart
    installable!

7. Install / Upgrade JupyterHub Chart!
   ```bash
   helm upgrade --wait --install --namespace=hub hub jupyterhub/ -f minikube-config.yaml
   ```

   You can easily change the options in `minikube-config.yaml` file to test what
   you want, or create another `config.yaml` file & pass that as an additional
   `-f config.yaml` file to the `helm upgrade` command.

8. Open the URL for your instance of JupyterHub!

   ```bash
   minikube service --namespace=hub proxy-public
   ```

8. Make the changes you want. You need to re-run step 6 if you changed anything
   under `images`, but only step 7 if you changed things only under `jupyterhub`


## Releasing a new version of the helm chart

The following steps can be followed to release a new version of the Helm Chart.
Presently, we expect a release approximately every 5-7 weeks.


### Create an issue for the new release

Use this issue to coordinate efforts and keep track of progress. You can
copy / paste the raw Markdown from the following list, which will be covered
in more detail below.

```
Title: Release {{release-name}}
Content:

This issue will be used to coordinate the next release of the helm
chart, {{release-name}}. Instructions for creating the release can be found in
[CONTRIBUTING.md](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/master/CONTRIBUTING.md#releasing-a-new-version-of-the-helm-chart).
Below is the checklist for this release.

- [ ] Code, tests, and documentation to support a release are stable.
- [ ] Make a CHANGELOG
- [ ] Generate and add the list of contributors
- [ ] Build and push a new Docker image to DockerHub
- [ ] Commit version bump in `Chart.yaml` and `Values.yaml`
- [ ] Update references in documentation to the new version (note: documentation
      should be stable and there should be no anticipated major changes to content).
- [ ] Confirm that a new deployment using the updated instructions works
- [ ] Create and push a new tag for this release
- [ ] Create and publish a new GitHub release
- [ ] Write / publish a blog post based largely off of the CHANGELOG
- [ ] Set ReadTheDocs to begin using `latest` by default
- [ ] Celebrate!
```

As there are often many documentation improvements following the release of
a new version, we set ReadTheDocs to serve `latest/` until the first docs are
written that are next-version-specific. As soon as documentation must be
written for the **next** version of the Helm Chart, you can use the following
checklist:

```
- [ ] Create a new tag for a documentation release (same release name with `-doc` at the end)
- [ ] Publish this tag
- [ ] Set ReadTheDocs to point to the **new tag** by default instead of `latest`
- [ ] Continue making next-version-specific changes to the documentation.
```

**Note**: Switching the documentation to `latest` after a new release is a stop-gap
measure to accomodate the fact that the documentation is still changing relatively
rapidly. Once the documentation as a whole stabilizes (after a few more release
cycles), we plan to begin switching straight from the last version to the new version
of documentation without going through latest.

### Make a CHANGELOG

This needs to be manually created, following the format of
current [CHANGELOG](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/master/CHANGELOG.md). The general structure should be:

* A short description of the general theme / points of interest for
 this release.
* Breaking changes + a link to the [upgrade instructions](https://zero-to-jupyterhub.readthedocs.io/en/v0.5-doc/upgrading.html) in the docs
* A list of features with brief descriptions under each.
* The contributor list mentioned in the section below.

### Add list of contributors

We try to recognize *all* sorts of contributors, rather
than just code committers.

Use the script in `tools/contributors.py` to list all
contributions (anyone who made a commit or a comment)
since the latest release. For each
release, you'll need to find the versions of all repos
involved:

* [z2jh](https://github.com/jupyterhub/zero-to-jupyterhub-k8s)
* [KubeSpawner](https://github.com/jupyterhub/kubespawner)
* [JupyterHub](https://github.com/jupyterhub/jupyterhub)
* [OAuthenticator](https://github.com/jupyterhub/oauthenticator))

Edit `contributors.py` to have the appropriate dates
for each of these versions. Then, run the script and paste
the output into the changelog. For an
example, see [the v0.5 list of contributors](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/v0.5/CHANGELOG.md#contributors).


### Push built images to DockerHub + bump version

The JupyterHub helm chart uses a Docker image that's registered
on DockerHub. When releasing a new version of the helm chart,
you also need to push a new version of this image. To do so,
you must have:

1. Docker running locally
2. An account on DockerHub that you are logged into from
  your local docker installation.
3. Push rights for images under `jupyterhub/` on
  the DockerHub registry.
4. Push rights to the `jupyterhub/helm-chart` repository on GitHub.
5. A local SSH key that will let you push to the `helm-chart` repository
  on GitHub. See [these instructions](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) for information on how to create this.

**Note**: If you don't have a DockerHub account, or don't have push rights to
the DockerHub registry, open an issue and ping one of the core devs.

If you have all of this, you can then:

1. Check out latest master of [z2jh](https://github.com/jupyterhub/zero-to-jupyterhub-k8s)
2. Run `chartpress --tag <VERSION> --push --publish-chart`.
  * For example, to relase `v0.5`, you would run
  `chartpress --tag v0.5 --push --publish-chart`.
  Note the `v` before version.
3. This will also modify the files `Chart.yaml` and `values.yaml`.
  Commit these changes.
4. Look through the [z2jh documentation](https://zero-to-jupyterhub.readthedocs.io) and find any references to
  the Helm Chart version (e.g., look for the flag `--version`, as well
  as for all `helm upgrade` and `helm install` commands).
  Update these references to point to the new version you are releasing.
5. Make a PR to the z2jh repository and notify the team to take a look.

After this PR gets merged:

1. Go to https://zero-to-jupyterhub.readthedocs.io/en/latest and
  deploy a JupyterHub using the instructions (make sure that
  you're reading from `/en/latest`). Make sure your latest
  changes are present, and that the JupyterHub successfully deploys
  and functions properly.

Next, move on to making a GitHub release, described below.

### Tagging and making a GitHub release

Now that our Docker image is pushed and we have updated the documentation
for z2jh, it's time to make a new GitHub release. To do this, you must have:

1. Push rights to the `jupyterhub/zero-to-jupyterhub-k8s` repo

You will need to make a git tag, and then create a GitHub release.

1. Make sure you're on branch `master` with your latest changes from
  the section above pulled.
2. Make a git tag with:
  ```
  git tag -a <VERSION>
  ```

  Where `<VERSION>` should be the new version that you're releasing.
  Note the `v` before the version number.

  Git will ask you to include a message with the tag.
  Paste the entire contents of the CHANGELOG for this particular release.
  An easy way to do this is to paste the contents in a text file, and
  then refer to that text file with the call to commit:
  `git tag -a <VERSION> -F <PATH-TO-FILE.txt>`
3. Push the tags to the `jupyterhub/zero-to-jupyterhub-k8s` repo with
  `git push <REMOTE-NAME> --tags`.
  Note that `<REMOTE-NAME>` is whatever your local git uses to refer
  to the `jupyerhub/` organization's repository (e.g., `official`
  or `upstream`)
3. Make a **GitHub Release**:
  * go to https://github.com/jupyterhub/zero-to-jupyterhub-k8s/releases and click 'Draft new release'.
  * The title should be the new version, followed by the name of the cricketer for the release. Like so:`v0.5: "Hamid Hassan"`.
  * The description should include the entire changelog entry for this release.
  * Make sure the title/description/tag name look correct, and then click
    on `Publish Release`.

You've just made a GitHub release!


### RTD update

Wait a few hours to let the release 'cool' and make sure that links,
webpages, etc have updated. Then, update our documentation settings on
readthedocs to show `latest` by default. This marks the official
'release' of the version!

### Last step - release a blog post and tell the world!

The final step is to release a blog post. This doesn't have to be
done by the person who performed all of the above actions.

To release a blog post for the new version, start a draft on the Jupyter Medium
blog. Copy/paste the section of the CHANGELOG corresponding to the new
release, then make minor modifications to make it more blog-friendly.

Don't forget to tell the JupyterHub community about the new release, and
to encourage people to talk about it on social media!

That's it! Congratulations on making a new release of JupyterHub!

### Extra step - release a documentation release

It is common that documentation changes are made shortly after a new release.
To handle this, we often create a documentation release a few days after a
major release.

To do this, confirm that all changes to the documentation
are merged into master, then create a new tag with the same release name and
`-doc` appended to the end. Create a GitHub release with the new tag and a
description that points to the original release description. Finally, set
our ReadTheDocs settings to point users to the new `-doc` tag by default instead
of `latest`.
