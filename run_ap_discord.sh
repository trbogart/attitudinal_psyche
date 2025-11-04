#! /bin/bash

log() {
  echo ------------------------------------------
  echo "$@"
}
error() {
  echo "$@" >&2
  exit 1
}

run_python() {
  error_msg=$1
  shift
  if command -v python3 >/dev/null 2>&1; then
    python3 "$@" || error "$error_msg"
  elif command -v python >/dev/null 2>&1; then
    python "$@" || error "$error_msg"
  else
    error "Python not installed"
  fi
}

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
SCRIPT=ap_discord.py
cd "$SCRIPT_DIR" || error "Unable to find script directory $SCRIPT_DIR"

if [[ ! -f .venv/bin/activate ]]; then
  log "Creating venv"
  run_python "Unable to create venv" -m venv .venv
fi

log "Activating venv"
source .venv/bin/activate || error "Unable to activate venv"

log "Installing pip"
run_python "Unable to install pip" -m ensurepip

log "Upgrading dependencies"
pip install -q -U pip -r requirements.txt --require-virtualenv || error "Unable to upgrade dependencies"

log "Running $SCRIPT"
run_python "Error running $SCRIPT" "$SCRIPT"
