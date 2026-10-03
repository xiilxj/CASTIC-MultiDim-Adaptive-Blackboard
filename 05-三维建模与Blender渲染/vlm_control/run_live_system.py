#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================================================================
第42届瑞安市青少年科技创新大赛 (CASTIC) 参赛重点攻坚工程
模块名称: 赛场全自动真机活体交互数字孪生系统 Python 核心启动器
文件路径: D:\\Desktop\\CASTICpjhb\\05-三维建模与Blender渲染\\vlm_control\\run_live_system.py
========================================================================================
"""

import os
import sys
import subprocess
import time

def find_blender():
    candidates = [
        r"D:\Blender Foundation\Blender 5.0\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 5.0\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender\blender.exe",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return "blender"

def check_dependencies():
    missing = []
    try:
        import cv2
    except ImportError:
        missing.append("opencv-python")
    try:
        import numpy
    except ImportError:
        missing.append("numpy")

    if missing:
        print(f"[提示] 检测到当前 Python 环境缺少依赖: {missing}")
        print("[提示] 正在自动执行快速安装 (pip install)...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install"] + missing, check=True)
            print("[提示] 依赖安装完成！")
        except Exception as e:
            print(f"[警告] 自动安装失败: {e}，请手动执行 pip install {' '.join(missing)}")

def main():
    print("=" * 75)
    print("第 42 届瑞安市科技创新大赛 - 光衡 (GH-VI-2026) 真机活体数字孪生系统")
    print("=" * 75)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    blend_file = os.path.join(base_dir, "vi7_anti_glare_simulation_v2.blend")
    addon_script = os.path.join(base_dir, "blender_live_viewport_addon.py")
    operator_script = os.path.join(base_dir, "vlm_interactive_live_operator.py")

    # 1. 检测依赖
    check_dependencies()

    # 2. 查找 Blender
    blender_exe = find_blender()
    print(f"[*] 锁定 Blender 执行程序: {blender_exe}")
    print(f"[*] 锁定 3D 数字孪生母本: {blend_file}")

    # 3. 启动 Blender 活体视口 (后台/窗口化进程)
    print("\n[步骤 1/2] 正在拉起 Blender 3D 沉浸式视口 (60 FPS 实时监听)...")
    blender_proc = None
    try:
        blender_cmd = [blender_exe, blend_file, "-P", addon_script]
        blender_proc = subprocess.Popen(blender_cmd)
        print("[+] Blender 活体视口已成功启动！请将 Blender 窗口置于屏幕一侧。")
    except Exception as e:
        print(f"[警告] 启动 Blender 异常: {e}，请直接在 Blender 中手动打开该 .blend 文件！")

    # 稍作等待以确保 Blender 加载
    time.sleep(2)

    # 4. 启动上位机多相机视觉感知中枢
    print("\n[步骤 2/2] 正在启动多相机视觉感知与自然语言 Agent 控制台...")
    print("-----------------------------------------------------------------------")
    print("操作指南:")
    print(" 1. 窗口将自动捕获您的摄像头 (对准面部与眼部)；")
    print(" 2. 当您对着摄像头【眯眼】或使用【手机手电筒照光】，Blender 中的黑板将实时转动；")
    print(" 3. 侧窗百叶窗将自动拉下，危险红光熄灭，安全偏转绿光射向天花板；")
    print(" 4. 按键盘 'Q' 键或 ESC 退出实时交互。")
    print("-----------------------------------------------------------------------\n")

    try:
        import vlm_interactive_live_operator
        operator = vlm_interactive_live_operator.LiveInteractiveOperator(
            user_instruction=vlm_interactive_live_operator.DEFAULT_PROMPT,
            cam_id=0 # 默认使用摄像头 0
        )
        operator.run_interactive_loop(max_frames=999999)
    except Exception as e:
        print(f"[错误] 控制台运行异常: {e}")
    finally:
        if blender_proc:
            print("[*] 正在安全退出系统...")

if __name__ == "__main__":
    main()
