Tips and Snippets
=================

This is a page to collect a few particularly useful patterns and snippets
that help you interact with your Kubernetes cluster and JupyterHub.
If there's something that you think is generic enough (and not obvious enough)
to be added to this page, please feel free to make a PR!

``kubectl`` autocompletion
--------------------------

Kubernetes has a helper script that allows you to auto-complete commands
and references to objects when using ``kubectl``. This lets you
:kbd:`TAB`-complete and saves a lot of time.

`Here are the instructions to install kubectl auto-completion <https://kubernetes.io/docs/tasks/tools/install-kubectl/#enabling-shell-autocompletion>`_.

``helm`` autocompletion
-----------------------

Helm also has an auto-completion script that lets you :kbd:`TAB`-complete
your commands when using Helm.

`Here are the instructions to install helm auto-completion <https://helm.sh/docs/helm/helm_completion/>`_.


Managing ``kubectl`` contexts
-----------------------------

Oftentimes people manage multiple Kubernetes deployments at the same time.
``kubectl`` handles this with the idea of "contexts", which specify which
Kubernetes deployment you are referring to when you type ``kubectl get XXX``.

To see a list of contexts currently available to you, use the following
command:

.. code-block:: bash

    kubectl config get-contexts

This will list all of your Kubernetes contexts. You can select a particular
context by entering:

.. code-block:: bash

    kubectl config use-context <CONTEXT-NAME>


Specifying a default namespace for a context
--------------------------------------------

If you grow tired of typing ``namespace=XXX`` each time you type a kubernetes
command, here's a snippet that will allow you set a default namespace for
a given Kubernetes context:

.. code-block:: bash

    kubectl config set-context $(kubectl config current-context) \
	    --namespace=<YOUR-NAMESPACE>

The above command will only apply to the currently active context, and will
allow you to skip the ``--namespace=`` part of your commands for this context.


Using labels and selectors with ``kubectl``
-------------------------------------------

Sometimes it's useful to select an entire class of Kubernetes objects rather
than referring to them by their name. You can attach an arbitrary set of
labels to a Kubernetes object, and can then refer to those labels when
searching with ``kubectl``.

To search based on a label value, use the ``-l`` or ``--selector=`` keyword
arguments. For example, JupyterHub creates a specific subset of labels for all
user pods. You can search for all user pods with the following label query:

.. code-block:: bash

    kubectl --namespace=<YOUR-NAMESPACE> get pod \
	    -l "component=singleuser-server"

For more information, see the `Kubernetes labels and selectors page <https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/>`_.

Asking for a more verbose or structured output
----------------------------------------------

Sometimes the information that's in the default output for ``kubectl get <XXX>``
is not enough for your needs, or isn't structured the way you'd like. We
recommend looking into the different Kubernetes output options, which can be
modified like so:

.. code-block:: bash

    kubectl --namespace=<NAMESPACE> get pod -o <json|yaml|wide|name...>

You can find more information on what kinds of output you can generate at
`the kubectl information page <https://kubernetes.io/docs/reference/kubectl/overview/>`_.
(click and search for the text "Output Options")
