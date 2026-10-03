@echo off
chcp 65001 >nul
title GH-VI-2026 实机交互数字孪生一键启动中枢
color 0B

echo ===============================================================================
echo          第 42 届瑞安市青少年科技创新大赛 (CASTIC) 参赛重点攻坚工程
echo            光衡 (GH-VI-2026) 多模态数字孪生实机活体交互系统启动器
echo ===============================================================================
echo.
echo [*] 正在初始化运行环境与路径...
set BLENDER_EXE=D:\Blender Foundation\Blender 5.0\blender.exe
set SCENE_BLEND=D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control\vi7_anti_glare_simulation_v2.blend
set BLENDER_ADDON=D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control\blender_live_viewport_addon.py
set VLM_OPERATOR=D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control\vlm_interactive_live_operator.py

if not exist "%BLENDER_EXE%" (
    echo [错误] 未在 D:\Blender Foundation\Blender 5.0\ 找到 blender.exe，请检查路径！
    pause
    exit /b
)

echo.
echo [*] 步骤 1/2: 正在拉起 Blender 3D 沉浸式数字孪生活体视口 (60 FPS 监听中枢)...
start "" "%BLENDER_EXE%" "%SCENE_BLEND%" -P "%BLENDER_ADDON%"

timeout /t 3 >nul

echo.
echo [*] 步骤 2/2: 正在启动上位机多相机视觉感知与自然语言 Agent 交互控制台...
echo -------------------------------------------------------------------------------
echo  [操作提示]:
echo   1. 控制台窗口将自动捕获您的摄像头 (支持内置/外接USB/运动相机)；
echo   2. 当您对着摄像头【眯眼】或使用【手机手电筒照射】，Blender 里的黑板将实时偏转！
echo   3. 右侧仪表盘将实时展现 Agent 工具调用 (Tool Calling) 过程与调节参数；
echo   4. 按 'Q' 键或 ESC 退出实时交互。
echo -------------------------------------------------------------------------------
echo.

python "%VLM_OPERATOR%"

pause
