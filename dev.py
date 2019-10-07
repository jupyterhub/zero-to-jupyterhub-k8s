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
import re
import shutil
import subprocess
import sys
import textwrap

import dotenv
import colorama

colorama.init()

def depend_on(binaries=[], envs=[]):
    """
    A decorator to ensure the function is called with the relevant binaries
    available and relevant environment variables set.
    """
    def decorator_depend_on(func):
        @functools.wraps(func)
        def wrapper_depend_on(*args, **kwargs):
            missing_binaries = []
            for binary in binaries:
                if shutil.which(binary) is None:
                    missing_binaries.append(binary)
            missing_envs = []
            for env in envs:
                if not os.environ.get(env):
                    missing_envs.append(env)

            if missing_binaries or missing_envs:
                print('Exiting due to missing dependencies for "%s"' % func.__name__)
                print("- Binaries: %s" % missing_binaries)
                print("- Env vars: %s" % missing_envs)
                print("")
                if missing_binaries:
                    print("Install and make the binaries available on your PATH!")
                if missing_envs:
                    print("Update your .env file!")
                sys.exit(1)
            else:
                return func(*args, **kwargs)

        return wrapper_depend_on

    return decorator_depend_on


@depend_on(binaries=["kind"], envs=["KUBE_VERSION"])
def kind_start(recreate):
    # check for a existing jh-dev cluster and conditionally delete it
    kind_clusters = _run(
        cmd=["kind", "get", "clusters"],
        print_command=False,
        capture_output=True,
    )
    kind_cluster_exist = bool(re.search(r"\bjh-dev\b", kind_clusters))
    if kind_cluster_exist:
        print('The kind cluster "jh-dev" exists already.')
        if recreate:
            _run(["kind", "delete", "cluster", "--name", "jh-dev"])
        else:
            sys.exit(1)


    # start a new cluster with a fixed name, kubernetes version
    print('Creating kind cluster "jh-dev".')
    _run([
        "kind", "create", "cluster",
        "--name", "jh-dev",
        "--image", "kindest/node:v%s" % os.environ["KUBE_VERSION"],
        "--config", "ci/kind-config.yaml",
    ])
    
    kubeconfig_path = _run(
        cmd=[
            "kind", "get", "kubeconfig-path",
            "--name", "jh-dev",
        ],
        print_command=False,
        capture_output=True,
    )

    if os.environ["KUBECONFIG"] != kubeconfig_path:
        print("Updating your .env file's KUBECONFIG value to \"%s\"" % kubeconfig_path)
        dotenv.set_key(".env", "KUBECONFIG", kubeconfig_path)
        os.environ["KUBECONFIG"] = kubeconfig_path

    print('Making "jh-dev" the default namespace in the cluster.')
    _run([
        "kubectl", "config", "set-context",
        "--current",
        "--namespace", "jh-dev",
    ])


    # To test network policies, we need a custom CNI like Calico. We have disabled
    # the default CNI through kind-config.yaml and will need to manually install a
    # CNI for the nodes to become Ready.
    # Setup daemonset/calico-etcd, a prerequisite for calico-node
    print("Installing a custom CNI: Calico (async, in cluster)")
    _run(
        cmd=[
            "kubectl", "apply",
            "-f", "https://docs.projectcalico.org/v3.9/getting-started/kubernetes/installation/hosted/etcd.yaml",
        ],
        print_end="",
    )
    # NOTE: A toleration to schedule on a node that isn't ready is missing, but
    #       this pod will be part of making sure the node can become ready.
    #
    #       toleration:
    #         - key: node.kubernetes.io/not-ready
    #           effect: NoSchedule
    _run(
        cmd=[
            "kubectl", "patch", "daemonset/calico-etcd",
            "--namespace", "kube-system",
            "--type", "json",
            "--patch", '[{"op":"add", "path":"/spec/template/spec/tolerations/-", "value":{"key":"node.kubernetes.io/not-ready", "effect":"NoSchedule"}}]',
        ],
        print_end="",
    )
    # Setup daemonset/calico-node, that will allow nodes to enter a ready state
    _run(
        cmd=[
            "kubectl", "apply",
            "-f", "https://docs.projectcalico.org/v3.9/getting-started/kubernetes/installation/hosted/calico.yaml",
        ],
        print_end="",
    )
    # NOTE: Connection details to daemonset/calico-etcd is missing so we need to
    #       manually add them.
    calico_etcd_endpoint = _run(
        cmd=[
            "kubectl", "get", "service/calico-etcd",
            "--namespace", "kube-system",
            "--output", "jsonpath=http://{.spec.clusterIP}:{.spec.ports[0].port}",
        ],
        print_command=False,
        capture_output=True,
    )
    _run(
        cmd=[
            "kubectl", "patch", "configmap/calico-config",
            "--namespace", "kube-system",
            "--type", "merge",
            "--patch", '{"data":{"etcd_endpoints":"%s"}}' % calico_etcd_endpoint,
        ],
        print_end="",
    )
    # NOTE: daemonset/calico-node pods' main container fails to start up without
    #       an additional environment variable configured to disable a check
    #       that we fail.
    #
    #       env:
    #         - name: FELIX_IGNORELOOSERPF
    #           value: "true"
    _run(
        cmd=[
            "kubectl", "patch", "daemonset/calico-node",
            "--namespace", "kube-system",
            "--type", "json",
            "--patch", '[{"op":"add", "path":"/spec/template/spec/containers/0/env/-", "value":{"name":"FELIX_IGNORELOOSERPF", "value":"true"}}]',
        ],
    )

    print("Waiting for Kubernetes nodes to become ready.")
    _run(
        # NOTE: kubectl wait has a bug relating to using the --all flag in 1.13
        #       at least Due to this, we wait only for the kind-control-plane
        #       node, which currently is the only node we start with kind but
        #       could be configured in kind-config.yaml.
        #
        #       ref: https://github.com/kubernetes/kubernetes/pull/71746
        cmd=[
            "kubectl", "wait", "node/jh-dev-control-plane",
            "--for", "condition=ready",
            "--timeout", "2m",
        ],
        error_callback=_log_wait_node_timeout,
    )

    print("Installing Helm's tiller asynchronously in the cluster.")
    _run(
        cmd=[
            "kubectl", "create", "serviceaccount", "tiller",
            "--namespace", "kube-system",
        ],
        print_end="",
    )
    _run(
        cmd=[
            "kubectl", "create", "clusterrolebinding", "tiller",
            "--clusterrole", "cluster-admin",
            "--serviceaccount", "kube-system:tiller",
        ],
        print_end="",
    )
    _run([
        "helm", "init",
        "--service-account", "tiller",
    ])

    print("Waiting for Helm's tiller to become ready in the cluster.")
    _run(
        cmd=[
            "kubectl", "rollout", "status", "deployment/tiller-deploy",
            "--namespace", "kube-system",
            "--timeout", "2m",
        ],
        error_callback=_log_tiller_rollout_timeout,
    )

    print('Kind cluster "jh-dev" successfully setup!')


@depend_on(binaries=["kind"], envs=[])
def kind_stop():
    print('Deleting kind cluster "jh-dev".')
    _run(["kind", "delete", "cluster", "--name", "jh-dev"])


@depend_on(binaries=["chartpress", "helm"], envs=["KUBECONFIG", "CHARTPRESS_COMMIT_RANGE"])
def upgrade(values):
    print("Building images and updating image tags if needed.")
    commit_range = os.environ.get(
        "TRAVIS_COMMIT_RANGE",
        os.environ["CHARTPRESS_COMMIT_RANGE"]
    )
    _run([
        "chartpress",
        "--commit-range", commit_range,
    ])
    # git --no-pager diff

    if "kind-config-jh-dev" in os.environ["KUBECONFIG"]:
        print("Loading the locally built images into the kind cluster.")
        cmd = [
            "python3", "ci/kind-load-docker-images.py",
            "--kind-cluster", "jh-dev",
        ]
        for value in values:
            cmd.append("--values")
            cmd.append(value)
        _run(cmd=cmd)


    print("Installing/upgrading the Helm chart on the Kubernetes cluster.")
    _run([
        "helm", "upgrade", "jh-dev", "./jupyterhub",
        "--install",
        "--namespace", "jh-dev",
        "--values", "dev-config.yaml",
        "--wait",
    ])

    print("Waiting for the proxy and hub to become ready.")
    _run(
        cmd=[
            "kubectl", "rollout", "status", "deployment/proxy",
            "--timeout", "1m",
        ],
        print_end=""
    )
    _run([
        "kubectl", "rollout", "status", "deployment/hub",
        "--timeout", "1m",
    ])

    # FIXME: we don't do any port-forwarding


@depend_on(binaries=["kubectl", "pytest"], envs=["KUBECONFIG"])
def test():
    _run(["pytest", "-v", "--exitfirst", "./tests"])


@depend_on(binaries=["helm", "yamllint", "kubeval"], envs=[])
def check_templates():
    kubernetes_versions = None
    kubernetes_versions = kubernetes_versions or os.environ.get("VALIDATE_KUBE_VERSIONS", None)
    kubernetes_versions = kubernetes_versions or os.environ.get("KUBE_VERSION", None)

    _run([
        "python3", "tools/templates/lint-and-validate.py",
         "--kubernetes-versions", kubernetes_versions,
    ])


@depend_on(binaries=["black"], envs=[])
def check_python_code(apply):
    raise NotImplementedError()
    # invoke black


@depend_on(binaries=[], envs=["GITHUB_ACCESS_TOKEN"])
def changelog():
    raise NotImplementedError()
    # invoke gitlab-activity


def _log_tiller_rollout_timeout():
    print("Helm's tiller never became ready!")
    _run(
        cmd=["kubectl", "describe", "nodes",],
        exit_on_error=False,
        print_end="",
    )
    _run(
        cmd=[
            "kubectl", "describe", "deployment/tiller",
            "--namespace", "kube-system",
        ],
        exit_on_error=False,
        print_end="",
    )
    _run(
        cmd=[
            "kubectl", "logs", "deployment/tiller",
            "--namespace", "kube-system",
        ],
        exit_on_error=False,
    )


def _log_wait_node_timeout():
    print("Kubernetes nodes never became ready")
    _run(
        cmd=["kubectl", "describe", "nodes",],
        exit_on_error=False,
        print_end="",
    )
    _run(
        cmd=[
            "kubectl", "describe", "calico-etcd",
            "--namespace", "kube-system",
        ],
        exit_on_error=False,
        print_end="",
    )
    _run(
        cmd=[
            "kubectl", "logs", "calico-etcd",
            "--namespace", "kube-system",
        ],
        exit_on_error=False,
        print_end="",
    )
    _run(
        cmd=[
            "kubectl", "describe", "calico-node",
            "--namespace", "kube-system",
        ],
        exit_on_error=False,
        print_end="",
    )
    _run(
        cmd=[
            "kubectl", "logs", "calico-node",
            "--namespace", "kube-system",
        ],
        exit_on_error=False,
    )


def _print_command(text):
    print(
        colorama.Style.BRIGHT +
        "$ " +
        colorama.Fore.GREEN +
        text +
        colorama.Style.RESET_ALL +
        colorama.Fore.WHITE +
        colorama.Style.DIM
    )

def _run(cmd, print_command=True, print_end="\n", print_error=True, error_callback=None, exit_on_error=True, **kwargs):
    """Run a subcommand and exit if it fails"""
    if kwargs.get("capture_output", None):
        if kwargs.get("text", None) is None:
            kwargs["text"] = True

        # FIXME: This is a workaround for Python 3.6 that won't be required in
        #        Python 3.7.
        del kwargs["capture_output"]
        kwargs["stdout"] = kwargs["stderr"] = subprocess.PIPE

    if print_command:
        _print_command(" ".join(map(pipes.quote, cmd)))
    completed_process = subprocess.run(cmd, **kwargs)
    if print_command:
        print(colorama.Style.RESET_ALL, end=print_end)

    if completed_process.returncode != 0:
        print(
            "`{}` errored ({})".format(" ".join(map(pipes.quote, cmd)), e.returncode),
            file=sys.stderr,
        )
        if error_callback:
            error_callback(cmd)
        if exit_on_error:
            sys.exit(e.returncode)

    if completed_process.stdout:
        return completed_process.stdout.strip()


def _get_argparser():
    _ = argparse.ArgumentParser(
        description="Local development help for jupyterhub/zero-to-jupyterhub-k8s"
    )

    _cmds = _.add_subparsers(title="Commands", dest="cmd")

    kind = _cmds.add_parser(
        "kind", help="Kubernetes-in-Docker (kind) cluster management."
    )

    kind_cmds = kind.add_subparsers(title="Commands", dest="sub_cmd")
    kind_start = kind_cmds.add_parser(
        "start", help="Start and initialize a kind Kubernetes cluster."
    )
    kind_start.add_argument(
        "--recreate",
        action="store_true",
        help="If the cluster is already started, delete it and start a new.",
    )
    kind_stop = kind_cmds.add_parser(
        "stop", help="Stop and delete a previously started kind Kubernetes cluster."
    )

    upgrade = _cmds.add_parser(
        "upgrade", help="Install or upgrade the Helm chart in the Kubernetes cluster."
    )
    upgrade.add_argument(
        "-f",
        "--values",
        action="append",
        default=["dev-config.yaml"],
        help="A Helm values file, this argument can be passed multiple times.",
    )

    test = _cmds.add_parser(
        "test", help="Run tests on the deployed Helm chart in the Kubernetes cluster."
    )

    check = _cmds.add_parser(
        "check", help="Run checks on your developed helm templates and python code."
    )
    check_cmds = check.add_subparsers(title="Commands", dest="sub_cmd")
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
    
    # initialize defaults and load environment variables from the .env file
    if not os.path.exists(".env"):
        default_dotenv_file = textwrap.dedent(
            """\
            ## Environment variables loaded and used by the ./dev script. They
            ## will take precedence over system variables.
            #
            ## GITHUB_ACCESS_TOKEN is needed to generate changelog entries etc.
            ##
            GITHUB_ACCESS_TOKEN=
            #
            ## CHARTPRESS_COMMIT_RANGE can help us avoids image rebuilds. If
            ## the main repo remote isn't named origin, correct it here.
            ##
            CHARTPRESS_COMMIT_RANGE=origin/master..HEAD
            #
            ## KUBECONFIG is required to be set explicitly in order to avoid
            ## potential modifications of non developer clusters. It should
            ## be to the path where the kubernetes config resides.
            ##
            KUBECONFIG=
            #
            ## KUBE_VERSION is used to create a kind cluster and as a fallback
            ## if you have not specified VALIDATE_KUBE_VERSIONS. Note that only
            ## versions that are found on kindest/node can be used.
            ##
            ## ref: https://hub.docker.com/r/kindest/node/tags
            ##
            # KUBE_VERSION=1.15.3
            #
            ## VALIDATE_KUBE_VERSIONS is used when you check your Helm
            ## templates. Are the generated Kubernetes resources valid
            ## resources for these Kubernetes versions?
            ##
            # VALIDATE_KUBE_VERSIONS=1.14.0,1.15.0
            """
        )
        with open('.env', 'w+') as f:
            f.write(default_dotenv_file)

    dotenv.load_dotenv(override=True)

    # run suitable command and pass arguments
    if args.cmd == "kind":
        if args.sub_cmd == "start":
            kind_start(recreate=args.recreate)
        if args.sub_cmd == "stop":
            kind_stop()

    if args.cmd == "upgrade":
        upgrade(args.values)

    if args.cmd == "test":
        test()

    if args.cmd == "check":
        if args.sub_cmd == "templates":
            check_templates()
        if args.sub_cmd == "python-code":
            check_python_code(apply=args.apply)

    if args.cmd == "changelog":
        changelog()
