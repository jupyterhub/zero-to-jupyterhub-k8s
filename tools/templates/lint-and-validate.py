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

def lint(yamllint_config, chart_values, kubernetes_version, output_dir):
    """Calls `helm lint`, `helm template`, `yamllint` and `kubeval`."""

    print("### Clearing output directory")
    subprocess.check_call([
        'mkdir', '-p', output_dir,
    ])
    subprocess.check_call([
        'rm', '-rf', output_dir + '/*',
    ])

    print("### Linting started")
    print("### 1/4 - helm lint")
    subprocess.check_call([
        'helm', 'lint', '../../jupyterhub',
        '--values', chart_values,
    ])

    print("### 2/4 - helm template")
    subprocess.check_call([
        'helm', 'template', '../../jupyterhub',
        '--values', chart_values, 
        '--output-dir', output_dir
    ])
    
    print("### 3/4 - yamllint")
    subprocess.check_call([
        'yamllint', '-c', yamllint_config, output_dir
    ])

    print("### 4/4 - kubeval")
    for filename in glob.iglob(output_dir + '/**/*.yaml', recursive=True):
        subprocess.check_call([
            'kubeval', filename,
            '--kubernetes-version', kubernetes_version,
            '--strict',
            '--schema-location', 'https://raw.githubusercontent.com/consideRatio'
        ])

    print()
    print("### Linting and validation of templates finished: All good!")


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--yamllint-config', default='yamllint-config.yaml', help='Specify the yamllint config')
    argparser.add_argument('--chart-values', default='chart-values.yaml', help='Specify additional chart value files')
    argparser.add_argument('--kubernetes-version', default='1.10.5', help='Validate against this Kubernetes version')
    argparser.add_argument('--output-dir', default='rendered-templates', help='Specify an output directory for the rendered templates')
    args = argparser.parse_args()
    
    lint(args.yamllint_config, args.chart_values, args.kubernetes_version, args.output_dir)
