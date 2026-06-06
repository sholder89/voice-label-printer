@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo Installing/updating dependencies...
python -m pip install -r requirements.txt -q
if errorlevel 1 (
    echo ERROR: pip install failed. Make sure Python is installed and added to PATH.
    pause
    exit /b 1
)

:: Load .env from parent directory if present
if exist "..\\.env" (
    for /f "usebackq tokens=1,* delims==" %%A in ("..\\.env") do (
        set "line=%%A"
        if not "!line:~0,1!"=="#" if not "%%A"=="" set "%%A=%%B"
    )
)

echo Starting Label Printer (system tray)...
start "" pythonw app.py
