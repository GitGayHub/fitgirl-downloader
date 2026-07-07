@echo off
title FitGirl Repack Downloader
echo ==============================================
echo        FitGirl Repack Downloader
echo ==============================================
echo.
echo Cleaning up any old running server instances...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000" ^| findstr "LISTENING"') do (
    taskkill /f /pid %%a >nul 2>&1
)
echo.
echo Starting web GUI in default browser...
start /b cmd /c "timeout /t 2 /nobreak >nul && start "" http://localhost:8000"
echo.
echo Starting server...
".venv\Scripts\python.exe" main.py
echo.
echo Server stopped.
pause
