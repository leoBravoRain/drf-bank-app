#!/usr/bin/env bash

set -e
set -o pipefail

# BUILDING AND LOADING IMAGE TO k8S

# NOTIFICATIONS SYSTEM
echo "🔧 Building notifications-fast-api image..."
docker build -t notifications-fast-api ./notifications_system/

echo "📦 Loading notifications-fast-api into minikube nodes..."
./scripts/load-image-to-minikube-nodes.sh notifications-fast-api

# DRF API
echo "🔧 Building quotation_api-drf image..."
docker build -t quotation_api-drf .

echo "📦 Loading quotation_api-drf into minikube nodes..."
./scripts/load-image-to-minikube-nodes.sh quotation_api-drf

# ANALYTICS SERVICE (NEST)
echo "🔧 Building analytics_service_nest image..."
docker build -t analytics_service_nest ./analytics_service/

echo "📦 Loading analytics_service_nest into minikube nodes..."
./scripts/load-image-to-minikube-nodes.sh analytics_service_nest



##############################################
# APPLY K8S MANIFESTS
##############################################

echo "📄 Applying Kubernetes manifests..."

# NOTIFICATIONS SYSTEM
echo "📄 Applying notifications-fast-api k8s YAML..."
kubectl apply -f kubernetes/notifications-fast-api/

# DRF API
echo "📄 Applying drf-api k8s YAML..."
kubectl apply -f kubernetes/drf-api/

# ANALYTICS SERVICE (NEST)
echo "📄 Applying analytics-service-nest YAML..."
kubectl apply -f kubernetes/analytics-service-nest/



##############################################
# FORCE RESTART USING SCALE LOGIC
##############################################

echo "🔄 Scaling deployments in Kubernetes..."

# NOTIFICATIONS SYSTEM
echo "⛔ Stopping notifications-fast-api..."
kubectl scale deployment notifications-fast-api --replicas=0
echo "🚀 Starting notifications-fast-api..."
kubectl scale deployment notifications-fast-api --replicas=1

# DRF API
echo "⛔ Stopping drf-api..."
kubectl scale deployment drf-api --replicas=0
echo "🚀 Starting drf-api..."
kubectl scale deployment drf-api --replicas=1

# ANALYTICS SERVICE
echo "⛔ Stopping analytics-service-nest..."
kubectl scale deployment analytics-service-nest --replicas=0
echo "🚀 Starting analytics-service-nest..."
kubectl scale deployment analytics-service-nest --replicas=1


echo "✅ Done! Images built, manifests applied, and deployments restarted."
