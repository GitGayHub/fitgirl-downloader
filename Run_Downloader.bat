@echo off
title FitGirl Repack Downloader
echo ==============================================
echo        FitGirl Repack Downloader
echo ==============================================
echo.
echo Starting web GUI in default browser...
start /b cmd /c "timeout /t 2 /nobreak >nul && start "" http://localhost:8000"
echo.
echo Starting server...
python main.py
echo.
echo Server stopped.
pause
