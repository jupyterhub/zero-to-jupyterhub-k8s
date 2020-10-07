.. _authentication:

Authentication
==============

Authentication allows you to control who has access to your JupyterHub deployment.
There are many options available to you in controlling authentication, many of
which are described below.

Authenticating with OAuth2
--------------------------

JupyterHub's `oauthenticator <https://github.com/jupyterhub/oauthenticator>`_
has support for enabling your users to authenticate via a third-party OAuth
provider, including GitHub, Google, and CILogon.

Follow the service-specific instructions linked on the
`oauthenticator repository <https://github.com/jupyterhub/oauthenticator>`_
to generate your JupyterHub instance's OAuth2 client ID and client secret. Then
declare the values in the helm chart (``config.yaml``).

Here are example configurations for common authentication services. Note
that in each case, you need to get the authentication credential information
before you can configure the helm chart for authentication.

GitHub
^^^^^^

GitHub is the largest hosting service for git repositories. It is free to create an account
at GitHub, and relatively straightforward to set up OAuth credentials so that
users can authenticate with their GitHub username/password.

To create OAuth credentials on GitHub, follow these steps:

* Click your profile picture -> settings -> developer settings
* Make sure you're on the "OAuth Apps" tab, then click "New OAuth App"
* Fill out the forms (you'll need your hub address) and generate your ID/Secret.

To enable GitHub authentication, add the following to your `config.yml`:

.. code-block:: yaml

   auth:
     type: github
     github:
       clientId: "y0urg1thubc1ient1d"
       clientSecret: "an0ther1ongs3cretstr1ng"
       callbackUrl: "http://<your_jupyterhub_host>/hub/oauth_callback"

Make sure that the `callbackUrl` matches the one you set in GitHub.

Giving access to individual GitHub users
++++++++++++++++++++++++++++++++++++++++
The configuration above will allow *any* GitHub user to access your JupyterHub.
You can restrict access to a white-list of GitHub users by adding the following
to your configuration.

.. code-block:: yaml

   auth:
     type: github
     admin:
       access: true
       users:
         - user1
         # ...
     whitelist:
       users:
         - user2
         # ...

In this case, `user1` will have *admin* access and `user2` will have regular
access to your JupyterHub.


Giving access to organizations on GitHub
++++++++++++++++++++++++++++++++++++++++
You can also restrict access to all of the members of one or more GitHub
organizations. To do so, see the configuration below.

.. code-block:: yaml

   auth:
     type: github
     github:
       # ...
       orgWhitelist:
         - "SomeOrgName"
     scopes:
       - "read:user"

``auth.scopes`` can take other values as described in the `GitHub Oauth scopes
documentation
<https://developer.github.com/apps/building-oauth-apps/understanding-scopes-for-oauth-apps/>`_
but we recommend ``read:user`` as this requires no additional configuration by
GitHub organisations and users.
For example, omitting the scope means members of an organisation must `set
their membership to Public
<https://docs.github.com/en/github/setting-up-and-managing-your-github-user-account/publicizing-or-hiding-organization-membership>`_
to login, whereas setting it to ``read:org`` may require approval of the
application by a GitHub organisation admin.
Please see `this issue
<https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues/687>`_ for further
information.

.. note::

   Changing ``auth.scopes`` will not change the scope for existing OAuth tokens, you must invalidate them.


Google
^^^^^^

Google authentication is used by many universities (it is part of the "G Suite").
Note that using Google authentication requires your Hub to have a domain name
(it cannot **only** be accessible via an IP address).
For more information on authenticating with Google oauth, see the :ref:`google_oauth`.

.. code-block:: yaml

   auth:
     type: google
     google:
       clientId: "yourlongclientidstring.apps.googleusercontent.com"
       clientSecret: "adifferentlongstring"
       callbackUrl: "http://<your_jupyterhub_host>/hub/oauth_callback"
       hostedDomain:
         - "youruniversity.edu"
       loginService: "Your University"

CILogon
^^^^^^^

.. code-block:: yaml

   auth:
     type: cilogon
     cilogon:
       clientId: "y0urc1logonc1ient1d"
       clientSecret: "an0ther1ongs3cretstr1ng"
       callbackUrl: "http://<your_jupyterhub_host>/hub/oauth_callback"

In order to overcome the `caveats <https://github.com/jupyterhub/oauthenticator/blob/master/oauthenticator/cilogon.py>`_ of implementing CILogon OAuthAuthenticator for JupyterHub,
i.e. default username_claim of ePPN does not work for all providers, e.g. generic OAuth such as Google, Use c.CILogonOAuthenticator.username_claim = 'email' to use email instead of ePPN as the JupyterHub username:

Add to your config.yaml file to :ref:`inject extra python based configuration that should be in jupyterhub_config.py <schema:hub.extraConfig>` as below:

.. code-block:: yaml

   hub:
     extraConfig:
       myAuthConfig: |
         c.CILogonOAuthenticator.username_claim = 'email'


Globus
^^^^^^

Globus Auth is a foundational identity and access management platform service
designed to address unique needs of the science and engineering community.
Globus provides cloud-based services for reliably moving, sharing, publishing
and discovering data, whether your files live on a supercomputer, lab cluster,
tape archive, public cloud, or your own laptop. Start a Globus app
`here <https://developers.globus.org/>`_!

.. code-block:: yaml

   auth:
     type: globus
     globus:
       clientId: "y0urc1logonc1ient1d"
       clientSecret: "an0ther1ongs3cretstr1ng"
       callbackUrl: "https://<your_jupyterhub_host>/hub/oauth_callback"
       identityProvider: "youruniversity.edu"


Azure Active Directory
^^^^^^^^^^^^^^^^^^^^^^

Azure Active Directory <https://docs.microsoft.com/en-us/azure/active-directory/>`_
is an identity provider from Microsoft Azure.
The main additional option to configure for Azure AD from any other
oauth provider is the tenant id.

.. code-block:: yaml

   auth:
     type: azuread
     azuread:
       clientId: "your-aad-client-id"
       clientSecret: "your-aad-client-secret"
       tenantId: "your-aad-tenant-id"
       callbackUrl: "https://<your_jupyterhub_host>/hub/oauth_callback"


OpenID Connect
^^^^^^^^^^^^^^

`OpenID Connect <https://openid.net/connect>`_ is an identity layer on top of the
OAuth 2.0 protocol, implemented by
`various servers and services <https://openid.net/developers/certified/#OPServices>`_.
While OpenID Connect endpoint discovery is not supported by oauthentiator,
you can still configure JupyterHub to authenticate with OpenID Connect providers
by specifying all endpoints in GenericOAuthenticator.
By setting `login_service` you can customize the label on the login button.

Here's an example for authenticating against `keycloak <https://www.keycloak.org/docs/latest/securing_apps/index.html#endpoints>`_,
after you `configure an OIDC Client <https://www.keycloak.org/docs/latest/server_admin/index.html#oidc-clients>`_
and obtain the confidential client credentials.

.. code-block:: yaml

   hub:
     extraEnv:
       OAUTH2_AUTHORIZE_URL: https://${host}/auth/realms/${realm}/protocol/openid-connect/auth
       OAUTH2_TOKEN_URL: https://${host}/auth/realms/${realm}/protocol/openid-connect/token
       OAUTH_CALLBACK_URL: https://<your_jupyterhub_host>/hub/oauth_callback
   auth:
     type: custom
     custom:
       className: oauthenticator.generic.GenericOAuthenticator
       config:
         login_service: "keycloak"
         client_id: "y0urc1logonc1ient1d"
         client_secret: "an0ther1ongs3cretstr1ng"
         token_url: https://${host}/auth/realms/${realm}/protocol/openid-connect/token
         userdata_url: https://${host}/auth/realms/${realm}/protocol/openid-connect/userinfo
         userdata_method: GET
         userdata_params: {'state': 'state'}
         username_key: preferred_username

Auth0
^^^^^

Auth0 is a popular commercial provider of identity management. The JupyterHub helm chart does not include support for
Auth0 by default.  To use Auth0, ``extraEnv`` and ``extraConfig`` must be configured as follows:

Note that without the scope defined, authenticating to JupyterHub after already being logged in to Auth0 will fail.

.. code-block:: yaml

    hub:
      extraEnv:
        AUTH0_SUBDOMAIN: 'prod-8ua-1yy9'
      extraConfig:
        myConfig.py: |
          c.JupyterHub.authenticator_class = 'oauthenticator.auth0.Auth0OAuthenticator'
          c.Auth0OAuthenticator.client_id = 'client-id-from-auth0-here'
          c.Auth0OAuthenticator.client_secret = 'client-secret-from-auth0-here'
          c.Auth0OAuthenticator.oauth_callback_url = 'https://<your_jupyterhub_host>/hub/oauth_callback'
          c.Auth0OAuthenticator.scope = ['openid', 'email']
          c.Authenticator.admin_users = {
              'devops@example.com'
          }
          c.Authenticator.auto_login = True
.. _google_oauth:

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
   "/hub/oauth_callback". For example, `http://{example.com}/hub/oauth_callback`.

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

The ``callbackUrl`` key is set to the authorized redirect URI you specified
earlier. Set ``hostedDomain`` to your institution's domain name. The value of
``loginService`` is a descriptive term for your institution that reminds your
users which account they are using to login.


Authenticating with LDAP
--------------------------

JupyterHub supports LDAP and Active Directory authentication.
Read the `ldapauthenticator <https://github.com/jupyterhub/ldapauthenticator>`_
documentation for a full explanation of the available parameters.

Example LDAP Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^

`auth.ldap.server.address` and `auth.ldap.dn.templates` are required. Other
fields are optional.

.. code-block:: yaml

   auth:
     type: ldap
     ldap:
       server:
         address: ldap.EXAMPLE.org
       dn:
         templates:
           - 'cn={username},ou=edir,ou=people,ou=EXAMPLE-UNIT,o=EXAMPLE'

Example Active Directory Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example is equivalent to that given in the
`ldapauthenticator README <https://github.com/jupyterhub/ldapauthenticator/blob/master/README.md>`_.

.. code-block:: yaml

   auth:
     type: ldap
     ldap:
       server:
         address: ad.EXAMPLE.org
       dn:
         lookup: true
         search:
           filter: '({login_attr}={login})'
           user: 'ldap_search_user_technical_account'
           password: 'secret'
         templates:
           - 'uid={username},ou=people,dc=wikimedia,dc=org'
           - 'uid={username},ou=developers,dc=wikimedia,dc=org'
         user:
           searchBase: 'ou=people,dc=wikimedia,dc=org'
           escape: False
           attribute: 'sAMAccountName'
           dnAttribute: 'cn'
       allowedGroups:
         - 'cn=researcher,ou=groups,dc=wikimedia,dc=org'
         - 'cn=operations,ou=groups,dc=wikimedia,dc=org'

Example Auth0 Configuration
---------------------------

Auth0 (even on free billing plan) allows you to leverage its OAuth flow. It is based on OpenID Connect implementation, but extends it. Assuming the application is already created and you fetched Client Id, Client Secret and Auth0 authorization domain.

.. code-block:: yaml

   hub:
     extraEnv:
       OAUTH_CALLBACK_URL: https://<HUB_DOMAIN>/hub/oauth_callback
   auth:
     type: custom
     scopes: # that is essential to request certain scope, otherwise user profile call won't return anything
       - "openid"
       - "name"
       - "profile"
       - "email"
     custom:
       className: oauthenticator.generic.GenericOAuthenticator
       config:
         login_service: "My Auth0"
         client_id: "<CLIENT_ID>"
         client_secret: "<CLIENT_SECRET>"
         authorize_url: https://<DOMAIN>.us.auth0.com/authorize
         token_url: https://<DOMAIN>.us.auth0.com/oauth/token
         userdata_url: https://<DOMAIN>.us.auth0.com/userinfo
         userdata_method: GET
         username_key: name # define the specific key to for username from JSON returned by `/userinfo`



Adding a Whitelist
------------------

JupyterHub can be configured to only allow a specified
`whitelist <https://jupyterhub.readthedocs.io/en/latest/getting-started/authenticators-users-basics.html#create-a-set-of-allowed-users>`_
of users to login. This is especially useful if you are
using an authenticator with an authentication service open to the general
public, such as GitHub or Google.

.. note::

   A whitelist must be used **along with another authenticator**. It simply restricts the usernames that
   are allowed for your JupyterHub, but is not an authenticator by itself.

You can specify this list of usernames in your `config.yaml`:

.. code-block:: yaml

   auth:
     whitelist:
       users:
         - user1
         - user2

For example, here's the configuration to use a white list along with the Dummy Authenticator.
By default, the Dummy Authenticator will accept any username if they provide the right password.
But combining it with a whitelist, users must input **both** an accepted username *and* password.

.. code-block:: yaml

   auth:
     type: dummy
     dummy:
       password: 'mypassword'
     whitelist:
       users:
         - user1
         - user2
