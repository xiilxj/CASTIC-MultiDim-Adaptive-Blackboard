@echo off
chcp 65001 > nul
title GH-VI-2026 多模态VLM数字孪生光环境控制系统 v2.0
color 0B

echo ==============================================================================
echo        GH-VI-2026 多模态 VLM 教室光环境数字孪生主控系统 (v2.0 终极实战版)
echo ==============================================================================
echo  [1] 正在自动检测 Python 解释器...

set PYTHON_CMD=

if exist "C:\Users\Lenovo\AppData\Local\Programs\Python\Python314\python.exe" (
    set "PYTHON_CMD=C:\Users\Lenovo\AppData\Local\Programs\Python\Python314\python.exe"
    goto :FOUND
)

if exist "C:\Users\Lenovo\AppData\Local\Programs\Python\Python312\python.exe" (
    set "PYTHON_CMD=C:\Users\Lenovo\AppData\Local\Programs\Python\Python312\python.exe"
    goto :FOUND
)

if exist "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\python.exe" (
    set "PYTHON_CMD=C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\python.exe"
    goto :FOUND
)

where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PYTHON_CMD=python"
    goto :FOUND
)

where py >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PYTHON_CMD=py"
    goto :FOUND
)

:FOUND
if "%PYTHON_CMD%"=="" (
    echo [错误] 未能在当前系统中找到 Python 解释器！
    echo 请确认 Python 是否已正确安装。
    pause
    exit /b 1
)

echo  [OK] 锁定 Python 核心: %PYTHON_CMD%
echo.
echo  [2] 正在切换至项目工作目录...
set "WORK_DIR=D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control"
cd /d "%WORK_DIR%"
if %ERRORLEVEL% neq 0 (
    echo [错误] 无法进入工作目录: %WORK_DIR%
    pause
    exit /b 1
)

echo  [OK] 所在工作目录: %CD%
echo.
echo  [3] 正在拉起 GH-VI-2026 VLM 视觉感知与光环境数字孪生系统...
echo      • 按键提示: [V] 键切换视角 (学生实况 / Blender教室全景)
echo      • 按键提示: [C] 键切换摄像头 (机内 / USB运动相机 / 仿真流)
echo      • 按键提示: [M] 键切换大模型 (Qwen2.5-VL / MiniCPM-V / InternVL)
echo      • 按键提示: [1][2][3] 键一键触发核心评委问答宏
echo ==============================================================================
echo.

"%PYTHON_CMD%" vlm_light_digital_twin_system_v2_0.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo ==============================================================================
    echo [运行提示] 系统退出，退出代码: %ERRORLEVEL%
    echo 如遇依赖缺失，可在终端运行: "%PYTHON_CMD%" -m pip install opencv-python numpy
    echo ==============================================================================
)

pause
