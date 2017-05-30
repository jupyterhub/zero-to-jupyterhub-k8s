.. _cost:

Estimating costs
================

Cost estimates depend highly on your deployment setup. Several factors that
significantly influence cost estimates, include:

- Hardware provided to users
- Number of users
- Usage patterns of users

Hardware
--------

**Memory (RAM)** makes up the largest part of a cost estimate. More RAM means
that your users will be able to work with larger datasets with more
flexibility, but it can also be expensive. As a general rule, costs associated
with RAM scale at <XXX> cost.

**Persistent storage for users**, if needed, is another element that will impact
the cost estimate. If users don't have persistent storage, then disks will be
wiped after users finish their sessions. None of their changes will be saved.
This requires significantly fewer storage resources, and also results in faster
load times. Storage roughly scales at <XXX> cost.

Users
-----

The number of users has a direct relationship to cost estimates. Since a
deployment may support different types of users (i.e. researchers, students,
instructors) with varying hardware and storage needs, take into account both the
type of users and the number per type.

User usage patterns
-------------------

Another important factor is what usage pattern your users will have. Will they
all use the JupyterHub at once, such as during a large class workshop?
will users use JupyterHub at different times of day?

The usage patterns and peak load on the system have important implications for
the resources you need to provide. In the future JupyterHub will have
auto-scaling functionality, but currently it does not. This means that you need
to provision resources for the *maximum* expected number of users at one time.


Examples
--------

Here are a few examples that describe the use cases and amount of resources
used by a particular JupyterHub implementation, and how much it might cost.
Your estimates will vary.

Data 8
~~~~~~

The Data 8 course at UC Berkeley used a JupyterHub to coordinate all course
material and to provide a platform where students would run their code. This
consisted of many hundreds of students, who had minimal requirements in terms
of CPU and memory usage. Ryan Lovett put together a short Jupyter notebook
`estimating the cost for computational resources`_ depending on the student
needs.

.. _estimating the cost for computational resources: https://github.com/data-8/jupyterhub-k8s/blob/master/docs/cost-estimation/gce_budgeting.ipynb
