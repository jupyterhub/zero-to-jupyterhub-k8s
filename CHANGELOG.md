# Changelog

Here you can find upgrade changes in between releases and upgrade instructions.

## [0.10]

### [0.10.0]

#### Breaking changes:

- Predefined Kubernetes
  [NetworkPolicies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
  are now created by default, explicitly describing allowed incoming (_ingress_)
  and outgoing (_egress_) network communication for the hub, proxy, and user
  pods. These network policies explicitly allow only the network communication
  known to be needed, with the exception of the user pods outgoing
  communication, where all outgoing communication is allowed by default.
  
  Note that these network policies only influence network communication in a
  Kubernetes cluster if a NetworkPolicy controller enforce them, such as Calico.

  With network policies enabled, you may require additional configuration,
  especially for deployments that include additional components that access
  JupyterHub pods directly (i.e. not through the `proxy-public` service).

  See the [security
  documentation](https://zero-to-jupyterhub.readthedocs.io/en/latest/administrator/security.html#kubernetes-network-policies)
  for more details on this.

## [0.9]

### [0.9.0] - 2020-04-15

#### Release summary

This Helm chart release is mainly a maintenance release featuring the latest
JupyterHub (1.1.0) and authenticators along with bug fixes and some additional
helpful configuration options.

Noteworthy:
- An issue with automatic acquisition of HTTPS certificates has been resolved
  since 0.9.0-beta.3.
- Fixed a compatibility issue with Kubernetes 1.16+
- The `images/hub/requirements.txt` file in this repo can now be used to track
  what specific version has been used at any point in time.
- [jupyterhub-nativeauthenticator](https://native-authenticator.readthedocs.io/en/latest/) added to the JupyterHub Docker image.

Bumped dependencies:
- jupyterhub version 1.1.0
- jupyterhub-ldapauthenticator version 1.3.0
- jupyterhub-kubespawner version 0.11.1
- oauthenticator version 0.11.0
- kubernetes version 10.0.1

#### Upgrade instructions (IMPORTANT)

1. If you are using Helm 2, upgrade to the latest Helm 2 version. And if you are
   using Helm 3, upgrade to the latest Helm 3 version.
   
   Upgrading to Helm 3 from Helm 2 requires additional steps not covered here,
   so for now please stay with your current major version of helm (2 or 3).

   ```
   # Figure out what version you currently have locally, you should use
   # release of the same major version you have used before.
   helm version
   ```

   Install either the latest [Helm
   2](https://v2.helm.sh/docs/using_helm/#installing-helm) or [Helm
   3](https://helm.sh/docs/intro/install/) depending on what major version you
   currently had worked with.

   ```
   # verify you successfully upgraded helm
   helm version

   # if you just upgraded helm 2, also upgrade tiller
   helm init --upgrade --service-account=tiller
   ```

2. Use `--cleanup-on-fail` when using `helm upgrade`.

   Helm can enter a problematic state by a `helm` install or upgrade process
   which started creating Kubernetes resources, but then didn't finish at all or
   didn't finish successfully. It can cause resources created that helm will
   later come in conflict with.

   To mitigate this, we suggest always using `--cleanup-on-fail` with this Helm
   chart, it is a solid behavior that reduce a lot of head ache.

3. If you use `--wait`, or `--atomic` which implies `--wait`: do not manually
   cancel the upgrade!

   If you would abort the upgrade when using `--wait` and Kubernetes resources
   has been created, resources will have been created that can cause conflict
   with future upgrades and require you to manually clean them up.

4. Delete resources that could cause issues before upgrading.

   ```shell
   # replace <NAMESPACE> below with where jupyterhub is installed
   kubectl delete -n <NAMESPACE> clusterrole,clusterrolebinding,role,rolebinding,serviceaccount,deployment,configmap,service -l component=autohttps
   ```

#### Troubleshooting upgrade

If you get an error similar to the one below, it is a symptom of having
attempted a `helm upgrade` that failed where helm lost track of some newly
created resources. A good solution is to delete all of these resources and try
again.

```shell
# replace <NAMESPACE> below with where jupyterhub is installed
kubectl delete -n <NAMESPACE> clusterrole,clusterrolebinding,role,rolebinding,serviceaccount,deployment,configmap,service -l component=autohttps
```

To avoid this in the future, use `--cleanup-on-fail` with the `helm upgrade`
command. It is not a fool proof way to avoid it, but . And note that even if that flag is used, an interupption for example during `--wait` or `--atomic` which implies `--wait`, be
aware of an interruption while waiting can very likely cause this to arise on
the following upgrade attempt.

> ```
> error: kind ConfigMap with the name "traefik-proxy-config" already exists in
> the cluster and wasn't defined in the previous release. Before upgrading,
> please either delete the resource from the cluster or remove it from the chart
> ```

#### Dependency updates

* Bump configurable-http-proxy image [#1598](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1598) ([@consideRatio](https://github.com/consideRatio))
* fix: Bump to base-notebook with JH 1.1.0 etc [#1588](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1588) ([@bitnik](https://github.com/bitnik))

#### Maintenance

* Docs: refactor/docs for local development of docs [#1617](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1617) ([@consideRatio](https://github.com/consideRatio))
* [MRG] sphinx: linkcheck in travis (allowed to fail) [#1611](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1611) ([@manics](https://github.com/manics))
* [MRG] Sphinx: warnings are errors [#1610](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1610) ([@manics](https://github.com/manics))
* pydata theme [#1608](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1608) ([@choldgraf](https://github.com/choldgraf))
* Small typo fix in doc [#1591](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1591) ([@sebastianpfischer](https://github.com/sebastianpfischer))
* [MRG] Pin sphinx theme [#1589](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1589) ([@manics](https://github.com/manics))
* init helm and tiller with history-max settings [#1587](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1587) ([@bitnik](https://github.com/bitnik))
* Changelog for 0.9.0-beta.4 [#1585](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1585) ([@manics](https://github.com/manics))
* freeze environment in hub image [#1562](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1562) ([@minrk](https://github.com/minrk))

### [0.9.0-beta.4] - 2020-02-26

#### Added
* Add nativeauthenticator to hub image [#1583](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1583) ([@consideRatio](https://github.com/consideRatio))
* Add option to remove named server when culling [#1558](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1558) ([@betatim](https://github.com/betatim))

#### Dependency updates
* jupyterhub-ldapauthenticator==1.3 [#1576](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1576) ([@manics](https://github.com/manics))
* First-class azuread support, oauth 0.11 [#1563](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1563) ([@minrk](https://github.com/minrk))
* simplify hub-requirements [#1560](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1560) ([@minrk](https://github.com/minrk))
* Bump to base-notebook with JH 1.1.0 etc [#1549](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1549) ([@consideRatio](https://github.com/consideRatio))

#### Fixed
* Fix removing of named servers when culled [#1567](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1567) ([@consideRatio](https://github.com/consideRatio))

#### Maintenance
* Added gitlab URL [#1577](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1577) ([@metonymic-smokey](https://github.com/metonymic-smokey))
* Fix reference doc link [#1570](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1570) ([@clkao](https://github.com/clkao))
* Add contributor badge [#1559](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1559) ([@GeorgianaElena](https://github.com/GeorgianaElena))
* Trying to clean up formatting [#1555](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1555) ([@jeremycadams](https://github.com/jeremycadams))
* Remove unneeded directive in traefik config [#1554](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1554) ([@yuvipanda](https://github.com/yuvipanda))
* Added documentation of secret https mode [#1553](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1553) ([@RossRKK](https://github.com/RossRKK))
* Helm 3 preview [#1543](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1543) ([@manics](https://github.com/manics))


### [0.9.0-beta.3] - 2020-01-17

#### Dependency updates

* Deploy jupyterhub 1.1.0 stable [#1548](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1548) ([@minrk](https://github.com/minrk))
* Bump chartpress for Helm 3 compatible dev releases [#1542](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1542) ([@consideRatio](https://github.com/consideRatio))

#### Fixed

* Replace kube-lego + nginx ingress with traefik [#1539](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1539) ([@yuvipanda](https://github.com/yuvipanda))

#### Maintenance
* Update step zero for Azure docs with commands to setup an VNet and network policy [#1527](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1527) ([@sgibson91](https://github.com/sgibson91))
* Fix duplicate docs label [#1544](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1544) ([@manics](https://github.com/manics))
* Made GCP docs of compute zone names generic [#1431](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1431) ([@metonymic-smokey](https://github.com/metonymic-smokey))

### [0.9.0-beta.2] - 2019-12-26

#### Fixed

* Fix major breaking change if all HTTPS options was disabled introduced just before beta.1 [#1534](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1534) ([@dirkcgrunwald](https://github.com/dirkcgrunwald))

### [0.9.0-beta.1] - 2019-12-26

Some highlights of relevance for this release are:

- The default configuration is now catering to autoscaling clusters where nodes
  can be added and removed, as compared to fixed clusters where there is only a
  fixed amount of nodes. Set `scheduling.userScheduler.enabled` to false if you
  are on a fixed size cluster.
- Kubernetes 1.16 compatibility achieved
- Updated dependencies
  - jupyterhub==1.1.0b1
  - kubernetes==0.10.1
  - kubespawner==0.11.1
  - oauthenticator==0.10.0

#### Added

* Added ability to configure liveness/readiness probes on the hub/proxy [#1480](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1480) ([@mrow4a](https://github.com/mrow4a))
* Added ability to use an existing/shared image pull secret for hub and image pullers [#1426](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1426) ([@LaurentGoderre](https://github.com/LaurentGoderre))
* Added ability to configure the proxy's load balancer service's access restrictions (`loadBalancerSourceRanges`) [#1418](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1418) ([@GergelyKalmar](https://github.com/GergelyKalmar))
* Added `user-scheduler` pod->node scheduling policy configuration [#1409](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1409) ([@yuvipanda](https://github.com/yuvipanda))
* Added ability to add additional ingress rules to k8s NetworkPolicy resources [#1380](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1380) ([@yuvipanda](https://github.com/yuvipanda))
* Enabled the continuous image puller by default [#1276](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1276) ([@consideRatio](https://github.com/consideRatio))
* Added ability to configure initContainers of the hub pod [#1274](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1274) ([@scottyhq](https://github.com/scottyhq))
* Enabled the user-scheduler by default [#1272](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1272) ([@minrk](https://github.com/minrk))
* Added ability to use an existing jupyterhub configuration k8s secret for hub (not recommended) [#1142](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1142) ([@koen92](https://github.com/koen92))
* Added use of liveness/readinessProbe by default [#1004](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1004) ([@tmshn](https://github.com/tmshn))

#### Dependency updates

* Bump JupyterHub to 1.1.0b1 [#1533](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1533) ([@consideRatio](https://github.com/consideRatio))
* Update JupyterHub version [#1524](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1524) ([@bitnik](https://github.com/bitnik))
* Re-add ltiauthenticator 0.4.0 to hub image [#1519](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1519) ([@consideRatio](https://github.com/consideRatio))
* Fix hub image dependency versions, disable ltiauthenticator, use chartpress==0.5.0 [#1518](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1518) ([@consideRatio](https://github.com/consideRatio))
* Update hub image dependencies and RELEASE.md regarding dependencies [#1484](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1484) ([@consideRatio](https://github.com/consideRatio))
* Bump kubespawner to 0.11.1 for spawner progress bugfix [#1502](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1502) ([@consideRatio](https://github.com/consideRatio))
* Updated hub image dependencies [#1484](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1484) ([@consideRatio](https://github.com/consideRatio))
* Updated kube-scheduler binary used by user-scheduler, kubespawner, kubernetes python client, and oauthenticator [#1483](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1483) ([@consideRatio](https://github.com/consideRatio))
* Bump CHP to 4.2.0 - we get quicker chart upgrades now [#1481](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1481) ([@consideRatio](https://github.com/consideRatio))
* Bump singleuser-sample [#1473](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1473) ([@consideRatio](https://github.com/consideRatio))
* Bump python-kubernetes to 9.0.* (later also to 10.0.*) [#1454](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1454) ([@clkao](https://github.com/clkao))
* Bump tmpauthenticator to 0.6 (needed for jupyterhub 1.0) [#1299](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1299) ([@manics](https://github.com/manics))
* Include jupyter-firstuseauthenticator. [#1288](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1288) ([@danielballan](https://github.com/danielballan))
* Bump jupyterhub to 1.0.0 (later also to a post 1.0.0 commit) [#1263](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1263) ([@minrk](https://github.com/minrk))
* Bump CHP image to 4.1.0 from 3.0.0 (later to 4.2.0) [#1246](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1246) ([@consideRatio](https://github.com/consideRatio))
* Bump oauthenticator 0.8.2 (later to 0.10.0) [#1239](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1239) ([@minrk](https://github.com/minrk))
* Bump jupyterhub to 1.0b2 (later to an post 1.0.0 commit) [#1224](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1224) ([@minrk](https://github.com/minrk))

#### Fixed

* Workaround upstream kubernetes issue regarding https health check [#1531](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1531) ([@sstarcher](https://github.com/sstarcher))
* User-scheduler RBAC permissions for local-path-provisioner + increase robustness of hub.baseUrl interaction with the hub deployments health endpoint [#1530](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1530) ([@cutiechi](https://github.com/cutiechi))
* Fixing #1300 User-scheduler doesn't work with rancher/local-path-provisioner [#1516](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1516) ([@cgiraldo](https://github.com/cgiraldo))
* Move z2jh.py to a python and linux distribution agnostic path [#1478](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1478) ([@mrow4a](https://github.com/mrow4a))
* Bugfix for proxy upgrade strategy in PR #1401 [#1404](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1404) ([@consideRatio](https://github.com/consideRatio))
* Use recreate CHP proxy pod's deployment strategy [#1401](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1401) ([@consideRatio](https://github.com/consideRatio))
* Proxy deployment: Change probes to https port [#1378](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1378) ([@chicocvenancio](https://github.com/chicocvenancio))
* Readiness and liveness probes re-added [#1361](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1361) ([@consideRatio](https://github.com/consideRatio))
* Use 443 as https port or redirection. FIX #806 [#1341](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1341) ([@chicocvenancio](https://github.com/chicocvenancio))
* Revert "Configure liveness/readinessProbe" [#1356](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1356) ([@consideRatio](https://github.com/consideRatio))
* Ensure helm chart configuration is passed to JupyterHub where needed [#1338](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1338) ([@bitnik](https://github.com/bitnik))
* Make proxy redirect to the service port 443 instead of the container port 8443 [#1337](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1337) ([@LucidNeko](https://github.com/LucidNeko))
* Disable becoming root inside hub and proxy containers [#1280](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1280) ([@yuvipanda](https://github.com/yuvipanda))
* Configure KubeSpawner with the `singleuser.image.pullPolicy` properly [#1248](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1248) ([@vmarkovtsev](https://github.com/vmarkovtsev))
* Supply `hub.runAsUser` for the hub at the container level instead of the pod level [#1240](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1240) ([@tmc](https://github.com/tmc))
* Relax HSTS requirement on subdomains [#1219](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1219) ([@yuvipanda](https://github.com/yuvipanda))

#### Maintenance

* typo [#1529](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1529) ([@raybellwaves](https://github.com/raybellwaves))
* fix link to Helm chart best practices [#1523](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1523) ([@rpwagner](https://github.com/rpwagner))
* Adding Globus to the list of users [#1522](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1522) ([@rpwagner](https://github.com/rpwagner))
* Missing page link for our RBAC documentation #1508 [#1514](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1514) ([@n3o-Bhushan](https://github.com/n3o-Bhushan))
* Correction of warnings from: make html [#1513](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1513) ([@consideRatio](https://github.com/consideRatio))
* Fixing URL for user-management documentation #1511 [#1512](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1512) ([@n3o-Bhushan](https://github.com/n3o-Bhushan))
* DOC: fixing authentication link in user customization guide [#1510](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1510) ([@n3o-Bhushan](https://github.com/n3o-Bhushan))
* DOC: fix kubernetes setup link [#1505](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1505) ([@raybellwaves](https://github.com/raybellwaves))
* Update changelog for 0.9.0-beta.1 [#1503](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1503) ([@consideRatio](https://github.com/consideRatio))
* Fix broken link in architecture.rst [#1488](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1488) ([@amcnicho](https://github.com/amcnicho))
* Bump kind to 0.6.0 and kindest/node versions [#1487](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1487) ([@clkao](https://github.com/clkao))
* Avoid rate limiting for k8s resource validation [#1485](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1485) ([@consideRatio](https://github.com/consideRatio))
* Switching to the Pandas Sphinx theme [#1472](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1472) ([@choldgraf](https://github.com/choldgraf))
* Add vi / less to hub image [#1471](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1471) ([@yuvipanda](https://github.com/yuvipanda))
* Added existing pull secrets changes from PR #1426 to schema [#1461](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1461) ([@sgloutnikov](https://github.com/sgloutnikov))
* Chart upgrade tests [#1459](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1459) ([@consideRatio](https://github.com/consideRatio))
* Replaced broken links in authentication document #1449 [#1457](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1457) ([@n3o-Bhushan](https://github.com/n3o-Bhushan))
* Fix typo in home page of docs [#1456](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1456) ([@celine168](https://github.com/celine168))
* Use helm 2.15.1 [#1453](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1453) ([@consideRatio](https://github.com/consideRatio))
* Support CD with git tags [#1450](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1450) ([@consideRatio](https://github.com/consideRatio))
* Added Laurent Goderre as contributor [#1443](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1443) ([@LaurentGoderre](https://github.com/LaurentGoderre))
* Note about future hard deprecation [#1441](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1441) ([@consideRatio](https://github.com/consideRatio))
* Fix link formatting for ingress.enabled [#1438](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1438) ([@jtpio](https://github.com/jtpio))
* CI rework - use kind, validate->test->publish, contrib and release rework [#1422](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1422) ([@consideRatio](https://github.com/consideRatio))
* Mounting jupyterhub_config.py etc. [#1407](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1407) ([@consideRatio](https://github.com/consideRatio))
* Ignore venv files [#1388](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1388) ([@GeorgianaElena](https://github.com/GeorgianaElena))
* Added example for populating notebook user home directory [#1382](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1382) ([@gareth-j](https://github.com/gareth-j))
* Fix typo in jupyterhub_config.py comment [#1376](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1376) ([@loganlinn](https://github.com/loganlinn))
* Fixed formatting error in links [#1363](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1363) ([@tlkh](https://github.com/tlkh))
* Instructions for adding GPUs and increasing shared memory [#1358](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1358) ([@tlkh](https://github.com/tlkh))
* delete redundant prepuller documentation [#1348](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1348) ([@bitnik](https://github.com/bitnik))
* Add py-spy to hub image [#1327](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1327) ([@yuvipanda](https://github.com/yuvipanda))
* Changing Azure Container Service to Azure Kubernetes Service [#1322](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1322) ([@seanmck](https://github.com/seanmck))
* add explanation for lifecycle_hooks in kubespawner_override [#1309](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1309) ([@clancychilds](https://github.com/clancychilds))
* Update chart version to 0.8.2 in the docs [#1304](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1304) ([@jtpio](https://github.com/jtpio))
*  Fix azure cli VMSSPreview feature register command  [#1298](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1298) ([@dazzag24](https://github.com/dazzag24))
* Unbreak git build [#1294](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1294) ([@joshbode](https://github.com/joshbode))
* Update Dockerfile to JH 1.0 [#1291](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1291) ([@vilhelmen](https://github.com/vilhelmen))
* Fix a couple of mistakes in Google Kubernetes instructions [#1290](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1290) ([@astrofrog](https://github.com/astrofrog))
* Suggest quotes around tag. [#1289](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1289) ([@danielballan](https://github.com/danielballan))
* hub: Add useful debugging tools to hub image [#1279](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1279) ([@yuvipanda](https://github.com/yuvipanda))
* Clean up a line in the CI logs [#1278](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1278) ([@consideRatio](https://github.com/consideRatio))
* Fix prePuller.extraImages linting etc [#1275](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1275) ([@consideRatio](https://github.com/consideRatio))
* Fixed minor bug in google pricing calculator [#1264](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1264) ([@noahbjohnson](https://github.com/noahbjohnson))
* [MRG] Update to Docs: Deploying an Autoscaling Kubernetes cluster on Azure [#1258](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1258) ([@sgibson91](https://github.com/sgibson91))
* Update to Docs: Add Azure scale command to Expanding/Contracting Cluster section [#1256](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1256) ([@sgibson91](https://github.com/sgibson91))
* removing extra buttons [#1254](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1254) ([@choldgraf](https://github.com/choldgraf))
* test appVersion in Chart.yaml [#1238](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1238) ([@minrk](https://github.com/minrk))
* Adjusts whitespace for a code block in AWS instructions. [#1237](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1237) ([@arokem](https://github.com/arokem))
* Change heading of multiple-profiles section [#1236](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1236) ([@moschlar](https://github.com/moschlar))
* Suggest Discourse in issue template [#1234](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1234) ([@manics](https://github.com/manics))
* Added OAuth callback URL to keycloak OIDC example [#1232](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1232) ([@sgloutnikov](https://github.com/sgloutnikov))
* Updated notes, pod status to Running [#1231](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1231) ([@sgloutnikov](https://github.com/sgloutnikov))
* Updated AWS EKS region-availability statement. [#1223](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1223) ([@javabrett](https://github.com/javabrett))
* Fix the default value of lifecycleHooks [#1218](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1218) ([@consideRatio](https://github.com/consideRatio))
* Update user-environment.rst [#1217](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1217) ([@manycoding](https://github.com/manycoding))
* Add Digital Ocean Cloud Instructions for Kubernetes [#1192](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/1192) ([@alexmorley](https://github.com/alexmorley))



## [0.8]

### [0.8.2] - 2019-04-01

Bumped the underlying JupyterHub to 0.9.6.

### [0.8.1] - 2019-03-28

Bumped the underlying JupyterHub to 0.9.5.

### [0.8.0] - [Richie Benaud](https://en.wikipedia.org/wiki/Richie_Benaud) - 2019-01-24

This release contains JupyterHub version 0.9.4. It requires Kubernetes >= 1.11 and Helm >= 2.11.0.
See [the Helm Chart repository](https://github.com/jupyterhub/helm-chart#release-notes) for
a list of relevant dependencies for all Helm Chart versions.

It contains new features, additional configuration options, and bug fixes.

#### Upgrading from 0.7

To upgrade your cluster:

1. backup your hub-db-dir persistent volume and previous configuration files, to be safe
2. read changes here and make any needed updates to your configuration
3. upgrade the chart:

    helm repo update
    helm upgrade $RELEASE --force --version 0.8.0 --values config.yaml

The `--force` flag allows deletion and recreation of objects
that have certain changes, such as different labels,
which are forbidden otherwise.

#### Breaking changes

- Github organisation OAuth: `auth.github.org_whitelist` has been renamed to `auth.github.orgWhitelist` to be consistent with helm's camelCase style


#### Troubleshooting

If you encounter issues with upgrades, check for changed configuration in this document, and make sure your config is up to date.

If you aren't able to get the upgrade to work,
you can [rollback](https://docs.helm.sh/helm/#helm-rollback)
to a previous version with:

    helm rollback $RELEASE


Feel free to [ping us on gitter](https://gitter.im/jupyterhub/jupyterhub)
if you have problems or questions.

#### New Features

##### Easier user-selectable profiles upon login

Profile information is now passed through to KubeSpawner. This means you can
[specify multiple user profiles that users can select from](https://zero-to-jupyterhub.readthedocs.io/en/latest/user-environment.html?highlight=profile#allow-users-to-create-their-own-conda-environments)
when they log in. ([#402](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues/402))

##### Configurable image pull secrets

Improvements to the Helm Chart to let users specify private information that lets
the Hub pull from private Docker registries. New information includes
Kubernetes Secrets, an email field, large JSON blobs in the password field (required
in order to pull from a private gcr.io registry from an external cluster).

It also ensures that the image puller DaemonSets have the same credentials to pull the images.

(thanks to @AlexMorreale) #851

##### Improved user scheduling and resource management

#891

Want to make your autoscheduler work efficiently? Then you should schedule pods to pack tight instead of spread out. The user scheduler accomplishes this.


- **Pod priority and User placeholders** - #929

Want to scale up before users arrive so they don't end up waiting for the node to pull an image of several gigabytes in size? By adding a configurable fixed amount of user placeholder pods with a lower [pod priority](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/) than real user pods, we can accomplish this. It requires k8s v1.11 though.


- **preferScheduleNextToRealUsers - improves autoscaling** - #930
  This setting slightly improves the ability for a cluster autoscaler to scale down by increasing the likelihood of user placeholders being left alone on a node rather than real users. Real users can't be moved around while user placeholder pods can

#### Minor upgrades and development improvements

- **Update jupyterhub to 0.9.4**
- **Update kubespawner to 0.10.1**
- **Allow setting of storage labels** - #924
- **Tolerations for node taints** - #925
- **Making the core and user pods affinity have configurable presets** - #927
- **Improved linting and validation + CI integration** - #844
- **Improved CI tests** - #846
- **Cleanup of orphaned files** - #842
  Two files were left unused in the repo.
- **cull.maxAge bugfix** - #853
  `cull.maxAge` previously didn't influence the culler service, as the value was never consumed. This is fixed by a single one line commit in a PR.
- **No more duplicates of puller pods** - #854
  Nobody wants pods running that does nothing. By using the new `before-hook-creation` value for the `deletion-policy` Helm hook together with a single name for our Helm hook resources, we can ensure never having orphaned image pullers.
- **Remove pod-culler image** - #890 #919
  Before JupyterHub 0.9 the pod-culler was a standalone pod with a custom image. But now it is a internal service of the JupyterHub pod, so in this PR we slim the remnant code.
- **Upgrade to k8s 1.9 APIs** - #920
  Migrate to more stable K8s resource APIs from `beta`.
- **Update of the singleuser-sample image** - #888
  `git` and `nbgitpuller` are now available by default
- **Switch to using a StatefulSet for the Hub** __*__
  The Hub should perhaps be a StatefulSet rather than a Deployment as it tends to be tied to a PV that can only be mounted by one single Hub. See this issue: https://github.com/helm/charts/issues/1863
- Show users deprecation and error messages when they use certain deprecated
  configuration (e.g. `hub.extraConfig` as a single string)
  or incompatible combinations.
- **Updates to the guide** - #850
- **Updates to inline documentation** - #939

#### [Richie Benaud](https://www.cricket.com.au/players/richie-benaud/gvp5xSjUp0q6Qd7IM5TbCg)

_(excerpt from https://www.cricket.com.au/players/richie-benaud/gvp5xSjUp0q6Qd7IM5TbCg)_

Possibly the most iconic man in Australian cricket, Richie Benaud enjoyed a career spanning nearly
70 years in the game. On the field, he scored 767 runs at 19.66 in his 27 matches against England,
while he also picked up 83 wickets. Off the field,
he has been just as important. His commentary has been second to none since making his radio debut in 1960.

While playing for Australia, fans flocked to the cricket to watch Benaud led sides
dominate whoever they played. The late 1950’s to early 1960’s was a golden period in
Australian cricket, with players such as Simpson, Lawry and Harvey
scoring runs, while Benaud and Davidson did the damage with the ball.

Richie Benaud was responsible for resurrecting cricket in this country. The world was
changing at that time, and so was cricket. It was being shown on television for the
first time, while radio coverage was becoming more advanced. Benaud
felt he had a duty to the Australian public to make the game more entertaining. Sure,
you could argue that the 1961 series was dull, but at least Australia
retained the Ashes. Nobody will forget the tied Test against the West Indies, or Benaud’s
audacious move to bowl around the wicket in Manchester.

Benaud is credited with popularising the tactics we see today. Huddles after a wicket
were born in the Benaud era. Declaring just before stumps in a bid to steal a late wicket
was something he thrived upon. Bowling into the rough is now seen
as common practice.

Benaud was also prepared to try new things with the ball. He worked very hard on
perfecting his wrong’un, the flipper and the top-spinner. His leg-spinner even had variety
to it, making him one of the most complete tweakers at the time.

His leadership earned him respect immediately. Players loved being guided the
likeable larrikin from Penrith. He looked after everyone both as a team, but also on an
individual basis. His teammates trusted his innovative ideas, while
he trusted them to execute them to the fullest.

For most Australians, summer means cricket. And cricket means hearing the dulcet
tones of their favourite commentator, Richie Benaud. From the cream coloured suit, to the
witty repartee with his colleagues, Benaud is the complete package


#### Contributors

This release wouldn't have been possible without the wonderful contributors
to the [zero-to-jupyterhub](https://github.com/jupyterhub/zero-to-jupyterhub-k8s),
and [KubeSpawner](https://github.com/jupyterhub/kubespawner) repos.
We'd like to thank everyone who contributed in any form - Issues, commenting
on issues, PRs and reviews since the last Zero to JupyterHub release.

[(Frank) Yu Cheng Gu](https://github.com/frankgu968)
[1160300422-RenQJ](https://github.com/1160300422)
[1kastner](https://github.com/1kastner)
[2efper](https://github.com/2efPer)
[A. Tan ](https://github.com/amanda-tan)
[Aadi Deshpande](https://github.com/cilquirm)
[abremirata28](https://github.com/abremirata28)
[AcademicAdmin](https://github.com/AcademicAdmin)
[Adam Huffman](https://github.com/verdurin)
[Adrian Wilke](https://github.com/adibaba)
[Akanksha Bhardwaj](https://github.com/sashafierce)
[Akhil Lawrence](https://github.com/akhilputhiry)
[Al Johri](https://github.com/AlJohri)
[AlbanWende](https://github.com/AlbanWende)
[Alejandro del Castillo](https://github.com/adelcast)
[Aleksandr Blekh](https://github.com/ablekh)
[Alex Morreale](https://github.com/AlexMorreale)
[Alex Newman](https://github.com/posix4e)
[Alexander Comerford](https://github.com/cmrfrd)
[Alexander Sadleir](https://github.com/maxious)
[amangarg96](https://github.com/amangarg96)
[Amirahmad Khordadi](https://github.com/khordadi)
[Andreas Hilboll](https://github.com/andreas-h)
[andregouveiasantana](https://github.com/andregouveiasantana)
[Andrew](https://github.com/feriat)
[Andrew Catellier](https://github.com/whlteXbread)
[angelikamukhina](https://github.com/angelikamukhina)
[Anton Khodak](https://github.com/anton-khodak)
[arcady-genkin](https://github.com/arcady-genkin)
[Ariel Rokem](https://github.com/arokem)
[Arne Küderle](https://github.com/AKuederle)
[atne2008](https://github.com/atne2008)
[awalther](https://github.com/awalther)
[Ben Zipperer](https://github.com/benzipperer)
[Beneath](https://github.com/beneathcrypto)
[Benjamin Egelund-Müller](https://github.com/bem7)
[BertR](https://github.com/BertR)
[bharathwgl](https://github.com/bharathwgl)
[bing-he](https://github.com/bing-he)
[bjyxmas](https://github.com/bjyxmas)
[bpoettinger](https://github.com/bpoettinger)
[Brad Skaggs](https://github.com/bskaggs)
[Braden](https://github.com/brasie)
[Brian E. Granger](https://github.com/ellisonbg)
[Bruno P. Kinoshita](https://github.com/kinow)
[brynjsmith](https://github.com/brynjsmith)
[Calvin Canh Tran](https://github.com/canhtran)
[camer314](https://github.com/camer314)
[Carol Willing](https://github.com/willingc)
[Caspian](https://github.com/Cas-pian)
[cfoisy-osisoft](https://github.com/cfoisy-osisoft)
[ChanakyaBandara](https://github.com/ChanakyaBandara)
[chang-zhijie](https://github.com/chang-zhijie)
[Chao Wang](https://github.com/wangxiaoxiao88)
[Chen Zhiwei](https://github.com/chenzhiwei)
[Chester Li](https://github.com/chaoleili)
[Chia-liang Kao](https://github.com/clkao)
[Chris Holdgraf](https://github.com/choldgraf)
[Chris Seal](https://github.com/cmseal)
[Christian Alis](https://github.com/ianalis)
[Christian Mesh](https://github.com/cam72cam)
[chrlunden](https://github.com/chrlunden)
[Clancy Childs](https://github.com/clancychilds)
[Clemens Tolboom](https://github.com/clemens-tolboom)
[cmw2196](https://github.com/cmw2196)
[Cody Scott](https://github.com/Siecje)
[Craig Willis](https://github.com/craig-willis)
[cristofercri](https://github.com/cristofercri)
[Curtis Maves](https://github.com/cmaves)
[cybertony](https://github.com/cybertony)
[Daisuke Taniwaki](https://github.com/dtaniwaki)
[Dalon Lobo](https://github.com/dalonlobo)
[danamer](https://github.com/danamer)
[Daniel Bachler](https://github.com/danyx23)
[Daniel Chalef](https://github.com/danielchalef)
[Daniel Hnyk](https://github.com/hnykda)
[danielpcs](https://github.com/danielpcs)
[Danny H](https://github.com/toblender)
[DataVictorEngineer](https://github.com/DataVictorEngineer)
[Dave Hirschfeld](https://github.com/dhirschfeld)
[Dave Porter](https://github.com/porterde)
[David Andersen](https://github.com/dtandersen)
[David John Gagne](https://github.com/djgagne)
[Davide](https://github.com/davidedelvento)
[Deleted user](https://github.com/ghost)
[Denis Shestakov](https://github.com/denshe)
[Dennis Kipping](https://github.com/dkipping)
[Derek Ludwig](https://github.com/dsludwig)
[DerekHeldtWerle](https://github.com/DerekHeldtWerle)
[DewinGoh](https://github.com/DewinGoh)
[Diogo](https://github.com/dmvieira)
[djknight1](https://github.com/djknight1)
[DmitrII Gerasimenko](https://github.com/kidig)
[Doug Blank](https://github.com/dsblank)
[Dr. Di Prodi](https://github.com/robomotic)
[Dr. Zoltán Katona](https://github.com/zkatona)
[Dylan Nelson](https://github.com/dnelson86)
[ebebpl](https://github.com/ebebpl)
[Eliran Bivas](https://github.com/bivas)
[eode](https://github.com/eode)
[Eran Pinhas](https://github.com/eran-pinhas)
[eric-leblouch](https://github.com/eric-leblouch)
[ericblau](https://github.com/ericblau)
[Erik LaBianca](https://github.com/easel)
[Erik Sundell](https://github.com/consideRatio)
[Ermakov Petr](https://github.com/ermakovpetr)
[erolosty](https://github.com/erolosty)
[Evan Savage](https://github.com/candu)
[Evert Rol](https://github.com/evertrol)
[Ezequiel Gioia](https://github.com/eze1981)
[fahadabbas91](https://github.com/fahadabbas91)
[farzadz](https://github.com/farzadz)
[foxlisimulation](https://github.com/foxlisimulation)
[frouzbeh](https://github.com/frouzbeh)
[Félix-Antoine Fortin](https://github.com/cmd-ntrf)
[Gabriel Abdalla Cavalcante](https://github.com/gcavalcante8808)
[Gabriel Fair](https://github.com/gabefair)
[Gaetan Semet](https://github.com/gsemet)
[Gang Chen](https://github.com/ssword)
[Gary Lucas](https://github.com/luck02)
[Georgiana Elena](https://github.com/GeorgianaElena)
[gerroon](https://github.com/gerroon)
[Giuseppe Attardi](https://github.com/attardi)
[Glen A Knight](https://github.com/glenak1911)
[Gonzalo Fernandez ordas](https://github.com/rainmanh)
[Guilherme Oenning](https://github.com/goenning)
[Guo Zhang](https://github.com/Guo-Zhang)
[gweis](https://github.com/gweis)
[Gábor Lipták](https://github.com/gliptak)
[Hagen Hoferichter](https://github.com/h4gen)
[hani1814](https://github.com/hani1814)
[Hans Permana](https://github.com/hans-permana)
[hhuuggoo](https://github.com/hhuuggoo)
[hichemken](https://github.com/hichemken)
[HT-Moh](https://github.com/HT-Moh)
[HuangHenghua](https://github.com/HuangHenghua)
[HuiWang](https://github.com/scially)
[Ian Carroll](https://github.com/itcarroll)
[Ian Stuart](https://github.com/perllaghu)
[Ivan Brezina](https://github.com/ibre5041)
[J Forde](https://github.com/jzf2101)
[J Gerard](https://github.com/jgerardsimcock)
[j08rebelo](https://github.com/j08rebelo)
[Jacob Matuskey](https://github.com/jmatuskey)
[Jacob Tomlinson](https://github.com/jacobtomlinson)
[Jaime Ferrando Huertas](https://github.com/jiwidi)
[James Swineson](https://github.com/Jamesits)
[jameshgrn](https://github.com/jameshgrn)
[Jan Niederau](https://github.com/Japhiolite)
[Jason Belsky](https://github.com/jbelsky)
[Jason Hu](https://github.com/Jameshzc)
[Jason Rigby](https://github.com/jasonrig)
[jason4zhu](https://github.com/jason4zhu)
[Jeff Whitworth](https://github.com/jwhitwo)
[Jeffrey Bush](https://github.com/coderforlife)
[jeffwji](https://github.com/jeffwji)
[Jessica B. Hamrick](https://github.com/jhamrick)
[jfleury-eidos](https://github.com/jfleury-eidos)
[Ji Ma](https://github.com/ma-ji)
[Jiren Jin](https://github.com/jinjiren)
[jiyer2016](https://github.com/jiyer2016)
[jlc175](https://github.com/jlc175)
[jmabry](https://github.com/jmabry)
[jmchandonia](https://github.com/jmchandonia)
[jmf](https://github.com/jmfcodes)
[Joe Hamman](https://github.com/jhamman)
[Joerg Klein](https://github.com/joergklein)
[John Chase](https://github.com/johnchase)
[John Readey](https://github.com/jreadey)
[John Shojaei](https://github.com/titan550)
[Jonathan Terhorst](https://github.com/terhorst)
[Jordan Miller](https://github.com/LegitStack)
[Josh Bode](https://github.com/joshbode)
[Joshua Milas](https://github.com/DeepHorizons)
[JP Moresmau](https://github.com/JPMoresmau)
[jpays](https://github.com/jpays)
[Juan Cruz-Benito](https://github.com/cbjuan)
[Julian Rüth](https://github.com/saraedum)
[Julien Chastang](https://github.com/julienchastang)
[Justin Ray Vrooman](https://github.com/vroomanj)
[Jürgen Hermann](https://github.com/jhermann)
[Kah Mun](https://github.com/kavemun)
[kangzebin](https://github.com/kangzebin)
[Kelly L. Rowland](https://github.com/kellyrowland)
[Kenan Erdogan](https://github.com/bitnik)
[Kerwin Sun](https://github.com/00Kai0)
[kevbutler](https://github.com/kevbutler)
[Kevin Bates](https://github.com/kevin-bates)
[khawarhere](https://github.com/khawarhere)
[kide007](https://github.com/kide007)
[Kim-Seonghyeon](https://github.com/Kim-Seonghyeon)
[kishitaku0630](https://github.com/kishitaku0630)
[Koshmaar](https://github.com/Koshmaar)
[Koustuv Sinha](https://github.com/koustuvsinha)
[krinsman](https://github.com/krinsman)
[Kristian Gregorius Hustad](https://github.com/KGHustad)
[Kristiyan](https://github.com/katsar0v)
[KSHITIJA SAHARAN](https://github.com/kshitija08)
[Kuriakin Zeng](https://github.com/kuriakinzeng)
[Kyla Harper](https://github.com/kyla-harper)
[Lachlan Musicman](https://github.com/datakid)
[Laurent Abbal](https://github.com/laurentabbal)
[Leo Gallucci](https://github.com/elgalu)
[Leopold Talirz](https://github.com/ltalirz)
[Li-Xian Chen](https://github.com/twbrandon7)
[Lisa Stillwell](https://github.com/lstillwe)
[ljb445300387](https://github.com/ljb445300387)
[Loïc Antoine Gombeaud](https://github.com/LoicAG)
[Loïc Estève](https://github.com/lesteve)
[Lucas Durand](https://github.com/lucasdurand)
[Lukasz Tracewski](https://github.com/tracek)
[m.fab](https://github.com/go-bears)
[Ma](https://github.com/ma010)
[mangecoeur](https://github.com/mangecoeur)
[Manish Kushwaha](https://github.com/manish0749)
[Marc Illien](https://github.com/jackblackCH)
[marinalopez2110](https://github.com/marinalopez2110)
[Mark Mirmelstein](https://github.com/markm42)
[Marlene Silva Marchena](https://github.com/msmarchena)
[Martin Gergov](https://github.com/marto1)
[Martin Zugnoni](https://github.com/martinzugnoni)
[Marvin Solano](https://github.com/marvin-solano)
[Marwan Baghdad](https://github.com/MrwanBaghdad)
[Matthias Bussonnier](https://github.com/Carreau)
[Matthias Klan](https://github.com/mklan)
[Matthias Lee](https://github.com/matthiaslee)
[Matthieu Boileau](https://github.com/boileaum)
[Max Mensing](https://github.com/madmax2012)
[mdivk](https://github.com/mdivk)
[Meesam Shah](https://github.com/meesam15)
[Michael Carroll](https://github.com/neffo)
[Michael Huttner](https://github.com/mhuttner)
[Michael Lovci](https://github.com/mlovci)
[Michael McCarthy](https://github.com/RonanMcCarthy)
[Michael Milligan](https://github.com/mbmilligan)
[Michael Pilosov](https://github.com/mathematicalmichael)
[michec81](https://github.com/michec81)
[Mike Croucher](https://github.com/mikecroucher)
[MikeSpark](https://github.com/MikeSpark)
[Min RK](https://github.com/minrk)
[MisterZ](https://github.com/Misteur-Z)
[Moritz Kirschner](https://github.com/cellador)
[Moritz Schlarb](https://github.com/moschlar)
[moskiGithub](https://github.com/moskiGithub)
[mpolidori](https://github.com/mpolidori)
[mrclttnz](https://github.com/mrclttnz)
[MubashirullahD](https://github.com/MubashirullahD)
[Muhammad-Imtiaz](https://github.com/Muhammad-Imtiaz)
[mxcheng2011](https://github.com/mxcheng2011)
[myidealab](https://github.com/myidealab)
[Naineel Shah](https://github.com/naineel)
[narala558](https://github.com/narala558)
[newturok](https://github.com/newturok)
[Ney Torres](https://github.com/Neyt)
[Nic Wayand](https://github.com/NicWayand)
[Nico Bellack](https://github.com/bellackn)
[nifuki](https://github.com/nifuki)
[Nils Werner](https://github.com/nils-werner)
[not4everybody](https://github.com/not4everybody)
[NotSharath](https://github.com/NotSharath)
[nschiraldi](https://github.com/nschiraldi)
[Nujjy](https://github.com/Nujjy)
[oscar6echo](https://github.com/oscar6echo)
[Paperone80](https://github.com/Paperone80)
[Patafix](https://github.com/Patafix)
[Paul Mazzuca](https://github.com/PaulMazzuca)
[Paul Shealy](https://github.com/paulshealy1)
[Paulo Roberto de Oliveira Castro](https://github.com/prcastro)
[Pav K](https://github.com/kalaytan)
[payalbhatia](https://github.com/payalbhatia)
[Peter Parente](https://github.com/parente)
[Peter Reid](https://github.com/ReidWeb)
[Phil Elson](https://github.com/pelson)
[Phil Fenstermacher](https://github.com/pcfens)
[Philipp Kats](https://github.com/Casyfill)
[phpdistiller](https://github.com/phpdistiller)
[phxedmond](https://github.com/phxedmond)
[Piotr](https://github.com/karpikpl)
[Pouria Hadjibagheri](https://github.com/xenatisch)
[powerLeePlus](https://github.com/powerLeePlus)
[Pratik Lal](https://github.com/pratik-lal)
[pydeepak](https://github.com/Deepakdubey90)
[Qcy](https://github.com/chaoyue729)
[R. C. Thomas](https://github.com/rcthomas)
[raghav130593](https://github.com/raghav130593)
[Rahul Sharma](https://github.com/rahulswimmer)
[Rama Krishna Jinka](https://github.com/rjinka)
[RBALAJI5](https://github.com/RBALAJI5)
[rbq](https://github.com/rbq)
[Richard C Gerkin](https://github.com/rgerkin)
[Richard Darst](https://github.com/rkdarst)
[Richard Huntrods](https://github.com/huntrods)
[richyanicky](https://github.com/richyanicky)
[Rob Nagler](https://github.com/robnagler)
[robin](https://github.com/rollbackchen)
[robotsp](https://github.com/robotsp)
[rothwewi](https://github.com/rothwewi)
[rushikeshraut777](https://github.com/rushikeshraut777)
[Ryan](https://github.com/ev1lm0nk3y)
[Ryan Abernathey](https://github.com/rabernat)
[Ryan Lovett](https://github.com/ryanlovett)
[Ryan McGuire](https://github.com/EnigmaCurry)
[rzuidhof](https://github.com/rzuidhof)
[Saiprasad Balasubramanian](https://github.com/backtrackbaba)
[Sam Manzer](https://github.com/samuelmanzer)
[samRddhimat](https://github.com/samRddhimat)
[Santosh](https://github.com/sdandey)
[Saranya411](https://github.com/Saranya411)
[Scott Crooks](https://github.com/sc250024)
[sdementen](https://github.com/sdementen)
[SeaDude](https://github.com/SeaDude)
[SergeyK1](https://github.com/SergeyK1)
[Shannon](https://github.com/jingsong-liu)
[Shi Pengcheng](https://github.com/shipengcheng1230)
[shibbas](https://github.com/shibbas)
[Shinichi TAMURA](https://github.com/tmshn)
[Shiva1789](https://github.com/Shiva1789)
[sidebo](https://github.com/sidebo)
[Sigurður Baldursson](https://github.com/sigurdurb)
[Simon Li](https://github.com/manics)
[Sindre Gulseth](https://github.com/sgulseth)
[SivaMaplelabs](https://github.com/SivaMaplelabs)
[sjillidimudi](https://github.com/sjillidimudi)
[skruse](https://github.com/skruse)
[smoulderme](https://github.com/smoulderme)
[Solaris](https://github.com/SolarisYan)
[Spencer Ogden](https://github.com/spencerogden)
[sreekanthmg](https://github.com/sreekanthmg)
[Steven B](https://github.com/sblack4)
[Steven Silvester](https://github.com/blink1073)
[StudyQuant](https://github.com/studyquant)
[Subhash](https://github.com/signinred)
[Suchit](https://github.com/asuchit)
[summerswallow](https://github.com/summerswallow)
[summerswallow-whi](https://github.com/summerswallow-whi)
[Søren Fuglede Jørgensen](https://github.com/fuglede)
[Taewon](https://github.com/tkang007)
[Tania Allard](https://github.com/trallard)
[Taposh Dutta Roy](https://github.com/taposh)
[techie879](https://github.com/techie879)
[ThibTrip](https://github.com/ThibTrip)
[Thomas Mendoza](https://github.com/tgmachina)
[thomas-rabiller-azimut](https://github.com/thomas-rabiller-azimut)
[Thong Kuah](https://github.com/kuahyeow)
[thongnnguyen](https://github.com/thongnnguyen)
[Tim Crone](https://github.com/tjcrone)
[Tim Head](https://github.com/betatim)
[Timothy Griffiths](https://github.com/timgriffiths)
[Timothy Liu](https://github.com/tlkh)
[Todd Gamblin](https://github.com/tgamblin)
[Tom](https://github.com/T0mWz)
[Tomer Leibovich](https://github.com/tomerleib)
[tregin](https://github.com/tregin)
[Tren Huang](https://github.com/spiketren)
[Tuhina Chatterjee](https://github.com/tuhina2020)
[Tyler Gregory](https://github.com/01100010011001010110010101110000)
[Uday](https://github.com/udaynaik)
[Udit Arora](https://github.com/uditarora)
[Vasu Gaur](https://github.com/gaurcs)
[Victor Lopez](https://github.com/victorcete)
[Vidit Agarwal](https://github.com/IamViditAgarwal)
[VidJa](https://github.com/VidJa)
[Vincent Feng](https://github.com/iVincentFeng)
[vishal49naik49](https://github.com/vishal49naik49)
[Vivek](https://github.com/II-VSB-II)
[Vivek Rai](https://github.com/raivivek)
[vivekbiet](https://github.com/vivekbiet)
[Vlad-Mihai Sima](https://github.com/vladmihaisima)
[Volker Braun](https://github.com/vbraun)
[wangcong](https://github.com/congfairy)
[Wangsoo Kim](https://github.com/wangsookim)
[whositwhatnow](https://github.com/whositwhatnow)
[Will](https://github.com/xuwaters)
[Will Starms](https://github.com/vilhelmen)
[Willem Pienaar](https://github.com/woop)
[Xavier Lange](https://github.com/xrl)
[YborBorn](https://github.com/YborBorn)
[YizTian](https://github.com/tony-tian)
[Yoav Tzelnick](https://github.com/yoavtzelnick)
[YoongHM](https://github.com/yoonghm)
[yugushihuang](https://github.com/yugushihuang)
[Yuvi Panda](https://github.com/yuvipanda)
[Yuze Ma](https://github.com/bobmayuze)
[Zac Flamig](https://github.com/zflamig)
[Zach Day](https://github.com/zacharied)
[Zachary Sailer](https://github.com/Zsailer)
[Zafer Cesur](https://github.com/zcesur)
[zmkhazi](https://github.com/zmkhazi)
[zneudl](https://github.com/zneudl)
[田进](https://github.com/EndlessTJ)
[邱雨波](https://github.com/CraftHeart)
[高彦涛](https://github.com/gytlinux)


## [0.7.0](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/compare/v0.6...0.7.0) - [Alex Blackwell](https://en.wikipedia.org/wiki/Alex_Blackwell) - 2018-09-03

This release contains JupyterHub version 0.9.2, additional configuration options
and various bug fixes.

**IMPORTANT:** This upgrade will require your users to stop their work at some
point and have their pod restarted. You may want to give them a heads up ahead
of time or do it during nighttime if none are active then.

### Upgrading from v0.6

If you are running `v0.5` of the chart, you should upgrade to `v0.6` first
before upgrading to `0.7.0`. You can find out what version you are using by
running `helm list`.

Follow the steps below to upgrade from `v0.6` to `0.7.0`.

#### 1. (Optional) Ensure the hub's and users' data isn't lost

This step is optional, but a recommended safeguard when the hub's and users'
data is considered important. The changes makes the PersistentVolumes (PVs),
which represent storage (user data and hub database) remain even if the
PersistentVolumeClaims (PVCs) are deleted. The downside of this is that it
requires you to perform manual cleanup of PVs when you want to stop spending
money for the storage.

```sh
# The script is a saftey measure and patches your PersistentVolumes (PV) to
# not be garbage collected if the PersistentVolumeClaim (PVC) are deleted.
NAMESPACE=<YOUR-NAMESPACE>

# Ensure the hub's and users' data isn't lost
hub_and_user_pvs=($(kubectl get persistentvolumeclaim --no-headers --namespace $NAMESPACE | awk '{print $3}'))
for pv in ${hub_and_user_pvs[@]};
do
    kubectl patch persistentvolume $pv --patch '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
done
```

#### 2. Update Helm (v2.9.1+ required)

```sh
# Update helm
curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash

# Update tiller (on the cluster)
helm init --upgrade --service-account=tiller

# Verify the update
# NOTE: you may need to cancel and re-run the command, it should work within 30
#       seconds.
helm version
# VERIFY: Did it return both the client and server version?
# Client: &version.Version{SemVer:"v2.10.0", GitCommit:"9ad53aac42165a5fadc6c87be0dea6b115f93090", GitTreeState:"clean"}
# Server: &version.Version{SemVer:"v2.10.0", GitCommit:"9ad53aac42165a5fadc6c87be0dea6b115f93090", GitTreeState:"clean"}
```

#### 3. (Optional) Clean up pre-puller resources

The pre-puller component of v0.6 could leave leftover resources after it finished,
instead of cleaning up after itself.
This script removes the pre-puller resources created by v0.6.

```sh
# This script will delete resources that were meant to be temporary
# The bug that caused this is fixed in version 0.7.0 of the Helm chart
NAMESPACE=<YOUR-NAMESPACE>

resource_types="daemonset,serviceaccount,clusterrole,clusterrolebinding,job"
for bad_resource in $(kubectl get $resource_types --namespace $NAMESPACE | grep '/pre-pull' | awk '{print $1}');
do
    kubectl delete $bad_resource --namespace $NAMESPACE --now
done

kubectl delete $resource_types --selector hub.jupyter.org/deletable=true --namespace $NAMESPACE --now
```

#### 4. (Recommended) Clean up problematic revisions in your Helm release

This step is recommended due to bugs in Helm that could cause your JupyterHub
Helm chart installation (release) to get stuck in an invalid state.
The symptoms are often that `helm upgrade` commands fail with the reason that some resource does or doesn't exist.

```sh
# Look up the name of your Helm release (installation of a Helm chart)
helm list

# Store the name of the Helm release
RELEASE_NAME=<YOUR-RELEASE-NAME>

# Give yourself an overview of this release's revisions
helm history $RELEASE_NAME

# Check if you have multiple revisions in a DEPLOYED status (a bug), or if you
# have old PENDING_UPGRADES or FAILED revisions (may be problematic).
helm history $RELEASE_NAME | grep --extended-regexp "DEPLOYED|FAILED|PENDING_UPGRADE"

# If you have multiple revisions in DEPLOYED status, this script will clean up
# all configmaps except the latest with DEPLOYED status.
deployed_revisions=($(helm history $RELEASE_NAME | grep DEPLOYED | awk '{print $1}'))
for revision in ${deployed_revisions[@]::${#deployed_revisions[@]}-1};
do
    kubectl delete configmap $RELEASE_NAME.v$revision --namespace kube-system
done

# It seems plausible that upgrade failures could have to do with revisions
# having a PENDING_UPGRADE or FAILED status in the revision history. To delete
# them run the following command.
kubectl delete configmap --selector "NAME=$RELEASE_NAME,STATUS in (FAILED,PENDING_UPGRADE)" --namespace kube-system
```

#### 5. Perform the upgrade

**IMPORTANT:** Do not miss out on the `--force` flag!
`--force` is required due to changes in labelling of jupyterhub resources
in 0.7.
Helm cannot upgrade from the labelling scheme in 0.6 to that in 0.7 without `--force`, which deletes and recreates the deployments.

```sh
RELEASE_NAME=<YOUR-RELEASE-NAME>
NAMESPACE=<YOUR-NAMESPACE>

helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
helm repo update

# NOTE: We need the --force flag to allow recreation of resources that can't be
#       upgraded to the new state by a patch.
helm upgrade $RELEASE_NAME jupyterhub/jupyterhub --install \
    --force \
    --version=0.7.0 \
    --namespace=$NAMESPACE \
    --values config.yaml \
    --timeout 1800
```

#### 6. Manage active users

Active users with running pods must restart their pods. If they don't the next
time they attempt to access their server they may end up with `{“error”:
“invalid_redirect_uri”, “error_description”: “Invalid redirect URI”}`.

You have the power to force this to happen, but it will abort what they are
doing right now. If you want them to be able to do it in their own pace, you
could use the `/hub/admin` path and shut them down manually when they are done.

```
NAMESPACE=<YOUR-NAMESPACE>

# Inspect what users are currently running
kubectl get pod --selector component=singleuser-server --namespace $NAMESPACE

# Force all of them to shutdown their servers, and ensure the hub gets to
# realize that happened through a restart.
kubectl delete pod --selector component=singleuser-server --namespace $NAMESPACE
kubectl delete pod --selector component=hub --namespace $NAMESPACE
```

#### Troubleshooting - Cleanup of cluster

If things fail, you can try the following before installing the chart. If you
decide to take these steps, we recommend step 1 is taken first in order to not
loose data and that you ensure the old data is made available by the
troubleshooting step below.

```sh
RELEASE_NAME=<YOUR-RELEASE-NAME>

# WARNING: Deletes everything installed by the Helm chart!
# WARNING: If you have not changed the reclaim policy of the hub in step 1, the
#          hub never be able to remember anything about past users. Also note
#          that even if you have taken step 1, you must also make the PVs become
#          `Available` again before the hub starts up again.
# NOTE: This does not include user pods or user storage PVCs as they have been
#       indirectly created by KubeSpawner
helm delete $RELEASE_NAME --purge

# WARNING: Deletes everything within the namespace!
# WARNING: If you have not changed the reclaim policy of the hub and users in
#          step 1, the hub's stored information about the users and the user's
#          storage will be lost forever. Also note that even if you have taken
#          step 1, you must also make the hub and users PVs become `Available`
#          before the hub and users startup again.
kubectl delete namespace <YOUR-NAMESPACE>
```

If you took these steps and step 1, you should probably right now continue with
the next troubleshooting section about making `Released` PVs `Available` for
reuse.

#### Troubleshooting - Make `Released` PVs `Available` for reuse

If you followed step 1 and 2, you can after cleanup of a cluster reuse the old
hub's and users' storage if you do this step before you installs the Helm chart
again.

In more technical words: if you have deleted PVCs such as `hub-db-dir` or
`claim-anyusername`, their PVs will end in a `Released` state assuming they had
a `reclaimPolicy` set to `Retain`. To make use of these PVs again, we must make
them `Available` for the to future PVCs that needs a PV to bind to.

```sh
NAMESPACE=<YOUR-NAMESPACE>

# Ensure the hub's and users' PVs are made `Available` again
hub_and_user_pvs=($(kubectl get persistentvolume | grep -E "Released.+$NAMESPACE/(hub-db-dir|claim-)" | awk '{print $1}'))
for pv in ${hub_and_user_pvs[@]};
do
    kubectl patch persistentvolume $pv --patch '{"spec":{"claimRef":{"uid":null}}}}'
done

# Ensure you don't have any PVCs in the lost state
lost_pvcs=($(kubectl get persistentvolumeclaim --namespace $NAMESPACE | grep -E "(hub-db-dir|claim-).+Lost" | awk '{print $1}'))
for pvc in ${lost_pvcs[@]};
do
    echo kubectl delete persistentvolumeclaim $pvc --namespace $NAMESPACE
done
```

### Contributors

[A. Tan ](https://github.com/amanda-tan)
[Aaron Culich](https://github.com/aculich)
[abhismvit](https://github.com/abhismvit)
[AC](https://github.com/miramar-labs)
[AcademicAdmin](https://github.com/AcademicAdmin)
[Adam Grant](https://github.com/harmon)
[Adam Huffman](https://github.com/verdurin)
[Adam Thornton](https://github.com/athornton)
[Adam Tilghman](https://github.com/agt-ucsd)
[Adam-Origamiiris](https://github.com/Adam-Origamiiris)
[Afreen Rahman](https://github.com/Afreen04)
[agustaf](https://github.com/agustaf)
[agustiin](https://github.com/agustiin)
[aisensiy](https://github.com/aisensiy)
[Ajay Changulani](https://github.com/Ajay-Changulani)
[Akhil Lawrence](https://github.com/akhilputhiry)
[akkibatra](https://github.com/akkibatra)
[Alan King](https://github.com/kingaj12)
[Albert J. de Vera](https://github.com/ajdevera)
[Alejandro del Castillo](https://github.com/adelcast)
[Alejandro Gastón Alvarez](https://github.com/alealv)
[Aleksandr Blekh](https://github.com/ablekh)
[Alex Leith](https://github.com/alexgleith)
[Alex Marandon](https://github.com/amarandon)
[Alex Mellnik](https://github.com/amellnik)
[Alex Moore](https://github.com/Akmoore7)
[Alex Morreale](https://github.com/AlexMorreale)
[Alex Tasioulis](https://github.com/alex1x)
[Alexander](https://github.com/bzz)
[Alexander Hendorf](https://github.com/alanderex)
[Alexander Kruzhkov](https://github.com/YOxan)
[Alexander Morley](https://github.com/alexmorley)
[Alexander Schwartzberg](https://github.com/aeksco)
[Allen Downey](https://github.com/AllenDowney)
[AlphaSRE](https://github.com/AlphaSRE)
[Alramzey](https://github.com/Alramzey)
[amangarg96](https://github.com/amangarg96)
[Amirahmad Khordadi](https://github.com/khordadi)
[Amit Rathi](https://github.com/amit1rrr)
[Analect](https://github.com/Analect)
[anasos](https://github.com/anasos)
[Andre Celere](https://github.com/acelere)
[Andrea Abelli](https://github.com/abelliae)
[Andrea Turrini](https://github.com/andreat)
[Andrea Zonca](https://github.com/zonca)
[Andreas Heider](https://github.com/ah-)
[Andrew Berger](https://github.com/rueberger)
[Andrew Melo](https://github.com/PerilousApricot)
[andrewcheny](https://github.com/andrewcheny)
[András Tóth](https://github.com/tothandras)
[André Luiz Diniz](https://github.com/andrelu)
[Andy Berner](https://github.com/andybrnr)
[Andy Doddington](https://github.com/Andy-Doddington)
[angus evans](https://github.com/joingithubkor)
[Anirudh Vyas](https://github.com/AnirudhVyas)
[Ankit ](https://github.com/ankitml)
[Ankit Sharma](https://github.com/ankitksharma)
[ankit2894](https://github.com/ankit2894)
[Anthony Suen](https://github.com/anthonysuen)
[Anton Akhmerov](https://github.com/akhmerov)
[Antonino Ingargiola](https://github.com/tritemio)
[Antonio Serrano](https://github.com/AntonioSerrano)
[AranVinkItility](https://github.com/AranVinkItility)
[Arda Aytekin](https://github.com/aytekinar)
[Ariel Balter](https://github.com/abalter)
[Ariel Rokem](https://github.com/arokem)
[arkroop](https://github.com/arkroop)
[Arthur](https://github.com/konfiot)
[arthur](https://github.com/ppLorins)
[Arthur Koziel](https://github.com/arthurk)
[ArvinSiChuan](https://github.com/ArvinSiChuan)
[aseishas](https://github.com/aseishas)
[at-cchaloux](https://github.com/at-cchaloux)
[atullo2](https://github.com/atullo2)
[Bastian Greshake Tzovaras](https://github.com/gedankenstuecke)
[bbarney213](https://github.com/bbarney213)
[bbrauns](https://github.com/bbrauns)
[Ben Chuanlong Du](https://github.com/dclong)
[Benjamin Paz](https://github.com/bendavidpaz)
[Benoit Rospars](https://github.com/brospars)
[BerserkerTroll](https://github.com/BerserkerTroll)
[BhagyasriYella](https://github.com/BhagyasriYella)
[bhavybarca](https://github.com/bhavybarca)
[Birgetit](https://github.com/Birgetit)
[bitnik](https://github.com/bitnik)
[Borislav Aymaliev](https://github.com/aymaliev)
[Botty Dimanov](https://github.com/bottydim)
[Brad Skaggs](https://github.com/bskaggs)
[Brandon Sharitt](https://github.com/bsharitt)
[Brent](https://github.com/xuande)
[Brian E. Granger](https://github.com/ellisonbg)
[Brian Ray](https://github.com/brianray)
[Bruce Beauchamp](https://github.com/Prettyfield)
[Bruce Chiarelli](https://github.com/bccomm)
[Byă](https://github.com/hungbya)
[Camilla](https://github.com/Winterflower)
[Camilo Núñez Fernández](https://github.com/camilo-nunez)
[Cara](https://github.com/cara-a-k)
[carluri](https://github.com/carluri)
[Carol Willing](https://github.com/willingc)
[Caspian](https://github.com/Cas-pian)
[chack05](https://github.com/chack05)
[chang-zhijie](https://github.com/chang-zhijie)
[chaomaer](https://github.com/chaomaer)
[chaoyue729](https://github.com/chaoyue729)
[Charles Forelle](https://github.com/cforelle)
[chenyg0911](https://github.com/chenyg0911)
[Chester Li](https://github.com/chaoleili)
[Chia-liang Kao](https://github.com/clkao)
[Chico Venancio](https://github.com/chicocvenancio)
[Chris Fournier](https://github.com/cfournie)
[Chris Holdgraf](https://github.com/choldgraf)
[Chris Seal](https://github.com/cmseal)
[Chris Van Pelt](https://github.com/vanpelt)
[Christiaan Swanepoel](https://github.com/christiaanjs)
[Christian Alis](https://github.com/ianalis)
[Christian Hotz-Behofsits](https://github.com/inkrement)
[Christian Mesh](https://github.com/cam72cam)
[Christian Moscardi](https://github.com/cmoscardi)
[Christine Banek](https://github.com/cbanek)
[Christopher Hench](https://github.com/henchc)
[ckbhatt](https://github.com/ckbhatt)
[Claudius Mbemba](https://github.com/User1m)
[cloud-science](https://github.com/cloud-science)
[Cody Scott](https://github.com/Siecje)
[Cord](https://github.com/CordThomas)
[Cory Johns](https://github.com/johnsca)
[cqzlxl](https://github.com/cqzlxl)
[Craig Willis](https://github.com/craig-willis)
[Curtis Maves](https://github.com/cmaves)
[cyberquasar](https://github.com/cyberquasar)
[cybertony](https://github.com/cybertony)
[cyberyor](https://github.com/cyberyor)
[Daisuke Taniwaki](https://github.com/dtaniwaki)
[daleshsd](https://github.com/daleshsd)
[Dan Allan](https://github.com/danielballan)
[Dan Hoerst](https://github.com/DanHoerst)
[Dan Lidral-Porter](https://github.com/aperiodic)
[Daniel](https://github.com/daniel-ciocirlan)
[Daniel Morrison](https://github.com/draker42)
[danielmaitre](https://github.com/danielmaitre)
[danielrychel](https://github.com/danielrychel)
[Dario Romero](https://github.com/darioromero)
[darky2004](https://github.com/darky2004)
[DataVictorEngineer](https://github.com/DataVictorEngineer)
[Dave Aitken](https://github.com/actionshrimp)
[Dave Hirschfeld](https://github.com/dhirschfeld)
[David Bath](https://github.com/davidbath)
[David Doherty](https://github.com/dado0583)
[David Kügler](https://github.com/dkuegler)
[David Maxson](https://github.com/scnerd)
[David Napier](https://github.com/dnapier)
[David Pérez Comendador](https://github.com/perez1987)
[David Pérez-Suárez](https://github.com/dpshelio)
[David Sanftenberg](https://github.com/dbsanfte)
[Davide](https://github.com/davidedelvento)
[deep-42-thought](https://github.com/deep-42-thought)
[Deleted user](https://github.com/ghost)
[DerekHeldtWerle](https://github.com/DerekHeldtWerle)
[Dhawal Patel](https://github.com/dhawal55)
[disimone](https://github.com/disimone)
[DmitrII Gerasimenko](https://github.com/kidig)
[Dmitry Mishin](https://github.com/dimm0)
[Dominic Suciu](https://github.com/domsooch)
[Don Kelly](https://github.com/karfai)
[Doug Holt](https://github.com/dholt)
[Dragos Cojocari](https://github.com/dragos-cojocari)
[dturaev](https://github.com/dturaev)
[Dwight Townsend](https://github.com/townsenddw)
[Dylan Lentini](https://github.com/dyltini)
[Eamon Keane](https://github.com/EamonKeane)
[Eddy Elbrink](https://github.com/elbrinke)
[Emmanuel Gomez](https://github.com/emmanuel)
[Enol Fernández](https://github.com/enolfc)
[epoch1970](https://github.com/epoch1970)
[Eric Charles](https://github.com/echarles)
[Erik Sundell](https://github.com/consideRatio)
[Ermakov Petr](https://github.com/ermakovpetr)
[ernestmartinez](https://github.com/ernestmartinez)
[EtienneDesticourt](https://github.com/EtienneDesticourt)
[Evan](https://github.com/eexe1)
[Evan Van Dam](https://github.com/evandam)
[Evert Rol](https://github.com/evertrol)
[eylenth](https://github.com/eylenth)
[Ezequiel Gioia](https://github.com/eze1981)
[fahadabbas91](https://github.com/fahadabbas91)
[Faras Sadek](https://github.com/farassadek)
[forbxy](https://github.com/forbxy)
[Francisco Zamora-Martinez](https://github.com/pakozm)
[FU Zhipeng](https://github.com/gavin971)
[Fyodor](https://github.com/lgg)
[Félix-Antoine Fortin](https://github.com/cmd-ntrf)
[G YASHASVI](https://github.com/iamyashasvi)
[Gaetan Semet](https://github.com/gsemet)
[Gaëtan Lehmann](https://github.com/glehmann)
[gbrahmi](https://github.com/gbrahmi)
[George Jose](https://github.com/G2Jose)
[Gerben Welter](https://github.com/GerbenWelter)
[Gerhard Burger](https://github.com/burgerga)
[GladysNalvarte](https://github.com/GladysNalvarte)
[Glen A Knight](https://github.com/glenak1911)
[Graham Dumpleton](https://github.com/GrahamDumpleton)
[grant-guo](https://github.com/grant-guo)
[GRC](https://github.com/gaorongchao)
[Guillaume EB](https://github.com/guillaumeeb)
[guimou](https://github.com/guimou)
[Guo Zhang](https://github.com/Guo-Zhang)
[gweis](https://github.com/gweis)
[Hagen Hoferichter](https://github.com/h4gen)
[hanbeibei](https://github.com/hanbeibei)
[hani1814](https://github.com/hani1814)
[Hans Petter Bieker](https://github.com/hpbieker)
[happytest143](https://github.com/happytest143)
[Hassan Mudassir](https://github.com/hassanmudassir-rzt)
[Helder Rodrigues](https://github.com/HelderGualberto)
[hemantasingh](https://github.com/hemantasingh)
[Henddher Pedroza](https://github.com/wjehenddher)
[hjclub123](https://github.com/hjclub123)
[huhuhang](https://github.com/huhuhang)
[Hunter Jackson](https://github.com/hunterjackson)
[Ian](https://github.com/yfc845)
[Indrajeet Singh](https://github.com/itsindra)
[ironv](https://github.com/ironv)
[IssacPan](https://github.com/IssacPan)
[Ivan Grbavac](https://github.com/grbinho)
[J Forde](https://github.com/jzf2101)
[J Gerard](https://github.com/jgerardsimcock)
[Jacob Tomlinson](https://github.com/jacobtomlinson)
[James Curtin](https://github.com/jamescurtin)
[James Davidheiser](https://github.com/jdavidheiser)
[James Londal](https://github.com/jlondal)
[James Veitch](https://github.com/darth-veitcher)
[Jan Kalo](https://github.com/JanKalo)
[Jason Kuruzovich](https://github.com/jkuruzovich)
[Jason Williams](https://github.com/JasonJWilliamsNY)
[jason4zhu](https://github.com/jason4zhu)
[javin-gn](https://github.com/javin-gn)
[Jeremie Vallee](https://github.com/jeremievallee)
[Jeremy Lewi](https://github.com/jlewi)
[Jeremy Tuloup](https://github.com/jtpio)
[Jerry Schuman](https://github.com/pingthings)
[Jesse Cai](https://github.com/jcaip)
[Jesse Kinkead](https://github.com/jkinkead)
[Jesse Zhang](https://github.com/EmptyCrown)
[Jessica Wong](https://github.com/jessawong)
[Jim Basney](https://github.com/jbasney)
[Jim Hendricks](https://github.com/jhendric98)
[Jiri Kuncar](https://github.com/jirikuncar)
[jlsimms](https://github.com/jlsimms)
[jm2004](https://github.com/jm2004)
[Joakim](https://github.com/Sefriol)
[JocelynDelalande](https://github.com/JocelynDelalande)
[Joe Hamman](https://github.com/jhamman)
[Joel Pfaff](https://github.com/joelpfaff)
[John Kaltenbach](https://github.com/jkbach)
[John Readey](https://github.com/jreadey)
[johnbotsis](https://github.com/johnbotsis)
[johnkpark](https://github.com/johnkpark)
[johnpaulantony](https://github.com/johnpaulantony)
[Jonas Adler](https://github.com/adler-j)
[Jonathan](https://github.com/yocode)
[Jonathan Brant](https://github.com/jbrant)
[Jonathan Wheeler](https://github.com/jondoesntgit)
[jonny86](https://github.com/jonny86)
[Joost W. Döbken](https://github.com/JWDobken)
[Jose Manuel Monsalve Diaz](https://github.com/josemonsalve2)
[Josh Barnes](https://github.com/jcb91)
[Josh Temple](https://github.com/joshtemple)
[João Barreto](https://github.com/JoaoBarreto)
[jpolchlo](https://github.com/jpolchlo)
[JPUnD](https://github.com/JPUnD)
[Juan Cabanela](https://github.com/JuanCab)
[Julien Chastang](https://github.com/julienchastang)
[Jurian Kuyvenhoven](https://github.com/JurianK)
[Justin Holmes](https://github.com/sherl0cks)
[Justin Moen](https://github.com/superquest)
[justkar4u](https://github.com/justkar4u)
[JYang25](https://github.com/JYang25)
[Jürgen Hermann](https://github.com/jhermann)
[kakzhetak](https://github.com/kakzhetak)
[kaliko](https://github.com/mxjeff)
[Kam Kasravi](https://github.com/kkasravi)
[Kannan Kumar](https://github.com/kannankumar)
[karthikpitchaimani](https://github.com/karthikpitchaimani)
[Kenneth Lyons](https://github.com/ixjlyons)
[Kevin P. Fleming](https://github.com/kpfleming)
[kevkid](https://github.com/kevkid)
[Kirill Dubovikov](https://github.com/kdubovikov)
[Knarfux](https://github.com/fbessou)
[Ko Ohashi](https://github.com/kouohhashi)
[krinsman](https://github.com/krinsman)
[KrisL](https://github.com/gixita)
[Kristiyan](https://github.com/katsar0v)
[lambertjosh](https://github.com/lambertjosh)
[Lars Biemans](https://github.com/lbiemans)
[Leo Gallucci](https://github.com/elgalu)
[leolurunhe](https://github.com/leolurunhe)
[Leopold Talirz](https://github.com/ltalirz)
[LeoPsidom](https://github.com/leopsidom)
[lfzyx](https://github.com/lfzyx)
[lgc019](https://github.com/lgc019)
[Lifubang](https://github.com/lifubang)
[liusztc09](https://github.com/liusztc09)
[liuzhliang](https://github.com/liuzhliang)
[llancellotti](https://github.com/llancellotti)
[lmerli84](https://github.com/lmerli84)
[loginoff](https://github.com/loginoff)
[Louis Garman](https://github.com/leg100)
[Luca De Feo](https://github.com/defeo)
[Luca Grazioli](https://github.com/Luke035)
[Lucas Durand](https://github.com/lucasdurand)
[Lucas Kushner](https://github.com/lphk92)
[Lukasz Lempart](https://github.com/wookasz)
[Lukasz Tracewski](https://github.com/tracek)
[Lutz Behnke](https://github.com/cypherfox)
[M Pacer](https://github.com/mpacer)
[Maciej Sawicki](https://github.com/viroos)
[madsi1m](https://github.com/madsi1m)
[mak-aravind](https://github.com/mak-aravind)
[Malin Aandahl](https://github.com/MalinAan)
[Manjukb](https://github.com/Manjukb)
[Marc BUFFAT](https://github.com/mbuffat)
[marciocourense](https://github.com/marciocourense)
[Marco Pleines](https://github.com/MarcoMeter)
[Marcus Hunger](https://github.com/fnordian)
[Marcus Levine](https://github.com/marcusianlevine)
[Mario Campos](https://github.com/mario-campos)
[Marius van Niekerk](https://github.com/mariusvniekerk)
[Mark Mirmelstein](https://github.com/markm42)
[marmaduke woodman](https://github.com/maedoc)
[Martin Forde](https://github.com/mforde84)
[Martín Anzorena](https://github.com/martjanz)
[maryamdev](https://github.com/maryamdev)
[Mas](https://github.com/airtime166)
[mascarom](https://github.com/mascarom)
[Mathew Blonc](https://github.com/blonc)
[Matt Hansen](https://github.com/hansen-m)
[Matteo Ipri](https://github.com/matteoipri)
[matthdan](https://github.com/matthdan)
[Matthew Bray](https://github.com/mattjbray)
[Matthew Rocklin](https://github.com/mrocklin)
[Matthias Bussonnier](https://github.com/Carreau)
[Matthias Klan](https://github.com/mklan)
[mattvw](https://github.com/mattvw)
[Max Joseph](https://github.com/mbjoseph)
[Maxim Moinat](https://github.com/MaximMoinat)
[mdivk](https://github.com/mdivk)
[Mereep](https://github.com/Mereep)
[merlin1608](https://github.com/merlin1608)
[Micah](https://github.com/micahscopes)
[Micah Smith](https://github.com/micahjsmith)
[Michael Huttner](https://github.com/mhuttner)
[Michael Milligan](https://github.com/mbmilligan)
[Michael Ransley](https://github.com/mransley)
[michec81](https://github.com/michec81)
[Michele Bertasi](https://github.com/mbrt)
[Miguel Caballer](https://github.com/micafer)
[Mike Hamer](https://github.com/mikehamer)
[Min RK](https://github.com/minrk)
[MincingWords](https://github.com/MincingWords)
[MisterZ](https://github.com/david-dumas)
[mohanamurali7](https://github.com/mohanamurali7)
[Mohit](https://github.com/Mohitsharma44)
[Monica Dessole](https://github.com/mdessole)
[moskiGithub](https://github.com/moskiGithub)
[mrkjones1979](https://github.com/mrkjones1979)
[mzilinski](https://github.com/mzilinski)
[n3f](https://github.com/n3f)
[Naeem Rashid](https://github.com/naeemkhan12)
[Naineel Shah](https://github.com/naineel)
[NaizEra](https://github.com/NaizEra)
[nauhpc](https://github.com/nauhpc)
[ndiy](https://github.com/ndiy)
[Neelanshu92](https://github.com/Neelanshu92)
[Nehemiah I. Dacres](https://github.com/dacresni)
[Neth Six](https://github.com/nethsix)
[ngokhoa96](https://github.com/ngokhoa96)
[Nick Brown](https://github.com/uptownnickbrown)
[Nickolaus D. Saint](https://github.com/NickolausDS)
[nickray](https://github.com/nickray)
[Nico Bellack](https://github.com/bellackn)
[Nicolas M. Thiéry](https://github.com/nthiery)
[Nikolay Dandanov](https://github.com/ndandanov)
[Nikolay Voronchikhin](https://github.com/nikolayvoronchikhin)
[niveau0](https://github.com/niveau0)
[Norman Gray](https://github.com/nxg)
[ogre0403](https://github.com/ogre0403)
[Ola Tarkowska](https://github.com/ola-t)
[oneklc](https://github.com/oneklc)
[OpenThings](https://github.com/openthings)
[ormskirk77](https://github.com/ormskirk77)
[P.J. Little](https://github.com/pjlittle)
[Pat W](https://github.com/patwoowong)
[Patafix](https://github.com/Patafix)
[Paul Adams](https://github.com/p5a0u9l)
[Paul Laskowski](https://github.com/paul-laskowski)
[Paul Mazzuca](https://github.com/PaulMazzuca)
[Paulo Roberto de Oliveira Castro](https://github.com/prcastro)
[Pav K](https://github.com/kalaytan)
[pedrovgp](https://github.com/pedrovgp)
[pekosro](https://github.com/pekosro)
[Peter Majchrak](https://github.com/petoknm)
[pgarapon](https://github.com/pgarapon)
[Phil Fenstermacher](https://github.com/pcfens)
[philippschw](https://github.com/philippschw)
[Phuong Cao](https://github.com/pmcao)
[picca](https://github.com/picca)
[Pierre Accorsi](https://github.com/paccorsi)
[Pinakibiswasdevops](https://github.com/Pinakibiswasdevops)
[Pius Nyakoojo](https://github.com/PiusNyakoojo)
[pjamason](https://github.com/pjamason)
[Pouria Hadjibagheri](https://github.com/xenatisch)
[Prabhu Kasinathan](https://github.com/prabhu1984)
[Pramod Rizal](https://github.com/prkriz)
[Pranay Hasan Yerra](https://github.com/pranayhasan)
[Prateek](https://github.com/prateekpg2455)
[prateek2408](https://github.com/prateek2408)
[Prerak Mody](https://github.com/prerakmody)
[Przybyszo](https://github.com/Przybyszo)
[psnx](https://github.com/psnx)
[pydo](https://github.com/yonghuming)
[pyjones1](https://github.com/pyjones1)
[R. C. Thomas](https://github.com/rcthomas)
[Rachidramadan1990](https://github.com/Rachidramadan1990)
[radudragusin](https://github.com/radudragusin)
[Rafael Ladislau](https://github.com/rafael-ladislau)
[Rafael Mejia](https://github.com/rafmesal)
[raghu20ram](https://github.com/raghu20ram)
[raja](https://github.com/raksja)
[Ramin](https://github.com/transfluxus)
[Ranjit](https://github.com/ranjitiyer)
[Raphael Nestler](https://github.com/rnestler)
[RaRam](https://github.com/RaRam)
[Raviraju Vysyaraju](https://github.com/ravirajuv)
[reddyvenu](https://github.com/reddyvenu)
[Ricardo Rocha](https://github.com/rochaporto)
[Rich Signell](https://github.com/rsignell-usgs)
[Richard Caunt](https://github.com/psyvision)
[Richard Darst](https://github.com/rkdarst)
[Richard England](https://github.com/renglandatsmu)
[Richard Ting](https://github.com/richardtin)
[Rizwan Saeed](https://github.com/rizwansaeed)
[Rob](https://github.com/rtruxal)
[Robert Casey](https://github.com/rcasey-iris)
[Robert Drysdale](https://github.com/robdrysdale)
[Robert Jiang ](https://github.com/robert-juang)
[Robert Schroll](https://github.com/rschroll)
[robin](https://github.com/rollbackchen)
[Robin](https://github.com/robmarkcole)
[Robin Scheibler](https://github.com/fakufaku)
[roemer2201](https://github.com/roemer2201)
[Rok Roškar](https://github.com/rokroskar)
[Roman Gorodeckij](https://github.com/holms)
[roversne](https://github.com/roversne)
[Roy Wedge](https://github.com/rwedge)
[Royi](https://github.com/RoyiAvital)
[Rui Zhang](https://github.com/zhangruiskyline)
[Ruslan Usifov](https://github.com/tantra35)
[Ryan Abernathey](https://github.com/rabernat)
[Ryan Lovett](https://github.com/ryanlovett)
[rydeng](https://github.com/rydeng)
[sabarnwa](https://github.com/sabarnwa)
[sabyasm](https://github.com/sabyasm)
[sadanand25](https://github.com/sadanand25)
[Sam Manzer](https://github.com/samuelmanzer)
[Sambaiah Kilaru](https://github.com/ksambaiah)
[samy](https://github.com/goforthanddie)
[Sangram Gaikwad](https://github.com/sangramga)
[sanjaydatasciencedojo](https://github.com/sanjaydatasciencedojo)
[Sanmati Jain](https://github.com/jainsanmati)
[saransha](https://github.com/saransha)
[Saranya411](https://github.com/Saranya411)
[sarath145p](https://github.com/sarath145p)
[Satendra Kumar](https://github.com/satendrakumar)
[saurav maharjan](https://github.com/saurssauravjs)
[saurs saurav](https://github.com/isaurssaurav)
[SB](https://github.com/SofianeB)
[sbailey-auro](https://github.com/sbailey-auro)
[Scott Crooks](https://github.com/sc250024)
[Scott Sanderson](https://github.com/ssanderson)
[SeaDude](https://github.com/SeaDude)
[semanticyongjia](https://github.com/semanticyongjia)
[serlina](https://github.com/serlina)
[Seshadri Ramaswami](https://github.com/sesh1989)
[shalan7](https://github.com/shalan7)
[Shana Matthews](https://github.com/shanamatthews)
[Shannon](https://github.com/jingsong-liu)
[Shantanu Singh](https://github.com/shantanusingh16)
[Shengxin Huang](https://github.com/FukoH)
[shilpam11](https://github.com/shilpam11)
[Shiva Prasanth](https://github.com/cedric05)
[shreddd](https://github.com/shreddd)
[Shuo YU](https://github.com/collinwo)
[Sigurður Baldursson](https://github.com/sigurdurb)
[Simon Li](https://github.com/manics)
[Sirawit Pongnakintr](https://github.com/s6007589)
[SivaMaplelabs](https://github.com/SivaMaplelabs)
[smiller5678](https://github.com/smiller5678)
[srican](https://github.com/srican)
[srini_b](https://github.com/Srinivasb0)
[Stanislav Nazmutdinov](https://github.com/PrintScr)
[stczwd](https://github.com/stczwd)
[Stefano Nicotri](https://github.com/stefanonicotri)
[Stefano Taschini](https://github.com/taschini)
[Stephanie Gott](https://github.com/gottsme)
[Stephen Lecrenski](https://github.com/slecrenski)
[Stephen Pascoe](https://github.com/stephenpascoe)
[Stephen Sackett](https://github.com/ssackett)
[Steven Silvester](https://github.com/blink1073)
[Stéphane Pouyllau](https://github.com/spouyllau)
[sudheer0553](https://github.com/sudheer0553)
[Sugu Sougoumarane](https://github.com/sougou)
[Suman Addanki](https://github.com/suman724)
[summerswallow](https://github.com/summerswallow)
[summerswallow-whi](https://github.com/summerswallow-whi)
[sundeepChandhoke](https://github.com/sundeepChandhoke)
[Sunip Mukherjee](https://github.com/sunipkmukherjee)
[svzdvdoptum](https://github.com/svzdvdoptum)
[swgong](https://github.com/sw-gong)
[Sylvain Desroziers](https://github.com/sdesrozis)
[syutbai](https://github.com/syutbai)
[T. George](https://github.com/tgeorgeux)
[tankeryang](https://github.com/tankeryang)
[TapasSpark](https://github.com/TapasSpark)
[Tassos Sarbanes](https://github.com/sarbanes)
[teddy Kossoko](https://github.com/KOSSOKO)
[tgamal](https://github.com/tgamal)
[Thomas Ashish Cherian](https://github.com/PandaWhoCodes)
[Thomas Kluyver](https://github.com/takluyver)
[Thomas Mendoza](https://github.com/tgmachina)
[thongnnguyen](https://github.com/thongnnguyen)
[Thoralf Gutierrez](https://github.com/thoralf-gutierrez)
[Tim Crone](https://github.com/tjcrone)
[Tim Freund](https://github.com/timfreund)
[Tim Head](https://github.com/betatim)
[Tim Kennell Jr.](https://github.com/tikenn)
[Tim Klever](https://github.com/tklever)
[Tim Shi](https://github.com/strin)
[TimKreuzer](https://github.com/TimKreuzer)
[Tirthankar Chakravarty](https://github.com/tchakravarty)
[titansmc](https://github.com/titansmc)
[Tobias Morville](https://github.com/TMorville)
[tobiaskaestner](https://github.com/tobiaskaestner)
[Tom Davidson](https://github.com/tjd2002)
[Tom Kwong](https://github.com/tk3369)
[Tom O'Connor](https://github.com/ichasepucks)
[Tomas Barton](https://github.com/deric)
[Tommaso Fabbri](https://github.com/tfabbri)
[Tyler Erickson](https://github.com/tylere)
[tzujan](https://github.com/tzujan)
[uday2002](https://github.com/uday2002)
[Umar Sikander](https://github.com/umar-sik)
[UsDAnDreS](https://github.com/UsDAnDreS)
[Vaclav Pavlin](https://github.com/vpavlin)
[Varun M S](https://github.com/meranamvarun)
[Victor Paraschiv](https://github.com/vicpara)
[vishwesh5](https://github.com/vishwesh5)
[Vladimir Kozhukalov](https://github.com/kozhukalov)
[vpvijay87](https://github.com/vpvijay87)
[W.](https://github.com/ManifoldFR)
[wangaiwudi](https://github.com/wangaiwudi)
[Wei Hao](https://github.com/whao)
[weih1121](https://github.com/weih1121)
[weimindong2016](https://github.com/weimindong2016)
[whitebluecloud](https://github.com/whitebluecloud)
[whositwhatnow](https://github.com/whositwhatnow)
[will](https://github.com/zsluedem)
[Will Starms](https://github.com/vilhelmen)
[William H](https://github.com/sylus)
[William Hosford](https://github.com/whosford)
[wtsyang](https://github.com/wtsyang)
[XIAHUALOU](https://github.com/XIAHUALOU)
[xuhuijun](https://github.com/xuhuijun)
[Y-L-18](https://github.com/Y-L-18)
[yee379](https://github.com/yee379)
[yeisonseverinopucv](https://github.com/yeisonseverinopucv)
[Yiding](https://github.com/wydwww)
[Yifan Li](https://github.com/Eagles2F)
[yougha54](https://github.com/yougha54)
[Youri Noel Nelson](https://github.com/ynnelson)
[yuandongfang](https://github.com/yuandongfang)
[Yueqi Wang](https://github.com/yueqiw)
[yugushihuang](https://github.com/yugushihuang)
[Yuhi Ishikura](https://github.com/uphy)
[Yuval Kalugny](https://github.com/kalugny)
[Yuvi Panda](https://github.com/yuvipanda)
[Zac Flamig](https://github.com/zflamig)
[Zachary Sailer](https://github.com/Zsailer)
[Zachary Zhao](https://github.com/zacharyzhao)
[ZachGlassman](https://github.com/ZachGlassman)
[zaf](https://github.com/zafeirakopoulos)
[Zafer Cesur](https://github.com/zcesur)
[zearaujo07](https://github.com/zearaujo07)
[Zeb Nicholls](https://github.com/znicholls)
[Zelphir Kaltstahl](https://github.com/ZelphirKaltstahl)
[ZenRay](https://github.com/ZenRay)
[zero](https://github.com/zero-88)
[zeusal](https://github.com/zeusal)
[Zhongyi](https://github.com/zhongyiio)
[Zhou (Joe) Yuan](https://github.com/yuanzhou)
[ziedbouf](https://github.com/ziedbouf)
[zlshi](https://github.com/zlshi)
[zmkhazi](https://github.com/zmkhazi)
[Zoltan Fedor](https://github.com/zoltan-fedor)
[zyc](https://github.com/499244188)
[Øystein Efterdal](https://github.com/oefterdal)
[孙永乐](https://github.com/cattei)
[张旭](https://github.com/zhangxu999)
[武晨光](https://github.com/mission-young)
[陈镇秋](https://github.com/ChenZhenQiu)

## [0.6] - [Ellyse Perry](https://en.wikipedia.org/wiki/Ellyse_Perry) - 2017-01-29

This release is primarily focused on better support
for Autoscaling, Microsoft Azure support & better
default security. There are also a number of bug fixes
and configurability improvements!

### Breaking changes

#### Pre-puller configuration
In prior versions (v0.5), if you wanted to disable the pre-puller,
you would use:

```yaml
prePuller:
  enabled: false
```

Now, to disable the pre-puller, you need to use:

```yaml
prePuller:
  hook:
    enabled: false
```

See the [pre-puller docs](http://zero-to-jupyterhub.readthedocs.io/en/latest/advanced.html#pre-pulling-images-for-faster-startup) for more info!

### Upgrading from 0.5

This release does not require any special steps to upgrade from v0.5. See the [upgrade documentation](https://zero-to-jupyterhub.readthedocs.io/en/latest/upgrading.html)
for general upgrading steps.

If you are running v0.4 of the chart, you should upgrade to v0.5 first
before upgrading to v0.6. You can find out what version you are using
by running `helm list`.

#### Troubleshooting

If your helm upgrade fails due to the error `no Ingress with the name "jupyterhub-internal" found`,
you may be experiencing a [helm bug](https://github.com/kubernetes/helm/issues/3275). To work
around this, run `kubectl --namespace=<YOUR-NAMESPACE> delete ingress jupyterhub-internal` and
re-run the `helm upgrade` command. Note that this will cause a short unavailability of your hub
over HTTPS, which will resume normal availability once the deployment upgrade completes.

### New Features

#### More secure by default

z2jh is more secure by default with 0.6. We now
block access to cloud security metadata endpoints by
default.

See the [security documentation](http://zero-to-jupyterhub.readthedocs.io/en/latest/security.html) for more details. It has seen a number of improvements, and we recommend
you read through it!

#### Autoscaling improvements

Some cloud providers support the [kubernetes node autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler),
which can add / remove nodes depending on how much your
cluster is being used. In this release, we made a few
changes to let z2jh interact better with the autoscaler!

- Configure z2jh to ['pack' your users](http://zero-to-jupyterhub.readthedocs.io/en/latest/advanced.html#picking-a-scheduler-strategy)
  onto nodes, rather than 'spread' them across nodes.
- A ['continuous' pre-puller](http://zero-to-jupyterhub.readthedocs.io/en/latest/advanced.html?highlight=prepull#pre-pulling-images-for-faster-startup)
  that allows user images to
  be pulled on new nodes easily, leading to faster startup
  times for users on new nodes. ([link])
- Hub and Proxy pod will not be disrupted by autoscaler,
  by using [PodDisruptionBudget](https://kubernetes.io/docs/tasks/run-application/configure-pdb/)s. The Hub & Proxy will also stick
  together if possible, thus minimizing the number of nodes
  that can not be downsized by the autoscaler.

There is more work to be done for good autoscaling support,
but this is a good start!

#### Better Azure support

Azure's new managed Kubernetes service ([AKS](https://docs.microsoft.com/en-us/azure/aks/)) is much
better supported by this version!

- We have much better documentation on using z2jh with Azure!
- We rewrote our pre-puller so it works on Azure (previously it did not)

Azure AKS is still in preview mode, so be aware of that
before using it in any production workloads!

See the [setting up Kubernetes on Microsoft AKS](http://zero-to-jupyterhub.readthedocs.io/en/latest/create-k8s-cluster.html#setting-up-kubernetes-on-microsoft-azure-container-service-aks) section for more information.

#### Better configurability

We now have better documentation and bug fixes for configurability!

- `extraConfig` can be a dictionary instead of just a
  string. This helps when you have to split your `config.yaml`
  into multiple files for complex deployments
- How user storage works by default is [better documented](http://zero-to-jupyterhub.readthedocs.io/en/latest/user-storage.html)
- Reading config in `extraConfig` from `extraConfigMap` now actually works!
- You can configure the URL that users are directed to after they log in.
  This allows [defaulting users to JupyterLab](http://zero-to-jupyterhub.readthedocs.io/en/latest/user-environment.html#use-jupyterlab-by-default)
- You can pre-pull multiple images now, for custom configuration that needs multiple images
- [Better instructions](http://zero-to-jupyterhub.readthedocs.io/en/latest/user-environment.html#pre-populating-user-s-home-directory-with-files)
  on pre-populating your user's filesystem using [nbgitpuller](https://github.com/data-8/nbgitpuller)

### [Ellyse Perry](https://en.wikipedia.org/wiki/Ellyse_Perry)

_(excerpt from https://www.cricket.com.au/players/ellyse-perry/1aMxKNyEOUiJqhq7N5Tlwg)_

Arguably the best athlete in Australia, Ellyse Perry’s profile continues to rise
with the dual cricket and soccer international having played World Cups for both sports.

Perry became the youngest Australian ever to play senior international cricket when
she made her debut in the second ODI of the Rose Bowl Series in Darwin in July 2007
before her 17th birthday.

She went on to make her domestic debut in the 2007-08 Women’s National Cricket League
season, taking 2-29 from 10 overs in her first match.

Since her national debut, Perry has become a regular fixture for the Southern Stars,
playing in the 2009 ICC Women’s World Cup and the ICC Women’s World Twenty20 in the same year.

Leading Australia’s bowling attack, Perry played a crucial role in the ICC Women’s
World Twenty20 Final in the West Indies in 2010.

The match came down to the wire, with New Zealand requiring five runs off the last
ball to claim the title. Under immense pressure, Perry bowled the final ball of the
tournament, which New Zealand’s Sophie Devine struck straight off the bat.

The talented footballer stuck out her boot to deflect the ball to Lisa Sthalekar at
mid-on, securing the trophy for Australia. Perry’s figures of 3-18 in the final saw
her take home the Player of the Match award.

Perry featured prominently in Australia's three-peat of World T20 victories,
selected for the Team of the Tournament in 2012 and 2014.

She was named [ICC Female Cricketer of the Year](http://www.abc.net.au/news/2017-12-22/ellyse-perry-named-iccs-womens-cricketer-of-the-year/9280538) in 2017.

### Contributors

This release wouldn't have been possible without the wonderful contributors
to the [zero-to-jupyterhub](https://github.com/jupyterhub/zero-to-jupyterhub-k8s),
and [KubeSpawner](https://github.com/jupyterhub/kubespawner) repos.
We'd like to thank everyone who contributed in any form - Issues, commenting
on issues, PRs and reviews since the last Zero to JupyterHub release.

In alphabetical order,

- [Aaron Culich](https://github.com/aculich)
- [Anirudh Ramanathan](https://github.com/foxish)
- [Antoine Dao](https://github.com/twanito)
- [BerserkerTroll](https://github.com/BerserkerTroll)
- [Carol Willing](https://github.com/willingc)
- [Chris Holdgraf](https://github.com/choldgraf)
- [Christian Mesh](https://github.com/cam72cam)
- [Erik Sundell](https://github.com/consideRatio)
- [forbxy](https://github.com/forbxy)
- [Graham Dumpleton](https://github.com/GrahamDumpleton)
- [gweis](https://github.com/gweis)
- [Ian Allison](https://github.com/ianabc)
- [Jason Kuruzovich](https://github.com/jkuruzovich)
- [Jesse Kinkead](https://github.com/jkinkead)
- [madanam1](https://github.com/madanam1)
- [Matthew Rocklin](https://github.com/mrocklin)
- [Matthias Bussonnier](https://github.com/Carreau)
- [Min RK](https://github.com/minrk)
- [Ryan Lovett](https://github.com/ryanlovett)
- [Simon Li](https://github.com/manics)
- [Steve Buckingham](https://github.com/stevebuckingham)
- [Steven Normore](https://github.com/snormore)
- [Tim Head](https://github.com/betatim)
- [Yuvi Panda](https://github.com/yuvipanda)
- [ZachGlassman](https://github.com/ZachGlassman)

## [0.5] - [Hamid Hassan](http://www.espncricinfo.com/afghanistan/content/player/311427.html) - 2017-12-05

JupyterHub 0.8, HTTPS & scalability.

### Upgrading from 0.4

See the [upgrade documentation](https://zero-to-jupyterhub.readthedocs.io/en/latest/upgrading.html) for upgrade steps.

### New Features

#### JupyterHub 0.8

JupyterHub 0.8 is full of new features - see [CHANGELOG](https://jupyterhub.readthedocs.io/en/0.8.1/changelog.html#id1)
for more details. Specific features made to benefit this chart are:

1. No more 'too many redirects' errors at scale.
2. Lots of performance improvements, we now know we can handle up to 4k active users
3. Concurrent spawn limits (set via `hub.concurrentSpawnLimit`) can be used to limit the concurrent
   number of users who can try to launch on the hub at any given time. This can be
   tuned to avoid crashes when hundreds of users try to launch at the same time. It gives
   them a friendly error message + asks them to try later, rather than spinning forever.
4. Active Server limit (set via `hub.activeServerLimit`) can be used to limit the
   total number of active users that can be using the hub at any given time. This allows
   admins to control the size of their clusters.
5. Memory limits & guarantees (set via `singleuser.memory`) can now contain fractional
   units. So you can say `0.5G` instead of having to use `512M`.

And lots more!

#### Much easier HTTPS

It is our responsibility as software authors to make it very easy for admins to set up
HTTPS for their users. v0.5 makes this much easier than v0.4. You can find the new
instructions [here](http://zero-to-jupyterhub.readthedocs.io/en/latest/extending-jupyterhub.html#setting-up-https) and
they are much simpler!

You can also now use your own HTTPS certificates & keys rather than using Let's Encrypt.

#### More authenticators supported

The following new authentication providers have been added:

1. GitLab
2. CILogon
3. Globus

You can also set up a whitelist of users by adding to the list in `auth.whitelist.users`.


#### Easier customization of `jupyterhub_config.py`

You can always put extra snippets of `jupyterhub_config.py` configuration in
`hub.extraConfig`. Now you can also add extra environment variables to the hub
in `hub.extraEnv` and extra configmap items via `hub.extraConfigMap`. ConfigMap
items can be arbitrary YAML, and you can read them via the `get_config` function in
your `hub.extraConfig`. This makes it cleaner to customize the hub's config in
ways that's not yet possible with config.yaml.

#### Hub Services support

You can also add [external JupyterHub Services](http://jupyterhub.readthedocs.io/en/latest/reference/services.html)
by adding them to `hub.services`. Note that you are still responsible for actually
running the service somewhere (perhaps as a deployment object).

#### More customization options for user server environments

More options have been added under `singleuser` to help you customize the environment
that the user is spawned in. You can change the uid / gid of the user with `singleuser.uid`
and `singleuser.fsGid`, mount extra volumes with `singleuser.storage.extraVolumes` &
`singleuser.storage.extraVolumeMounts` and provide extra environment variables with
`singleuser.extraEnv`.

### Hamid Hassan

Hamid Hassan is a fast bowler who currently plays for the Afghanistan National
Cricket Team. With nicknames ranging from
["Afghanistan's David Beckham"](https://www.rferl.org/a/interview-afghan-cricketer-living-the-dream/24752618.html) to
["Rambo"](http://www.nzherald.co.nz/nz/news/article.cfm?c_id=1&objectid=11413633),
he is considered by many to be Afghanistan's first Cricket Superhero. Currently
known for fast (145km/h+) deliveries, cartwheeling celebrations, war painted
face and having had to flee Afghanistan as a child to escape from war. He [says](http://www.nzherald.co.nz/nz/news/article.cfm?c_id=1&objectid=11413633)
he plays because "We are ambassadors for our country and we want to show the
world that Afghanistan is not like people recognise it by terrorists and these
things. We want them to know that we have a lot of talent as well"

### Contributors

This release wouldn't have been possible without the wonderful contributors
to the [zero-to-jupyterhub](https://github.com/jupyterhub/zero-to-jupyterhub-k8s),
[JupyterHub](https://github.com/jupyterhub/jupyterhub), [KubeSpawner](https://github.com/jupyterhub/kubespawner)
and [OAuthenticator](http://github.com/jupyterhub/oauthenticator) repos.
We'd like to thank everyone who contributed in any form - Issues, commenting
on issues, PRs and reviews since the last Zero to JupyterHub release.

In alphabetical order,

- [Aaron Culich](https://github.com/aculich)
- [abeche](https://github.com/alexxxxx)
- [Abhinandan Dubey](https://github.com/alivcor)
- [Adam Thornton](https://github.com/athornton)
- [Adrin Jalali](https://github.com/adrinjalali)
- [Aidis Stukas](https://github.com/aidiss)
- [Aleksandr Blekh](https://github.com/ablekh)
- [Alessandro Vozza](https://github.com/ams0)
- [Alex Hilson](https://github.com/alexhilson)
- [Analect](https://github.com/Analect)
- [Andrea Zonca](https://github.com/zonca)
- [Andreas](https://github.com/Jibbow)
- [Andrew Berger](https://github.com/rueberger)
- [András Tóth](https://github.com/tothandras)
- [angrylandmammal](https://github.com/angrylandmammal)
- [Anirudh Ramanathan](https://github.com/foxish)
- [Antonino Ingargiola](https://github.com/tritemio)
- [apachipa](https://github.com/apachipa)
- [Ariel Rokem](https://github.com/arokem)
- [astrodb](https://github.com/astrodb)
- [Ayushi Agarwal](https://github.com/ayushiagarwal)
- [batchku](https://github.com/batchku)
- [bbhopesh](https://github.com/bbhopesh)
- [Bill Major](https://github.com/rwmajor2)
- [Brad Svee](https://github.com/sveesible)
- [Brian E. Granger](https://github.com/ellisonbg)
- [BrianVanEtten](https://github.com/BrianVanEtten)
- [calz1](https://github.com/calz1)
- [Camilo Núñez Fernández](https://github.com/camilo-nunez)
- [Carol Willing](https://github.com/willingc)
- [Chris Holdgraf](https://github.com/choldgraf)
- [Christian Barra](https://github.com/barrachri)
- [Christian Moscardi](https://github.com/cmoscardi)
- [Christophe Lecointe](https://github.com/christophelec)
- [Christopher Hench](https://github.com/henchc)
- [Christopher Ostrouchov](https://github.com/costrouc)
- [ckbhatt](https://github.com/ckbhatt)
- [Cody Scott](https://github.com/Siecje)
- [Colin Goldberg](https://github.com/colingoldberg)
- [daleshsd](https://github.com/daleshsd)
- [danroliver](https://github.com/danroliver)
- [Dave Hirschfeld](https://github.com/dhirschfeld)
- [David](https://github.com/davidXire)
- [Davide](https://github.com/davidedelvento)
- [deisi](https://github.com/deisi)
- [Dennis Pfisterer](https://github.com/pfisterer)
- [Dennis Verspuij](https://github.com/dennisverspuij)
- [Diogo](https://github.com/dmvieira)
- [dmceballosg](https://github.com/dmceballosg)
- [Dominic Follett-Smith](https://github.com/dominicfollett)
- [Doug Blank](https://github.com/dsblank)
- [Enol Fernández](https://github.com/enolfc)
- [Erik Sundell](https://github.com/consideRatio)
- [erolosty](https://github.com/erolosty)
- [FalseProtagonist](https://github.com/FalseProtagonist)
- [fmilano1975](https://github.com/fmilano1975)
- [Forrest Collman](https://github.com/fcollman)
- [Fred Mitchell](https://github.com/fm75)
- [Gil Forsyth](https://github.com/gforsyth)
- [Goutham Balaraman](https://github.com/gouthambs)
- [gryslik](https://github.com/gryslik)
- [gweis](https://github.com/gweis)
- [haasad](https://github.com/haasad)
- [hani1814](https://github.com/hani1814)
- [Hanno Rein](https://github.com/hannorein)
- [harschware](https://github.com/harschware)
- [Ian Allison](https://github.com/ianabc)
- [Isaiah Leonard](https://github.com/ihleonard-c3)
- [J Forde](https://github.com/jzf2101)
- [Jacob Tomlinson](https://github.com/jacobtomlinson)
- [jai11](https://github.com/jai11)
- [jbmarcille](https://github.com/jbmarcille)
- [Jeet Shah](https://github.com/iamjeet)
- [Jeroen Vuurens](https://github.com/jeroenvuurens)
- [Jessica B. Hamrick](https://github.com/jhamrick)
- [jiamicu](https://github.com/jiamicu)
- [jiancai1992](https://github.com/jiancai1992)
- [jm2004](https://github.com/jm2004)
- [joefromct](https://github.com/joefromct)
- [John Haley](https://github.com/johnhaley81)
- [jonny86](https://github.com/jonny86)
- [Joshua Milas](https://github.com/DeepHorizons)
- [JoshuaC3](https://github.com/JoshuaC3)
- [João Vítor Amaro](https://github.com/joaoamaro70)
- [Justin Ray Vrooman](https://github.com/vroomanj)
- [Keith Callenberg](https://github.com/keithcallenberg)
- [KenB](https://github.com/y2kbowen)
- [Kenneth Lyons](https://github.com/ixjlyons)
- [krak3nnn](https://github.com/krak3nnn)
- [Kristiyan](https://github.com/katsar0v)
- [Kuisong Tong](https://github.com/ktong)
- [kuldeepyadav](https://github.com/kuldeepyadav)
- [Kyle Kelley](https://github.com/rgbkrk)
- [lcfcefyn](https://github.com/lcfcefyn)
- [Leo Gallucci](https://github.com/elgalu)
- [lesiano](https://github.com/lesiano)
- [Lorena A. Barba](https://github.com/labarba)
- [lrob](https://github.com/lrob)
- [Lukasz Tracewski](https://github.com/tracek)
- [Mahesh Vangala](https://github.com/vangalamaheshh)
- [Marco Sirabella](https://github.com/mjsir911)
- [marcostrullato](https://github.com/marcostrullato)
- [Marius van Niekerk](https://github.com/mariusvniekerk)
- [MarkusTeufelberger](https://github.com/MarkusTeufelberger)
- [Matt Koken](https://github.com/patback66)
- [Matteo Cerutti](https://github.com/m4ce)
- [Matthias Bussonnier](https://github.com/Carreau)
- [Michael Li](https://github.com/tianhuil)
- [Mike](https://github.com/s-t-e-a-l-t-h)
- [MikeM](https://github.com/mmacny)
- [Min RK](https://github.com/minrk)
- [misolietavec](https://github.com/misolietavec)
- [Moiz Sajid](https://github.com/moizsajid)
- [Morgan Jones](https://github.com/mogthesprog)
- [mraky](https://github.com/mraky)
- [mrinmoyprasad](https://github.com/mrinmoyprasad)
- [nabriis](https://github.com/nabriis)
- [Nickolaus D. Saint](https://github.com/NickolausDS)
- [Nocturnal316](https://github.com/Nocturnal316)
- [Olivier Cloarec](https://github.com/ocloarec)
- [Pedro Henriques dos Santos Teixeira](https://github.com/pedroteixeira)
- [Pranay Hasan Yerra](https://github.com/pranayhasan)
- [prof-schacht](https://github.com/prof-schacht)
- [Puneet Jindal](https://github.com/puneetjindal)
- [R. C. Thomas](https://github.com/rcthomas)
- [ramonberger](https://github.com/ramonberger)
- [Randy Guthrie](https://github.com/randguth)
- [Richard Caunt](https://github.com/psyvision)
- [richmoore1962](https://github.com/richmoore1962)
- [Rishika Sinha](https://github.com/rsinha25)
- [Robert Wlodarczyk](https://github.com/SimplicityGuy)
- [Ruben Orduz](https://github.com/rdodev)
- [Ryan Lovett](https://github.com/ryanlovett)
- [Ryan Wang](https://github.com/rwangr)
- [rydeng](https://github.com/rydeng)
- [SarunasG](https://github.com/SarunasG)
- [Saul Shanabrook](https://github.com/saulshanabrook)
- [Scott Calabrese Barton](https://github.com/scbarton)
- [Scott Sanderson](https://github.com/ssanderson)
- [Simon Li](https://github.com/manics)
- [Stefano Nicotri](https://github.com/stefanonicotri)
- [surma-lodur](https://github.com/surma-lodur)
- [Sven Mayer](https://github.com/SamyStyle)
- [swigicat](https://github.com/swigicat)
- [SY_Wang](https://github.com/kiwi0217)
- [Thomas Kluyver](https://github.com/takluyver)
- [Thomas Mendoza](https://github.com/tgmachina)
- [Tim Head](https://github.com/betatim)
- [toddpfaff](https://github.com/toddpfaff)
- [Tom O'Connor](https://github.com/ichasepucks)
- [toncek87](https://github.com/toncek87)
- [Tony ](https://github.com/Montereytony)
- [Travis Sturzl](https://github.com/tsturzl)
- [Tyler Cloutier](https://github.com/cloutiertyler)
- [uday2002](https://github.com/uday2002)
- [Udita Bose](https://github.com/uditabose)
- [uttamkumar123](https://github.com/uttamkumar123)
- [will](https://github.com/zsluedem)
- [Wilmer Ramirez](https://github.com/will17cr)
- [xgdgsc](https://github.com/xgdgsc)
- [Yan Zhao](https://github.com/yan130)
- [Yinan Li](https://github.com/liyinan926)
- [yoryicopo](https://github.com/yoryicopo)
- [Yu-Hang "Maxin" Tang](https://github.com/yhtang)
- [Yuvi Panda](https://github.com/yuvipanda)
- [Zachary Ogren](https://github.com/zogren)
- [Zhenwen Zhang](https://github.com/zhangzhenwen)
- [Zoltan Fedor](https://github.com/zoltan-fedor)


## [0.4] - [Akram](#akram) - 2017-06-23

Stability, HTTPS & breaking changes.

### Installation and upgrades

We **recommend** that you delete prior versions of the package and install the
latest version. If you are very familiar with Kubernetes, you can upgrade from
an older version, but we still suggest deleting and recreating your
installation.

### Breaking changes

* The **name of a user pod** and a **dynamically created home directory [PVC (PersistentVolumeClaim)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)** no longer include
  the `userid` in them by default. If you are using dynamic PVCs for `home`
  directories (which is the default), you will need to *manually rename* these
  directories before upgrading.
  Otherwise, new PVCs will be created, and users might freak out when viewing the newly created directory and think that their home directory appears empty.

  See [PR #56](https://github.com/jupyterhub/kubespawner/pull/56) on
  what needs to change.

* A **[StorageClass](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#storageclasses)**
  is no longer created by default. This shouldn't affect most new installs,
  since most cloud provider installations have a default (as of Kubernetes 1.6).
  If you are using an older version of Kubernetes, the easiest thing to do is to
  upgrade to a newer version. If not, you can create a StorageClass manually
  and everything should continue to work.

* `token.proxy` is removed. Use **`proxy.secretToken`** instead.
  If your `config.yaml` contains something that looks like the following:

  ```yaml
  token:
      proxy: <some-secret>
  ```

  you should change that to:

  ```yaml
  proxy:
      secretToken: <some-secret>
  ```

### Added

* Added **GitHub Authentication support**, thanks to [Jason Kuruzovich](https://github.com/jkuruzovich).
* Added **[Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) support**!
  If your cluster already has Ingress support (with automatic Let's Encrypt support, perhaps),
  you can easily use that now.
* We now add a **label** to user pods / PVCs with their usernames.
* Support using a **static PVC** for user `home` directories or for the hub database. This makes this release usable
  with clusters where you only have one NFS share that must be used for the whole hub.
* **PostgreSQL** is now a supported hub database backend provider.
* You can set annotations & labels on the **proxy-public service** now.

### Changed

* We now use the official [configurable http proxy](http://github.com/jupyterhub/configurable-http-proxy)
  (CHP) as the proxy, rather than the unofficial
  [nchp](https://github.com/yuvipanda/jupyterhub-nginx-chp). This should be a
  no-op (or require no changes) for the most part. JupyterHub errors might
  display a nicer error page.
* The version of KubeSpawner uses the official Kubernetes
  [python client](https://github.com/kubernetes-incubator/client-python/) rather
  than [pycurl](http://pycurl.io/). This helps with scalability a little.

### Removed

* The deprecated `createNamespace` parameter no longer works, alongside the
  deprecated `name` parameter. You probably weren't using these anyway - they
  were kept only for backwards compatibility with very early versions.

### Contributors

This release made possible by the awesome work of the following contributors
(in alphabetical order):

* [Analect](https://github.com/analect)
* [Carol Willing](https://github.com/willingc)
* [Jason Kuruzovich](https://github.com/jkuruzovich)
* [Min RK](https://github.com/minrk/)
* [Yuvi Panda](https://github.com/yuvipanda/)

<3

### Akram

[Wasim Akram](https://en.wikipedia.org/wiki/Wasim_Akram) (وسیم اکرم) is considered by many to be
the greatest pace bowler of all time and a founder of the fine art of
[reverse swing bowling](https://en.wikipedia.org/wiki/Swing_bowling#Reverse_swing).

## 0.3

### [0.3.1] - 2017-05-19

KubeSpawner updates. [Release note](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/releases/tag/v0.3.1)

### [0.3] - 2017-05-15

Deployer UX fixes. [Release note](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/releases/tag/v0.3)

## [0.2] - 2017-05-01

Minor cleanups and features. [Release note](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/releases/tag/v0.2)

## [0.1] - 2017-04-10

Initial Public Release. [Release note](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/releases/tag/v0.1)
