# What is this folder about?

This folder contains tests that [pytest](https://docs.pytest.org/en/latest/) will run in our CI/CD pipeline on Travis. These tests must be able to speak directly to a running hub within a Kubernetes cluster etc. In practice, the tests will be set up using a `dev` script.
