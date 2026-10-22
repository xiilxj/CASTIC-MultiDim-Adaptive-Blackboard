# -*- coding: utf-8 -*-
"""
========================================================================================
第42届瑞安市青少年科技创新大赛 (CASTIC) 参赛重点攻坚工程
模块名称: Blender 5.0 数字孪生后台监听与异步离线视口渲染桥接器
文件路径: 05-三维建模与Blender渲染/vlm_control/blender_digital_twin_bridge.py
========================================================================================
功能定位:
  1. 监听 live_control_state.json 的黑板展开状态与微倾角度；
  2. 自动驱动 Blender 场景中 Ctrl_Flip_Left 主铰链旋转 (0.0° ~ 4.5°)；
  3. 自动调控红色刺眼反光光锥与绿色避眩光上导光锥的缩放显示；
  4. 渲染最新的教室全景图至 live_blender_frame.png，供前端 GUI 毫秒级热更投射！
========================================================================================
"""

import bpy
import json
import math
import os
import time

STATE_FILE = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control\live_control_state.json"
OUT_IMG = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control\live_blender_frame.png"

def main_loop():
    print("[BlenderBridge] Blender 5.0 数字孪生后台监听已就绪，正在轮询 IPC 状态...")
    last_yaw = -999.0

    while True:
        try:
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    state = json.load(f)
                
                target_yaw = float(state.get("target_board_yaw_deg", 4.5))
                if abs(target_yaw - last_yaw) > 0.05:
                    print(f"[BlenderBridge] 捕获黑板目标偏角更新: {target_yaw:.2f}° (前值: {last_yaw:.2f}°)")
                    last_yaw = target_yaw

                    # 1. 驱动 Blender 核心控制器
                    ctrl = bpy.data.objects.get("Ctrl_Flip_Left")
                    if ctrl:
                        ctrl.rotation_mode = 'XYZ'
                        ctrl.rotation_euler.z = math.radians(target_yaw)

                    # 2. 调控光锥
                    danger_core = bpy.data.objects.get("Beam_Danger_Glared_POV_Core")
                    safe_core = bpy.data.objects.get("Beam_Safe_Yawed_Ceiling_Core")
                    progress = max(0.0, min(1.0, target_yaw / 4.5))

                    if danger_core:
                        s_val = max(0.01, 1.0 - progress)
                        danger_core.scale = (s_val, s_val, 1.0)
                    if safe_core:
                        s_val = max(0.05, progress)
                        safe_core.scale = (s_val, s_val, 1.0)

                    # 3. 渲染单帧并保存
                    scene = bpy.context.scene
                    cam = bpy.data.objects.get("Camera_Classroom_Overview_v2")
                    if cam:
                        scene.camera = cam
                    scene.render.filepath = OUT_IMG
                    scene.render.resolution_x = 1280
                    scene.render.resolution_y = 720
                    scene.render.resolution_percentage = 100
                    print(f"[BlenderBridge] 开始渲染最新视口帧至: {OUT_IMG}...")
                    bpy.ops.render.render(write_still=True)
                    print(f"[BlenderBridge] 视口帧渲染完成并已写入！")
        except Exception as e:
            print(f"[BlenderBridge] 轮询异常: {e}")

        time.sleep(1.0)

if __name__ == "__main__":
    main_loop()
