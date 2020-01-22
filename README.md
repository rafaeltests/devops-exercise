# Abraxas DevOps Exercise

## Intro

Thank you for your interest and participation in our recruitment process for our DevOps Engineer position, to continue with the process we ask you to take the following technical test and share your result with us.

If you have any questions or comments during the test, do not hesitate to contact us by email at reclutamiento@grupoabraxas.com

## Get your environment ready

You'll need:

1. A Github account
2. A docker hub account
3. Access to a kubernetes cluster for testing purposes (It can be Minikube or any other public or private option)
4. Fork this repository, then clone it locally.
5. MetallB software (for Kubenetes in Bare metal or Minikube)

## Ready for action?

Great!!
As a DevOps we need you to create a mechanism to deploy nanoservices. You'll be in charge of deploy, monitor, scale applications and promote the DevOps culture with the development team. But let's start by the begining, below you'll find the requirements for this test.

### Dockerize services

Dockerize the given service at [app.py](app.py), including all it's required dependencies installed and ready to rock.

The Dockerfile references a vanilla Ubuntu version 18.04 and install python in order to comply with flask requirements.

Only app.py and requirement.txt are copied during the image build, avoiding not related files from the root folder.

### CI/CD

Implement a Github Actions workflow to build and publish your docker image on [docker hub](https://hub.docker.com/).

The solution used a github workflow file docker.yml, found at .github/workflows this workflow is responsible to pull the code in case of new commit in the repository for that branch. Only master branch is currently configured.
The same workflow is in charge also to build, tag and push the docker image to the docker hub.

The docker images are stored at:
https://hub.docker.com/repository/docker/rafaeltests/app

A unique identifier is used to for image tagging and also, the latest image receives the "latest" tag that will be deployed in the kubernetes via manifest.

For this time no automatic deploy is being considered for Minikube. The current github workflow can be extended with actions to deploy in a kubernetes cloud provider, for example.

### Deployment

Before the application deployment we need to install MetallB, which will provide the external IP address for the service when using Minikube or a bare metal deployment. In this way, MetallB will pretend to be a physical or cloud load balancer. For cloud based deployments this step is not required because such External IP is delivered by the provider, usually through an internet facing load balancer.

MetallB installation: https://metallb.universe.tf/installation/

- Execute: 
  kubectl apply -f https://raw.githubusercontent.com/google/metallb/v0.8.3/manifests/metallb.yaml

MetallLB can provide IPs for the load balancers services exposed in the cluster based on different configurations. For this scenario we use a address range, 192.168.99.20-192.168.99.100  . They vary depending on environment, virtualization solution or physical.

- Apply the configmap:

    1. kubectl apply -f metallb-configmap.yml

- Make sure MetallB is running under its own namespace, the commands below must show the components:

    1. kubectl get pods        -n metallb-system

    2. kubectl get deployments -n metallb-system

    3. kubectl get daemonsets  -n metallb-system

    4. kubectl get replicaset  -n metallb-system

Now, with MetalLB running, is time to deploy the application:

Create a service configuration file to deploy the service on your kubernetes cluster and expose it to the world.

The service configuration file app-service.yml uses LoadBalancer type since we want the service externally accesible and the traffic sent to specific port in the cluster nodes.

The main advantages are the LoadBalancer offers more flexibility compared to NodePort service which has some limitations with ports or changes in Node's IP. 

- Execute:
  kubectl apply -f app-service.yml

In addition of the service, for this deployment, uses the kubernetes deployment object which allows updates, scallability and roll out management for pods.

Since we are providing a stateless application, its definition is very simple.

- Let's apply the app-deployment.yml file

  kubectl apply -f app-deployment.yml

### Checklist

Running pods:

1. kubectl get pods

app-deployment-77d94f7984-wb8k9   1/1     Running   0          122m
app-deployment-77d94f7984-xs2jd   1/1     Running   0          122m

App service:

2. kubectl get services

NAME          TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)          AGE
app-service   LoadBalancer   10.96.222.57   192.168.99.20   8000:32500/TCP   124m
kubernetes    ClusterIP      10.96.0.1      <none>          443/TCP          17h

App deployment object:

3. kubectl get deployments

NAME                              READY   STATUS    RESTARTS   AGE
app-deployment-77d94f7984-wb8k9   1/1     Running   0          124m
app-deployment-77d94f7984-xs2jd   1/1     Running   0          124m


Service and app test:

curl -v http://192.168.99.20:8000

A response like this should return:
'''
* Expire in 0 ms for 6 (transfer 0x5578bc60df50)
*   Trying 192.168.99.20...
* TCP_NODELAY set
* Expire in 200 ms for 4 (transfer 0x5578bc60df50)
* Connected to 192.168.99.20 (192.168.99.20) port 8000 (#0)
> GET / HTTP/1.1
> Host: 192.168.99.20:8000
> User-Agent: curl/7.64.0
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: text/html; charset=utf-8
< Content-Length: 14
< Server: Werkzeug/0.16.0 Python/2.7.17
< Date: Wed, 22 Jan 2020 01:02:52 GMT
< 
* Closing connection 0
Hello World!!!
'''

### Extra Points

- Improve the given python service so it maintains a counter of the amount of **POST** requests it served, and return it on **GET** requests.

## Deliverables

- A link to the public docker registry where the image is published.
  https://hub.docker.com/repository/docker/rafaeltests/app


- A link to your repository containing:
    https://github.com/rafaeltests/devops-exercise

    1. The Dockerfile(s) for the image(s).
    2. The kubernetes file(s) for the service deployment(s). The deployment should be replicable on our kubernetes cluster.
    3. Optionally the code for the improved version of the service.

## General Guidelines

Your code should be as simple as possible, yet well documented and robust.
Spend some time on designing your solution. Think about operational use cases from the real world. Few examples:

1. What happens if a service crashes?
2. How much effort will it take to create a new service? D.R.Y!

## Reference

- [Run a Stateless Application Using a Deployment](https://kubernetes.io/docs/tasks/run-application/run-stateless-application-deployment/)

