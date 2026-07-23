@echo off
REM Debug / console launcher. Normal users should use the Start Menu shortcut
REM (Launch_Downloader.vbs) which starts the app with no CMD window.
setlocal EnableExtensions
cd /d "%~dp0"

REM Prefer silent app launch (no pause, no console pile-up)
if exist "%~dp0Launch.ps1" (
    powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "%~dp0Launch.ps1"
    exit /b %ERRORLEVEL%
)

REM Fallback: kill old + run python in this console (dev only)
if not exist ".venv\Scripts\python.exe" (
    echo ERROR: .venv\Scripts\python.exe not found
    pause
    exit /b 1
)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0kill_old_servers.ps1" >nul 2>&1
start /b "" powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "for($i=0;$i -lt 50;$i++){ try { $r=Invoke-WebRequest -Uri 'http://127.0.0.1:8000/' -UseBasicParsing -TimeoutSec 1; if($r.StatusCode -eq 200){ Start-Process 'http://127.0.0.1:8000/'; exit 0 } } catch {} ; Start-Sleep -Milliseconds 100 }"
".venv\Scripts\python.exe" main.py
echo Server stopped with code %ERRORLEVEL%
pause
endlocal
