#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================================================================
第42届瑞安市青少年科技创新大赛 (CASTIC) 参赛重点攻坚工程
模块名称: VI7 数字孪生光学教室三机位静帧渲染验证脚本
文件路径: D:\\Desktop\\CASTICpjhb\\05-三维建模与Blender渲染\\vlm_control\\render_simulation_previews.py
========================================================================================
"""

import bpy
import os

def render_previews():
    blend_path = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control\vi7_anti_glare_simulation.blend"
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'RenderSettings') and 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    
    # 我们设置在 Frame 200 (外翻 180° 避光或平展状态) 或者 Frame 1
    # 让我们测试 Frame 200 (已经外展) 或者 Frame 120
    scene.frame_set(200)

    out_dir = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control"

    cameras = [
        ("Camera_Classroom_Overview", "preview_sim_overview.png"),
        ("Camera_Student_POV", "preview_sim_student_pov.png"),
        ("Camera_VLM_Sensor", "preview_sim_vlm_sensor.png")
    ]

    for cam_name, img_name in cameras:
        cam_obj = bpy.data.objects.get(cam_name)
        if cam_obj:
            scene.camera = cam_obj
            target_path = os.path.join(out_dir, img_name)
            scene.render.filepath = target_path
            print(f"[Render] 正在渲染机位: {cam_name} -> {target_path}")
            bpy.ops.render.render(write_still=True)
            print(f"[Render] 完成: {target_path}")
        else:
            print(f"[Render] 警告: 未找到相机 {cam_name}")

if __name__ == "__main__":
    render_previews()
