@echo off
rem ==============================================================================
rem 第42届全国青少年科技创新大赛 (CASTIC)
rem 多模态 VLM 自适应防眩光智慧黑板与无影补光系统 - 旗舰版一键总控启动器
rem ==============================================================================
chcp 65001 > nul
title CASTIC 多模态 VLM 智慧教室数字孪生系统 v3.0 旗舰版
color 0B

echo ==============================================================================
echo       CASTIC-2026 多模态 VLM 光环境自适应调控系统 (旗舰版一键自愈启动)
echo ==============================================================================
echo.

rem 1. 定位 Python 运行环境
set "PY_EXE=C:\Program Files\Python310\python.exe"
if not exist "%PY_EXE%" (
    if exist "C:\Users\Lenovo\AppData\Local\Programs\Python\Python310\python.exe" (
        set "PY_EXE=C:\Users\Lenovo\AppData\Local\Programs\Python\Python310\python.exe"
    ) else (
        set "PY_EXE=python"
    )
)
echo [1/3] 核心解释器已锁定: %PY_EXE%

rem 2. 检测并自愈拉起本地 Qwen2.5-VL 模型服务 (llama-server.exe)
echo [2/3] 正在检测本地 Qwen2.5-VL 神经视觉模型引擎 (端口 8080)...
netstat -ano | findstr ":8080 " | findstr "LISTENING" > nul
if %errorlevel% equ 0 (
    echo       [OK] Qwen2.5-VL 本地推理中枢已在线 (端口 8080 活跃)。
) else (
    echo       [提示] 正在后台热拉起 Qwen2.5-VL (本地 Vulkan GPU 加速)...
    set "LLAMA_DIR=D:\llama-b10066-bin-win-vulkan-x64"
    set "MODEL_PATH=D:\llama-b10066-bin-win-vulkan-x64\models\Qwen2.5-VL-3B-Instruct-Q4_K_M.gguf"
    if exist "%LLAMA_DIR%\llama-server.exe" (
        start "Qwen2.5-VL Backend Engine" /min "%LLAMA_DIR%\llama-server.exe" -m "%MODEL_PATH%" --port 8080 -ngl 99 -c 4096 --host 127.0.0.1
        timeout /t 3 > nul
        echo       [OK] 模型引擎后台拉起指令已下发。
    ) else (
        echo       [警告] 未检测到 llama-server 路径，系统将自动使用单机物理推导高保真引擎。
    )
)

rem 3. 启动 PyQt5 前台主控交互界面
echo [3/3] 正在启动主控交互界面 (v3.0 旗舰版)...
cd /d "D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control"
start "" "%PY_EXE%" vlm_gui_system_v3_0.py

echo.
echo ==============================================================================
echo [完成] CASTIC 旗舰版系统启动指令已全部执行！
echo [提示] 按键盘 'V' 可在“3D全景”、“受照学生第一人称视角”、“真实摄像头”三路自由切换。
echo ==============================================================================
timeout /t 3 > nul
exit
