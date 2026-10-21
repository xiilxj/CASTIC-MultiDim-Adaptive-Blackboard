@echo off
rem ==============================================================================
rem GH-VI-2026 VLM Digital Twin Control System v2.0 (GBK Native)
rem ==============================================================================
title GH-VI-2026 多模态VLM数字孪生光环境控制系统 v2.0
color 0B

echo ==============================================================================
echo        GH-VI-2026 多模态 VLM 教室光环境数字孪生主控系统 (v2.0 终极实战版)
echo ==============================================================================
echo.

set "PYTHON_CMD=C:\Users\Lenovo\AppData\Local\Programs\Python\Python314\python.exe"

if not exist "%PYTHON_CMD%" (
    echo [提示] 正在检索系统环境变量中的 Python...
    where python >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON_CMD=python"
    ) else (
        where py >nul 2>&1
        if %errorlevel% equ 0 (
            set "PYTHON_CMD=py"
        ) else (
            echo [错误] 未在系统中检测到 Python，请检查 Python 安装路径！
            pause
            exit /b 1
        )
    )
)

echo [OK] 锁定 Python 核心: %PYTHON_CMD%
echo.
echo [操作快捷键提示]:
echo   - 按 [V] 键: 自由切换左侧视口 (学生实况面部/眯眼 vs Blender 3D 教室全景数字孪生)
echo   - 按 [C] 键: 自由切换摄像头 (外接 USB 运动相机 / 机内镜头 / 仿真测试流)
echo   - 按 [M] 键: 切换 VLM 视觉大模型 (Qwen2.5-VL / MiniCPM-V 2.6 / InternVL 2.5)
echo   - 按 [1][2][3] 键: 快速触发评委核心问答宏 (眯眼应激 / 眩光重塑 / 节能闭环)
echo   - 按 [Q] 键或 [ESC]: 退出系统
echo ==============================================================================
echo.
echo 正在拉起交互窗口，请稍候...
echo.

cd /d "D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control"
"%PYTHON_CMD%" vlm_light_digital_twin_system_v2_0.py

if %errorlevel% neq 0 (
    echo.
    echo ==============================================================================
    echo [提示] 系统运行结束，退出代码: %errorlevel%
    echo 如遇依赖缺失，可运行: "%PYTHON_CMD%" -m pip install opencv-python numpy
    echo ==============================================================================
    pause
)
