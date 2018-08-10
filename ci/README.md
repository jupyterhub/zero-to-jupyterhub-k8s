# CI for Zero-To-JupyterHub-K8s

## 

## Vagrant
Vagrant could help you simulate the CI with Travis which is done when making a pull request to the jupyterhub/zero-to-jupyterhub-k8s repository.

```bash
# To be run in a terminal from the ci directory
vagrant up
vagrant ssh

cd /zero-to-jupyterhub-k8s
# Now run the steps under install and script in .travis.yml
# . ci/0-setup-env-vars.sh
# and more...
exit

vagrant destroy
```