(amazon-aws-eks)=

# Kubernetes on Amazon Web Services (AWS) with Elastic Container with Kubernetes (EKS)

AWS has released native support for Kubernetes, which is available in [selected regions][selected regions].

This guide uses AWS to set up a cluster. This mirrors the steps found at [Getting Started with Amazon EKS][getting started with amazon eks] with some details filled in that are absent

## Procedure

1. Create a IAM Role for EKS Service Role.
   Instructions for creating a role can be found
   [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create.html).
   It should have the following policies:

   - AmazonEKSClusterPolicy
   - AmazonEKSServicePolicy
   - AmazonEC2ContainerRegistryReadOnly

   (From the user interface, select EKS as the service, then follow the default steps)

2. Create a VPC if you don't already have one.
   This step has a lot of variability so it is left to the user. However, one deployment can be found at [Getting Started with Amazon EKS][getting started with amazon eks], under _Create your Amazon EKS Cluster VPC_
3. Create a Security Group for the EKS Control Plane to use
   You do not need to set any permissions on this. The steps below will automatically define access control between the EKS Control Plane and the individual nodes
4. Create your EKS cluster (using the user interface)
   Use the IAM Role in step 1 and Security Group defined in step 3. The cluster name is going to be used throughout. We'll use `Z2JHKubernetesCluster` as an example.
5. Install **kubectl** and **aws-iam-authenticator**
   Refer to [Getting Started with Amazon EKS][getting started with amazon eks] on _Configure kubectl for Amazon EKS_
6. Configure _kubeconfig_
   Also see [Getting Started with Amazon EKS][getting started with amazon eks] _Step 2: Configure kubectl for Amazon EKS_

   From the user interface on AWS you can retrieve the `endpoint-url`, `base64-encoded-ca-cert`. `cluster-name` is the name given in step 4. If you are using profiles in your AWS configuration, you can uncomment the `env` block and specify your profile as `aws-profile`.:

   ```yaml
   apiVersion: v1
   clusters:
     - cluster:
       server: <endpoint-url>
       certificate-authority-data: <base64-encoded-ca-cert>
       name: kubernetes
       contexts:
         - context:
           cluster: kubernetes
           user: aws
           name: aws
           current-context: aws
           kind: Config
           preferences: {}
           users:
             - name: aws
               user:
                 exec:
                   apiVersion: client.authentication.k8s.io/v1alpha1
                   command: aws-iam-authenticator
                   args:
                     - "token"
                     - "-i"
                     - "<cluster-name>"
                   # env:
                   # - name: AWS_PROFILE
                   #   value: "<aws-profile>"
   ```

7. Verify kubectl works

   ```
   kubectl get svc
   ```

   should return `kubernetes` and `ClusterIP`

8. Create the nodes using CloudFormation

   See [Getting Started with Amazon EKS][getting started with amazon eks] _Step 3: Launch and Configure Amazon EKS Worker Nodes_

   **Warning** if you are endeavoring to deploy on a private network, the cloudformation template creates a public IP for each worker node though there is no route to get there if you specified only private subnets. Regardless, if you wish to correct this, you can edit the cloudformation template by changing `Resources.NodeLaunchConfig.Properties.AssociatePublicIpAddress` from `'true'` to `'false'`

9. Create a AWS authentication ConfigMap

   This is necessary for the workers to find the master plane.

   See [Getting Started with Amazon EKS][getting started with amazon eks] _Step 3: Launch and Configure Amazon EKS Worker Nodes_

[getting started with amazon eks]: https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html
[selected regions]: https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/

## Cluster Autoscaler

If you'd like to do some {ref}`optimizations <efficient-cluster-autoscaling>`,
you need to deploy Cluster Autoscaler (CA) first.
