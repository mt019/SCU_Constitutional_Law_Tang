#!/usr/bin/env bash
set -euo pipefail

# One-click: start Jupyter via Docker Compose and print the access URL.
# Works whether Jupyter prints a token URL or runs without token.

HOST=${JUPYTER_HOST:-127.0.0.1}
PORT=${JUPYTER_PORT:-11418}

echo "[info] Starting 'jupyter' service (detached)…"
docker compose up -d jupyter >/dev/null

# Try to grab a token URL from logs (if token is enabled)
raw_url=$(docker compose logs --no-color jupyter 2>/dev/null \
  | sed -n 's@.*http://[^ ]*\?token=[A-Za-z0-9._-]*@\0@p' \
  | tail -n 1 || true)

if [[ -n "${raw_url:-}" ]]; then
  # Normalize container URL to host bind address
  # Replace :8888 with :$PORT and host with $HOST
  url=$(printf '%s' "$raw_url" \
    | sed -E "s@://[^/:]+:([0-9]+)@://$HOST:$PORT@" \
    | sed -E "s@://127\.0\.0\.1:@://$HOST:@")
else
  # No token in logs (token disabled). Use lab URL directly.
  url="http://$HOST:$PORT/lab"
fi

# Wait briefly for the port to be ready (best-effort)
ready=0
for _ in {1..40}; do
  if command -v nc >/dev/null 2>&1; then
    if nc -z "$HOST" "$PORT" 2>/dev/null; then ready=1; break; fi
  elif command -v curl >/dev/null 2>&1; then
    if curl -fsS "http://$HOST:$PORT" >/dev/null 2>&1; then ready=1; break; fi
  else
    # Fallback: attempt TCP via bash if available
    if (exec 3<>"/dev/tcp/$HOST/$PORT") 2>/dev/null; then exec 3>&-; ready=1; break; fi
  fi
  sleep 0.25
done

echo "[ok] Jupyter URL: $url"

