#!/bin/bash

# Script to load Docker image to all minikube nodes (including worker nodes)
# Usage: ./load-image-to-minikube-nodes.sh <image-name>

set -e

IMAGE_NAME=${1:-quotation_api-drf:latest}

echo "Loading image ${IMAGE_NAME} to all minikube nodes..."

# Create a safe filename by replacing / and : with _
SAFE_FILENAME=$(echo "${IMAGE_NAME}" | tr '/:' '_')
TAR_FILE="/tmp/${SAFE_FILENAME}.tar"

# Get list of all minikube nodes
NODES=$(minikube node list | awk '{print $1}' | tail -n +2)

for NODE in $NODES; do
    echo "Loading image to node: ${NODE}..."

    # Save image to tar file
    docker save ${IMAGE_NAME} -o ${TAR_FILE}

    # Copy to node and load
    minikube cp ${TAR_FILE} ${NODE}:${TAR_FILE}
    minikube ssh -n ${NODE} -- docker load -i ${TAR_FILE}

    # Cleanup local file
    rm -f ${TAR_FILE}

    # Cleanup on remote node (ignore errors if file doesn't exist)
    minikube ssh -n ${NODE} -- "rm -f ${TAR_FILE} || true"

    echo "✓ Image loaded to ${NODE}"
done

echo "Done! Image ${IMAGE_NAME} is now available on all minikube nodes."
