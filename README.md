# AI-Driven Cloud Resource Scaling System

A machine learning-based system that predicts CPU usage and automatically scales cloud resources using Docker and Kubernetes. The system uses both pretrained data and real-time metrics to make predictions in a sliding window pattern.

## Overview

This system:
- Predicts server CPU usage every 1 minute
- Provides 10-minute future predictions using a sliding window
- Automatically scales Docker containers based on predictions
- Runs on a Kubernetes cluster
- Supports flexible training and prediction window sizes

## Architecture

The system consists of two main components:
1. AI Model Container
   - Handles CPU usage predictions
   - Processes real-time data
   - Manages sliding window predictions

2. Server Container
   - Runs the target application
   - Scales based on AI predictions
   - Monitors real-time CPU usage

## Prerequisites

- Docker Engine or Docker Desktop
- Minikube
- kubectl
- Python 3.x
- pip

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd AIDriven_CloudResource_ScalingSystem
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Setup and Deployment

### 1. Start the Kubernetes Cluster

First, ensure Docker is running, then:

```bash
# Start Minikube
minikube start

# Verify node status
kubectl get nodes
```

### 2. Deploy to Kubernetes

```bash
# Apply deployment configuration
kubectl apply -f deployment.yaml

# Apply service configuration
kubectl apply -f service.yaml

# Verify deployment
kubectl get deployments
kubectl get pods
kubectl get services
```

### 3. Run the AI Model

Execute the following commands in sequence:

```bash
# Start the main AI model and scaling program
python main2.py

# Run visualization tool
python Graph.py
```

## Components

### main2.py
- Core AI model implementation
- Real-time prediction engine
- Scaling logic controller

### Graph.py
- CPU usage visualization
- Prediction trend analysis
- Real-time monitoring interface

### server.py
- Cloud server implementation
- Resource usage monitoring
- Service endpoint management

### automateclient.py (Testing Tool)
- Request simulation
- Load testing
- Environment simulation

## Configuration

### deployment.yaml
```yaml
# Example configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: scaling-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: scaling-system
```

### service.yaml
```yaml
# Example configuration
apiVersion: v1
kind: Service
metadata:
  name: scaling-service
spec:
  type: LoadBalancer
  ports:
    - port: 80
```

## Usage

1. **Normal Operation**
   - Start the Kubernetes cluster
   - Deploy the containers
   - Run the AI model
   - Monitor through Graph.py

2. **Testing**
   - Use automateclient.py to simulate load
   - Monitor scaling behavior
   - Analyze prediction accuracy

## Monitoring and Visualization

The system provides real-time monitoring through Graph.py, showing:
- Current CPU usage
- Predicted usage trends
- Scaling events
- Performance metrics

## Development

### Adding Custom Services
1. Modify server.py to implement your service
2. Update Docker configuration
3. Rebuild and push containers
4. Update Kubernetes configurations

### Modifying AI Model
1. Adjust prediction windows in main2.py
2. Update training parameters
3. Modify scaling thresholds

## Troubleshooting

Common issues and solutions:
1. Kubernetes connection issues
   - Verify Minikube status
   - Check Docker daemon
   - Confirm kubectl configuration

2. Model prediction issues
   - Check training data
   - Verify sliding window configuration
   - Monitor resource availability

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with detailed changes

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).


## Contact
[Sankhadeep Roy Choudhury](https://github.com/sankhadeeproycbowdhury)
