(authentication)=

# Authentication and authorization

Authentication is about identity, while _authorization_ is about access rights.
In this section you will learn how to configure both. For example, you can
configure to authenticate GitHub users and authorize those part of a specific
GitHub organization.

Before configuring this, you should have [setup HTTPS](https).

## Useful understanding

### Authenticator classes

As JupyterHub can't know how to authenticate all kinds of users, it expose
configuration to extend its capabilities to rely on a dedicated [_authenticator
class_](https://jupyterhub.readthedocs.io/en/stable/reference/authenticators.html).
Several such classes are already made available through [installed Python
packages](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/master/images/hub/requirements.txt).

### The Authenticator base class

JupyterHub provides a base class,
[`Authenticator`](https://github.com/jupyterhub/jupyterhub/blob/master/jupyterhub/auth.py),
that all other authenticator classes are supposed to derive from. By configuring
this base class, we influence the behavior of the derived class as well.

### The configuration system

We configure JupyterHub to use our chosen authenticator class and the
authenticator class in question through this Helm chart's
[`hub.config`](schema_hub.config) configuration.

## Configuring authorization

Some authenticator classes contain dedicated authorization logic, but that
doesn't stop you from using the common base class authorization logic.

```yaml
hub:
  config:
    Authenticator:
      admin_users:
        - user1
        - user2
      allowed_users:
        - user3
        - user4
    # ...
    DummyAuthenticator:
      password: a-shared-secret-password
    JupyterHub:
      authenticator_class: dummyauthenticator.DummyAuthenticator
```

```{note}
Please refer to [JupyterHub's own documentation](https://jupyterhub.readthedocs.io/en/latest/getting-started/authenticators-users-basics.html) for more details.
```

## Configuring authenticator classes

### OAuth2 based authentication

JupyterHub's
[oauthenticator](https://github.com/jupyterhub/oauthenticator) has
support for enabling your users to authenticate via a third-party OAuth
provider, including GitHub, Google, and CILogon.

Follow the service-specific instructions linked on the [oauthenticator
repository](https://oauthenticator.readthedocs.io/en/stable/) to generate
your JupyterHub instance's OAuth2 client ID and client secret. Then
declare the values in the helm chart (`config.yaml`).

Here are example configurations for common authentication services. Note
that in each case, you need to get the client ID and secret
before you can configure the helm chart for authentication.

#### GitHub

GitHub is the largest hosting service for git repositories. It is free
to create an account at GitHub, and relatively straightforward to set up
OAuth credentials so that users can authenticate with their GitHub
username/password.

To create OAuth credentials on GitHub, follow these steps:

-   Click your profile picture -> settings -> developer settings
-   Make sure you're on the "OAuth Apps" tab, then click "New OAuth
    App"
-   Fill out the forms (you'll need your hub address) and generate your
    ID/Secret.

To enable GitHub authentication, add the following to your
`config.yml`:

```yaml
hub:
  config:
    OAuthenticator:
      client_id: your-client-id
      client_secret: your-client-secret
      oauth_callback_url: https://your-jupyterhub-domain/hub/oauth_callback
    JupyterHub:
      authenticator_class: oauthenticator.github.GitHubOAuthenticator
```

Make sure that the `oauth_callback_url` matches the one
you set in GitHub.

##### Giving access to organizations on GitHub

You can also restrict access to all of the members of one or more GitHub
organizations. To do so, see the configuration below.

```yaml
hub:
  config:
    GitHubOAuthenticator:
      allowed_organizations:
        - my-github-organization
    OAuthenticator:
      scope:
        - read:user
```

`scope` can take other values as described in the [GitHub OAuth scopes
documentation](https://developer.github.com/apps/building-oauth-apps/understanding-scopes-for-oauth-apps/)
but we recommend `read:user` as this requires no additional
configuration by GitHub organisations and users. For example, omitting
the scope means members of an organisation must [set their membership to
Public](https://docs.github.com/en/github/setting-up-and-managing-your-github-user-account/publicizing-or-hiding-organization-membership)
to login, whereas setting it to `read:org` may require approval of the
application by a GitHub organisation admin. Please see [this
issue](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues/687)
for further information.

```{note}
Changing `scope` will not change the scope for existing OAuth tokens,
you must invalidate them.
```

#### Google

Google authentication is used by many universities (it is part of the
"G Suite"). Note that using Google authentication requires your Hub to
have a domain name (it cannot **only** be accessible via an IP address).

```yaml
hub:
  config:
    OAuthenticator:
      client_id: your-client-id.apps.googleusercontent.com
      client_secret: your-client-secret
      oauth_callback_url: https://your-jupyterhub-domain/hub/oauth_callback
    GoogleOAuthenticator:
      hosted_domain:
        - your-university.edu
      login_service: Your university
    JupyterHub:
      authenticator_class: oauthenticator.GoogleOAuthenticator
```

#### CILogon

```yaml
hub:
  config:
    OAuthenticator:
      client_id: your-client-id
      client_secret: your-client-secret
      oauth_callback_url: https://your-jupyterhub-domain/hub/oauth_callback
    JupyterHub:
      authenticator_class: oauthenticator.CILogonOAuthenticator
```

Based on [this
caveat](https://github.com/jupyterhub/oauthenticator/blob/6f239bebecbb3fb0242de7f753ae1c93ed101340/oauthenticator/cilogon.py#L5-L14),
you may need to also set the following.

```yaml
hub:
  config:
    CILogonOAuthenticator:
      username_claim: email
```

#### Globus

Globus Auth is a foundational identity and access management platform
service designed to address unique needs of the science and engineering
community. Globus provides cloud-based services for reliably moving,
sharing, publishing and discovering data, whether your files live on a
supercomputer, lab cluster, tape archive, public cloud, or your own
laptop. Start a Globus app [here](https://developers.globus.org/)!

```yaml
hub:
  config:
    OAuthenticator:
      client_id: your-client-id
      client_secret: your-client-secret
      oauth_callback_url: https://your-jupyterhub-domain/hub/oauth_callback
    GlobusOAuthenticator:
      identity_provider: your-university.edu
    JupyterHub:
      authenticator_class: oauthenticator.globus.GlobusOAuthenticator
```

#### Azure Active Directory

Azure Active Directory
\<<https://docs.microsoft.com/en-us/azure/active-directory/>>`_ is an
identity provider from Microsoft Azure. The main additional option to
configure for Azure AD from any other oauth provider is the tenant id.

```yaml
hub:
  config:
    OAuthenticator:
      client_id: your-aad-client-id
      client_secret: your-aad-client-secret
      oauth_callback_url: https://your-jupyterhub-domain/hub/oauth_callback
    AzureAdOAuthenticator:
      tenant_id: your-aad-tenant-id
    JupyterHub:
      authenticator_class: oauthenticator.azuread.AzureAdOAuthenticator
```

#### OpenID Connect

[OpenID Connect](https://openid.net/connect) is an identity layer on top
of the OAuth 2.0 protocol, implemented by [various servers and
services](https://openid.net/developers/certified/#OPServices). While
OpenID Connect endpoint discovery is not supported by oauthentiator, you
can still configure JupyterHub to authenticate with OpenID Connect
providers by specifying all endpoints in GenericOAuthenticator. By
setting `login_service` you can customize the label on the
login button.

Here's an example for authenticating against
[keycloak](https://www.keycloak.org/docs/latest/securing_apps/index.html#endpoints),
after you [configure an OIDC
Client](https://www.keycloak.org/docs/latest/server_admin/index.html#oidc-clients)
and obtain the confidential client credentials.

```yaml
hub:
  config:
    OAuthenticator:
      client_id: your-client-id
      client_secret: your-client-secret
      oauth_callback_url: https://your-jupyterhub-domain/hub/oauth_callback
      authorize_url: https://${host}/auth/realms/${realm}/protocol/openid-connect/auth
      token_url: https://${host}/auth/realms/${realm}/protocol/openid-connect/token
      userdata_url: https://${host}/auth/realms/${realm}/protocol/openid-connect/userinfo
    GenericOAuthenticator:
      login_service: keycloak
      username_key: preferred_username
      userdata_params:
        state: state
    JupyterHub:
      authenticator_class: oauthenticator.generic.GenericOAuthenticator
```

#### Auth0

Auth0 is a popular commercial provider of identity management. The
JupyterHub helm chart does not include support for Auth0 by default. To
use Auth0, `extraEnv` and `extraConfig` must be configured as follows:

Note that without the scopes defined, authenticating to JupyterHub after
already being logged in to Auth0 will fail.

```yaml
hub:
  config:
    OAuthenticator:
      client_id: client-id-from-auth0-here
      client_secret: client-secret-from-auth0-here
      oauth_callback_url: https://your-jupyterhub-domain/hub/oauth_callback
      scope:
        - openid
        - email
    Auth0OAuthenticator:
      auth0_subdomain: prod-8ua-1yy9
    Authenticator:
      admin_users:
        - devops@example.com
      auto_login: true
    JupyterHub:
      authenticator_class: oauthenticator.auth0.Auth0OAuthenticator
```

#### Full Example of Google OAuth2

If your institution is a [G Suite customer](https://gsuite.google.com)
that integrates with Google services such as Gmail, Calendar, and Drive,
you can authenticate users to your JupyterHub using Google for
authentication.

1.  Log in to the [Google API
    Console](https://console.developers.google.com).
2.  Select a project > Create a project\... and set 'Project name'.
    This is a short term that is only displayed in the console. If you
    have already created a project you may skip this step.
3.  Type "Credentials" in the search field at the top and click to
    access the Credentials API.
4.  Click "Create credentials", then "OAuth client ID". Choose
    "Application type" > "Web application".
5.  Enter a name for your JupyterHub instance. You can give it a
    descriptive name or set it to be the hub's hostname.
6.  Set "Authorized JavaScript origins" to be your hub's URL.
7.  Set "Authorized redirect URIs" to be your hub's URL followed by
    `/hub/oauth_callback`. For example,
    `https://your-jupyterhub-domain/hub/oauth_callback`.
8.  When you click "Create", the console will generate and display a
    Client ID and Client Secret. Save these values.
9.  Type "consent screen" in the search field at the top and click to
    access the OAuth consent screen. Here you will customize what your
    users see when they login to your JupyterHub instance for the first
    time. Click Save when you are done.
10. In your helm chart, create a stanza that contains these OAuth
    fields:

```yaml
hub:
  config:
    OAuthenticator:
      client_id: your-client-id.apps.googleusercontent.com
      client_secret: your-client-secret
      oauth_callback_url: https://your-jupyterhub-domain/hub/oauth_callback
    GoogleOAuthenticator:
      hosted_domain:
        - your-university.edu
      login_service: Your university
    JupyterHub:
      authenticator_class: oauthenticator.GoogleOAuthenticator
```

The `oauth_callback_url` key is set to the authorized redirect URI you
specified earlier. Set `hosted_domain` to your institution's domain
name. The value of `login_service` is a descriptive term for your
institution that reminds your users which account they are using to
login.

#### Authenticating with LDAP

JupyterHub supports LDAP and Active Directory authentication. Read the
[ldapauthenticator](https://github.com/jupyterhub/ldapauthenticator)
documentation for a full explanation of the available parameters. The
full mapping between parameters set in `values.yaml` and
`ldapauthenticator` parameter names can be found in
[jupyterhub_config.py](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/master/jupyterhub/files/hub/jupyterhub_config.py#L353).

#### Example LDAP Configuration

`server_address` and `bind_dn_template` are
required. Other fields are optional.

```yaml
hub:
  config:
    JupyterHub:
      authenticator_class: ldapauthenticator.LDAPAuthenticator
    LDAPAuthenticator:
      bind_dn_template:
        - cn={username},ou=edir,ou=people,ou=EXAMPLE-UNIT,o=EXAMPLE
      server_address: ldap.EXAMPLE.org
```

#### Example Active Directory Configuration

This example is equivalent to that given in the [ldapauthenticator
README](https://github.com/jupyterhub/ldapauthenticator/blob/master/README.md).

```yaml
hub:
  config:
    JupyterHub:
      authenticator_class: ldapauthenticator.LDAPAuthenticator
    LDAPAuthenticator:
      allowed_groups:
        - cn=researcher,ou=groups,dc=wikimedia,dc=org
        - cn=operations,ou=groups,dc=wikimedia,dc=org
      bind_dn_template:
        - uid={username},ou=people,dc=wikimedia,dc=org
        - uid={username},ou=developers,dc=wikimedia,dc=org
      escape_userdn: false
      lookup_dn: true
      lookup_dn_search_filter: ({login_attr}={login})
      lookup_dn_search_password: secret
      lookup_dn_search_user: ldap_search_user_technical_account
      lookup_dn_user_dn_attribute: cn
      server_address: ad.EXAMPLE.org
      user_attribute: sAMAccountName
      user_search_base: ou=people,dc=wikimedia,dc=org
```

#### Example Auth0 Configuration

Auth0 (even on free billing plan) allows you to leverage its OAuth flow.
It is based on OpenID Connect implementation, but extends it. Assuming
the application is already created and you fetched Client Id, Client
Secret and Auth0 authorization domain.

```yaml
hub:
  config:
    OAuthenticator:
      client_id: your-client-id
      client_secret: your-client-secret
      oauth_callback_url: https://your-jupyterhub-domain/hub/oauth_callback
      authorize_url: https://your-domain.us.auth0.com/authorize
      token_url: https://your-domain.us.auth0.com/oauth/token
      userdata_url: https://your-domain.us.auth0.com/userinfo
      scope:
        - openid
        - name
        - profile
        - email
    GenericOAuthenticator:
      login_service: My Auth0
      username_key: name
    JupyterHub:
      authenticator_class: oauthenticator.generic.GenericOAuthenticator
```
