@echo off
cd /d "%~dp0"
title GH-VI-2026 Digital Twin Launcher
color 0A

echo =====================================================================
echo  CASTIC GH-VI-2026 Live Digital Twin Interactive Launcher
echo =====================================================================
echo [*] Starting Python Core Engine...
echo [*] Current Directory: %CD%
echo.

python run_live_system.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Python failed to start. Trying with py launcher...
    py run_live_system.py
)

pause
