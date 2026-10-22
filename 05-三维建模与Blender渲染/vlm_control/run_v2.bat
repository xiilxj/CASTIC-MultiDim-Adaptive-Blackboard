@echo off
title GH-VI-2026 VLM Digital Twin v2.0
color 0B
cd /d "%~dp0"
set "PY_EXE=C:\Program Files\Python310\python.exe"
if not exist "%PY_EXE%" set "PY_EXE=python"
"%PY_EXE%" vlm_light_digital_twin_system_v2_0.py %*
if %errorlevel% neq 0 pause
