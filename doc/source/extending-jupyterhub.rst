.. _extending-jupyterhub:

Extending your JupyterHub setup
===============================

The helm chart used to install JupyterHub has a lot of options for you to tweak.
This page lists some of the most common changes.

.. _apply-config-changes:

Applying configuration changes
------------------------------

The general method is:

1. Make a change to the ``config.yaml``
2. Run a helm upgrade:

     .. code-block:: bash

        helm upgrade <YOUR_RELEASE_NAME> jupyterhub/jupyterhub --version=v0.4 -f config.yaml

   Where ``<YOUR_RELEASE_NAME>`` is the parameter you passed to ``--name`` when
   `installing jupyterhub <setup-jupyterhub.html#install-jupyterhub>`_ with
   ``helm install``. If you don't remember it, you can probably find it by doing
   ``helm list``.
3. Wait for the upgrade to finish, and make sure that when you do
   ``kubectl --namespace=<YOUR_NAMESPACE> get pod`` the hub and proxy pods are
   in ``Ready`` state. Your configuration change has been applied!

Authenticating with OAuth2
--------------------------

JupyterHub's `oauthenticator <https://github.com/jupyterhub/oauthenticator>`_
has support for enabling your users to authenticate via a third-party OAuth
provider, including GitHub, Google, and CILogon.

Follow the service-specific instructions linked on the
`oauthenticator repository <https://github.com/jupyterhub/oauthenticator>`_
to generate your JupyterHub instance's OAuth2 client ID and client secret. Then
declare the values in the helm chart (``config.yaml``).

Here are example configurations for two common authentication services. Note
that in each case, you need to get the authentication credential information
before you can configure the helmchart for authentication.

**Google**

For more information see the full example of Google OAuth2 in the next section.

.. code-block:: yaml

    auth:
      type: google
      google:
        clientId: "yourlongclientidstring.apps.googleusercontent.com"
        clientSecret: "adifferentlongstring"
        callbackUrl: "http://<your_jupyterhub_host>/hub/oauth_callback"
        hostedDomain: "youruniversity.edu"
        loginService: "Your University"

**GitHub**

.. code-block:: yaml

      auth:
        type: github
        github:
          clientId: "y0urg1thubc1ient1d"
          clientSecret: "an0ther1ongs3cretstr1ng"
          callbackUrl: "http://<your_jupyterhub_host>/hub/oauth_callback"

Full Example of Google OAuth2
-----------------------------

If your institution is a `G Suite customer <https://gsuite.google.com>`_ that
integrates with Google services such as Gmail, Calendar, and Drive, you can
authenticate users to your JupyterHub using Google for authentication.

.. note::
       Google requires that you specify a fully qualified domain name for your
       hub rather than an IP address.

1. Log in to the `Google API Console <https://console.developers.google.com>`_.

2. Select a project > Create a project... and set 'Project name'. This is a
   short term that is only displayed in the console. If you have already
   created a project you may skip this step.

3. Type "Credentials" in the search field at the top and click to access the
   Credentials API.

4. Click "Create credentials", then "OAuth client ID". Choose
   "Application type" > "Web application".

5. Enter a name for your JupyterHub instance. You can give it a descriptive
   name or set it to be the hub's hostname.

6. Set "Authorized JavaScript origins" to be your hub's URL.

7. Set "Authorized redirect URIs" to be your hub's URL followed by
   "/hub/oauth_callback". For example, http://example.com/hub/oauth_callback.

8. When you click "Create", the console will generate and display a Client ID
   and Client Secret. Save these values.

9. Type "consent screen" in the search field at the top and click to access the
   OAuth consent screen. Here you will customize what your users see when they
   login to your JupyterHub instance for the first time. Click Save when you
   are done.

10. In your helm chart, create a stanza that contains these OAuth fields:

.. code-block:: bash

    auth:
      type: google
      google:
        clientId: "yourlongclientidstring.apps.googleusercontent.com"
        clientSecret: "adifferentlongstring"
        callbackUrl: "http://<your_jupyterhub_host>/hub/oauth_callback"
        hostedDomain: "youruniversity.edu"
        loginService: "Your University"

The 'callbackUrl' key is set to the authorized redirect URI you specified
earlier. Set 'hostedDomain' to your institution's domain name. The value of
'loginService' is a descriptive term for your institution that reminds your
users which account they are using to login.

Expanding and contracting the size of your cluster
--------------------------------------------------

You can easily scale up or down your cluster's size to meet usage demand or to
save cost when the cluster is not being used. Use the ``resize`` command and
provide a new cluster size (i.e. number of nodes) as a command line option
``--size``:

.. code-block:: bash

   gcloud container clusters resize \
                <YOUR-CLUSTER-NAME> \
                --size <NEW-SIZE> \
                --zone <YOUR-CLUSTER-ZONE>

To display the cluster's name, zone, or current size, use the command:

.. code-block:: bash

   gcloud container clusters list

After resizing the cluster, it may take a couple of minutes for the new cluster
size to be reported back as the service is adding or removing nodes.

.. note::

   When organizing and running a workshop, resizing a cluster gives you a way
   to save cost and prepare JupyterHub before the event. For example:

   - **One week before the workshop:** You can create the cluster, set
     everything up, and then resize the cluster to zero nodes to save cost.
   - **On the day of the workshop:** You can scale the cluster up to a suitable
     size for the workshop. This workflow also helps you avoid scrambling on
     the workshop day to set up the cluster and JupyterHub.
   - **After the workshop:** The cluster can be deleted.
