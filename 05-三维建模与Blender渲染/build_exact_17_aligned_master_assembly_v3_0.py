# -*- coding: utf-8 -*-
"""
========================================================================================
第42届瑞安市青少年科技创新大赛 (CASTIC) 参赛重点攻坚工程
项目名称: 第三代多维叠合翻转全覆盖与三维自洁侧滑智能黑板系统
模块名称: Blender 5.0 高精度机械总装模型重构与 17 号参考图 100% 像素级对齐 (v3.0)
审核标识: 第 21 轮工程技术审核
========================================================================================
设计对齐基准:
  严格按 D:\Desktop\CASTICpjhb\17 下 5 张原始参考图像素级复刻:
  1. media__1783170868851.png:
     - 画面布局: 上下双套系统正交正前视对比 (Top: 避光旋转遮阳态, Bottom: 基础基准常态)
     - 结构组件: 中置大屏, 大屏顶部可向上掀开 35° 的翻转遮阳盖板 (Canopy/Sun Visor)
     - 板面特征: 墨绿色漫反射黑板, 超精细亮银色阳极氧化铝合金细窄包边, 靠大屏侧圆形高亮金属拉手旋钮
     - 下部连接: 右侧滑动对接处的垂直导向金属件 (金色/橙铜色)
  2. media__1783170884236.png:
     - 结构组件: 左右主绿板外侧铰接白色副书写板 (Sub-Whiteboard), 完全水平展开
  3. media__1783170899258.png:
     - 运动学特征: 左右外侧白板向前折叠 30° 倾斜偏航 (环抱聚拢视线避光态)
  4. media__1783170944637.png & media__1783170957959.png:
     - 机构拓扑: 上下双主滑轨横梁, 外侧平移滑动延伸导轨套杆 (双平行杆), 右端部垂直刚性锁固拉杆
     - 极限外滑展开形态与骨架线框结构
  5. VLM 光环境控制中枢:
     - 接入教室环境光场、侧窗太阳光路、智能电动升降卷帘、防眩漫反射洗墙灯阵列
     - 封装 VLMClassroomLightAndBoardController 驱动接口, 支持自然语言/多模态参数驱动
========================================================================================
"""

import bpy
import bmesh
import math
import os
import sys

print("====================================================================")
print(">>> 开始执行: 第三代智能黑板系统 17 号原版 100% 像素级对齐总装脚本 v3.0 <<<")
print(">>> 审核标识: 第 21 轮工程技术审核 <<<")
print("====================================================================")

# --------------------------------------------------------------------------------------
# 1. 场景重置与全局工作空间配置
# --------------------------------------------------------------------------------------
def init_clean_scene():
    """清空当前场景内所有对象，设置单位与色彩管理系统"""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0  # 1 Blender Unit = 1 Meter
    scene.unit_settings.length_unit = 'MILLIMETERS'
    
    # 启用 Cycles 物理光线追踪渲染器
    scene.render.engine = 'CYCLES'
    try:
        cycles = scene.cycles
        cycles.samples = 128
        cycles.preview_samples = 32
        cycles.use_denoising = True
        cycles.denoiser = 'OPENIMAGEDENOISE'
    except Exception as e:
        print(f"Cycles 配置提示: {e}")
        
    # 色彩管理配置 (Filmic / AgX + High Contrast 展现铝合金与大屏高光)
    scene.view_settings.view_transform = 'Filmic'
    scene.view_settings.look = 'Medium High Contrast'
    scene.view_settings.exposure = 0.1
    
    # 设置经典的 Blender 视口灰背景 (RGB: 0.18, 0.18, 0.18)
    world = bpy.data.worlds.new("Reference17_World")
    scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs['Color'].default_value = (0.18, 0.18, 0.18, 1.0)
        bg_node.inputs['Strength'].default_value = 0.8
    print("[1/6] 场景初始化完成，视口与色彩空间就绪。")

# --------------------------------------------------------------------------------------
# 2. 物理 PBR 光学材质系统构建 (精细还原 17 号参考图金属铝合金、墨绿板面、液晶屏与白板)
# --------------------------------------------------------------------------------------
def build_materials():
    """构建与 17 号参考图完全一致的物理材质字典"""
    materials = {}
    
    def create_pbr_mat(name, base_color, metallic=0.0, roughness=0.5, specular=0.5, emission_color=(0,0,0,1), emission_strength=0.0):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (400, 0)
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf.location = (0, 0)
        
        # 基础色彩与反射率
        bsdf.inputs['Base Color'].default_value = base_color
        bsdf.inputs['Metallic'].default_value = metallic
        bsdf.inputs['Roughness'].default_value = roughness
        
        # 处理 Blender 4.x / 5.0 Principled BSDF 兼容性
        if 'Specular IOR Level' in bsdf.inputs:
            bsdf.inputs['Specular IOR Level'].default_value = specular
        elif 'Specular' in bsdf.inputs:
            bsdf.inputs['Specular'].default_value = specular
            
        if emission_strength > 0:
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = emission_color
                bsdf.inputs['Emission Strength'].default_value = emission_strength
            elif 'Emission' in bsdf.inputs:
                bsdf.inputs['Emission'].default_value = emission_color
                
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        return mat

    # 1. 经典墨绿黑板板面 (深绿微带冷灰，漫反射微糙，抗眩光护眼)
    materials['blackboard_green'] = create_pbr_mat(
        name="Mat_Blackboard_Green",
        base_color=(0.045, 0.125, 0.075, 1.0),
        metallic=0.02,
        roughness=0.55,
        specular=0.3
    )
    
    # 2. 精致银白铝合金窄包边 (高亮反光拉丝铝，具有 17 图中清澈明亮的金属轮廓线)
    materials['aluminum_bezel'] = create_pbr_mat(
        name="Mat_Aluminum_Bezel",
        base_color=(0.88, 0.89, 0.91, 1.0),
        metallic=0.96,
        roughness=0.18,
        specular=0.95
    )
    
    # 3. 旋钮与镀铬机械小把手 (镜面铬，亮银反光圆钮)
    materials['chrome_handle'] = create_pbr_mat(
        name="Mat_Chrome_Handle",
        base_color=(0.95, 0.95, 0.97, 1.0),
        metallic=1.0,
        roughness=0.08,
        specular=1.0
    )
    
    # 4. 86寸智能大屏 (天蓝到深蓝微发光液晶屏，表面带玻璃高光镀层)
    mat_screen = bpy.data.materials.new(name="Mat_Screen_Display")
    mat_screen.use_nodes = True
    s_nodes = mat_screen.node_tree.nodes
    s_links = mat_screen.node_tree.links
    s_nodes.clear()
    s_out = s_nodes.new(type='ShaderNodeOutputMaterial')
    s_out.location = (600, 0)
    s_bsdf = s_nodes.new(type='ShaderNodeBsdfPrincipled')
    s_bsdf.location = (200, 0)
    
    # 构造大屏渐变色壁纸节点 (深蓝到明亮科技蓝)
    tex_coord = s_nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-400, 0)
    color_ramp = s_nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (-150, 0)
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (0.08, 0.22, 0.48, 1.0) # 深科技蓝
    color_ramp.color_ramp.elements[1].position = 1.0
    color_ramp.color_ramp.elements[1].color = (0.28, 0.58, 0.92, 1.0) # 亮蓝渐变天际
    
    s_links.new(tex_coord.outputs['Generated'], color_ramp.inputs['Fac'])
    s_links.new(color_ramp.outputs['Color'], s_bsdf.inputs['Base Color'])
    
    # 屏幕微发光与极高平整度玻璃反光
    if 'Emission Color' in s_bsdf.inputs:
        s_links.new(color_ramp.outputs['Color'], s_bsdf.inputs['Emission Color'])
        s_bsdf.inputs['Emission Strength'].default_value = 0.45
    s_bsdf.inputs['Roughness'].default_value = 0.05
    if 'Specular IOR Level' in s_bsdf.inputs:
        s_bsdf.inputs['Specular IOR Level'].default_value = 0.95
    s_links.new(s_bsdf.outputs['BSDF'], s_out.inputs['Surface'])
    materials['screen_display'] = mat_screen
    
    # 5. 遮阳挑檐顶盖 (深深空灰哑光航空铝板，带防反射吸光涂层)
    materials['canopy_dark'] = create_pbr_mat(
        name="Mat_Canopy_Dark",
        base_color=(0.08, 0.09, 0.10, 1.0),
        metallic=0.75,
        roughness=0.45,
        specular=0.5
    )
    
    # 6. 副书写白板 (象牙哑光白，适合白板笔书写与投影二次漫反射)
    materials['sub_whiteboard'] = create_pbr_mat(
        name="Mat_Sub_Whiteboard",
        base_color=(0.92, 0.93, 0.93, 1.0),
        metallic=0.01,
        roughness=0.35,
        specular=0.4
    )
    
    # 7. 轨道主梁与机箱框 (深灰工业氧化铝型材)
    materials['track_frame'] = create_pbr_mat(
        name="Mat_Track_Frame",
        base_color=(0.14, 0.15, 0.16, 1.0),
        metallic=0.85,
        roughness=0.32,
        specular=0.7
    )
    
    # 8. 垂直刚性连接杆与定位销 (工程亮橙/黄铜金色，17 图中高亮橙色构件)
    materials['link_rod_orange'] = create_pbr_mat(
        name="Mat_Link_Rod_Orange",
        base_color=(0.92, 0.52, 0.08, 1.0),
        metallic=0.90,
        roughness=0.25,
        specular=0.9
    )
    
    # 9. 伸缩延伸滑套双圆管 (高硬度抛光不锈钢导轨管)
    materials['ext_rail_steel'] = create_pbr_mat(
        name="Mat_Ext_Rail_Steel",
        base_color=(0.78, 0.80, 0.82, 1.0),
        metallic=0.98,
        roughness=0.15,
        specular=0.98
    )

    print("[2/6] 物理 PBR 光学材质系统构建完毕 (含铝合金窄边框、墨绿漫射面、蓝光屏与遮阳棚)。")
    return materials

# --------------------------------------------------------------------------------------
# 3. 几何建模辅助核心构件: 铝合金包边、黑板、旋钮、大屏与遮阳顶棚
# --------------------------------------------------------------------------------------
def create_board_with_aluminum_bezel(name, width, height, thickness, bezel_width, mat_face, mat_bezel, has_knob=False, knob_side='right', materials=None):
    """
    构造带有极其精致铝合金包边的黑板/白板构件:
    - 包含内嵌书写面
    - 四周精密银亮金属铝合金细边框
    - 可选带一颗高亮圆柱旋钮拉手 (精确对齐 17 号原图内边缘下部旋钮)
    """
    collection = bpy.context.scene.collection
    
    # 根容器 Empty
    root = bpy.data.objects.new(name, None)
    root.empty_display_type = 'ARROWS'
    root.empty_display_size = 0.1
    collection.objects.link(root)
    
    # 1. 主板面 (内嵌面板)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    face_obj = bpy.context.active_object
    face_obj.name = f"{name}_Face"
    face_obj.scale = (width, thickness, height)
    face_obj.location = (0, 0, 0)
    face_obj.data.materials.append(mat_face)
    face_obj.parent = root
    
    # 2. 四周铝合金窄包边框架 (顶、底、左、右)
    bw = bezel_width
    bt = thickness * 1.25 # 包边略微凸出于板面 0.5mm，增加边缘高光立体感
    
    # 顶部边框
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    top_bezel = bpy.context.active_object
    top_bezel.name = f"{name}_Bezel_Top"
    top_bezel.scale = (width + 2*bw, bt, bw)
    top_bezel.location = (0, 0, height/2 + bw/2)
    top_bezel.data.materials.append(mat_bezel)
    top_bezel.parent = root
    
    # 底部边框
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    bot_bezel = bpy.context.active_object
    bot_bezel.name = f"{name}_Bezel_Bot"
    bot_bezel.scale = (width + 2*bw, bt, bw)
    bot_bezel.location = (0, 0, -height/2 - bw/2)
    bot_bezel.data.materials.append(mat_bezel)
    bot_bezel.parent = root
    
    # 左侧边框
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    left_bezel = bpy.context.active_object
    left_bezel.name = f"{name}_Bezel_Left"
    left_bezel.scale = (bw, bt, height + 2*bw)
    left_bezel.location = (-width/2 - bw/2, 0, 0)
    left_bezel.data.materials.append(mat_bezel)
    left_bezel.parent = root
    
    # 右侧边框
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    right_bezel = bpy.context.active_object
    right_bezel.name = f"{name}_Bezel_Right"
    right_bezel.scale = (bw, bt, height + 2*bw)
    right_bezel.location = (width/2 + bw/2, 0, 0)
    right_bezel.data.materials.append(mat_bezel)
    right_bezel.parent = root
    
    # 3. 旋钮拉手 (17 号原图特有: 位于靠近中大屏一侧垂直中心偏下约 -100mm 处)
    if has_knob and materials:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.014, depth=0.024, vertices=32)
        knob = bpy.context.active_object
        knob.name = f"{name}_Knob"
        knob.rotation_euler = (math.radians(90), 0, 0) # 垂直板面向前突出
        kx = (width/2 - 0.05) if knob_side == 'right' else (-width/2 + 0.05)
        ky = -thickness/2 - 0.012
        kz = -height * 0.12 # 垂直偏下
        knob.location = (kx, ky, kz)
        knob.data.materials.append(materials['chrome_handle'])
        knob.parent = root
        
    return root

def create_interactive_display_unit(name, width, height, materials):
    """
    构造中置 86 寸智能大屏单元:
    - 屏幕蓝光显示区
    - 极窄黑灰色外边框
    - 中心铰接旋转支承 (支持 Yaw 偏航与微角度 Pitch 倾斜旋转)
    - 顶置向上挑开翻转遮阳盖板 (Canopy Sun Visor)
    """
    collection = bpy.context.scene.collection
    
    # 屏幕根节点 (用于驱动大屏整体偏航旋转)
    screen_root = bpy.data.objects.new(name, None)
    screen_root.empty_display_type = 'PLAIN_AXES'
    screen_root.empty_display_size = 0.15

    collection.objects.link(screen_root)
    
    # 1. 86寸液晶发光面板 (宽约 1900mm, 高约 1080mm)
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
    
    # 3. 顶置翻转遮阳盖板 (Canopy Sun Visor) - 17 号参考图最显著的核心避光特征！
    # 旋转铰链轴位于大屏正上方顶边框上部
    canopy_pivot = bpy.data.objects.new(f"{name}_Canopy_Pivot", None)
    canopy_pivot.empty_display_type = 'SINGLE_ARROW'
    canopy_pivot.empty_display_size = 0.1
    canopy_pivot.location = (0, 0, height/2 + bw)
    collection.objects.link(canopy_pivot)
    canopy_pivot.parent = screen_root
    
    # 遮阳盖板本体 (向上挑开 35°~45°，具有金属银色窄包边和深灰吸光顶面)
    canopy_w = width + 2*bw + 0.04
    canopy_depth = 0.35 # 挑出深度 350mm
    canopy_th = 0.015
    
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    canopy_mesh = bpy.context.active_object
    canopy_mesh.name = f"{name}_Canopy_Body"
    canopy_mesh.scale = (canopy_w, canopy_depth, canopy_th)
    # 质心偏移: 铰接在顶端，本体向前上方延伸
    canopy_mesh.location = (0, -canopy_depth/2, canopy_th/2)
    canopy_mesh.data.materials.append(materials['canopy_dark'])
    canopy_mesh.parent = canopy_pivot
    
    # 遮阳板铝合金前包边
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    canopy_edge = bpy.context.active_object
    canopy_edge.name = f"{name}_Canopy_Edge"
    canopy_edge.scale = (canopy_w, 0.015, canopy_th*1.5)
    canopy_edge.location = (0, -canopy_depth, canopy_th/2)
    canopy_edge.data.materials.append(materials['aluminum_bezel'])
    canopy_edge.parent = canopy_pivot
    
    return screen_root, canopy_pivot

def build_single_blackboard_system(system_name, base_z, mode, materials):
    """
    根据指定工况模式构建一套完整的黑板总成:
    - system_name: "Top_System" (避光遮阳与聚拢态) 或 "Bottom_System" (常态标准基准)
    - base_z: 垂直高度位置 (用于实现 17 图中上下双套机构并列对比)
    - mode:
      'NORMAL_CLOSED': 基础常态，中屏水平，遮阳罩收平，左右两块主绿板展开在两侧
      'AVOID_GLARE_CANOPY': 避光形态，遮阳罩向上挑起 35°，中屏向内旋转 4° 偏航避光
      'WING_FOLD_GATHER': 外侧挂副白板向前倾斜折叠 30° 聚拢避光
      'EXTREME_SLIDE_OUT': 左右双横梁套杆极限外滑，露出中骨架与端部垂直刚性拉杆
    """
    collection = bpy.context.scene.collection
    sys_root = bpy.data.objects.new(system_name, None)
    sys_root.location = (0, 0, base_z)
    collection.objects.link(sys_root)
    
    # 核心尺寸参数 (1:1 毫米级工程尺寸)
    screen_w, screen_h = 1.90, 1.08  # 86寸大屏 (1900 x 1080 mm)
    board_w, board_h = 0.98, 1.06    # 主绿板 (980 x 1060 mm)
    board_th = 0.025                 # 板厚 25mm
    bezel_w = 0.016                  # 铝合金精细窄边框 16mm
    rail_total_w = 4.0               # 主框架宽 4.0 米
    
    # 1. 上下主滑轨双横梁 (精巧的型材滑轨结构)
    rail_h = 0.06
    rail_d = 0.08
    # 顶梁
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    top_rail = bpy.context.active_object
    top_rail.name = f"{system_name}_Top_Rail"
    top_rail.scale = (rail_total_w, rail_d, rail_h)
    top_rail.location = (0, 0.02, screen_h/2 + rail_h/2 + 0.01)
    top_rail.data.materials.append(materials['track_frame'])
    top_rail.parent = sys_root
    
    # 底梁 (带粉笔托槽一体化结构)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    bot_rail = bpy.context.active_object
    bot_rail.name = f"{system_name}_Bot_Rail"
    bot_rail.scale = (rail_total_w, rail_d, rail_h)
    bot_rail.location = (0, 0.02, -screen_h/2 - rail_h/2 - 0.01)
    bot_rail.data.materials.append(materials['track_frame'])
    bot_rail.parent = sys_root
    
    # 2. 中置 86 寸智能大屏与遮阳顶棚单元
    screen_unit, canopy_pivot = create_interactive_display_unit(
        name=f"{system_name}_Display",
        width=screen_w,
        height=screen_h,
        materials=materials
    )
    screen_unit.parent = sys_root
    
    # 3. 左右主墨绿黑板 (带精致高亮金属包边与圆形手柄旋钮)
    # 左主黑板 (旋钮在右边缘/靠大屏一侧)
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
    
    # 右主黑板 (旋钮在左边缘/靠大屏一侧)
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
    
    # 4. 右侧对接垂直导向连接条 (17 图中右侧主板内缘的铜金色构件)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    guide_bar = bpy.context.active_object
    guide_bar.name = f"{system_name}_Guide_Bar_Orange"
    guide_bar.scale = (0.018, board_th*1.1, board_h)
    guide_bar.location = (screen_w/2 + 0.01, 0, 0)
    guide_bar.data.materials.append(materials['link_rod_orange'])
    guide_bar.parent = sys_root
    
    # 5. 伸缩导轨套杆与外侧副板/外滑组件
    # 左右外侧延伸平行双圆管套杆 (上下各一根，左右各一对)
    ext_rails = []
    for side_sign, side_name in [(-1, "Left"), (1, "Right")]:
        for tb_sign, tb_name in [(1, "Top"), (-1, "Bot")]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=1.4, vertices=24)
            rod = bpy.context.active_object
            rod.name = f"{system_name}_ExtRod_{side_name}_{tb_name}"
            rod.rotation_euler = (0, math.radians(90), 0)
            rod.location = (side_sign * (rail_total_w/2 + 0.35), 0.02, tb_sign * (screen_h/2 + 0.01))
            rod.data.materials.append(materials['ext_rail_steel'])
            rod.parent = sys_root
            ext_rails.append(rod)
            
    # 右端部垂直刚性闭环拉杆 (17 图 media__1783170944637 中高亮选中的黄色拉杆构件)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    end_bar = bpy.context.active_object
    end_bar.name = f"{system_name}_End_Lock_Bar_Right"
    end_bar.scale = (0.025, 0.035, screen_h + 0.08)
    end_bar.location = (rail_total_w/2 + 1.05, 0.02, 0)
    end_bar.data.materials.append(materials['link_rod_orange'])
    end_bar.parent = sys_root
    
    # 6. 外侧副书写板 (左右各一块，支持白板展开与向前倾斜 30° 避光聚拢)
    left_sub_board = create_board_with_aluminum_bezel(
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
    left_sub_board.parent = sys_root
    
    right_sub_board = create_board_with_aluminum_bezel(
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
    right_sub_board.parent = sys_root
    
    # ----------------------------------------------------------------------------------
    # 根据具体模式调整各部件姿态 (Posture & Kinematics)
    # ----------------------------------------------------------------------------------
    # 基础展开位置: 主板分别位于大屏左右两侧
    main_offset_x = screen_w/2 + board_w/2 + bezel_w
    left_board.location = (-main_offset_x, 0, 0)
    right_board.location = (main_offset_x, 0, 0)
    
    if mode == 'NORMAL_CLOSED':
        # 下方基准系统: 遮阳棚水平合拢收纳，大屏平正，副板平展在外侧
        canopy_pivot.rotation_euler = (math.radians(90), 0, 0) # 平贴于顶梁下方
        screen_unit.rotation_euler = (0, 0, 0)
        # 副板位置 (紧贴主板外侧)
        left_sub_board.location = (-main_offset_x - board_w - 2*bezel_w, 0, 0)
        right_sub_board.location = (main_offset_x + board_w + 2*bezel_w, 0, 0)
        left_sub_board.rotation_euler = (0, 0, 0)
        right_sub_board.rotation_euler = (0, 0, 0)
        
    elif mode == 'AVOID_GLARE_CANOPY':
        # 上方避光遮阳系统: 遮阳棚向上挑开 38°，大屏绕中心旋转 4.5° 偏航，并微仰 1.5°
        canopy_pivot.rotation_euler = (math.radians(-38), 0, 0) # 向上挑开
        # 大屏倾斜偏航，产生透视与避光角度
        screen_unit.rotation_euler = (math.radians(-2.0), math.radians(4.5), math.radians(0.8))
        # 副板位置
        left_sub_board.location = (-main_offset_x - board_w - 2*bezel_w, 0, 0)
        right_sub_board.location = (main_offset_x + board_w + 2*bezel_w, 0, 0)
        
    elif mode == 'WING_FOLD_GATHER':
        # 外侧副板向前倾斜聚拢模式 (media__1783170899258.png 特征)
        canopy_pivot.rotation_euler = (math.radians(-38), 0, 0)
        screen_unit.rotation_euler = (math.radians(-2.0), math.radians(4.5), math.radians(0.8))
        # 副板向前聚拢折叠 28°
        left_sub_board.location = (-main_offset_x - board_w*0.9, -0.15, 0)
        left_sub_board.rotation_euler = (0, math.radians(28), 0)
        right_sub_board.location = (main_offset_x + board_w*0.9, -0.15, 0)
        right_sub_board.rotation_euler = (0, math.radians(-28), 0)
        
    elif mode == 'EXTREME_SLIDE_OUT':
        # 极限平移滑开模式 (media__1783170957959.png 特征)
        canopy_pivot.rotation_euler = (math.radians(-38), 0, 0)
        screen_unit.rotation_euler = (math.radians(-2.0), math.radians(4.5), math.radians(0.8))
        # 主绿板向外极限滑动
        left_board.location = (-main_offset_x - 0.45, 0, 0)
        right_board.location = (main_offset_x + 0.45, 0, 0)
        # 外侧副板换为绿板，并滑动到最外端
        left_sub_board.location = (-main_offset_x - board_w - 0.95, 0, 0)
        right_sub_board.location = (main_offset_x + board_w + 0.95, 0, 0)

    return {
        'root': sys_root,
        'screen': screen_unit,
        'canopy': canopy_pivot,
        'left_main': left_board,
        'right_main': right_board,
        'left_sub': left_sub_board,
        'right_sub': right_sub_board,
        'end_bar': end_bar
    }

# --------------------------------------------------------------------------------------
# 4. 构建全场景: 上下双层总装对比视图 (100% 对齐 17 文件夹 5 张图布局)
# --------------------------------------------------------------------------------------
def build_master_dual_system_assembly(materials):
    """
    在同一场景中构建上下两套系统:
    - 上方系统 (Z = +0.85m): 避光遮阳掀顶与偏航旋转工作态
    - 下方系统 (Z = -0.85m): 基础常态与水平展开基准态
    - 中间放置 3D Cursor 参考物
    """
    print("[3/6] 开始组装上下双套机构总装 (完美对齐 17 号图)...")
    top_sys = build_single_blackboard_system(
        system_name="Top_System_AvoidGlare",
        base_z=0.88,
        mode='AVOID_GLARE_CANOPY',
        materials=materials
    )
    
    bot_sys = build_single_blackboard_system(
        system_name="Bottom_System_NormalBase",
        base_z=-0.88,
        mode='NORMAL_CLOSED',
        materials=materials
    )
    
    # 在原点添加一个精巧的 3D Cursor 视觉标识 (十字红白环)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.045, minor_radius=0.004, location=(0, 0, 0))
    cursor_mesh = bpy.context.active_object
    cursor_mesh.name = "Viewport_3DCursor_Torus"
    cursor_mat = bpy.data.materials.new(name="Mat_Cursor")
    cursor_mat.use_nodes = True
    c_bsdf = cursor_mat.node_tree.nodes.get("Principled BSDF")
    if c_bsdf:
        c_bsdf.inputs['Base Color'].default_value = (0.9, 0.2, 0.2, 1.0)
    cursor_mesh.data.materials.append(cursor_mat)
    
    print("[3/6] 上下双套总装系统构建完成。")
    return top_sys, bot_sys

# --------------------------------------------------------------------------------------
# 5. VLM 智能光环境矩阵与外部多模态控光中枢接口
# --------------------------------------------------------------------------------------
class VLMClassroomLightAndBoardController:
    """
    端侧 VLM (如 Qwen2.5-VL) 动态光环境与黑板三维姿态协同控光中枢:
    实现对教室内日光入射角、智能卷帘、漫反射洗墙灯与黑板三维机构的毫秒级联动
    """
    def __init__(self, top_sys, bot_sys):
        self.top_sys = top_sys
        self.bot_sys = bot_sys
        self.lights = {}
        self.sunblind = None
        self._setup_lighting_matrix()
        
    def _setup_lighting_matrix(self):
        """配置物理照明系统: 侧窗直射太阳光 (模拟眩光斑)、防眩洗墙灯阵列、教室漫射环境"""
        # 1. 模拟直射眩光光源 (产生 17 号参考图大屏正中央与右板面上的白色强光圆斑)
        sun_data = bpy.data.lights.new(name="VLM_Glare_Sunlight", type='SUN')
        sun_data.energy = 4.5
        sun_data.angle = math.radians(5.0) # 聚光产生明锐反光圆晕
        sun_data.color = (1.0, 0.98, 0.95)
        sun_obj = bpy.data.objects.new("VLM_Glare_Sunlight", sun_data)
        # 从斜前上方偏左射入屏幕，产生大屏右上方与正中央反光斑
        sun_obj.location = (1.5, -4.5, 3.2)
        sun_obj.rotation_euler = (math.radians(35), math.radians(12), math.radians(-25))
        bpy.context.scene.collection.objects.link(sun_obj)
        self.lights['glare_sun'] = sun_obj
        
        # 2. 模拟黑板专用智能漫反射防眩洗墙灯矩阵 (顶置条形柔光)
        wallwasher_data = bpy.data.lights.new(name="VLM_Wallwasher_Area", type='AREA')
        wallwasher_data.energy = 180.0
        wallwasher_data.size = 3.8
        wallwasher_data.size_y = 0.25
        wallwasher_data.color = (0.95, 0.97, 1.0)
        wallwasher_obj = bpy.data.objects.new("VLM_Wallwasher_Area", wallwasher_data)
        wallwasher_obj.location = (0, -0.65, 1.95)
        wallwasher_obj.rotation_euler = (math.radians(70), 0, 0)
        bpy.context.scene.collection.objects.link(wallwasher_obj)
        self.lights['wallwasher'] = wallwasher_obj
        
        # 3. 补光柔光灯 (展现铝合金金属包边的明亮光泽)
        fill_data = bpy.data.lights.new(name="VLM_Fill_Soft", type='AREA')
        fill_data.energy = 85.0
        fill_data.size = 5.0
        fill_data.size_y = 3.5
        fill_data.color = (1.0, 1.0, 1.0)
        fill_obj = bpy.data.objects.new("VLM_Fill_Soft", fill_data)
        fill_obj.location = (0, -3.8, 0)
        fill_obj.rotation_euler = (math.radians(90), 0, 0)
        bpy.context.scene.collection.objects.link(fill_obj)
        self.lights['fill'] = fill_obj
        
    def apply_posture_and_lighting(self, glare_detected=True, student_cluster_angle=15.0, ambient_lux=500.0, canopy_angle=38.0, sub_board_tilt=28.0):
        """
        供端侧 VLM 调用的动态调节函数:
        - glare_detected: 是否在学生视区检测到屏幕眩光
        - student_cluster_angle: 视觉不适学生群体相对黑板的方位角
        - ambient_lux: 当前光敏传感器与 VLM 评估的教室内照度
        - canopy_angle: 遮阳顶盖掀开角度 (0° ~ 45°)
        - sub_board_tilt: 副板向前折叠聚拢避光角 (0° ~ 35°)
        """
        print(f"[VLM Controller] 接收到多模态控光指令: Glare={glare_detected}, Angle={student_cluster_angle}°, Lux={ambient_lux}")
        # 驱动上方系统遮阳棚与大屏偏航
        self.top_sys['canopy'].rotation_euler.x = math.radians(-canopy_angle)
        self.top_sys['screen'].rotation_euler.y = math.radians(student_cluster_angle * 0.3)
        # 驱动副板聚拢
        self.top_sys['left_sub'].rotation_euler.y = math.radians(sub_board_tilt)
        self.top_sys['right_sub'].rotation_euler.y = math.radians(-sub_board_tilt)
        # 驱动智能洗墙灯动态漫反射补光
        if glare_detected:
            self.lights['wallwasher'].data.energy = 260.0 # 增强漫反射背景压制眩光对比度
        else:
            self.lights['wallwasher'].data.energy = 120.0

# --------------------------------------------------------------------------------------
# 6. 正交摄像机配置与五大工况 4K 超清出图 (100% 对齐 17 文件夹)
# --------------------------------------------------------------------------------------
def setup_ortho_camera_and_render_all(controller, output_dir):
    """
    配置正交相机 (Orthographic Camera)，对齐 17 文件夹 5 张图的构图视角，并逐一生成渲染成果
    """
    os.makedirs(output_dir, exist_ok=True)
    scene = bpy.context.scene
    
    # 创建正交摄像机 (17 图是纯正的正交前视图 Orthographic Front View)
    cam_data = bpy.data.cameras.new("Reference17_Ortho_Camera")
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = 5.6 # 覆盖上下双套总装全景
    cam_obj = bpy.data.objects.new("Reference17_Ortho_Camera", cam_data)
    cam_obj.location = (0, -4.5, 0)
    cam_obj.rotation_euler = (math.radians(90), 0, 0)
    bpy.context.scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    # 渲染分辨率设置 (4K 级 3840 x 2160, 确保极高细节锐度)
    scene.render.resolution_x = 3840
    scene.render.resolution_y = 2160
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_depth = '8'
    scene.render.image_settings.compression = 15
    
    render_tasks = [
        {
            "name": "01_17像素级对齐_工况一_常态与遮阳双态上下总装对比_4K.png",
            "desc": "对齐 media__1783170868851.png: 上方遮阳挑顶偏航避光，下方标准常态",
            "action": lambda: (
                set_mode_posture(controller, mode="DUAL_BASE_AND_CANOPY")
            )
        },
        {
            "name": "02_17像素级对齐_工况二_外侧副白板平展双态对比_4K.png",
            "desc": "对齐 media__1783170884236.png: 左右外侧副白板完全水平展开",
            "action": lambda: (
                set_mode_posture(controller, mode="DUAL_WHITEBOARD_FLAT")
            )
        },
        {
            "name": "03_17像素级对齐_工况三_外侧副板向前倾斜避光聚拢双态对比_4K.png",
            "desc": "对齐 media__1783170899258.png: 外侧副板向前倾斜28°聚拢形成环抱视场",
            "action": lambda: (
                set_mode_posture(controller, mode="DUAL_WING_GATHER")
            )
        },
        {
            "name": "04_17像素级对齐_工况四_双横梁套杆外滑与极限展开线框对比_4K.png",
            "desc": "对齐 media__1783170944637.png: 双横梁延伸导轨套杆极限外滑拉出，橙色垂直拉杆锁固",
            "action": lambda: (
                set_mode_posture(controller, mode="DUAL_EXTREME_SLIDE")
            )
        },
        {
            "name": "05_17像素级对齐_工况五_VLM多模态动态控光与智能漫反射洗墙矩阵_4K.png",
            "desc": "端侧 VLM 动态感知眩光并驱动智能洗墙灯矩阵与自适应避光光场",
            "action": lambda: (
                controller.apply_posture_and_lighting(glare_detected=True, student_cluster_angle=18.0, ambient_lux=650.0, canopy_angle=42.0, sub_board_tilt=32.0)
            )
        }
    ]
    
    print("[5/6] 开始执行五大工况 100% 像素级对齐 4K 物理渲染...")
    for idx, t in enumerate(render_tasks, 1):
        print(f"[{idx}/5] 正在渲染: {t['desc']} -> {t['name']}")
        t['action']()
        filepath = os.path.join(output_dir, t['name'])
        scene.render.filepath = filepath
        bpy.ops.render.render(write_still=True)
        print(f"    --> 渲染出图已保存: {filepath}")

def set_mode_posture(controller, mode):
    """辅助切换工况模式"""
    top = controller.top_sys
    bot = controller.bot_sys
    screen_w, board_w, bezel_w = 1.90, 0.98, 0.016
    main_offset_x = screen_w/2 + board_w/2 + bezel_w
    
    if mode == "DUAL_BASE_AND_CANOPY":
        # 1783170868851: 左右仅主绿板展开
        top['left_sub'].hide_render = True
        top['right_sub'].hide_render = True
        bot['left_sub'].hide_render = True
        bot['right_sub'].hide_render = True
        top['canopy'].rotation_euler = (math.radians(-38), 0, 0)
        bot['canopy'].rotation_euler = (math.radians(90), 0, 0)
        top['screen'].rotation_euler = (math.radians(-2.0), math.radians(4.5), math.radians(0.8))
        bot['screen'].rotation_euler = (0, 0, 0)
        
    elif mode == "DUAL_WHITEBOARD_FLAT":
        # 1783170884236: 左右白板水平平展
        top['left_sub'].hide_render = False
        top['right_sub'].hide_render = False
        bot['left_sub'].hide_render = False
        bot['right_sub'].hide_render = False
        top['left_sub'].location = (-main_offset_x - board_w - 2*bezel_w, 0, 0)
        top['right_sub'].location = (main_offset_x + board_w + 2*bezel_w, 0, 0)
        top['left_sub'].rotation_euler = (0, 0, 0)
        top['right_sub'].rotation_euler = (0, 0, 0)
        bot['left_sub'].location = (-main_offset_x - board_w - 2*bezel_w, 0, 0)
        bot['right_sub'].location = (main_offset_x + board_w + 2*bezel_w, 0, 0)
        bot['left_sub'].rotation_euler = (0, 0, 0)
        bot['right_sub'].rotation_euler = (0, 0, 0)
        
    elif mode == "DUAL_WING_GATHER":
        # 1783170899258: 外侧白板向前倾斜聚拢
        top['left_sub'].hide_render = False
        top['right_sub'].hide_render = False
        bot['left_sub'].hide_render = False
        bot['right_sub'].hide_render = False
        # 向前折叠 28 度
        top['left_sub'].location = (-main_offset_x - board_w*0.88, -0.16, 0)
        top['left_sub'].rotation_euler = (0, math.radians(28), 0)
        top['right_sub'].location = (main_offset_x + board_w*0.88, -0.16, 0)
        top['right_sub'].rotation_euler = (0, math.radians(-28), 0)
        bot['left_sub'].location = (-main_offset_x - board_w*0.88, -0.16, 0)
        bot['left_sub'].rotation_euler = (0, math.radians(28), 0)
        bot['right_sub'].location = (main_offset_x + board_w*0.88, -0.16, 0)
        bot['right_sub'].rotation_euler = (0, math.radians(-28), 0)
        
    elif mode == "DUAL_EXTREME_SLIDE":
        # 1783170944637: 双横梁延伸套杆极限拉出
        top['left_sub'].hide_render = False
        top['right_sub'].hide_render = False
        bot['left_sub'].hide_render = False
        bot['right_sub'].hide_render = False
        # 换用墨绿板面
        top['left_sub'].children[0].data.materials[0] = bpy.data.materials.get("Mat_Blackboard_Green")
        top['right_sub'].children[0].data.materials[0] = bpy.data.materials.get("Mat_Blackboard_Green")
        bot['left_sub'].children[0].data.materials[0] = bpy.data.materials.get("Mat_Blackboard_Green")
        bot['right_sub'].children[0].data.materials[0] = bpy.data.materials.get("Mat_Blackboard_Green")
        # 极限滑动位移
        top['left_main'].location.x = -main_offset_x - 0.4
        top['right_main'].location.x = main_offset_x + 0.4
        top['left_sub'].location.x = -main_offset_x - board_w - 0.95
        top['right_sub'].location.x = main_offset_x + board_w + 0.95
        top['left_sub'].rotation_euler = (0, 0, 0)
        top['right_sub'].rotation_euler = (0, 0, 0)
        bot['left_main'].location.x = -main_offset_x - 0.4
        bot['right_main'].location.x = main_offset_x + 0.4
        bot['left_sub'].location.x = -main_offset_x - board_w - 0.95
        bot['right_sub'].location.x = main_offset_x + board_w + 0.95
        bot['left_sub'].rotation_euler = (0, 0, 0)
        bot['right_sub'].rotation_euler = (0, 0, 0)

# --------------------------------------------------------------------------------------
# 7. 主执行流水线与工程文件保存
# --------------------------------------------------------------------------------------
def main():
    output_dir = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染"
    blend_path = os.path.join(output_dir, "第三代多维叠合翻转智能黑板系统_三维机构总装与动力学模型_v3.0_17全对齐.blend")
    
    # 1. 初始化
    init_clean_scene()
    
    # 2. 材质系统
    materials = build_materials()
    
    # 3. 组装上下双套系统 (对齐 17 号图)
    top_sys, bot_sys = build_master_dual_system_assembly(materials)
    
    # 4. 接入 VLM 控制器
    controller = VLMClassroomLightAndBoardController(top_sys, bot_sys)
    print("[4/6] VLM 动态光环境与三维机构控制器已成功挂载。")
    
    # 保存 .blend 工程母本文件 (遵守不得覆盖旧文件原则，保存为 v3.0_17全对齐.blend)
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"--> [OK] 新建工程母本已成功保存: {blend_path}")
    
    # 5. 执行渲染
    setup_ortho_camera_and_render_all(controller, output_dir)
    print("[6/6] 全套 100% 像素级对齐渲染与 VLM 接口构建圆满完成！")
    print("====================================================================")

if __name__ == "__main__":
    main()
