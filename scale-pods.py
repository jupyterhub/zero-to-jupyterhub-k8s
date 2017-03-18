#!/usr/bin/env python3

import subprocess
import sys
import yaml

def count_pods(namespace, prefix=b'jupyter-'):
	'''Count all "jupyter-" pods in a namespace.'''
	cmd = ['kubectl', '--context='+KUBECTL_CONTEXT,
		'--namespace='+namespace, 'get', 'pods',
		'-o=custom-columns=NAME:.metadata.name']
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
	line = p.readline()
	count = 0
	while line:
		if line.startswith(prefix): count += 1
		line = p.readline()
		continue
	p.close()
	return count

def get_hub_pod(namespace, prefix=b'hub-deployment'):
	'''Return the name of the hub pod.'''
	cmd = ['kubectl', '--context='+KUBECTL_CONTEXT,
		'--namespace='+namespace, 'get', 'pods',
		'-o=custom-columns=NAME:.metadata.name']
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
	line = p.readline()
	while line:
		if line.startswith(prefix): return line.strip()
		line = p.readline()
		continue
	p.close()
	return ''

def get_singleuser_image(namespace, hub_pod):
	'''Return the name:tag of the hub's singleuser image.'''
	cmd = ['kubectl', '--context='+KUBECTL_CONTEXT,
		'--namespace='+namespace, 'get', 'pod', '-o=yaml',
		hub_pod]
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
	buf = p.read()
	p.close()

	description = yaml.load(buf)
	image = ''
	for env in description['spec']['containers'][0]['env']:
		if env['name'] == 'SINGLEUSER_IMAGE':
			image = env['value']
			break

	return image

## MAIN
NAMESPACES = ['datahub', 'prob140', 'stat28']
CLUSTER = 'prod'
KUBECTL_CONTEXT = 'gke_data-8_us-central1-a_prod'
POD_THRESHOLD = 0.9
BUMP_INCREMENT = 2

NODE_POOL = 'highmem-pool'
USERS_PER_NODE = 24

# How many nodes do we have?
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

# How many pods does that accommodate?
max_pods = node_count * USERS_PER_NODE

# How many pods are active?
cur_pods = 0
for ns in NAMESPACES:
	cur_pods += count_pods(ns)

if cur_pods < POD_THRESHOLD * max_pods:
	print(cur_pods)
	sys.exit(0)

new_node_count = node_count + BUMP_INCREMENT
cmd = ['gcloud', '--quiet', 'container', 'clusters', 'resize', CLUSTER,
	'--node-pool='+NODE_POOL, '--size', str(new_node_count)]
print(' '.join(cmd))
p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
buf = p.read()
p.close()

# Populate latest singleuser image on all nodes
for ns in NAMESPACES:
	hub_pod = get_hub_pod(ns)
	image = get_singleuser_image(ns, hub_pod)
	if not image: continue

	cmd = ['./populate.bash', CLUSTER, image]
	print(' '.join(cmd))
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
	buf = p.read()
	p.close()
