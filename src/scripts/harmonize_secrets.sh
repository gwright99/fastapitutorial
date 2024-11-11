#!/usr/bin/env bash

# Activate from ~/fastapitutorial/

## GITHUB ACTIONS
## -------------------------------------------------------------
# https://cli.github.com/manual/gh_secret_set
# $ gh secret list --repo gwright99/fastapitutorial

b64content=$(base64 -w 0 < .env)

echo "Creating GHA Secret 'ENVFILE'"
gh secret delete ENVFILE --repo gwright99/fastapitutorial || true
gh secret set ENVFILE --repo gwright99/fastapitutorial $b64content


## K8S SECRET
## -------------------------------------------------------------
echo "Creating K8s Secret 'envfile'"
# Copy from development machine to host with kubectl access to cluster
# NOTE: Don't appear to be necessary, see below.
# scp .env testcontrol1:/tmp/fastapi.env

# Choose to base64 encode single line for reasons listed here:
# # https://www.jeffgeerling.com/blog/2019/mounting-kubernetes-secret-single-file-inside-pod
# 'base64 -w 0' emits the base64 output on a single line.
# Grab content of local .env, dont need to copy it across to the kubectl-linked server!
b64content=$(base64 -w 0 < .env)

ssh testcontrol1 << EOF
  kubectl delete secret envfile -n fastapi  || true
  kubectl create secret generic envfile --from-literal=.env=$b64content
EOF




