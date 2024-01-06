```bash
FROM python:3.8-slim
WORKDIR /src
COPY . /src
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```
```bash
docker build -t my-app .
docker run -p 5000:5000 my-app
```

# Kubernetes
## my-app-deployment.yaml
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: MY-app-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: MY-app
  template:
    metadata:
      labels:
        app: MY-app
    spec:
      containers:
      - name: MY-app
        image: MY-app:latest
        ports:
        - containerPort: 5000
```

## my-app-service.yaml
```
apiVersion: v1
kind: Service
metadata:
  name: MY-app-service
spec:
  selector:
    app: flask-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: NodePort # or LoadBalancer if available (i.e. not running minikube)

```

```
kubectl apply -f my-app-deployment.yaml
kubectl apply -f my-app-service.yaml
```