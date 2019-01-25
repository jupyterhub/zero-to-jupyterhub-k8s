# Changelog
Here you can find upgrade changes in between releases and upgrade instructions.

Releases are named after famous [Cricket](https://en.wikipedia.org/wiki/Cricket) players.



## [Unreleased](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/compare/0.8.0..master)

### Breaking changes
- Github organisation OAuth: `auth.github.org_whitelist` has been renamed to `auth.github.orgWhitelist`

### New Features


## [0.8.0](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/compare/0.7.0..0.8.0) - [Richie Benaud](https://en.wikipedia.org/wiki/Richie_Benaud) - 2019-01-24

This release contains JupyterHub version 0.9.4. It requires Kubernetes >= 1.11 and Helm >= 2.11.0.
See [the Helm Chart repository](https://github.com/jupyterhub/helm-chart#versions-coupled-to-each-chart-release) for
a list of relevant dependencies for all Helm Chart versions.

It contains new features, additional configuration options, and bug fixes.

### Upgrading from 0.7

TODO: Instructions

#### Troubleshooting

TODO: Instructions

### New Features

#### TODO: ITEM 1


### [Richie Benaud](https://www.cricket.com.au/players/richie-benaud/gvp5xSjUp0q6Qd7IM5TbCg)

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


### Contributors

This release wouldn't have been possible without the wonderful contributors
to the [zero-to-jupyterhub](https://github.com/jupyterhub/zero-to-jupyterhub-k8s),
and [KubeSpawner](https://github.com/jupyterhub/kubespawner) repos.
We'd like to thank everyone who contributed in any form - Issues, commenting
on issues, PRs and reviews since the last Zero to JupyterHub release.

<TODO: list of contributors>

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

## Support

If you need support, reach out to us on
[gitter](https://gitter.im/jupyterhub/jupyterhub) or open an
[issue](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues).


[Unreleased]: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/compare/v0.6...HEAD
[0.6]: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/compare/v0.5...v0.6
[0.5]: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/compare/v0.4...v0.5
[0.4]: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/compare/v0.3.1...v0.4
[0.3.1]: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/compare/v0.3...v0.3.1
[0.3]: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/compare/v0.2...v0.3
[0.2]: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/compare/v0.1...v0.2
[0.1]: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/releases/tag/v0.1
