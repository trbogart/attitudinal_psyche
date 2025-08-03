#! /bin/zsh

cd "${0:a:h}"

if [[ ! -d .vm/bin ]]; then
  python3 -m venv .vm || exit 1
  pip install -r requirements.txt || exit 1
fi
. .vm/bin/activate || exit 1
python3 ap_discord.py | tee discord.log 2>&1