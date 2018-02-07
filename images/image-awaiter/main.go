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
	"crypto/tls"
	"crypto/x509"
	"flag"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"time"
)

// Return a HTTPS transport that has TLS configuration specified properly
func makeHttpTransport(caPath string, clientCertPath string, clientKeyPath string) (*http.Transport, error) {
	// Load client cert/key if they exist
	certificates := []tls.Certificate{}

	if clientCertPath != "" && clientKeyPath != "" {
		cert, err := tls.LoadX509KeyPair(clientCertPath, clientKeyPath)
		if err != nil {
			return nil, err
		}
		certificates = append(certificates, cert)
	}

	// Load CA cert
	caCert, err := ioutil.ReadFile(caPath)
	if err != nil {
		return nil, err
	}
	caCertPool := x509.NewCertPool()
	caCertPool.AppendCertsFromPEM(caCert)

	// Setup HTTPS transport
	tlsConfig := &tls.Config{
		Certificates: certificates,
		RootCAs:      caCertPool,
	}
	tlsConfig.BuildNameToCertificate()
	transport := &http.Transport{TLSClientConfig: tlsConfig}

	return transport, nil
}

func makeHeaders(authTokenPath string) (map[string]string, error) {
	authToken, err := ioutil.ReadFile(authTokenPath)
	if err != nil {
		return nil, err
	}
	return map[string]string{
		"Authorization": "Bearer " + string(authToken),
	}, nil
}

func main() {
	caPathPtr := flag.String("ca-path", "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt", "Path to CA bundle used to verify kubernetes master")
	clientCertPathPtr := flag.String("client-certificate-path", "", "Path to client certificate used to authenticate with kubernetes server")
	clientKeyPathPtr := flag.String("client-key-path", "", "Path to client certificate key used to authenticate with kubernetes server")
	authTokenPathPtr := flag.String("auth-token-path", "/var/run/secrets/kubernetes.io/serviceaccount/token", "Auth Token to use when making API requests")
	apiServerAddressPtr := flag.String("api-server-address", "", "Address of the Kubernetes API Server to contact")
	namespacePtr := flag.String("namespace", "", "Namespace to spawn daemonset in")
	daemonsetSpecPtr := flag.String("daemonset-spec", "", "Full JSON spec of daemonset to create when pulling images")
	flag.Parse()

	transport, err := makeHttpTransport(*caPathPtr, *clientCertPathPtr, *clientKeyPathPtr)
	if err != nil {
		log.Fatal(err)
	}

	headers, err := makeHeaders(*authTokenPathPtr)
	if err != nil {
		log.Fatal(err)
	}

	nodes, err := getNodes(transport, *apiServerAddressPtr, headers)
	if err != nil {
		log.Fatal(err)
	}

	images := flag.Args()

	if imagesPresent(nodes, images) {
		log.Printf("All images present on all nodes! Exiting...")
		os.Exit(0)
	}

	daemonsetName, _ := makeDaemonset(transport, *apiServerAddressPtr, headers, *namespacePtr, *daemonsetSpecPtr)

	log.Printf("DaemonSet %s created", daemonsetName)

	for {
		nodes, err = getNodes(transport, *apiServerAddressPtr, headers)
		if err != nil {
			log.Fatal(err)
		}

		if imagesPresent(nodes, images) {
			log.Printf("All images present on all nodes!")
			break
		}

		time.Sleep(2 * time.Second)
	}

	deleteDaemonset(transport, *apiServerAddressPtr, headers, *namespacePtr, daemonsetName)
}
