@echo off
setlocal
cd /d "%~dp0"

echo === Installing/updating server dependencies ===
pushd server
python -m pip install -r requirements-local.txt -q
if errorlevel 1 ( popd & echo ERROR: server pip install failed. & pause & exit /b 1 )
popd

echo === Installing/updating client dependencies ===
pushd client
python -m pip install -r requirements.txt -q
if errorlevel 1 ( popd & echo ERROR: client pip install failed. & pause & exit /b 1 )
popd

echo === Launching server + client (system tray) ===
call "%~dp0run-all.bat"

echo.
echo Server setup page : http://localhost:5001/
echo Client web UI     : http://localhost:5000/
echo Both run in the system tray. Close this window any time.
