.. _security:

Security Considerations
=======================

Setting up HTTPS
----------------

Enabling HTTPS is an important security practice.
Zero to JupyterHub makes doing so quite
easy since version 0.5, integrating with `Let's Encrypt <https://letsencrypt.org/>`_
for free HTTPS certificates.

.. note::

   Alternatively, you can purchase your own SSL certificates from a certificate provider.

Set up your domain
~~~~~~~~~~~~~~~~~~

1. Buy a domain name from a registrar. Pick whichever one you want.
2. Create an ``A record`` from the domain you want to use, pointing to the
   ``EXTERNAL-IP`` of the ``proxy-public`` service. The exact way to do this
   will depend on the DNS provider that you're using.
3. Wait for the change to propagate. Propagation can take several minutes to
   several hours. Wait until you can type in the name of the domain you bought
   and it shows you the JupyterHub landing page.

   It is important that you wait - prematurely going to the next step might cause problems!

Configure JupyterHub to use HTTPS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that your domain is ready, it's time to configure JupyterHub to use HTTPS
when connecting to it.

1. Tell JupyterHub to use HTTPS via ``config.yaml``

  a. If you're using letsencrypt, add your domain name and contact email
     for letsencrypt renewal to ``config.yaml``:

    .. code-block:: yaml

      proxy:
        https:
          hosts:
            - <your-domain-name>
          letsencrypt:
            contactEmail: <your-email-address>

  b. If you have your own SSL certificate, you can configure SSL manually.
     Add to ``config.yaml``:

    .. code-block:: yaml

      proxy:
        https:
          hosts:
            - <your-domain-name>
          type: manual

    and paste the contents of your ssl key and certificate into a file
    called ``secrets.yaml``, like so:

    .. code-block:: yaml

      proxy:
        https:
          manual:
            key: |
              -----BEGIN RSA PRIVATE KEY-----
              ...
              -----END RSA PRIVATE KEY-----
            cert: |
              -----BEGIN CERTIFICATE-----
              ...
              -----END CERTIFICATE-----

2. Apply the config changes by running ``helm upgrade ...``.
3. Wait for about a minute, now your hub is HTTPS enabled!

Role Based Access Control (RBAC)
--------------------------------

Kubernetes supports (and often requires) using
`Role Based Access Control (RBAC)
<https://kubernetes.io/docs/admin/authorization/rbac/>`_
to secure which pods / users can perform what kinds of actions on the cluster.
If RBAC is disabled, all pods are given ``root`` equivalent permission on the
Kubernetes cluster and all the nodes in it, which is bad!

As of ``v0.5``, the helm chart can natively work with RBAC enabled clusters. We ship
appropriate minimal RBAC rules for the various components we use. If you want to
disable the RBAC rules for whatever reason, you can do so with the following
snippet in your config.yaml:

.. raw:: yaml

   rbac:
      enabled: false

We recommend keeping RBAC enabled. Proceed with caution if disabling RBAC,
as this introduces security vulnerabilities.
