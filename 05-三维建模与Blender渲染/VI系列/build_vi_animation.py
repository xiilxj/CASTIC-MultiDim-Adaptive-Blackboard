#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================================================================
第42届瑞安市青少年科技创新大赛 (CASTIC) 参赛重点攻坚工程
工程代号: 第三代（VI系列 / GH-VI-2026）真实物理运动学全流程关键帧动画母本构建脚本
文件路径: D:\\Desktop\\CASTICpjhb\\05-三维建模与Blender渲染\\VI系列\\build_vi_animation.py
审核标识: 第 24 轮工程技术审核
========================================================================================
功能定位:
  严格按照用户确立的底层机构动力学真相，在 Blender 中全自动装配并注入 480 帧关键帧动画：
  1. 墙体基底 (4000mm): 左侧 1m 固定黑板 + 中置 2m 86寸大屏 + 右侧 1m 固定黑板；
  2. 阶段一 (Frame 1~120):
     - 初 (1~40): 绳索杆向内伸出中央碰头，双层黑板沿杆向中滑移闭合，100% 遮蔽中置大屏；
     - 末 (41~120): 双层黑板向两侧外滑退回固定板正前方，绳索杆缩回，大屏完整裸露显现；
  3. 阶段二 (Frame 121~200):
     - 活动框架连同黑板与绳索杆整体绕外侧翻转主轴向外翻动 (Yaw 18° 立体避光)；
  4. 阶段三 (Frame 201~280):
     - 带有金属框架的衍生杆从主滑槽向外侧横向衍生伸出 1000mm；
  5. 阶段四 (Frame 281~430):
     - 4A (281~350): 双层黑板整体沿外侧衍生杆向外滑动到最外端边界；
     - 4B (351~430): 最前面一层折叠板绕内侧铰链向镜头方向朝内翻开 180°，严丝合缝填补 1000mm 空缺！
  6. 阶段五 (Frame 431~480):
     - 呈现 6000mm 满幅全景巨幕定格与镜头微动态环绕。
  母本保存为: vi1.blend (不启动视频渲染，供用户优先交互审阅关键帧与曲线)
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
    world = bpy.data.worlds.new("VI_World")
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
        base_color=(0.052, 0.145, 0.085, 1.0), # #416951
        metallic=0.01,
        roughness=0.55,
        specular=0.35
    )
    mats['aluminum_bezel'] = create_pbr(
        "Mat_Aluminum_Bezel",
        base_color=(0.58, 0.59, 0.60, 1.0), # #c7c8ca
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
    """创建带精致 6063 铝合金边框的黑板网格组件"""
    collection = bpy.context.scene.collection
    root = bpy.data.objects.new(name, None)
    collection.objects.link(root)
    
    inner_w = width - 2 * bezel_w
    inner_h = height - 2 * bezel_w
    
    # 板芯
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    face = bpy.context.active_object
    face.name = f"{name}_Face"
    face.scale = (inner_w, thickness * 0.90, inner_h)
    face.location = (0, 0, 0)
    face.data.materials.append(materials['blackboard_green'])
    face.parent = root
    
    # 边框 (上下左右)
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

def set_bezier_interpolation(obj):
    """将对象的所有动画曲线设置为平滑 Bezier 加减速 (兼容 Blender 5.0 全新 Action 架构)"""
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
        print(f">> [Info] 插值设置跳过或已采用默认Bezier: {e}")

def build_vi1_animation_scene(output_dir):
    """
    核心装配与关键帧全量注入
    """
    scene = bpy.context.scene
    collection = scene.collection
    mats = build_materials()
    
    # 根节点
    sys_root = bpy.data.objects.new("GH_VI_System_Root", None)
    sys_root.location = (0, 0, 0)
    collection.objects.link(sys_root)
    
    # 几何标准参数
    screen_w, screen_h = 2.00, 1.14
    board_w, board_h = 0.99, 1.10
    single_th = 0.012 # 12mm
    bezel_w = 0.015
    rail_total_w = 4.0
    rail_h, rail_d = 0.060, 0.080
    
    # -------------------------------------------------------------------------
    # 1. 后方固定教室墙体基准 (4000mm: 1m固定板 + 2m大屏 + 1m固定板)
    # -------------------------------------------------------------------------
    # (1) 中置 86 寸智能大屏外壳与发光显示屏 (Y = +0.02m)
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
    
    # 遮阳平檐 (0.0° 水平放平，长 2.04m，前挑 140mm)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    canopy = bpy.context.active_object
    canopy.name = "Fixed_Canopy_Flat"
    canopy.scale = (screen_w + 0.04, 0.14, 0.016)
    canopy.location = (0, -0.05, screen_h/2 + 0.01)
    canopy.data.materials.append(mats['canopy_dark'])
    canopy.parent = sys_root
    
    # (2) 左右两侧固定黑板模块 (固定在墙面不动，Y = +0.01m)
    fixed_left = create_board_mesh("Fixed_Wall_Blackboard_Left", board_w, board_h, single_th, bezel_w, mats)
    fixed_left.location = (-1.50, 0.01, 0)
    fixed_left.parent = sys_root
    
    fixed_right = create_board_mesh("Fixed_Wall_Blackboard_Right", board_w, board_h, single_th, bezel_w, mats)
    fixed_right.location = (1.50, 0.01, 0)
    fixed_right.parent = sys_root
    
    # (3) 上下固定 C 型导轨主梁 (长 4000mm，X in [-2.0, +2.0])
    for tb_sign, tb_name in [(1, "Top"), (-1, "Bot")]:
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        rail = bpy.context.active_object
        rail.name = f"Fixed_Main_Rail_{tb_name}"
        rail.scale = (rail_total_w, rail_d, rail_h)
        rail.location = (0, -0.012, tb_sign * (screen_h/2 + rail_h/2 + 0.005))
        rail.data.materials.append(mats['track_frame'])
        rail.parent = sys_root
        
    # -------------------------------------------------------------------------
    # 2. 前方可动总成控制器与机构拓扑 (左右各一套)
    # -------------------------------------------------------------------------
    controllers = {}
    
    for side_name, side_sign in [("Left", -1), ("Right", 1)]:
        # (1) 翻转主铰链控制器 Ctrl_Flip (第二阶段翻转主轴，位于外侧边缘 X = ±2.0m)
        ctrl_flip = bpy.data.objects.new(f"Ctrl_Flip_{side_name}", None)
        ctrl_flip.location = (side_sign * 2.00, -0.015, 0)
        collection.objects.link(ctrl_flip)
        ctrl_flip.parent = sys_root
        
        # 翻转青色五金转轴 (上下两组)
        for h_z in [0.42, -0.42]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.016, depth=0.08, vertices=24)
            h_obj = bpy.context.active_object
            h_obj.name = f"Hinge_Flip_{side_name}_{'Top' if h_z>0 else 'Btm'}"
            h_obj.location = (side_sign * 2.00, -0.015, h_z)
            h_obj.data.materials.append(mats['hinge_cyan'])
            h_obj.parent = sys_root # 固连于基座外缘
            
        # (2) 活动金属支撑框架 Movable_Frame (挂载于 Ctrl_Flip，随动翻转)
        m_frame = bpy.data.objects.new(f"Movable_Frame_{side_name}", None)
        m_frame.location = (-side_sign * 0.50, 0, 0) # 相对主铰链向内 0.5m (常态中心处于 X = ±1.5m)
        collection.objects.link(m_frame)
        m_frame.parent = ctrl_flip
        
        # (3) 阶段一向内碰头伸缩绳索杆 Ctrl_Rod_Inward (相对 Ctrl_Flip 动作)
        # 常态收拢，阶段一初向内伸出 1000mm，在中央 X = 0 处碰头对接
        ctrl_rod_in = bpy.data.objects.new(f"Ctrl_Rod_Inward_{side_name}", None)
        ctrl_rod_in.location = (0, 0, 0)
        collection.objects.link(ctrl_rod_in)
        ctrl_rod_in.parent = ctrl_flip
        
        # 绳索杆物理套管模型 (上下各一根，深灰色精密铝合金)
        for tb_sign, tb_name in [(1, "Top"), (-1, "Bot")]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=1.00, vertices=24)
            r_in_mesh = bpy.context.active_object
            r_in_mesh.name = f"Rod_Inward_Mesh_{side_name}_{tb_name}"
            r_in_mesh.rotation_euler = (0, math.radians(90), 0)
            # 杆件中心在铰链内侧 0.5m，展开时向中心伸至 X=0
            r_in_mesh.location = (-side_sign * 0.50, 0, tb_sign * (screen_h/2 + rail_h/2 + 0.005))
            r_in_mesh.data.materials.append(mats['ext_rail_steel'])
            r_in_mesh.parent = ctrl_rod_in
            
        # (4) 阶段三向外衍生金属框架套杆 Ctrl_Rod_Outward (相对 Ctrl_Flip 动作)
        # 常态收拢在主梁内，阶段三向外横向伸出 1000mm
        ctrl_rod_out = bpy.data.objects.new(f"Ctrl_Rod_Outward_{side_name}", None)
        ctrl_rod_out.location = (0, 0, 0)
        collection.objects.link(ctrl_rod_out)
        ctrl_rod_out.parent = ctrl_flip
        
        for tb_sign, tb_name in [(1, "Top"), (-1, "Bot")]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.014, depth=1.00, vertices=24)
            r_out_mesh = bpy.context.active_object
            r_out_mesh.name = f"Rod_Outward_Mesh_{side_name}_{tb_name}"
            r_out_mesh.rotation_euler = (0, math.radians(90), 0)
            r_out_mesh.location = (side_sign * 0.50, 0, tb_sign * (screen_h/2 + rail_h/2 + 0.005))
            r_out_mesh.data.materials.append(mats['ext_rail_steel'])
            r_out_mesh.parent = ctrl_rod_out
            
        # (5) 双层黑板滑块控制器 Ctrl_Slide (挂载在 Ctrl_Flip 上，可在杆件上横向滑动)
        ctrl_slide = bpy.data.objects.new(f"Ctrl_Slide_{side_name}", None)
        ctrl_slide.location = (-side_sign * 0.50, -0.015, 0) # 初始处于常态中心 X = ±1.5m, Y = -0.030m
        collection.objects.link(ctrl_slide)
        ctrl_slide.parent = ctrl_flip
        
        # 滑块暗装导向滑靴 (上下各一)
        for tb_sign, tb_name in [(1, "Top"), (-1, "Bot")]:
            bpy.ops.mesh.primitive_cube_add(size=1.0)
            sb = bpy.context.active_object
            sb.name = f"Slider_Shoe_{side_name}_{tb_name}"
            sb.scale = (board_w * 0.95, rail_d * 0.55, rail_h * 0.55)
            sb.location = (0, 0, tb_sign * (screen_h/2 + rail_h/2 + 0.005))
            sb.data.materials.append(mats['track_frame'])
            sb.parent = ctrl_slide
            
        # (6) 后层承重黑板 (双层黑板之后板，12mm，固连于滑动控制器)
        back_board = create_board_mesh(f"Back_Main_Board_{side_name}", board_w, board_h, single_th, bezel_w, mats)
        back_board.location = (0, 0, 0)
        back_board.parent = ctrl_slide
        
        # (7) 内侧折叠铰链 Ctrl_Fold (第四阶段翻折轴，位于双层黑板靠近大屏的内侧边缘)
        # 相对滑块中心: X = -side_sign * (board_w/2), Y = -0.014m
        ctrl_fold = bpy.data.objects.new(f"Ctrl_Fold_{side_name}", None)
        ctrl_fold.location = (-side_sign * (board_w/2), -0.014, 0)
        collection.objects.link(ctrl_fold)
        ctrl_fold.parent = ctrl_slide # 随滑块移动
        
        # 折叠品红色五金铰链轴 (上下两组)
        for f_z in [0.42, -0.42]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.014, depth=0.08, vertices=24)
            f_obj = bpy.context.active_object
            f_obj.name = f"Hinge_Fold_{side_name}_{'Top' if f_z>0 else 'Btm'}"
            f_obj.location = (-side_sign * (board_w/2), -0.014, f_z)
            f_obj.data.materials.append(mats['hinge_magenta'])
            f_obj.parent = ctrl_slide
            
        # (8) 最前面一层折叠黑板 (前板，12mm，挂载在 Ctrl_Fold 上)
        # 当 Fold=0° 时，前板平贴在后板前方 (相对 Ctrl_Fold 偏移 side_sign * board_w/2, Y = -0.002m)
        front_board = create_board_mesh(f"Front_Folding_Board_{side_name}", board_w, board_h, single_th, bezel_w, mats)
        front_board.location = (side_sign * (board_w/2), -0.002, 0)
        front_board.parent = ctrl_fold
        
        controllers[side_name] = {
            'ctrl_flip': ctrl_flip,
            'ctrl_rod_in': ctrl_rod_in,
            'ctrl_rod_out': ctrl_rod_out,
            'ctrl_slide': ctrl_slide,
            'ctrl_fold': ctrl_fold,
            'side_sign': side_sign,
            'board_w': board_w
        }

    # -------------------------------------------------------------------------
    # 3. 摄像机与照明系统
    # -------------------------------------------------------------------------
    cam_data = bpy.data.cameras.new("VI_Master_Camera_Data")
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = 5.20 # 默认视距
    cam_obj = bpy.data.objects.new("VI_Master_Camera", cam_data)
    cam_obj.location = (0, -4.6, 0)
    cam_obj.rotation_euler = (math.radians(90), 0, 0)
    collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    # 日光与补光
    sun_data = bpy.data.lights.new(name="Sun_VI", type='SUN')
    sun_data.energy = 2.4
    sun_data.color = (1.0, 0.98, 0.95)
    sun_obj = bpy.data.objects.new("Sun_VI", sun_data)
    collection.objects.link(sun_obj)
    sun_obj.location = (-4.0, -5.0, 6.0)
    sun_obj.rotation_euler = (math.radians(45), math.radians(-15), math.radians(35))
    
    fill_data = bpy.data.lights.new(name="Fill_Area_VI", type='AREA')
    fill_data.energy = 150.0
    fill_data.size = 6.0
    fill_obj = bpy.data.objects.new("Fill_Area_VI", fill_data)
    collection.objects.link(fill_obj)
    fill_obj.location = (0, -4.0, 0)
    fill_obj.rotation_euler = (math.radians(90), 0, 0)
    
    # -------------------------------------------------------------------------
    # 4. 关键帧动画全量注入 (480 帧 / 16 秒 / 30 FPS)
    # -------------------------------------------------------------------------
    print(">> [Keyframes] 开始全流程 4 阶段关键帧精准注入...")
    
    l_ctrl = controllers['Left']
    r_ctrl = controllers['Right']
    
    # -------------------------------------------------------------------------
    # 【阶段一初：完全闭合封屏形态】 (Frame 1 ~ 40)
    # - 绳索杆向内伸出对接 (伸出 1000mm)
    # - 双层黑板沿杆向中滑移，100% 遮蔽 86寸大屏
    # - 折叠板保持贴合 (Fold = 0°)
    # - 翻转轴为 0°，外衍生杆为 0m
    # -------------------------------------------------------------------------
    for c in [l_ctrl, r_ctrl]:
        sgn = c['side_sign']
        
        # 1. 内伸绳索杆：伸出 1.0m (相对铰链向中偏 1.0m)
        c['ctrl_rod_in'].location.x = -sgn * 1.00
        c['ctrl_rod_in'].keyframe_insert(data_path="location", index=0, frame=1)
        c['ctrl_rod_in'].keyframe_insert(data_path="location", index=0, frame=40)
        
        # 2. 滑块：向中心滑动 1.0m (相对铰链位移从 -sgn*0.5 变至 -sgn*1.5，世界位置 X = ±0.5m 遮蔽大屏)
        c['ctrl_slide'].location.x = -sgn * 1.50
        c['ctrl_slide'].keyframe_insert(data_path="location", index=0, frame=1)
        c['ctrl_slide'].keyframe_insert(data_path="location", index=0, frame=40)
        
        # 3. 翻转轴：0°
        c['ctrl_flip'].rotation_euler.z = 0.0
        c['ctrl_flip'].keyframe_insert(data_path="rotation_euler", index=2, frame=1)
        c['ctrl_flip'].keyframe_insert(data_path="rotation_euler", index=2, frame=40)
        
        # 4. 外衍生杆：0m
        c['ctrl_rod_out'].location.x = 0.0
        c['ctrl_rod_out'].keyframe_insert(data_path="location", index=0, frame=1)
        c['ctrl_rod_out'].keyframe_insert(data_path="location", index=0, frame=40)
        
        # 5. 折叠板：0° (贴合)
        c['ctrl_fold'].rotation_euler.z = 0.0
        c['ctrl_fold'].keyframe_insert(data_path="rotation_euler", index=2, frame=1)
        c['ctrl_fold'].keyframe_insert(data_path="rotation_euler", index=2, frame=40)
        
    cam_data.ortho_scale = 4.80
    cam_data.keyframe_insert(data_path="ortho_scale", frame=1)
    cam_data.keyframe_insert(data_path="ortho_scale", frame=40)

    # -------------------------------------------------------------------------
    # 【阶段一末：外滑复位露屏形态】 (Frame 41 ~ 120)
    # - 双层黑板向外侧滑动 1.0m，退回到左右固定黑板正前方 (X = ±1.5m)
    # - 绳索杆向外完全缩回 (0m)
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
    # 【阶段二：活动框架整体向外侧翻动】 (Frame 121 ~ 200)
    # - 折叠黑板带着绳索杆作为一个整体，绕外侧轴向两侧翻动 (Yaw 18°)
    # - 立体避光姿态
    # -------------------------------------------------------------------------
    for c in [l_ctrl, r_ctrl]:
        sgn = c['side_sign']
        
        c['ctrl_rod_in'].location.x = 0.0
        c['ctrl_rod_in'].keyframe_insert(data_path="location", index=0, frame=200)
        
        c['ctrl_slide'].location.x = -sgn * 0.50
        c['ctrl_slide'].keyframe_insert(data_path="location", index=0, frame=200)
        
        # 整体向外翻动 18°
        c['ctrl_flip'].rotation_euler.z = sgn * math.radians(18.0)
        c['ctrl_flip'].keyframe_insert(data_path="rotation_euler", index=2, frame=200)
        
        c['ctrl_rod_out'].location.x = 0.0
        c['ctrl_rod_out'].keyframe_insert(data_path="location", index=0, frame=200)
        
        c['ctrl_fold'].rotation_euler.z = 0.0
        c['ctrl_fold'].keyframe_insert(data_path="rotation_euler", index=2, frame=200)

    # -------------------------------------------------------------------------
    # 【阶段三：带有金属框架的衍生杆向外衍生】 (Frame 201 ~ 280)
    # - 金属框架衍生杆从滑槽向外侧横向伸出 1000mm
    # - 保持偏航翻转角度不变
    # -------------------------------------------------------------------------
    for c in [l_ctrl, r_ctrl]:
        sgn = c['side_sign']
        
        c['ctrl_rod_in'].location.x = 0.0
        c['ctrl_rod_in'].keyframe_insert(data_path="location", index=0, frame=280)
        
        c['ctrl_slide'].location.x = -sgn * 0.50
        c['ctrl_slide'].keyframe_insert(data_path="location", index=0, frame=280)
        
        c['ctrl_flip'].rotation_euler.z = sgn * math.radians(18.0)
        c['ctrl_flip'].keyframe_insert(data_path="rotation_euler", index=2, frame=280)
        
        # 外衍生杆伸出 1.0m
        c['ctrl_rod_out'].location.x = sgn * 1.00
        c['ctrl_rod_out'].keyframe_insert(data_path="location", index=0, frame=280)
        
        c['ctrl_fold'].rotation_euler.z = 0.0
        c['ctrl_fold'].keyframe_insert(data_path="rotation_euler", index=2, frame=280)
        
    cam_data.ortho_scale = 5.80
    cam_data.keyframe_insert(data_path="ortho_scale", frame=280)

    # -------------------------------------------------------------------------
    # 【阶段四 A：双层黑板整体沿衍生杆向外移动到边界】 (Frame 281 ~ 350)
    # - 双层黑板沿伸出的金属框架滑动至最外边界 (移动 1000mm)
    # - 在中间留下 1000mm 滑动空缺
    # -------------------------------------------------------------------------
    for c in [l_ctrl, r_ctrl]:
        sgn = c['side_sign']
        
        c['ctrl_rod_in'].location.x = 0.0
        c['ctrl_rod_in'].keyframe_insert(data_path="location", index=0, frame=350)
        
        # 滑块滑至外侧边界：相对铰链从 -sgn*0.5m 变为 +sgn*0.5m (外移 1.0m，世界 X = ±2.5m)
        c['ctrl_slide'].location.x = sgn * 0.50
        c['ctrl_slide'].keyframe_insert(data_path="location", index=0, frame=350)
        
        c['ctrl_flip'].rotation_euler.z = sgn * math.radians(18.0)
        c['ctrl_flip'].keyframe_insert(data_path="rotation_euler", index=2, frame=350)
        
        c['ctrl_rod_out'].location.x = sgn * 1.00
        c['ctrl_rod_out'].keyframe_insert(data_path="location", index=0, frame=350)
        
        # 前层板尚未翻开
        c['ctrl_fold'].rotation_euler.z = 0.0
        c['ctrl_fold'].keyframe_insert(data_path="rotation_euler", index=2, frame=350)

    # -------------------------------------------------------------------------
    # 【阶段四 B：最前面一层绕内侧铰链向镜头方向朝内翻开 180° 填补空缺】 (Frame 351 ~ 430)
    # - 翻转主轴微回平 (Yaw 回到 0°，保持平整板书面)
    # - 前层折叠板绕内侧铰链向前向内翻折 180°
    # - 严丝合缝填补刚才移动留下的 1000mm 空缺！
    # -------------------------------------------------------------------------
    for c in [l_ctrl, r_ctrl]:
        sgn = c['side_sign']
        
        c['ctrl_rod_in'].location.x = 0.0
        c['ctrl_rod_in'].keyframe_insert(data_path="location", index=0, frame=430)
        
        c['ctrl_slide'].location.x = sgn * 0.50
        c['ctrl_slide'].keyframe_insert(data_path="location", index=0, frame=430)
        
        # 翻转轴回平至 0° 平整基准
        c['ctrl_flip'].rotation_euler.z = 0.0
        c['ctrl_flip'].keyframe_insert(data_path="rotation_euler", index=2, frame=430)
        
        c['ctrl_rod_out'].location.x = sgn * 1.00
        c['ctrl_rod_out'].keyframe_insert(data_path="location", index=0, frame=430)
        
        # 最前面一层绕内侧铰链向镜头方向向内翻折 180°！
        # 对于 Right(sgn=1): 绕内侧铰链向内回转 -180°
        # 对于 Left(sgn=-1): 绕内侧铰链向内回转 +180°
        c['ctrl_fold'].rotation_euler.z = -sgn * math.radians(180.0)
        c['ctrl_fold'].keyframe_insert(data_path="rotation_euler", index=2, frame=430)
        
    cam_data.ortho_scale = 6.60
    cam_data.keyframe_insert(data_path="ortho_scale", frame=430)

    # -------------------------------------------------------------------------
    # 【阶段五：6000mm 满幅全景巨幕定格与镜头微环绕】 (Frame 431 ~ 480)
    # - 保持最终完美的 6 米满幅无缝连贯黑板+大屏状态
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
    # 5. 保存 vi1.blend 工程母本文件 (严格遵从用户指令：不直接导出视频，先供用户审阅关键帧)
    # -------------------------------------------------------------------------
    vi1_blend_path = os.path.join(output_dir, "vi1.blend")
    bpy.ops.wm.save_as_mainfile(filepath=vi1_blend_path)
    print(f">> [Master Saved] 成功保存核心动画母本文件: {vi1_blend_path}")
    
    return vi1_blend_path

def main():
    print("=" * 75)
    print(">> [Init] 启动第三代（VI系列）真实运动学全流程关键帧动画母本构建工程...")
    print("=" * 75)
    
    output_dir = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\VI系列"
    os.makedirs(output_dir, exist_ok=True)
    
    reset_scene()
    setup_render_settings()
    build_vi1_animation_scene(output_dir)
    
    print("=" * 75)
    print(">> [Complete] vi1.blend 已成功落盘！未触发视频渲染，已准备好供用户检验关键帧。")
    print("=" * 75)

if __name__ == '__main__':
    main()
