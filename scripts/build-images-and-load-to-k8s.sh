#!/usr/bin/env bash

set -e
set -o pipefail

echo "🔧 Building notifications-fast-api image..."
docker build -t notifications-fast-api ./notifications_system/

echo "📦 Loading notifications-fast-api into minikube nodes..."
./scripts/load-image-to-minikube-nodes.sh notifications-fast-api

echo "🔧 Building quotation_api-drf image..."
docker build -t quotation_api-drf .

echo "📦 Loading quotation_api-drf into minikube nodes..."
./scripts/load-image-to-minikube-nodes.sh quotation_api-drf

echo "🔄 Scaling deployments in Kubernetes..."

echo "⛔ Stopping notifications-fast-api..."
kubectl scale deployment notifications-fast-api --replicas=0

echo "🚀 Starting notifications-fast-api..."
kubectl scale deployment notifications-fast-api --replicas=1

echo "⛔ Stopping drf-api..."
kubectl scale deployment drf-api --replicas=0

echo "🚀 Starting drf-api..."
kubectl scale deployment drf-api --replicas=1

echo "✅ Done! All images built, loaded, and deployments restarted."
