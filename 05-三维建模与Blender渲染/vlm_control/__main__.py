#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CASTIC GH-VI-2026 数字孪生系统主入口模块
"""
import sys
import os

# 将当前目录加入系统搜索路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from vlm_interactive_live_operator import LiveInteractiveOperator, DEFAULT_PROMPT

def main():
    print("=" * 70)
    print("正在启动 GH-VI-2026 多模态实机交互数字孪生系统...")
    print("=" * 70)
    
    # 优先尝试物理摄像头 (0 为笔记本内置，1 为外接 USB/运动相机)
    operator = LiveInteractiveOperator(user_instruction=DEFAULT_PROMPT, cam_id=0)
    operator.run_interactive_loop(max_frames=999999)

if __name__ == "__main__":
    main()
