package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

// Partial structure of a Kubernetes DaemonSet object
// Only contains fields we will actively be using, to make JSON parsing nicer
type DaemonSet struct {
	Kind   string `json:"kind"`
	Status struct {
		DesiredNumberScheduled int `json:"desiredNumberScheduled"`
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

func isImagesPresent(ds *DaemonSet) bool {
	desired := ds.Status.DesiredNumberScheduled
	ready := ds.Status.NumberReady

	log.Printf("%d of %d nodes currently has the required images.", ready, desired)

	return desired == ready
}
