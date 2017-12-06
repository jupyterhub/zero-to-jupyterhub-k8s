.. _security:

Security Considerations
=======================

Setting up HTTPS
----------------

Enabling HTTPS is an important part of keeping the internet secure for
your users & the world at large. Zero to JupyterHub makes doing so quite
easy since version 0.5, integrating with `Let's Encrypt <https://letsencrypt.org/>`_
for free HTTPS certificates.

You can also purchase your own SSL certificates from a certificate provider.

1. Buy a domain name from a registrar. Pick whichever one you want.
2. Create an ``A record`` from the domain you want to use, pointing to the
   ``EXTERNAL-IP`` of the ``proxy-public`` service.
3. Wait for the change to propagate. Propagation can take several minutes to
   several hours. Wait until you can type in the name of the domain you bought
   and it shows you the JupyterHub landing page.

   It is important that you wait - prematurely going to the next step might cause problems!

4. Tell JupyterHub to use HTTPS via ``config.yaml``

  a. For letsencrypt, add your domain name and contact email for letsencrypt renewal to ``config.yaml``:

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

    and paste the contents of your ssl key and certificate to ``secrets.yaml``:

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

5. Apply the config changes by running ``helm upgrade ...``.
6. Wait for about a minute, now your hub is HTTPS enabled! Congratulations, your
   users are now more secure now than they were before!

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

We highly recommend against doing so, however, as this will introduce
security vulnerabilities to your deployment!
