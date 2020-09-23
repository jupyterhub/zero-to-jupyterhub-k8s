// Program used to delay a helm upgrade process until all relevant nodes have
// pulled required images. It is an image-awaiter. It can simply wait because
// the hook-image-puller daemonset that will get the images pulled is already
// started when this job starts. When all images are pulled, this job exits.

/*
K8s API access of relevance
- curl http://localhost:8080/apis/apps/v1/namespaces/<ns>/demonsets/<ds>
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
	var caPath, clientCertPath, clientKeyPath, authTokenPath, apiServerAddress, namespace, daemonSet string
	flag.StringVar(&caPath, "ca-path", "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt", "Path to CA bundle used to verify kubernetes master")
	flag.StringVar(&clientCertPath, "client-certificate-path", "", "Path to client certificate used to authenticate with kubernetes server")
	flag.StringVar(&clientKeyPath, "client-key-path", "", "Path to client certificate key used to authenticate with kubernetes server")
	flag.StringVar(&authTokenPath, "auth-token-path", "/var/run/secrets/kubernetes.io/serviceaccount/token", "Auth Token to use when making API requests")
	flag.StringVar(&apiServerAddress, "api-server-address", "", "Address of the Kubernetes API Server to contact")
	flag.StringVar(&namespace, "namespace", "", "Namespace of the DaemonSet that will perform image pulling")
	flag.StringVar(&daemonSet, "daemonset", "hook-image-puller", "The name DaemonSet that will perform image pulling")
	var debug bool
	flag.BoolVar(&debug, "debug", false, "Communicate through a 'kubectl proxy --port 8080' setup instead.")
	var podSchedulingWaitDuration int
	flag.IntVar(&podSchedulingWaitDuration, "pod-scheduling-wait-duration", 10, "Duration of seconds to await the desired number of scheduled pods to become ready until transitioning to awaiting the currently scheduled pods to become ready instead. Set to -1 for an infinite duration.")

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

	for i := 0; true; i++ {
		ds, err := getDaemonSet(transportPtr, apiServerAddress, headers, namespace, daemonSet)
		if err != nil {
			log.Fatal(err)
		}

		waitForPodsToSchedule := podSchedulingWaitDuration == -1 || i < podSchedulingWaitDuration
		if areDaemonSetPodsReady(ds, waitForPodsToSchedule) {
			log.Printf("Image download on nodes awaited successfully: shutting down!")
			break
		}

		time.Sleep(1 * time.Second)
	}
}
