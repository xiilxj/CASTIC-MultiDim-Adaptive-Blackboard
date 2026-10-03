# -*- coding: utf-8 -*-
"""
========================================================================================
第42届瑞安市青少年科技创新大赛 (CASTIC) 参赛重点攻坚工程
项目名称: 第三代多维叠合翻转全覆盖与三维自洁侧滑智能黑板系统
模块名称: S系列 - 真实物理色彩与光学对齐终极脚本 (v3.0 像素采样标定版)
审核标识: 第 21 轮工程技术审核
========================================================================================
像素级真实色彩标定数据 (严格基于 17 原图像素采样):
  1. 墨绿黑板板面: sRGB [65, 105, 81] (#416951) -> 线性 Base Color (0.052, 0.145, 0.085, 1.0)
  2. 86寸大屏天青蓝: sRGB [81, 130, 170] (#5182aa) -> 线性 Base Color (0.082, 0.228, 0.405, 1.0)
  3. 上方大屏高光斑: sRGB [226, 227, 228] (#e2e3e4)
  4. 阳极氧化铝包边: sRGB [199, 200, 202] (#c7c8ca) -> Metallic 0.95, Roughness 0.18
  5. 视口背景工业深灰: sRGB [58, 58, 58] (#3a3a3a) -> World Background 0.045
  6. 遮阳板彻底放平压死 (0° 水平向前平整探出)，大屏水平放正，S1 彻底隐藏副板
========================================================================================
"""

import bpy
import bmesh
import math
import os
import sys

print("====================================================================")
print(">>> 开始执行: S系列色彩精准标定构建与物理光追出图 v3.0 <<<")
print(">>> 审核标识: 第 21 轮工程技术审核 <<<")
print("====================================================================")

def set_obj_hierarchy_visibility(obj, visible=True):
    if obj is None:
        return
    obj.hide_render = not visible
    obj.hide_viewport = not visible
    for child in obj.children:
        set_obj_hierarchy_visibility(child, visible)

def init_clean_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0
    scene.unit_settings.length_unit = 'MILLIMETERS'
    
    scene.render.engine = 'CYCLES'
    try:
        cycles = scene.cycles
        cycles.samples = 64
        cycles.preview_samples = 16
        cycles.use_denoising = True
        cycles.denoiser = 'OPENIMAGEDENOISE'
    except Exception as e:
        print(f"Cycles 配置提示: {e}")
        
    scene.view_settings.view_transform = 'Filmic'
    scene.view_settings.look = 'Medium High Contrast'
    scene.view_settings.exposure = 0.0
    
    # 严格匹配 17 原版视口灰背景 sRGB [58, 58, 58] (#3a3a3a)
    world = bpy.data.worlds.new("S_Series_World_v3")
    scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs['Color'].default_value = (0.045, 0.045, 0.045, 1.0) # 对应屏幕显示约 RGB 58
        bg_node.inputs['Strength'].default_value = 1.0
    print("[1/5] 场景环境与真实视口灰背景配置就绪。")

def build_calibrated_materials():
    materials = {}
    
    def create_pbr(name, base_color, metallic=0.0, roughness=0.5, specular=0.5):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        out = nodes.new(type='ShaderNodeOutputMaterial')
        out.location = (400, 0)
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf.location = (0, 0)
        
        bsdf.inputs['Base Color'].default_value = base_color
        bsdf.inputs['Metallic'].default_value = metallic
        bsdf.inputs['Roughness'].default_value = roughness
        
        if 'Specular IOR Level' in bsdf.inputs:
            bsdf.inputs['Specular IOR Level'].default_value = specular
        elif 'Specular' in bsdf.inputs:
            bsdf.inputs['Specular'].default_value = specular
            
        links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
        return mat

    # 1. 经典沉稳深墨绿黑板 (精确匹配原图采样 sRGB [65, 105, 81] #416951)
    materials['blackboard_green'] = create_pbr(
        name="Mat_Blackboard_Green_Calibrated",
        base_color=(0.052, 0.145, 0.085, 1.0),
        metallic=0.01,
        roughness=0.55,
        specular=0.35
    )
    
    # 2. 阳极氧化亮银铝合金细包边 (匹配采样 sRGB [199, 200, 202] #c7c8ca)
    materials['aluminum_bezel'] = create_pbr(
        name="Mat_Aluminum_Bezel_Calibrated",
        base_color=(0.58, 0.59, 0.60, 1.0),
        metallic=0.96,
        roughness=0.16,
        specular=0.98
    )
    
    # 3. 镀铬镜面小圆钮手柄
    materials['chrome_handle'] = create_pbr(
        name="Mat_Chrome_Handle_Calibrated",
        base_color=(0.95, 0.95, 0.98, 1.0),
        metallic=1.0,
        roughness=0.08,
        specular=1.0
    )
    
    # 4. 86寸液晶大屏 (精确匹配原图采样 sRGB [81, 130, 170] #5182aa + 玻璃高光)
    mat_screen = bpy.data.materials.new(name="Mat_Screen_Display_Calibrated")
    mat_screen.use_nodes = True
    s_nodes = mat_screen.node_tree.nodes
    s_links = mat_screen.node_tree.links
    s_nodes.clear()
    s_out = s_nodes.new(type='ShaderNodeOutputMaterial')
    s_out.location = (600, 0)
    s_bsdf = s_nodes.new(type='ShaderNodeBsdfPrincipled')
    s_bsdf.location = (200, 0)
    
    # 大屏采用纯正清亮天青蓝底色 (辅以微自发光与镜面高光，杜绝冲蚀发白)
    s_bsdf.inputs['Base Color'].default_value = (0.082, 0.228, 0.405, 1.0) # 采样真实蓝
    if 'Emission Color' in s_bsdf.inputs:
        s_bsdf.inputs['Emission Color'].default_value = (0.082, 0.228, 0.405, 1.0)
        s_bsdf.inputs['Emission Strength'].default_value = 0.20 # 轻微发光，不破坏高光对比
    s_bsdf.inputs['Roughness'].default_value = 0.10
    if 'Specular IOR Level' in s_bsdf.inputs:
        s_bsdf.inputs['Specular IOR Level'].default_value = 0.95
    elif 'Specular' in s_bsdf.inputs:
        s_bsdf.inputs['Specular'].default_value = 0.95
        
    s_links.new(s_bsdf.outputs['BSDF'], s_out.inputs['Surface'])
    materials['screen_display'] = mat_screen
    
    # 5. 遮阳挑檐顶盖 (深深灰吸光涂层)
    materials['canopy_dark'] = create_pbr(
        name="Mat_Canopy_Dark_Calibrated",
        base_color=(0.06, 0.07, 0.08, 1.0),
        metallic=0.75,
        roughness=0.45,
        specular=0.5
    )
    
    # 6. 外侧副书写白板 (象牙白漫反射)
    materials['sub_whiteboard'] = create_pbr(
        name="Mat_Sub_Whiteboard_Calibrated",
        base_color=(0.85, 0.86, 0.88, 1.0),
        metallic=0.01,
        roughness=0.36,
        specular=0.4
    )
    
    # 7. 滑轨主横梁型材 (深灰工业氧化铝)
    materials['track_frame'] = create_pbr(
        name="Mat_Track_Frame_Calibrated",
        base_color=(0.10, 0.11, 0.12, 1.0),
        metallic=0.85,
        roughness=0.30,
        specular=0.7
    )
    
    # 8. 垂直刚性连接杆与定位销 (工程高亮橙色)
    materials['link_rod_orange'] = create_pbr(
        name="Mat_Link_Rod_Orange_Calibrated",
        base_color=(0.92, 0.52, 0.08, 1.0),
        metallic=0.88,
        roughness=0.22,
        specular=0.9
    )
    
    # 9. 伸缩延伸滑套平行双圆管
    materials['ext_rail_steel'] = create_pbr(
        name="Mat_Ext_Rail_Steel_Calibrated",
        base_color=(0.78, 0.80, 0.82, 1.0),
        metallic=0.98,
        roughness=0.15,
        specular=0.98
    )

    print("[2/5] 像素采样标定材质编译完毕 (大屏天青蓝 #5182aa、墨绿黑板 #416951 就绪)。")
    return materials

def create_board_with_aluminum_bezel(name, width, height, thickness, bezel_width, mat_face, mat_bezel, has_knob=False, knob_side='right', materials=None):
    collection = bpy.context.scene.collection
    root = bpy.data.objects.new(name, None)
    root.empty_display_type = 'PLAIN_AXES'
    root.empty_display_size = 0.1
    collection.objects.link(root)
    
    # 主板面
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    face_obj = bpy.context.active_object
    face_obj.name = f"{name}_Face"
    face_obj.scale = (width, thickness, height)
    face_obj.location = (0, 0, 0)
    face_obj.data.materials.append(mat_face)
    face_obj.parent = root
    
    # 铝合金细窄包边 (微凸出板面 0.8mm)
    bw = bezel_width
    bt = thickness * 1.20
    for b_name, b_loc, b_scale in [
        ("Top", (0, 0, height/2 + bw/2), (width + 2*bw, bt, bw)),
        ("Bot", (0, 0, -height/2 - bw/2), (width + 2*bw, bt, bw)),
        ("Left", (-width/2 - bw/2, 0, 0), (bw, bt, height + 2*bw)),
        ("Right", (width/2 + bw/2, 0, 0), (bw, bt, height + 2*bw))
    ]:
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        b_obj = bpy.context.active_object
        b_obj.name = f"{name}_Bezel_{b_name}"
        b_obj.scale = b_scale
        b_obj.location = b_loc
        b_obj.data.materials.append(mat_bezel)
        b_obj.parent = root
        
    # 圆钮拉手 (靠中大屏侧垂直偏下)
    if has_knob and materials:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.020, vertices=32)
        knob = bpy.context.active_object
        knob.name = f"{name}_Knob"
        knob.rotation_euler = (math.radians(90), 0, 0)
        kx = (width/2 - 0.045) if knob_side == 'right' else (-width/2 + 0.045)
        knob.location = (kx, -thickness/2 - 0.010, -height * 0.13)
        knob.data.materials.append(materials['chrome_handle'])
        knob.parent = root
        
    return root

def create_screen_and_flat_canopy(name, width, height, materials):
    collection = bpy.context.scene.collection
    screen_root = bpy.data.objects.new(name, None)
    screen_root.empty_display_type = 'PLAIN_AXES'
    screen_root.empty_display_size = 0.15
    collection.objects.link(screen_root)
    
    # 1. 86寸液晶面板
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    panel = bpy.context.active_object
    panel.name = f"{name}_Panel"
    panel.scale = (width, 0.02, height)
    panel.location = (0, 0, 0)
    panel.data.materials.append(materials['screen_display'])
    panel.parent = screen_root
    
    # 2. 大屏窄外框 (深色内嵌立体边框)
    bw = 0.020
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    frame = bpy.context.active_object
    frame.name = f"{name}_OuterFrame"
    frame.scale = (width + 2*bw, 0.045, height + 2*bw)
    frame.location = (0, -0.003, 0) # 向前凸出 3mm 勾勒清晰黑灰边框
    frame.data.materials.append(materials['track_frame'])
    frame.parent = screen_root
    
    # 3. 顶置遮阳盖板 (Canopy) - 彻底放平压死 (rotation = 0°)，与顶梁严格平行！
    canopy_pivot = bpy.data.objects.new(f"{name}_Canopy_Pivot", None)
    canopy_pivot.empty_display_type = 'SINGLE_ARROW'
    canopy_pivot.empty_display_size = 0.1
    canopy_pivot.location = (0, 0, height/2 + bw)
    collection.objects.link(canopy_pivot)
    canopy_pivot.parent = screen_root
    
    canopy_w = width + 2*bw + 0.04
    canopy_depth = 0.30
    canopy_th = 0.014
    
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    canopy_mesh = bpy.context.active_object
    canopy_mesh.name = f"{name}_Canopy_Body"
    canopy_mesh.scale = (canopy_w, canopy_depth, canopy_th)
    canopy_mesh.location = (0, -canopy_depth/2, canopy_th/2)
    canopy_mesh.data.materials.append(materials['canopy_dark'])
    canopy_mesh.parent = canopy_pivot
    
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    canopy_edge = bpy.context.active_object
    canopy_edge.name = f"{name}_Canopy_Edge"
    canopy_edge.scale = (canopy_w, 0.014, canopy_th*1.4)
    canopy_edge.location = (0, -canopy_depth, canopy_th/2)
    canopy_edge.data.materials.append(materials['aluminum_bezel'])
    canopy_edge.parent = canopy_pivot
    
    # 遮阳板彻底放平压死
    canopy_pivot.rotation_euler = (0, 0, 0)
    
    return screen_root, canopy_pivot

def build_single_s_system(system_name, base_z, materials):
    collection = bpy.context.scene.collection
    sys_root = bpy.data.objects.new(system_name, None)
    sys_root.location = (0, 0, base_z)
    collection.objects.link(sys_root)
    
    screen_w, screen_h = 1.90, 1.08
    board_w, board_h = 0.98, 1.06
    board_th = 0.024
    bezel_w = 0.015
    rail_total_w = 4.0
    rail_h = 0.055
    rail_d = 0.075
    
    # 1. 上下主滑轨横梁
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    top_rail = bpy.context.active_object
    top_rail.name = f"{system_name}_Top_Rail"
    top_rail.scale = (rail_total_w, rail_d, rail_h)
    top_rail.location = (0, 0.02, screen_h/2 + rail_h/2 + 0.01)
    top_rail.data.materials.append(materials['track_frame'])
    top_rail.parent = sys_root
    
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    bot_rail = bpy.context.active_object
    bot_rail.name = f"{system_name}_Bot_Rail"
    bot_rail.scale = (rail_total_w, rail_d, rail_h)
    bot_rail.location = (0, 0.02, -screen_h/2 - rail_h/2 - 0.01)
    bot_rail.data.materials.append(materials['track_frame'])
    bot_rail.parent = sys_root
    
    # 2. 中置大屏 (屏幕水平放正，绝对不滚转倾斜！)
    screen_unit, canopy_pivot = create_screen_and_flat_canopy(
        name=f"{system_name}_Display",
        width=screen_w,
        height=screen_h,
        materials=materials
    )
    screen_unit.parent = sys_root
    screen_unit.rotation_euler = (0, 0, 0)
    
    # 3. 左右主墨绿黑板
    left_board = create_board_with_aluminum_bezel(
        name=f"{system_name}_MainBoard_Left",
        width=board_w,
        height=board_h,
        thickness=board_th,
        bezel_width=bezel_w,
        mat_face=materials['blackboard_green'],
        mat_bezel=materials['aluminum_bezel'],
        has_knob=True,
        knob_side='right',
        materials=materials
    )
    left_board.parent = sys_root
    
    right_board = create_board_with_aluminum_bezel(
        name=f"{system_name}_MainBoard_Right",
        width=board_w,
        height=board_h,
        thickness=board_th,
        bezel_width=bezel_w,
        mat_face=materials['blackboard_green'],
        mat_bezel=materials['aluminum_bezel'],
        has_knob=True,
        knob_side='left',
        materials=materials
    )
    right_board.parent = sys_root
    
    # 4. 右侧对接垂直导向条 (橙金色)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    guide_bar = bpy.context.active_object
    guide_bar.name = f"{system_name}_Guide_Bar_Orange"
    guide_bar.scale = (0.018, board_th*1.1, board_h)
    guide_bar.location = (screen_w/2 + 0.01, 0, 0)
    guide_bar.data.materials.append(materials['link_rod_orange'])
    guide_bar.parent = sys_root
    
    # 5. 伸缩延伸双圆管
    ext_rails = []
    for side_sign, side_name in [(-1, "Left"), (1, "Right")]:
        for tb_sign, tb_name in [(1, "Top"), (-1, "Bot")]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.010, depth=1.45, vertices=24)
            rod = bpy.context.active_object
            rod.name = f"{system_name}_ExtRod_{side_name}_{tb_name}"
            rod.rotation_euler = (0, math.radians(90), 0)
            rod.location = (side_sign * (rail_total_w/2 + 0.36), 0.02, tb_sign * (screen_h/2 + 0.01))
            rod.data.materials.append(materials['ext_rail_steel'])
            rod.parent = sys_root
            ext_rails.append(rod)
            
    # 右端垂直拉杆 (工程高亮橙色)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    end_bar = bpy.context.active_object
    end_bar.name = f"{system_name}_End_Lock_Bar_Right"
    end_bar.scale = (0.024, 0.034, screen_h + 0.08)
    end_bar.location = (rail_total_w/2 + 1.08, 0.02, 0)
    end_bar.data.materials.append(materials['link_rod_orange'])
    end_bar.parent = sys_root
    
    # 6. 两翼外侧副板
    left_sub = create_board_with_aluminum_bezel(
        name=f"{system_name}_SubBoard_Left",
        width=board_w,
        height=board_h,
        thickness=board_th * 0.85,
        bezel_width=bezel_w,
        mat_face=materials['sub_whiteboard'],
        mat_bezel=materials['aluminum_bezel'],
        has_knob=False,
        materials=materials
    )
    left_sub.parent = sys_root
    
    right_sub = create_board_with_aluminum_bezel(
        name=f"{system_name}_SubBoard_Right",
        width=board_w,
        height=board_h,
        thickness=board_th * 0.85,
        bezel_width=bezel_w,
        mat_face=materials['sub_whiteboard'],
        mat_bezel=materials['aluminum_bezel'],
        has_knob=False,
        materials=materials
    )
    right_sub.parent = sys_root
    
    main_offset_x = screen_w/2 + board_w/2 + bezel_w
    left_board.location = (-main_offset_x, 0, 0)
    right_board.location = (main_offset_x, 0, 0)
    left_sub.location = (-main_offset_x - board_w - 2*bezel_w, 0, 0)
    right_sub.location = (main_offset_x + board_w + 2*bezel_w, 0, 0)
    
    return {
        'root': sys_root,
        'screen': screen_unit,
        'canopy': canopy_pivot,
        'left_main': left_board,
        'right_main': right_board,
        'left_sub': left_sub,
        'right_sub': right_sub,
        'end_bar': end_bar,
        'guide_bar': guide_bar,
        'screen_w': screen_w,
        'board_w': board_w,
        'bezel_w': bezel_w
    }

def build_s_series_dual_master_v3(materials):
    top_sys = build_single_s_system("Top_S3", base_z=0.72, materials=materials)
    bot_sys = build_single_s_system("Bot_S3", base_z=-0.72, materials=materials)
    
    bpy.ops.mesh.primitive_torus_add(major_radius=0.038, minor_radius=0.0035, location=(0, 0, 0))
    cursor = bpy.context.active_object
    cursor.name = "Viewport_3DCursor_Torus_S3"
    c_mat = bpy.data.materials.new(name="Mat_Cursor_S3")
    c_mat.use_nodes = True
    c_bsdf = c_mat.node_tree.nodes.get("Principled BSDF")
    if c_bsdf:
        c_bsdf.inputs['Base Color'].default_value = (0.9, 0.2, 0.2, 1.0)
    cursor.data.materials.append(c_mat)
    
    return top_sys, bot_sys

# --------------------------------------------------------------------------------------
# 5. 精准物理灯光: 在上方大屏正中央上方打出原图采样正圆高光斑 (#e2e3e4)
# --------------------------------------------------------------------------------------
def setup_calibrated_lighting():
    col = bpy.context.scene.collection
    
    # 1. 模拟大屏正中上方圆润高光斑 (Spot 聚光灯，高聚光束直射上方大屏)
    spot_screen = bpy.data.lights.new(name="Light_Screen_Spot", type='SPOT')
    spot_screen.energy = 650.0
    spot_screen.spot_size = math.radians(24.0)
    spot_screen.spot_blend = 0.35
    spot_screen.color = (1.0, 1.0, 1.0)
    spot_screen_obj = bpy.data.objects.new("Light_Screen_Spot", spot_screen)
    spot_screen_obj.location = (0.12, -2.1, 0.96) # 正照上方大屏中央偏上
    spot_screen_obj.rotation_euler = (math.radians(16), math.radians(3), 0)
    col.objects.link(spot_screen_obj)
    
    # 2. 模拟右侧黑板上的柔和漫反射光斑
    spot_board = bpy.data.lights.new(name="Light_Board_Spot", type='SPOT')
    spot_board.energy = 220.0
    spot_board.spot_size = math.radians(28.0)
    spot_board.spot_blend = 0.50
    spot_board.color = (1.0, 1.0, 1.0)
    spot_board_obj = bpy.data.objects.new("Light_Board_Spot", spot_board)
    spot_board_obj.location = (1.45, -2.3, 0.75)
    spot_board_obj.rotation_euler = (math.radians(15), math.radians(-8), 0)
    col.objects.link(spot_board_obj)
    
    # 3. 柔和正面补光
    front_fill = bpy.data.lights.new(name="Light_Front_Fill", type='AREA')
    front_fill.energy = 70.0
    front_fill.size = 5.4
    front_fill.size_y = 3.6
    front_fill.color = (0.96, 0.98, 1.0)
    front_fill_obj = bpy.data.objects.new("Light_Front_Fill", front_fill)
    front_fill_obj.location = (0, -3.6, 0)
    front_fill_obj.rotation_euler = (math.radians(90), 0, 0)
    col.objects.link(front_fill_obj)
    
    print("[3/5] 精准物理照明配置完毕 (大屏正中高光球与黑板漫射光晕就绪)。")

# --------------------------------------------------------------------------------------
# 6. S 系列渲染出图: 严格使用 17 原版纵横比与安全覆盖机制
# --------------------------------------------------------------------------------------
def render_s_series_v3(top_sys, bot_sys, output_dir):
    scene = bpy.context.scene
    
    cam_data = bpy.data.cameras.new("S_Series_Camera_v3")
    cam_data.type = 'ORTHO'
    cam_obj = bpy.data.objects.new("S_Series_Camera_v3", cam_data)
    cam_obj.location = (0, -4.5, 0)
    cam_obj.rotation_euler = (math.radians(90), 0, 0)
    bpy.context.scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_depth = '8'
    scene.render.image_settings.compression = 15
    
    screen_w = top_sys['screen_w']
    board_w = top_sys['board_w']
    bezel_w = top_sys['bezel_w']
    main_offset_x = screen_w/2 + board_w/2 + bezel_w
    
    tasks = [
        # S1: 对齐 media__1783170868851.png (画幅紧凑长宽比约 1.48:1)
        {
            "name": "S1.png",
            "res_x": 3550,
            "res_y": 2390,
            "ortho_scale": 4.55,
            "setup": lambda: setup_s1_v3(top_sys, bot_sys, main_offset_x)
        },
        # S2: 对齐 media__1783170884236.png (副白板完全水平平展，画幅长宽比约 2:1)
        {
            "name": "S2.png",
            "res_x": 3840,
            "res_y": 1920,
            "ortho_scale": 6.30,
            "setup": lambda: setup_s2_v3(top_sys, bot_sys, main_offset_x, board_w, bezel_w)
        },
        # S3: 对齐 media__1783170899258.png (副白板绕垂直轴向前折叠 28°，底边严格保持水平)
        {
            "name": "S3.png",
            "res_x": 3840,
            "res_y": 2120,
            "ortho_scale": 6.25,
            "setup": lambda: setup_s3_v3(top_sys, bot_sys, main_offset_x, board_w, bezel_w)
        },
        # S4: 对齐 media__1783170944637.png (双横梁套杆外滑，外侧副板为墨绿板，右下橙色拉杆)
        {
            "name": "S4.png",
            "res_x": 3840,
            "res_y": 1520,
            "ortho_scale": 6.90,
            "setup": lambda: setup_s4_v3(top_sys, bot_sys, main_offset_x, board_w, bezel_w)
        },
        # S5: 对齐 media__1783170957959.png (极限全开露大屏，外侧全绿板扩展)
        {
            "name": "S5.png",
            "res_x": 3840,
            "res_y": 1520,
            "ortho_scale": 6.90,
            "setup": lambda: setup_s5_v3(top_sys, bot_sys, main_offset_x, board_w, bezel_w)
        }
    ]
    
    print("[4/5] 开始执行 S 系列 v3.0 物理色彩标定出图...")
    for idx, t in enumerate(tasks, 1):
        print(f"\n>>> [{idx}/5] 正在渲染: {t['name']}")
        scene.render.resolution_x = t['res_x']
        scene.render.resolution_y = t['res_y']
        cam_data.ortho_scale = t['ortho_scale']
        t['setup']()
        filepath = os.path.join(output_dir, t['name'])
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                pass
        scene.render.filepath = filepath
        bpy.ops.render.render(write_still=True)
        print(f"    --> [OK] 渲染完成并已保存: {filepath}")

def setup_s1_v3(top, bot, main_offset_x):
    """S1: 遮阳板彻底放平压死，大屏绝对水平放正零歪斜，两翼副板彻底递归隐藏"""
    set_obj_hierarchy_visibility(top['left_sub'], False)
    set_obj_hierarchy_visibility(top['right_sub'], False)
    set_obj_hierarchy_visibility(bot['left_sub'], False)
    set_obj_hierarchy_visibility(bot['right_sub'], False)
    
    top['left_main'].location = (-main_offset_x, 0, 0)
    top['right_main'].location = (main_offset_x, 0, 0)
    bot['left_main'].location = (-main_offset_x, 0, 0)
    bot['right_main'].location = (main_offset_x, 0, 0)
    
    top['canopy'].rotation_euler = (0, 0, 0)
    top['screen'].rotation_euler = (0, 0, 0)
    bot['canopy'].rotation_euler = (0, 0, 0)
    bot['screen'].rotation_euler = (0, 0, 0)

def setup_s2_v3(top, bot, main_offset_x, board_w, bezel_w):
    """S2: 副白板水平平铺展开"""
    set_obj_hierarchy_visibility(top['left_sub'], True)
    set_obj_hierarchy_visibility(top['right_sub'], True)
    set_obj_hierarchy_visibility(bot['left_sub'], True)
    set_obj_hierarchy_visibility(bot['right_sub'], True)
    
    top['canopy'].rotation_euler = (0, 0, 0)
    top['screen'].rotation_euler = (0, 0, 0)
    bot['canopy'].rotation_euler = (0, 0, 0)
    bot['screen'].rotation_euler = (0, 0, 0)
    
    mat_white = bpy.data.materials.get("Mat_Sub_Whiteboard_Calibrated")
    for s in [top, bot]:
        s['left_sub'].children[0].data.materials[0] = mat_white
        s['right_sub'].children[0].data.materials[0] = mat_white
        sub_x = main_offset_x + board_w + 2*bezel_w
        s['left_sub'].location = (-sub_x, 0, 0)
        s['right_sub'].location = (sub_x, 0, 0)
        s['left_sub'].rotation_euler = (0, 0, 0)
        s['right_sub'].rotation_euler = (0, 0, 0)
        s['left_main'].location.x = -main_offset_x
        s['right_main'].location.x = main_offset_x

def setup_s3_v3(top, bot, main_offset_x, board_w, bezel_w):
    """S3: 副白板向前折叠 28°，底边严格保持水平对齐"""
    set_obj_hierarchy_visibility(top['left_sub'], True)
    set_obj_hierarchy_visibility(top['right_sub'], True)
    set_obj_hierarchy_visibility(bot['left_sub'], True)
    set_obj_hierarchy_visibility(bot['right_sub'], True)
    
    top['canopy'].rotation_euler = (0, 0, 0)
    top['screen'].rotation_euler = (0, 0, 0)
    bot['canopy'].rotation_euler = (0, 0, 0)
    bot['screen'].rotation_euler = (0, 0, 0)
    
    mat_white = bpy.data.materials.get("Mat_Sub_Whiteboard_Calibrated")
    for s in [top, bot]:
        s['left_sub'].children[0].data.materials[0] = mat_white
        s['right_sub'].children[0].data.materials[0] = mat_white
        s['left_main'].location.x = -main_offset_x
        s['right_main'].location.x = main_offset_x
        
        fold_angle = math.radians(28)
        hinge_lx = -main_offset_x - board_w/2 - bezel_w
        hinge_rx = main_offset_x + board_w/2 + bezel_w
        
        s['left_sub'].location = (hinge_lx - (board_w/2) * math.cos(fold_angle), -(board_w/2) * math.sin(fold_angle), 0)
        s['left_sub'].rotation_euler = (0, 0, -fold_angle) # 严格仅绕垂直 Z 轴！
        
        s['right_sub'].location = (hinge_rx + (board_w/2) * math.cos(fold_angle), -(board_w/2) * math.sin(fold_angle), 0)
        s['right_sub'].rotation_euler = (0, 0, fold_angle)

def setup_s4_v3(top, bot, main_offset_x, board_w, bezel_w):
    """S4: 双横梁延伸套杆外滑，外侧副板为墨绿板，右下橙色拉杆"""
    set_obj_hierarchy_visibility(top['left_sub'], True)
    set_obj_hierarchy_visibility(top['right_sub'], True)
    set_obj_hierarchy_visibility(bot['left_sub'], True)
    set_obj_hierarchy_visibility(bot['right_sub'], True)
    
    top['canopy'].rotation_euler = (0, 0, 0)
    top['screen'].rotation_euler = (0, 0, 0)
    bot['canopy'].rotation_euler = (0, 0, 0)
    bot['screen'].rotation_euler = (0, 0, 0)
    
    mat_green = bpy.data.materials.get("Mat_Blackboard_Green_Calibrated")
    for s in [top, bot]:
        s['left_sub'].children[0].data.materials[0] = mat_green
        s['right_sub'].children[0].data.materials[0] = mat_green
        s['left_main'].location.x = -main_offset_x - 0.38
        s['right_main'].location.x = main_offset_x + 0.38
        s['left_sub'].location = (-main_offset_x - board_w - 0.95, 0, 0)
        s['right_sub'].location = (main_offset_x + board_w + 0.95, 0, 0)
        s['left_sub'].rotation_euler = (0, 0, 0)
        s['right_sub'].rotation_euler = (0, 0, 0)

def setup_s5_v3(top, bot, main_offset_x, board_w, bezel_w):
    setup_s4_v3(top, bot, main_offset_x, board_w, bezel_w)

def main():
    s_dir = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\S系列"
    blend_path = os.path.join(s_dir, "S_Series_Master_v3.blend")
    
    init_clean_scene()
    materials = build_calibrated_materials()
    top_sys, bot_sys = build_s_series_dual_master_v3(materials)
    setup_calibrated_lighting()
    
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"--> [OK] S系列色彩标定母本工程已成功保存: {blend_path}")
    
    render_s_series_v3(top_sys, bot_sys, s_dir)
    print("\n[5/5] S系列 v3.0 物理色彩标定出图全部完成！")
    print("====================================================================")

if __name__ == "__main__":
    main()
