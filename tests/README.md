# What is this folder about?

We have setup tests for [pytest](https://docs.pytest.org/en/latest/) that will run in our CI/CD pipeline on Travis. These test assumes it is able to speak directly to a running hub within a Kubernetes cluster etc. In practice, they assume you have been using `dev` script to set it all up.
