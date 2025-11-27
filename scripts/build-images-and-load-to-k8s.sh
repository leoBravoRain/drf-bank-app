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

# ANALYTICS SERVICE
echo "🔧 Building analytics_service_nest image..."
docker build -t analytics_service_nest ./analytics_service/

echo "📦 Loading analytics_service_nest into minikube nodes..."
./scripts/load-image-to-minikube-nodes.sh analytics_service_nest

# SCALLING APPS IN K8S (TO FORCE RESTART)
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
echo "⛔ Stopping analytics-service..."
kubectl scale deployment analytics-service --replicas=0

echo "🚀 Starting analytics-service..."
kubectl scale deployment analytics-service --replicas=1


echo "✅ Done! All images built, loaded, and deployments restarted."
