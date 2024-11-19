(authentication)=

# Authentication and authorization

Authentication is about identity, while _authorization_ is about permissions. In
this section you will learn how to configure both by choosing and configuring a
_JupyterHub Authenticator class_.

As an example, you can configure JupyterHub to delegate authentication and
authorization to the GitHubOAuthenticator. It enable users to login with GitHub
accounts, where perhaps only a few specific users and other users users part of
a specific GitHub organization is allowed access.

Before configuring authentication with an external identity provider, you must
have [setup HTTPS](https).

## Useful understanding

### Authenticator classes

By default a Z2JH deployment use the
{external:py:class}`jupyterhub.auth.DummyAuthenticator` JupyterHub authenticator
class that allows anyone to login with any username and password. This should
only be used for initial testing purposes.

You should decide on a [jupyterhub authenticator class] to use. Several such
classes are available in the hub image through [installed Python packages], and
a few of them are described below.

[authenticator class]: https://jupyterhub.readthedocs.io/en/stable/reference/authenticators.html
[installed python packages]: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/HEAD/images/hub/requirements.txt

### The configuration system

First we should configure JupyterHub to use our chosen authenticator class and
the authenticator class itself through this Helm chart's
[`hub.config`](schema_hub.config) configuration.

## General configuration

As all authenticator classes derive from the
{external:py:class}`jupyterhub.auth.Authenticator` base class, they share some
configuration options. Below are some common configuration options from the base
class.

### [allowed_users](https://jupyterhub.readthedocs.io/en/stable/reference/api/auth.html#jupyterhub.auth.Authenticator.allowed_users) / [admin_users](https://jupyterhub.readthedocs.io/en/stable/reference/api/auth.html#jupyterhub.auth.LocalAuthenticator.admin_users)

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
      authenticator_class: dummy
```

In the above configuration, we have configured three things:

1. JupyterHub is instructed to use the dummy authenticator to login (only appropriate for testing purposes),
2. anyone will be able to login with username `user1-4` and the password `a-shared-secret-password`
3. `user1` and `user2` will have admin permissions, while `user3` and `user4` will be regular users.

### [auto_login](https://jupyterhub.readthedocs.io/en/stable/reference/api/auth.html#jupyterhub.auth.Authenticator.auto_login)

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

### [enable_auth_state](https://jupyterhub.readthedocs.io/en/stable/reference/api/auth.html#jupyterhub.auth.Authenticator.enable_auth_state)

If you want JupyterHub to persist often sensitive information received as part
of logging in, you need to enable it.

```yaml
hub:
  config:
    Authenticator:
      enable_auth_state: true
```

For more information about authentication state, see [JupyterHub's own
documentation](https://jupyterhub.readthedocs.io/en/stable/reference/authenticators.html#authentication-state)
about authentication state.

````{note}
The encryption and decryption of auth state requires a cryptographical key.

As of version 1.0.0 this will automatically be generated and there is no need to
set it manually.

If you wish to reset a generated key, you can use `kubectl edit` on the k8s
Secret typically named `hub` and remove the `hub.config.CryptKeeper.keys` entry
in the k8s Secret, then perform a new `helm upgrade`.

To manually set a cryptographical key, you can do it like this.

```yaml
hub:
  config:
    CryptKeeper:
      keys:
        - 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
```
````

## Configuring authenticator classes

Below we provide a few configuration examples of commonly used authentication
classes. For more details about them, please see the authentication class' own
documentation.

### OAuth2 based authentication

JupyterHub's [oauthenticator](https://github.com/jupyterhub/oauthenticator)
project has support for enabling your users to authenticate via a third-party
OAuth2 _identity provider_ such as GitHub, Google, and CILogon. All of these
will require an OAuth2 _client id_ and _client secret_.

For details on how to acquire a client id and client secret, please refer to
[oauthenticator's
documentation](https://oauthenticator.readthedocs.io/en/stable/tutorials/general-setup.html).

#### GitHub

```{warning}
This documentation may not have been updated recently. Due to that, please only use this
_as a complement_ to the official [GitHubOAuthenticator documentation].

[githuboauthenticator documentation]: https://oauthenticator.readthedocs.io/en/latest/tutorials/provider-specific-setup/providers/github.html

Going onwards, the goal is to ensure we have good documentation in the
OAuthenticator project and reference that instead of maintaining similar
documentation in this project also.
```

GitHub is the largest hosting service for git repositories. It is free to create
an account at GitHub, and relatively straightforward to set up OAuth credentials
so that users can authenticate with their GitHub username/password.

To create OAuth credentials on GitHub, follow these steps:

- Click your profile picture -> settings -> developer settings
- Make sure you're on the "OAuth Apps" tab, then click "New OAuth App"
- Fill out the forms (you'll need your hub address) and generate your
  ID/Secret.

To enable GitHub authentication, your `config.yaml` should contain the following
configuration:

```yaml
hub:
  config:
    GitHubOAuthenticator:
      client_id: your-client-id
      client_secret: your-client-secret
      oauth_callback_url: https://your-jupyterhub-domain/hub/oauth_callback
    JupyterHub:
      authenticator_class: github
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
      scope:
        - read:org
```

If you would like to restrict access to a specific team within a GitHub organization, use
the following syntax:

```yaml
hub:
  config:
    GitHubOAuthenticator:
      allowed_organizations:
        - my-github-organization:my-team
      scope:
        - read:org
```

```{admonition} About the choice of scope
The narrower scope `read:user` is sufficient for a configuration of `allowed_organizations` to function if you both list only entire organizations rather than specific teams, and if the users [make their organization membership public](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-your-membership-in-organizations/publicizing-or-hiding-organization-membership).

The broader scope `read:org` doesn't have the limitations of `read:user`, but will require a one-off approval by the admins of the GitHub organizations' listed in `allowed_organizations`. This kind of approval can be requested by organization users [as documented on GitHub](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-your-membership-in-organizations/requesting-organization-approval-for-oauth-apps).

For details about GitHub scopes, see [GitHub's documentation](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps).
```

#### Google

```{warning}
This documentation may not have been updated recently. Due to that, please only use this
_as a complement_ to the official [GoogleOAuthenticator documentation].

[googleoauthenticator documentation]: https://oauthenticator.readthedocs.io/en/latest/tutorials/provider-specific-setup/providers/google.html

Going onwards, the goal is to ensure we have good documentation in the
OAuthenticator project and reference that instead of maintaining similar
documentation in this project also.
```

Google authentication is used by many universities (it is part of "G Suite").

If your institution is a [G Suite customer](https://workspace.google.com) that
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
    GoogleOAuthenticator:
      client_id: your-client-id.apps.googleusercontent.com
      client_secret: your-client-secret
      oauth_callback_url: https://your-jupyterhub-domain/hub/oauth_callback
      hosted_domain:
        - your-university.edu
      login_service: Your university
    JupyterHub:
      authenticator_class: google
```

The `oauth_callback_url` key is set to the authorized redirect URI you specified
earlier. Set `hosted_domain` to your institution's domain name. The value of
`login_service` is a descriptive term for your institution that reminds your
users which account they are using to login.

#### CILogon

```{warning}
This documentation may not have been updated recently. Due to that, please only use this
_as a complement_ to the official [CILogonOAuthenticator documentation].

[ciLogonoauthenticator documentation]: https://oauthenticator.readthedocs.io/en/latest/tutorials/provider-specific-setup/providers/cilogon.html

Going onwards, the goal is to ensure we have good documentation in the
OAuthenticator project and reference that instead of maintaining similar
documentation in this project also.
```

Please see CyberInfrastructure Logon's [website](https://www.cilogon.org) for
more information about what kind of identity is managed by CILogon.

```yaml
hub:
  config:
    CILogonOAuthenticator:
      client_id: your-client-id
      client_secret: your-client-secret
      oauth_callback_url: https://your-jupyterhub-domain/hub/oauth_callback
    JupyterHub:
      authenticator_class: cilogon
```

#### Globus

```{warning}
This documentation may not have been updated recently. Due to that, please only use this
_as a complement_ to the official [GlobusOAuthenticator documentation].

[globusoauthenticator documentation]: https://oauthenticator.readthedocs.io/en/latest/tutorials/provider-specific-setup/providers/globus.html

Going onwards, the goal is to ensure we have good documentation in the
OAuthenticator project and reference that instead of maintaining similar
documentation in this project also.
```

Globus Auth is a foundational identity and access management platform
service designed to address unique needs of the science and engineering
community. Globus provides cloud-based services for reliably moving,
sharing, publishing and discovering data, whether your files live on a
supercomputer, lab cluster, tape archive, public cloud, or your own
laptop. Start a Globus app [here](https://developers.globus.org/)!

```yaml
hub:
  config:
    GlobusOAuthenticator:
      client_id: your-client-id
      client_secret: your-client-secret
      oauth_callback_url: https://your-jupyterhub-domain/hub/oauth_callback
      identity_provider: your-university.edu
    JupyterHub:
      authenticator_class: globus
```

#### Azure Active Directory

```{warning}
This documentation may not have been updated recently. Due to that, please only use this
_as a complement_ to the official [AzureAdOAuthenticator documentation].

[azureadoauthenticator documentation]: https://oauthenticator.readthedocs.io/en/latest/tutorials/provider-specific-setup/providers/azuread.html

Going onwards, the goal is to ensure we have good documentation in the
OAuthenticator project and reference that instead of maintaining similar
documentation in this project also.
```

[Azure Active Directory](https://learn.microsoft.com/en-us/azure/active-directory/)
is an identity provider from Microsoft Azure. Apart from needing a OAuth2
_client id_ and _client secret_, you will also need a _tenant id_.

```yaml
hub:
  config:
    AzureAdOAuthenticator:
      client_id: your-client-id
      client_secret: your-client-secret
      oauth_callback_url: https://your-jupyterhub-domain/hub/oauth_callback
      tenant_id: your-tenant-id
    JupyterHub:
      authenticator_class: azuread
```

#### Auth0

```{warning}
This documentation may not have been updated recently. Due to that, please only use this
_as a complement_ to the official [Auth0OAuthenticator documentation].

[auth0oauthenticator documentation]: https://oauthenticator.readthedocs.io/en/latest/tutorials/provider-specific-setup/providers/auth0.html

Going onwards, the goal is to ensure we have good documentation in the
OAuthenticator project and reference that instead of maintaining similar
documentation in this project also.
```

[Auth0](https://auth0.com/) is a commercial provider of identity management.

```yaml
hub:
  config:
    Auth0OAuthenticator:
      client_id: client-id-from-auth0-here
      client_secret: client-secret-from-auth0-here
      oauth_callback_url: https://your-jupyterhub-domain/hub/oauth_callback
      auth0_domain: prod-8ua-1yy9.auth0.com
      scope:
        - openid
        - email
    JupyterHub:
      authenticator_class: auth0
```

#### GenericOAuthenticator - OpenID Connect

```{warning}
This documentation may not have been updated recently. Due to that, please only use this
_as a complement_ to the official [GenericOAuthenticator documentation].

[genericoauthenticator documentation]: https://oauthenticator.readthedocs.io/en/latest/tutorials/provider-specific-setup/providers/generic.html

Going onwards, the goal is to ensure we have good documentation in the
OAuthenticator project and reference that instead of maintaining similar
documentation in this project also.
```

[OpenID Connect](https://openid.net/connect) is an identity layer on top of the
OAuth 2.0 protocol, implemented by [various servers and
services](https://openid.net/certified-open-id-developer-tools/). While OpenID
Connect endpoint discovery is not supported by oauthentiator, you can still
configure JupyterHub to authenticate with OpenID Connect providers by specifying
all endpoints in the GenericOAuthenticator class.

##### KeyCloak

```{warning}
This documentation may not have been updated recently. Due to that, please only use this
_as a complement_ to the official [GenericOAuthenticator documentation].

Going onwards, the goal is to ensure we have good documentation in the
OAuthenticator project and reference that instead of maintaining similar
documentation in this project also.
```

[KeyCloak](https://www.keycloak.org) is an open source based provider of
identity management that you can host yourself. Below is an example on how you
can configure the GenericOAuthenticator class to authenticate against a KeyCloak
server (version 17 or later).

To configure an OpenID Connect client, see [KeyCloak's own
documentation](https://www.keycloak.org/docs/latest/server_admin/index.html#_oidc_clients).

```yaml
hub:
  config:
    GenericOAuthenticator:
      client_id: your-client-id
      client_secret: your-client-secret
      oauth_callback_url: https://your-jupyterhub-domain/hub/oauth_callback
      authorize_url: https://${host}/realms/${realm}/protocol/openid-connect/auth
      token_url: https://${host}/realms/${realm}/protocol/openid-connect/token
      userdata_url: https://${host}/realms/${realm}/protocol/openid-connect/userinfo
      login_service: keycloak
      username_claim: preferred_username
      userdata_params:
        state: state
      # Allow all Keycloak users
      allow_all: true
      admin_users:
        - admin
    JupyterHub:
      authenticator_class: generic-oauth
```

### LDAP and Active Directory

```{warning}
This documentation may not have been updated recently. Due to that, please only use this
_as a complement_ to the official [LDAPAuthenticator documentation].

[ldapauthenticator documentation]: https://github.com/jupyterhub/ldapauthenticator#readme

Going onwards, the goal is to ensure we have good documentation in the
OAuthenticator project and reference that instead of maintaining similar
documentation in this project also.
```

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
[ldapauthenticator README](https://github.com/jupyterhub/ldapauthenticator/blob/HEAD/README.md).

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
