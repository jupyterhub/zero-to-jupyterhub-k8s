// This program will be run as a helm hook before an actual helm upgrade have
// started. It will simply wait for image pulling to complete by the
// helm-image-puller daemonset's pods, it will poll these pods and exit when
// they are all running.

// TODO:
// - Consider what the query param called 'includeUninitialized' will do
// - Consider unschedulable nodes and how the DS will schedule pods on them
//   make sure the daemonsets schedules the pods wisely.

/*
FUTURE REWORK:
Stop using /api/v1/pods and instead use /api/v1/namespaces/<ns>/daemonsets/hook-image-puller/status
- Current solution: curl http://localhost:8080/api/v1/pods?labelSelector=component=hook-image-puller
- K8s 1.8 solution: curl http://localhost:8080/apis/apps/v1beta2/namespaces/<ns>/demonsets/hook-image-puller/status
- K8s 1.9 solution: curl http://localhost:8080/api/v1/namespaces/<ns>/demonsets/hook-image-puller/status

{
	"kind": "DaemonSet",
	"apiVersion": "apps/v1beta2",

	...

	"status": {
		"currentNumberScheduled": 2,
		"numberMisscheduled": 0,
		"desiredNumberScheduled": 2,
		"numberReady": 2,
		"observedGeneration": 1,
		"updatedNumberScheduled": 2,
		"numberAvailable": 2
	}
}
*/

package main

import (
	"crypto/tls"
	"crypto/x509"
	"flag"
	"io/ioutil"
	"log"
	"net/http"
	"time"
)

// Return a HTTPS transport that has TLS configuration specified properly
func makeHTTPTransport(debug bool, caPath string, clientCertPath string, clientKeyPath string) (*http.Transport, error) {
	idleConnTimeout := 30 * 60 * time.Second

	// If you debug through a kubectl proxy, certificates etc. isn't required
	if debug {
		transportPtr := &http.Transport{IdleConnTimeout: idleConnTimeout}
		return transportPtr, nil
	}

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
	transportPtr := &http.Transport{TLSClientConfig: tlsConfig, IdleConnTimeout: idleConnTimeout}

	return transportPtr, nil
}

func makeHeaders(debug bool, authTokenPath string) (map[string]string, error) {
	if debug {
		return map[string]string{}, nil
	}

	authToken, err := ioutil.ReadFile(authTokenPath)
	if err != nil {
		return nil, err
	}
	return map[string]string{
		"Authorization": "Bearer " + string(authToken),
	}, nil
}

func main() {
	var caPath, clientCertPath, clientKeyPath, authTokenPath, apiServerAddress string
	var debug bool
	flag.StringVar(&caPath, "ca-path", "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt", "Path to CA bundle used to verify kubernetes master")
	flag.StringVar(&clientCertPath, "client-certificate-path", "", "Path to client certificate used to authenticate with kubernetes server")
	flag.StringVar(&clientKeyPath, "client-key-path", "", "Path to client certificate key used to authenticate with kubernetes server")
	flag.StringVar(&authTokenPath, "auth-token-path", "/var/run/secrets/kubernetes.io/serviceaccount/token", "Auth Token to use when making API requests")
	flag.StringVar(&apiServerAddress, "api-server-address", "", "Address of the Kubernetes API Server to contact")
	flag.BoolVar(&debug, "debug", false, "Communicate through a 'kubectl proxy --port 8080' setup instead.")
	flag.Parse()

	if debug {
		apiServerAddress = "http://localhost:8080"
	}

	transportPtr, err := makeHTTPTransport(debug, caPath, clientCertPath, clientKeyPath)
	if err != nil {
		log.Fatal(err)
	}

	headers, err := makeHeaders(debug, authTokenPath)
	if err != nil {
		log.Fatal(err)
	}

	for {
		pods, err := getImagePullerPods(transportPtr, apiServerAddress, headers)
		if err != nil {
			log.Fatal(err)
		}

		if isImagesPresent(pods) {
			log.Printf("All images present on all nodes!")
			break
		}

		time.Sleep(2 * time.Second)
	}
}
