#!/usr/bin/env bash

# Activate from ~/fastapitutorial/
echo "Starting"

scp .env testcontrol1:/tmp/fastapi.env

# K8s secret must be lowercase
ssh testcontrol1 << EOF
kubectl create secret generic envfile -n fastapi --from-env-file=/tmp/fastapi.env
EOF
