@echo off
cd /D "%~dp0"

if not exist .venv\Scripts (
    python -m venv .venv || exit 1
)
cmd /k "cd .venv\Scripts && activate.bat && cd ..\.. && pip install -q -r requirements.txt && python ap_discord.py"
