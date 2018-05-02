Tips and command snippets
=========================

This is a page to collect a few particularly useful patterns and snippets
that help you interact with your Kubernetes cluster and JupyterHub.
If there's something that you think is generic enough (and not obvious enough)
to be added to this page, please feel free to make a PR!

``kubectl`` autocompletion
--------------------------

Kubernetes has a helper script that allows you to auto-complete commands
and references to objects when using ``kubectl``. This lets you
``<TAB>``-complete and saves a lot of time.

`Here are the instructions to install kubectl auto-completion <https://kubernetes.io/docs/tasks/tools/install-kubectl/#enabling-shell-autocompletion>`_.

``helm`` autocompletion
-----------------------

Helm also has an auto-completion script that lets you ``<TAB>``-complete
your commands when using Helm.

`Here are the instructions to install helm auto-completion <https://docs.helm.sh/helm/#helm-completion>`_.


Managing ``kubectl`` contexts
-----------------------------

Oftentimes people manage multiple Kubernetes deployments at the same time.
``kubectl`` handles this with the idea of "contexts", which specify which
kubernetes deployment you are referring to when you type ``kubectl get XXX``.

To see a list of contexts currently available to you, use the following
command:

    kubectl config get-contexts

This will list all of your Kubernetes contexts. You can select a particular
context by entering:

    kubectl config use-context <CONTEXT-NAME>


Specifying a default namespace for a context
--------------------------------------------

If you grow tired of typing ``namespace=XXX`` each time you type a kubernetes
command, here's a snippet that will allow you set a _default_ namespace for
a given Kubernetes context:

    kubectl config set-context $(kubectl config current-context) --namespace=<YOUR-NAMESPACE>

The above command will only apply to the _currently active context_, and will
allow you to skip the ``--namespace=`` part of your commands for this context.


Using labels and selectors with ``kubectl``
-------------------------------------------

Sometimes it's useful to select an entire _class_ of Kubernetes objects rather
than referring to them by their name. You can attach an arbitrary set of
_labels_ to a Kubernetes object, and can then refer to those labels when
searching with ``kubectl``.

To search based on a label value, use the ``-l`` or ``--label`` keyword
arguments. For example, JupyterHub creates a specific subset of labels for all
user pods. You can search for all user pods with the following label query:

    kubectl --namespace=<YOUR-NAMESPACE> get pod -l "component=singleuser-server"
