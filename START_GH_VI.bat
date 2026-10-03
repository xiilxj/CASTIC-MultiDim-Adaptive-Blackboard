@echo off
title CASTIC GH-VI-2026 Live Controller
color 0A
cd /d "%~dp0"
echo =======================================================================
echo  CASTIC GH-VI-2026 Live Digital Twin Controller
echo =======================================================================
echo [*] Launching Python engine...
echo.

py -3.10 run_live_system.py
if %ERRORLEVEL% EQU 0 goto :eof

echo [*] Python 3.10 failed or not found, trying default python...
python run_live_system.py
if %ERRORLEVEL% EQU 0 goto :eof

echo [*] Trying py launcher...
py run_live_system.py

pause
