@echo off
setlocal
cd /d "%~dp0"

echo Installing/updating server dependencies...
python -m pip install -r requirements-local.txt -q
if errorlevel 1 (
    echo ERROR: pip install failed. Make sure Python is installed and added to PATH.
    pause
    exit /b 1
)

echo Starting Voice Label Server (system tray)...
start "" pythonw run_local.py
