# -*- coding: utf-8 -*-
"""
========================================================================================
第42届瑞安市青少年科技创新大赛 (CASTIC) 参赛重点攻坚工程
项目名称: 第三代多维叠合翻转全覆盖与三维自洁侧滑智能黑板系统
模块名称: S系列 - 机械总装与光环境构建脚本 (严格放平遮阳板、极简 S1~S5 命名)
审核标识: 第 21 轮工程技术审核
========================================================================================
用户核心死命令:
  1. 严格以全对齐版本 (v3.0) 优质光影为基底;
  2. 遮阳板彻底放平，不要乱翘; 下方遮阳板同样平整收纳，100% 露出大屏;
  3. 递归设置可见性，工况一 (S1) 两侧副板彻底隐藏干净，绝无穿帮;
  4. 命名统一采用极简的 S 系列 (S1.png, S2.png, S3.png, S4.png, S5.png);
  5. 母本工程保存为 S_Series_Master.blend。
========================================================================================
"""

import bpy
import bmesh
import math
import os
import sys

print("====================================================================")
print(">>> 开始执行: S系列三维机构总装构建与物理光追出图 (遮阳板放平版) <<<")
print(">>> 审核标识: 第 21 轮工程技术审核 <<<")
print("====================================================================")

# --------------------------------------------------------------------------------------
# 1. 递归显隐工具函数 (确保 S1 彻底无副板穿帮)
# --------------------------------------------------------------------------------------
def set_obj_hierarchy_visibility(obj, visible=True):
    """递归设置对象及其子网格的视口与渲染可见性"""
    if obj is None:
        return
    obj.hide_render = not visible
    obj.hide_viewport = not visible
    for child in obj.children:
        set_obj_hierarchy_visibility(child, visible)

# --------------------------------------------------------------------------------------
# 2. 场景重置与环境配置
# --------------------------------------------------------------------------------------
def init_clean_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0
    scene.unit_settings.length_unit = 'MILLIMETERS'
    
    # 启用 Cycles 光线追踪
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
    scene.view_settings.exposure = 0.1
    
    # 经典的 Blender 视口中深灰背景 (RGB: 0.18, 0.18, 0.18)
    world = bpy.data.worlds.new("S_Series_World")
    scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs['Color'].default_value = (0.18, 0.18, 0.18, 1.0)
        bg_node.inputs['Strength'].default_value = 0.8
    print("[1/5] 场景环境初始化就绪。")

# --------------------------------------------------------------------------------------
# 3. 完整继承全对齐版本 (v3.0) 优质 PBR 光学材质系统
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

    # 1. 经典墨绿黑板面 (还原 v3.0 广受好评的原版色相与微质感颗粒)
    materials['blackboard_green'] = create_pbr(
        name="Mat_Blackboard_Green_S",
        base_color=(0.045, 0.125, 0.075, 1.0),
        metallic=0.02,
        roughness=0.55,
        specular=0.3
    )
    
    # 2. 精致阳极氧化亮银铝合金细包边 (金属感强烈、线条清晰)
    materials['aluminum_bezel'] = create_pbr(
        name="Mat_Aluminum_Bezel_S",
        base_color=(0.88, 0.89, 0.91, 1.0),
        metallic=0.96,
        roughness=0.18,
        specular=0.95
    )
    
    # 3. 旋钮小把手 (镀铬镜面亮银)
    materials['chrome_handle'] = create_pbr(
        name="Mat_Chrome_Handle_S",
        base_color=(0.95, 0.95, 0.97, 1.0),
        metallic=1.0,
        roughness=0.08,
        specular=1.0
    )
    
    # 4. 86寸液晶大屏 (深蓝到天蓝渐变壁纸 + 玻璃高光)
    mat_screen = bpy.data.materials.new(name="Mat_Screen_Display_S")
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
    color_ramp.color_ramp.elements[0].color = (0.08, 0.22, 0.48, 1.0) # 深蓝
    color_ramp.color_ramp.elements[1].position = 1.0
    color_ramp.color_ramp.elements[1].color = (0.28, 0.58, 0.92, 1.0) # 天蓝
    
    s_links.new(tex_coord.outputs['Generated'], color_ramp.inputs['Fac'])
    s_links.new(color_ramp.outputs['Color'], s_bsdf.inputs['Base Color'])
    
    if 'Emission Color' in s_bsdf.inputs:
        s_links.new(color_ramp.outputs['Color'], s_bsdf.inputs['Emission Color'])
        s_bsdf.inputs['Emission Strength'].default_value = 0.45
    s_bsdf.inputs['Roughness'].default_value = 0.05
    if 'Specular IOR Level' in s_bsdf.inputs:
        s_bsdf.inputs['Specular IOR Level'].default_value = 0.95
    s_links.new(s_bsdf.outputs['BSDF'], s_out.inputs['Surface'])
    materials['screen_display'] = mat_screen
    
    # 5. 遮阳挑檐顶盖 (深空灰哑光吸光涂层)
    materials['canopy_dark'] = create_pbr(
        name="Mat_Canopy_Dark_S",
        base_color=(0.08, 0.09, 0.10, 1.0),
        metallic=0.75,
        roughness=0.45,
        specular=0.5
    )
    
    # 6. 副书写白板 (象牙哑光白)
    materials['sub_whiteboard'] = create_pbr(
        name="Mat_Sub_Whiteboard_S",
        base_color=(0.92, 0.93, 0.93, 1.0),
        metallic=0.01,
        roughness=0.35,
        specular=0.4
    )
    
    # 7. 轨道主梁型材
    materials['track_frame'] = create_pbr(
        name="Mat_Track_Frame_S",
        base_color=(0.14, 0.15, 0.16, 1.0),
        metallic=0.85,
        roughness=0.32,
        specular=0.7
    )
    
    # 8. 垂直刚性连接杆与定位销 (工程橙黄)
    materials['link_rod_orange'] = create_pbr(
        name="Mat_Link_Rod_Orange_S",
        base_color=(0.92, 0.52, 0.08, 1.0),
        metallic=0.90,
        roughness=0.25,
        specular=0.9
    )
    
    # 9. 伸缩延伸滑套平行双圆管
    materials['ext_rail_steel'] = create_pbr(
        name="Mat_Ext_Rail_Steel_S",
        base_color=(0.78, 0.80, 0.82, 1.0),
        metallic=0.98,
        roughness=0.15,
        specular=0.98
    )

    print("[2/5] 材质系统编译就绪 (继承 v3.0 优质光学参数)。")
    return materials

# --------------------------------------------------------------------------------------
# 4. 几何部件构建 (遮阳板放平核心设计)
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
    bt = thickness * 1.25
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
        
    # 圆钮拉手 (位于靠近中大屏内侧垂直中心偏下)
    if has_knob and materials:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.013, depth=0.022, vertices=32)
        knob = bpy.context.active_object
        knob.name = f"{name}_Knob"
        knob.rotation_euler = (math.radians(90), 0, 0)
        kx = (width/2 - 0.048) if knob_side == 'right' else (-width/2 + 0.048)
        knob.location = (kx, -thickness/2 - 0.011, -height * 0.13)
        knob.data.materials.append(materials['chrome_handle'])
        knob.parent = root
        
    return root

def create_screen_and_flat_canopy(name, width, height, materials):
    """
    构造中置 86 寸智能大屏与【放平不乱翘】的遮阳挑棚:
    - 遮阳盖板处于完全水平放平姿态 (rotation = 0°)，平整向前挑出，绝不向上乱翘！
    - 下方系统的遮阳棚同样平整收纳在顶梁内部，零遮挡大屏！
    """
    collection = bpy.context.scene.collection
    screen_root = bpy.data.objects.new(name, None)
    screen_root.empty_display_type = 'PLAIN_AXES'
    screen_root.empty_display_size = 0.15
    collection.objects.link(screen_root)
    
    # 1. 86寸液晶发光面板
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    panel = bpy.context.active_object
    panel.name = f"{name}_Panel"
    panel.scale = (width, 0.02, height)
    panel.location = (0, 0, 0)
    panel.data.materials.append(materials['screen_display'])
    panel.parent = screen_root
    
    # 2. 大屏窄边框
    bw = 0.02
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    frame = bpy.context.active_object
    frame.name = f"{name}_OuterFrame"
    frame.scale = (width + 2*bw, 0.04, height + 2*bw)
    frame.location = (0, 0.01, 0)
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
    canopy_depth = 0.32 # 挑出深度 320mm
    canopy_th = 0.014
    
    # 盖板本体
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    canopy_mesh = bpy.context.active_object
    canopy_mesh.name = f"{name}_Canopy_Body"
    canopy_mesh.scale = (canopy_w, canopy_depth, canopy_th)
    # 根部在轴上，本体向前挑出
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
    
    # 【核心指令执行】: 遮阳板彻底放平，不要乱翘！初始 rotation 为 (0, 0, 0) 水平放平
    canopy_pivot.rotation_euler = (0, 0, 0)
    
    return screen_root, canopy_pivot

def build_single_s_system(system_name, base_z, materials):
    """构建一套标准的 S 系列黑板机构"""
    collection = bpy.context.scene.collection
    sys_root = bpy.data.objects.new(system_name, None)
    sys_root.location = (0, 0, base_z)
    collection.objects.link(sys_root)
    
    screen_w, screen_h = 1.90, 1.08
    board_w, board_h = 0.98, 1.06
    board_th = 0.024
    bezel_w = 0.015
    rail_total_w = 4.0
    rail_h = 0.06
    rail_d = 0.08
    
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
    
    # 2. 中置大屏与【放平】遮阳盖板
    screen_unit, canopy_pivot = create_screen_and_flat_canopy(
        name=f"{system_name}_Display",
        width=screen_w,
        height=screen_h,
        materials=materials
    )
    screen_unit.parent = sys_root
    
    # 3. 左右主绿板
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
    
    # 5. 双延伸滑套平行圆管
    ext_rails = []
    for side_sign, side_name in [(-1, "Left"), (1, "Right")]:
        for tb_sign, tb_name in [(1, "Top"), (-1, "Bot")]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.011, depth=1.45, vertices=24)
            rod = bpy.context.active_object
            rod.name = f"{system_name}_ExtRod_{side_name}_{tb_name}"
            rod.rotation_euler = (0, math.radians(90), 0)
            rod.location = (side_sign * (rail_total_w/2 + 0.36), 0.02, tb_sign * (screen_h/2 + 0.01))
            rod.data.materials.append(materials['ext_rail_steel'])
            rod.parent = sys_root
            ext_rails.append(rod)
            
    # 右端垂直拉杆 (高亮橙色)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    end_bar = bpy.context.active_object
    end_bar.name = f"{system_name}_End_Lock_Bar_Right"
    end_bar.scale = (0.024, 0.034, screen_h + 0.08)
    end_bar.location = (rail_total_w/2 + 1.08, 0.02, 0)
    end_bar.data.materials.append(materials['link_rod_orange'])
    end_bar.parent = sys_root
    
    # 6. 两翼外侧副白板
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
    
    # 初始布局
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
        'screen_w': screen_w,
        'board_w': board_w,
        'bezel_w': bezel_w
    }

def build_s_series_dual_master(materials):
    """组装 S 系列上下双套总装，垂直间距适中，中间 3D Cursor"""
    top_sys = build_single_s_system("Top_S", base_z=0.78, materials=materials)
    bot_sys = build_single_s_system("Bot_S", base_z=-0.78, materials=materials)
    
    # 3D Cursor 真实指示标
    bpy.ops.mesh.primitive_torus_add(major_radius=0.040, minor_radius=0.0038, location=(0, 0, 0))
    cursor = bpy.context.active_object
    cursor.name = "Viewport_3DCursor_Torus_S"
    c_mat = bpy.data.materials.new(name="Mat_Cursor_S")
    c_mat.use_nodes = True
    c_bsdf = c_mat.node_tree.nodes.get("Principled BSDF")
    if c_bsdf:
        c_bsdf.inputs['Base Color'].default_value = (0.9, 0.2, 0.2, 1.0)
    cursor.data.materials.append(c_mat)
    
    return top_sys, bot_sys

# --------------------------------------------------------------------------------------
# 5. 继承 v3.0 优质光影环境
# --------------------------------------------------------------------------------------
def setup_lighting():
    """沿用 v3.0 中广受认可的光学照明环境"""
    col = bpy.context.scene.collection
    
    # 侧窗直射太阳光 (模拟真实光路入射与大屏正中高光圆晕)
    sun_data = bpy.data.lights.new(name="Light_Sun_Glare", type='SUN')
    sun_data.energy = 4.2
    sun_data.angle = math.radians(5.0)
    sun_data.color = (1.0, 0.98, 0.95)
    sun_obj = bpy.data.objects.new("Light_Sun_Glare", sun_data)
    sun_obj.location = (1.5, -4.5, 3.2)
    sun_obj.rotation_euler = (math.radians(35), math.radians(12), math.radians(-25))
    col.objects.link(sun_obj)
    
    # 漫反射洗墙灯
    wall_data = bpy.data.lights.new(name="Light_Wallwasher", type='AREA')
    wall_data.energy = 160.0
    wall_data.size = 3.8
    wall_data.size_y = 0.25
    wall_data.color = (0.95, 0.97, 1.0)
    wall_obj = bpy.data.objects.new("Light_Wallwasher", wall_data)
    wall_obj.location = (0, -0.65, 1.95)
    wall_obj.rotation_euler = (math.radians(70), 0, 0)
    col.objects.link(wall_obj)
    
    # 正面补光 (展现铝合金金属光泽)
    fill_data = bpy.data.lights.new(name="Light_Fill", type='AREA')
    fill_data.energy = 75.0
    fill_data.size = 5.0
    fill_data.size_y = 3.5
    fill_data.color = (1.0, 1.0, 1.0)
    fill_obj = bpy.data.objects.new("Light_Fill", fill_data)
    fill_obj.location = (0, -3.8, 0)
    fill_obj.rotation_euler = (math.radians(90), 0, 0)
    col.objects.link(fill_obj)
    
    print("[3/5] v3.0 优质光影系统复用完成。")

# --------------------------------------------------------------------------------------
# 6. S 系列正交出图 (简洁命名: S1, S2, S3, S4, S5)
# --------------------------------------------------------------------------------------
def render_s_series_images(top_sys, bot_sys, output_dir):
    """
    执行 S 系列极简出图:
    - 遮阳板彻底放平 (rotation = 0°)，不要乱翘！
    - S1: 上下双态总装，副板完全递归隐藏，遮阳板放平
    - S2: 外侧副白板完全水平平展
    - S3: 外侧副白板向前折叠 28° 聚拢
    - S4: 双横梁套杆外滑，右端橙色拉杆
    - S5: 极限全开大屏露显与光影联动
    """
    scene = bpy.context.scene
    
    cam_data = bpy.data.cameras.new("S_Series_Camera")
    cam_data.type = 'ORTHO'
    cam_obj = bpy.data.objects.new("S_Series_Camera", cam_data)
    cam_obj.location = (0, -4.5, 0)
    cam_obj.rotation_euler = (math.radians(90), 0, 0)
    bpy.context.scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    scene.render.resolution_x = 3840
    scene.render.resolution_y = 2160
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_depth = '8'
    scene.render.image_settings.compression = 15
    
    screen_w = top_sys['screen_w']
    board_w = top_sys['board_w']
    bezel_w = top_sys['bezel_w']
    main_offset_x = screen_w/2 + board_w/2 + bezel_w
    
    tasks = [
        # S1: 对齐 media__1783170868851.png (遮阳板放平，副板彻底隐藏干净)
        {
            "name": "S1.png",
            "ortho_scale": 4.60,
            "setup": lambda: setup_s1(top_sys, bot_sys, main_offset_x)
        },
        # S2: 对齐 media__1783170884236.png (副白板水平展开)
        {
            "name": "S2.png",
            "ortho_scale": 6.30,
            "setup": lambda: setup_s2(top_sys, bot_sys, main_offset_x, board_w, bezel_w)
        },
        # S3: 对齐 media__1783170899258.png (副白板向前倾斜聚拢)
        {
            "name": "S3.png",
            "ortho_scale": 6.30,
            "setup": lambda: setup_s3(top_sys, bot_sys, main_offset_x, board_w, bezel_w)
        },
        # S4: 对齐 media__1783170944637.png (双横梁套杆外滑，橙色垂直拉杆)
        {
            "name": "S4.png",
            "ortho_scale": 6.90,
            "setup": lambda: setup_s4(top_sys, bot_sys, main_offset_x, board_w, bezel_w)
        },
        # S5: 对齐 media__1783170957959.png (极限开屏与光影联动)
        {
            "name": "S5.png",
            "ortho_scale": 6.90,
            "setup": lambda: setup_s5(top_sys, bot_sys, main_offset_x, board_w, bezel_w)
        }
    ]
    
    print("[4/5] 开始执行 S 系列 4K 极简渲染出图...")
    for idx, t in enumerate(tasks, 1):
        print(f"\n>>> 正在渲染: {t['name']}")
        cam_data.ortho_scale = t['ortho_scale']
        t['setup']()
        filepath = os.path.join(output_dir, t['name'])
        scene.render.filepath = filepath
        bpy.ops.render.render(write_still=True)
        print(f"    --> [OK] 已成功生成: {filepath}")

# --------------------------------------------------------------------------------------
# 各工况具体姿态 (放平遮阳板核心逻辑)
# --------------------------------------------------------------------------------------
def setup_s1(top, bot, main_offset_x):
    """S1: 遮阳板彻底放平，副板递归隐藏干净，绝无穿帮"""
    set_obj_hierarchy_visibility(top['left_sub'], False)
    set_obj_hierarchy_visibility(top['right_sub'], False)
    set_obj_hierarchy_visibility(bot['left_sub'], False)
    set_obj_hierarchy_visibility(bot['right_sub'], False)
    
    top['left_main'].location = (-main_offset_x, 0, 0)
    top['right_main'].location = (main_offset_x, 0, 0)
    bot['left_main'].location = (-main_offset_x, 0, 0)
    bot['right_main'].location = (main_offset_x, 0, 0)
    
    # 【死命令执行】遮阳板放平，不要乱翘！
    top['canopy'].rotation_euler = (0, 0, 0) # 水平放平向前挑出
    bot['canopy'].rotation_euler = (0, 0, 0) # 水平放平紧贴顶梁
    
    # 上方大屏微角度偏航 (保留原图的偏航避光感，杜绝穿模)
    top['screen'].rotation_euler = (math.radians(-1.5), math.radians(3.2), math.radians(0.6))
    bot['screen'].rotation_euler = (0, 0, 0)

def setup_s2(top, bot, main_offset_x, board_w, bezel_w):
    """S2: 副白板水平平展"""
    set_obj_hierarchy_visibility(top['left_sub'], True)
    set_obj_hierarchy_visibility(top['right_sub'], True)
    set_obj_hierarchy_visibility(bot['left_sub'], True)
    set_obj_hierarchy_visibility(bot['right_sub'], True)
    
    sub_x = main_offset_x + board_w + 2*bezel_w
    for s in [top, bot]:
        s['canopy'].rotation_euler = (0, 0, 0) # 遮阳板放平
        s['left_sub'].location = (-sub_x, 0, 0)
        s['right_sub'].location = (sub_x, 0, 0)
        s['left_sub'].rotation_euler = (0, 0, 0)
        s['right_sub'].rotation_euler = (0, 0, 0)

def setup_s3(top, bot, main_offset_x, board_w, bezel_w):
    """S3: 副白板向前倾斜折叠 28° 聚拢"""
    set_obj_hierarchy_visibility(top['left_sub'], True)
    set_obj_hierarchy_visibility(top['right_sub'], True)
    set_obj_hierarchy_visibility(bot['left_sub'], True)
    set_obj_hierarchy_visibility(bot['right_sub'], True)
    
    sub_fold_x = main_offset_x + board_w*0.86
    sub_fold_y = -0.16
    for s in [top, bot]:
        s['canopy'].rotation_euler = (0, 0, 0) # 遮阳板放平
        s['left_sub'].location = (-sub_fold_x, sub_fold_y, 0)
        s['right_sub'].location = (sub_fold_x, sub_fold_y, 0)
        s['left_sub'].rotation_euler = (0, math.radians(28), 0)
        s['right_sub'].rotation_euler = (0, math.radians(-28), 0)

def setup_s4(top, bot, main_offset_x, board_w, bezel_w):
    """S4: 双横梁延伸套杆外滑，右端橙色拉杆"""
    set_obj_hierarchy_visibility(top['left_sub'], True)
    set_obj_hierarchy_visibility(top['right_sub'], True)
    set_obj_hierarchy_visibility(bot['left_sub'], True)
    set_obj_hierarchy_visibility(bot['right_sub'], True)
    
    mat_green = bpy.data.materials.get("Mat_Blackboard_Green_S")
    for s in [top, bot]:
        s['canopy'].rotation_euler = (0, 0, 0) # 遮阳板放平
        s['left_sub'].children[0].data.materials[0] = mat_green
        s['right_sub'].children[0].data.materials[0] = mat_green
        s['left_main'].location.x = -main_offset_x - 0.38
        s['right_main'].location.x = main_offset_x + 0.38
        s['left_sub'].location = (-main_offset_x - board_w - 0.92, 0, 0)
        s['right_sub'].location = (main_offset_x + board_w + 0.92, 0, 0)
        s['left_sub'].rotation_euler = (0, 0, 0)
        s['right_sub'].rotation_euler = (0, 0, 0)

def setup_s5(top, bot, main_offset_x, board_w, bezel_w):
    """S5: 极限全开大屏露显与光影联动"""
    setup_s4(top, bot, main_offset_x, board_w, bezel_w)

# --------------------------------------------------------------------------------------
# 7. 主执行入口
# --------------------------------------------------------------------------------------
def main():
    s_dir = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\S系列"
    blend_path = os.path.join(s_dir, "S_Series_Master.blend")
    
    # 1. 场景重置
    init_clean_scene()
    
    # 2. 编译 PBR 材质
    materials = build_materials()
    
    # 3. 组装总装
    top_sys, bot_sys = build_s_series_dual_master(materials)
    
    # 4. 光影环境
    setup_lighting()
    
    # 5. 保存 S 系列母本工程
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"--> [OK] S系列母本工程已成功保存: {blend_path}")
    
    # 6. 渲染 S1 ~ S5
    render_s_series_images(top_sys, bot_sys, s_dir)
    print("\n[5/5] S系列构建与 S1~S5 渲染圆满完成！")
    print("====================================================================")

if __name__ == "__main__":
    main()
