package main

import (
	"context"
	"flag"
	"fmt"
	v1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/errors"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/util/validation"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/clientcmd"
	"k8s.io/client-go/util/homedir"
	"log"
	"os"
	"path/filepath"
	"strings"
)

func buildConfig(kubeconfig string) (*rest.Config, error) {
	// load kubeconfig from command line
	if kubeconfig != "" {
		cfg, err := clientcmd.BuildConfigFromFlags("", kubeconfig)
		if err != nil {
			return nil, err
		}
		log.Printf("Using kubeconfig %v.", kubeconfig)
		return cfg, nil
	}

	// try the default location HOME/.kube/config
	if home := homedir.HomeDir(); home != "" {
		kubeconfig = filepath.Join(home, ".kube", "config")
		cfg, err := clientcmd.BuildConfigFromFlags("", kubeconfig)
		if err == nil {
			log.Printf("Using kubeconfig %v.", kubeconfig)
			return cfg, nil
		}
	}

	// try in-cluster auth
	cfg, err := rest.InClusterConfig()
	if err != nil {
		return nil, err
	}
	log.Printf("Using in-cluster config.")
	return cfg, nil
}

func usage() {
	log.Println("Usage: taintmanager [-add TAINT] [-remove TAINT] [-node NODE_NAME] [-kubeconfig /PATH/TO/KUBECONFIG]")
	flag.PrintDefaults()
	os.Exit(1)
}

func main() {
	kubeconfig := flag.String("kubeconfig", "", "(optional) absolute path to the kubeconfig file")
	nodeName := flag.String("node", "", "(optional) The name of the node to add/remove taints. Can be passed through environment variable MY_NODE_NAME")
	taintAdd := flag.String("add", "", "The taint to add")
	taintRemove := flag.String("remove", "", "The taint to remove")
	flag.Parse()

	// load kubeconfig
	config, err := buildConfig(*kubeconfig)
	if err != nil {
		log.Printf(err.Error())
		log.Printf("Failed to load kubeconfig")
		usage()
	}

	// parse taints
	tAdd, errAdd := parseTaint(*taintAdd)
	tRemove, errRemove := parseTaint(*taintRemove)
	if errAdd != nil && errRemove != nil {
		log.Println("Please specify at least one option -add or -remove")
		usage()
	}

	// check node name
	if *nodeName == "" {
		// try from env var
		*nodeName = os.Getenv("MY_NODE_NAME")
	}
	if *nodeName == "" {
		log.Println("Please specify the node name")
		usage()
	}
	log.Printf("Node name %v\n", *nodeName)

	// creates the clientset
	clientset, err := kubernetes.NewForConfig(config)
	if err != nil {
		panic(err.Error())
	}
	node, err := clientset.CoreV1().Nodes().Get(context.TODO(), *nodeName, metav1.GetOptions{})
	if errors.IsNotFound(err) {
		log.Printf("Node %v not found in default namespace\n", *nodeName)
	} else if statusError, isStatus := err.(*errors.StatusError); isStatus {
		log.Printf("Error getting node %v\n", statusError.ErrStatus.Message)
	} else if err != nil {
		panic(err.Error())
	} else {
		log.Printf("Found node %v\n", node.GetName())
		for k, v := range node.Spec.Taints {
			log.Printf("%v: %v\n", k, v)
		}
		if errAdd == nil {
			node.Spec.Taints = append(node.Spec.Taints, tAdd)
			clientset.CoreV1().Nodes().Update(context.TODO(), node, metav1.UpdateOptions{})
			log.Printf("Taint %v is added to node %v.", tAdd.ToString(), *nodeName)
		}
		if errRemove == nil {
			for i, taint := range node.Spec.Taints {
				if taint.Key == tRemove.Key {
					node.Spec.Taints = append(node.Spec.Taints[:i], node.Spec.Taints[i+1:]...)
					log.Printf("Taint %v is removed from node %v.", tRemove.ToString(), *nodeName)
					clientset.CoreV1().Nodes().Update(context.TODO(), node, metav1.UpdateOptions{})
				}
			}
		}
	}
}

// copied from https://github.com/kubernetes/kubernetes/blob/v1.25.4/pkg/util/taints/taints.go
// parseTaint parses a taint from a string, whose form must be either
// '<key>=<value>:<effect>', '<key>:<effect>', or '<key>'.
func parseTaint(st string) (v1.Taint, error) {
	var taint v1.Taint

	var key string
	var value string
	var effect v1.TaintEffect

	parts := strings.Split(st, ":")
	switch len(parts) {
	case 1:
		key = parts[0]
	case 2:
		effect = v1.TaintEffect(parts[1])
		if err := validateTaintEffect(effect); err != nil {
			return taint, err
		}

		partsKV := strings.Split(parts[0], "=")
		if len(partsKV) > 2 {
			return taint, fmt.Errorf("invalid taint spec: %v", st)
		}
		key = partsKV[0]
		if len(partsKV) == 2 {
			value = partsKV[1]
			if errs := validation.IsValidLabelValue(value); len(errs) > 0 {
				return taint, fmt.Errorf("invalid taint spec: %v, %s", st, strings.Join(errs, "; "))
			}
		}
	default:
		return taint, fmt.Errorf("invalid taint spec: %v", st)
	}

	if errs := validation.IsQualifiedName(key); len(errs) > 0 {
		return taint, fmt.Errorf("invalid taint spec: %v, %s", st, strings.Join(errs, "; "))
	}

	taint.Key = key
	taint.Value = value
	taint.Effect = effect

	return taint, nil
}

func validateTaintEffect(effect v1.TaintEffect) error {
	if effect != v1.TaintEffectNoSchedule && effect != v1.TaintEffectPreferNoSchedule && effect != v1.TaintEffectNoExecute {
		return fmt.Errorf("invalid taint effect: %v, unsupported taint effect", effect)
	}

	return nil
}
