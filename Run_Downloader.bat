@echo off
setlocal EnableExtensions
title FitGirl Repack Downloader
cd /d "%~dp0"

echo ==============================================
echo        FitGirl Repack Downloader
echo ==============================================
echo.

echo Closing previous FitGirl servers (keeping this window)...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0kill_old_servers.ps1"
if errorlevel 1 (
    echo Warning: cleanup script reported an error, continuing anyway...
)

echo.
echo Opening dashboard in browser in 2s...
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://localhost:8000/"

echo Starting server...
if not exist ".venv\Scripts\python.exe" (
    echo ERROR: .venv\Scripts\python.exe not found
    echo Run from C:\VibeCoding\fitgirl-downloader after creating the venv.
    pause
    exit /b 1
)
if not exist "main.py" (
    echo ERROR: main.py not found in %CD%
    pause
    exit /b 1
)

".venv\Scripts\python.exe" main.py
set ERR=%ERRORLEVEL%

echo.
if not "%ERR%"=="0" (
    echo Server exited with code %ERR%
) else (
    echo Server stopped.
)
pause
endlocal
