# Changelog

## [Unreleased]

## Releases

Releases are now named after famous [Cricket](https://en.wikipedia.org/wiki/Cricket) players.

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

## Support

If you need support, reach out to us on
[gitter](https://gitter.im/jupyterhub/jupyterhub) or open an
[issue](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues).


[Unreleased]: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/compare/v0.4...HEAD
[0.4]: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/compare/v0.3...v0.3.1
[0.3]: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/compare/v0.2...v0.3
[0.2]: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/compare/v0.1...v0.2
[0.1]: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/releases/tag/v0.1
