#!/usr/bin/env python3
"""
Lints the chart's yaml files without any cluster interaction. For this script to
function, you must install yamllint and kubeval.

- https://github.com/adrienverge/yamllint
- https://github.com/garethr/kubeval
"""


import argparse
import glob
import subprocess

def lint(config, values, kubernetes_version):
    """Calls `helm lint`, `helm template` and `yamllint`."""

    output = 'lint-output'

    print("### helm lint")
    subprocess.check_call([
        'helm', 'lint', '../jupyterhub',
        '--values', values,
    ])

    print("### helm template")
    subprocess.check_call([
        'helm', 'template', '../jupyterhub',
        '--values', values, 
        '--output-dir', output
    ])
    
    print("### yamllint")
    subprocess.check_call([
        'yamllint', '-c', config, output
    ])

    print("### kubeval")
    for filename in glob.iglob(output + '/**/*.yaml', recursive=True):
        subprocess.check_call([
            'kubeval', filename,
            '--kubernetes-version', kubernetes_version,
            '--strict'
        ])

    print()
    print("### All good!")


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--config', default='lint-config.yaml', help='Specify the yamllint config')
    argparser.add_argument('--values', default='lint-chart-values.yaml', help='Specify additional chart value files')
    argparser.add_argument('--output', default='lint-output', help='Specify an output directory')
    argparser.add_argument('--kubernetes-version', default='1.8.0', help='Validate against this kubernetes version')
    args = argparser.parse_args()
    
    lint(args.config, args.values, args.kubernetes_version)
