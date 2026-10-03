#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rebuild_gen3_master_assembly_v2_0.py (精修版)
第42届瑞安市青少年科技创新大赛 · 第三代多维智能黑板
Blender 5.0 高精度三维机械重构与全场景 VLM 光环境自适应调控母本系统 (v2.0)

核心精修：
1. 彻底解决父子级矩阵装配偏差：建立严格的 local_parent 拓扑绑定，确保板面严格装入 1200mm 导轨框架内；
2. 还原原始工程原图质感：双 C 导轨铝型材截面、Canopy 倾斜遮光雨棚外檐、86寸大屏内凹沉台、不锈钢套杆与黄铜铰链；
3. 第三代多层对角线正交折叠：内层主绿板 + 外层副白板，折叠向内合拢时两扇白板在 X=0 中心严密锁合（4000mm封屏），向外折叠叠合且侧滑展开至 6000mm；
4. 全教室 VLM 光环境矩阵：侧窗太阳光、可动遮阳百叶卷帘、黑板防眩洗墙条形灯、顶置环境灯；
5. 相机机位采用 35mm 工程广角与 60mm 微距精准构图，画面完美无裁切。
"""

import bpy
import math
import os
import mathutils

def clear_scene():
    """彻底清空当前场景"""
    bpy.ops.wm.read_factory_settings(use_empty=True)

def setup_render_engine():
    """配置渲染引擎与色彩管理"""
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0 # 1 BU = 1 米
    
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 3840
    scene.render.resolution_y = 2160
    scene.render.resolution_percentage = 100
    
    scene.display_settings.display_device = 'sRGB'
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - High Contrast'

def create_pbr_material(name, base_color, metallic=0.0, roughness=0.4, specular=0.5, ior=1.45):
    """创建标准化 PBR 物理材质"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_bsdf.inputs['Base Color'].default_value = base_color
    node_bsdf.inputs['Metallic'].default_value = metallic
    node_bsdf.inputs['Roughness'].default_value = roughness
    if 'Specular IOR Level' in node_bsdf.inputs:
        node_bsdf.inputs['Specular IOR Level'].default_value = specular
    elif 'Specular' in node_bsdf.inputs:
        node_bsdf.inputs['Specular'].default_value = specular
    if 'IOR' in node_bsdf.inputs:
        node_bsdf.inputs['IOR'].default_value = ior
        
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(node_bsdf.outputs['BSDF'], node_output.inputs['Surface'])
    return mat

def create_materials():
    """构建整套物理材质字典"""
    mats = {}
    mats['green_board'] = create_pbr_material("Mat_Enamel_Green", (0.06, 0.18, 0.09, 1.0), metallic=0.0, roughness=0.45, specular=0.2)
    mats['white_board'] = create_pbr_material("Mat_White_Board", (0.92, 0.92, 0.90, 1.0), metallic=0.0, roughness=0.38, specular=0.3)
    mats['ag_screen'] = create_pbr_material("Mat_AG_Screen", (0.012, 0.012, 0.018, 1.0), metallic=0.05, roughness=0.15, specular=0.4, ior=1.52)
    mats['anodized_frame'] = create_pbr_material("Mat_Anodized_Alum", (0.12, 0.12, 0.13, 1.0), metallic=0.88, roughness=0.32, specular=0.6)
    mats['stainless_steel'] = create_pbr_material("Mat_Polished_SUS304", (0.86, 0.86, 0.88, 1.0), metallic=0.98, roughness=0.10, specular=0.9)
    mats['gold_hinge'] = create_pbr_material("Mat_Brass_Hinge", (0.88, 0.65, 0.14, 1.0), metallic=0.92, roughness=0.22, specular=0.8)
    mats['blinds_fabric'] = create_pbr_material("Mat_Blinds_Fabric", (0.78, 0.78, 0.75, 1.0), metallic=0.0, roughness=0.85, specular=0.1)
    mats['classroom_wall'] = create_pbr_material("Mat_Classroom_Wall", (0.85, 0.85, 0.83, 1.0), metallic=0.0, roughness=0.65, specular=0.2)
    mats['classroom_floor'] = create_pbr_material("Mat_Classroom_Floor", (0.42, 0.35, 0.28, 1.0), metallic=0.0, roughness=0.55, specular=0.3)
    return mats

def attach_to_parent(child, parent, local_loc=(0,0,0), local_rot=(0,0,0)):
    """严密的父子级装配函数，重置逆矩阵以保证局部空间绝对正确"""
    child.parent = parent
    child.matrix_parent_inverse.identity()
    child.location = local_loc
    child.rotation_euler = local_rot

def build_classroom_context(mats):
    """构建真实的教室墙面、侧窗与天花板光环境物理上下文"""
    # 1. 前景黑板挂载主墙面 (X: -5 ~ +5m, Z: 0 ~ 3.8m, Y: -0.06m)
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, -0.06, 1.8), rotation=(math.radians(90), 0, 0))
    wall = bpy.context.active_object
    wall.name = "Classroom_Front_Wall"
    wall.scale = (10.0, 3.8, 1.0)
    wall.data.materials.append(mats['classroom_wall'])
    
    # 2. 地面 (X: -5 ~ +5m, Y: 0 ~ 8m, Z: 0)
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, 4.0, 0), rotation=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "Classroom_Floor"
    floor.scale = (10.0, 8.0, 1.0)
    floor.data.materials.append(mats['classroom_floor'])

    # 3. 左侧采光窗户结构 (X: -4.8m, Y: 1.0 ~ 6.0m, Z: 1.0 ~ 3.2m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-4.8, 3.5, 2.1))
    window_frame = bpy.context.active_object
    window_frame.name = "Window_Wall_Side"
    window_frame.scale = (0.1, 4.5, 2.2)
    window_frame.data.materials.append(mats['anodized_frame'])

def build_smart_lighting_and_blinds(mats):
    """构建由 VLM 动态控制的全套教室光环境与遮阳系统"""
    # 1. 侧窗直射太阳光源 (斜射黑板产生眩光)
    light_data_sun = bpy.data.lights.new(name="Sun_Window_Data", type='SUN')
    light_data_sun.energy = 4.2
    light_data_sun.color = (1.0, 0.96, 0.90)
    sun_obj = bpy.data.objects.new("VLM_Controlled_Sun", light_data_sun)
    bpy.context.collection.objects.link(sun_obj)
    sun_obj.location = (-7.0, 4.0, 4.5)
    sun_obj.rotation_euler = (math.radians(-32), math.radians(40), math.radians(-65))

    # 2. 电动遮阳卷帘系统 (Smart Blinds)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-4.72, 3.5, 3.1))
    blinds_box = bpy.context.active_object
    blinds_box.name = "Smart_Blinds_Header"
    blinds_box.scale = (0.10, 4.3, 0.14)
    blinds_box.data.materials.append(mats['anodized_frame'])

    # 卷帘帘布
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(-4.70, 3.5, 2.1), rotation=(0, math.radians(90), 0))
    blinds_fabric = bpy.context.active_object
    blinds_fabric.name = "Smart_Blinds_Fabric"
    blinds_fabric.scale = (2.0, 4.2, 1.0)
    blinds_fabric.data.materials.append(mats['blinds_fabric'])

    # 3. 顶部黑板专用无眩光漫反射条形洗墙灯 (Wash Lighting for Blackboard)
    light_board_data = bpy.data.lights.new(name="Light_Board_Wash_Data", type='AREA')
    light_board_data.energy = 200.0
    light_board_data.color = (0.96, 0.98, 1.0)
    light_board_data.shape = 'RECTANGLE'
    light_board_data.size = 4.0
    light_board_data.size_y = 0.20
    light_board_obj = bpy.data.objects.new("VLM_Controlled_BoardLight", light_board_data)
    bpy.context.collection.objects.link(light_board_obj)
    light_board_obj.location = (0.0, 0.50, 2.45)
    light_board_obj.rotation_euler = (math.radians(-28), 0, 0)

    # 4. 后排学生区域环境照明灯
    light_room_data = bpy.data.lights.new(name="Light_Classroom_Ambient_Data", type='AREA')
    light_room_data.energy = 160.0
    light_room_data.color = (1.0, 1.0, 1.0)
    light_room_data.shape = 'SQUARE'
    light_room_data.size = 2.5
    light_room_obj = bpy.data.objects.new("VLM_Controlled_AmbientLight", light_room_data)
    bpy.context.collection.objects.link(light_room_obj)
    light_room_obj.location = (0.0, 4.2, 3.4)

def build_main_frame_and_screen(mats):
    """构建复刻原始质感的主外框、Canopy遮光雨棚、排砂滑轨与86寸大屏沉台"""
    # 1. 顶部 Canopy 遮光雨棚与上滑轨 (Z: 2.10 ~ 2.22m, 前挑 140mm)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.07, 2.16))
    canopy_top = bpy.context.active_object
    canopy_top.name = "Canopy_Top_Assembly"
    canopy_top.scale = (4.06, 0.16, 0.10)
    canopy_top.data.materials.append(mats['anodized_frame'])

    # 遮光倾斜护檐板 (向下倾斜 15°)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.14, 2.18), rotation=(math.radians(15), 0, 0))
    visor_top = bpy.context.active_object
    visor_top.name = "Canopy_Light_Visor"
    visor_top.scale = (4.06, 0.08, 0.02)
    visor_top.data.materials.append(mats['anodized_frame'])

    # 2. 底部排灰槽与集尘导轨梁 (Z: 0.82 ~ 0.90m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.05, 0.86))
    tray_bottom = bpy.context.active_object
    tray_bottom.name = "Dust_Tray_Bottom"
    tray_bottom.scale = (4.06, 0.14, 0.08)
    tray_bottom.data.materials.append(mats['anodized_frame'])

    # 3. 左右垂直立柱端盖 (高 1300mm, 宽 60mm, 厚 120mm)
    for sign, name in [(-1, "Outer_Pillar_L"), (1, "Outer_Pillar_R")]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(sign * 2.01, 0.05, 1.51))
        pillar = bpy.context.active_object
        pillar.name = name
        pillar.scale = (0.06, 0.12, 1.30)
        pillar.data.materials.append(mats['anodized_frame'])

    # 4. 中置 86寸 纳米微晶 AG 大屏沉台 (宽 2000mm × 高 1200mm, Z中心 1.51m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.015, 1.51))
    screen_bezel = bpy.context.active_object
    screen_bezel.name = "Screen_Bezel_86Inch"
    screen_bezel.scale = (2.02, 0.03, 1.22)
    screen_bezel.data.materials.append(mats['anodized_frame'])

    # 纳米微晶高平整度显示屏面板
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.028, 1.51))
    screen_glass = bpy.context.active_object
    screen_glass.name = "Screen_AG_Glass"
    screen_glass.scale = (1.92, 0.012, 1.08)
    screen_glass.data.materials.append(mats['ag_screen'])

    # 5. 左右底层固定书写黑板 (X=±1500mm, 宽 1000mm × 高 1200mm)
    for sign, name in [(-1, "Fixed_Base_Board_L"), (1, "Fixed_Base_Board_R")]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(sign * 1.50, 0.015, 1.51))
        board = bpy.context.active_object
        board.name = name
        board.scale = (0.98, 0.02, 1.18)
        board.data.materials.append(mats['green_board'])

def build_rigged_telescopic_and_folding_mechanism(mats):
    """构建核心机构：空物体层级约束、双横梁套杆、对角线双铰链与双层板面"""
    root_ctrl = bpy.data.objects.new("MASTER_RIG_ROOT", None)
    root_ctrl.empty_display_type = 'SPHERE'
    root_ctrl.location = (0, 0, 0)
    bpy.context.collection.objects.link(root_ctrl)

    sides = [
        {"side": "L", "sign": -1, "base_x": -1.50},
        {"side": "R", "sign":  1, "base_x":  1.50}
    ]

    controllers = {}

    for item in sides:
        s = item["side"]
        sgn = item["sign"]

        # -------------------------------------------------------------
        # 1. 侧滑滑块控制器 (Slide Controller, 基准挂在全局 base_x, 0.08, 1.51)
        # -------------------------------------------------------------
        ctrl_slide = bpy.data.objects.new(f"Ctrl_Slide_{s}", None)
        ctrl_slide.empty_display_type = 'ARROWS'
        ctrl_slide.location = (item["base_x"], 0.08, 1.51)
        ctrl_slide.parent = root_ctrl
        ctrl_slide.matrix_parent_inverse.identity()
        bpy.context.collection.objects.link(ctrl_slide)
        controllers[f"slide_{s}"] = ctrl_slide

        # 限位约束 (在 LOCAL 空间滑动 0 ~ sgn*1.0m)
        const_s = ctrl_slide.constraints.new(type='LIMIT_LOCATION')
        const_s.owner_space = 'LOCAL'
        const_s.use_min_x = True; const_s.use_max_x = True
        if sgn < 0:
            const_s.min_x = -1.0; const_s.max_x = 0.0
        else:
            const_s.min_x = 0.0; const_s.max_x = 1.0
        const_s.use_min_y = True; const_s.max_y = 0.0; const_s.min_y = 0.0
        const_s.use_min_z = True; const_s.max_z = 0.0; const_s.min_z = 0.0

        # 双横梁不锈钢伸缩套杆 (上下各一根，在局部坐标系中)
        for z_off in [0.58, -0.58]: # 对应全局 Z: 2.09m 与 0.93m
            bpy.ops.mesh.primitive_cylinder_add(radius=0.016, depth=1.15, rotation=(0, math.radians(90), 0))
            rod = bpy.context.active_object
            rod.name = f"Telescopic_Rod_{s}_{'Top' if z_off>0 else 'Btm'}"
            attach_to_parent(rod, ctrl_slide, local_loc=(0, 0, z_off))
            rod.data.materials.append(mats['stainless_steel'])

        # 端部垂直拉杆 (外侧连接上下套杆)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=1.16)
        tie_rod = bpy.context.active_object
        tie_rod.name = f"Vertical_Tie_Rod_{s}"
        attach_to_parent(tie_rod, ctrl_slide, local_loc=(sgn * 0.49, 0, 0))
        tie_rod.data.materials.append(mats['stainless_steel'])

        # -------------------------------------------------------------
        # 2. 对角线外侧翻转铰链 (Yaw Hinge, 位于外侧端 sgn * 0.48)
        # -------------------------------------------------------------
        ctrl_yaw = bpy.data.objects.new(f"Ctrl_Yaw_{s}", None)
        ctrl_yaw.empty_display_type = 'SINGLE_ARROW'
        ctrl_yaw.parent = ctrl_slide
        ctrl_yaw.matrix_parent_inverse.identity()
        ctrl_yaw.location = (sgn * 0.48, 0.02, 0.0)
        bpy.context.collection.objects.link(ctrl_yaw)
        controllers[f"yaw_{s}"] = ctrl_yaw

        const_y = ctrl_yaw.constraints.new(type='LIMIT_ROTATION')
        const_y.owner_space = 'LOCAL'
        const_y.use_limit_x = True; const_y.min_x = 0; const_y.max_x = 0
        const_y.use_limit_y = True; const_y.min_y = 0; const_y.max_y = 0
        const_y.use_limit_z = True
        const_y.min_z = math.radians(-15.0)
        const_y.max_z = math.radians(15.0)

        # 外侧翻转铰链真实五金座 (上下两组)
        for h_z in [0.42, -0.42]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.016, depth=0.10)
            h_obj = bpy.context.active_object
            h_obj.name = f"Hinge_Pivot_Yaw_{s}_{'Top' if h_z>0 else 'Btm'}"
            attach_to_parent(h_obj, ctrl_slide, local_loc=(sgn * 0.48, 0.02, h_z))
            h_obj.data.materials.append(mats['gold_hinge'])

        # -------------------------------------------------------------
        # 3. 内侧主活动绿板 (Inner Board - Enamel Green)
        # -------------------------------------------------------------
        # 板长 0.98m，高 1.18m，厚 0.022m。向内伸展，中心距铰链 -sgn * 0.49m
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        inner_board = bpy.context.active_object
        inner_board.name = f"Inner_Green_Board_{s}"
        inner_board.scale = (0.98, 0.022, 1.18)
        attach_to_parent(inner_board, ctrl_yaw, local_loc=(-sgn * 0.49, 0.0, 0.0))
        inner_board.data.materials.append(mats['green_board'])

        # 铝合金外包边
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        inner_rim = bpy.context.active_object
        inner_rim.name = f"Inner_Board_Rim_{s}"
        inner_rim.scale = (1.00, 0.024, 1.20)
        attach_to_parent(inner_rim, inner_board, local_loc=(0, 0, 0))
        inner_rim.data.materials.append(mats['anodized_frame'])

        # -------------------------------------------------------------
        # 4. 对角线内侧折叠铰链 (Fold Hinge, 位于绿板内侧端)
        # -------------------------------------------------------------
        # 距偏航铰链 -sgn * 0.98m，Y 向前偏移 0.025m
        ctrl_fold = bpy.data.objects.new(f"Ctrl_Fold_{s}", None)
        ctrl_fold.empty_display_type = 'SINGLE_ARROW'
        ctrl_fold.parent = ctrl_yaw
        ctrl_fold.matrix_parent_inverse.identity()
        ctrl_fold.location = (-sgn * 0.98, 0.026, 0.0)
        bpy.context.collection.objects.link(ctrl_fold)
        controllers[f"fold_{s}"] = ctrl_fold

        const_f = ctrl_fold.constraints.new(type='LIMIT_ROTATION')
        const_f.owner_space = 'LOCAL'
        const_f.use_limit_x = True; const_f.min_x = 0; const_f.max_x = 0
        const_f.use_limit_y = True; const_f.min_y = 0; const_f.max_y = 0
        const_f.use_limit_z = True
        if sgn < 0:
            const_f.min_z = 0.0; const_f.max_z = math.radians(180.0)
        else:
            const_f.min_z = math.radians(-180.0); const_f.max_z = 0.0

        # 内侧铰链五金轴销
        for f_z in [0.42, -0.42]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.014, depth=0.09)
            f_obj = bpy.context.active_object
            f_obj.name = f"Hinge_Pivot_Fold_{s}_{'Top' if f_z>0 else 'Btm'}"
            attach_to_parent(f_obj, ctrl_yaw, local_loc=(-sgn * 0.98, 0.026, f_z))
            f_obj.data.materials.append(mats['gold_hinge'])

        # -------------------------------------------------------------
        # 5. 外侧折叠副白板 (Outer Fold Whiteboard - 象牙白)
        # -------------------------------------------------------------
        # 当 Fold=0° 时贴合在绿板正面，中心向外偏移 sgn * 0.49m；
        # 当 Fold=180° 时向内铺开，中心向内偏移 -sgn * 0.49m，覆盖到中心 X=0！
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        outer_board = bpy.context.active_object
        outer_board.name = f"Outer_Fold_Whiteboard_{s}"
        outer_board.scale = (0.97, 0.016, 1.17)
        attach_to_parent(outer_board, ctrl_fold, local_loc=(sgn * 0.49, 0.018, 0.0))
        outer_board.data.materials.append(mats['white_board'])

        # 外侧副板包边
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        outer_rim = bpy.context.active_object
        outer_rim.name = f"Outer_Board_Rim_{s}"
        outer_rim.scale = (0.99, 0.018, 1.19)
        attach_to_parent(outer_rim, outer_board, local_loc=(0, 0, 0))
        outer_rim.data.materials.append(mats['anodized_frame'])

    return controllers

def setup_camera(target_loc, cam_loc, focal_length=35.0):
    """设置透视观察相机并自动精确瞄准"""
    cam_data = bpy.data.cameras.new(name="Render_Camera_Data")
    cam_data.lens = focal_length
    cam_data.clip_start = 0.1
    cam_data.clip_end = 100.0
    cam_obj = bpy.data.objects.new("Master_Render_Camera", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    
    cam_obj.location = cam_loc
    direction = mathutils.Vector(target_loc) - mathutils.Vector(cam_loc)
    rot_quat = direction.to_track_quat('-Z', 'Y')
    cam_obj.rotation_euler = rot_quat.to_euler()
    bpy.context.scene.camera = cam_obj
    return cam_obj

def apply_vlm_action(controllers, yaw_l=0.0, yaw_r=0.0, slide_l=0.0, slide_r=0.0, fold_l=0.0, fold_r=0.0):
    """对外暴露的 VLM 决策驱动接口：毫秒级驱动各机构空物体姿态"""
    if "slide_L" in controllers:
        controllers["slide_L"].location.x = slide_l
    if "slide_R" in controllers:
        controllers["slide_R"].location.x = slide_r
    if "yaw_L" in controllers:
        controllers["yaw_L"].rotation_euler.z = math.radians(yaw_l)
    if "yaw_R" in controllers:
        controllers["yaw_R"].rotation_euler.z = math.radians(yaw_r)
    if "fold_L" in controllers:
        controllers["fold_L"].rotation_euler.z = math.radians(fold_l)
    if "fold_R" in controllers:
        controllers["fold_R"].rotation_euler.z = math.radians(fold_r)
    bpy.context.view_layer.update()

def main():
    print("[1/5] 清空场景并配置环境...")
    clear_scene()
    setup_render_engine()
    
    print("[2/5] 编译高级 PBR 物理光学材质系统...")
    mats = create_materials()

    print("[3/5] 构建教室光环境上下文与智能灯光遮阳系统...")
    build_classroom_context(mats)
    build_smart_lighting_and_blinds(mats)

    print("[4/5] 重构主承重外框、Canopy遮光雨棚、86寸大屏与对角线铰链总成...")
    build_main_frame_and_screen(mats)
    controllers = build_rigged_telescopic_and_folding_mechanism(mats)

    output_dir = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染"
    os.makedirs(output_dir, exist_ok=True)
    blend_path = os.path.join(output_dir, "第三代多维叠合翻转智能黑板系统_三维机构总装与动力学模型_v2.0.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"--> 模型母本工程已保存: {blend_path}")

    # -------------------------------------------------------------
    # 多工况渲染出图
    # -------------------------------------------------------------
    print("[5/5] 执行五大工况 4K 超清物理渲染...")

    # 相机机位 1：标准正面工程全景视角 (35mm 广角，距离 5.6m，完美容纳全机与雨棚)
    cam = setup_camera(target_loc=(0.0, 0.08, 1.51), cam_loc=(0.0, 5.6, 1.62), focal_length=35.0)

    # 工况一：全覆盖封屏形态 (整机4000mm，副板向内展180°在中央X=0严密锁合闭合，彻底封屏)
    apply_vlm_action(controllers, yaw_l=0, yaw_r=0, slide_l=0, slide_r=0, fold_l=180, fold_r=-180)
    bpy.context.scene.render.filepath = os.path.join(output_dir, "01_工况一_全覆盖封屏与漫反射光场形态_v2.0_4K.png")
    bpy.ops.render.render(write_still=True)
    print("--> 工况一渲染完成")

    # 工况二：常态大屏露显双层叠合形态 (整机4000mm，副板折叠贴合在绿板前方，中央86寸大屏全露)
    apply_vlm_action(controllers, yaw_l=0, yaw_r=0, slide_l=0, slide_r=0, fold_l=0, fold_r=0)
    bpy.context.scene.render.filepath = os.path.join(output_dir, "02_工况二_常态大屏露显与侧窗漫射形态_v2.0_4K.png")
    bpy.ops.render.render(write_still=True)
    print("--> 工况二渲染完成")

    # 工况三：平移侧滑极限展开与自适应避光光场重塑形态 (外滑1000mm，整机6000mm，偏航14°避光)
    apply_vlm_action(controllers, yaw_l=14, yaw_r=-14, slide_l=-1.0, slide_r=1.0, fold_l=0, fold_r=0)
    bpy.context.scene.render.filepath = os.path.join(output_dir, "03_工况三_平移侧滑极限展开与自适应避光光场重塑形态_v2.0_4K.png")
    bpy.ops.render.render(write_still=True)
    print("--> 工况三渲染完成")

    # 工况四：右侧端部微距特写 (聚焦对角线双铰链、双横梁套杆与两层折叠板间隙)
    cam.location = (2.35, 2.20, 1.70)
    cam.data.lens = 55.0
    direction = mathutils.Vector((1.50, 0.08, 1.51)) - mathutils.Vector((2.35, 2.20, 1.70))
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.render.filepath = os.path.join(output_dir, "04_对角线双铰链与双横梁伸缩套杆三维立体机构微距特写_v2.0_4K.png")
    bpy.ops.render.render(write_still=True)
    print("--> 工况四特写渲染完成")

    # 工况五：全教室智能光环境矩阵与VLM动态控光全景 (大景深广角展示侧窗阳光、遮阳帘、防眩洗墙灯与黑板)
    cam.location = (-4.0, 5.8, 2.8)
    cam.data.lens = 30.0
    direction = mathutils.Vector((0.0, 0.08, 1.51)) - mathutils.Vector((-4.0, 5.8, 2.8))
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.render.filepath = os.path.join(output_dir, "05_全教室智能光环境矩阵与VLM动态控光中枢全景_v2.0_4K.png")
    bpy.ops.render.render(write_still=True)
    print("--> 工况五全景渲染完成")

    print("==========================================")
    print("精修版高精模型与五大工况 4K 渲染出图全部就绪！")
    print("==========================================")

if __name__ == "__main__":
    main()
