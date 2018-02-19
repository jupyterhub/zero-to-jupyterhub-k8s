package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

// Partial Structure of Kubernetes Pods objects
// Only contains fields we will actively be using, to make JSON parsing nicer
type PodList struct {
	Kind  string `json:"kind"`
	Items []Pod
}

type Pod struct {
	Status struct {
		Phase string `json:"phase"`
	} `json:"status"`
}

// Return a *PodList of pods spawned by the image-puller daemonset
func getImagePullerPods(transport *http.Transport, server string, headers map[string]string) (*PodList, error) {
	client := &http.Client{Transport: transport}
	url := server + "/api/v1/pods" + "?labelSelector=component=hook-image-puller" + "&limit=1000"

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

	pods := &PodList{}
	data, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	err = json.Unmarshal(data, &pods)

	if pods.Kind != "PodList" {
		// Something went wrong!
		return nil, errors.New(fmt.Sprintf("Can not parse API response as PodList: %s", string(data)))
	}

	return pods, err
}

func isPodRunning(pod *Pod) bool {
	return pod.Status.Phase == "Running"
}

// Returns true if all the image puller pod is in the running phase. The running
// phase implies that all the init containers images have been utilized by the
// image puller pods, so hence all nodes (one for each image puller pod) have
// pulled the required images.
func isImagesPresent(pods *PodList) bool {
	podsRunning := 0
	totalPods := 0

	for _, pod := range pods.Items {
		if isPodRunning(&pod) {
			podsRunning++
		}
		totalPods++
	}

	log.Printf("%d of %d nodes got the required images", podsRunning, totalPods)
	return podsRunning == totalPods
}
