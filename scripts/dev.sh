#!/usr/bin/env bash
# Start both Mizani agents and the web app, wait for health, print URLs.
set -euo pipefail

cd "$(dirname "$0")/.."
export PETTA_PATH="$PWD/agent/vendor/petta"

# load .env if present (never required)
if [[ -f .env ]]; then
  set -a; source .env; set +a
fi

COMM_PORT="${MIZANI_COMMUNITY_PORT:-8101}"
FAC_PORT="${MIZANI_FACILITY_PORT:-8102}"
export MIZANI_PEER="${MIZANI_PEER:-http://127.0.0.1:${FAC_PORT}}"

cleanup() {
  echo "stopping..."
  kill "${COMM_PID:-}" "${FAC_PID:-}" "${WEB_PID:-}" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

cd agent
MIZANI_ROLE=community uv run uvicorn mizani.app:create_app --factory --port "${COMM_PORT}" &
COMM_PID=$!
MIZANI_ROLE=facility uv run uvicorn mizani.app:create_app --factory --port "${FAC_PORT}" &
FAC_PID=$!
cd ..

cd web
pnpm dev &
WEB_PID=$!
cd ..

wait_health() {
  local url="$1" name="$2" tries=120
  until curl -sf "${url}/health" >/dev/null 2>&1; do
    tries=$((tries - 1))
    if [[ $tries -le 0 ]]; then
      echo "${name} did not become healthy" >&2
      exit 1
    fi
    sleep 0.5
  done
}

wait_health "http://127.0.0.1:${COMM_PORT}" "community agent"
wait_health "http://127.0.0.1:${FAC_PORT}" "facility agent"

echo ""
echo "  Mizani is up:"
echo "    community agent  http://127.0.0.1:${COMM_PORT}  (edge-v1)"
echo "    facility agent   http://127.0.0.1:${FAC_PORT}  (full-v1)"
echo "    web app          http://localhost:3000"
echo ""

wait
