#!/usr/bin/python

import subprocess
import sys
import yaml

def count_pods(namespace):
	cmd = ['kubectl', '--namespace='+namespace, 'get', 'pods',
		'-o=custom-columns=NAME:.metadata.name']
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
	line = p.readline()
	count = 0
	while line:
		if line.startswith(b'jupyter-'): count += 1
		line = p.readline()
		continue
	p.close()
	return count

NAMESPACES = ['datahub', 'prob140', 'stat28']
USERS_PER_NODE = 7
CLUSTER = 'prod'
POD_THRESHOLD = 0.9
BUMP_INCREMENT = 2

cmd = ['gcloud', 'container', 'clusters', 'describe', CLUSTER]
p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
buf = p.read()
p.close()

try:
	description = yaml.load(buf)
except Exception as e:
	print(str(e))
	sys.exit(1)

node_count = description['currentNodeCount']
max_pods = node_count * USERS_PER_NODE

cur_pods = 0
for ns in NAMESPACES:
	cur_pods += count_pods(ns)

if cur_pods < POD_THRESHOLD * max_pods:
	print(cur_pods)
	sys.exit(0)

new_node_count = node_count + BUMP_INCREMENT
cmd = ['gcloud', 'container', 'clusters', 'resize', CLUSTER, '--size',
	str(new_node_count)]
print(' '.join(cmd))
p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
buf = p.read()
p.close()
