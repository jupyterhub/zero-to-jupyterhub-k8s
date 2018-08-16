- why return something from the test function?
- maybe move all the test_api_... functions into a new test_api.py file and rename them test_create_user instead of test_api_create_user?
- we need to make sure we are absolutely in the right directory before we run this. Maybe test that .kube etc exist and that some other directories and files we know should be in the repo at a certain place are exactly where we think they are so this script can be sure it is not about to rm -rf something the user did want to keep :)
    you can use "$(dirname "$0")" to get the directory.
    In general, ~everything should be using absolute paths here, especially deletions.
- Let's delete the unused Vagrantfile's
- Let's use helm version in order to wait for tiller

"this could just be $SUDO"

Instead of unsetting and resetting -u, this can be ${CICD:-}, which explicitly defaults to an empty string if undefined.

autocomplete:
We also probably shouldn't be setting up autocompletion in a script for CI. That's up to users' own environments, so let's remove this block.

remove the prefixes on the scripts:
    One change I would like to avoid: the number prefixes on the scripts I think are detrimental. Adding a number may indicate a certain amount of order, but they also mean that any changes/additions also requires renaming every file that comes after. Going back to simple, descriptive names is probably better in the long run.


minikube update-context


CONSIDER:
Run checks that which kubectl which minikube and which helm points to the binary in repo.