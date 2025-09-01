#! /bin/bash

error() {
  echo "$@" >&2
  exit 1
}

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
# shellcheck disable=SC2164
cd "$SCRIPT_DIR" || error "Unable to find script directory $SCRIPT_DIR"

if [[ ! -f .venv/bin/activate ]]; then
  if command -v python3 >/dev/null 2>&1; then
    python3 -m venv .venv || error "Unable to create venv"
  elif command -v python >/dev/null 2>&1; then
    python -m venv .venv || error "Unable to create venv"
  else
    error "Python not installed"
  fi
fi
. .venv/bin/activate || error "Unable to activate venv"
pip install -q -r requirements.txt || error "Unable to install requirements"
if command -v python3 >/dev/null 2>&1; then
  python3 ap_discord.py | tee discord.log 2>&1
elif command -v python >/dev/null 2>&1; then
  python ap_discord.py | tee discord.log 2>&1
else
  error "Python not installed"
fi
