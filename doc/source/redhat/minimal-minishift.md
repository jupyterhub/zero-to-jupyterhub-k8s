# Minimalist Documentation for minishift on MacOS

## Installing minishift

[Detail from official docs](https://docs.openshift.org/latest/minishift/getting-started/installing.html)

Install a hypervisor, `xhyve`:

```bash
brew install docker-machine-driver-xhyve
sudo chown root:wheel $(brew --prefix)/opt/docker-machine-driver-xhyve/bin/docker-machine-driver-xhyve
sudo chmod u+s $(brew --prefix)/opt/docker-machine-driver-xhyve/bin/docker-machine-driver-xhyve
```

Install minishift stable:

```bash
brew cask install minishift  # use --force if upgrading
```

## Launching minishift

*Command*

```bash
minishift start
```

*Response*

```bash
-- Starting profile 'minishift'
-- Checking if requested OpenShift version 'v3.7.1' is valid ... OK
-- Checking if requested OpenShift version 'v3.7.1' is supported ... OK
-- Checking if requested hypervisor 'xhyve' is supported on this platform ... OK
...
OpenShift server started.

The server is accessible via web console at:
    https://192.168.64.2:8443

You are logged in as:
    User:     developer
    Password: <any value>

To login as administrator:
    oc login -u system:admin

-- Exporting of OpenShift images is occuring in background process with pid 12909.
```

## Configure minishift for your development Mac

*Command*

```bash
minishift oc-env
```

*Response*

```bash
export PATH="/Users/willingc/.minishift/cache/oc/v3.7.1/darwin:$PATH"
# Run this command to configure your shell:
# eval $(minishift oc-env)
```

*Command*

```bash
export PATH="/Users/willingc/.minishift/cache/oc/v3.7.1/darwin:$PATH"
eval $(minishift oc-env)
echo $PATH
```

*Response*

```bash
# Nothing displayed for `export PATH...`
# Nothing displayed for `eval $(minishift oc-env)`
/Users/willingc/.minishift/cache/oc/v3.7.1/darwin:/Library/Frameworks/Python.framework/Versions/3  ... :/bin:/usr/sbin:/sbin:/usr/local/go/bin:/opt/X11/bin
# Your $PATH's output will differ.
```

## minishift commands


- `minishift ip`: get IP address of cluster
- `minishift oc-env`: display command to update PATH to the openshift command line interface, `oc`

## Creating a new app

TODO