@echo off
:: Fast launcher (no dependency install) — used by Windows auto-start.
:: For first run / after updates, use start-all.bat instead so deps install.
start "" /d "%~dp0server" pythonw run_local.py
start "" /d "%~dp0client" pythonw app.py
