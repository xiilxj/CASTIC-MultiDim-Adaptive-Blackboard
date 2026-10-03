#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
第三代（Z系列）多维叠合翻转全覆盖与三维自洁侧滑智能教学黑板系统
Blender 3D 参数化建模与动力学运动总装母本脚本 (Z-Series Master Assembly)
=============================================================================
- 工程版本: GuangHeng-Gen3 (GH-Z-2026) v1.0
- 规范依据: 《第三代全系统设计规格与技术参数数据集 v1.2 (对角线双铰链终极版)》
- 核心机构学实现:
  1. 双层贴合黑板扇叶: 内层主板(12mm) + 外层折叠板(12mm) + 2mm磁吸阻尼间隙 = 26mm 总叠合厚度
  2. 对角线双铰链空间正交解耦拓扑:
     - 里面的外侧 (X=±2000mm, Y=内): 偏航(Yaw)与纵向俯仰(Pitch -15°~+15°)主铰链
     - 外面的内侧 (X=±1000mm, Y=外): 0°~180° 向中回转折叠封屏(Fold)铰链
  3. 双横梁自洁排灰滑轨 + Φ28mm SUS304 高刚度伸缩套杆 + 工程高亮橙色刚性垂直端部拉杆
  4. 86寸超窄边框 4K 微晶防眩显示屏沉台 + 水平平直遮阳挑檐 (0° 平檐，彻底杜绝乱翘)
  5. 采样物理色彩标定: 大屏#5182aa, 墨绿黑板#416951, 视口背景#3a3a3a, 边框拉丝银#c7c8ca
  6. 三大标准工况自动生成与 4K 高保真物理渲染
=============================================================================
"""

import bpy
import math
import os
import sys

def reset_scene():
    """彻底重置并清理 Blender 场景"""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for c in list(bpy.data.collections):
        bpy.data.collections.remove(c)
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for mesh in list(bpy.data.meshes):
        bpy.data.meshes.remove(mesh)
    for mat in list(bpy.data.materials):
        bpy.data.materials.remove(mat)
    for light in list(bpy.data.lights):
        bpy.data.lights.remove(light)
    for cam in list(bpy.data.cameras):
        bpy.data.cameras.remove(cam)

def setup_render_engine():
    """配置 Cycles 物理渲染器与色彩管理 (严密匹配 17 号原版色彩基底)"""
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    
    # 尝试启用 GPU 加速
    try:
        cycles_prefs = bpy.context.preferences.addons['cycles'].preferences
        cycles_prefs.compute_device_type = 'OPTIX'
        for d in cycles_prefs.devices:
            d.use = True
        scene.cycles.device = 'GPU'
    except Exception:
        try:
            cycles_prefs = bpy.context.preferences.addons['cycles'].preferences
            cycles_prefs.compute_device_type = 'CUDA'
            for d in cycles_prefs.devices:
                d.use = True
            scene.cycles.device = 'GPU'
        except Exception:
            scene.cycles.device = 'CPU'
            
    scene.cycles.samples = 128
    scene.cycles.preview_samples = 32
    scene.cycles.use_denoising = True
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'None'
    scene.view_settings.exposure = 0.0
    scene.view_settings.gamma = 1.0
    
    # 视口深灰背景 (严格标定 sRGB [58, 58, 58] -> #3a3a3a)
    world = bpy.data.worlds.new("Z_Series_World")
    scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs['Color'].default_value = (0.038, 0.038, 0.038, 1.0)
        bg_node.inputs['Strength'].default_value = 1.0

def create_pbr_material(name, base_color, metallic=0.0, roughness=0.5, specular=0.5):
    """创建标准 PBR 材质辅助函数"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = base_color
        if 'Metallic' in bsdf.inputs:
            bsdf.inputs['Metallic'].default_value = metallic
        if 'Roughness' in bsdf.inputs:
            bsdf.inputs['Roughness'].default_value = roughness
        if 'Specular IOR Level' in bsdf.inputs:
            bsdf.inputs['Specular IOR Level'].default_value = specular
        elif 'Specular' in bsdf.inputs:
            bsdf.inputs['Specular'].default_value = specular
    return mat

def build_calibrated_materials():
    """建立经由 17 号参考图采样像素级标定的物理材质库"""
    materials = {}
    
    # 1. 墨绿黑板搪瓷书写板面 (严格标定 sRGB [65, 105, 81] -> #416951)
    materials['blackboard_green'] = create_pbr_material(
        name="Mat_Z_Blackboard_Green",
        base_color=(0.052, 0.145, 0.085, 1.0),
        metallic=0.0,
        roughness=0.55,
        specular=0.25
    )
    
    # 2. 6063-T5 阳极氧化铝合金拉丝包边 (微弱金属光泽与反射)
    materials['aluminum_bezel'] = create_pbr_material(
        name="Mat_Z_Aluminum_Bezel",
        base_color=(0.72, 0.73, 0.74, 1.0),
        metallic=0.96,
        roughness=0.16,
        specular=0.98
    )
    
    # 3. 镀铬镜面小圆钮手柄
    materials['chrome_handle'] = create_pbr_material(
        name="Mat_Z_Chrome_Handle",
        base_color=(0.95, 0.95, 0.98, 1.0),
        metallic=1.0,
        roughness=0.08,
        specular=1.0
    )
    
    # 4. 86寸微晶防眩液晶大屏 (严格标定 sRGB [81, 130, 170] -> #5182aa + 玻璃高光)
    mat_screen = bpy.data.materials.new(name="Mat_Z_Screen_Display")
    mat_screen.use_nodes = True
    s_nodes = mat_screen.node_tree.nodes
    s_links = mat_screen.node_tree.links
    s_nodes.clear()
    s_out = s_nodes.new(type='ShaderNodeOutputMaterial')
    s_bsdf = s_nodes.new(type='ShaderNodeBsdfPrincipled')
    s_bsdf.inputs['Base Color'].default_value = (0.082, 0.228, 0.405, 1.0)
    if 'Emission Color' in s_bsdf.inputs:
        s_bsdf.inputs['Emission Color'].default_value = (0.082, 0.228, 0.405, 1.0)
        s_bsdf.inputs['Emission Strength'].default_value = 0.20 # 轻微发光，保障镜面高光反射
    s_bsdf.inputs['Roughness'].default_value = 0.10
    if 'Specular IOR Level' in s_bsdf.inputs:
        s_bsdf.inputs['Specular IOR Level'].default_value = 0.95
    elif 'Specular' in s_bsdf.inputs:
        s_bsdf.inputs['Specular'].default_value = 0.95
    s_links.new(s_bsdf.outputs['BSDF'], s_out.inputs['Surface'])
    materials['screen_display'] = mat_screen
    
    # 5. 遮阳挑檐顶盖 (深灰吸光防眩涂层)
    materials['canopy_dark'] = create_pbr_material(
        name="Mat_Z_Canopy_Dark",
        base_color=(0.06, 0.07, 0.08, 1.0),
        metallic=0.75,
        roughness=0.45,
        specular=0.5
    )
    
    # 6. 滑轨主横梁型材 (深灰工业氧化铝型材)
    materials['track_frame'] = create_pbr_material(
        name="Mat_Z_Track_Frame",
        base_color=(0.10, 0.11, 0.12, 1.0),
        metallic=0.85,
        roughness=0.30,
        specular=0.7
    )
    
    # 7. 垂直刚性闭环端部拉杆与传动销钉 (工程高亮橙色)
    materials['link_rod_orange'] = create_pbr_material(
        name="Mat_Z_Link_Rod_Orange",
        base_color=(0.92, 0.52, 0.08, 1.0),
        metallic=0.88,
        roughness=0.22,
        specular=0.95
    )
    
    # 8. SUS304 高精度冷拔不锈钢伸缩内套杆
    materials['ext_rail_steel'] = create_pbr_material(
        name="Mat_Z_ExtRail_Steel",
        base_color=(0.85, 0.86, 0.88, 1.0),
        metallic=0.95,
        roughness=0.14,
        specular=0.98
    )
    
    # 9. 对角线空间铰链标识色 (青色=翻转主轴，品红=折叠铺开轴)
    materials['hinge_flip_cyan'] = create_pbr_material(
        name="Mat_Z_Hinge_Flip_Cyan",
        base_color=(0.15, 0.80, 0.90, 1.0),
        metallic=0.85,
        roughness=0.25,
        specular=0.9
    )
    materials['hinge_fold_magenta'] = create_pbr_material(
        name="Mat_Z_Hinge_Fold_Magenta",
        base_color=(0.90, 0.20, 0.80, 1.0),
        metallic=0.85,
        roughness=0.25,
        specular=0.9
    )
    
    return materials

def create_board_with_aluminum_bezel(name, width, height, thickness, bezel_width, mat_face, mat_bezel, has_knob=False, knob_side='right', materials=None):
    """
    创建带有标准 6063-T5 阳极氧化铝合金拉丝边框的精致黑板扇叶
    """
    collection = bpy.context.scene.collection
    root = bpy.data.objects.new(name, None)
    collection.objects.link(root)
    
    inner_w = width - 2 * bezel_width
    inner_h = height - 2 * bezel_width
    
    # 黑板中心书写板芯
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    face = bpy.context.active_object
    face.name = f"{name}_Face"
    face.scale = (inner_w, thickness * 0.92, inner_h)
    face.location = (0, 0, 0)
    face.data.materials.append(mat_face)
    face.parent = root
    
    # 铝合金边框 (上、下、左、右四段精准拼接)
    # 上下边框
    for tb_sign, tb_name in [(1, "Top"), (-1, "Bot")]:
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        bezel_tb = bpy.context.active_object
        bezel_tb.name = f"{name}_Bezel_{tb_name}"
        bezel_tb.scale = (width, thickness, bezel_width)
        bezel_tb.location = (0, 0, tb_sign * (height/2 - bezel_width/2))
        bezel_tb.data.materials.append(mat_bezel)
        bezel_tb.parent = root
        
    # 左右边框
    for lr_sign, lr_name in [(-1, "Left"), (1, "Right")]:
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        bezel_lr = bpy.context.active_object
        bezel_lr.name = f"{name}_Bezel_{lr_name}"
        bezel_lr.scale = (bezel_width, thickness, inner_h)
        bezel_lr.location = (lr_sign * (width/2 - bezel_width/2), 0, 0)
        bezel_lr.data.materials.append(mat_bezel)
        bezel_lr.parent = root
        
    # 镀铬小圆钮拉手 (嵌入式手柄)
    if has_knob and materials:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.016, depth=0.018, vertices=32)
        knob = bpy.context.active_object
        knob.name = f"{name}_Knob"
        knob.rotation_euler = (math.radians(90), 0, 0)
        knob_x = (width/2 - 0.08) if knob_side == 'right' else (-width/2 + 0.08)
        knob.location = (knob_x, -thickness/2 - 0.009, 0)
        knob.data.materials.append(materials['chrome_handle'])
        knob.parent = root
        
    return root

def build_single_z_system(system_name, base_z, materials):
    """
    构建一套完整的第三代（Z系列）多维叠合翻转智能黑板机构学总装
    - 双层黑板: 内层主板(12mm) + 外层折叠板(12mm)
    - 对角线双铰链空间正交拓扑
    - 双横梁滑轨、伸缩套杆与工程拉杆
    """
    collection = bpy.context.scene.collection
    sys_root = bpy.data.objects.new(system_name, None)
    sys_root.location = (0, 0, base_z)
    collection.objects.link(sys_root)
    
    # 标准工程尺寸参数 (GB/T 28231 与 v1.2 规范)
    screen_w, screen_h = 1.98, 1.14
    screen_disp_w, screen_disp_h = 1.90, 1.08
    board_w, board_h = 0.99, 1.10
    layer_th = 0.012  # 单层板厚 12mm
    bezel_w = 0.015   # 铝合金边框宽 15mm
    rail_total_w = 4.0
    rail_h = 0.060
    rail_d = 0.080
    
    # -------------------------------------------------------------------------
    # 1. 上下固定主滑轨横梁 (6063-T5 铝合金 C 型槽型材)
    # -------------------------------------------------------------------------
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    top_rail = bpy.context.active_object
    top_rail.name = f"{system_name}_Top_Rail"
    top_rail.scale = (rail_total_w, rail_d, rail_h)
    top_rail.location = (0, -0.005, screen_h/2 + rail_h/2 + 0.005)
    top_rail.data.materials.append(materials['track_frame'])
    top_rail.parent = sys_root
    
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    bot_rail = bpy.context.active_object
    bot_rail.name = f"{system_name}_Bot_Rail"
    bot_rail.scale = (rail_total_w, rail_d, rail_h)
    bot_rail.location = (0, -0.005, -screen_h/2 - rail_h/2 - 0.005)
    bot_rail.data.materials.append(materials['track_frame'])
    bot_rail.parent = sys_root
    
    # -------------------------------------------------------------------------
    # 2. 中置 86寸 大屏与水平平直遮阳挑檐 (0° 平檐，后置沉台安全避让黑板)
    # -------------------------------------------------------------------------
    screen_root = bpy.data.objects.new(f"{system_name}_Screen_Root", None)
    screen_root.location = (0, 0, 0)
    collection.objects.link(screen_root)
    screen_root.parent = sys_root
    
    # 86寸大屏外壳沉台 (后置 Y = +0.055m)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    screen_casing = bpy.context.active_object
    screen_casing.name = f"{system_name}_Screen_Casing"
    screen_casing.scale = (screen_w, 0.045, screen_h)
    screen_casing.location = (0, 0.055, 0)
    screen_casing.data.materials.append(materials['track_frame'])
    screen_casing.parent = screen_root
    
    # 显示面板发光玻璃 (Y = +0.032m，前端在 +0.0245m，预留 25mm 充足避让间距)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    screen_face = bpy.context.active_object
    screen_face.name = f"{system_name}_Screen_Display_Glass"
    screen_face.scale = (screen_disp_w, 0.015, screen_disp_h)
    screen_face.location = (0, 0.032, 0)
    screen_face.data.materials.append(materials['screen_display'])
    screen_face.parent = screen_root
    
    # 遮阳平檐 (紧固于大屏上方，自然向前挑出 140mm，倾角 0.0° 水平放平)
    canopy_pivot = bpy.data.objects.new(f"{system_name}_Canopy_Pivot", None)
    canopy_pivot.location = (0, 0.055, screen_h/2 + 0.01)
    canopy_pivot.rotation_euler = (0, 0, 0) # 水平绝对放平！
    collection.objects.link(canopy_pivot)
    canopy_pivot.parent = screen_root
    
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    canopy_blade = bpy.context.active_object
    canopy_blade.name = f"{system_name}_Canopy_Blade_Flat"
    canopy_blade.scale = (screen_w + 0.04, 0.14, 0.016)
    canopy_blade.location = (0, -0.07, 0)
    canopy_blade.data.materials.append(materials['canopy_dark'])
    canopy_blade.parent = canopy_pivot
    
    # -------------------------------------------------------------------------
    # 3. 左右两侧机构组件（滑块、套杆、垂直拉杆、对角线双铰链与双层板）
    # -------------------------------------------------------------------------
    left_comp = build_side_mechanism(system_name, "Left", -1, screen_w, screen_h, board_w, board_h, layer_th, bezel_w, rail_total_w, materials, sys_root)
    right_comp = build_side_mechanism(system_name, "Right", 1, screen_w, screen_h, board_w, board_h, layer_th, bezel_w, rail_total_w, materials, sys_root)
    
    return {
        'root': sys_root,
        'screen_root': screen_root,
        'canopy_pivot': canopy_pivot,
        'left': left_comp,
        'right': right_comp,
        'screen_w': screen_w,
        'board_w': board_w
    }

def build_side_mechanism(system_name, side_name, side_sign, screen_w, screen_h, board_w, board_h, layer_th, bezel_w, rail_total_w, materials, sys_root):
    """构建单侧（左侧或右侧）的完整滑移套杆、对角线双铰链与双层贴合黑板"""
    collection = bpy.context.scene.collection
    
    # 侧滑滑块控制器 (Slide Controller, 基准挂在常态中心，Y = -0.005m)
    base_center_x = side_sign * (screen_w/2 + board_w/2 + 0.01)
    ctrl_slide = bpy.data.objects.new(f"{system_name}_Ctrl_Slide_{side_name}", None)
    ctrl_slide.location = (base_center_x, -0.005, 0)
    collection.objects.link(ctrl_slide)
    ctrl_slide.parent = sys_root
    
    rail_h = 0.060
    rail_d = 0.080
    
    # -------------------------------------------------------------------------
    # 隐藏式重型内滑块 (100% 收纳于 6063-T5 主导轨内腔，两翼绝无外凸钢架)
    # -------------------------------------------------------------------------
    # 上下各配置一段隐蔽式铝合金导向滑块 (与主滑轨同材质，两端绝对平齐无外凸)
    for tb_sign, tb_name in [(1, "Top"), (-1, "Bot")]:
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        g_block = bpy.context.active_object
        g_block.name = f"{system_name}_SliderBlock_{side_name}_{tb_name}"
        g_block.scale = (board_w * 0.96, rail_d * 0.65, rail_h * 0.65)
        g_block.location = (0, 0, tb_sign * (screen_h/2 + rail_h/2 + 0.005))
        g_block.data.materials.append(materials['track_frame'])
        g_block.parent = ctrl_slide
    
    # -------------------------------------------------------------------------
    # 对角线双铰链之一：【里面的外侧】翻转主铰链 (Flip / Yaw / Pitch Hinge)
    # 位于内层主板远离大屏的外侧竖直边缘 (X = outer_edge, Y = 0 相对滑块)
    # -------------------------------------------------------------------------
    outer_edge_x = side_sign * (board_w/2)
    ctrl_flip = bpy.data.objects.new(f"{system_name}_Ctrl_Flip_{side_name}", None)
    ctrl_flip.location = (outer_edge_x, 0, 0) # 里面的外侧
    collection.objects.link(ctrl_flip)
    ctrl_flip.parent = ctrl_slide
    
    # 翻转主铰链青色五金转轴 (上下两组)
    for h_z in [0.42, -0.42]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.016, depth=0.08, vertices=24)
        h_obj = bpy.context.active_object
        h_obj.name = f"{system_name}_Hinge_Flip_{side_name}_{'Top' if h_z>0 else 'Btm'}"
        h_obj.location = (outer_edge_x, 0, h_z)
        h_obj.data.materials.append(materials['hinge_flip_cyan'])
        h_obj.parent = ctrl_slide
        
    # -------------------------------------------------------------------------
    # 内层主板 (里面的板，厚度 12mm，主受力构件)
    # -------------------------------------------------------------------------
    inner_board = create_board_with_aluminum_bezel(
        name=f"{system_name}_Inner_MainBoard_{side_name}",
        width=board_w,
        height=board_h,
        thickness=layer_th,
        bezel_width=bezel_w,
        mat_face=materials['blackboard_green'],
        mat_bezel=materials['aluminum_bezel'],
        has_knob=False,
        materials=materials
    )
    # 挂载在翻转主铰链上，中心向内偏移 board_w/2
    inner_board.location = (-side_sign * (board_w/2), 0, 0)
    inner_board.parent = ctrl_flip
    
    # -------------------------------------------------------------------------
    # 对角线双铰链之二：【外面的内侧】多维折叠铺开铰链 (Fold 180° Hinge)
    # 位于外层板靠近大屏的内侧竖直边缘 (X = inner_edge, Y = -0.012m 面向教室前缘)
    # -------------------------------------------------------------------------
    ctrl_fold = bpy.data.objects.new(f"{system_name}_Ctrl_Fold_{side_name}", None)
    ctrl_fold.location = (-side_sign * board_w, -0.012, 0) # 外面的内侧
    collection.objects.link(ctrl_fold)
    ctrl_fold.parent = ctrl_flip # 固连于主翻转骨架，随翻转随动
    
    # 折叠铰链品红色五金转轴 (上下两组)
    for f_z in [0.42, -0.42]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.014, depth=0.08, vertices=24)
        f_obj = bpy.context.active_object
        f_obj.name = f"{system_name}_Hinge_Fold_{side_name}_{'Top' if f_z>0 else 'Btm'}"
        f_obj.location = (-side_sign * board_w, -0.012, f_z)
        f_obj.data.materials.append(materials['hinge_fold_magenta'])
        f_obj.parent = ctrl_flip
        
    # -------------------------------------------------------------------------
    # 外层折叠板 (外面的板，厚度 12mm，具有双面墨绿书写层)
    # -------------------------------------------------------------------------
    outer_board = create_board_with_aluminum_bezel(
        name=f"{system_name}_Outer_FoldingBoard_{side_name}",
        width=board_w,
        height=board_h,
        thickness=layer_th,
        bezel_width=bezel_w,
        mat_face=materials['blackboard_green'],
        mat_bezel=materials['aluminum_bezel'],
        has_knob=True,
        knob_side='right' if side_sign > 0 else 'left',
        materials=materials
    )
    # 当 Fold = 0° 时，外层板向外平贴于内层板前方 (距折叠铰链偏移 -0.002m，保留2mm磁吸消隙间隙)
    outer_board.location = (side_sign * (board_w/2), -0.002, 0)
    outer_board.parent = ctrl_fold
    
    return {
        'ctrl_slide': ctrl_slide,
        'ctrl_flip': ctrl_flip,
        'ctrl_fold': ctrl_fold,
        'inner_board': inner_board,
        'outer_board': outer_board,
        'side_sign': side_sign,
        'board_w': board_w
    }

def set_state_covered(system):
    """
    配置工况一：初始闭合·市面主流全覆盖封屏形态 [COVERED - 4000mm]
    - 外层折叠板向中回转 180° 对接，100% 遮蔽保护 86 寸大屏
    - 侧滑滑移 = 0，翻转避光 = 0
    - 整机呈现 4000mm 连续无缝墨绿黑板纯板书状态
    """
    for side_name in ['left', 'right']:
        comp = system[side_name]
        sgn = comp['side_sign']
        comp['ctrl_slide'].location.x = sgn * (system['screen_w']/2 + comp['board_w']/2 + 0.01)
        comp['ctrl_flip'].rotation_euler = (0, 0, 0)
        # 外层板绕内侧铰链向中心旋转 180°
        comp['ctrl_fold'].rotation_euler = (0, 0, -sgn * math.radians(180))

def set_state_compact(system):
    """
    配置工况二：常态多媒体·大屏露显双层叠合形态 [COMPACT - 4000mm]
    - 外层折叠板回折 180° 与内层主板紧密叠合（厚 26mm）
    - 中间 86 寸 4K 大屏全景露出
    - 左右各保留 1000mm 叠合黑板书写区
    """
    for side_name in ['left', 'right']:
        comp = system[side_name]
        sgn = comp['side_sign']
        comp['ctrl_slide'].location.x = sgn * (system['screen_w']/2 + comp['board_w']/2 + 0.01)
        comp['ctrl_flip'].rotation_euler = (0, 0, 0)
        comp['ctrl_fold'].rotation_euler = (0, 0, 0) # 贴合态

def set_state_deployed_antiglare(system, yaw_deg=14.0, pitch_deg=-8.0, slide_m=1.0):
    """
    配置工况三：大视野与三维空间避光极限展开形态 [DEPLOYED - 6000mm]
    - 左右叠合黑板向外平移侧滑 1000mm（总宽 6000mm）
    - 显露双横梁 Φ28mm 伸缩内套杆与垂直拉杆
    - 整组叠合黑板绕外侧主铰链做偏航旋转 (Yaw) 与纵向俯仰 (Pitch) 避光
    """
    for side_name in ['left', 'right']:
        comp = system[side_name]
        sgn = comp['side_sign']
        # 向外侧滑 1.0 米
        base_x = sgn * (system['screen_w']/2 + comp['board_w']/2 + 0.01)
        comp['ctrl_slide'].location.x = base_x + sgn * slide_m
        # 折叠板保持紧密贴合
        comp['ctrl_fold'].rotation_euler = (0, 0, 0)
        # 整体做空间偏航与俯仰避光
        comp['ctrl_flip'].rotation_euler = (
            math.radians(pitch_deg),
            0,
            sgn * math.radians(yaw_deg)
        )

def set_state_deployed_filled(system, slide_m=1.0):
    """
    配置工况三之二：极限侧滑展开且折叠板回填连贯全景板书形态 [DEPLOYED_FILLED - 6000mm]
    - 左右叠合黑板向外平移侧滑 1000mm（整机跨度达 6000mm）
    - 主翻转轴放平 (Yaw=0°, Pitch=0°，保持平整板书基准面)
    - 折叠板绕【外面的内侧铰链】再次向内回转 180°（掰开向内）
    - 折叠板严丝合缝填补外侧主板与中置 86 寸大屏之间的 1000mm 间隙！
    - 呈现：左翼 2000mm 连续墨绿黑板 + 中间 2000mm 86寸大屏 + 右翼 2000mm 连续墨绿黑板 = 6000mm 满幅教学巨幕！
    """
    for side_name in ['left', 'right']:
        comp = system[side_name]
        sgn = comp['side_sign']
        # 向外侧滑 1.0 米
        base_x = sgn * (system['screen_w']/2 + comp['board_w']/2 + 0.01)
        comp['ctrl_slide'].location.x = base_x + sgn * slide_m
        # 主翻转轴放平
        comp['ctrl_flip'].rotation_euler = (0, 0, 0)
        # 外层折叠板向中回转 180° 对接填补空缺
        comp['ctrl_fold'].rotation_euler = (0, 0, -sgn * math.radians(180))

def setup_lights_and_camera(output_dir):
    """搭建正交高清相机与真实物理采光系统"""
    scene = bpy.context.scene
    collection = scene.collection
    
    # 1. 正交高清摄像机
    cam_data = bpy.data.cameras.new("Z_Master_Camera_Data")
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = 5.20 # 默认视距
    cam_obj = bpy.data.objects.new("Z_Master_Camera", cam_data)
    cam_obj.location = (0, -4.5, 0)
    cam_obj.rotation_euler = (math.radians(90), 0, 0)
    collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    scene.render.resolution_x = 3840
    scene.render.resolution_y = 2160
    scene.render.resolution_percentage = 100
    
    # 2. 定向 Spot 聚光灯 (精准复刻原版采样 #e2e3e4 正圆高光球)
    spot_data = bpy.data.lights.new(name="Spot_Screen_Highlight", type='SPOT')
    spot_data.energy = 650.0
    spot_data.spot_size = math.radians(32.0)
    spot_data.spot_blend = 0.45
    spot_data.color = (1.0, 1.0, 1.0)
    spot_obj = bpy.data.objects.new("Spot_Screen_Highlight", spot_data)
    collection.objects.link(spot_obj)
    spot_obj.location = (0.22, -2.8, 1.88)
    spot_obj.rotation_euler = (math.radians(34), math.radians(4), math.radians(8))
    
    # 3. 柔和主日光 (Sun Light)
    sun_data = bpy.data.lights.new(name="Sun_Classroom", type='SUN')
    sun_data.energy = 2.4
    sun_data.color = (1.0, 0.98, 0.95)
    sun_obj = bpy.data.objects.new("Sun_Classroom", sun_data)
    collection.objects.link(sun_obj)
    sun_obj.location = (-4.0, -5.0, 6.0)
    sun_obj.rotation_euler = (math.radians(45), math.radians(-15), math.radians(35))
    
    # 4. 前方漫反射补光板 (Area Light)
    fill_data = bpy.data.lights.new(name="Fill_Ambient_Area", type='AREA')
    fill_data.energy = 140.0
    fill_data.size = 6.0
    fill_data.color = (0.95, 0.97, 1.0)
    fill_obj = bpy.data.objects.new("Fill_Ambient_Area", fill_data)
    collection.objects.link(fill_obj)
    fill_obj.location = (0, -4.0, 0)
    fill_obj.rotation_euler = (math.radians(90), 0, 0)
    
    return cam_obj

def render_state(scene, cam_obj, filepath, ortho_scale=5.20):
    """渲染指定工况至 4K 文件"""
    cam_obj.data.ortho_scale = ortho_scale
    scene.render.filepath = filepath
    print(f">> [Render] 正在渲染 4K 图像: {filepath} (ortho_scale={ortho_scale})...")
    bpy.ops.render.render(write_still=True)
    print(f">> [Render] 成功保存: {filepath}")

def main():
    print("=" * 75)
    print(">> [Init] 启动第三代（Z系列）多维叠合翻转全覆盖黑板 Blender 3D 构建工程...")
    print("=" * 75)
    
    if os.name == 'nt' or sys.platform.startswith('win'):
        output_dir = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\Z系列"
    else:
        # 兼容 WSL / Linux
        output_dir = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\Z系列"
    os.makedirs(output_dir, exist_ok=True)
    
    reset_scene()
    setup_render_engine()
    materials = build_calibrated_materials()
    
    # 构建第三代核心黑板机构总装 (单体标准基准置于 Z = 0)
    system = build_single_z_system("GuangHeng_Z_System", 0.0, materials)
    cam_obj = setup_lights_and_camera(output_dir)
    
    # 保存第三代核心工程母本文件
    master_blend_path = os.path.join(output_dir, "Z_Series_Master.blend")
    bpy.ops.wm.save_as_mainfile(filepath=master_blend_path)
    print(f">> [Master] 成功保存第三代核心母本工程: {master_blend_path}")
    
    scene = bpy.context.scene
    
    # -------------------------------------------------------------------------
    # 渲染 Z1：工况一·市面主流全覆盖封屏形态 [COVERED - 4000mm]
    # -------------------------------------------------------------------------
    print(">> [Config] 切换至工况一：全覆盖封屏形态 (Fold=180°, 100% 遮蔽保护 86寸大屏)...")
    set_state_covered(system)
    z1_path = os.path.join(output_dir, "Z1_工况一_全覆盖封屏形态_4000mm_4K.png")
    render_state(scene, cam_obj, z1_path, ortho_scale=4.75)
    
    # -------------------------------------------------------------------------
    # 渲染 Z2：工况二·常态多媒体大屏露显双层叠合形态 [COMPACT - 4000mm]
    # -------------------------------------------------------------------------
    print(">> [Config] 切换至工况二：常态多媒体露显形态 (Fold=0°, 叠合厚度 26mm, 露大屏)...")
    set_state_compact(system)
    z2_path = os.path.join(output_dir, "Z2_工况二_常态大屏露显双层叠合形态_4000mm_4K.png")
    render_state(scene, cam_obj, z2_path, ortho_scale=4.75)
    
    # -------------------------------------------------------------------------
    # 渲染 Z3_1：工况三之一·平移侧滑极限展开与避光偏航形态 [DEPLOYED_ANTIGLARE - 6000mm]
    # -------------------------------------------------------------------------
    print(">> [Config] 切换至工况三之一：大视野侧滑与空间避光形态 (Slide=1.0m, Yaw=14°, Pitch=-8°)...")
    set_state_deployed_antiglare(system, yaw_deg=14.0, pitch_deg=-8.0, slide_m=1.0)
    z3_1_path = os.path.join(output_dir, "Z3_1_工况三之一_平移侧滑极限展开与避光偏航形态_6000mm_4K.png")
    render_state(scene, cam_obj, z3_1_path, ortho_scale=6.60)
    z3_legacy_path = os.path.join(output_dir, "Z3_工况三_平移侧滑极限展开与避光偏航形态_6000mm_4K.png")
    try:
        import shutil
        shutil.copyfile(z3_1_path, z3_legacy_path)
    except Exception:
        pass
    
    # -------------------------------------------------------------------------
    # 渲染 Z3_2：工况三之二·极限侧滑展开且折叠板回填连贯全景板书形态 [DEPLOYED_FILLED - 6000mm]
    # -------------------------------------------------------------------------
    print(">> [Config] 切换至工况三之二：外滑1.0m且折叠板向内翻折180°回填全景形态 (Slide=1.0m, Fold=180°)...")
    set_state_deployed_filled(system, slide_m=1.0)
    z3_2_path = os.path.join(output_dir, "Z3_2_工况三之二_极限侧滑展开且折叠板回填连贯板书形态_6000mm_4K.png")
    render_state(scene, cam_obj, z3_2_path, ortho_scale=6.60)
    
    # -------------------------------------------------------------------------
    # 渲染 Z4：对角线双铰链精密机构微距特写
    # -------------------------------------------------------------------------
    print(">> [Config] 切换至对角线双铰链微距机构特写机位...")
    set_state_compact(system) # 常态叠合下展现内侧品红折叠轴与外侧青色翻转轴
    cam_obj.location = (1.50, -2.0, 0.35)
    cam_obj.rotation_euler = (math.radians(78), 0, math.radians(12))
    z4_path = os.path.join(output_dir, "Z4_对角线双铰链精密机构特写_4K.png")
    render_state(scene, cam_obj, z4_path, ortho_scale=1.90)
    
    # 复位相机
    cam_obj.location = (0, -4.5, 0)
    cam_obj.rotation_euler = (math.radians(90), 0, 0)
    
    print("=" * 75)
    print(">> [Success] 第三代（Z系列）三大标准工况与精密特写 4K 渲染全量完成！")
    print("=" * 75)

if __name__ == '__main__':
    main()
