Estimating costs
================

It is difficult to estimate costs exactly, because this depends highly on your
particular setup. In general, there are a few primary factors that control
cost:

1. What kind of hardware do your users need?
2. How many users do you have?
3. What usage pattern will your users have?

Hardware
--------
The largest driver of cost in hardware is memory (RAM). More RAM means that your
users will be able to work with larger datasets with more flexibility, but it
can also be expensive. As a general rule, costs associated with RAM scale
at <XXX> cost.

Another consideration is whether to allow your users to have persistent storage.
If users don't have persistant storage, then disks will be wiped once users
are finished with their sessions. None of their changes will be saved. This
requires significantly fewer storage resources, and also results in faster
load times. Storage roughly scales at <XXX> cost.

User usage patterns
-------------------
Another important factor is what usage pattern your users will have. Will they
all use the JupyterHub at once? Or will their usage be more spread out
evenly over time? This has important implications for the resources you need
to provide. In the future JupyterHub will have auto-scaling functionality,
but currently it does not. This means that you need to provision resources
for the *maximum* expected number of users at one time.


Examples
--------
Here are a few examples that describe the use cases and amount of resources
used by a particular JupyterHub implementation, and how much it might cost.

Data 8
~~~~~~
The Data 8 course at UC Berkeley used a JupyterHub to coordinate all course
material and to provide a platform where students would run their code. This
consisted of many hundreds of students, who had minimal requirements in terms
of CPU and memory usage. Ryan Lovett put together `a short jupyter notebook <https://github.com/data-8/jupyterhub-k8s/blob/master/docs/cost-estimation/gce_budgeting.ipynb>`_ estimating the cost for computational resources depending on the student needs.
