#!/usr/bin/env bash
set -e
# start compose (detached) for test environment
cd $(dirname "$0")/../../..
docker-compose -f infra/docker-compose.yaml up -d --build
# optional: start kafka compose if exists
if [ -f infra/docker-compose.kafka.yaml ]; then
  docker-compose -f infra/docker-compose.kafka.yaml up -d --build
fi
# wait for services
echo "Waiting for services to become ready..."
sleep 8
