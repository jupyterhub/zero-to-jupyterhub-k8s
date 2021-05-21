(cost)=

# Appendix: Projecting deployment costs

```{admonition} Clarification on cost projections
:class: warning

As a non-profit research project, Project Jupyter does not offer,
recommend, or sell cloud deployment services for JupyterHub.

The information in this section is offered as guidance as requested
by our users. We **caution** that costs can vary widely based
on providers selected and your use cases.
```

## Cost calculators for cloud providers

Below are several links to cost estimators for cloud providers:

- [Google Cloud Platform cost calculator](https://cloud.google.com/products/calculator/)
- [Amazon AWS cost calculator](https://calculator.s3.amazonaws.com/index.html)
- [Microsoft Azure cost claculator](https://azure.microsoft.com/en-us/pricing/calculator/)

## Factors influencing costs

Cost estimates depend highly on your deployment setup. Several factors that
significantly influence cost estimates, include:

- Computational resources provided to users
- Number of users
- Usage patterns of users

### Computational Resources

**Memory (RAM)** makes up the largest part of a cost estimate. More RAM means
that your users will be able to work with larger datasets with more
flexibility, but it can also be expensive.

**Persistent storage for users**, if needed, is another element that will impact
the cost estimate. If users don't have persistent storage, then disks will be
wiped after users finish their sessions. None of their changes will be saved.
This requires significantly fewer storage resources, and also results in faster
load times.

For an indicator of how costs scale with computational resources, see the
[Google Cloud pricing page](https://cloud.google.com/compute/all-pricing).

### Users

The number of users has a direct relationship to cost estimates. Since a
deployment may support different types of users (i.e. researchers, students,
instructors) with varying hardware and storage needs, take into account both the
type of users and the number per type.

### User usage patterns

Another important factor is what usage pattern your users will have. Will they
all use the JupyterHub at once, such as during a large class workshop?
will users use JupyterHub at different times of day?

The usage patterns and peak load on the system have important implications for
the resources you need to provide. In the future JupyterHub will have
auto-scaling functionality, but currently it does not. This means that you need
to provision resources for the _maximum_ expected number of users at one time.

## Examples

Here are a few examples that describe different use cases and the amount of
resources used by a particular JupyterHub implementation. There are many
factors that go into these estimates, and you should expect that your actual
costs may vary significantly under other conditions.

### Data 8

The Data 8 course at UC Berkeley used a JupyterHub to coordinate all course
material and to provide a platform where students would run their code. This
consisted of many hundreds of students, who had minimal requirements in terms
of CPU and memory usage. Ryan Lovett put together a short Jupyter notebook
[estimating the cost for computational resources][estimating the cost for computational resources] depending on the student
needs.

[estimating the cost for computational resources]: https://github.com/data-8/jupyterhub-k8s/blob/HEAD/docs/cost-estimation/gce_budgeting.ipynb
