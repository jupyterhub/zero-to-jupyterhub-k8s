# Autoscaling

As of Fall 2016, Data 8's JupyterHub deployment on Ansible
(https://github.com/data-8/jupyterhub-deploy) uses statically allocated
resources. In order to handle load spikes we have to pre-provision
enough nodes for maximum espected capacity at all times, resulting in
waste of CPU time.

Because Kubernetes allows us to easily autoscale clusters, we can expect
significant cost savings over the previous deployment.

Initial calculations estimate that we can save around $15124.11 per month over
the existing deployment.

## Cost Savings

We are currently using Microsoft Azure as our cloud provider. There are ~510
students in the Fall 2016 offering of Data 8. Based on previous load behavior,
we provision enough resources for 371 students, or ~75% of the maximum possible
load using 53 Basic A4 nodes. These VMs are statically allocated, so we always
have them running even when the number of students is significantly lower than
the max capacity.

Each node costs $458.30 / month which comes out to a total of $24,290.11 /
month. Usage patterns on data8 show that an average of ~113 students are online
per 24 hour period with peaks around ~300 and lows around ~25.

Supposing we use the autoscaling feature of Kubernetes, we can let each node be
80% utilized before provisioning a new one. This means on average we'll
provision enough resources for 140 students for each day. Let's assume that we
can maintain 80% utilization consistently throughout the day. This means we'll
use `140 / 371 = 37.7%` of the resources we were using before.

This equates to having to provision an average of 20 nodes, resulting in
estimated cost savings of $15124.11 a month.

## Implementation on Kubernetes

Kubernetes natively supports autoscaling as of July 2016
([blog post][autoscaling]). As of November 8 2016, autoscaling is supported on
the two out of the three cloud providers we are targetting: [GCE][], and
[AWS][]. Azure's new Container Service only supports manual scaling as of this
writing, with autoscaling expected soon ([link][ACS]).

[autoscaling]: http://blog.kubernetes.io/2016/07/autoscaling-in-kubernetes.html
[GCE]: http://blog.kubernetes.io/2016/07/autoscaling-in-kubernetes.html
[AWS]: https://aws.amazon.com/about-aws/whats-new/2016/05/amazon-ec2-container-service-supports-automatic-service-scaling/
[ACS]: https://azure.microsoft.com/en-us/documentation/articles/container-service-scale/

Implementation-wise, we need to create a [HorizontalPodAutoscaler][]
object in our k8s config in order to make use of autoscaling.

[HorizontalPodAutoscaler]: http://kubernetes.io/docs/api-reference/autoscaling/v1/definitions/#_v1_horizontalpodautoscaler
