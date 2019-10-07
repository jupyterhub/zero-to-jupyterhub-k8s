#!/usr/bin/env python3
"""
Checks that can be made:
1. Are we using the correct cluster? If not KUBECONFIG is set explicitly in an
   env var or through an .env file, we could fail.
2. Are the required dependencies available on path or in the ./bin folder?

Requirements:
- KUBECONFIG is set
- dev-config.yaml is used
-

.env file:
    GITHUB_ACCESS_TOKEN     - for release changes and contributors
    KUBECONFIG              - for kind clusters
    HELM_HOME               - for plugins
    CHARTPRESS_COMMIT_RANGE - ?
"""

import argparse
import functools
import os
import pipes
import shutil
import subprocess
import sys

import dotenv


def depend_on(binaries=[], envs=[]):
    def decorator_depend_on(func):
        @functools.wraps(func)
        def wrapper_depend_on(*args, **kwargs):
            missing_binaries = []
            for binary in binaries:
                if shutil.which(binary) is None:
                    missing_binaries.append(binary)
            missing_envs = []
            for env in envs:
                if os.environ.get(env) is None:
                    missing_envs.append(env)

            if missing_binaries or missing_envs:
                print('Exiting due to missing dependencies for "%s"' % func.__name__)
                print("- Binaries: %s" % missing_binaries)
                print("- Env vars: %s" % missing_envs)

                sys.exit(1)
            else:
                return func(*args, **kwargs)

        return wrapper_depend_on

    return decorator_depend_on


@depend_on(binaries=["kind"], envs=["KUBECONFIG"])
def kind_start(force):
    # check if there is a cluster existing already
    # then delete it

    # start a new cluster with a fixed name, kubernetes version
    # configure a default namespace
    
    # install calico
    # install helm
    pass


@depend_on(binaries=["kind"], envs=["KUBECONFIG"])
def kind_stop():
    # delete the kind cluster
    pass


@depend_on(binaries=["chartpress", "helm"], envs=["KUBECONFIG"])
def upgrade():
    # consider commit-range
    # run chartpress
    # (conditionally) load images to a kind cluster
    # helm upgrade / install with dev-config
    # (?) port-forward
    pass


@depend_on(binaries=["kubectl", "pytest"], envs=["KUBECONFIG"])
def test():
    # pytest
    pass


@depend_on(binaries=["kubectl", "kubeval", ], envs=[])
def check_templates():
    # lint-and-validate script
    pass


@depend_on(binaries=["black"], envs=[])
def check_python_code(apply):
    # black
    pass


@depend_on(binaries=[], envs=["GITHUB_ACCESS_TOKEN"])
def changelog():
    # req: GITHUB_ACCESS_TOKEN

    # gitlab-activity
    pass


def _check_output(cmd, **kwargs):
    """Run a subcommand and exit if it fails"""
    try:
        return subprocess.check_output(cmd, **kwargs)
    except subprocess.CalledProcessError as e:
        print(
            "`{}` exited with status {}".format(
                " ".join(map(pipes.quote, cmd)), e.returncode
            ),
            file=sys.stderr,
        )
        sys.exit(e.returncode)


def _get_argparser():
    _ = argparse.ArgumentParser(
        description="Local development help for jupyterhub/zero-to-jupyterhub-k8s"
    )
    _cmds = _.add_subparsers(title="Commands", dest="cmd", required=True)

    kind = _cmds.add_parser(
        "kind", help="Kubernetes-in-Docker (kind) cluster management."
    )
    kind_cmds = kind.add_subparsers(title="Commands", dest="sub_cmd", required=True)
    kind_start = kind_cmds.add_parser(
        "start", help="Start and initialize a kind Kubernetes cluster."
    )
    kind_start.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="If the cluster is already started, delete it and start a new.",
    )
    kind_stop = kind_cmds.add_parser(
        "stop", help="Stop and delete a previously started kind Kubernetes cluster."
    )

    upgrade = _cmds.add_parser(
        "upgrade", help="Install or upgrade the Helm chart in the Kubernetes cluster."
    )

    test = _cmds.add_parser(
        "test", help="Run tests on the deployed Helm chart in the Kubernetes cluster."
    )

    check = _cmds.add_parser(
        "check", help="Run checks on your developed helm templates and python code."
    )
    check_cmds = check.add_subparsers(title="Commands", dest="sub_cmd", required=True)
    check_templates = check_cmds.add_parser(
        "templates",
        help="Run checks on the Helm templates and the Kubernetes resources they generate using: helm lint, helm templates, yamllint, and kubeval.",
    )
    check_python_code = check_cmds.add_parser(
        "python-code", help="Run checks on the python code using: black."
    )
    check_python_code.add_argument(
        "--apply",
        action="store_true",
        help="Apply autoformatting to the Python code files.",
    )

    changelog = _cmds.add_parser(
        "changelog",
        help="Generate a changelog since last release using: choldgraf/github-activity.",
    )

    return _


if __name__ == "__main__":
    # parse passed command line arguments
    argparser = _get_argparser()
    args = argparser.parse_args()
    
    # DEBUGGING:
    print(args)

    # load environment variables from the .env file
    dotenv.load_dotenv()

    # run suitable command and pass arguments
    if args.cmd == "kind":
        if args.sub_cmd == "start":
            kind_start(force=args.force)
        if args.sub_cmd == "stop":
            kind_stop()

    if args.cmd == "upgrade":
        upgrade()

    if args.cmd == "test":
        test()

    if args.cmd == "check":
        if args.sub_cmd == "templates":
            check_templates()
        if args.sub_cmd == "python-code":
            check_python_code(apply=args.apply)

    if args.cmd == "changelog":
        changelog()
