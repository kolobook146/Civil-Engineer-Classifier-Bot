#!/bin/zsh
# Stop the webhook stack on macOS
# cd "/Users/kolobook/Documents/TG Build Bot"
# ./scripts/stop_webhook_stack_macos.sh

set -euo pipefail

GRACEFUL_WAIT_SECONDS=5


collect_pids() {
  local pattern="$1"
  pgrep -f "$pattern" 2>/dev/null || true
}


signal_processes() {
  local signal_name="$1"
  shift
  local pids=("$@")

  if (( ${#pids[@]} == 0 )); then
    return 0
  fi

  kill "-$signal_name" "${pids[@]}" 2>/dev/null || true
}


wait_for_exit() {
  local timeout_seconds="$1"
  shift
  local pids=("$@")

  if (( ${#pids[@]} == 0 )); then
    return 0
  fi

  local start_ts
  start_ts="$(date +%s)"

  while true; do
    local alive=()
    local pid
    for pid in "${pids[@]}"; do
      if kill -0 "$pid" 2>/dev/null; then
        alive+=("$pid")
      fi
    done

    if (( ${#alive[@]} == 0 )); then
      return 0
    fi

    local now_ts
    now_ts="$(date +%s)"
    if (( now_ts - start_ts >= timeout_seconds )); then
      printf '%s\n' "${alive[@]}"
      return 1
    fi

    sleep 0.2
  done
}


stop_group() {
  local label="$1"
  local pattern="$2"

  local pids=()
  local raw_pids
  raw_pids="$(collect_pids "$pattern")"
  if [[ -n "$raw_pids" ]]; then
    pids=("${(@f)raw_pids}")
  fi

  if (( ${#pids[@]} == 0 )); then
    echo "$label: not running"
    return 0
  fi

  echo "$label: sending SIGINT to PID(s): ${pids[*]}"
  signal_processes INT "${pids[@]}"

  local remaining_pids=()
  local remaining_raw
  if remaining_raw="$(wait_for_exit "$GRACEFUL_WAIT_SECONDS" "${pids[@]}")"; then
    echo "$label: stopped gracefully"
    return 0
  fi

  if [[ -n "$remaining_raw" ]]; then
    remaining_pids=("${(@f)remaining_raw}")
  fi

  echo "$label: still running after ${GRACEFUL_WAIT_SECONDS}s, sending SIGTERM to PID(s): ${remaining_pids[*]}"
  signal_processes TERM "${remaining_pids[@]}"

  if wait_for_exit 2 "${remaining_pids[@]}" >/dev/null; then
    echo "$label: stopped after SIGTERM"
    return 0
  fi

  echo "$label: some processes are still running and may need manual intervention"
  return 1
}


overall_status=0

stop_group "Webhook server" "python3 src/main_webhook.py" || overall_status=1
stop_group "Queue worker" "python3 src/main_queue_worker.py" || overall_status=1
stop_group "ngrok tunnel" "ngrok http 8080" || overall_status=1

if (( overall_status == 0 )); then
  echo "Webhook stack stop completed."
else
  echo "Webhook stack stop completed with warnings."
fi

exit "$overall_status"
