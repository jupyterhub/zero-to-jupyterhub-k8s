// Pulls a given list of images on all nodes on a cluster.
//
// This program will perform the following sequence of actions
//
// 1. Check if the given list of images already exist on all scheduleable nodes.
//    If they do, exit!
// 2. If they don't, create a deamonset (the spec for which is passed in
//    as the `daemonset-spec` commandline parameter)
// 3. Check every 2s if the images are present in all scheduleable nodes.
// 4. Once image is in all schedulable nodes, kill the daemonset created in (2) and exit
//
package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"net/http"
)

type DaemonSet struct {
	Kind     string `json:"kind"`
	Metadata struct {
		Name string `json:"name"`
	} `json:"metadata"`
}

// Make a daemonset with given spec & return its name
func makeDaemonset(transport *http.Transport, server string, headers map[string]string, namespace string, daemonsetSpec string) (string, error) {
	client := &http.Client{Transport: transport}
	url := server + "/apis/extensions/v1beta1/namespaces/" + namespace + "/daemonsets"

	req, err := http.NewRequest("POST", url, bytes.NewBufferString(daemonsetSpec))
	if err != nil {
		return "", err
	}

	for k, v := range headers {
		req.Header.Add(k, v)
	}

	resp, err := client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	data, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	daemonset := &DaemonSet{}

	err = json.Unmarshal(data, &daemonset)
	if err != nil {
		return "", err
	}

	if daemonset.Kind != "Daemonset" {
		// Something went wrong!
		return "", errors.New(fmt.Sprintf("Can not parse API response as DaemonSet: %s", string(data)))
	}

	return daemonset.Metadata.Name, nil

}

// Delete a given daemonset in a namespace
func deleteDaemonset(transport *http.Transport, server string, headers map[string]string, namespace string, daemonsetName string) error {
	client := &http.Client{Transport: transport}
	url := server + "/apis/extensions/v1beta1/namespaces/" + namespace + "/daemonsets"
	// This will always be the same JSON, so no need to make a struct for this
	body := "{\"apiVersion\": \"v1\", \"kind\": \"DeleteOptions\", \"propagationPolicy\": \"Foreground\"}"

	req, err := http.NewRequest("DELETE", url, bytes.NewBufferString(body))
	if err != nil {
		return err
	}

	for k, v := range headers {
		req.Header.Add(k, v)
	}

	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	_, err = ioutil.ReadAll(resp.Body)
	if err != nil {
		return err
	}

	return nil
}
