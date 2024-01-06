#!/bin/bash

docker build -t gsk-app .

# Use this to run your container locally
# docker run -p 5000:5000 gsk-app

# I assume that kubernetes cluster already exists ... otherwise I panic!
# I also assume that kubectl environments are setup ... but I am rusty on navigating these
kubectl apply -f gsk_app_deployment.yml
kubectl apply -f gsk_app_service.yml