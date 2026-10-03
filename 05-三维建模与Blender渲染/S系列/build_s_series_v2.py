# -*- coding: utf-8 -*-
"""
========================================================================================
第42届瑞安市青少年科技创新大赛 (CASTIC) 参赛重点攻坚工程
项目名称: 第三代多维叠合翻转全覆盖与三维自洁侧滑智能黑板系统
模块名称: S系列 - 机械总装与光环境精修脚本 v2.0 (遮阳板压平绝不歪斜、全要素精准对齐)
审核标识: 第 21 轮工程技术审核
========================================================================================
用户精准指示闭环:
  1. 遮阳板彻底放平压死 (0° 水平向前平整探出)，大屏严禁平面内滚转歪斜 (Rotation 彻底归零，绝不歪)；
  2. 消除大屏表面斜切大三角形过曝反光，采用定向柔光 Spot 精确还原正中白色高光圆斑；
  3. 修复 S3 副板旋转轴向: 严格绕垂直轴旋转，底边保持水平齐平，绝不歪斜成菱形；
  4. 修复 S4/S5 板面: 外侧副板设为墨绿板，双圆管滑轨套杆与右端工程橙色刚性拉杆清晰醒目；
  5. 修复下方大屏右侧垂直金黄色/橙铜色导向条；
  6. 优化画幅比例与构图，紧凑饱满容纳上下双机构。
========================================================================================
"""

import bpy
import bmesh
import math
import os
import sys

print("====================================================================")
print(">>> 开始执行: S系列三维总装构建与物理光追出图 v2.0 (全要素精修对齐版) <<<")
print(">>> 审核标识: 第 21 轮工程技术审核 <<<")
print("====================================================================")

# --------------------------------------------------------------------------------------
# 1. 递归显隐控制
# --------------------------------------------------------------------------------------
def set_obj_hierarchy_visibility(obj, visible=True):
    if obj is None:
        return
    obj.hide_render = not visible
    obj.hide_viewport = not visible
    for child in obj.children:
        set_obj_hierarchy_visibility(child, visible)

# --------------------------------------------------------------------------------------
# 2. 场景环境初始化
# --------------------------------------------------------------------------------------
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
    scene.view_settings.exposure = 0.05
    
    # 经典工业视口中深灰背景 (RGB: 0.18, 0.18, 0.18)
    world = bpy.data.worlds.new("S_Series_World_v2")
    scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs['Color'].default_value = (0.18, 0.18, 0.18, 1.0)
        bg_node.inputs['Strength'].default_value = 0.8
    print("[1/5] 场景初始化与工业灰背景配置就绪。")

# --------------------------------------------------------------------------------------
# 3. 严格校准的高级物理 PBR 材质系统
# --------------------------------------------------------------------------------------
def build_materials():
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

    # 1. 经典沉稳深墨绿黑板面 (带微漫反射颗粒，对齐 17 原版质感)
    materials['blackboard_green'] = create_pbr(
        name="Mat_Blackboard_Green_S2",
        base_color=(0.035, 0.105, 0.060, 1.0),
        metallic=0.01,
        roughness=0.58,
        specular=0.35
    )
    
    # 2. 阳极氧化亮银铝合金细包边 (反光清澈明亮，线条纤细锐利)
    materials['aluminum_bezel'] = create_pbr(
        name="Mat_Aluminum_Bezel_S2",
        base_color=(0.90, 0.91, 0.93, 1.0),
        metallic=0.98,
        roughness=0.15,
        specular=0.98
    )
    
    # 3. 镀铬镜面小圆钮手柄 (17 图中明亮小圆点)
    materials['chrome_handle'] = create_pbr(
        name="Mat_Chrome_Handle_S2",
        base_color=(0.98, 0.98, 1.0, 1.0),
        metallic=1.0,
        roughness=0.06,
        specular=1.0
    )
    
    # 4. 86寸液晶大屏 (鲜明清澈天蓝壁纸 + 玻璃镀膜反光)
    mat_screen = bpy.data.materials.new(name="Mat_Screen_Display_S2")
    mat_screen.use_nodes = True
    s_nodes = mat_screen.node_tree.nodes
    s_links = mat_screen.node_tree.links
    s_nodes.clear()
    s_out = s_nodes.new(type='ShaderNodeOutputMaterial')
    s_out.location = (600, 0)
    s_bsdf = s_nodes.new(type='ShaderNodeBsdfPrincipled')
    s_bsdf.location = (200, 0)
    
    tex_coord = s_nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-400, 0)
    color_ramp = s_nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (-150, 0)
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (0.10, 0.28, 0.58, 1.0) # 底部深科技蓝
    color_ramp.color_ramp.elements[1].position = 1.0
    color_ramp.color_ramp.elements[1].color = (0.24, 0.52, 0.88, 1.0) # 顶部清澈天蓝
    
    s_links.new(tex_coord.outputs['Generated'], color_ramp.inputs['Fac'])
    s_links.new(color_ramp.outputs['Color'], s_bsdf.inputs['Base Color'])
    
    if 'Emission Color' in s_bsdf.inputs:
        s_links.new(color_ramp.outputs['Color'], s_bsdf.inputs['Emission Color'])
        s_bsdf.inputs['Emission Strength'].default_value = 0.40
    s_bsdf.inputs['Roughness'].default_value = 0.12
    if 'Specular IOR Level' in s_bsdf.inputs:
        s_bsdf.inputs['Specular IOR Level'].default_value = 0.95
    elif 'Specular' in s_bsdf.inputs:
        s_bsdf.inputs['Specular'].default_value = 0.95
    # Blender 5.0 Coat 物理清漆玻璃反射层 (产生原图大屏正中央晶莹剔透的高光圆斑)
    if 'Coat Weight' in s_bsdf.inputs:
        s_bsdf.inputs['Coat Weight'].default_value = 1.0
        s_bsdf.inputs['Coat Roughness'].default_value = 0.03
        s_bsdf.inputs['Coat IOR'].default_value = 1.50
    s_links.new(s_bsdf.outputs['BSDF'], s_out.inputs['Surface'])
    materials['screen_display'] = mat_screen

    
    # 5. 遮阳挑檐顶盖 (深空灰吸光涂层)
    materials['canopy_dark'] = create_pbr(
        name="Mat_Canopy_Dark_S2",
        base_color=(0.10, 0.11, 0.12, 1.0),
        metallic=0.70,
        roughness=0.45,
        specular=0.5
    )
    
    # 6. 外侧副书写白板 (象牙白漫反射)
    materials['sub_whiteboard'] = create_pbr(
        name="Mat_Sub_Whiteboard_S2",
        base_color=(0.92, 0.93, 0.94, 1.0),
        metallic=0.01,
        roughness=0.36,
        specular=0.4
    )
    
    # 7. 滑轨主横梁型材 (深灰工业氧化铝)
    materials['track_frame'] = create_pbr(
        name="Mat_Track_Frame_S2",
        base_color=(0.15, 0.16, 0.17, 1.0),
        metallic=0.85,
        roughness=0.30,
        specular=0.7
    )
    
    # 8. 垂直刚性连接杆与定位销 (工程高亮橙色)
    materials['link_rod_orange'] = create_pbr(
        name="Mat_Link_Rod_Orange_S2",
        base_color=(0.92, 0.52, 0.08, 1.0),
        metallic=0.88,
        roughness=0.22,
        specular=0.9
    )
    
    # 9. 伸缩延伸滑套平行双圆管
    materials['ext_rail_steel'] = create_pbr(
        name="Mat_Ext_Rail_Steel_S2",
        base_color=(0.80, 0.82, 0.84, 1.0),
        metallic=0.98,
        roughness=0.15,
        specular=0.98
    )

    print("[2/5] 材质系统编译就绪。")
    return materials

# --------------------------------------------------------------------------------------
# 4. 几何部件构建: 遮阳板水平压平、大屏水平放正绝不歪斜
# --------------------------------------------------------------------------------------
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
    
    # 铝合金细窄包边
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
    """
    构造中置 86 寸智能大屏与【水平压死放平】遮阳盖板:
    - 大屏与遮阳板严格保持水平水平水平！绝不滚转倾斜！
    - 遮阳板彻底放平压死 (0° 水平向前平整挑出)，与顶梁严格平行！
    - 下方系统的遮阳棚紧贴顶梁，零遮挡大屏！
    """
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
    
    # 2. 大屏窄边框 (向前微凸 4mm，在正交前视中清晰勾勒出深黑内嵌边框层次)
    bw = 0.022
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    frame = bpy.context.active_object
    frame.name = f"{name}_OuterFrame"
    frame.scale = (width + 2*bw, 0.045, height + 2*bw)
    frame.location = (0, -0.004, 0)
    frame.data.materials.append(materials['track_frame'])
    frame.parent = screen_root

    
    # 3. 顶置遮阳盖板 (Canopy) - 旋转轴位于大屏正上方顶边框上部
    canopy_pivot = bpy.data.objects.new(f"{name}_Canopy_Pivot", None)
    canopy_pivot.empty_display_type = 'SINGLE_ARROW'
    canopy_pivot.empty_display_size = 0.1
    canopy_pivot.location = (0, 0, height/2 + bw)
    collection.objects.link(canopy_pivot)
    canopy_pivot.parent = screen_root
    
    canopy_w = width + 2*bw + 0.04
    canopy_depth = 0.32
    canopy_th = 0.014
    
    # 盖板本体
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    canopy_mesh = bpy.context.active_object
    canopy_mesh.name = f"{name}_Canopy_Body"
    canopy_mesh.scale = (canopy_w, canopy_depth, canopy_th)
    canopy_mesh.location = (0, -canopy_depth/2, canopy_th/2)
    canopy_mesh.data.materials.append(materials['canopy_dark'])
    canopy_mesh.parent = canopy_pivot
    
    # 盖板铝合金前包边
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    canopy_edge = bpy.context.active_object
    canopy_edge.name = f"{name}_Canopy_Edge"
    canopy_edge.scale = (canopy_w, 0.014, canopy_th*1.4)
    canopy_edge.location = (0, -canopy_depth, canopy_th/2)
    canopy_edge.data.materials.append(materials['aluminum_bezel'])
    canopy_edge.parent = canopy_pivot
    
    # 彻底放平压死: rotation 为 (0, 0, 0) 水平放平，绝不乱翘
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
    
    # 2. 中置大屏与水平压死遮阳板 (大屏与遮阳板完全平直放正，绝不倾斜歪倒！)
    screen_unit, canopy_pivot = create_screen_and_flat_canopy(
        name=f"{system_name}_Display",
        width=screen_w,
        height=screen_h,
        materials=materials
    )
    screen_unit.parent = sys_root
    # 确保屏幕自身旋转彻底归零，绝不在二维视口中歪斜！
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
    
    # 4. 右侧对接垂直导向条 (金黄/铜橙色，对齐 17 原图大屏右侧清晰导轨)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    guide_bar = bpy.context.active_object
    guide_bar.name = f"{system_name}_Guide_Bar_Orange"
    guide_bar.scale = (0.018, board_th*1.1, board_h)
    guide_bar.location = (screen_w/2 + 0.01, 0, 0)
    guide_bar.data.materials.append(materials['link_rod_orange'])
    guide_bar.parent = sys_root
    
    # 5. 伸缩延伸滑套双圆管
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
    
    # 6. 两翼外侧副书写板
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

def build_s_series_dual_master_v2(materials):
    """上下双套总装，垂直间距适中紧凑，中间 3D Cursor"""
    top_sys = build_single_s_system("Top_S2", base_z=0.72, materials=materials)
    bot_sys = build_single_s_system("Bot_S2", base_z=-0.72, materials=materials)
    
    # 3D Cursor 真实指示标
    bpy.ops.mesh.primitive_torus_add(major_radius=0.038, minor_radius=0.0035, location=(0, 0, 0))
    cursor = bpy.context.active_object
    cursor.name = "Viewport_3DCursor_Torus_S2"
    c_mat = bpy.data.materials.new(name="Mat_Cursor_S2")
    c_mat.use_nodes = True
    c_bsdf = c_mat.node_tree.nodes.get("Principled BSDF")
    if c_bsdf:
        c_bsdf.inputs['Base Color'].default_value = (0.9, 0.2, 0.2, 1.0)
    cursor.data.materials.append(c_mat)
    
    return top_sys, bot_sys

# --------------------------------------------------------------------------------------
# 5. 精准物理灯光: 彻底消除大面积斜切白反光，还原大屏正中高光圆斑与右板漫射光晕
# --------------------------------------------------------------------------------------
def setup_calibrated_lighting():
    col = bpy.context.scene.collection
    
    # 1. 模拟大屏正中上方圆润高光斑 (Spot 聚光灯，高能量柔光束)
    spot_screen = bpy.data.lights.new(name="Light_Screen_Spot", type='SPOT')
    spot_screen.energy = 750.0
    spot_screen.spot_size = math.radians(25.0) # 聚光产生圆润白斑
    spot_screen.spot_blend = 0.35              # 边缘柔和羽化
    spot_screen.color = (1.0, 0.98, 0.95)
    spot_screen_obj = bpy.data.objects.new("Light_Screen_Spot", spot_screen)
    spot_screen_obj.location = (0.15, -2.2, 0.95) # 正对上方大屏中央偏上
    spot_screen_obj.rotation_euler = (math.radians(18), math.radians(3), 0)
    col.objects.link(spot_screen_obj)
    
    # 2. 模拟右侧黑板上的柔和圆形漫反射光斑
    spot_board = bpy.data.lights.new(name="Light_Board_Spot", type='SPOT')
    spot_board.energy = 260.0
    spot_board.spot_size = math.radians(30.0)
    spot_board.spot_blend = 0.45
    spot_board.color = (1.0, 1.0, 1.0)
    spot_board_obj = bpy.data.objects.new("Light_Board_Spot", spot_board)
    spot_board_obj.location = (1.45, -2.4, 0.75)
    spot_board_obj.rotation_euler = (math.radians(15), math.radians(-8), 0)
    col.objects.link(spot_board_obj)
    
    # 3. 柔和正面补光
    front_fill = bpy.data.lights.new(name="Light_Front_Fill", type='AREA')
    front_fill.energy = 80.0
    front_fill.size = 5.4
    front_fill.size_y = 3.6
    front_fill.color = (0.96, 0.98, 1.0)
    front_fill_obj = bpy.data.objects.new("Light_Front_Fill", front_fill)
    front_fill_obj.location = (0, -3.6, 0)
    front_fill_obj.rotation_euler = (math.radians(90), 0, 0)
    col.objects.link(front_fill_obj)
    
    print("[3/5] 精准物理照明配置完毕 (强化正中高光球与黑板漫射光晕)。")


# --------------------------------------------------------------------------------------
# 6. S 系列渲染出图: S1~S5 严格修复所有问题
# --------------------------------------------------------------------------------------
def render_s_series_v2(top_sys, bot_sys, output_dir):
    scene = bpy.context.scene
    
    cam_data = bpy.data.cameras.new("S_Series_Camera_v2")
    cam_data.type = 'ORTHO'
    cam_obj = bpy.data.objects.new("S_Series_Camera_v2", cam_data)
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
        # S1: 对齐 media__1783170868851.png (画幅紧凑长宽比约 1.48:1，大屏与遮阳板放平绝不歪斜，副板彻底隐藏)
        {
            "name": "S1.png",
            "res_x": 3550,
            "res_y": 2390,
            "ortho_scale": 4.55,
            "setup": lambda: setup_s1_v2(top_sys, bot_sys, main_offset_x)
        },
        # S2: 对齐 media__1783170884236.png (副白板完全水平平展，画幅长宽比约 2:1)
        {
            "name": "S2.png",
            "res_x": 3840,
            "res_y": 1920,
            "ortho_scale": 6.30,
            "setup": lambda: setup_s2_v2(top_sys, bot_sys, main_offset_x, board_w, bezel_w)
        },
        # S3: 对齐 media__1783170899258.png (副白板绕垂直轴向前折叠 28°，底边严格保持水平，绝无菱形歪角！)
        {
            "name": "S3.png",
            "res_x": 3840,
            "res_y": 2120,
            "ortho_scale": 6.25,
            "setup": lambda: setup_s3_v2(top_sys, bot_sys, main_offset_x, board_w, bezel_w)
        },
        # S4: 对齐 media__1783170944637.png (双横梁套杆外滑，外侧副板为墨绿板，右下橙色拉杆醒目)
        {
            "name": "S4.png",
            "res_x": 3840,
            "res_y": 1520,
            "ortho_scale": 6.90,
            "setup": lambda: setup_s4_v2(top_sys, bot_sys, main_offset_x, board_w, bezel_w)
        },
        # S5: 对齐 media__1783170957959.png (极限全开露大屏，外侧全绿板扩展)
        {
            "name": "S5.png",
            "res_x": 3840,
            "res_y": 1520,
            "ortho_scale": 6.90,
            "setup": lambda: setup_s5_v2(top_sys, bot_sys, main_offset_x, board_w, bezel_w)
        }
    ]
    
    print("[4/5] 开始执行 S 系列 v2.0 精修渲染出图...")
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



# --------------------------------------------------------------------------------------
# 各工况姿态精修逻辑 (彻底纠偏)
# --------------------------------------------------------------------------------------
def setup_s1_v2(top, bot, main_offset_x):
    """S1: 遮阳板彻底放平压死，大屏绝对水平放正零歪斜，两翼副板彻底递归隐藏"""
    set_obj_hierarchy_visibility(top['left_sub'], False)
    set_obj_hierarchy_visibility(top['right_sub'], False)
    set_obj_hierarchy_visibility(bot['left_sub'], False)
    set_obj_hierarchy_visibility(bot['right_sub'], False)
    
    # 主板位于标准展开位置
    top['left_main'].location = (-main_offset_x, 0, 0)
    top['right_main'].location = (main_offset_x, 0, 0)
    bot['left_main'].location = (-main_offset_x, 0, 0)
    bot['right_main'].location = (main_offset_x, 0, 0)
    
    # 【死命令执行】遮阳板与大屏绝对水平放平压死，Rotation 彻底归零，杜绝任何倾斜歪角！
    top['canopy'].rotation_euler = (0, 0, 0)
    top['screen'].rotation_euler = (0, 0, 0)
    bot['canopy'].rotation_euler = (0, 0, 0)
    bot['screen'].rotation_euler = (0, 0, 0)

def setup_s2_v2(top, bot, main_offset_x, board_w, bezel_w):
    """S2: 副白板水平平铺展开"""
    set_obj_hierarchy_visibility(top['left_sub'], True)
    set_obj_hierarchy_visibility(top['right_sub'], True)
    set_obj_hierarchy_visibility(bot['left_sub'], True)
    set_obj_hierarchy_visibility(bot['right_sub'], True)
    
    # 遮阳板与大屏保持平正放平
    top['canopy'].rotation_euler = (0, 0, 0)
    top['screen'].rotation_euler = (0, 0, 0)
    bot['canopy'].rotation_euler = (0, 0, 0)
    bot['screen'].rotation_euler = (0, 0, 0)
    
    # 副板换回白板材质
    mat_white = bpy.data.materials.get("Mat_Sub_Whiteboard_S2")
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

def setup_s3_v2(top, bot, main_offset_x, board_w, bezel_w):
    """S3: 副白板向前折叠 28°，底边严格保持水平，绝不发生菱形歪角！"""
    set_obj_hierarchy_visibility(top['left_sub'], True)
    set_obj_hierarchy_visibility(top['right_sub'], True)
    set_obj_hierarchy_visibility(bot['left_sub'], True)
    set_obj_hierarchy_visibility(bot['right_sub'], True)
    
    top['canopy'].rotation_euler = (0, 0, 0)
    top['screen'].rotation_euler = (0, 0, 0)
    bot['canopy'].rotation_euler = (0, 0, 0)
    bot['screen'].rotation_euler = (0, 0, 0)
    
    mat_white = bpy.data.materials.get("Mat_Sub_Whiteboard_S2")
    for s in [top, bot]:
        s['left_sub'].children[0].data.materials[0] = mat_white
        s['right_sub'].children[0].data.materials[0] = mat_white
        s['left_main'].location.x = -main_offset_x
        s['right_main'].location.x = main_offset_x
        
        # 旋转必须严格绕垂直轴 Z 进行！
        # 在正交前视中，绕 Z 轴旋转向前聚拢，底边依然与主板底边在同一直线上！
        fold_angle = math.radians(28)
        # 铰链位于主板外侧边缘，副板绕铰链向前旋转
        hinge_lx = -main_offset_x - board_w/2 - bezel_w
        hinge_rx = main_offset_x + board_w/2 + bezel_w
        
        # 左副板向前折叠 (向 +Y 旋转，即在俯视图中向内偏角)
        s['left_sub'].location = (hinge_lx - (board_w/2) * math.cos(fold_angle), -(board_w/2) * math.sin(fold_angle), 0)
        s['left_sub'].rotation_euler = (0, 0, -fold_angle) # 严格仅绕 Z 轴！
        
        # 右副板向前折叠
        s['right_sub'].location = (hinge_rx + (board_w/2) * math.cos(fold_angle), -(board_w/2) * math.sin(fold_angle), 0)
        s['right_sub'].rotation_euler = (0, 0, fold_angle)  # 严格仅绕 Z 轴！

def setup_s4_v2(top, bot, main_offset_x, board_w, bezel_w):
    """S4: 双横梁延伸套杆外滑，外侧副板为墨绿板，右下橙色拉杆清晰呈现"""
    set_obj_hierarchy_visibility(top['left_sub'], True)
    set_obj_hierarchy_visibility(top['right_sub'], True)
    set_obj_hierarchy_visibility(bot['left_sub'], True)
    set_obj_hierarchy_visibility(bot['right_sub'], True)
    
    top['canopy'].rotation_euler = (0, 0, 0)
    top['screen'].rotation_euler = (0, 0, 0)
    bot['canopy'].rotation_euler = (0, 0, 0)
    bot['screen'].rotation_euler = (0, 0, 0)
    
    mat_green = bpy.data.materials.get("Mat_Blackboard_Green_S2")
    for s in [top, bot]:
        # 外侧副板换为墨绿板 (全绿板工况)
        s['left_sub'].children[0].data.materials[0] = mat_green
        s['right_sub'].children[0].data.materials[0] = mat_green
        # 主绿板向外滑出 0.38m
        s['left_main'].location.x = -main_offset_x - 0.38
        s['right_main'].location.x = main_offset_x + 0.38
        # 外侧副板向外极限滑动
        s['left_sub'].location = (-main_offset_x - board_w - 0.95, 0, 0)
        s['right_sub'].location = (main_offset_x + board_w + 0.95, 0, 0)
        s['left_sub'].rotation_euler = (0, 0, 0)
        s['right_sub'].rotation_euler = (0, 0, 0)

def setup_s5_v2(top, bot, main_offset_x, board_w, bezel_w):
    """S5: 极限全开露出完整中置大屏与光影联动"""
    setup_s4_v2(top, bot, main_offset_x, board_w, bezel_w)

# --------------------------------------------------------------------------------------
# 7. 主执行函数
# --------------------------------------------------------------------------------------
def main():
    s_dir = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\S系列"
    blend_path = os.path.join(s_dir, "S_Series_Master_v2.blend")
    
    init_clean_scene()
    materials = build_materials()
    top_sys, bot_sys = build_s_series_dual_master_v2(materials)
    setup_calibrated_lighting()
    
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"--> [OK] S系列母本工程 v2.0 已成功保存: {blend_path}")
    
    render_s_series_v2(top_sys, bot_sys, s_dir)
    print("\n[5/5] S系列 v2.0 精修构建与 S1~S5 出图全部完成！")
    print("====================================================================")

if __name__ == "__main__":
    main()
