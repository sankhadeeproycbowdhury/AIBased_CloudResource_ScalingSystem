# AIDreiven_CloudResource_ScalingSystem

## AI model, designed on pretrained data as well as simultaneous real-time data. Predicts the future CPU usage percentage of a server running on a cloud in every 1 min thus giving the future prediction of evry 10 min in a sliding window pattern ( time for traning and future prediction window size are flexible)

## Thus the server docker image and Ai model Docker image are pushed in docker hub and fetched in real time according to the predictions of AI model in order to scale up or down as per need. The images are runned on a local kubernettes clusters runnig at localhost's virtual enviroment. In future they can be ran on real cluster as well.


## Associated steps and commands

### First start Docker Engin or Docker Desktop
### Then run following Commands in terminal(inside Docker File) :
#### 1 minikube star 
#### 2 kubectl get nodes
#### 3 kubectl apply -f deployment.yaml 
#### 4 kubectl apply -f service.yaml 
verify using kubectl get deployments or kubectl get pods or kubectl get services. Preinstall Docker, Minikube and kubectl

### pip install all requiremensts in requirements.txt file, then Run ( inside Ai model File) 
#### python main2.py 
#### python Graph.py
one after Another.
main2 runs the actual model and scalling program, Graph is for graphical vizualization of CPU usage percentage prediction.

### server.py is a simple service running on cloud server (change as per client or need), automateclient is to send requests to the serevr automatically to simulate real time enviroment.(only for testing purpose not mandetory).

