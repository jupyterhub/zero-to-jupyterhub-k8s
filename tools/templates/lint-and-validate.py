#!/usr/bin/env python3
"""
Lints and validates the chart's template files and their rendered output without
any cluster interaction. For this script to function, you must install yamllint
and kubeval.

- https://github.com/adrienverge/yamllint

pip install yamllint

- https://github.com/garethr/kubeval

LATEST=curl --silent "https://api.github.com/repos/garethr/kubeval/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/'
wget https://github.com/garethr/kubeval/releases/download/$LATEST/kubeval-linux-amd64.tar.gz
tar xf kubeval-darwin-amd64.tar.gz
mv kubeval /usr/local/bin
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

def lint(yamllint_config, values, kubernetes_version, output_dir, debug):
    """Calls `helm lint`, `helm template`, `yamllint` and `kubeval`."""

    print("### Clearing output directory")
    check_call([
        'mkdir', '-p', output_dir,
    ])
    check_call([
        'rm', '-rf', output_dir + '/*',
    ])

    print("### Linting started")
    print("### 1/4 - helm lint")
    helm_lint_cmd = [
        'helm', 'lint', '../../jupyterhub',
        '--values', values,
    ]
    if debug:
        helm_lint_cmd.append('--debug')
    check_call(helm_lint_cmd)

    print("### 2/4 - helm template")
    helm_template_cmd = [
        'helm', 'template', '../../jupyterhub',
        '--values', values,
        '--output-dir', output_dir
    ]
    if debug:
        helm_template_cmd.append('--debug')
    check_call(helm_template_cmd)

    print("### 3/4 - yamllint")
    check_call([
        'yamllint', '-c', yamllint_config, output_dir
    ])

    print("### 4/4 - kubeval")
    for filename in glob.iglob(output_dir + '/**/*.yaml', recursive=True):
        check_call([
            'kubeval', filename,
            '--kubernetes-version', kubernetes_version,
            '--strict',
            '--schema-location', 'https://raw.githubusercontent.com/consideRatio'
        ])

    print()
    print("### Linting and validation of templates finished: All good!")


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--debug', action='store_true', help='Run helm lint and helm template with the --debug flag')
    argparser.add_argument('--values', default='lint-and-validate-values.yaml', help='Specify Helm values in a YAML file (can specify multiple)')
    argparser.add_argument('--kubernetes-version', default='1.11.0', help='Version of Kubernetes to validate against')
    argparser.add_argument('--output-dir', default='rendered-templates', help='Output directory for the rendered templates. Warning: content in this will be wiped.')
    argparser.add_argument('--yamllint-config', default='yamllint-config.yaml', help='Specify a yamllint config')

    args = argparser.parse_args()

    lint(args.yamllint_config, args.values, args.kubernetes_version, args.output_dir, args.debug)
