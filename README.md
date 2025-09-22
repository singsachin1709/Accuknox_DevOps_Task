# Accuknox_DevOps_Task

## Problem Statement 1: Deploy Wisecow Application on Amazon EKS with TLS
This project demonstrates how to deploy a simple **Fortune + Cowsay app on Amazon EKS with secure TLS termination** using **Nginx Ingress Controller** and **Cert-Manager**.

## 📌 Project Architecture

- **Application:** A simple Bash-based app serving fortunes with cowsay via Netcat.
- **Containerization:** App is containerized using Docker.
- **Kubernetes Deployment:** Pod + Service manifest used for deployment.
- **Ingress Controller:** Nginx Ingress routes external traffic to the app.
- **TLS Security:** Cert-Manager + Let’s Encrypt used for automated certificate management.

## 🛠️ Prerequisites

- AWS Account with EKS cluster set up
- kubectl installed and connected to your EKS cluster
- helm installed for Nginx Ingress & Cert-Manager
- Domain name (e.g., devopstutorial.xyz) pointing to the EKS Ingress LoadBalancer in Route53

## ⚙️ Steps
### 1. Install Nginx Ingress Controller
```
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace

```

## 2. Install Cert-Manager
```
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace \
  --version v1.15.1 \
  --set installCRDs=true
```

## 3. Create ClusterIssuer for Let’s Encrypt
```
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v2.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
      - http01:
          ingress:
            class: nginx
```
Apply it:
```
kubectl apply -f cluster-issuer.yml
```

## 4. Deploy the App

Deployment + Service
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: simple-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: simple-app
  template:
    metadata:
      labels:
        app: simple-app
    spec:
      containers:
        - name: simple-app
          image: <your-dockerhub-username>/simple-app:latest
          ports:
            - containerPort: 4499
---
apiVersion: v1
kind: Service
metadata:
  name: simple-app-service
spec:
  selector:
    app: simple-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 4499
```

## 5. Create Ingress with TLS
```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: simple-app-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts:
        - devopstutorial.xyz
        - www.devopstutorial.xyz
      secretName: simple-app-tls
  rules:
    - host: devopstutorial.xyz
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: simple-app-service
                port:
                  number: 80
    - host: www.devopstutorial.xyz
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: simple-app-service
                port:
                  number: 80
```

Apply it:
```
kubectl apply -f ingress.yml
```

## 🌐 Access the App
- Visit: https://devopstutorial.xyz
- Or: https://www.devopstutorial.xyz

Both should now be secured with HTTPS (Let’s Encrypt TLS).

## ✅ Verification

### Check certificate status:
```
kubectl get certificate
```
### Check ingress:
```
kubectl get ingress
```
### 📖 Summary
This task covers:
- Deploying an app on EKS
- Setting up Nginx Ingress Controller
- Enabling TLS with Cert-Manager & Let’s Encrypt
- Configuring DNS in Route53

# Problem Statement 2: 
## Task 1: System Health Monitoring Script
### 📌 Objective
Develop a script that monitors the health of a Linux system. It checks the following metrics and sends alerts if thresholds are exceeded:
- CPU usage
- Memory usage
- Disk space usage
- Number of running processes

If any metric goes beyond a defined threshold, the script logs an ALERT with a timestamp.

### 🚀 Features
- Monitors real-time system resources.
- Customizable thresholds for alerts.
- Console alerts + log file storage.
- Lightweight and easy to schedule via cron.

### 🛠️ Requirements
- Python 3.7+
- Install dependencies:
```
pip install psutil
```
### 📜 Script: ``` system_health_monitor.py ```
```
import psutil
import datetime

# Thresholds
CPU_THRESHOLD = 80      # percent
MEMORY_THRESHOLD = 80   # percent
DISK_THRESHOLD = 90     # percent
PROCESS_THRESHOLD = 300 # max number of processes

# Log file
LOG_FILE = "system_health.log"

def log_alert(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{timestamp} - ALERT: {message}"
    print(log_message)
    with open(LOG_FILE, "a") as f:
        f.write(log_message + "\n")

def check_cpu():
    usage = psutil.cpu_percent(interval=1)
    if usage > CPU_THRESHOLD:
        log_alert(f"High CPU usage detected: {usage}%")

def check_memory():
    memory = psutil.virtual_memory()
    if memory.percent > MEMORY_THRESHOLD:
        log_alert(f"High memory usage detected: {memory.percent}%")

def check_disk():
    disk = psutil.disk_usage('/')
    if disk.percent > DISK_THRESHOLD:
        log_alert(f"High disk usage detected: {disk.percent}%")

def check_processes():
    num_processes = len(psutil.pids())
    if num_processes > PROCESS_THRESHOLD:
        log_alert(f"High number of running processes: {num_processes}")

if __name__ == "__main__":
    check_cpu()
    check_memory()
    check_disk()
    check_processes()
```
### ▶️ Usage
Run the script manually:
```
python system_health_monitor.py
```
### Example output:
```
2025-09-22 11:20:45 - ALERT: High CPU usage detected: 92%
2025-09-22 11:20:46 - ALERT: High memory usage detected: 85%
```
Alerts are also saved in ```system_health.log```.

# Task 2: Application Health Checker
## 📌 Objective
Develop a script that checks the uptime of an application and determines if it is functioning correctly by verifying its HTTP status code. The script should detect whether the application is UP (functioning) or DOWN (unavailable or not responding).

## 🚀 Features
- Sends HTTP requests to one or more application URLs.
- Verifies if the response status code is 200 OK.
- Logs the application status (UP or DOWN) with timestamps.
- Handles connection errors, timeouts, and invalid responses.
- Can be scheduled with cron (Linux/macOS) or Task Scheduler (Windows) for automated monitoring.

## 🛠️ Requirements
- Python 3.7+
- Install dependencies:
```
pip install requests
```

## 📜 Script (app_health_checker.py)
```
import requests
import datetime

# List of application URLs to monitor
applications = [
    "https://example.com",   # Replace with your app URL
    "https://api.example.com"
]

# Log file
LOG_FILE = "app_health.log"

def log_status(url, status):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"{timestamp} - {url} is {status}"
    print(message)
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

def check_application(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            log_status(url, "UP")
        else:
            log_status(url, f"DOWN (HTTP {response.status_code})")
    except requests.RequestException as e:
        log_status(url, f"DOWN (Error: {e})")

if __name__ == "__main__":
    for app in applications:
        check_application(app)
```

## ▶️ Usage
Run the script manually:
```
python app_health_checker.py
```
### Example output:
```
2025-09-22 10:30:15 - https://example.com is UP
2025-09-22 10:30:15 - https://api.example.com is DOWN (HTTP 500)
```


# Problem Statement 3: Enforcing Zero Trust Security with KubeArmor on EKS
This task builds upon Task 1 by adding KubeArmor security policies to enforce a Zero Trust model for the deployed simple app on Amazon EKS.

## 📌 What is KubeArmor?
KubeArmor is a runtime security enforcement system for Kubernetes.
It allows you to:
- Enforce file, process, and network security policies on running pods
- Block/allow actions at runtime (e.g., preventing shell execution, blocking /etc access)
- Achieve Zero Trust by restricting pods to only what they need

## 🛠️ Prerequisites
- Task 1 completed (app deployed on EKS with TLS)
- helm installed
- kubectl configured for your cluster

## ⚙️ Steps
### 1. Install KubeArmor on EKS
```
helm repo add kubearmor https://kubearmor.github.io/charts
helm repo update

helm install kubearmor kubearmor/kubearmor \
  --namespace kubearmor --create-namespace \
  --set kubearmor.hostPolicy.enabled=true \
  --set kubearmor.logLevel=info
```
Verify installation:
```
kubectl get pods -n kubearmor
```
### 2. Label Pods for Policy Enforcement
Apply labels so KubeArmor knows which pods to enforce:
```
kubectl label pod <simple-app-pod-1> kubearmor=enabled
kubectl label pod <simple-app-pod-2> kubearmor=enabled
```
### 3. Create KubeArmor Policy for Zero Trust
Save as k8s/kubearmor-zero-trust-simple-app.yml
```
apiVersion: security.kubearmor.com/v1
kind: KubeArmorPolicy
metadata:
  name: zero-trust-simple-app
  namespace: default
spec:
  selector:
    matchLabels:
      kubearmor: enabled
  file:
    matchDirectories:
      - dir: /etc
        recursive: true
        action: Block
  process:
    matchPaths:
      - path: /bin/bash
        action: Block
      - path: /bin/sh
        action: Block
```
###What this does:
- Blocks access to /etc inside the pod
- Prevents spawning new shells (bash, sh) → stopping privilege escalation

### 4. Apply the Policy
```
kubectl apply -f k8s/kubearmor-zero-trust-simple-app.yml
```
# 📖 Summary
In this task, we:
- Installed KubeArmor in the EKS cluster
- Applied Zero Trust policy to two simple-app pods
- Blocked access to critical files and restricted process execution
This enforces runtime security on top of the deployment from Task 1.
