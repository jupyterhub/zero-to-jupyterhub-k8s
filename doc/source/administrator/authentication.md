(authentication)=

# Authentication and authorization

Authentication is about identity, while _authorization_ is about permissions. In
this section you will learn how to configure both. As an example, you can
configure authentication using GitHub accounts and restrict what users are
authorized based on membership of a GitHub organization.

Before configuring this, you should have [setup HTTPS](https).

## Useful understanding

### Authenticator classes

JupyterHub are by itself unable to authenticate any kind of identity, but
instead relies on _one_ chosen [_authenticator
class_](https://jupyterhub.readthedocs.io/en/stable/reference/authenticators.html)
to do it. Several such classes are already made available through [installed
Python
packages](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/master/images/hub/requirements.txt).

JupyterHub provides a base class,
[`Authenticator`](https://github.com/jupyterhub/jupyterhub/blob/master/jupyterhub/auth.py),
that all other authenticator classes are supposed to derive from. By configuring
this base class, we influence the behavior of the derived class as well.

### The configuration system

We configure JupyterHub to use our chosen authenticator class and the
authenticator class itself through this Helm chart's
[`hub.config`](schema_hub.config) configuration.

## General configuration

As all authenticator classes derive from the `Authenticator` base class, they
share some configuration options. Below are some common configuration options,
but please refer to the official [configuration
reference](https://jupyterhub.readthedocs.io/en/latest/api/auth.html) for more
details.

### [allowed_users](https://jupyterhub.readthedocs.io/en/latest/api/auth.html#jupyterhub.auth.Authenticator.allowed_users) / [admin_users](https://jupyterhub.readthedocs.io/en/latest/api/auth.html#jupyterhub.auth.LocalAuthenticator.admin_users)

Some authenticator classes may have dedicated logic in addition this this to
authorize users.

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

### [auto_login](https://jupyterhub.readthedocs.io/en/latest/api/auth.html#jupyterhub.auth.Authenticator.auto_login)

If you have configured authentication with GitHub for example, the page
`/hub/login` will feature a single orange button that users are to press to
login. If you want to bypass this screen and send users directly to GitHub login, you can
set `auto_login` to `true`.

```yaml
hub:
  config:
    Authenticator:
      auto_login: true
```

### [enable_auth_state](https://jupyterhub.readthedocs.io/en/latest/api/auth.html#jupyterhub.auth.Authenticator.enable_auth_state)

If you want JupyterHub to persist often sensitive information received as part
of logging in, you need to enable it and provide one or more keys for encryption
and decryption.

The recommended way of doing so for this Helm chart is to configure
[CryptKeeper](https://github.com/jupyterhub/jupyterhub/blob/master/jupyterhub/crypto.py)
with keys rather than setting an environment variable.

For more information, see [JupyterHub's own
documentation](https://jupyterhub.readthedocs.io/en/latest/reference/authenticators.html#authentication-state)
about authentication state.

```yaml
hub:
  config:
    Authenticator:
      enable_auth_state: true
    CryptKeeper:
      keys:
        - 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
```

## Configuring authenticator classes

Below we provide a few configuration examples of commonly used authentication
classes. For more details about them, please see the authentication class' own
documentation.

### OAuth2 based authentication

JupyterHub's [oauthenticator](https://github.com/jupyterhub/oauthenticator) has
support for enabling your users to authenticate via a third-party OAuth2
_identity provider_ such as GitHub, Google, and CILogon. All of these will
require an OAuth2 _client id_ and _client secret_.

For details on how to acquire a client id and client secret, please refer to
[oauthenticator's
documentation](https://oauthenticator.readthedocs.io/en/stable/getting-started.html).

#### GitHub

GitHub is the largest hosting service for git repositories. It is free to create
an account at GitHub, and relatively straightforward to set up OAuth credentials
so that users can authenticate with their GitHub username/password.

To create OAuth credentials on GitHub, follow these steps:

-   Click your profile picture -> settings -> developer settings
-   Make sure you're on the "OAuth Apps" tab, then click "New OAuth App"
-   Fill out the forms (you'll need your hub address) and generate your
    ID/Secret.

To enable GitHub authentication, your `config.yaml` should contain the following
configuration:

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

Make sure that the `oauth_callback_url` matches the one you set in GitHub.

To restrict access to the members of one or more GitHub organizations, amend
your previous configuration with these parts.

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

```{admonition} Alternative scopes
While you can set other scopes than `read:user` as described in [GitHub OAuth scopes documentation](https://docs.github.com/en/free-pro-team@latest/developers/apps/scopes-for-oauth-apps), we recommend `read:user`.

With `read:user`, the user will be requested to permit JupyterHub to read their profile data. The benefit of this choice is that it won't require configuration by the GitHub organizations' admins by by its members.
```

#### Google

Google authentication is used by many universities (it is part of "G Suite").

If your institution is a [G Suite customer](https://gsuite.google.com) that
integrates with Google services such as Gmail, Calendar, and Drive, you can
authenticate users to your JupyterHub using Google for authentication.

1.  Log in to the [Google API Console](https://console.developers.google.com).
2.  Select a project > Create a project... and set 'Project name'. This is a
    short term that is only displayed in the console. If you have already
    created a project you may skip this step.
3.  Type "Credentials" in the search field at the top and click to access the
    Credentials API.
4.  Click "Create credentials", then "OAuth client ID". Choose "Application
    type" > "Web application".
5.  Enter a name for your JupyterHub instance. You can give it a descriptive
    name or set it to be the hub's hostname.
6.  Set "Authorized JavaScript origins" to be your hub's URL.
7.  Set "Authorized redirect URIs" to be your hub's URL followed by
    `/hub/oauth_callback`. For example,
    `https://your-jupyterhub-domain/hub/oauth_callback`.
8.  When you click "Create", the console will generate and display a Client ID
    and Client Secret. Save these values.
9.  Type "consent screen" in the search field at the top and click to access the
    OAuth consent screen. Here you will customize what your users see when they
    login to your JupyterHub instance for the first time. Click Save when you
    are done.
10. Update your Helm chart's configuration (`config.yaml`) to look like this.

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
      authenticator_class: oauthenticator.google.GoogleOAuthenticator
```

The `oauth_callback_url` key is set to the authorized redirect URI you specified
earlier. Set `hosted_domain` to your institution's domain name. The value of
`login_service` is a descriptive term for your institution that reminds your
users which account they are using to login.

#### CILogon

Please see CyberInfrastructure Logon's [website](https://www.cilogon.org) for
more information about what kind of identity is managed by CILogon.

```yaml
hub:
  config:
    OAuthenticator:
      client_id: your-client-id
      client_secret: your-client-secret
      oauth_callback_url: https://your-jupyterhub-domain/hub/oauth_callback
    JupyterHub:
      authenticator_class: oauthenticator.cilogon.CILogonOAuthenticator
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

[Azure Active Directory](https://docs.microsoft.com/en-us/azure/active-directory/)
 is an identity provider from Microsoft Azure. Apart from needing a OAuth2
 _client id_ and _client secret_, you will also need a _tenant id_.

```yaml
hub:
  config:
    OAuthenticator:
      client_id: your-client-id
      client_secret: your-client-secret
      oauth_callback_url: https://your-jupyterhub-domain/hub/oauth_callback
    AzureAdOAuthenticator:
      tenant_id: your-tenant-id
    JupyterHub:
      authenticator_class: oauthenticator.azuread.AzureAdOAuthenticator
```

#### Auth0

[Auth0](https://auth0.com/) is a commercial provider of identity management.

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
#### GenericOAuthenticator - OpenID Connect

[OpenID Connect](https://openid.net/connect) is an identity layer on top of the
OAuth 2.0 protocol, implemented by [various servers and
services](https://openid.net/developers/certified/#OPServices). While OpenID
Connect endpoint discovery is not supported by oauthentiator, you can still
configure JupyterHub to authenticate with OpenID Connect providers by specifying
all endpoints in the GenericOAuthenticator class.

##### Auth0

Below is an example on how you can configure the GenericOAuthenticator to
authenticate against Auth0.

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
      username_key: name
    JupyterHub:
      authenticator_class: oauthenticator.generic.GenericOAuthenticator
```

##### KeyCloak

[KeyCloak](https://www.keycloak.org) is an open source based provider of
identity management that you can host yourself. Below is an example on how you
can configure the GenericOAuthenticator class to authenticate against a KeyCloak
server.

To configure an OpenID Connect client, see [KeyCloak's own
documentation](https://www.keycloak.org/docs/latest/server_admin/index.html#oidc-clients).

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

### LDAP and Active Directory

JupyterHub supports LDAP and Active Directory authentication. Read the
[ldapauthenticator](https://github.com/jupyterhub/ldapauthenticator)
documentation for a full explanation of the available parameters.

Only `server_address` and `bind_dn_template` are required, so a minimal
configuration would look like this.

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

Another example is provided below, equivalent to the example given in the
[ldapauthenticator README](https://github.com/jupyterhub/ldapauthenticator/blob/master/README.md).

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
