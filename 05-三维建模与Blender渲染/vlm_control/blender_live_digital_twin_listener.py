#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================================================================
第42届瑞安市青少年科技创新大赛 (CASTIC) 参赛重点攻坚工程
模块名称: Blender 实时数字孪生事件驱动器与机构动态响应中枢
文件路径: D:\\Desktop\\CASTICpjhb\\05-三维建模与Blender渲染\\vlm_control\\blender_live_digital_twin_listener.py
审核标识: 第 34 轮工程技术审核
========================================================================================
功能定位:
  1. 在 Blender 内部常驻运行 (通过 bpy.app.timers 高频定时器，30 FPS)；
  2. 实时非阻塞读取 live_control_state.json 共享控制状态；
  3. 机构平滑阻尼联动驱动 (S曲线平滑 Lerp 插值):
     - Ctrl_Flip_Left: 绕本地 Z 轴实时偏转 (0° ~ 18°)
     - 危险红色光束 Beam_Danger_Glared_POV: 随避光完成逐渐衰减熄灭
     - 安全绿色光束 Beam_Safe_Yawed_Ceiling: 随偏转完成高亮激活射向天花板
     - 侧窗阳光 Spot_Tyndall_Beam: 随百叶帘降下实现智能调光
  4. 支持无头单帧验证与常驻视口动态演示双模。
========================================================================================
"""

import bpy
import json
import math
import os
import sys

STATE_FILE = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control\live_control_state.json"
if not os.path.exists(STATE_FILE):
    # WSL 兼容路径
    STATE_FILE = r"/mnt/d/Desktop/CASTICpjhb/05-三维建模与Blender渲染/vlm_control/live_control_state.json"

# 缓存当前动画变量
current_state = {
    "current_yaw_deg": 0.0,
    "target_yaw_deg": 0.0,
    "smart_blinds_pct": 0.0,
    "last_mtime": 0.0
}

def update_digital_twin_frame():
    global current_state
    
    # 1. 检测状态文件是否有更新
    if not os.path.exists(STATE_FILE):
        return 0.05

    try:
        mtime = os.path.getmtime(STATE_FILE)
        if mtime != current_state["last_mtime"]:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                current_state["target_yaw_deg"] = float(data.get("target_board_yaw_deg", 0.0))
                current_state["smart_blinds_pct"] = float(data.get("smart_blinds_pct", 0.0))
                current_state["last_mtime"] = mtime
    except Exception as e:
        # 避免读取冲突
        return 0.05

    # 2. S 曲线阻尼平滑插值 (Lerp)，模拟物理电机加减速
    target_yaw = current_state["target_yaw_deg"]
    curr_yaw = current_state["current_yaw_deg"]
    diff = target_yaw - curr_yaw

    if abs(diff) > 0.01:
        # 平滑移动 15% 步长
        curr_yaw += diff * 0.15
        current_state["current_yaw_deg"] = curr_yaw

        # 驱动 Blender 核心控制器: Ctrl_Flip_Left
        ctrl_flip_l = bpy.data.objects.get("Ctrl_Flip_Left")
        if ctrl_flip_l:
            ctrl_flip_l.rotation_mode = 'XYZ'
            # 偏航角旋转 (向内偏转)
            ctrl_flip_l.rotation_euler.z = math.radians(curr_yaw)

        # 驱动侧窗百叶窗下放位移 (Arch_Window_Frame_Alloy / 百叶帘)
        # 驱动穿透性日光与高能激光束强弱
        danger_core = bpy.data.objects.get("Beam_Danger_Glared_POV_Core")
        danger_halo = bpy.data.objects.get("Beam_Danger_Glared_POV_Halo")
        safe_core = bpy.data.objects.get("Beam_Safe_Yawed_Ceiling_Core")
        safe_halo = bpy.data.objects.get("Beam_Safe_Yawed_Ceiling_Halo")

        # 当偏转角度达到 12° 以上时，危险红光完全切除消散，安全绿光完全点亮
        progress = max(0.0, min(1.0, curr_yaw / 18.0))

        if danger_core and danger_halo:
            # 避光过程中红光逐渐隐去
            danger_core.scale = (1.0 - progress * 0.95, 1.0 - progress * 0.95, 1.0)
            danger_halo.scale = (1.0 - progress * 0.95, 1.0 - progress * 0.95, 1.0)

        if safe_core and safe_halo:
            # 安全绿光显现
            safe_core.scale = (0.05 + progress * 0.95, 0.05 + progress * 0.95, 1.0)
            safe_halo.scale = (0.05 + progress * 0.95, 0.05 + progress * 0.95, 1.0)

        # 调光百叶帘与丁达尔斜射光强度
        spot_tyndall = bpy.data.objects.get("Spot_Tyndall_Beam")
        if spot_tyndall and hasattr(spot_tyndall, "data"):
            # 随百叶窗遮蔽 65%，侧窗入射光强度从 2500W 降至 900W 舒适柔和漫光
            spot_tyndall.data.energy = 2500.0 * (1.0 - progress * 0.64)

    return 0.033 # 约 30 FPS 刷新

def register_live_listener():
    print("[DigitalTwinListener] 启动 Blender 实时数字孪生监听服务...")
    # 移除旧定时器以防重复
    if update_digital_twin_frame in bpy.app.timers.registered_timers():
        bpy.app.timers.unregister(update_digital_twin_frame)
    bpy.app.timers.register(update_digital_twin_frame, persistent=True)
    print("[DigitalTwinListener] 监听器已就绪！每 33ms 自动轮询 live_control_state.json")

def execute_single_state_update(target_yaw_deg=18.0, blinds_pct=65.0):
    """
    单次步进驱动模式 (用于无头脚本调用与测试)
    """
    ctrl_flip_l = bpy.data.objects.get("Ctrl_Flip_Left")
    if ctrl_flip_l:
        ctrl_flip_l.rotation_mode = 'XYZ'
        ctrl_flip_l.rotation_euler.z = math.radians(target_yaw_deg)
        print(f"[DigitalTwinListener] 已将 Ctrl_Flip_Left 偏航角调整至: {target_yaw_deg}°")

    spot_tyndall = bpy.data.objects.get("Spot_Tyndall_Beam")
    if spot_tyndall and hasattr(spot_tyndall, "data"):
        spot_tyndall.data.energy = 2500.0 * (1.0 - (blinds_pct / 100.0))
        print(f"[DigitalTwinListener] 已将侧窗丁达尔强光功率调整至: {spot_tyndall.data.energy} W")

if __name__ == "__main__":
    if "--live" in sys.argv:
        register_live_listener()
    else:
        # 默认执行一次状态响应并保存
        execute_single_state_update(18.0, 65.0)
