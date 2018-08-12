# User Dummies

If you would like to test your cluster autoscaling in a controlled fashion, you
can simulate users dropping in with this Deployment.

Example:
$ echo 'Simulating four users...'
$ kubectl patch deployment user-dummy --patch '{"spec": {"replicas": 4}}'