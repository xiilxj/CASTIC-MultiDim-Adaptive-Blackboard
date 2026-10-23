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

rem 1. 静态锁定 Python 运行环境
set "PY_EXE=C:\Program Files\Python310\python.exe"
if exist "%PY_EXE%" goto :py_found
if exist "C:\Users\Lenovo\AppData\Local\Programs\Python\Python310\python.exe" (
    set "PY_EXE=C:\Users\Lenovo\AppData\Local\Programs\Python\Python310\python.exe"
    goto :py_found
)
set "PY_EXE=python"

:py_found
echo [1/3] 核心解释器已锁定: %PY_EXE%

rem 2. 静态锁定模型路径与多模态视觉投影层权重
set "LLAMA_DIR=D:\llama-b10066-bin-win-vulkan-x64"
set "MODEL_PATH=D:\llama-b10066-bin-win-vulkan-x64\models\Qwen2.5-VL-3B-Instruct-Q4_K_M.gguf"
set "MMPROJ_PATH=D:\llama-b10066-bin-win-vulkan-x64\models\mmproj-model-f16.gguf"
set "WORK_DIR=D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control"

echo [2/3] 正在检测本地 Qwen2.5-VL 神经视觉模型引擎 (端口 8080)...
netstat -ano | findstr ":8080 " | findstr "LISTENING" > nul
if not errorlevel 1 goto :server_online

echo       [提示] 正在后台热拉起 Qwen2.5-VL (本地 Vulkan GPU 加速 + mmproj 视觉投影层)...
if exist "%LLAMA_DIR%\llama-server.exe" (
    start "Qwen2.5-VL Backend Engine" /min "%LLAMA_DIR%\llama-server.exe" -m "%MODEL_PATH%" --mmproj "%MMPROJ_PATH%" --port 8080 -ngl 99 -c 4096 --host 127.0.0.1
    timeout /t 3 > nul
    echo       [OK] 模型引擎后台拉起指令已下发。
    goto :start_gui
)
echo       [警告] 未检测到 llama-server 路径，系统将自动使用单机物理推导高保真引擎。
goto :start_gui

:server_online
echo       [OK] Qwen2.5-VL 本地推理中枢已在线 (端口 8080 活跃)。

:start_gui
rem 3. 启动 PyQt5 前台主控交互界面
echo [3/3] 正在启动主控交互界面 (v3.0 旗舰版)...
cd /d "%WORK_DIR%"
start "" "%PY_EXE%" vlm_gui_system_v3_0.py

echo.
echo ==============================================================================
echo [完成] CASTIC 旗舰版系统启动指令已全部执行！
echo [操作提示]
echo   - 键盘 'V' : 循环切换 [3D全景环顾] / [受照学生第一人称视角] / [真实摄像头]
echo   - 鼠标右键拖拽 : 360度自由旋转视角 (仰望天花板无影灯 / 俯视课桌落点)
echo   - 鼠标左键拖拽 : 拖动黑板手电筒光斑；滚轮调节照度 (0~5000 Lux)
echo ==============================================================================
timeout /t 3 > nul
exit /b 0
