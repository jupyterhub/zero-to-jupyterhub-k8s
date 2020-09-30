package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

// Partial structure of a Kubernetes DaemonSet object. Note that we want to use
// the non-optional fields of the Status struct only to ensure this is a robust
// implementation.
//
// ref: https://github.com/kubernetes/kubernetes/blob/e23d83eead3b5ae57731afb0209f4a2aaa4009dd/pkg/apis/apps/types.go#L590
type DaemonSet struct {
	Kind   string `json:"kind"`
	Status struct {
		// The number of nodes that are running at least 1
		// daemon pod and are supposed to run the daemon pod.
		CurrentNumberScheduled int `json:"currentNumberScheduled"`
		// The number of nodes that are running the daemon pod, but are
		// not supposed to run the daemon pod.
		DesiredNumberScheduled int `json:"desiredNumberScheduled"`
		// The number of nodes that should be running the daemon pod and have one
		// or more of the daemon pod running and ready.
		NumberReady            int `json:"numberReady"`
	} `json:"status"`
}

// Return a *DaemonSet and the relevant state its in
func getDaemonSet(transportPtr *http.Transport, server string, headers map[string]string, namespace string, daemonSet string) (*DaemonSet, error) {
	client := &http.Client{Transport: transportPtr}
	url := server + "/apis/apps/v1/namespaces/" + namespace + "/daemonsets/" + daemonSet

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, err
	}

	for k, v := range headers {
		req.Header.Add(k, v)
	}

	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	ds := &DaemonSet{}
	data, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	err = json.Unmarshal(data, &ds)

	if ds.Kind != "DaemonSet" {
		// Something went wrong!
		return nil, fmt.Errorf(fmt.Sprintf("Can not parse API response as DaemonSet: %s", string(data)))
	}

	return ds, err
}

// Return a bool indicating if the provided DaemonSet's _currently_ scheduled
// pods (which does the image pulling) are ready, or in the case of a
// strictCheck, if the _desired_ number of scheduled pods are ready.
func areDaemonSetPodsReady(ds *DaemonSet, waitForPodsToSchedule bool) bool {
	current := ds.Status.CurrentNumberScheduled
	desired := ds.Status.DesiredNumberScheduled
	ready := ds.Status.NumberReady

	log.Printf("%d image puller pods are ready out of the %d currently scheduled and %d desired number scheduled.", ready, current, desired)
	if waitForPodsToSchedule {
		return ready == desired
	} else {
		return ready >= current
	}
}
