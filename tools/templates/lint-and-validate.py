#!/usr/bin/env python3
"""
Lints and validates the chart's template files and their rendered output without
any cluster interaction. For this script to function, you must install yamllint
and kubeval.

USAGE:

  tools/templates/lint-and-validate.py

DEPENDENCIES:

yamllint: https://github.com/adrienverge/yamllint

  pip install yamllint

kubeval: https://github.com/instrumenta/kubeval

  LATEST=$(curl --silent "https://api.github.com/repos/instrumenta/kubeval/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
  wget https://github.com/instrumenta/kubeval/releases/download/$LATEST/kubeval-linux-amd64.tar.gz
  tar xf kubeval-linux-amd64.tar.gz
  sudo mv kubeval /usr/local/bin
"""

import os
import sys
import argparse
import glob
import pipes
import subprocess

os.chdir(os.path.dirname(sys.argv[0]))

def check_call(cmd, **kwargs):
    """Run a subcommand and exit if it fails"""
    try:
        subprocess.check_call(cmd, **kwargs)
    except subprocess.CalledProcessError as e:
        print(
            "`{}` exited with status {}".format(
                ' '.join(map(pipes.quote, cmd)),
                e.returncode,
            ),
            file=sys.stderr,
        )
        sys.exit(e.returncode)

def lint(yamllint_config, values, kubernetes_versions, output_dir, debug):
    """Calls `helm lint`, `helm template`, `yamllint` and `kubeval`."""

    print("### Clearing output directory")
    check_call([
        'mkdir', '-p', output_dir,
    ])
    check_call([
        'rm', '-rf', output_dir + '/*',
    ])

    print("### Linting started")
    print("### 1/4 - helm lint: lint helm templates")
    helm_lint_cmd = [
        'helm', 'lint', '../../jupyterhub',
        '--values', values,
    ]
    if debug:
        helm_lint_cmd.append('--debug')
    check_call(helm_lint_cmd)

    print("### 2/4 - helm template: generate kubernetes resources")
    helm_template_cmd = [
        'helm', 'template', '../../jupyterhub',
        '--values', values,
        '--output-dir', output_dir
    ]
    if debug:
        helm_template_cmd.append('--debug')
    check_call(helm_template_cmd)

    print("### 3/4 - yamllint: yaml lint generated kubernetes resources")
    check_call([
        'yamllint', '-c', yamllint_config, output_dir
    ])

    print("### 4/4 - kubeval: validate generated kubernetes resources")
    for kubernetes_version in kubernetes_versions.split(","):
        print("#### kubernetes_version ", kubernetes_version)
        for filename in glob.iglob(output_dir + '/**/*.yaml', recursive=True):
            check_call([
                'kubeval', filename,
                '--kubernetes-version', kubernetes_version,
                '--strict',
            ])

    print()
    print("### Linting and validation of helm templates and generated kubernetes resources OK!")


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--debug', action='store_true', help='Run helm lint and helm template with the --debug flag')
    argparser.add_argument('--values', default='lint-and-validate-values.yaml', help='Specify Helm values in a YAML file (can specify multiple)')
    argparser.add_argument('--kubernetes-versions', default='1.15.0', help='List of Kubernetes versions to validate against separated by ","')
    argparser.add_argument('--output-dir', default='rendered-templates', help='Output directory for the rendered templates. Warning: content in this will be wiped.')
    argparser.add_argument('--yamllint-config', default='yamllint-config.yaml', help='Specify a yamllint config')

    args = argparser.parse_args()

    lint(args.yamllint_config, args.values, args.kubernetes_versions, args.output_dir, args.debug)
