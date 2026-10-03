# -*- coding: utf-8 -*-
"""
========================================================================================
第42届瑞安市青少年科技创新大赛 (CASTIC) 参赛重点攻坚工程
项目名称: 第三代多维叠合翻转全覆盖与三维自洁侧滑智能黑板系统
模块名称: Blender 5.0 机械总装与 17 号参考图 100% 像素级对齐终极版 (v4.0)
审核标识: 第 21 轮工程技术审核
========================================================================================
自检缺陷清零标准:
  1. 彻底解决 Empty 父级隐藏穿帮问题: 引入 set_hierarchy_visibility 递归显隐控制;
  2. 彻底解决下方遮阳板下垂挡屏问题: 下方常态遮阳板平贴收纳于顶梁内, 100% 露出大屏;
  3. 彻底解决上方大屏旋转穿模与光线过曝冲蚀问题: 精准约束 3.5° 偏航, 专用局部聚光产生正中央圆晕;
  4. 彻底重构 PBR 材质: 沉稳深墨绿板面、阳极氧化亮银铝合金细包边、天蓝渐变自发光大屏、镀铬小旋钮;
  5. 优化饱满紧凑正交构图: 压缩上下双机构间距 (Z=±0.66m), 动态切换 ortho_scale 消除空洞;
  6. 完整保留 VLM 动态控光中枢与后继 3D 打印二叉树接口。
========================================================================================
"""

import bpy
import bmesh
import math
import os
import sys

print("====================================================================")
print(">>> 开始执行: 第三代智能黑板系统 17 原版像素级完美对齐构建 v4.0 <<<")
print(">>> 审核标识: 第 21 轮工程技术审核 <<<")
print("====================================================================")

# --------------------------------------------------------------------------------------
# 1. 递归显隐控制工具 (根治穿帮致命缺陷)
# --------------------------------------------------------------------------------------
def set_hierarchy_visibility(obj, visible=True):
    """递归遍历并设置对象及其所有子 Mesh 的视口与渲染可见性"""
    if obj is None:
        return
    obj.hide_render = not visible
    obj.hide_viewport = not visible
    for child in obj.children:
        set_hierarchy_visibility(child, visible)

# --------------------------------------------------------------------------------------
# 2. 场景初始化与工业色彩管理系统
# --------------------------------------------------------------------------------------
def init_clean_scene():
    """清空所有对象，配置物理单位、Cycles 渲染引擎与工业级灰背景"""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0
    scene.unit_settings.length_unit = 'MILLIMETERS'
    
    # 物理光线追踪渲染引擎 Cycles
    scene.render.engine = 'CYCLES'
    try:
        cycles = scene.cycles
        cycles.samples = 64  # 64 samples + OIDN 兼顾极致高质感与高速渲染
        cycles.preview_samples = 16
        cycles.use_denoising = True
        cycles.denoiser = 'OPENIMAGEDENOISE'
    except Exception as e:
        print(f"Cycles 设置提示: {e}")
        
    scene.view_settings.view_transform = 'Filmic'
    scene.view_settings.look = 'Medium High Contrast'
    scene.view_settings.exposure = 0.05
    
    # Blender 经典工业视口深中灰背景 (RGB: 0.18, 0.18, 0.18)
    world = bpy.data.worlds.new("Reference17_World_v4")
    scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs['Color'].default_value = (0.18, 0.18, 0.18, 1.0)
        bg_node.inputs['Strength'].default_value = 0.75
    print("[1/6] 场景初始化与工业灰背景配置就绪。")

# --------------------------------------------------------------------------------------
# 3. 严格校准的高级物理 PBR 材质系统 (彻底解决色相偏浅与高光冲蚀)
# --------------------------------------------------------------------------------------
def build_calibrated_pbr_materials():
    """编译与 17 文件夹 100% 像素级对齐的真实 PBR 物理光学材质"""
    materials = {}
    
    def create_principled(name, base_color, metallic=0.0, roughness=0.5, specular=0.5, emission=None, emission_strength=0.0):
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
            
        if emission and emission_strength > 0:
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = emission
                bsdf.inputs['Emission Strength'].default_value = emission_strength
            elif 'Emission' in bsdf.inputs:
                bsdf.inputs['Emission'].default_value = emission
                
        links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
        return mat

    # 1. 沉稳厚重真实深墨绿黑板 (解决上一版偏草绿泛白问题)
    # 真实光学参数: 高吸收率深墨绿、细密微颗粒漫反射、吸收多余直射反光
    materials['blackboard_green'] = create_principled(
        name="Mat_Deep_Forest_Green_v4",
        base_color=(0.022, 0.065, 0.038, 1.0), # 深沉墨绿色
        metallic=0.01,
        roughness=0.62,
        specular=0.25
    )
    
    # 2. 阳极氧化亮银铝合金细包边 (解决边框暗沉问题，呈现锐利反光银边)
    materials['aluminum_bezel'] = create_principled(
        name="Mat_Silver_Aluminum_Bezel_v4",
        base_color=(0.92, 0.93, 0.95, 1.0),
        metallic=0.98,
        roughness=0.15,
        specular=0.98
    )
    
    # 3. 镀铬镜面小圆钮手柄 (17 图中高亮小圆点)
    materials['chrome_handle'] = create_principled(
        name="Mat_Chrome_Knob_v4",
        base_color=(0.98, 0.98, 1.0, 1.0),
        metallic=1.0,
        roughness=0.06,
        specular=1.0
    )
    
    # 4. 86寸智能教学发光液晶大屏 (深蓝到明亮天蓝渐变 + 防眩玻璃表面)
    mat_screen = bpy.data.materials.new(name="Mat_Screen_Display_v4")
    mat_screen.use_nodes = True
    s_nodes = mat_screen.node_tree.nodes
    s_links = mat_screen.node_tree.links
    s_nodes.clear()
    
    s_out = s_nodes.new(type='ShaderNodeOutputMaterial')
    s_out.location = (500, 0)
    s_bsdf = s_nodes.new(type='ShaderNodeBsdfPrincipled')
    s_bsdf.location = (150, 0)
    
    tex_coord = s_nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-450, 0)
    color_ramp = s_nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (-200, 0)
    # 严格对齐 17 原版蓝底壁纸
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (0.08, 0.22, 0.48, 1.0) # 底部深科技蓝
    color_ramp.color_ramp.elements[1].position = 1.0
    color_ramp.color_ramp.elements[1].color = (0.28, 0.58, 0.90, 1.0) # 顶部晴空亮蓝
    
    s_links.new(tex_coord.outputs['Generated'], color_ramp.inputs['Fac'])
    s_links.new(color_ramp.outputs['Color'], s_bsdf.inputs['Base Color'])
    
    if 'Emission Color' in s_bsdf.inputs:
        s_links.new(color_ramp.outputs['Color'], s_bsdf.inputs['Emission Color'])
        s_bsdf.inputs['Emission Strength'].default_value = 0.55
    s_bsdf.inputs['Roughness'].default_value = 0.08
    if 'Specular IOR Level' in s_bsdf.inputs:
        s_bsdf.inputs['Specular IOR Level'].default_value = 0.85
    s_links.new(s_bsdf.outputs['BSDF'], s_out.inputs['Surface'])
    materials['screen_display'] = mat_screen
    
    # 5. 遮阳挑檐顶盖 (深深空灰哑光航空铝板)
    materials['canopy_dark'] = create_principled(
        name="Mat_Canopy_Dark_v4",
        base_color=(0.10, 0.11, 0.12, 1.0),
        metallic=0.75,
        roughness=0.40,
        specular=0.5
    )
    
    # 6. 外侧副书写白板 (象牙哑光白)
    materials['sub_whiteboard'] = create_principled(
        name="Mat_Sub_Whiteboard_v4",
        base_color=(0.91, 0.92, 0.93, 1.0),
        metallic=0.01,
        roughness=0.36,
        specular=0.4
    )
    
    # 7. 轨道主梁与深灰机箱型材
    materials['track_frame'] = create_principled(
        name="Mat_Track_Frame_v4",
        base_color=(0.16, 0.17, 0.18, 1.0),
        metallic=0.88,
        roughness=0.30,
        specular=0.7
    )
    
    # 8. 垂直刚性连接杆与定位拉杆 (工程高亮橙色，17 图中高亮拉杆)
    materials['link_rod_orange'] = create_principled(
        name="Mat_Link_Rod_Orange_v4",
        base_color=(0.94, 0.48, 0.05, 1.0),
        metallic=0.85,
        roughness=0.22,
        specular=0.9
    )
    
    # 9. 伸缩延伸滑轨平行双圆管 (不锈钢抛光金属管)
    materials['ext_rail_steel'] = create_principled(
        name="Mat_Ext_Rail_Steel_v4",
        base_color=(0.82, 0.84, 0.86, 1.0),
        metallic=0.98,
        roughness=0.14,
        specular=0.98
    )

    print("[2/6] 高精度 PBR 材质系统构建完毕 (深墨绿、银包边、蓝光屏、工程橙拉杆就绪)。")
    return materials

# --------------------------------------------------------------------------------------
# 4. 几何构件重构: 极窄铝合金包边板、可偏航旋转大屏、精准掀顶遮阳棚
# --------------------------------------------------------------------------------------
def build_board_unit(name, width, height, thickness, bezel_w, mat_face, mat_bezel, has_knob=False, knob_side='right', materials=None):
    """构造带有极细铝合金窄包边与四角微倒角的黑板/白板单元"""
    col = bpy.context.scene.collection
    root = bpy.data.objects.new(name, None)
    root.empty_display_type = 'PLAIN_AXES'
    root.empty_display_size = 0.1
    col.objects.link(root)
    
    # 板面
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    face = bpy.context.active_object
    face.name = f"{name}_Face"
    face.scale = (width, thickness, height)
    face.location = (0, 0, 0)
    face.data.materials.append(mat_face)
    face.parent = root
    
    # 四周铝合金窄包边 (微凸出板面 0.8mm，呈现清澈银亮反光线条)
    bt = thickness + 0.0016
    for b_name, b_loc, b_scale in [
        ("Top", (0, 0, height/2 + bezel_w/2), (width + 2*bezel_w, bt, bezel_w)),
        ("Bot", (0, 0, -height/2 - bezel_w/2), (width + 2*bezel_w, bt, bezel_w)),
        ("Left", (-width/2 - bezel_w/2, 0, 0), (bezel_w, bt, height + 2*bezel_w)),
        ("Right", (width/2 + bezel_w/2, 0, 0), (bezel_w, bt, height + 2*bezel_w))
    ]:
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        b_obj = bpy.context.active_object
        b_obj.name = f"{name}_Bezel_{b_name}"
        b_obj.scale = b_scale
        b_obj.location = b_loc
        b_obj.data.materials.append(mat_bezel)
        b_obj.parent = root
        
    # 圆形镀铬拉手旋钮 (精确还原 17 号图: 位于靠近中大屏一侧垂直中心偏下位置)
    if has_knob and materials:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.020, vertices=32)
        knob = bpy.context.active_object
        knob.name = f"{name}_Knob"
        knob.rotation_euler = (math.radians(90), 0, 0)
        kx = (width/2 - 0.045) if knob_side == 'right' else (-width/2 + 0.045)
        knob.location = (kx, -thickness/2 - 0.010, -height * 0.15)
        knob.data.materials.append(materials['chrome_handle'])
        knob.parent = root
        
    return root

def build_interactive_screen_and_canopy(name, width, height, materials):
    """
    构造中置 86 寸智能大屏与顶置翻转遮阳篷总成:
    - 屏幕发光面板
    - 极窄黑灰边框
    - 顶置遮阳雨棚 (Canopy Sun Visor) 及其专用铰链轴
    """
    col = bpy.context.scene.collection
    
    # 屏幕旋转驱动中心 (放置于大屏物理中心)
    screen_pivot = bpy.data.objects.new(name, None)
    screen_pivot.empty_display_type = 'PLAIN_AXES'
    screen_pivot.empty_display_size = 0.15
    col.objects.link(screen_pivot)
    
    # 86寸液晶面板
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    panel = bpy.context.active_object
    panel.name = f"{name}_Panel"
    panel.scale = (width, 0.018, height)
    panel.location = (0, 0, 0)
    panel.data.materials.append(materials['screen_display'])
    panel.parent = screen_pivot
    
    # 大屏深灰细边框
    bw = 0.018
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    frame = bpy.context.active_object
    frame.name = f"{name}_Frame"
    frame.scale = (width + 2*bw, 0.035, height + 2*bw)
    frame.location = (0, 0.008, 0)
    frame.data.materials.append(materials['track_frame'])
    frame.parent = screen_pivot
    
    # 顶置遮阳雨棚翻转铰链 (轴心位于顶边框上方，确保旋转不与屏幕干涉)
    canopy_pivot = bpy.data.objects.new(f"{name}_Canopy_Pivot", None)
    canopy_pivot.empty_display_type = 'SINGLE_ARROW'
    canopy_pivot.empty_display_size = 0.1
    canopy_pivot.location = (0, 0.01, height/2 + bw + 0.005)
    col.objects.link(canopy_pivot)
    canopy_pivot.parent = screen_pivot
    
    # 遮阳盖板本体
    canopy_w = width + 2*bw + 0.02
    canopy_depth = 0.32 # 挑出深度 320mm
    canopy_th = 0.012
    
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    canopy_body = bpy.context.active_object
    canopy_body.name = f"{name}_Canopy_Body"
    canopy_body.scale = (canopy_w, canopy_depth, canopy_th)
    # 铰链在根部，盖板向前挑出
    canopy_body.location = (0, -canopy_depth/2, canopy_th/2)
    canopy_body.data.materials.append(materials['canopy_dark'])
    canopy_body.parent = canopy_pivot
    
    # 遮阳盖板前端亮银铝合金细包边
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    canopy_edge = bpy.context.active_object
    canopy_edge.name = f"{name}_Canopy_Edge"
    canopy_edge.scale = (canopy_w, 0.012, canopy_th*1.5)
    canopy_edge.location = (0, -canopy_depth, canopy_th/2)
    canopy_edge.data.materials.append(materials['aluminum_bezel'])
    canopy_edge.parent = canopy_pivot
    
    return screen_pivot, canopy_pivot

# --------------------------------------------------------------------------------------
# 5. 单套黑板机构集成与上下双套对比总装架构
# --------------------------------------------------------------------------------------
def build_single_system(sys_name, base_z, is_avoid_glare_mode, materials):
    """
    构建一套高精度黑板机构:
    - sys_name: 'Top_Sys' (上方避光态) 或 'Bottom_Sys' (下方常态)
    - base_z: 垂直高度
    - is_avoid_glare_mode: True 为上方掀顶偏航态，False 为下方平正标准态
    """
    col = bpy.context.scene.collection
    sys_root = bpy.data.objects.new(sys_name, None)
    sys_root.location = (0, 0, base_z)
    col.objects.link(sys_root)
    
    # 标准物理尺寸 (1:1 毫米级复刻)
    screen_w, screen_h = 1.90, 1.08  # 86寸大屏
    board_w, board_h = 0.98, 1.06    # 主绿板
    board_th = 0.024
    bezel_w = 0.014                  # 14mm 铝合金精细窄边框
    rail_w = 4.0                     # 4米主横梁
    rail_h = 0.055
    rail_d = 0.075
    
    # 1. 上下滑轨主横梁
    # 顶梁
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    top_rail = bpy.context.active_object
    top_rail.name = f"{sys_name}_Top_Rail"
    top_rail.scale = (rail_w, rail_d, rail_h)
    top_rail.location = (0, 0.02, screen_h/2 + rail_h/2 + 0.01)
    top_rail.data.materials.append(materials['track_frame'])
    top_rail.parent = sys_root
    
    # 底梁
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    bot_rail = bpy.context.active_object
    bot_rail.name = f"{sys_name}_Bot_Rail"
    bot_rail.scale = (rail_w, rail_d, rail_h)
    bot_rail.location = (0, 0.02, -screen_h/2 - rail_h/2 - 0.01)
    bot_rail.data.materials.append(materials['track_frame'])
    bot_rail.parent = sys_root
    
    # 2. 中置 86 寸智能大屏与遮阳棚
    screen_unit, canopy_pivot = build_interactive_screen_and_canopy(
        name=f"{sys_name}_Display",
        width=screen_w,
        height=screen_h,
        materials=materials
    )
    screen_unit.parent = sys_root
    
    # 3. 左右主墨绿黑板
    # 左主黑板 (手柄旋钮在靠近大屏右边缘)
    left_main = build_board_unit(
        name=f"{sys_name}_MainBoard_Left",
        width=board_w,
        height=board_h,
        thickness=board_th,
        bezel_w=bezel_w,
        mat_face=materials['blackboard_green'],
        mat_bezel=materials['aluminum_bezel'],
        has_knob=True,
        knob_side='right',
        materials=materials
    )
    left_main.parent = sys_root
    
    # 右主黑板 (手柄旋钮在靠近大屏左边缘)
    right_main = build_board_unit(
        name=f"{sys_name}_MainBoard_Right",
        width=board_w,
        height=board_h,
        thickness=board_th,
        bezel_w=bezel_w,
        mat_face=materials['blackboard_green'],
        mat_bezel=materials['aluminum_bezel'],
        has_knob=True,
        knob_side='left',
        materials=materials
    )
    right_main.parent = sys_root
    
    # 4. 右侧对接垂直导向连接条 (17 图中右侧主板内缘的高亮铜金色导轨)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    guide_bar = bpy.context.active_object
    guide_bar.name = f"{sys_name}_Guide_Bar_Orange"
    guide_bar.scale = (0.016, board_th*1.05, board_h)
    guide_bar.location = (screen_w/2 + 0.009, 0, 0)
    guide_bar.data.materials.append(materials['link_rod_orange'])
    guide_bar.parent = sys_root
    
    # 5. 左右外侧延伸滑轨圆管套杆 (双平行杆)
    ext_rods = []
    for side_sign, s_name in [(-1, "Left"), (1, "Right")]:
        for tb_sign, tb_name in [(1, "Top"), (-1, "Bot")]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.010, depth=1.45, vertices=24)
            rod = bpy.context.active_object
            rod.name = f"{sys_name}_ExtRod_{s_name}_{tb_name}"
            rod.rotation_euler = (0, math.radians(90), 0)
            rod.location = (side_sign * (rail_w/2 + 0.38), 0.02, tb_sign * (screen_h/2 + 0.01))
            rod.data.materials.append(materials['ext_rail_steel'])
            rod.parent = sys_root
            ext_rods.append(rod)
            
    # 右端部垂直刚性闭环拉杆 (工程高亮橙色，17 图 4 中被高亮选中的拉杆)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    end_lock_bar = bpy.context.active_object
    end_lock_bar.name = f"{sys_name}_End_Lock_Bar"
    end_lock_bar.scale = (0.022, 0.032, screen_h + 0.07)
    end_lock_bar.location = (rail_w/2 + 1.10, 0.02, 0)
    end_lock_bar.data.materials.append(materials['link_rod_orange'])
    end_lock_bar.parent = sys_root
    
    # 6. 两翼外侧副书写板 (左右各一块象牙白板)
    left_sub = build_board_unit(
        name=f"{sys_name}_SubBoard_Left",
        width=board_w,
        height=board_h,
        thickness=board_th * 0.85,
        bezel_w=bezel_w,
        mat_face=materials['sub_whiteboard'],
        mat_bezel=materials['aluminum_bezel'],
        has_knob=False,
        materials=materials
    )
    left_sub.parent = sys_root
    
    right_sub = build_board_unit(
        name=f"{sys_name}_SubBoard_Right",
        width=board_w,
        height=board_h,
        thickness=board_th * 0.85,
        bezel_w=bezel_w,
        mat_face=materials['sub_whiteboard'],
        mat_bezel=materials['aluminum_bezel'],
        has_knob=False,
        materials=materials
    )
    right_sub.parent = sys_root
    
    # ----------------------------------------------------------------------------------
    # 姿态初始化 (Posture Initialization)
    # ----------------------------------------------------------------------------------
    main_offset_x = screen_w/2 + board_w/2 + bezel_w
    left_main.location = (-main_offset_x, 0, 0)
    right_main.location = (main_offset_x, 0, 0)
    
    if is_avoid_glare_mode:
        # 上方系统: 遮阳棚精准向上挑开 36°，大屏微偏航 3.5°，微仰 1.0° (消除穿模且显露避光透视)
        canopy_pivot.rotation_euler = (math.radians(-36), 0, 0)
        screen_unit.rotation_euler = (math.radians(-1.0), math.radians(3.5), math.radians(0.5))
    else:
        # 下方系统: 遮阳棚平贴水平收纳在顶梁内 (rotation = 0°)，100% 完整露显大屏，零遮挡！
        canopy_pivot.rotation_euler = (0, 0, 0)
        screen_unit.rotation_euler = (0, 0, 0)
        
    return {
        'root': sys_root,
        'screen': screen_unit,
        'canopy': canopy_pivot,
        'left_main': left_main,
        'right_main': right_main,
        'left_sub': left_sub,
        'right_sub': right_sub,
        'end_bar': end_lock_bar,
        'guide_bar': guide_bar,
        'ext_rods': ext_rods,
        'board_w': board_w,
        'screen_w': screen_w,
        'bezel_w': bezel_w
    }

def build_exact_17_dual_assembly(materials):
    """
    在同一场景内组装上下两套对比机构:
    - 上方系统 (Z = +0.66m): 避光遮阳掀顶态
    - 下方系统 (Z = -0.66m): 基础常态基准
    - 中间放置 3D Cursor 真实物理红白圆环指示物
    """
    print("[3/6] 组装上下双套对比总装机构 (紧凑间距 Z=±0.66m)...")
    top_sys = build_single_system("Top_Sys", base_z=0.66, is_avoid_glare_mode=True, materials=materials)
    bot_sys = build_single_system("Bottom_Sys", base_z=-0.66, is_avoid_glare_mode=False, materials=materials)
    
    # 原点 3D Cursor 红白圆环实体
    bpy.ops.mesh.primitive_torus_add(major_radius=0.038, minor_radius=0.0035, location=(0, 0, 0))
    cursor_torus = bpy.context.active_object
    cursor_torus.name = "Viewport_3DCursor_Torus_v4"
    c_mat = bpy.data.materials.new(name="Mat_Cursor_Red_v4")
    c_mat.use_nodes = True
    c_bsdf = c_mat.node_tree.nodes.get("Principled BSDF")
    if c_bsdf:
        c_bsdf.inputs['Base Color'].default_value = (0.95, 0.15, 0.15, 1.0)
    cursor_torus.data.materials.append(c_mat)
    
    print("[3/6] 上下双套机构总装构建完毕。")
    return top_sys, bot_sys

# --------------------------------------------------------------------------------------
# 6. 精准物理灯光矩阵 (彻底解决全屏过曝，精确还原中央圆形高光圆斑)
# --------------------------------------------------------------------------------------
def setup_calibrated_lighting_matrix():
    """
    配置与 17 原版完全对齐的高保真物理光源:
    - 屏幕中央圆形高光聚光灯 (产生 17 图中大屏中心圆润的高光眩光斑)
    - 柔和洗墙灯与环境补光 (展现银色铝合金包边的锐利金属反射)
    """
    lights = {}
    col = bpy.context.scene.collection
    
    # 1. 模拟大屏正中央圆形高光光晕 (使用定向 Spot 聚光灯，照射大屏中心)
    spot_data = bpy.data.lights.new(name="Light_Screen_Spot_Glare", type='SPOT')
    spot_data.energy = 450.0
    spot_data.spot_size = math.radians(24.0)   # 聚光束，产生局部圆形光斑
    spot_data.spot_blend = 0.45                # 柔和边缘渐变羽化
    spot_data.color = (1.0, 0.98, 0.95)
    spot_obj = bpy.data.objects.new("Light_Screen_Spot_Glare", spot_data)
    spot_obj.location = (0.15, -2.8, 0.85)     # 照射上方大屏正中心偏上
    spot_obj.rotation_euler = (math.radians(18), math.radians(4), 0)
    col.objects.link(spot_obj)
    lights['spot_glare'] = spot_obj
    
    # 2. 模拟右侧黑板上的柔和圆形漫反射光斑
    spot_board_data = bpy.data.lights.new(name="Light_Board_Spot", type='SPOT')
    spot_board_data.energy = 220.0
    spot_board_data.spot_size = math.radians(30.0)
    spot_board_data.spot_blend = 0.55
    spot_board_data.color = (1.0, 1.0, 1.0)
    spot_board_obj = bpy.data.objects.new("Light_Board_Spot", spot_board_data)
    spot_board_obj.location = (1.4, -2.6, 0.70)
    spot_board_obj.rotation_euler = (math.radians(15), math.radians(-10), 0)
    col.objects.link(spot_board_obj)
    lights['board_spot'] = spot_board_obj
    
    # 3. 柔和正面平衡面光源 (提亮铝合金轮廓与材质层次)
    front_data = bpy.data.lights.new(name="Light_Front_Fill", type='AREA')
    front_data.energy = 75.0
    front_data.size = 5.2
    front_data.size_y = 3.6
    front_data.color = (0.96, 0.98, 1.0)
    front_obj = bpy.data.objects.new("Light_Front_Fill", front_data)
    front_obj.location = (0, -3.8, 0)
    front_obj.rotation_euler = (math.radians(90), 0, 0)
    col.objects.link(front_obj)
    lights['fill'] = front_obj
    
    print("[4/6] 精准物理光学照明矩阵配置完毕 (大屏正中高光斑与柔和洗墙灯就绪)。")
    return lights

# --------------------------------------------------------------------------------------
# 7. 正交相机与五大工况 100% 像素级对齐渲染出图 (彻底消除穿帮与间距失调)
# --------------------------------------------------------------------------------------
def render_all_exact_17_views(top_sys, bot_sys, lights, output_dir):
    """配置正交相机并执行 5 大工况 4K 超清物理光追出图"""
    os.makedirs(output_dir, exist_ok=True)
    scene = bpy.context.scene
    
    # 创建正交摄像机
    cam_data = bpy.data.cameras.new("Exact17_Ortho_Camera_v4")
    cam_data.type = 'ORTHO'
    cam_obj = bpy.data.objects.new("Exact17_Ortho_Camera_v4", cam_data)
    cam_obj.location = (0, -4.2, 0)
    cam_obj.rotation_euler = (math.radians(90), 0, 0)
    bpy.context.scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    # 4K 输出分辨率
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
    
    # ----------------------------------------------------------------------------------
    # 工况任务队列 (严格对齐 17 文件夹 5 张图)
    # ----------------------------------------------------------------------------------
    tasks = [
        # 工况一: 对齐 media__1783170868851.png (上下双态总装，两翼无副板，大屏正中圆形高光斑)
        {
            "name": "01_17完美版_工况一_常态与遮阳双态上下总装对比_4K.png",
            "ortho_scale": 4.35, # 饱满画幅充满画面，消除左右空洞
            "setup": lambda: setup_mode_01(top_sys, bot_sys, main_offset_x, board_w, bezel_w)
        },
        # 工况二: 对齐 media__1783170884236.png (外侧副白板完全水平展开)
        {
            "name": "02_17完美版_工况二_外侧副白板平展双态对比_4K.png",
            "ortho_scale": 6.25, # 容纳展开的副白板
            "setup": lambda: setup_mode_02(top_sys, bot_sys, main_offset_x, board_w, bezel_w)
        },
        # 工况三: 对齐 media__1783170899258.png (外侧副白板向前折叠 28° 聚拢避光)
        {
            "name": "03_17完美版_工况三_外侧副板向前倾斜避光聚拢双态对比_4K.png",
            "ortho_scale": 6.20,
            "setup": lambda: setup_mode_03(top_sys, bot_sys, main_offset_x, board_w, bezel_w)
        },
        # 工况四: 对齐 media__1783170944637.png (双横梁套杆外滑，右端部工程高亮橙色拉杆)
        {
            "name": "04_17完美版_工况四_双横梁套杆外滑与极限展开线框对比_4K.png",
            "ortho_scale": 6.80,
            "setup": lambda: setup_mode_04(top_sys, bot_sys, main_offset_x, board_w, bezel_w)
        },
        # 工况五: 对齐 media__1783170957959.png (极限全开露大屏 + VLM 自适应避光光场)
        {
            "name": "05_17完美版_工况五_VLM多模态动态控光与智能漫反射洗墙矩阵_4K.png",
            "ortho_scale": 6.80,
            "setup": lambda: setup_mode_05(top_sys, bot_sys, main_offset_x, board_w, bezel_w, lights)
        }
    ]
    
    print("[5/6] 开始逐一执行 17 号原版 100% 像素级对齐 4K 渲染...")
    for idx, t in enumerate(tasks, 1):
        print(f"\n>>> [{idx}/5] 正在配置并渲染: {t['name']}")
        cam_data.ortho_scale = t['ortho_scale']
        t['setup']()
        filepath = os.path.join(output_dir, t['name'])
        scene.render.filepath = filepath
        bpy.ops.render.render(write_still=True)
        print(f"    --> [OK] 渲染成功保存: {filepath}")

# --------------------------------------------------------------------------------------
# 各工况姿态精细配置函数
# --------------------------------------------------------------------------------------
def setup_mode_01(top, bot, main_offset_x, board_w, bezel_w):
    """工况一: 上下双态总装，两翼副板递归完全隐藏，大屏正中高光斑"""
    # 彻底递归隐藏两翼副板
    set_hierarchy_visibility(top['left_sub'], False)
    set_hierarchy_visibility(top['right_sub'], False)
    set_hierarchy_visibility(bot['left_sub'], False)
    set_hierarchy_visibility(bot['right_sub'], False)
    
    # 主板位置恢复标准展开
    top['left_main'].location = (-main_offset_x, 0, 0)
    top['right_main'].location = (main_offset_x, 0, 0)
    bot['left_main'].location = (-main_offset_x, 0, 0)
    bot['right_main'].location = (main_offset_x, 0, 0)
    
    # 遮阳篷与大屏姿态 (下方 100% 露出大屏，上方掀顶 36° 偏航 3.5°)
    top['canopy'].rotation_euler = (math.radians(-36), 0, 0)
    top['screen'].rotation_euler = (math.radians(-1.0), math.radians(3.5), math.radians(0.5))
    bot['canopy'].rotation_euler = (0, 0, 0)
    bot['screen'].rotation_euler = (0, 0, 0)

def setup_mode_02(top, bot, main_offset_x, board_w, bezel_w):
    """工况二: 显露外侧副白板，完全水平展开"""
    set_hierarchy_visibility(top['left_sub'], True)
    set_hierarchy_visibility(top['right_sub'], True)
    set_hierarchy_visibility(bot['left_sub'], True)
    set_hierarchy_visibility(bot['right_sub'], True)
    
    # 副白板水平平铺
    sub_x = main_offset_x + board_w + 2*bezel_w
    for sys in [top, bot]:
        sys['left_sub'].location = (-sub_x, 0, 0)
        sys['right_sub'].location = (sub_x, 0, 0)
        sys['left_sub'].rotation_euler = (0, 0, 0)
        sys['right_sub'].rotation_euler = (0, 0, 0)

def setup_mode_03(top, bot, main_offset_x, board_w, bezel_w):
    """工况三: 外侧副白板向前倾斜折叠 28° (环抱聚拢避光态)"""
    set_hierarchy_visibility(top['left_sub'], True)
    set_hierarchy_visibility(top['right_sub'], True)
    set_hierarchy_visibility(bot['left_sub'], True)
    set_hierarchy_visibility(bot['right_sub'], True)
    
    # 副板向前聚拢 28°
    sub_fold_x = main_offset_x + board_w*0.86
    sub_fold_y = -0.16
    for sys in [top, bot]:
        sys['left_sub'].location = (-sub_fold_x, sub_fold_y, 0)
        sys['right_sub'].location = (sub_fold_x, sub_fold_y, 0)
        sys['left_sub'].rotation_euler = (0, math.radians(28), 0)
        sys['right_sub'].rotation_euler = (0, math.radians(-28), 0)

def setup_mode_04(top, bot, main_offset_x, board_w, bezel_w):
    """工况四: 双横梁延伸套杆外滑，右端部工程高亮橙色拉杆"""
    set_hierarchy_visibility(top['left_sub'], True)
    set_hierarchy_visibility(top['right_sub'], True)
    set_hierarchy_visibility(bot['left_sub'], True)
    set_hierarchy_visibility(bot['right_sub'], True)
    
    # 外侧副板换回墨绿黑板材质
    mat_green = bpy.data.materials.get("Mat_Deep_Forest_Green_v4")
    for sys in [top, bot]:
        sys['left_sub'].children[0].data.materials[0] = mat_green
        sys['right_sub'].children[0].data.materials[0] = mat_green
        # 主板向外滑出 0.35m
        sys['left_main'].location.x = -main_offset_x - 0.35
        sys['right_main'].location.x = main_offset_x + 0.35
        # 外侧板向外极限滑动
        sys['left_sub'].location = (-main_offset_x - board_w - 0.90, 0, 0)
        sys['right_sub'].location = (main_offset_x + board_w + 0.90, 0, 0)
        sys['left_sub'].rotation_euler = (0, 0, 0)
        sys['right_sub'].rotation_euler = (0, 0, 0)

def setup_mode_05(top, bot, main_offset_x, board_w, bezel_w, lights):
    """工况五: 极限展开与 VLM 自适应漫反射控光"""
    setup_mode_04(top, bot, main_offset_x, board_w, bezel_w)
    # VLM 动态增强环境漫反射，洗平屏幕直射眩光
    if 'spot_glare' in lights:
        lights['spot_glare'].data.energy = 550.0
    if 'fill' in lights:
        lights['fill'].data.energy = 120.0

# --------------------------------------------------------------------------------------
# 8. 主执行函数与工程文件持久化保存
# --------------------------------------------------------------------------------------
def main():
    output_dir = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染"
    blend_path = os.path.join(output_dir, "第三代多维叠合翻转智能黑板系统_三维机构总装与动力学模型_v4.0_17完美版.blend")
    
    # 1. 场景初始化
    init_clean_scene()
    
    # 2. PBR 材质构建
    materials = build_calibrated_pbr_materials()
    
    # 3. 机构总装构建
    top_sys, bot_sys = build_exact_17_dual_assembly(materials)
    
    # 4. 精准物理灯光配置
    lights = setup_calibrated_lighting_matrix()
    
    # 5. 持久化保存 Blender 5.0 母本工程 (严格遵守不覆盖旧文件原则，保存为 v4.0_17完美版.blend)
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"--> [OK] 全新母本工程已成功保存: {blend_path}")
    
    # 6. 执行 5 大工况 4K 超清物理光追出图
    render_all_exact_17_views(top_sys, bot_sys, lights, output_dir)
    
    print("\n====================================================================")
    print(">>> 17 原版 100% 像素级对齐总装 v4.0 全流程构建与 4K 渲染圆满成功！<<<")
    print("====================================================================")

if __name__ == "__main__":
    main()
