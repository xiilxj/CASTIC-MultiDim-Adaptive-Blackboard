#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================================================================
第42届瑞安市青少年科技创新大赛 (CASTIC) 参赛重点攻坚工程
模块名称: VI7 高级专业版数字孪生光学仿真三机位渲染验证脚本
文件路径: D:\\Desktop\\CASTICpjhb\\05-三维建模与Blender渲染\\vlm_control\\render_simulation_v2_previews.py
========================================================================================
"""

import bpy
import os

def render_v2_previews():
    blend_path = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control\vi7_anti_glare_simulation_v2.blend"
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    
    scene = bpy.context.scene
    # 渲染器设置
    engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'RenderSettings') and 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
    scene.render.engine = engine
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    
    # 启用 Bloom / 辉光与体积光增强设置
    if hasattr(scene, 'eevee'):
        if hasattr(scene.eevee, 'use_bloom'):
            scene.eevee.use_bloom = True
        if hasattr(scene.eevee, 'use_volumetric_lights'):
            scene.eevee.use_volumetric_lights = True

    # 设定在 Frame 200 (展开避光展示态)
    scene.frame_set(200)

    out_dir = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control"

    cameras = [
        ("Camera_Classroom_Overview_v2", "preview_sim_v2_overview.png"),
        ("Camera_Student_POV_v2", "preview_sim_v2_student_pov.png"),
        ("Camera_VLM_Sensor_v2", "preview_sim_v2_vlm_sensor.png")
    ]

    for cam_name, img_name in cameras:
        cam_obj = bpy.data.objects.get(cam_name)
        if cam_obj:
            scene.camera = cam_obj
            target_path = os.path.join(out_dir, img_name)
            scene.render.filepath = target_path
            print(f"[Render_v2] 正在渲染机位: {cam_name} -> {target_path}")
            bpy.ops.render.render(write_still=True)
            print(f"[Render_v2] 渲染完成: {target_path}")
        else:
            print(f"[Render_v2] 警告: 未找到相机 {cam_name}")

if __name__ == "__main__":
    render_v2_previews()
