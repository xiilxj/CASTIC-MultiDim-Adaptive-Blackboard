@echo off
@chcp 65001 >nul
title 光衡 GH-VI-2026: MATLAB 双全景物理仿真看板启动器
color 0b

echo ================================================================================
echo   ★ 光衡 (GH-VI-2026) MATLAB R2025b 双全景物理仿真看板一键拉起中枢 ★
echo   全国青少年科技创新大赛 (CASTIC) 参赛重点工程 · 物理与工程学专项
echo ================================================================================
echo.
echo  正在定位工作目录...
set "SIM_DIR=D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control"
cd /d "%SIM_DIR%"

echo  正在调用 MATLAB R2025b 引擎执行两大核心仿真程序：
echo    [1/2] castic_unified_equation_simulation.m (物理光学与人因感知大一统四分屏看板)
echo    [2/2] castic_live_demo_runner.m            (空间逆运动学与全天动态采光六分屏看板)
echo.

start "" matlab -nosplash -r "try, cd('D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control'); castic_unified_equation_simulation; castic_live_demo_runner; fprintf('\n================================================================================\n  ★ 双全景科研看板已全部成功绘制并弹出！请查看桌面交互 Figure 窗口 ★\n================================================================================\n'); catch ME, disp(ME.message); end"

echo ================================================================================
echo  [成功派发] MATLAB 仿真主进程已启动，两个交互式科研 Figure 视窗正在弹出！
echo  
echo  若已打开 MATLAB 窗口，亦可在 MATLAB 命令行直接黏贴以下两行运行：
echo    cd('D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control');
echo    castic_unified_equation_simulation; castic_live_demo_runner;
echo ================================================================================
echo.
pause
