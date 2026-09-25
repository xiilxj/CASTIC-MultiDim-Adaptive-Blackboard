# -*- coding: utf-8 -*-
"""
第三代多维叠合翻转全覆盖与三维自洁侧滑智能黑板系统 (Z系列)
Blender 5.0 参数化 3D 建模、物理装配与多工况光环境渲染脚本 (v1.2 工业级精修版)
设计标准: 严格契合 AutoCAD 2026 v1.2 工程图纸 (GH-GEN3-ASM-03)
机构拓扑: 对角线双铰链正交解耦 (Diagonal Topology) + 双横梁伸缩套杆 + 三大工况驱动
"""

import bpy
import math
import mathutils
from mathutils import Vector
import os
import sys

# -----------------------------------------------------------------------------
# 0. 环境初始化与场景清空
# -----------------------------------------------------------------------------
def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for block in bpy.data.meshes:
        bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        bpy.data.materials.remove(block)
    for block in bpy.data.cameras:
        bpy.data.cameras.remove(block)
    for block in bpy.data.lights:
        bpy.data.lights.remove(block)
    for block in bpy.data.collections:
        if block.name != "Collection":
            bpy.data.collections.remove(block)

reset_scene()

scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

# -----------------------------------------------------------------------------
# 1. 材质着色器系统 (PBR Shaders)
# -----------------------------------------------------------------------------
def create_pbr_material(name, base_color, metallic=0.0, roughness=0.5, clearcoat=0.0, emission_color=(0,0,0,1), emission_strength=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    node_bsdf.inputs['Base Color'].default_value = base_color
    node_bsdf.inputs['Metallic'].default_value = metallic
    node_bsdf.inputs['Roughness'].default_value = roughness
    if 'Coat Weight' in node_bsdf.inputs:
        node_bsdf.inputs['Coat Weight'].default_value = clearcoat
    elif 'Clearcoat' in node_bsdf.inputs:
        node_bsdf.inputs['Clearcoat'].default_value = clearcoat
        
    if emission_strength > 0:
        if 'Emission Color' in node_bsdf.inputs:
            node_bsdf.inputs['Emission Color'].default_value = emission_color
            node_bsdf.inputs['Emission Strength'].default_value = emission_strength
        elif 'Emission' in node_bsdf.inputs:
            node_bsdf.inputs['Emission'].default_value = emission_color
            
    links.new(node_bsdf.outputs['BSDF'], node_output.inputs['Surface'])
    return mat

# 高保真工程 PBR 材质
mat_board_green = create_pbr_material("Mat_Blackboard_Green", (0.02, 0.08, 0.04, 1.0), metallic=0.02, roughness=0.65) # 经典墨绿磨砂书写板面
mat_board_white = create_pbr_material("Mat_Enamel_White", (0.92, 0.93, 0.95, 1.0), metallic=0.05, roughness=0.22, clearcoat=0.3) # 搪瓷投影白板
mat_screen_glass = create_pbr_material("Mat_Screen_Glass", (0.012, 0.015, 0.025, 1.0), metallic=0.2, roughness=0.05, clearcoat=1.0) # 86寸大屏偏光玻璃
mat_frame_dark = create_pbr_material("Mat_Aluminum_Dark", (0.08, 0.09, 0.11, 1.0), metallic=0.85, roughness=0.32) # 6063-T5深灰阳极氧化铝型材
mat_steel = create_pbr_material("Mat_Stainless_Steel", (0.88, 0.89, 0.92, 1.0), metallic=0.98, roughness=0.12) # 304不锈钢高光套杆
mat_orange = create_pbr_material("Mat_Highlight_Orange", (0.98, 0.34, 0.02, 1.0), metallic=0.2, roughness=0.25) # 关键机构高亮工程橙
mat_wall = create_pbr_material("Mat_Classroom_Wall", (0.86, 0.87, 0.85, 1.0), metallic=0.0, roughness=0.85) # 教室乳胶漆背景墙
mat_floor = create_pbr_material("Mat_Floor_Wood", (0.36, 0.20, 0.10, 1.0), metallic=0.0, roughness=0.38) # 讲台实木地板
mat_bezel = create_pbr_material("Mat_Screen_Bezel", (0.03, 0.03, 0.04, 1.0), metallic=0.8, roughness=0.4) # 大屏外壳
mat_indicator = create_pbr_material("Mat_LED_Green", (0.1, 1.0, 0.2, 1.0), emission_color=(0.1, 1.0, 0.2, 1.0), emission_strength=5.0)

# -----------------------------------------------------------------------------
# 2. 教室环境基底建模
# -----------------------------------------------------------------------------
# 讲台实木地板
bpy.ops.mesh.primitive_plane_add(size=18.0, location=(0, 2.0, -0.9))
floor = bpy.context.active_object
floor.name = "Classroom_Floor"
floor.scale = (1.2, 0.8, 1.0)
floor.data.materials.append(mat_floor)

# 教室背景墙
bpy.ops.mesh.primitive_plane_add(size=18.0, location=(0, -0.10, 1.2), rotation=(math.radians(90), 0, 0))
back_wall = bpy.context.active_object
back_wall.name = "Classroom_Back_Wall"
back_wall.scale = (1.2, 0.6, 1.0)
back_wall.data.materials.append(mat_wall)

# -----------------------------------------------------------------------------
# 3. 智能黑板基准固定框架与 86 寸大屏
# -----------------------------------------------------------------------------
base_assembly = bpy.data.objects.new("Assembly_Base_Frame", None)
scene.collection.objects.link(base_assembly)

# 3.1 86寸大屏外壳 (X in [-1.0, 1.0], Y centered at 0.025, Z in [-0.6, 0.6])
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.025, 0))
screen_body = bpy.context.active_object
screen_body.name = "Screen_86Inch_Body"
screen_body.scale = (2.0, 0.05, 1.2)
screen_body.data.materials.append(mat_bezel)
screen_body.parent = base_assembly

# 液晶玻璃显示区 (朝向 +Y)
bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, 0.051, 0), rotation=(math.radians(90), 0, 0))
screen_glass = bpy.context.active_object
screen_glass.name = "Screen_Glass_Surface"
screen_glass.scale = (1.90, 1.0, 1.07)
screen_glass.data.materials.append(mat_screen_glass)
screen_glass.parent = screen_body

# 右内边框伺服电机机构 (主动偏光膜驱动接口)
bpy.ops.mesh.primitive_cylinder_add(radius=0.016, depth=0.08, location=(0.95, 0.055, 0.45))
servo_motor = bpy.context.active_object
servo_motor.name = "Screen_Polarizer_Servo"
servo_motor.data.materials.append(mat_orange)
servo_motor.parent = screen_body

# 状态指示灯
bpy.ops.mesh.primitive_cylinder_add(radius=0.005, depth=0.01, location=(0.96, 0.052, -0.56), rotation=(math.radians(90), 0, 0))
led_indicator = bpy.context.active_object
led_indicator.name = "Screen_Status_LED"
led_indicator.data.materials.append(mat_indicator)
led_indicator.parent = screen_body

# 3.2 上下双横梁铝合金主滑槽导轨 (长 4.0m, Z = ±0.63m)
def create_rail(name, z_pos, has_canopy=False):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.045, z_pos))
    rail = bpy.context.active_object
    rail.name = name
    rail.scale = (4.0, 0.07, 0.06)
    rail.data.materials.append(mat_frame_dark)
    rail.parent = base_assembly
    
    # 顶部卷轴式遮光雨棚 (Canopy)
    if has_canopy:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=4.02, location=(0, 0.075, z_pos + 0.04), rotation=(0, math.radians(90), 0))
        canopy = bpy.context.active_object
        canopy.name = "Top_Canopy_Roll"
        canopy.data.materials.append(mat_frame_dark)
        canopy.parent = rail
    return rail

rail_top = create_rail("Main_Rail_Top", 0.63, has_canopy=True)
rail_bottom = create_rail("Main_Rail_Bottom", -0.63, has_canopy=False)

# -----------------------------------------------------------------------------
# 4. 机构学侧滑组件与伸缩套杆 (Slide System)
# -----------------------------------------------------------------------------
# 左侧滑架空物体 (基准位置在 X = -2.0m)
ctrl_slide_L = bpy.data.objects.new("Ctrl_Slide_Left", None)
ctrl_slide_L.empty_display_type = 'SINGLE_ARROW'
ctrl_slide_L.empty_display_size = 0.25
ctrl_slide_L.location = (-2.0, 0.065, 0)
scene.collection.objects.link(ctrl_slide_L)
ctrl_slide_L.parent = base_assembly

# 右侧滑架空物体 (基准位置在 X = +2.0m)
ctrl_slide_R = bpy.data.objects.new("Ctrl_Slide_Right", None)
ctrl_slide_R.empty_display_type = 'SINGLE_ARROW'
ctrl_slide_R.empty_display_size = 0.25
ctrl_slide_R.location = (2.0, 0.065, 0)
scene.collection.objects.link(ctrl_slide_R)
ctrl_slide_R.parent = base_assembly

# 4.1 双横梁不锈钢伸缩内套杆组件 (在基准机架与侧滑端部之间跨接)
# 左侧伸缩内套杆 (两根: 上 Z=0.63, 下 Z=-0.63)
rods_L = []
for z_pos in [0.63, -0.63]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.014, depth=1.0, location=(-2.0, 0.045, z_pos), rotation=(0, math.radians(90), 0))
    rod = bpy.context.active_object
    rod.name = f"Telescopic_Rod_L_{'Top' if z_pos>0 else 'Btm'}"
    rod.data.materials.append(mat_steel)
    rod.parent = base_assembly
    rods_L.append(rod)

# 右侧伸缩内套杆
rods_R = []
for z_pos in [0.63, -0.63]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.014, depth=1.0, location=(2.0, 0.045, z_pos), rotation=(0, math.radians(90), 0))
    rod = bpy.context.active_object
    rod.name = f"Telescopic_Rod_R_{'Top' if z_pos>0 else 'Btm'}"
    rod.data.materials.append(mat_steel)
    rod.parent = base_assembly
    rods_R.append(rod)

# 4.2 外端部高刚性垂直拉杆 (End Tie Rod) —— 高亮工程橙！
# 随滑架平移, 位于滑块最外端
def create_end_tie_rod(side_sign, ctrl_slide):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    tie_rod = bpy.context.active_object
    tie_rod.name = f"End_Tie_Rod_{'L' if side_sign<0 else 'R'}"
    tie_rod.scale = (0.025, 0.045, 1.32)
    tie_rod.data.materials.append(mat_orange)
    tie_rod.parent = ctrl_slide
    return tie_rod

end_rod_L = create_end_tie_rod(-1, ctrl_slide_L)
end_rod_R = create_end_tie_rod(1, ctrl_slide_R)

# -----------------------------------------------------------------------------
# 5. 对角线双铰链与双层超薄黑板模组 (成二，两折叠并成)
# -----------------------------------------------------------------------------
def build_diagonal_double_blackboard(side_sign, ctrl_slide):
    # 5.1 翻转主铰链控制器 (里面的外侧, 对角线拓扑点 1)
    ctrl_flip = bpy.data.objects.new(f"Ctrl_Hinge_Flip_{'L' if side_sign<0 else 'R'}", None)
    ctrl_flip.empty_display_type = 'ARROWS'
    ctrl_flip.empty_display_size = 0.2
    ctrl_flip.location = (0, 0, 0)
    scene.collection.objects.link(ctrl_flip)
    ctrl_flip.parent = ctrl_slide
    
    # 外侧主铰链垂直轴座 (轴径 36mm) —— 橙色高亮！
    bpy.ops.mesh.primitive_cylinder_add(radius=0.018, depth=1.20, location=(0, 0, 0))
    hinge_main_post = bpy.context.active_object
    hinge_main_post.name = f"Hinge_Main_Post_{'L' if side_sign<0 else 'R'}"
    hinge_main_post.data.materials.append(mat_orange)
    hinge_main_post.parent = ctrl_flip
    
    # 5.2 内层主黑板 (翻转板: 宽 1.0m, 高 1.16m, 厚 12mm)
    # 从外侧铰链向中心延伸: 局部中心在 X = -side_sign * 0.5m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-side_sign * 0.5, 0.008, 0))
    main_board = bpy.context.active_object
    main_board.name = f"Main_Board_{'L' if side_sign<0 else 'R'}"
    main_board.scale = (1.0, 0.012, 1.16)
    main_board.data.materials.append(mat_board_green)
    main_board.parent = ctrl_flip
    
    # 5.3 折叠副铰链控制器 (外面的内侧, 对角线拓扑点 2)
    # 设在内层主黑板的内端: 局部坐标 X = -side_sign * 1.0m, Y = 0.018m
    ctrl_fold = bpy.data.objects.new(f"Ctrl_Hinge_Fold_{'L' if side_sign<0 else 'R'}", None)
    ctrl_fold.empty_display_type = 'SPHERE'
    ctrl_fold.empty_display_size = 0.1
    ctrl_fold.location = (-side_sign * 1.0, 0.018, 0)
    scene.collection.objects.link(ctrl_fold)
    ctrl_fold.parent = ctrl_flip
    
    # 内侧折叠铰链垂直轴座 —— 橙色高亮！
    bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=1.18, location=(0, 0, 0))
    hinge_fold_post = bpy.context.active_object
    hinge_fold_post.name = f"Hinge_Fold_Post_{'L' if side_sign<0 else 'R'}"
    hinge_fold_post.data.materials.append(mat_orange)
    hinge_fold_post.parent = ctrl_fold
    
    # 5.4 外层副黑板 (折叠板: 宽 1.0m, 高 1.16m, 厚 12mm)
    fold_pivot = bpy.data.objects.new(f"Fold_Pivot_{'L' if side_sign<0 else 'R'}", None)
    scene.collection.objects.link(fold_pivot)
    fold_pivot.parent = ctrl_fold
    
    # 默认叠合态: 从折叠轴向外折回贴合在主板前方 (中心局部 X = side_sign * 0.5m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side_sign * 0.5, 0.010, 0))
    fold_board = bpy.context.active_object
    fold_board.name = f"Fold_Board_{'L' if side_sign<0 else 'R'}"
    fold_board.scale = (1.0, 0.012, 1.16)
    fold_board.data.materials.append(mat_board_green)
    fold_board.parent = fold_pivot
    
    # 副板内侧复合防眩白板/投影板 (朝向大屏或外展)
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(side_sign * 0.5, 0.017, 0), rotation=(math.radians(90), 0, 0))
    chalk_face = bpy.context.active_object
    chalk_face.name = f"Chalk_Surface_{'L' if side_sign<0 else 'R'}"
    chalk_face.scale = (0.98, 1.0, 1.14)
    chalk_face.data.materials.append(mat_board_white)
    chalk_face.parent = fold_board
    
    return ctrl_flip, fold_pivot

flip_L, fold_L = build_diagonal_double_blackboard(-1, ctrl_slide_L)
flip_R, fold_R = build_diagonal_double_blackboard(1, ctrl_slide_R)

# -----------------------------------------------------------------------------
# 6. 教室光环境系统设计 (侧窗斜向强光 + 漫射补光)
# -----------------------------------------------------------------------------
# 6.1 侧窗主日光 (从左前方斜向射入，入射角约35°，产生典型眩光反射)
bpy.ops.object.light_add(type='SUN', location=(-7.0, 4.0, 4.5))
sun = bpy.context.active_object
sun.name = "Sun_Window_Light"
sun.data.energy = 4.2
sun.data.angle = math.radians(6.0)
sun.rotation_euler = (math.radians(52), math.radians(-16), math.radians(-65))

# 6.2 教室天花板漫射柔光
bpy.ops.object.light_add(type='AREA', location=(0, 3.2, 3.2))
ceiling_light = bpy.context.active_object
ceiling_light.name = "Ceiling_Diffuse_Light"
ceiling_light.data.energy = 400.0
ceiling_light.data.size = 3.5
ceiling_light.data.size_y = 7.0
ceiling_light.rotation_euler = (math.radians(20), 0, 0)

# 6.3 讲台前方补光
bpy.ops.object.light_add(type='AREA', location=(0, 4.5, 0.5))
fill_light = bpy.context.active_object
fill_light.name = "Front_Fill_Light"
fill_light.data.energy = 150.0
fill_light.data.size = 4.0
fill_light.rotation_euler = (0, 0, 0)

# -----------------------------------------------------------------------------
# 7. 摄像机与智能视线自动盯瞄系统 (Look-At System)
# -----------------------------------------------------------------------------
bpy.ops.object.camera_add(location=(0, 5.0, 0.25))
cam = bpy.context.active_object
cam.name = "Main_Camera"
cam.data.lens = 45 # 45mm黄金透视焦距
scene.camera = cam

def camera_look_at(camera_obj, target_point):
    """使用精准向量变换锁定观察目标点，彻底杜绝角度偏航与黑屏"""
    direction = target_point - camera_obj.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera_obj.rotation_euler = rot_quat.to_euler()

# -----------------------------------------------------------------------------
# 8. 渲染引擎与 4K 超清配置 (BLENDER_EEVEE 硬件加速)
# -----------------------------------------------------------------------------
scene.render.engine = 'BLENDER_EEVEE'
if hasattr(scene, 'eevee'):
    try:
        scene.eevee.taa_render_samples = 64
        scene.eevee.use_gtao = True
        scene.eevee.use_bloom = True
        scene.eevee.use_ssr = True
    except:
        pass

scene.render.resolution_x = 3840
scene.render.resolution_y = 2160
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.color_depth = '8'

# -----------------------------------------------------------------------------
# 9. 工况动作驱动函数与渲染管线
# -----------------------------------------------------------------------------
output_dir = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染"
os.makedirs(output_dir, exist_ok=True)

def update_telescopic_rods(slide_dist_L, slide_dist_R):
    """动态更新双横梁伸缩套杆的位置与伸出长度"""
    # 左侧伸缩套杆横跨在 X = [-2.0, -2.0 - slide_dist_L]
    for rod in rods_L:
        if slide_dist_L > 0.05:
            rod.location.x = -2.0 - (slide_dist_L / 2.0)
            rod.scale.z = slide_dist_L # 延展长度
        else:
            rod.location.x = -2.0
            rod.scale.z = 0.01 # 收缩隐藏于主轨内
            
    for rod in rods_R:
        if slide_dist_R > 0.05:
            rod.location.x = 2.0 + (slide_dist_R / 2.0)
            rod.scale.z = slide_dist_R
        else:
            rod.location.x = 2.0
            rod.scale.z = 0.01

def apply_state(state):
    """根据指定工况快速驱动模型铰链、滑动与折叠角度"""
    if state == "COND1_COVERED":
        # 工况一【初始闭合·市面主流全覆盖形态 4000mm】
        # 侧滑收缩 (X=±2.0m), 翻转 0°, 折叠副板向内铺开 180° 封死 86 寸大屏
        ctrl_slide_L.location = (-2.0, 0.065, 0)
        ctrl_slide_R.location = (2.0, 0.065, 0)
        update_telescopic_rods(0.0, 0.0)
        flip_L.rotation_euler = (0, 0, 0)
        flip_R.rotation_euler = (0, 0, 0)
        fold_L.rotation_euler = (0, 0, math.radians(-180)) # 向内展开180°
        fold_R.rotation_euler = (0, 0, math.radians(180))  # 向内展开180°
        
        # 相机标准透视全景 (正面稍高俯视，居中留白)
        cam.location = Vector((0.0, 4.9, 0.35))
        camera_look_at(cam, Vector((0.0, 0.0, 0.0)))
        
    elif state == "COND2_COMPACT":
        # 工况二【常态多媒体·大屏露显双层叠合形态 4000mm】
        # 侧滑收缩 (X=±2.0m), 翻转 0°, 折叠副板回折 0° 与主板紧密贴合, 露显 86 寸大屏
        ctrl_slide_L.location = (-2.0, 0.065, 0)
        ctrl_slide_R.location = (2.0, 0.065, 0)
        update_telescopic_rods(0.0, 0.0)
        flip_L.rotation_euler = (0, 0, 0)
        flip_R.rotation_euler = (0, 0, 0)
        fold_L.rotation_euler = (0, 0, 0) # 叠合贴合
        fold_R.rotation_euler = (0, 0, 0)
        
        cam.location = Vector((0.0, 4.9, 0.35))
        camera_look_at(cam, Vector((0.0, 0.0, 0.0)))
        
    elif state == "COND3_DEPLOYED":
        # 工况三【大视野与避光·平移侧滑极限展开 6000mm + 避光偏航】
        # 侧滑外滑 1.0m (左至 -3.0m, 右至 +3.0m), 完整露出双梁不锈钢套杆与橙色端部拉杆
        # 主板与叠合副板整体微调偏航 14° + 俯仰 -3° 避开侧窗直射高光
        ctrl_slide_L.location = (-3.0, 0.065, 0)
        ctrl_slide_R.location = (3.0, 0.065, 0)
        update_telescopic_rods(1.0, 1.0) # 套杆外展 1.0m
        flip_L.rotation_euler = (0, math.radians(-3), math.radians(14)) # 偏航避光
        flip_R.rotation_euler = (0, math.radians(-3), math.radians(-14))
        fold_L.rotation_euler = (0, 0, 0) # 保持叠合
        fold_R.rotation_euler = (0, 0, 0)
        
        # 适应 6 米超宽大视野全景，后移并居中
        cam.location = Vector((0.0, 6.8, 0.45))
        camera_look_at(cam, Vector((0.0, 0.0, 0.0)))
        
    elif state == "DETAIL_HINGE":
        # 局部特写【对角线双铰链与双横梁伸缩套杆精密机构特写】
        # 左侧滑架抽出 0.7m, 露出银色不锈钢伸缩内套杆与橙色端部拉杆
        # 主翻转微偏航 10°, 折叠铰链半展开 50°, 俯视截面清晰展露外侧翻转轴与内侧折叠轴的对角线拓扑！
        ctrl_slide_L.location = (-2.7, 0.065, 0)
        ctrl_slide_R.location = (2.0, 0.065, 0)
        update_telescopic_rods(0.7, 0.0)
        flip_L.rotation_euler = (0, 0, math.radians(10))
        fold_L.rotation_euler = (0, 0, math.radians(-50)) # 半展开 50°
        
        # 45° 黄金俯视透视视角对准左侧对角线铰链系统
        cam.location = Vector((-2.6, 2.8, 0.85))
        camera_look_at(cam, Vector((-1.9, 0.06, 0.0)))

# -----------------------------------------------------------------------------
# 10. 执行批量渲染出图与工程源文件保存
# -----------------------------------------------------------------------------
tasks = [
    ("COND1_COVERED", "01_工况一_全覆盖封屏形态_4000mm_4K.png"),
    ("COND2_COMPACT", "02_工况二_常态大屏露显双层叠合形态_4000mm_4K.png"),
    ("COND3_DEPLOYED", "03_工况三_平移侧滑极限展开与避光偏航形态_6000mm_4K.png"),
    ("DETAIL_HINGE", "04_对角线双铰链与双横梁伸缩套杆精密机构特写_4K.png")
]

print(">>> 开始 Blender 5.0 第三代智能黑板系统 3D 建模与多工况 4K 渲染管线 (v1.2 工业级精修版)...")

for state, filename in tasks:
    print(f"[*] 切换至状态: {state} ...")
    apply_state(state)
    bpy.context.view_layer.update()
    filepath = os.path.join(output_dir, filename)
    scene.render.filepath = filepath
    print(f"[*] 正在渲染 4K 输出: {filepath} ...")
    bpy.ops.render.render(write_still=True)
    print(f"[+] 渲染完成: {filename}")

# 恢复常态叠合状态并保存 .blend 工程文件
apply_state("COND2_COMPACT")
blend_path = os.path.join(output_dir, "第三代多维叠合翻转智能黑板系统_三维机构总装与动力学模型_v1.0.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print(f"[SUCCESS] 全量 3D 渲染与模型资产已冻结保存至: {blend_path}")
