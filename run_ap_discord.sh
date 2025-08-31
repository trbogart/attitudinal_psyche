#! /bin/bash

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
cd "$SCRIPT_DIR"

if [[ ! -d .venv/bin ]]; then
  python3 -m venv .venv || exit 1
fi
. .venv/bin/activate || exit 1
pip install -q -r requirements.txt || exit 1
python3 ap_discord.py | tee discord.log 2>&1