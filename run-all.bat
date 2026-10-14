@echo off
:: Fast launcher (no dependency install) — used by Windows auto-start.
:: For first run / after updates, use start-all.bat instead so deps install.
start "" /d "%~dp0server" pythonw run_local.py
:: The watchdog starts app.py and restarts it if it crashes or hangs.
start "" /d "%~dp0client" pythonw watchdog.py
