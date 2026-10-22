@echo off
rem ==============================================================================
rem GH-VI-2026 VLM Digital Twin Control System v3.0 (PyQt5 Edition)
rem ==============================================================================
chcp 936 > nul
title GH-VI-2026 多模态VLM数字孪生主控系统 v3.0
color 0B

echo ==============================================================================
echo        GH-VI-2026 多模态 VLM 教室光环境数字孪生主控系统 (v3.0 PyQt5 旗舰版)
echo ==============================================================================
echo.

set "PY_EXE=C:\Program Files\Python310\python.exe"

if not exist "%PY_EXE%" (
    if exist "C:\Users\Lenovo\AppData\Local\Programs\Python\Python310\python.exe" (
        set "PY_EXE=C:\Users\Lenovo\AppData\Local\Programs\Python\Python310\python.exe"
    ) else (
        set "PY_EXE=python"
    )
)

echo [OK] 锁定高兼容视觉引擎: %PY_EXE%
echo.
echo [核心特性指南]:
echo   - 原生中文打字: 直接点击界面内输入框，支持系统输入法自由打字对话！
echo   - 运动相机自动绑定: 默认自动锁定 [CAM 1] DJI Osmo Action 5 Pro 高清视频流
echo   - 算法双模切换: 界面上方一键单选 OpenCV 眯眼识别 或 Qwen2.5-VL 视觉大模型
echo   - 无影灯主动相消: 顶部光源全程锁定黑板，随日光动态加力消除反光干扰
echo   - 黑板展示态控制: 一键切换黑板展开关键帧动画与常规态
echo ==============================================================================
echo.
echo 正在拉起 PyQt5 现代暗黑交互窗口，请稍候...
echo.

cd /d "D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control"
"%PY_EXE%" vlm_gui_system_v3_0.py %*

if %errorlevel% neq 0 (
    echo.
    echo ==============================================================================
    echo [提示] 程序已退出，退出代码: %errorlevel%
    echo ==============================================================================
    pause
)
