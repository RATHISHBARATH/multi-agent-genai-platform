#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR=$(cd "$(dirname "$0")/.."; pwd)
cd "$ROOT_DIR"
echo "Starting services via docker-compose..."
docker-compose -f infra/docker-compose.yaml up -d --build
echo "Waiting for services to warm up..."
sleep 12
echo "Initializing DB..."
python3 - <<'PY'
from api.db import init_db
init_db()
print('DB initialized')
PY
echo "Running pytest integration tests..."
pytest -q backend/tests/integration -x
EXIT_CODE=$?
echo "Tearing down docker-compose..."
docker-compose -f infra/docker-compose.yaml down --volumes --remove-orphans
exit $EXIT_CODE
