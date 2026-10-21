@echo off
title GH-VI-2026 VLM Digital Twin v2.0
color 0B
cd /d "%~dp0"
set "PYTHON_CMD=C:\Users\Lenovo\AppData\Local\Programs\Python\Python314\python.exe"
if not exist "%PYTHON_CMD%" set "PYTHON_CMD=python"
"%PYTHON_CMD%" vlm_light_digital_twin_system_v2_0.py
if %errorlevel% neq 0 pause
