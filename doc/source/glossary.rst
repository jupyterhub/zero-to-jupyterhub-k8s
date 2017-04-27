Glossary
========

A partial glossary of terms used in this guide. For more complete
descriptions of the components in JupyterHub, see `the list of tools
used in JupyterHub <tools.html>`_. Here we try to keep the definition as
succint & relevant as possible, and provide links to learn more details.

`authenticator <http://jupyterhub.readthedocs.io/en/stable/authenticators.html>`_
  The way in which users are authenticated to log into JupyterHub. There are many authenticators
  available, like GitHub, Google, MediaWiki, Dummy (anyone can log in), etc.

persistent storage
  A filesystem attached to a user pod that allows the user to store notebooks / files that persist
  across multiple logins.

culler
  A separate process that stops the user pods of users who have not been active in a configured interval.

admin user
  A user who can access the JupyterHub admin panel. They can start/stop user pods, and potentially
  access their notebooks.
