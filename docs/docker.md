# Docker Containers

Using a stack of derived containers allows us to:

1. Disable caching, which should reliably pick up changes in the build scripts
1. Realize quicker build times

## Guidelines

Derived images can only change the following:

1. Set new environment variables
1. Add conda, pip, and apt packages
1. Add jupyter extensions
