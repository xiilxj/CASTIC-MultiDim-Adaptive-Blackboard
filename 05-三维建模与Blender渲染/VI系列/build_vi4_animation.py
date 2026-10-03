#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================================================================
第42届瑞安市青少年科技创新大赛 (CASTIC) 参赛重点攻坚工程
工程代号: 第三代（VI4系列 / GH-VI-2026）正前方零穿模书页式翻折回填与C型端头限位关键帧动画母本构建脚本
文件路径: D:\\Desktop\\CASTICpjhb\\05-三维建模与Blender渲染\\VI系列\\build_vi4_animation.py
输出文件: vi4.blend (严格遵从用户指令：不渲染视频，供用户进.blend文件审阅关键帧)
审核标识: 第 27 轮工程技术审核 (针对用户最新反馈彻底修复翻折轨迹：100% 从正前方划弧翻转回填，绝不穿过墙后)
========================================================================================
核心重构要点:
  1. 【正前方书页式翻折轨迹彻底校正】:
     - 阶段四 B (Frame 351~430): 折叠黑板绕内侧竖边铰链翻折回填时，
       中间帧轨迹世界 Y 轴严格保持在负值区间 (Y = -0.471m，面向摄像机/学生正前方)！
       像翻开精美书页一样从正前方优美向前翻开、向内平铺，彻底杜绝从后方穿过墙面的错误！
     - 翻转终点精准落入 X = ±2.510m，严丝合缝填补 ±[2.0m, 3.0m] 空缺，锁定 8000mm 满幅教学巨幕！
  2. 【阶段二活动框架整体外翻 180° 正前方开门轨迹】:
     - 阶段二 (Frame 121~200): 活动黑板整体绕外侧主铰链轴 (X=±2.0m) 翻转 180°，
       中间帧同样从正前方 (Y = -0.515m) 平滑向外推开平铺！
  3. 【金属衍生杆外端边界 C 形限位卡槽 (正C与反C)】:
     - 左侧衍生套杆最外端 (X=-4.0m): 卡槽开口朝向多媒体 (朝右)，正视呈现标准的【正 C (C)】！
     - 右侧衍生套杆最外端 (X=+4.0m): 卡槽开口朝向多媒体 (朝左)，正视呈现标准的【反 C (])】！
     - 滑块滑至外端边界时前端精准卡入 C 槽内部，形成刚性物理限位！
  4. 【初始态零外露杆件标准】:
     - Frame 1~40 初始闭合封屏时，仅绳索杆向内伸出碰头，外侧无任何杆件外露。
========================================================================================
"""

import bpy
import math
import os
import sys

def reset_scene():
    """彻底重置并净化场景"""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 480
    scene.render.fps = 30

def setup_render_settings():
    """配置预览与着色器参数"""
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        prefs.compute_device_type = 'OPTIX'
        for d in prefs.devices:
            d.use = True
        scene.cycles.device = 'GPU'
    except Exception:
        try:
            prefs = bpy.context.preferences.addons['cycles'].preferences
            prefs.compute_device_type = 'CUDA'
            for d in prefs.devices:
                d.use = True
            scene.cycles.device = 'GPU'
        except Exception:
            scene.cycles.device = 'CPU'
            
    scene.cycles.samples = 64
    scene.cycles.preview_samples = 32
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'None'
    
    # 标定视口背景 (#3a3a3a)
    world = bpy.data.worlds.new("VI4_World")
    scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs['Color'].default_value = (0.038, 0.038, 0.038, 1.0)
        bg_node.inputs['Strength'].default_value = 1.0

def create_pbr(name, base_color, metallic=0.0, roughness=0.5, specular=0.5):
    """创建标准 PBR 材质"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    out = nodes.new(type='ShaderNodeOutputMaterial')
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = base_color
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    if 'Specular IOR Level' in bsdf.inputs:
        bsdf.inputs['Specular IOR Level'].default_value = specular
    elif 'Specular' in bsdf.inputs:
        bsdf.inputs['Specular'].default_value = specular
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat

def build_materials():
    """构建标定物理材质库"""
    mats = {}
    mats['blackboard_green'] = create_pbr(
        "Mat_Blackboard_Green",
        base_color=(0.052, 0.145, 0.085, 1.0), # #416951 护眼墨绿
        metallic=0.01,
        roughness=0.55,
        specular=0.35
    )
    mats['aluminum_bezel'] = create_pbr(
        "Mat_Aluminum_Bezel",
        base_color=(0.58, 0.59, 0.60, 1.0), # #c7c8ca 铝合金
        metallic=0.96,
        roughness=0.16,
        specular=0.98
    )
    mats['track_frame'] = create_pbr(
        "Mat_Track_Frame_Dark",
        base_color=(0.12, 0.13, 0.14, 1.0),
        metallic=0.88,
        roughness=0.25,
        specular=0.7
    )
    mats['ext_rail_steel'] = create_pbr(
        "Mat_Ext_Rail_Steel",
        base_color=(0.85, 0.86, 0.88, 1.0),
        metallic=0.95,
        roughness=0.18,
        specular=0.95
    )
    mats['c_bracket_accent'] = create_pbr(
        "Mat_C_Bracket_Stop",
        base_color=(0.20, 0.22, 0.25, 1.0), # 精密深灰不锈钢卡槽
        metallic=0.92,
        roughness=0.20,
        specular=0.90
    )
    mats['hinge_cyan'] = create_pbr(
        "Mat_Hinge_Flip_Cyan",
        base_color=(0.15, 0.80, 0.90, 1.0),
        metallic=0.85,
        roughness=0.25,
        specular=0.9
    )
    mats['hinge_magenta'] = create_pbr(
        "Mat_Hinge_Fold_Magenta",
        base_color=(0.90, 0.20, 0.80, 1.0),
        metallic=0.85,
        roughness=0.25,
        specular=0.9
    )
    mats['canopy_dark'] = create_pbr(
        "Mat_Canopy_Dark",
        base_color=(0.06, 0.07, 0.08, 1.0),
        metallic=0.75,
        roughness=0.45,
        specular=0.5
    )
    
    # 86寸大屏液晶发光材质
    mat_screen = bpy.data.materials.new(name="Mat_Screen_Display")
    mat_screen.use_nodes = True
    s_nodes = mat_screen.node_tree.nodes
    s_links = mat_screen.node_tree.links
    s_nodes.clear()
    s_out = s_nodes.new(type='ShaderNodeOutputMaterial')
    s_bsdf = s_nodes.new(type='ShaderNodeBsdfPrincipled')
    s_bsdf.inputs['Base Color'].default_value = (0.082, 0.228, 0.405, 1.0) # #5182aa
    if 'Emission Color' in s_bsdf.inputs:
        s_bsdf.inputs['Emission Color'].default_value = (0.082, 0.228, 0.405, 1.0)
        s_bsdf.inputs['Emission Strength'].default_value = 0.20
    s_bsdf.inputs['Roughness'].default_value = 0.10
    if 'Specular IOR Level' in s_bsdf.inputs:
        s_bsdf.inputs['Specular IOR Level'].default_value = 0.95
    elif 'Specular' in s_bsdf.inputs:
        s_bsdf.inputs['Specular'].default_value = 0.95
    s_links.new(s_bsdf.outputs['BSDF'], s_out.inputs['Surface'])
    mats['screen_display'] = mat_screen
    
    return mats

def create_board_mesh(name, width, height, thickness, bezel_w, materials):
    """创建双面墨绿板芯且精致铝合金包边的黑板组件"""
    collection = bpy.context.scene.collection
    root = bpy.data.objects.new(name, None)
    collection.objects.link(root)
    
    inner_w = width - 2 * bezel_w
    inner_h = height - 2 * bezel_w
    
    # 双面墨绿板芯
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    face = bpy.context.active_object
    face.name = f"{name}_Face"
    face.scale = (inner_w, thickness * 0.90, inner_h)
    face.location = (0, 0, 0)
    face.data.materials.append(materials['blackboard_green'])
    face.parent = root
    
    # 上下左右边框
    for tb_sign, tb_name in [(1, "Top"), (-1, "Bot")]:
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        b = bpy.context.active_object
        b.name = f"{name}_Bezel_{tb_name}"
        b.scale = (width, thickness, bezel_w)
        b.location = (0, 0, tb_sign * (height/2 - bezel_w/2))
        b.data.materials.append(materials['aluminum_bezel'])
        b.parent = root
        
    for lr_sign, lr_name in [(-1, "Left"), (1, "Right")]:
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        b = bpy.context.active_object
        b.name = f"{name}_Bezel_{lr_name}"
        b.scale = (bezel_w, thickness, inner_h)
        b.location = (lr_sign * (width/2 - bezel_w/2), 0, 0)
        b.data.materials.append(materials['aluminum_bezel'])
        b.parent = root
        
    return root

def create_c_bracket_mesh(name, side_sign, rail_h, rail_d, materials):
    """
    创建高精度 C 形端头限位卡槽组件 (End Stop Bracket):
    - 左侧 (side_sign = -1): 卡口朝右指向多媒体，正视图呈现标准的【正 C (C)】！
    - 右侧 (side_sign = +1): 卡口朝左指向多媒体，正视图呈现标准的【反 C (])】！
    """
    collection = bpy.context.scene.collection
    root = bpy.data.objects.new(name, None)
    collection.objects.link(root)
    
    bracket_th = 0.025   # C型背板厚度 25mm
    flange_len = 0.090   # C型上下卡爪伸出长度 90mm
    total_h = 1.30       # 跨越上下导轨总高度 1300mm
    flange_h = 0.040     # 上下卡爪厚度 40mm
    d_depth = rail_d * 1.35 # 前后包覆深度
    
    # 1. C型竖向封头背板 (位于最外端，封闭外侧边界)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    back_plate = bpy.context.active_object
    back_plate.name = f"{name}_BackPlate"
    back_plate.scale = (bracket_th, d_depth, total_h)
    back_plate.location = (0, 0, 0)
    back_plate.data.materials.append(materials['c_bracket_accent'])
    back_plate.parent = root
    
    # 2. C型上下水平卡爪 (朝内侧伸出，形成 C 槽开口)
    open_dir = -side_sign # 向内开口的方向
    
    for tb_sign, tb_name in [(1, "Top"), (-1, "Bot")]:
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        flange = bpy.context.active_object
        flange.name = f"{name}_Flange_{tb_name}"
        flange.scale = (flange_len, d_depth, flange_h)
        flange.location = (open_dir * (flange_len / 2 + bracket_th / 2), 0, tb_sign * (total_h / 2 - flange_h / 2))
        flange.data.materials.append(materials['c_bracket_accent'])
        flange.parent = root
        
    return root

def set_bezier_interpolation(obj):
    """将对象的所有动画曲线设置为平滑 Bezier 加减速"""
    try:
        if obj.animation_data and obj.animation_data.action:
            act = obj.animation_data.action
            if hasattr(act, 'fcurves'):
                for fcurve in act.fcurves:
                    for kfp in fcurve.keyframe_points:
                        kfp.interpolation = 'BEZIER'
            elif hasattr(act, 'curves'):
                for curve in act.curves:
                    for kfp in curve.keyframe_points:
                        kfp.interpolation = 'BEZIER'
    except Exception as e:
        print(f">> [Info] 插值设置已使用默认 Bezier: {e}")

def build_vi4_animation_scene(output_dir):
    """
    构建 VI4 系列核心装配场景与全流程 480 帧关键帧
    """
    scene = bpy.context.scene
    collection = scene.collection
    mats = build_materials()
    
    # 根节点
    sys_root = bpy.data.objects.new("GH_VI4_System_Root", None)
    collection.objects.link(sys_root)
    sys_root.location = (0, 0, 0)
    
    # 几何尺寸标准
    screen_w, screen_h = 2.0, 1.15
    board_w, board_h = 0.99, 1.10
    single_th = 0.012 # 12mm 单板厚度
    bezel_w = 0.015
    rail_total_w = 4.0
    rail_h, rail_d = 0.060, 0.080
    
    # -------------------------------------------------------------------------
    # 1. 后方固定教室墙体基准 (4000mm: 1m固定板 + 2m大屏 + 1m固定板)
    # -------------------------------------------------------------------------
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    screen_casing = bpy.context.active_object
    screen_casing.name = "Fixed_Center_Screen_Casing"
    screen_casing.scale = (screen_w, 0.045, screen_h)
    screen_casing.location = (0, 0.025, 0)
    screen_casing.data.materials.append(mats['track_frame'])
    screen_casing.parent = sys_root
    
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    screen_glass = bpy.context.active_object
    screen_glass.name = "Fixed_Center_Screen_Display"
    screen_glass.scale = (screen_w - 0.06, 0.012, screen_h - 0.06)
    screen_glass.location = (0, 0.005, 0)
    screen_glass.data.materials.append(mats['screen_display'])
    screen_glass.parent = sys_root
    
    # 遮阳平檐 (长 2.04m)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    canopy = bpy.context.active_object
    canopy.name = "Fixed_Canopy_Flat"
    canopy.scale = (screen_w + 0.04, 0.14, 0.016)
    canopy.location = (0, -0.05, screen_h/2 + 0.01)
    canopy.data.materials.append(mats['canopy_dark'])
    canopy.parent = sys_root
    
    # 左右两侧固定黑板模块 (固定在墙面不动，Y = +0.01m)
    fixed_left = create_board_mesh("Fixed_Wall_Blackboard_Left", board_w, board_h, single_th, bezel_w, mats)
    fixed_left.location = (-1.50, 0.01, 0)
    fixed_left.parent = sys_root
    
    fixed_right = create_board_mesh("Fixed_Wall_Blackboard_Right", board_w, board_h, single_th, bezel_w, mats)
    fixed_right.location = (1.50, 0.01, 0)
    fixed_right.parent = sys_root
    
    # 上下固定 C 型导轨主梁 (长 4000mm，X in [-2.0, +2.0])
    for tb_sign, tb_name in [(1, "Top"), (-1, "Bot")]:
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        rail = bpy.context.active_object
        rail.name = f"Fixed_Main_Rail_{tb_name}"
        rail.scale = (rail_total_w, rail_d, rail_h)
        rail.location = (0, -0.012, tb_sign * (screen_h/2 + rail_h/2 + 0.005))
        rail.data.materials.append(mats['track_frame'])
        rail.parent = sys_root
        
    # -------------------------------------------------------------------------
    # 2. 前方可动总成控制器与机构拓扑 (左右对称)
    # -------------------------------------------------------------------------
    controllers = {}
    
    for side_name, side_sign in [("Left", -1), ("Right", 1)]:
        # (1) 翻转主铰链控制器 Ctrl_Flip (位于固定黑板最外侧边缘 X = ±2.0m)
        ctrl_flip = bpy.data.objects.new(f"Ctrl_Flip_{side_name}", None)
        ctrl_flip.location = (side_sign * 2.00, -0.015, 0)
        collection.objects.link(ctrl_flip)
        ctrl_flip.parent = sys_root
        
        # 青色翻转主转轴 (上下两组)
        for h_z in [0.42, -0.42]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.016, depth=0.08, vertices=24)
            h_obj = bpy.context.active_object
            h_obj.name = f"Hinge_Flip_{side_name}_{'Top' if h_z>0 else 'Btm'}"
            h_obj.location = (side_sign * 2.00, -0.015, h_z)
            h_obj.data.materials.append(mats['hinge_cyan'])
            h_obj.parent = sys_root
            
        # (2) 阶段一向内伸缩绳索杆控制器 Ctrl_Rod_Inward (挂载于 Ctrl_Flip)
        # 常态完全收纳在活动框架内部 (局部 X = -side_sign * 0.50)，绝不外露！
        ctrl_rod_in = bpy.data.objects.new(f"Ctrl_Rod_Inward_{side_name}", None)
        ctrl_rod_in.location = (0, 0, 0)
        collection.objects.link(ctrl_rod_in)
        ctrl_rod_in.parent = ctrl_flip
        
        for tb_sign, tb_name in [(1, "Top"), (-1, "Bot")]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=1.00, vertices=24)
            r_in_mesh = bpy.context.active_object
            r_in_mesh.name = f"Rod_Inward_Mesh_{side_name}_{tb_name}"
            r_in_mesh.rotation_euler = (0, math.radians(90), 0)
            r_in_mesh.location = (-side_sign * 0.50, 0, tb_sign * (screen_h/2 + rail_h/2 + 0.005))
            r_in_mesh.data.materials.append(mats['ext_rail_steel'])
            r_in_mesh.parent = ctrl_rod_in
            
        # (3) 阶段三向外衍生金属套杆控制器 Ctrl_Rod_Outward (挂载于 Ctrl_Flip)
        # 常态完全收纳在活动框架内部，初始外伸位移为 0，外侧无任何突出！
        ctrl_rod_out = bpy.data.objects.new(f"Ctrl_Rod_Outward_{side_name}", None)
        ctrl_rod_out.location = (0, 0, 0)
        collection.objects.link(ctrl_rod_out)
        ctrl_rod_out.parent = ctrl_flip
        
        for tb_sign, tb_name in [(1, "Top"), (-1, "Bot")]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.014, depth=1.00, vertices=24)
            r_out_mesh = bpy.context.active_object
            r_out_mesh.name = f"Rod_Outward_Mesh_{side_name}_{tb_name}"
            r_out_mesh.rotation_euler = (0, math.radians(90), 0)
            r_out_mesh.location = (-side_sign * 0.50, 0, tb_sign * (screen_h/2 + rail_h/2 + 0.005))
            r_out_mesh.data.materials.append(mats['ext_rail_steel'])
            r_out_mesh.parent = ctrl_rod_out
            
        # 衍生杆最外端 C 型端头限位卡槽 (固连于 ctrl_rod_out 最外端)
        # - 左侧: 开口朝向多媒体 (朝右)，正视呈现【正 C (C)】！
        # - 右侧: 开口朝向多媒体 (朝左)，正视呈现【反 C (])】！
        c_stop_bracket = create_c_bracket_mesh(
            f"C_Bracket_Stop_{side_name}",
            side_sign=side_sign,
            rail_h=rail_h,
            rail_d=rail_d,
            materials=mats
        )
        c_stop_bracket.location = (-side_sign * 1.00, 0, 0)
        c_stop_bracket.parent = ctrl_rod_out
            
        # (4) 双层黑板滑块控制器 Ctrl_Slide (挂载于 Ctrl_Flip)
        # 常态停留在固定黑板正前方：局部 X = -side_sign * 0.50m (对应世界 X = ±1.5m)
        ctrl_slide = bpy.data.objects.new(f"Ctrl_Slide_{side_name}", None)
        ctrl_slide.location = (-side_sign * 0.50, -0.015, 0)
        collection.objects.link(ctrl_slide)
        ctrl_slide.parent = ctrl_flip
        
        # 滑块滑靴
        for tb_sign, tb_name in [(1, "Top"), (-1, "Bot")]:
            bpy.ops.mesh.primitive_cube_add(size=1.0)
            sb = bpy.context.active_object
            sb.name = f"Slider_Shoe_{side_name}_{tb_name}"
            sb.scale = (board_w * 0.95, rail_d * 0.55, rail_h * 0.55)
            sb.location = (0, 0, tb_sign * (screen_h/2 + rail_h/2 + 0.005))
            sb.data.materials.append(mats['track_frame'])
            sb.parent = ctrl_slide
            
        # 后层主黑板 Layer 2 (固连于滑块，Y = -0.008m)
        board_back = create_board_mesh(f"Back_Main_Board_{side_name}", board_w, board_h, single_th, bezel_w, mats)
        board_back.location = (0, -0.008, 0)
        board_back.parent = ctrl_slide
        
        # (5) 最前层折叠黑板内侧铰链控制器 Ctrl_Fold (关键精确定位！)
        # 铰链位于面向多媒体大屏的【内侧竖边】(外翻滑动后对应世界 X = ±3.0m)
        ctrl_fold = bpy.data.objects.new(f"Ctrl_Fold_{side_name}", None)
        ctrl_fold.location = (side_sign * (board_w / 2), -0.024, 0)
        collection.objects.link(ctrl_fold)
        ctrl_fold.parent = ctrl_slide
        
        # 品红色内侧竖边铰链
        for h_z in [0.40, -0.40]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.010, depth=0.06, vertices=24)
            h_obj = bpy.context.active_object
            h_obj.name = f"Hinge_Fold_{side_name}_{'Top' if h_z>0 else 'Btm'}"
            h_obj.location = (0, 0, h_z)
            h_obj.data.materials.append(mats['hinge_magenta'])
            h_obj.parent = ctrl_fold
            
        # 前层折叠黑板 Layer 1 (常态未翻转时贴在后板正前方)
        board_front = create_board_mesh(f"Front_Folding_Board_{side_name}", board_w, board_h, single_th, bezel_w, mats)
        board_front.location = (-side_sign * (board_w / 2), 0, 0)
        board_front.parent = ctrl_fold
        
        controllers[side_name] = {
            'ctrl_flip': ctrl_flip,
            'ctrl_rod_in': ctrl_rod_in,
            'ctrl_rod_out': ctrl_rod_out,
            'ctrl_slide': ctrl_slide,
            'ctrl_fold': ctrl_fold,
            'board_front': board_front,
            'side_sign': side_sign,
            'board_w': board_w
        }
        
    # -------------------------------------------------------------------------
    # 3. 摄像机与照明系统
    # -------------------------------------------------------------------------
    cam_data = bpy.data.cameras.new("VI4_Master_Camera_Data")
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = 5.20 # 默认视距
    cam_obj = bpy.data.objects.new("VI4_Master_Camera", cam_data)
    cam_obj.location = (0, -5.6, 0)
    cam_obj.rotation_euler = (math.radians(90), 0, 0)
    collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    # 日光与补光
    sun_data = bpy.data.lights.new(name="Sun_VI4", type='SUN')
    sun_data.energy = 2.4
    sun_data.color = (1.0, 0.98, 0.95)
    sun_obj = bpy.data.objects.new("Sun_VI4", sun_data)
    collection.objects.link(sun_obj)
    sun_obj.location = (-4.0, -5.0, 6.0)
    sun_obj.rotation_euler = (math.radians(45), math.radians(-15), math.radians(35))
    
    fill_data = bpy.data.lights.new(name="Fill_Area_VI4", type='AREA')
    fill_data.energy = 150.0
    fill_data.size = 6.0
    fill_obj = bpy.data.objects.new("Fill_Area_VI4", fill_data)
    collection.objects.link(fill_obj)
    fill_obj.location = (0, -4.0, 3.5)
    fill_obj.rotation_euler = (math.radians(40), 0, 0)

    # -------------------------------------------------------------------------
    # 4. 全流程 480 帧动力学关键帧精准注入
    # -------------------------------------------------------------------------
    print(">> [Keyframes] 开始全流程 4 阶段关键帧精准注入...")
    
    l_ctrl = controllers['Left']
    r_ctrl = controllers['Right']
    
    # -------------------------------------------------------------------------
    # 【阶段一初：完全闭合封屏形态】 (Frame 1 ~ 40)
    # - 绳索杆向内伸出 1.0m，中央 X=0 碰头 (戳向里面！)
    # - 双层黑板沿绳索杆向中滑移 1.0m，遮蔽 86寸大屏
    # - 外侧没有任何杆子戳在外面 (外衍生套杆位移=0，C型卡槽在框边)
    # - 翻转主轴=0°，折叠板=0°
    # -------------------------------------------------------------------------
    for c in [l_ctrl, r_ctrl]:
        sgn = c['side_sign']
        
        # 1. 绳索杆：向内伸出 1.0m (相对铰链向中移动 -sgn * 1.0m)
        c['ctrl_rod_in'].location.x = -sgn * 1.00
        c['ctrl_rod_in'].keyframe_insert(data_path="location", index=0, frame=1)
        c['ctrl_rod_in'].keyframe_insert(data_path="location", index=0, frame=40)
        
        # 2. 滑块：向中心滑动 1.0m (相对铰链位置从 -sgn*0.5 变至 -sgn*1.5，世界位置 X = ±0.5m 遮蔽大屏)
        c['ctrl_slide'].location.x = -sgn * 1.50
        c['ctrl_slide'].keyframe_insert(data_path="location", index=0, frame=1)
        c['ctrl_slide'].keyframe_insert(data_path="location", index=0, frame=40)
        
        # 3. 翻转主轴：0°
        c['ctrl_flip'].rotation_euler.z = 0.0
        c['ctrl_flip'].keyframe_insert(data_path="rotation_euler", index=2, frame=1)
        c['ctrl_flip'].keyframe_insert(data_path="rotation_euler", index=2, frame=40)
        
        # 4. 外衍生杆：0m (完全收拢在主梁内部，C型卡槽紧贴框边，绝不突向外面！)
        c['ctrl_rod_out'].location.x = 0.0
        c['ctrl_rod_out'].keyframe_insert(data_path="location", index=0, frame=1)
        c['ctrl_rod_out'].keyframe_insert(data_path="location", index=0, frame=40)
        
        # 5. 折叠板：0° (贴合在后板前面)
        c['ctrl_fold'].rotation_euler.z = 0.0
        c['ctrl_fold'].keyframe_insert(data_path="rotation_euler", index=2, frame=1)
        c['ctrl_fold'].keyframe_insert(data_path="rotation_euler", index=2, frame=40)
        
    cam_data.ortho_scale = 4.80
    cam_data.keyframe_insert(data_path="ortho_scale", frame=1)
    cam_data.keyframe_insert(data_path="ortho_scale", frame=40)

    # -------------------------------------------------------------------------
    # 【阶段一末：外滑复位露屏形态】 (Frame 41 ~ 120)
    # - 双层黑板向外侧滑退 1.0m，退回到左右固定黑板正前方 (世界 X = ±1.5m)
    # - 绳索杆向外完全缩回 (0m，完全收回框架内部)
    # - 86寸大屏完整裸露显现
    # -------------------------------------------------------------------------
    for c in [l_ctrl, r_ctrl]:
        sgn = c['side_sign']
        
        # 绳索杆完全缩回
        c['ctrl_rod_in'].location.x = 0.0
        c['ctrl_rod_in'].keyframe_insert(data_path="location", index=0, frame=120)
        
        # 滑块退回固定板正前方 (相对铰链 X = -sgn*0.5m, 世界 X = ±1.5m)
        c['ctrl_slide'].location.x = -sgn * 0.50
        c['ctrl_slide'].keyframe_insert(data_path="location", index=0, frame=120)
        
        c['ctrl_flip'].rotation_euler.z = 0.0
        c['ctrl_flip'].keyframe_insert(data_path="rotation_euler", index=2, frame=120)
        
        c['ctrl_rod_out'].location.x = 0.0
        c['ctrl_rod_out'].keyframe_insert(data_path="location", index=0, frame=120)
        
        c['ctrl_fold'].rotation_euler.z = 0.0
        c['ctrl_fold'].keyframe_insert(data_path="rotation_euler", index=2, frame=120)
        
    cam_data.ortho_scale = 4.80
    cam_data.keyframe_insert(data_path="ortho_scale", frame=120)

    # -------------------------------------------------------------------------
    # 【阶段二：活动框架整体向外侧翻转整整 180°！】 (Frame 121 ~ 200)
    # - 活动黑板带着框架绕外侧主铰链轴 (X = ±2.0m) 完整向外翻转 180°！
    # - 轨迹完全在正前方 (Y=-0.515m) 平滑向外推开！
    # - 平铺展开到左右外侧 (世界 X = ±[2.0m, 3.0m])！
    # -------------------------------------------------------------------------
    for c in [l_ctrl, r_ctrl]:
        sgn = c['side_sign']
        
        c['ctrl_rod_in'].location.x = 0.0
        c['ctrl_rod_in'].keyframe_insert(data_path="location", index=0, frame=200)
        
        c['ctrl_slide'].location.x = -sgn * 0.50
        c['ctrl_slide'].keyframe_insert(data_path="location", index=0, frame=200)
        
        # 完整向外翻转整整 180 度！
        c['ctrl_flip'].rotation_euler.z = sgn * math.radians(180.0)
        c['ctrl_flip'].keyframe_insert(data_path="rotation_euler", index=2, frame=200)
        
        c['ctrl_rod_out'].location.x = 0.0
        c['ctrl_rod_out'].keyframe_insert(data_path="location", index=0, frame=200)
        
        c['ctrl_fold'].rotation_euler.z = 0.0
        c['ctrl_fold'].keyframe_insert(data_path="rotation_euler", index=2, frame=200)

    cam_data.ortho_scale = 6.20
    cam_data.keyframe_insert(data_path="ortho_scale", frame=200)

    # -------------------------------------------------------------------------
    # 【阶段三：带有金属框架的衍生杆向外衍生伸出】 (Frame 201 ~ 280)
    # - 翻转 180° 完成后，金属框架衍生套杆带着外端 C 型端头卡槽向外侧横向伸出 1000mm！
    # - 左侧正 C 卡槽被推至世界 X = -4.0m；右侧反 C 卡槽被推至世界 X = +4.0m！
    # - 形成极限外挂导轨！
    # -------------------------------------------------------------------------
    for c in [l_ctrl, r_ctrl]:
        sgn = c['side_sign']
        
        c['ctrl_rod_in'].location.x = 0.0
        c['ctrl_rod_in'].keyframe_insert(data_path="location", index=0, frame=280)
        
        c['ctrl_slide'].location.x = -sgn * 0.50
        c['ctrl_slide'].keyframe_insert(data_path="location", index=0, frame=280)
        
        c['ctrl_flip'].rotation_euler.z = sgn * math.radians(180.0)
        c['ctrl_flip'].keyframe_insert(data_path="rotation_euler", index=2, frame=280)
        
        # 衍生套杆向外伸出 1.0m (带着 C 型限位卡槽到达外边界)
        c['ctrl_rod_out'].location.x = -sgn * 1.00
        c['ctrl_rod_out'].keyframe_insert(data_path="location", index=0, frame=280)
        
        c['ctrl_fold'].rotation_euler.z = 0.0
        c['ctrl_fold'].keyframe_insert(data_path="rotation_euler", index=2, frame=280)
        
    cam_data.ortho_scale = 7.20
    cam_data.keyframe_insert(data_path="ortho_scale", frame=280)

    # -------------------------------------------------------------------------
    # 【阶段四 A：两侧黑板整体沿衍生杆向外移动到边界，被 C 型卡槽卡住！】 (Frame 281 ~ 350)
    # - 双层黑板沿伸出的金属框架滑动至最外边界 (移动 1000mm)
    # - 滑块前端精准扎入 C 型限位卡槽内牢牢卡住！
    # - 处于世界 X = ±[3.0m, 4.0m]！
    # - 在内侧世界 X = ±[2.0m, 3.0m] 留下刚刚移动产生的 1000mm 空缺！
    # -------------------------------------------------------------------------
    for c in [l_ctrl, r_ctrl]:
        sgn = c['side_sign']
        
        c['ctrl_rod_in'].location.x = 0.0
        c['ctrl_rod_in'].keyframe_insert(data_path="location", index=0, frame=350)
        
        # 滑块滑至外端边界：位置变为 -sgn*1.5m (卡入 C 型卡槽)
        c['ctrl_slide'].location.x = -sgn * 1.50
        c['ctrl_slide'].keyframe_insert(data_path="location", index=0, frame=350)
        
        c['ctrl_flip'].rotation_euler.z = sgn * math.radians(180.0)
        c['ctrl_flip'].keyframe_insert(data_path="rotation_euler", index=2, frame=350)
        
        c['ctrl_rod_out'].location.x = -sgn * 1.00
        c['ctrl_rod_out'].keyframe_insert(data_path="location", index=0, frame=350)
        
        # 前层折叠板此时仍贴合在后板前面
        c['ctrl_fold'].rotation_euler.z = 0.0
        c['ctrl_fold'].keyframe_insert(data_path="rotation_euler", index=2, frame=350)

    # -------------------------------------------------------------------------
    # 【阶段四 B：从正前方书页式翻折过来！绝不从后面翻动！】 (Frame 351 ~ 430)
    # 【核心修复】: 
    #   旋转角设为 -sgn * 180°！
    #   确保中间半圆弧轨迹严格处于世界 Y = -0.471m (面向镜头、面向学生的正前方空间)！
    #   像翻开书页一样从正前方优美翻过来，平铺落入世界 X = ±[2.0m, 3.0m] 空缺！
    # -------------------------------------------------------------------------
    for c in [l_ctrl, r_ctrl]:
        sgn = c['side_sign']
        
        c['ctrl_rod_in'].location.x = 0.0
        c['ctrl_rod_in'].keyframe_insert(data_path="location", index=0, frame=430)
        
        c['ctrl_slide'].location.x = -sgn * 1.50
        c['ctrl_slide'].keyframe_insert(data_path="location", index=0, frame=430)
        
        c['ctrl_flip'].rotation_euler.z = sgn * math.radians(180.0)
        c['ctrl_flip'].keyframe_insert(data_path="rotation_euler", index=2, frame=430)
        
        c['ctrl_rod_out'].location.x = -sgn * 1.00
        c['ctrl_rod_out'].keyframe_insert(data_path="location", index=0, frame=430)
        
        # 【从正前方翻过来】：角度符号设为 -sgn * 180°，确保轨迹 Y 为负值 (面向镜头正前方)！
        c['ctrl_fold'].rotation_euler.z = -sgn * math.radians(180.0)
        c['ctrl_fold'].keyframe_insert(data_path="rotation_euler", index=2, frame=430)
        
    cam_data.ortho_scale = 8.60
    cam_data.keyframe_insert(data_path="ortho_scale", frame=430)

    # -------------------------------------------------------------------------
    # 【阶段五：8000mm 满幅全景巨幕定格与展示】 (Frame 431 ~ 480)
    # - 保持最终完美的 8 米满幅无缝连贯黑板+大屏状态
    # -------------------------------------------------------------------------
    for c in [l_ctrl, r_ctrl]:
        sgn = c['side_sign']
        c['ctrl_rod_in'].keyframe_insert(data_path="location", index=0, frame=480)
        c['ctrl_slide'].keyframe_insert(data_path="location", index=0, frame=480)
        c['ctrl_flip'].keyframe_insert(data_path="rotation_euler", index=2, frame=480)
        c['ctrl_rod_out'].keyframe_insert(data_path="location", index=0, frame=480)
        c['ctrl_fold'].keyframe_insert(data_path="rotation_euler", index=2, frame=480)
        
        # 设置贝塞尔曲线平滑
        for obj in [c['ctrl_rod_in'], c['ctrl_slide'], c['ctrl_flip'], c['ctrl_rod_out'], c['ctrl_fold']]:
            set_bezier_interpolation(obj)
            
    cam_data.keyframe_insert(data_path="ortho_scale", frame=480)
    set_bezier_interpolation(cam_obj)
    
    print(">> [Keyframes] 480 帧完整动力学关键帧与 Bezier 平滑曲线全部注入完毕！")
    
    # -------------------------------------------------------------------------
    # 5. 保存 vi4.blend 工程母本文件 (严格遵从用户指令：不渲染视频，供用户进文件审阅)
    # -------------------------------------------------------------------------
    vi4_blend_path = os.path.join(output_dir, "vi4.blend")
    bpy.ops.wm.save_as_mainfile(filepath=vi4_blend_path)
    print(f">> [Master Saved] 成功保存全新动画母本文件: {vi4_blend_path}")
    
    return vi4_blend_path

def main():
    print("=" * 75)
    print(">> [Init] 启动第三代（VI4系列）正前方翻折与零穿模关键帧动画母本构建工程...")
    print("=" * 75)
    
    output_dir = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\VI系列"
    os.makedirs(output_dir, exist_ok=True)
    
    reset_scene()
    setup_render_settings()
    build_vi4_animation_scene(output_dir)
    
    print("=" * 75)
    print(">> [Complete] vi4.blend 已成功落盘！未触发视频渲染，已准备好供用户检验关键帧。")
    print("=" * 75)

if __name__ == '__main__':
    main()
