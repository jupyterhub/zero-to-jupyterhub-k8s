package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

// Partial Structure of Kubernetes Node objects
// Only contains fields we will actively be using, to make JSON parsing nicer
type NodeList struct {
	Kind  string `json:"kind"`
	Items []struct {
		Metadata struct {
			Name string `json:"name"`
		} `json:"metadata"`
		Spec struct {
			Unschedulable bool `json:"unschedulable"`
		} `json:"spec"`
		Status struct {
			Images []struct {
				Names []string `json:"names"`
			} `json:"images"`
		} `json:"status"`
	}
}

// Return a *NodeList with list of nodes present in cluster now
func getNodes(transport *http.Transport, server string, headers map[string]string) (*NodeList, error) {
	client := &http.Client{Transport: transport}
	url := server + "/api/v1/nodes"

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

	nodes := &NodeList{}
	data, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	err = json.Unmarshal(data, &nodes)

	if nodes.Kind != "NodeList" {
		// Something went wrong!
		return nil, errors.New(fmt.Sprintf("Can not parse API response as NodeList: %s", string(data)))
	}

	return nodes, err
}

// Return true if all the images in `images` are present in all the
// schedulable nodes in `nodes`
func imagesPresent(nodes *NodeList, images []string) bool {
	for _, node := range nodes.Items {
		// Ignore nodes that are cordoned
		if !node.Spec.Unschedulable {

			foundImages := 0

			for _, nodeImages := range node.Status.Images {
				for _, imageName := range nodeImages.Names {
					for _, neededImage := range images {
						if neededImage == imageName {
							foundImages += 1
							break
						}
					}
				}
			}

			log.Printf("%d of %d images pulled in node %s", foundImages, len(images), node.Metadata.Name)
			if foundImages != len(images) {
				return false
			}
		}
	}

	// If we get here then all nodes have all images we care about!
	return true
}
