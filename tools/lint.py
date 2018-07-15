#!/usr/bin/env python3
"""
Lints the chart's yaml files without any cluster interaction. For this script to
function, you must install yamllint and kubeval.

- https://github.com/adrienverge/yamllint
- https://github.com/garethr/kubeval
"""


import os
import sys
import argparse
import glob
import subprocess

os.chdir(os.path.dirname(sys.argv[0]))

def lint(config, values, kubernetes_version):
    """Calls `helm lint`, `helm template`, `yamllint` and `kubeval`."""

    output = 'lint-output'

    print("### Clearing output directory")
    subprocess.check_call([
        'mkdir', '-p', output,
    ])
    subprocess.check_call([
        'rm', '-rf', output + '/*',
    ])

    print("### Linting started")
    print("### 1/4 - helm lint")
    subprocess.check_call([
        'helm', 'lint', '../jupyterhub',
        '--values', values,
    ])

    print("### 2/4 - helm template")
    subprocess.check_call([
        'helm', 'template', '../jupyterhub',
        '--values', values, 
        '--output-dir', output
    ])
    
    print("### 3/4 - yamllint")
    subprocess.check_call([
        'yamllint', '-c', config, output
    ])

    print("### 4/4 - kubeval")
    for filename in glob.iglob(output + '/**/*.yaml', recursive=True):
        subprocess.check_call([
            'kubeval', filename,
            '--kubernetes-version', kubernetes_version,
            '--strict',
            '--schema-location', 'https://raw.githubusercontent.com/consideRatio'
        ])

    print()
    print("### Linting finished: All good!")


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--config', default='lint-config.yaml', help='Specify the yamllint config')
    argparser.add_argument('--values', default='lint-chart-values.yaml', help='Specify additional chart value files')
    argparser.add_argument('--output', default='lint-output', help='Specify an output directory')
    argparser.add_argument('--kubernetes-version', default='1.10.4', help='Validate against this kubernetes version')
    args = argparser.parse_args()
    
    lint(args.config, args.values, args.kubernetes_version)
