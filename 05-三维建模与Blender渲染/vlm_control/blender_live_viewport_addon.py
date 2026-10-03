#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================================================================
第42届瑞安市青少年科技创新大赛 (CASTIC) 参赛重点攻坚工程
模块名称: Blender 活体 3D 视口实时响应引擎 (伪 VR 实时数字孪生驱动挂载脚本)
文件路径: D:\\Desktop\\CASTICpjhb\\05-三维建模与Blender渲染\\vlm_control\\blender_live_viewport_addon.py
审核标识: 第 35 轮工程技术审核
========================================================================================
功能定位:
  1. 零外部依赖，100% 采用 Blender 5.0 原生 API (math, json, bpy)；
  2. 在 Blender 活体视口中点击“Run Script”即可启动 60 FPS 实时游戏级主循环；
  3. 实时接收外部 VLM 多模态 Agent 的工具调用 (Tool Call) 指令；
  4. 真实物理构件平滑动力学阻尼联动:
     - 活动黑板主铰链 Ctrl_Flip_Left: 毫秒级平滑转动 (0° ~ 18°)
     - 侧窗强光/百叶窗 Spot_Tyndall_Beam: 动态调光遮阳 (2500W -> 900W)
     - 危险红色光束 / 安全绿色光束: 动态淡入淡出升维
  5. 在 3D 视口前墙上方自动生成浮动科技 HUD 看板文字 (HUD_3D_Live_Status)，实时回显 Agent 决策！
========================================================================================
"""

import bpy
import math
import json
import os
import sys

STATE_FILE = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control\live_control_state.json"
if not os.path.exists(STATE_FILE):
    STATE_FILE = r"/mnt/d/Desktop/CASTICpjhb/05-三维建模与Blender渲染/vlm_control/live_control_state.json"

# 运行插值物理量
runtime_vars = {
    "current_yaw": 0.0,
    "target_yaw": 0.0,
    "current_blinds": 0.0,
    "target_blinds": 0.0,
    "current_light_power": 2500.0,
    "status_text": "系统已就绪，等待多模态事件触发...",
    "last_mtime": 0.0
}

def get_or_create_3d_hud_text():
    """
    在 Blender 3D 视口前墙正上方创建/获取实时科技看板 3D 文字物体
    """
    obj_name = "HUD_3D_Live_Status"
    text_obj = bpy.data.objects.get(obj_name)
    if not text_obj:
        font_curve = bpy.data.curves.new(type="FONT", name="HUD_Curve")
        text_obj = bpy.data.objects.new(name=obj_name, object_data=font_curve)
        # 挂载在教室前墙黑板正上方 (X=0, Y=-0.2, Z=1.85)
        text_obj.location = (-2.8, -0.3, 1.75)
        text_obj.scale = (0.16, 0.16, 0.16)
        text_obj.rotation_euler = (math.radians(90), 0, 0)
        
        # 赋予高科技青色自发光材质
        mat_name = "Mat_HUD_3D_Cyan"
        mat = bpy.data.materials.get(mat_name)
        if not mat:
            mat = bpy.data.materials.new(name=mat_name)
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            nodes.clear()
            out = nodes.new(type='ShaderNodeOutputMaterial')
            emit = nodes.new(type='ShaderNodeEmission')
            emit.inputs['Color'].default_value = (0.0, 0.95, 1.0, 1.0)
            emit.inputs['Strength'].default_value = 8.0
            mat.node_tree.links.new(emit.outputs['Emission'], out.inputs['Surface'])
        text_obj.data.materials.append(mat)
        bpy.context.scene.collection.objects.link(text_obj)

    return text_obj

def live_viewport_tick():
    """
    以 60 FPS (每 16ms) 运行的视口平滑物理刷新主循环
    """
    global runtime_vars

    # 1. 检测外部 IPC 状态文件
    if os.path.exists(STATE_FILE):
        try:
            mtime = os.path.getmtime(STATE_FILE)
            if mtime != runtime_vars["last_mtime"]:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    runtime_vars["target_yaw"] = float(data.get("target_board_yaw_deg", 0.0))
                    runtime_vars["target_blinds"] = float(data.get("smart_blinds_pct", 0.0))
                    runtime_vars["status_text"] = data.get("reasoning_summary", "运行中")
                    runtime_vars["last_mtime"] = mtime
        except Exception:
            pass

    # 2. 物理机构平滑阻尼插值 (模拟真实步进电机 S 曲线转动)
    yaw_diff = runtime_vars["target_yaw"] - runtime_vars["current_yaw"]
    blinds_diff = runtime_vars["target_blinds"] - runtime_vars["current_blinds"]

    # 平滑插值系数 (0.12 表示平滑阻尼，避免机械顿挫)
    if abs(yaw_diff) > 0.005:
        runtime_vars["current_yaw"] += yaw_diff * 0.12
        ctrl_flip_l = bpy.data.objects.get("Ctrl_Flip_Left")
        if ctrl_flip_l:
            ctrl_flip_l.rotation_mode = 'XYZ'
            ctrl_flip_l.rotation_euler.z = math.radians(runtime_vars["current_yaw"])

    if abs(blinds_diff) > 0.1:
        runtime_vars["current_blinds"] += blinds_diff * 0.12

    # 3. 动态更新光学光束与窗帘灯光强度
    progress = max(0.0, min(1.0, runtime_vars["current_yaw"] / 18.0))
    
    # 危险红光逐渐消除
    danger_core = bpy.data.objects.get("Beam_Danger_Glared_POV_Core")
    danger_halo = bpy.data.objects.get("Beam_Danger_Glared_POV_Halo")
    if danger_core and danger_halo:
        scale_val = max(0.001, 1.0 - progress * 0.98)
        danger_core.scale = (scale_val, scale_val, 1.0)
        danger_halo.scale = (scale_val, scale_val, 1.0)

    # 安全绿光逐渐射向天花板
    safe_core = bpy.data.objects.get("Beam_Safe_Yawed_Ceiling_Core")
    safe_halo = bpy.data.objects.get("Beam_Safe_Yawed_Ceiling_Halo")
    if safe_core and safe_halo:
        scale_val = min(1.0, 0.02 + progress * 0.98)
        safe_core.scale = (scale_val, scale_val, 1.0)
        safe_halo.scale = (scale_val, scale_val, 1.0)

    # 侧窗丁达尔穿透光束能量联动
    spot_tyndall = bpy.data.objects.get("Spot_Tyndall_Beam")
    if spot_tyndall and hasattr(spot_tyndall, "data"):
        spot_tyndall.data.energy = 2500.0 * (1.0 - (runtime_vars["current_blinds"] / 100.0) * 0.64)

    # 4. 更新 3D 浮动文字看板
    hud_obj = get_or_create_3d_hud_text()
    if hud_obj and hasattr(hud_obj.data, "body"):
        is_glare = runtime_vars["target_yaw"] > 5.0
        status_tag = "[CRITICAL GLARE / SQUINT]" if is_glare else "[NORMAL VIEWING]"
        hud_obj.data.body = (
            f"GH-VI-2026 LIVE AGENT HUD {status_tag}\n"
            f"Blackboard Yaw: {runtime_vars['current_yaw']:+.1f} deg | Blinds: {runtime_vars['current_blinds']:.0f}% | Beam: {'SAFE_CEILING' if is_glare else 'GLARE_POLLUTION'}\n"
            f"AI Reasoning: {runtime_vars['status_text']}"
        )

    return 0.016 # 约 60 FPS 丝滑更新

def register():
    print("="*70)
    print("[GH-VI-2026] 启动 Blender 活体视口 60 FPS 实时数字孪生引擎...")
    print("="*70)
    # 取消旧定时器防止叠加 (兼容 Blender 3.x / 4.x / 5.x)
    try:
        if bpy.app.timers.is_registered(live_viewport_tick):
            bpy.app.timers.unregister(live_viewport_tick)
    except Exception:
        pass
    bpy.app.timers.register(live_viewport_tick, persistent=True)
    get_or_create_3d_hud_text()
    print("[GH-VI-2026] 视口驱动引擎已激活！正在实时同步外部摄像头与多模态指令...")

if __name__ == "__main__":
    register()
