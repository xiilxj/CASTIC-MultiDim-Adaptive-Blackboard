@echo off
rem ==============================================================================
rem  GH-VI-2026: MATLAB Dual Dashboard One-Click Launcher (GBK Windows Native)
rem ==============================================================================
title 光衡 (GH-VI-2026) MATLAB 双全景物理仿真看板启动器
color 0b

echo ================================================================================
echo   [光衡 GH-VI-2026] MATLAB R2025b 双全景物理仿真看板一键启动中枢
echo   全国青少年科技创新大赛 (CASTIC) 参赛重点工程 · 物理与工程学专项
echo ================================================================================
echo.

set "TARGET_DIR=D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control"
cd /d "%TARGET_DIR%"

set "MATLAB_BIN="
if exist "D:\Program Files\MATLAB\R2025b\bin\matlab.exe" (
    set "MATLAB_BIN=D:\Program Files\MATLAB\R2025b\bin\matlab.exe"
    goto :RunMatlab
)
if exist "C:\Program Files\MATLAB\R2025b\bin\matlab.exe" (
    set "MATLAB_BIN=C:\Program Files\MATLAB\R2025b\bin\matlab.exe"
    goto :RunMatlab
)
for /f "delims=" %%I in ('where matlab.exe 2^>nul') do (
    set "MATLAB_BIN=%%I"
    goto :RunMatlab
)
goto :NoMatlab

:RunMatlab
echo  [成功定位] 发现 MATLAB 可执行引擎:
echo  "%MATLAB_BIN%"
echo.
echo  正在拉起两大核心仿真看板：
echo    1. castic_unified_equation_simulation.m [偏微积分大一统理论 4 分屏看板]
echo    2. castic_live_demo_runner.m            [物理光学与空间逆运动学 6 分屏全景看板]
echo.
start "" "%MATLAB_BIN%" -nosplash -r "try, cd('%TARGET_DIR%'); castic_unified_equation_simulation; castic_live_demo_runner; catch ME, disp(ME.message); end"
echo  [状态] MATLAB 仿真计算已派发，正在绘制并弹出交互 Figure 窗口！
goto :Done

:NoMatlab
echo  [提示] 未在默认路径找到 matlab.exe。
echo  若 MATLAB 已在运行，请直接在 MATLAB 命令行窗口粘贴运行下方命令：
goto :Done

:Done
echo.
echo ================================================================================
echo  【极简备用方案：直接在已打开的 MATLAB 命令行粘贴运行】
echo.
echo  cd('D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control'); castic_unified_equation_simulation; castic_live_demo_runner;
echo.
echo ================================================================================
echo.
pause
