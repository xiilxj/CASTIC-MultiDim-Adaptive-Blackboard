# -*- coding: utf-8 -*-
"""
========================================================================================
第42届瑞安市青少年科技创新大赛 (CASTIC)
Blender 5.0 真实视口实时投屏与黑板极限展开 (Frame 480) 广播中枢
文件路径: 05-三维建模与Blender渲染/vlm_control/blender_realtime_streamer.py
========================================================================================
功能定位:
  1. 打开 vi7_anti_glare_simulation_v2.blend 真实工程场景；
  2. 监听 live_control_state.json 的黑板开合与展开模式；
  3. 平滑驱动场景时间轴 (Frame 1 完全闭合 <---> Frame 480 最终极限满幅展开)；
  4. 毫秒级抓取 Blender 当前视口渲染画面并写入 D:\vlm_models\live_blender_feed.png，
     向前端主控系统提供真机无延迟数字孪生投屏流！
========================================================================================
"""

import bpy
import json
import os
import time

STATE_FILE = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control\live_control_state.json"
OUT_FEED = r"D:\vlm_models\live_blender_feed.png"

def run_streamer():
    print("[BlenderStreamer] 启动 Blender 5.0 实时数字孪生投屏引擎...")
    os.makedirs(os.path.dirname(OUT_FEED), exist_ok=True)

    scene = bpy.context.scene
    # 确保相机对准教室全景主视口
    cam = bpy.data.objects.get("Camera_Classroom_Overview_v2")
    if cam:
        scene.camera = cam

    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = OUT_FEED

    cur_frame = 480.0
    target_frame = 480.0

    print("[BlenderStreamer] 投屏广播已就绪，当前锁定 Frame 480 (最终极限展开状态)...")

    while True:
        try:
            # 1. 读取控制状态
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    st = json.load(f)
                is_open = st.get("blackboard_display_mode", True)
                # True: 阶段五 Frame 480 最终满幅极限展开; False: 阶段一 Frame 1 完全闭合碰头
                target_frame = 480.0 if is_open else 1.0

            # 2. 时间轴平滑过渡
            diff = target_frame - cur_frame
            if abs(diff) > 1.0:
                cur_frame += diff * 0.25
            else:
                cur_frame = target_frame

            scene.frame_set(int(cur_frame))

            # 3. 极速渲染一帧并输出到投屏路径
            bpy.ops.render.render(write_still=True)
            print(f"[BlenderStreamer] 实时投屏帧更新: Frame {int(cur_frame)}/480 -> {OUT_FEED}")

        except Exception as e:
            print(f"[BlenderStreamer] 异常: {e}")

        time.sleep(0.1)

if __name__ == "__main__":
    run_streamer()
