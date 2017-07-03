.. _glossary:

Glossary
========

.. Additions to the glossary are welcomed. Please add in alphabetical order.

A partial glossary of terms used in this guide. For more complete
descriptions of the components in JupyterHub, see `the list of tools
used in JupyterHub <tools.html>`_. Here we try to keep the definition as
succinct and relevant as possible, and provide links to learn more details.

admin user
    A user who can access the JupyterHub admin panel. They can start/stop user
    pods, and potentially access their notebooks.

`authenticator <http://jupyterhub.readthedocs.io/en/stable/authenticators.html>`_
    The way in which users are authenticated to log into JupyterHub. There are
    many authenticators available, like GitHub, Google, MediaWiki,
    Dummy (anyone can log in), etc.

culler
  A separate process that stops the user pods of users who have not been
  active in a configured interval.

persistent storage
    A filesystem attached to a user pod that allows the user to store
    notebooks and files that persist across multiple logins.
