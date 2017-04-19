Glossary
========

A partial glossary of terms used in this guide. We try to keep the definition as succint & relevant
as possible, and provide links to learn more details.

`kubernetes <https://kubernetes.io/>`_
  Kubernetes is an open-source system for automating deployment, scaling,
  and management of containerized applications. 

cluster
  A Kubernetes cluster, running on a cloud provider or bare metal. It can contain multiple
  JupyterHub releases (and other software) in many namespaces.

`namespace <https://kubernetes.io/docs/admin/namespaces/>`_
  A logical grouping of various objects (user pods, proxy, services, disks) in a kubernetes
  cluster. Usually you deploy one JupyterHub per namespace. They are also units of access
  control and quota.

user pod
  A container running Jupyter Notebook, spawned by a JupyterHub for a particular user. It is
  running a singleuser image and might be attached to persistent storage.

user image
  A docker image that sets up the environment (libraries, base operating system, conda/virtualenv,
  packages, etc) for the user pod. You can build your own or use something others have built.

`helm <https://helm.sh/>`_
  Helm helps define, install and upgrade complex applications (like JupyterHub) on a kubernetes
  cluster.

`chart <https://github.com/kubernetes/helm/blob/master/docs/charts.md>`_
  A chart is a package used by helm to install a complex application on a kubernetes cluster. There
  is a list of `community maintained charts <https://github.com/kubernetes/charts/tree/master/stable>`_
  available, and we use a chart to install and upgrade JupyterHub in this guide.

release
  EXPLAIN HELM RELEASES HERE, and how they relate to chart, namespace and cluster.

`authenticator <http://jupyterhub.readthedocs.io/en/stable/authenticators.html>`_
  The way in which users are authenticated to log into JupyterHub. There are many authenticators
  available, like GitHub, Google, MediaWiki, Dummy (anyone can log in), etc.

persistent storage
  A filesystem attached to a user pod that allows the user to store notebooks / files that persist
  across multiple logins.

culler
  A separate process that stops the user pods of users who have not been active in a configured interval.

admin user
  A user who can access the JupyterHub admin panel. They can start/stop user pods, and potentially
  access their notebooks.
