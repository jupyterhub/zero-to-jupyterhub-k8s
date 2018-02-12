.. _cost:

Estimating costs
================

Cost estimates depend highly on your deployment setup. Several factors that
significantly influence cost estimates, include:

- Computational resources provided to users
- Number of users
- Usage patterns of users

Computational Resources
-----------------------

**Memory (RAM)** makes up the largest part of a cost estimate. More RAM means
that your users will be able to work with larger datasets with more
flexibility, but it can also be expensive.

**Persistent storage for users**, if needed, is another element that will impact
the cost estimate. If users don't have persistent storage, then disks will be
wiped after users finish their sessions. None of their changes will be saved.
This requires significantly fewer storage resources, and also results in faster
load times.

For an example of how costs scale with computational resources, see the
`Google Cloud pricing page <https://cloud.google.com/compute/pricing>`_.

Interactive Cost Estimator
--------------------------

We've put together a small notebook that can help you estimate your costs
for a JupyterHub instance. The button below will take you to an interactive
notebook served with `Binder <https://mybinder.org>`_. Run the cells and
you'll be able to choose the computational requirements you have, as well as
draw a pattern of usage you expect over time. It will estimate the costs for
you.

.. warning::

   **The cost estimator is a very rough estimate.** It is based on Google Cloud
   Engine instances served from Oregon. Costs will vary based on your
   location / provider, and will be highly variable if you implement any kind
   of auto-scaling. Treat it as an order-of-magnitude estimate, not a hard rule.

.. raw:: html

   <a target="_blank" href="http://mybinder.org/v2/gh/jupyterhub/zero-to-jupyterhub-k8s/master?filepath=doc/ntbk/draw_function.ipynb">
   <button style="background-color: rgb(235, 119, 55); border: 1px solid; border-color: black; color: white; padding: 15px 32px; text-align: center; text-decoration: none; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 8px;">Launch the Cost Estimator</button></a>

For a description of how these costs are broken down, see below.

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
