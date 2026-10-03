#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================================================================
第42届瑞安市青少年科技创新大赛 (CASTIC) 参赛重点攻坚工程
模块名称: VI7 数字孪生光学仿真与多模态感知教室场景构建中枢
文件路径: D:\\Desktop\\CASTICpjhb\\05-三维建模与Blender渲染\\vlm_control\\build_vi7_anti_glare_simulation.py
输出产物: D:\\Desktop\\CASTICpjhb\\05-三维建模与Blender渲染\\vlm_control\\vi7_anti_glare_simulation.blend
审核标识: 第 31 轮工程技术审核
========================================================================================
几何与物理标定体系 (以黑板中心 Z=0.0 为基准):
  - 教室地面 (Floor): Z = -1.40m (黑板底沿下放 0.85m，符合中小学工效学规范)
  - 教室天花板 (Ceiling): Z = +2.20m (净高 3.6m)
  - 前墙 (Front Wall): Y = +0.06m (在黑板构件正后方)
  - 讲台 (Podium): 高 0.15m (Z 从 -1.40m 至 -1.25m)
  - 学生课桌 (Desk): 桌面高度 Z = -0.64m (距地 0.76m)
  - 学生座椅 (Chair): 座面高度 Z = -0.96m (距地 0.44m)
  - 学生人眼标定点 (Eye Point): 坐姿高度 Z = -0.25m (距地 1.15m)
  - 光学三光束:
    * 入射光束 (Sun_Incident): 侧窗 (-4.0, -3.5, 1.5) -> 黑板 (-1.5, -0.06, 0.0)
    * 未避光高危光束 (Danger_Reflected): 黑板 (-1.5, -0.06, 0.0) -> 学生眼 (-2.6, -2.95, -0.25)
    * 避光安全光束 (Safe_Reflected): 黑板 (-1.5, -0.06, 0.0) -> 天花板安全区 (0.6, -4.8, 2.15)
========================================================================================
"""

import bpy
import math
import os
import sys
import mathutils

def build_simulation_scene():
    source_blend = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\VI系列\vi7.blend"
    output_blend = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control\vi7_anti_glare_simulation.blend"

    print(f"[SimBuilder] 正在打开 VI7 基础母本工程: {source_blend}")
    bpy.ops.wm.open_mainfile(filepath=source_blend)

    scene = bpy.context.scene
    coll_root = scene.collection

    def get_or_create_coll(name):
        for c in coll_root.children:
            if c.name == name:
                return c
        c = bpy.data.collections.new(name)
        coll_root.children.link(c)
        return c

    coll_env = get_or_create_coll("01_Classroom_Environment")
    coll_seats = get_or_create_coll("02_Student_45_Seats_Matrix")
    coll_optics = get_or_create_coll("03_Optical_Ray_Tracing_Beams")
    coll_cams = get_or_create_coll("04_Multi_View_Cameras")

    # ---------------------------------------------------------
    # 1. 材质定义
    # ---------------------------------------------------------
    def create_emission_mat(name, color_rgba, strength):
        mat = bpy.data.materials.get(name)
        if not mat:
            mat = bpy.data.materials.new(name=name)
            mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        node_out = nodes.new(type='ShaderNodeOutputMaterial')
        node_emit = nodes.new(type='ShaderNodeEmission')
        node_emit.inputs['Color'].default_value = color_rgba
        node_emit.inputs['Strength'].default_value = strength
        links.new(node_emit.outputs['Emission'], node_out.inputs['Surface'])
        return mat

    def create_pbr_mat(name, base_color, roughness=0.5):
        mat = bpy.data.materials.get(name)
        if not mat:
            mat = bpy.data.materials.new(name=name)
            mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        node_out = nodes.new(type='ShaderNodeOutputMaterial')
        node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        node_bsdf.inputs['Base Color'].default_value = base_color
        node_bsdf.inputs['Roughness'].default_value = roughness
        links.new(node_bsdf.outputs['BSDF'], node_out.inputs['Surface'])
        return mat

    mat_beam_sun = create_emission_mat("Mat_Beam_Sun", (1.0, 0.88, 0.25, 1.0), 16.0)
    mat_beam_danger = create_emission_mat("Mat_Beam_Danger", (1.0, 0.05, 0.02, 1.0), 20.0)
    mat_beam_safe = create_emission_mat("Mat_Beam_Safe", (0.05, 1.0, 0.35, 1.0), 16.0)
    mat_wall = create_pbr_mat("Mat_Classroom_Wall", (0.90, 0.92, 0.94, 1.0), 0.8)
    mat_floor = create_pbr_mat("Mat_Classroom_Floor", (0.55, 0.52, 0.48, 1.0), 0.3)
    mat_desk = create_pbr_mat("Mat_Student_Desk", (0.82, 0.72, 0.55, 1.0), 0.4)
    mat_chair = create_pbr_mat("Mat_Student_Chair", (0.18, 0.35, 0.65, 1.0), 0.3)
    mat_window = create_pbr_mat("Mat_Window_Glass", (0.8, 0.9, 1.0, 0.1), 0.1)

    # ---------------------------------------------------------
    # 2. 真实教室空间结构构建 (以黑板中心 Z=0 为基准)
    # ---------------------------------------------------------
    print("[SimBuilder] 正在生成教室空间结构 (地板、前墙、天花板、侧窗、讲台)...")
    z_floor = -1.40
    z_ceiling = 2.20
    y_front = 0.06 # 黑板后方

    # A. 地板 (Floor): X in [-4.0, 4.0], Y in [0.06, -9.6], Z = -1.40
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -4.77, z_floor - 0.05))
    floor = bpy.context.active_object
    floor.name = "Env_Classroom_Floor"
    floor.scale = (8.0, 9.66, 0.1)
    floor.data.materials.append(mat_floor)
    coll_env.objects.link(floor)
    coll_root.objects.unlink(floor)

    # B. 天花板 (Ceiling): Z = +2.20
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -4.77, z_ceiling + 0.05))
    ceiling = bpy.context.active_object
    ceiling.name = "Env_Classroom_Ceiling"
    ceiling.scale = (8.0, 9.66, 0.1)
    ceiling.data.materials.append(mat_wall)
    coll_env.objects.link(ceiling)
    coll_root.objects.unlink(ceiling)

    # C. 前墙 (Front Wall): Y = +0.06, X in [-4.0, 4.0], Z in [-1.40, 2.20]
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, y_front + 0.05, 0.40))
    wall_front = bpy.context.active_object
    wall_front.name = "Env_Wall_Front"
    wall_front.scale = (8.0, 0.1, 3.60)
    wall_front.data.materials.append(mat_wall)
    coll_env.objects.link(wall_front)
    coll_root.objects.unlink(wall_front)

    # D. 采光侧墙与侧窗 (左侧 X = -4.0m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-4.0, -5.0, 0.60))
    window_frame = bpy.context.active_object
    window_frame.name = "Env_Window_Frame_Left"
    window_frame.scale = (0.08, 7.0, 2.0)
    window_frame.data.materials.append(mat_window)
    coll_env.objects.link(window_frame)
    coll_root.objects.unlink(window_frame)

    # E. 讲台 (Podium Platform): Y in [0.0, -1.2], X in [-3.8, 3.8], 高 0.15m (Z in [-1.40, -1.25])
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -0.60, z_floor + 0.075))
    podium = bpy.context.active_object
    podium.name = "Env_Podium_Platform"
    podium.scale = (7.6, 1.2, 0.15)
    podium.data.materials.append(mat_wall)
    coll_env.objects.link(podium)
    coll_root.objects.unlink(podium)

    # ---------------------------------------------------------
    # 3. 45 席学生座位阵列矩阵 (5 列 × 9 排)
    # ---------------------------------------------------------
    print("[SimBuilder] 正在阵列布局 45 席学生座位工效学视度矩阵...")
    cols_x = [-2.6, -1.3, 0.0, 1.3, 2.6] # 5 列 (靠窗列 X = -2.6m)
    rows_y = [-2.2 - i * 0.75 for i in range(9)] # 9 排

    def create_seat(col_idx, row_idx, cx, cy):
        # 课桌
        desk_z = z_floor + 0.38 # 中心高 -1.02m
        desk_name = f"Desk_C{col_idx+1}_R{row_idx+1}"
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, desk_z))
        desk = bpy.context.active_object
        desk.name = desk_name
        desk.scale = (0.65, 0.45, 0.76)
        desk.data.materials.append(mat_desk)
        coll_seats.objects.link(desk)
        coll_root.objects.unlink(desk)

        # 椅子
        chair_z = z_floor + 0.22 # 中心高 -1.18m
        chair_name = f"Chair_C{col_idx+1}_R{row_idx+1}"
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy - 0.35, chair_z))
        chair = bpy.context.active_object
        chair.name = chair_name
        chair.scale = (0.42, 0.40, 0.44)
        chair.data.materials.append(mat_chair)
        coll_seats.objects.link(chair)
        coll_root.objects.unlink(chair)

        # 学生眼睛视度标定点 (Z = -0.25m)
        eye_name = f"EyePoint_C{col_idx+1}_R{row_idx+1}"
        eye = bpy.data.objects.new(eye_name, None)
        eye.empty_display_type = 'SPHERE'
        eye.empty_display_size = 0.08
        eye.location = (cx, cy - 0.25, -0.25)
        coll_seats.objects.link(eye)

    for c_i, cx in enumerate(cols_x):
        for r_i, cy in enumerate(rows_y):
            create_seat(c_i, r_i, cx, cy)

    # ---------------------------------------------------------
    # 4. 三维物理光学光线追踪激光束管道
    # ---------------------------------------------------------
    print("[SimBuilder] 正在构建三维光学光线追踪激光束管道...")
    def create_laser_beam(name, p_start, p_end, radius, material):
        v_start = mathutils.Vector(p_start)
        v_end = mathutils.Vector(p_end)
        direction = v_end - v_start
        length = direction.length
        mid_point = (v_start + v_end) / 2.0

        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=length, location=mid_point)
        cyl = bpy.context.active_object
        cyl.name = name

        rot_quat = direction.to_track_quat('Z', 'Y')
        cyl.rotation_mode = 'QUATERNION'
        cyl.rotation_quaternion = rot_quat

        cyl.data.materials.append(material)
        coll_optics.objects.link(cyl)
        coll_root.objects.unlink(cyl)
        return cyl

    sun_source = (-4.0, -3.5, 1.5)           # 侧窗日光射入点
    hit_board = (-1.5, -0.06, 0.0)           # 照射在左侧活动黑板中心
    student_c1_r2_eye = (-2.6, -2.95, -0.25) # 第2排靠窗受害学生眼球位置
    ceiling_safe_target = (0.6, -4.8, 2.15)  # 避光偏航后折射至天花板中央安全区

    create_laser_beam("Optical_Beam_Sun_Incident", sun_source, hit_board, 0.022, mat_beam_sun)
    create_laser_beam("Optical_Beam_Danger_Glared_POV", hit_board, student_c1_r2_eye, 0.025, mat_beam_danger)
    create_laser_beam("Optical_Beam_Safe_Yawed_Ceiling", hit_board, ceiling_safe_target, 0.022, mat_beam_safe)

    # ---------------------------------------------------------
    # 5. 目标跟踪空物体与三机位摄影机矩阵
    # ---------------------------------------------------------
    print("[SimBuilder] 正在布设瞄准目标与三维答辩机位摄影机...")
    # 创建三个注视目标 Empty
    def create_target_empty(name, loc):
        tgt = bpy.data.objects.get(name)
        if not tgt:
            tgt = bpy.data.objects.new(name, None)
            coll_cams.objects.link(tgt)
        tgt.location = loc
        tgt.empty_display_type = 'PLAIN_AXES'
        tgt.empty_display_size = 0.2
        return tgt

    tgt_board_center = create_target_empty("Target_Board_Center", (0.0, 0.0, 0.0))
    tgt_glare_spot = create_target_empty("Target_Glare_Spot", (-1.5, 0.0, 0.0))
    tgt_classroom_center = create_target_empty("Target_Classroom_Center", (0.0, -5.0, -0.6))

    def create_camera_tracked(name, loc, target_obj, lens=35.0):
        cam_data = bpy.data.cameras.new(name=name)
        cam_data.lens = lens
        cam_data.clip_start = 0.1
        cam_data.clip_end = 100.0
        cam_obj = bpy.data.objects.new(name=name, object_data=cam_data)
        cam_obj.location = loc
        coll_cams.objects.link(cam_obj)

        # 添加 Track To 约束，实现精准瞄准
        c = cam_obj.constraints.new(type='TRACK_TO')
        c.target = target_obj
        c.track_axis = 'TRACK_NEGATIVE_Z'
        c.up_axis = 'UP_Y'
        return cam_obj

    # 机位 1: 教室后方全景鸟瞰摄影机 (Overview)
    cam_overview = create_camera_tracked(
        "Camera_Classroom_Overview",
        loc=(3.8, -9.0, 1.8),
        target_obj=tgt_board_center,
        lens=24.0
    )

    # 机位 2: 靠窗受害学生“小明”第一人称主观视角 (Student POV)
    cam_student_pov = create_camera_tracked(
        "Camera_Student_POV",
        loc=(-2.6, -2.95, -0.25),
        target_obj=tgt_glare_spot,
        lens=40.0
    )

    # 机位 3: 教室前墙天花板多模态感知探头视角 (VLM Perception Sensor)
    cam_vlm = create_camera_tracked(
        "Camera_VLM_Sensor",
        loc=(0.0, -0.4, 2.05),
        target_obj=tgt_classroom_center,
        lens=18.0
    )

    scene.camera = cam_student_pov

    # ---------------------------------------------------------
    # 6. 环境光照与日光
    # ---------------------------------------------------------
    print("[SimBuilder] 正在调校动态自然光照系统...")
    sun_data = bpy.data.lights.new(name="Sun_Natural_Window", type='SUN')
    sun_data.energy = 4.0
    sun_data.color = (1.0, 0.95, 0.88)
    sun_obj = bpy.data.objects.new(name="Sun_Natural_Window", object_data=sun_data)
    sun_obj.location = (-4.5, -3.5, 2.5)
    sun_obj.rotation_mode = 'XYZ'
    sun_obj.rotation_euler = (math.radians(35.0), math.radians(25.0), math.radians(-50.0))
    coll_env.objects.link(sun_obj)

    diffuse_data = bpy.data.lights.new(name="Light_Indoor_Diffused", type='AREA')
    diffuse_data.energy = 450.0
    diffuse_data.size = 6.0
    diffuse_data.color = (0.95, 0.97, 1.0)
    diffuse_obj = bpy.data.objects.new(name="Light_Indoor_Diffused", object_data=diffuse_data)
    diffuse_obj.location = (0.0, -4.8, 2.10)
    coll_env.objects.link(diffuse_obj)

    # ---------------------------------------------------------
    # 7. 保存全新工程文件
    # ---------------------------------------------------------
    print(f"[SimBuilder] 正在保存全新光学仿真工程母本: {output_blend}")
    bpy.ops.wm.save_as_mainfile(filepath=output_blend)
    print(f"[SimBuilder] 构建完毕！成功输出: {output_blend}")

if __name__ == "__main__":
    build_simulation_scene()
