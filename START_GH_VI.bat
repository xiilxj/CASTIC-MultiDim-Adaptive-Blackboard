@echo off
title CASTIC GH-VI-2026 Live Controller
color 0A
cd /d "%~dp0"
cd "05-三维建模与Blender渲染lm_control"
python run_live_system.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Trying with py command...
    py run_live_system.py
)
pause
