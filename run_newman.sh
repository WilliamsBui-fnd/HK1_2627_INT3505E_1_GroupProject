#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p reports
newman run tasks-api.postman_collection.json \
  -e postman/local.postman_environment.json \
  --env-var "base_url=${1:-http://127.0.0.1:5018}" \
  --env-var "token=${TASKS_API_TOKEN:-demo-token}" \
  -r cli,junit \
  --reporter-junit-export reports/junit.xml

