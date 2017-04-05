#/usr/bin/python3

"""Provides read and write access to Kubernetes API"""
import logging
import sys

from kubernetes import client, config

from utils import get_pod_host_name, get_pod_memory_request, \
    get_node_memory_capacity, check_list_intersection

scale_logger = logging.getLogger("scale")
logging.getLogger("kubernetes").setLevel(logging.WARNING)


class k8s_control:

    """Provides read and write access to Kubernetes API,
    and environment settings, including goals for the
    cluster always use the node and pods status at the
    time it was initiated

    self.pods omits certain pods based on settings"""

    def __init__(self, options):
        """ Needs to be initialized with options as an
        instance of settings"""
        self.context = self.configure_new_context(options.context)
        self.options = options
        self.v1 = client.CoreV1Api()
        self.pods = self.get_pods()
        self.nodes = self.get_nodes()
        self.critical_node_names = self.get_critical_node_names()
        self.critical_node_number = len(self.critical_node_names)
        self.noncritical_nodes = list(filter(lambda node: node.metadata.name not in self.critical_node_names,
                                             self.nodes))

    def configure_new_context(self, new_context):
        """ Loads .kube config to instantiate kubernetes
        with specified context"""
        contexts, _ = config.list_kube_config_contexts()
        try:
            contexts = [c['name'] for c in contexts]
            context_to_activate = list(
                filter(lambda context: new_context in context, contexts))
            assert len(context_to_activate) == 1  # avoid undefined behavior
            context_to_activate = context_to_activate[0]
        except (TypeError, IndexError):
            scale_logger.exception("Could not load context %s\n" % new_context)
            sys.exit(1)
        except AssertionError:
            scale_logger.fatal("Vague context specification")
            sys.exit(1)
        config.load_kube_config(context=context_to_activate)
        return context_to_activate

    def get_nodes(self):
        """Return a list of v1.Node"""
        scale_logger.debug("Getting all nodes in the cluster")
        return self.v1.list_node().items

    def get_pods(self):
        """Return a list of v1.Pod that needn't be omitted"""
        result = []
        scale_logger.debug("Getting all pods in all namespaces")
        pods = self.v1.list_pod_for_all_namespaces().items
        for pod in pods:
            if not (check_list_intersection(self.options.omit_labels, pod.metadata.labels) or
                    pod.metadata.namespace in self.options.omit_namespaces):
                result.append(pod)
        return result

    def show_nodes_status(self):
        """Print the status of all nodes in the cluster"""
        print(
            "Node name \t\t Num of pods on node \t Schedulable? \t Preemptible?")
        for node in self.nodes:
            print("%s\t%i\t%s\t%s" %
                  (node.metadata.name,
                   self.get_pods_number_on_node(node),
                   "U" if node.spec.unschedulable else "S",
                   "N" if node.metadata.name in self.critical_node_names else "P"
                   ))

    def set_unschedulable(self, node_name, value=True):
        """Set the spec key 'unschedulable'"""
        scale_logger.debug(
            "Setting %s node's unschedulable property to %r", node_name, value)
        assert node_name not in self.critical_node_names

        new_node = client.V1Node(
            api_version="v1",
            kind="Node",
            metadata=client.V1ObjectMeta(name=node_name),
            spec=client.V1NodeSpec(unschedulable=value)
        )
        # TODO: exception handling
        self.v1.patch_node(node_name, new_node)

    def get_total_cluster_memory_usage(self):
        """Gets the total memory usage of 
        all student pods"""
        total_mem_usage = 0
        for pod in self.pods:
            total_mem_usage += get_pod_memory_request(pod)
        return total_mem_usage

    def get_total_cluster_memory_capacity(self):
        """Returns the total memory capacity of all nodes, as student
        pods can be scheduled on any node that meets its Request criteria"""
        total_mem_capacity = 0
        for node in self.nodes:
            total_mem_capacity += get_node_memory_capacity(node)
        return total_mem_capacity

    def get_critical_node_names(self):
        """Return a list of nodes where critical pods
        are running"""
        result = []
        for pod in self.pods:
            if not check_list_intersection(pod.metadata.labels, self.options.preemptible_labels):
                pod_hostname = get_pod_host_name(pod)
                if pod_hostname not in result:
                    result.append(pod_hostname)
        return result

    def get_pods_number_on_node(self, node):
        """Return the effective number of pods on the node
        TODO: There must be a better way to determine number
        of running pods on node"""
        result = 0
        for pod in self.pods:
            if get_pod_host_name(pod) == node.metadata.name:
                result += 1
        return result

    def get_cluster_name(self):
        """Return the full name of the cluster"""
        return self.context

    def get_num_schedulable(self):
        """Return number of nodes schedulable AND NOT
        IN THE LIST OF CRITICAL NODES"""
        result = 0
        for node in self.noncritical_nodes:
            if not node.spec.unschedulable:
                result += 1
        return result

    def get_num_unschedulable(self):
        """Return number of nodes unschedulable

        ASSUMING CRITICAL NODES ARE SCHEDULABLE"""
        result = 0
        for node in self.nodes:
            if node.spec.unschedulable:
                result += 1
        return result


if __name__ == "__main__":
    import settings
    options = settings.settings()
    options.context = options.default_context
    k8s = k8s_control(options)
    print("Displaying information of cluster %s\n" % k8s.get_cluster_name())
    k8s.show_nodes_status()
    print("Current memory usage is %i" % k8s.get_total_cluster_memory_usage())
    print("Total memory capacity is %i" %
          k8s.get_total_cluster_memory_capacity())
