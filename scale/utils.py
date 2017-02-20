#/usr/bin/python3

"""Kubernetes API access functions"""

from kubernetes import client, config
#import requests

config.load_kube_config()
v1 = client.CoreV1Api()


# def generate_url(host, port):
#    return "http://" + host + ':' + port + "/api/v1/"


def get_nodes():
    """Return a list of v1.Node"""
    return v1.list_node().items
#     r = requests.get(generate_url(API_HOST, API_PORT) +
#                      "nodes")
#     assert r.status_code == 200
#     try:
#         nodesList = json.loads(r.text)
#         return nodesList['items']
#     except Exception as e:
#         # FIXME: proper exception handling
#         print(str(e))
#         sys.exit(1)


def get_pods():
    """Return a list of v1.Pod"""
    return v1.list_pod_for_all_namespaces().items
#     r = requests.get(generate_url(API_HOST, API_PORT) +
#                      "pods")
#     assert r.status_code == 200
#     try:
#         podsList = json.loads(r.text)
#         return podsList['items']
#     except Exception as e:
#         # FIXME: proper exception handling
#         print(str(e))
#         sys.exit(1)


# def get_namespaces_name():
#     """Return a list of namespaces in the form of string"""
#     r = requests.get(generate_url(API_HOST, API_PORT) +
#                      "namespaces")
#     assert r.status_code == 200
#     result = []
#     try:
#         namespaces = json.loads(r.text)
#         for each in namespaces.items:
#             result.append(get_name(each))
#         return result
#     except Exception as e:
#         # FIXME: proper exception handling
#         print(str(e))
#         sys.exit(1)


def get_pod_host_name(pod):
    """Return the host node name of the pod"""
    # Based on Kubernetes API:
    # https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_podspec
    # ** API is unclear the value of nodeName flag after the pod is scheduled
    return pod.spec.node_name


def get_cluster_name(node=get_nodes()[0]):
    """Return the (guessed) name of the cluster"""
    node_name = get_name(node)
    parts = node_name.split('-')
    assert len(parts) > 2
    return parts[1]


def get_pod_name(pod):
    """Return the name of the pod"""
    return get_name(pod)


def get_node_name(node):
    """Return the name of the node"""
    return get_name(node)


def get_pod_namespace(pod):
    """Return the namespace of the pod"""
    return pod.metadata.namespace


def get_pod_type(pod):
    """Return the Type of the pod"""
    # TODO: May not be the best approach
    return get_pod_name(pod).split('-')[0]


def set_unschedulable(node_name, value=True):
    """Set the spec key 'unschedulable'"""
    new_node = client.V1Node(
        api_version="v1",
        kind="Node",
        metadata=client.V1ObjectMeta(name=node_name),
        spec=client.V1NodeSpec(unschedulable=value)
    )
    # TODO: exception handling
    v1.patch_node(node_name, new_node)


def get_name(resource):
    """ Return name of a node, return '' if
    an error occurred """
    try:
        return resource.metadata.name
    except Exception:
        return ''


def is_unschedulable(node):
    """Return the value of 'Unschedulable' of a node"""
    return node.spec.unschedulable
