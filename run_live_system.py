#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CASTIC GH-VI-2026 根目录一键调度引导桥接脚本 (纯 ASCII 路径兼容)
"""
import os
import sys

# 锁定真实子目录
current_dir = os.path.dirname(os.path.abspath(__file__))
target_dir = os.path.join(current_dir, "05-三维建模与Blender渲染", "vlm_control")

if not os.path.exists(target_dir):
    # 兼容跨平台与相对路径
    alt_dir = os.path.join(r"D:\Desktop\CASTICpjhb", "05-三维建模与Blender渲染", "vlm_control")
    if os.path.exists(alt_dir):
        target_dir = alt_dir

# 切换工作空间并引入模块路径
sys.path.insert(0, target_dir)
os.chdir(target_dir)

import run_live_system

if __name__ == "__main__":
    run_live_system.main()
