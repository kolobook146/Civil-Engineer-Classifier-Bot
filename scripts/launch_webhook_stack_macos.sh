#!/bin/zsh

set -euo pipefail

PROJECT_DIR="/Users/kolobook/Documents/TG Build Bot"
ENV_FILE="$PROJECT_DIR/.env"
NGROK_LOCAL_API_URL="http://127.0.0.1:4040/api/tunnels"
NGROK_PORT=8080
NGROK_STARTUP_TIMEOUT_SECONDS=20


escape_for_applescript() {
  python3 - "$1" <<'PY'
import json
import sys

print(json.dumps(sys.argv[1])[1:-1])
PY
}


open_terminal_window() {
  local raw_command="$1"
  local escaped_command
  escaped_command="$(escape_for_applescript "$raw_command")"

  /usr/bin/osascript <<APPLESCRIPT >/dev/null
tell application "Terminal"
  activate
  do script "$escaped_command"
end tell
APPLESCRIPT
}


fetch_ngrok_public_url() {
  python3 - "$NGROK_LOCAL_API_URL" "$NGROK_STARTUP_TIMEOUT_SECONDS" <<'PY'
import json
import sys
import time
import urllib.error
import urllib.request

api_url = sys.argv[1]
timeout_seconds = int(sys.argv[2])
deadline = time.time() + timeout_seconds

while time.time() < deadline:
    try:
        with urllib.request.urlopen(api_url, timeout=1.5) as response:
            payload = json.load(response)
    except Exception:
        time.sleep(1)
        continue

    tunnels = payload.get("tunnels", [])
    for tunnel in tunnels:
        public_url = str(tunnel.get("public_url", ""))
        if public_url.startswith("https://"):
            print(public_url)
            raise SystemExit(0)
    time.sleep(1)

raise SystemExit(1)
PY
}


update_env_webhook_base_url() {
  local public_url="$1"
  python3 - "$ENV_FILE" "$public_url" <<'PY'
from pathlib import Path
import sys

env_path = Path(sys.argv[1])
public_url = sys.argv[2]

if not env_path.exists():
    raise SystemExit(f".env not found: {env_path}")

lines = env_path.read_text(encoding="utf-8").splitlines()
updated = False
for index, line in enumerate(lines):
    if line.startswith("WEBHOOK_PUBLIC_BASE_URL="):
        lines[index] = f"WEBHOOK_PUBLIC_BASE_URL={public_url}"
        updated = True
        break

if not updated:
    lines.append(f"WEBHOOK_PUBLIC_BASE_URL={public_url}")

env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY
}


if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing .env file: $ENV_FILE"
  exit 1
fi

if ! command -v ngrok >/dev/null 2>&1; then
  echo "ngrok is not installed or not available in PATH."
  echo "Install it first, then run this script again."
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is not available in PATH."
  exit 1
fi

QUEUE_COMMAND="printf '\\033]0;TG Queue Worker\\007'; cd \"$PROJECT_DIR\"; PYTHONPATH=src python3 src/main_queue_worker.py"
NGROK_COMMAND="printf '\\033]0;TG ngrok\\007'; cd \"$PROJECT_DIR\"; ngrok http $NGROK_PORT"
WEBHOOK_COMMAND="printf '\\033]0;TG Webhook\\007'; cd \"$PROJECT_DIR\"; PYTHONPATH=src python3 src/main_webhook.py"

open_terminal_window "$QUEUE_COMMAND"
sleep 0.5
open_terminal_window "$NGROK_COMMAND"

echo "Waiting for ngrok to publish an HTTPS tunnel on port $NGROK_PORT..."
public_url="$(fetch_ngrok_public_url)" || {
  echo "ngrok did not expose an HTTPS URL within ${NGROK_STARTUP_TIMEOUT_SECONDS}s."
  echo "Queue worker and ngrok windows were opened, but webhook was not started."
  exit 1
}

update_env_webhook_base_url "$public_url"

echo "Updated WEBHOOK_PUBLIC_BASE_URL in .env:"
echo "  $public_url"
echo "Starting webhook window..."

sleep 0.5
open_terminal_window "$WEBHOOK_COMMAND"

echo
echo "Stack started:"
echo "1. Queue worker"
echo "2. ngrok"
echo "3. Webhook server"
echo
echo "Webhook URL:"
echo "  ${public_url}/telegram/webhook"
echo
echo "If you stop ngrok and restart it, run this launcher again so .env is updated."
