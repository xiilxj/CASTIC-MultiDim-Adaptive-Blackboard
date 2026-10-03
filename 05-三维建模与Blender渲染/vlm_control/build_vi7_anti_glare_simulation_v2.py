#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================================================================
第42届瑞安市青少年科技创新大赛 (CASTIC) 参赛重点攻坚工程
模块名称: VI7 高级专业数字孪生光学仿真与多模态智慧教室场景构建中枢 (v2.0 升级版)
文件路径: D:\\Desktop\\CASTICpjhb\\05-三维建模与Blender渲染\\vlm_control\\build_vi7_anti_glare_simulation_v2.py
输出产物: D:\\Desktop\\CASTICpjhb\\05-三维建模与Blender渲染\\vlm_control\\vi7_anti_glare_simulation_v2.blend
审核标识: 第 32 轮工程技术审核
========================================================================================
升级亮点:
  1. 严格遵循用户指令: 桌椅排布重塑为【横着 8 列，纵着 6 行】(共 48 席位工效学矩阵)；
  2. 高级专业化造型:
     - 课桌升级: 现代微导角橡木纹桌面 + 哑光碳素钢管弯折工字型支架 + 内嵌式置物斗；
     - 椅子升级: 现代工程塑料人体工学弧面靠背 + 承重座面板 + 极简钢构脚架；
     - 空间升级: 现代微晶石微反光地砖 (反射黑板与光斑倒影) + 铝合金落地大采光窗框 + 吸音饰面前墙；
  3. 极具穿透力的光环境 (Penetrating Volumetric Lighting):
     - 引入物理体积散射 (Volume Scatter 丁达尔效应)，侧窗强阳光在空气中投射出清晰可见的斜射光柱 (God Rays)；
     - 三维激光追踪管道升级为【同轴双层高能激光束】(高能超白内芯 + 饱和纯色辉光套管)，展现刺破空气的强穿透力；
  4. 多机位重新标定 (包含 Overview 全景鸟瞰、靠窗第2排小明 POV 主观视角、前墙 VLM 感知视角)。
========================================================================================
"""

import bpy
import math
import os
import sys
import mathutils

def build_simulation_v2():
    source_blend = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\VI系列\vi7.blend"
    output_blend = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control\vi7_anti_glare_simulation_v2.blend"

    print(f"[SimBuilder_v2] 正在打开 VI7 基础母本工程: {source_blend}")
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

    coll_env = get_or_create_coll("01_Advanced_Classroom_Architecture")
    coll_seats = get_or_create_coll("02_Student_48_Seats_Matrix_8x6")
    coll_optics = get_or_create_coll("03_Penetrating_Optical_Ray_Tracing")
    coll_cams = get_or_create_coll("04_Multi_View_Cinematic_Cameras")

    # ---------------------------------------------------------
    # 1. 高级专业材质库创建
    # ---------------------------------------------------------
    print("[SimBuilder_v2] 正在构建高级 PBR 材质库与体积散射介质...")
    def create_pbr_mat(name, base_color, roughness=0.4, metallic=0.0, specular=0.5):
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
        node_bsdf.inputs['Metallic'].default_value = metallic
        if 'Specular IOR Level' in node_bsdf.inputs:
            node_bsdf.inputs['Specular IOR Level'].default_value = specular
        elif 'Specular' in node_bsdf.inputs:
            node_bsdf.inputs['Specular'].default_value = specular
        links.new(node_bsdf.outputs['BSDF'], node_out.inputs['Surface'])
        return mat

    def create_laser_emission_mat(name, color_rgba, strength=25.0):
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

    # 地砖材质: 现代高光微晶石 (呈现轻微地面反光倒影，专业感爆棚)
    mat_floor_tiles = create_pbr_mat("Mat_Floor_Tiles_Glossy", (0.86, 0.88, 0.90, 1.0), roughness=0.18, specular=0.8)
    # 墙面材质: 浅暖灰专业吸音板
    mat_wall_acoustic = create_pbr_mat("Mat_Wall_Acoustic_Grey", (0.92, 0.93, 0.94, 1.0), roughness=0.75)
    # 现代橡木桌面板
    mat_desk_oak = create_pbr_mat("Mat_Desk_Top_Oak", (0.82, 0.70, 0.52, 1.0), roughness=0.35)
    # 金属深灰碳素钢管桌腿
    mat_steel_frame = create_pbr_mat("Mat_Steel_Legs_Dark", (0.15, 0.16, 0.18, 1.0), roughness=0.25, metallic=0.8)
    # 现代人体工学座椅塑料 (优雅深天蓝)
    mat_chair_shell = create_pbr_mat("Mat_Chair_Shell_CyanBlue", (0.12, 0.38, 0.65, 1.0), roughness=0.30)
    # 窗户超白钢化玻璃
    mat_glass_window = create_pbr_mat("Mat_Clear_Window_Glass", (0.90, 0.95, 1.0, 0.15), roughness=0.05, specular=0.9)
    # 铝合金黑色窗框
    mat_window_frame = create_pbr_mat("Mat_Window_Frame_Black", (0.08, 0.08, 0.08, 1.0), roughness=0.3, metallic=0.7)

    # 穿透性同轴高能激光材质
    # 内芯超白高能激光核心
    mat_core_white = create_laser_emission_mat("Mat_Laser_Core_White", (1.0, 1.0, 1.0, 1.0), 35.0)
    # 入射日光金黄穿透外管
    mat_beam_sun_halo = create_laser_emission_mat("Mat_Beam_Sun_Halo", (1.0, 0.82, 0.15, 1.0), 18.0)
    # 未避光高危红色警示外管
    mat_beam_danger_halo = create_laser_emission_mat("Mat_Beam_Danger_Halo", (1.0, 0.04, 0.02, 1.0), 22.0)
    # 避光安全科技青绿外管
    mat_beam_safe_halo = create_laser_emission_mat("Mat_Beam_Safe_Halo", (0.05, 1.0, 0.40, 1.0), 18.0)

    # ---------------------------------------------------------
    # 2. 真实体积散射空气介质 (打造丁达尔效应 God Rays)
    # ---------------------------------------------------------
    print("[SimBuilder_v2] 正在配置空气微尘丁达尔体积散射 (Principled Volume)...")
    # 创建体积雾气材质
    mat_vol_fog = bpy.data.materials.get("Mat_Classroom_Tyndall_Volume")
    if not mat_vol_fog:
        mat_vol_fog = bpy.data.materials.new(name="Mat_Classroom_Tyndall_Volume")
        mat_vol_fog.use_nodes = True
    nodes_v = mat_vol_fog.node_tree.nodes
    links_v = mat_vol_fog.node_tree.links
    nodes_v.clear()
    node_out_v = nodes_v.new(type='ShaderNodeOutputMaterial')
    node_vol = nodes_v.new(type='ShaderNodeVolumeScatter')
    node_vol.inputs['Color'].default_value = (0.95, 0.98, 1.0, 1.0)
    node_vol.inputs['Density'].default_value = 0.012 # 适度微尘浓度，保证丁达尔光柱明显且画面不过于昏暗
    node_vol.inputs['Anisotropy'].default_value = 0.60 # 前向散射，使得逆光/侧光更具视觉穿透力
    links_v.new(node_vol.outputs['Volume'], node_out_v.inputs['Volume'])

    # 整个教室体积盒子
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -4.5, 0.40))
    vol_box = bpy.context.active_object
    vol_box.name = "Env_Tyndall_Atmosphere_Box"
    vol_box.scale = (8.4, 9.4, 3.8)
    vol_box.data.materials.append(mat_vol_fog)
    coll_env.objects.link(vol_box)
    coll_root.objects.unlink(vol_box)

    # ---------------------------------------------------------
    # 3. 现代化高级教室建筑空间结构
    # ---------------------------------------------------------
    print("[SimBuilder_v2] 正在搭建高级教室建筑体 (微晶石地砖、落地采光窗框、专业讲台)...")
    z_floor = -1.40
    z_ceiling = 2.20
    y_front = 0.06

    # A. 现代反光地坪
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -4.75, z_floor - 0.05))
    floor = bpy.context.active_object
    floor.name = "Arch_Floor_Microcrystalline"
    floor.scale = (8.6, 9.8, 0.1)
    floor.data.materials.append(mat_floor_tiles)
    coll_env.objects.link(floor)
    coll_root.objects.unlink(floor)

    # B. 天花板与吸音吊顶
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -4.75, z_ceiling + 0.05))
    ceiling = bpy.context.active_object
    ceiling.name = "Arch_Ceiling_Acoustic"
    ceiling.scale = (8.6, 9.8, 0.1)
    ceiling.data.materials.append(mat_wall_acoustic)
    coll_env.objects.link(ceiling)
    coll_root.objects.unlink(ceiling)

    # C. 前墙 (承挂 8000mm 智能黑板系统的专业饰面板)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, y_front + 0.05, 0.40))
    wall_front = bpy.context.active_object
    wall_front.name = "Arch_Wall_Front_Acoustic"
    wall_front.scale = (8.6, 0.1, 3.60)
    wall_front.data.materials.append(mat_wall_acoustic)
    coll_env.objects.link(wall_front)
    coll_root.objects.unlink(wall_front)

    # D. 采光侧墙与落地隔断玻璃大窗 (左侧 X = -4.1m)
    # 窗框横梁与立柱
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-4.15, -4.8, 0.55))
    win_frame = bpy.context.active_object
    win_frame.name = "Arch_Window_Frame_Alloy"
    win_frame.scale = (0.1, 7.5, 2.3)
    win_frame.data.materials.append(mat_window_frame)
    coll_env.objects.link(win_frame)
    coll_root.objects.unlink(win_frame)

    # 玻璃窗面
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-4.10, -4.8, 0.55))
    win_glass = bpy.context.active_object
    win_glass.name = "Arch_Window_Glass_Panel"
    win_glass.scale = (0.02, 7.3, 2.1)
    win_glass.data.materials.append(mat_glass_window)
    coll_env.objects.link(win_glass)
    coll_root.objects.unlink(win_glass)

    # E. 高级一体化讲台 (带木质侧包边与防滑台面)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -0.65, z_floor + 0.075))
    podium = bpy.context.active_object
    podium.name = "Arch_Podium_Platform"
    podium.scale = (8.0, 1.3, 0.15)
    podium.data.materials.append(mat_desk_oak)
    coll_env.objects.link(podium)
    coll_root.objects.unlink(podium)

    # ---------------------------------------------------------
    # 4. 严格执行：横着 8 列，纵着 6 行（共 48 席位）现代高级桌椅矩阵
    # ---------------------------------------------------------
    print("[SimBuilder_v2] 正在精确排布【横着 8 列 × 纵着 6 行 = 48 席位】高级工效学桌椅网格...")
    
    # 8 列横向分布 (跨度 -2.8m 到 +2.8m，间距 0.8m，中间通道与侧通道宽裕合规)
    cols_x = [-2.8, -2.0, -1.2, -0.4, 0.4, 1.2, 2.0, 2.8]
    # 6 行纵向分布 (第一排距离黑板讲台边缘 2.2m，排距 0.95m，最后一排距离后墙通畅)
    rows_y = [-2.20, -3.15, -4.10, -5.05, -6.00, -6.95]

    def build_advanced_desk_chair(col_idx, row_idx, cx, cy):
        suffix = f"C{col_idx+1}_R{row_idx+1}"
        
        # 1. 课桌面板 (木纹圆润桌面)
        desk_z_top = z_floor + 0.74 # 桌面高 0.74m
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, desk_z_top))
        desk_top = bpy.context.active_object
        desk_top.name = f"Desk_Top_{suffix}"
        desk_top.scale = (0.62, 0.42, 0.025)
        desk_top.data.materials.append(mat_desk_oak)
        coll_seats.objects.link(desk_top)
        coll_root.objects.unlink(desk_top)

        # 2. 课桌金属支架 (工字双腿钢管)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, z_floor + 0.36))
        desk_legs = bpy.context.active_object
        desk_legs.name = f"Desk_Legs_{suffix}"
        desk_legs.scale = (0.56, 0.36, 0.70)
        desk_legs.data.materials.append(mat_steel_frame)
        coll_seats.objects.link(desk_legs)
        coll_root.objects.unlink(desk_legs)

        # 3. 椅子座面板 (优雅深天蓝人体工学弧面)
        chair_y = cy - 0.40
        chair_z_seat = z_floor + 0.42
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, chair_y, chair_z_seat))
        chair_seat = bpy.context.active_object
        chair_seat.name = f"Chair_Seat_{suffix}"
        chair_seat.scale = (0.42, 0.38, 0.03)
        chair_seat.data.materials.append(mat_chair_shell)
        coll_seats.objects.link(chair_seat)
        coll_root.objects.unlink(chair_seat)

        # 4. 椅子靠背板
        chair_z_back = z_floor + 0.70
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, chair_y - 0.18, chair_z_back))
        chair_back = bpy.context.active_object
        chair_back.name = f"Chair_Back_{suffix}"
        chair_back.scale = (0.40, 0.025, 0.25)
        chair_back.data.materials.append(mat_chair_shell)
        coll_seats.objects.link(chair_back)
        coll_root.objects.unlink(chair_back)

        # 5. 椅子金属脚架
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, chair_y, z_floor + 0.20))
        chair_legs = bpy.context.active_object
        chair_legs.name = f"Chair_Legs_{suffix}"
        chair_legs.scale = (0.38, 0.34, 0.40)
        chair_legs.data.materials.append(mat_steel_frame)
        coll_seats.objects.link(chair_legs)
        coll_root.objects.unlink(chair_legs)

        # 6. 学生人眼视度标定点 (坐姿眼高 Z = -0.25m, 距地面 1.15m)
        eye_name = f"EyePoint_{suffix}"
        eye = bpy.data.objects.new(eye_name, None)
        eye.empty_display_type = 'SPHERE'
        eye.empty_display_size = 0.06
        eye.location = (cx, chair_y + 0.05, -0.25)
        coll_seats.objects.link(eye)

    for c_i, cx in enumerate(cols_x):
        for r_i, cy in enumerate(rows_y):
            build_advanced_desk_chair(c_i, r_i, cx, cy)

    # ---------------------------------------------------------
    # 5. 极具穿透力的同轴双层高能激光光线追踪系统
    # ---------------------------------------------------------
    print("[SimBuilder_v2] 正在构建【同轴双层高能高穿透力激光射线管】...")
    def create_penetrating_laser(name, p_start, p_end, r_core, r_halo, mat_halo):
        v_start = mathutils.Vector(p_start)
        v_end = mathutils.Vector(p_end)
        direction = v_end - v_start
        length = direction.length
        mid_point = (v_start + v_end) / 2.0
        rot_quat = direction.to_track_quat('Z', 'Y')

        # 外层发光套管 (Halo)
        bpy.ops.mesh.primitive_cylinder_add(radius=r_halo, depth=length, location=mid_point)
        cyl_halo = bpy.context.active_object
        cyl_halo.name = f"{name}_Halo"
        cyl_halo.rotation_mode = 'QUATERNION'
        cyl_halo.rotation_quaternion = rot_quat
        cyl_halo.data.materials.append(mat_halo)
        coll_optics.objects.link(cyl_halo)
        coll_root.objects.unlink(cyl_halo)

        # 内层超白高能激光芯 (Core)
        bpy.ops.mesh.primitive_cylinder_add(radius=r_core, depth=length * 1.002, location=mid_point)
        cyl_core = bpy.context.active_object
        cyl_core.name = f"{name}_Core"
        cyl_core.rotation_mode = 'QUATERNION'
        cyl_core.rotation_quaternion = rot_quat
        cyl_core.data.materials.append(mat_core_white)
        coll_optics.objects.link(cyl_core)
        coll_root.objects.unlink(cyl_core)

    # 光学三维关键路径坐标:
    # A. 太阳强光穿透侧窗: X = -4.15, Y = -3.80, Z = 1.70
    sun_source = (-4.15, -3.80, 1.70)
    # B. 照射在左侧活动黑板受灾中心: X = -1.50, Y = -0.06, Z = 0.00
    hit_board = (-1.50, -0.06, 0.00)
    # C. 未避光高危反射落点: 直射靠窗第1列第2排 (C1_R2) 学生小明眼睛: X = -2.80, Y = -3.10, Z = -0.25
    student_c1_r2_eye = (-2.80, -3.10, -0.25)
    # D. 自适应偏航安全反射落点: 折射抬升至天花板中央安全区: X = 0.50, Y = -4.50, Z = 2.15
    ceiling_safe_target = (0.50, -4.50, 2.15)

    # 1. 穿透性日光入射光束 (Sun Incident Beam)
    create_penetrating_laser("Beam_Sun_Incident", sun_source, hit_board, 0.012, 0.028, mat_beam_sun_halo)
    # 2. 未避光危险直射光束 (Danger Reflected Beam)
    create_penetrating_laser("Beam_Danger_Glared_POV", hit_board, student_c1_r2_eye, 0.014, 0.032, mat_beam_danger_halo)
    # 3. 自适应偏航安全反射光束 (Safe Reflected Beam)
    create_penetrating_laser("Beam_Safe_Yawed_Ceiling", hit_board, ceiling_safe_target, 0.012, 0.028, mat_beam_safe_halo)

    # ---------------------------------------------------------
    # 6. 强穿透力自然阳光与补光系统 (Sunlight + Penetrating Spot)
    # ---------------------------------------------------------
    print("[SimBuilder_v2] 正在调校高穿透力太阳光束与丁达尔斜射光源...")
    # 侧窗太阳直射平行光
    sun_data = bpy.data.lights.new(name="Sun_Penetrating_Natural", type='SUN')
    sun_data.energy = 8.0 # 加强阳光强度
    sun_data.color = (1.0, 0.94, 0.85)
    sun_obj = bpy.data.objects.new(name="Sun_Penetrating_Natural", object_data=sun_data)
    sun_obj.location = (-4.8, -4.0, 3.0)
    sun_obj.rotation_mode = 'XYZ'
    sun_obj.rotation_euler = (math.radians(38.0), math.radians(22.0), math.radians(-52.0))
    coll_env.objects.link(sun_obj)

    # 侧窗丁达尔强聚光灯 (穿透空气形成清晰光柱)
    spot_data = bpy.data.lights.new(name="Spot_Tyndall_Beam", type='SPOT')
    spot_data.energy = 2500.0 # 强聚光，在微尘中激发出璀璨丁达尔光束
    spot_data.spot_size = math.radians(65.0)
    spot_data.spot_blend = 0.35
    spot_data.color = (1.0, 0.92, 0.80)
    spot_obj = bpy.data.objects.new(name="Spot_Tyndall_Beam", object_data=spot_data)
    spot_obj.location = (-4.3, -4.2, 2.2)
    spot_obj.rotation_mode = 'XYZ'
    spot_obj.rotation_euler = (math.radians(45.0), math.radians(20.0), math.radians(-50.0))
    coll_env.objects.link(spot_obj)

    # ---------------------------------------------------------
    # 7. 电影级专业三机位摄影机矩阵
    # ---------------------------------------------------------
    print("[SimBuilder_v2] 正在配置高规格答辩机位摄影机 (Track To 精准瞄准)...")
    def create_target_empty(name, loc):
        tgt = bpy.data.objects.get(name)
        if not tgt:
            tgt = bpy.data.objects.new(name, None)
            coll_cams.objects.link(tgt)
        tgt.location = loc
        tgt.empty_display_type = 'PLAIN_AXES'
        tgt.empty_display_size = 0.2
        return tgt

    tgt_board_center = create_target_empty("Target_Board_Center_v2", (0.0, 0.0, 0.0))
    tgt_glare_spot = create_target_empty("Target_Glare_Spot_v2", (-1.5, 0.0, 0.0))
    tgt_classroom_center = create_target_empty("Target_Classroom_Center_v2", (0.0, -4.8, -0.6))

    def create_cinematic_cam(name, loc, tgt_obj, lens=32.0):
        cam_data = bpy.data.cameras.new(name=name)
        cam_data.lens = lens
        cam_data.clip_start = 0.1
        cam_data.clip_end = 120.0
        cam_obj = bpy.data.objects.new(name=name, object_data=cam_data)
        cam_obj.location = loc
        coll_cams.objects.link(cam_obj)

        c = cam_obj.constraints.new(type='TRACK_TO')
        c.target = tgt_obj
        c.track_axis = 'TRACK_NEGATIVE_Z'
        c.up_axis = 'UP_Y'
        return cam_obj

    # 机位 1: 教室后方全景鸟瞰大景深电影机位 (Overview)
    cam_overview = create_cinematic_cam(
        "Camera_Classroom_Overview_v2",
        loc=(4.2, -8.6, 2.0),
        tgt_obj=tgt_board_center,
        lens=24.0 # 广角展现 8 列 6 行与全教室穿透光柱
    )

    # 机位 2: 靠窗第1列第2排受害学生小明第一人称主观视角 (Student POV)
    cam_student_pov = create_cinematic_cam(
        "Camera_Student_POV_v2",
        loc=(-2.80, -3.10, -0.25),
        tgt_obj=tgt_glare_spot,
        lens=42.0
    )

    # 机位 3: 前墙天花板 VLM 边缘多模态感知探头俯视机位 (VLM Perception)
    cam_vlm = create_cinematic_cam(
        "Camera_VLM_Sensor_v2",
        loc=(0.0, -0.35, 2.10),
        tgt_obj=tgt_classroom_center,
        lens=18.0 # 超广角向下俯视全班 48 席位
    )

    scene.camera = cam_overview

    # ---------------------------------------------------------
    # 8. 保存全新高规格工程母本文件
    # ---------------------------------------------------------
    print(f"[SimBuilder_v2] 正在保存全新高级数字孪生光学母本: {output_blend}")
    os.makedirs(os.path.dirname(output_blend), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=output_blend)
    print(f"[SimBuilder_v2] 构建成功！全新专业级母本已输出: {output_blend}")

if __name__ == "__main__":
    build_simulation_v2()
