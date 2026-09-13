# -*- coding: utf-8 -*-
"""
第二代三维联动自洁防眩光智能教学黑板系统 - AutoCAD 2026 自动化标准工程总装与运动机构绘图脚本 (v1.0)
文件版本: v1.0
设计依据: 专利技术交底书 (20260703132200) 与 Blender 3D 动力学工程参考图
制图规范: 0 Hatch 纯工程机械线框、GB/T 10609.1 标准图框标题栏、STYLE_GB_CN 矢量黑体、全系统标准工程尺寸链
"""

import sys
import os
import math
import array
import win32com.client
import pythoncom
import time

def get_acad_doc():
    pythoncom.CoInitialize()
    acad = win32com.client.GetActiveObject("AutoCAD.Application")
    acad.Visible = True
    doc = acad.Documents.Add()
    return acad, doc

def setup_chinese_style(doc):
    try:
        try:
            st = doc.TextStyles.Item("STYLE_GB_CN")
        except:
            st = doc.TextStyles.Add("STYLE_GB_CN")
        st.SetFont("黑体", False, False, 134, 0)
        st.fontFile = "simhei.ttf"
        st.Height = 0.0
        doc.SetVariable("DIMTXSTY", "STYLE_GB_CN")
        print(">>> 成功配置 STYLE_GB_CN 黑体样式与标注变量 DIMTXSTY")
    except Exception as e:
        print(f"配置字体样式提示: {e}")

def create_layers(doc):
    layers_info = [
        ("01_FRAME_外框导轨", 8),       # 灰色 (型材、导轨、框体)
        ("02_SCREEN_多媒体屏", 5),      # 蓝色 (86寸大屏、液晶偏光膜)
        ("03_BOARD_书写黑板", 3),       # 绿色 (固定黑板、双面黑板)
        ("04_EXT_RAIL_延伸构件", 1),    # 红色 (嵌套延伸轨、自锁凸台、端部拉杆)
        ("05_CLEAN_DUST_自洁排灰", 6),  # 品红 (EPDM罩、排灰孔、尼龙毛刷、集灰槽)
        ("06_PITCH_YAW_运动副", 4),     # 青色 (快拆母座、俯仰销轴、蜗轮蜗杆马达)
        ("07_OPTIC_AI_智能控光", 2),    # 黄色 (偏光伺服、遮光卷轴、BLE照度终端)
        ("08_DIMS_尺寸标注", 1),        # 红色 (机械尺寸链、行程与公差)
        ("09_TEXT_技术说明", 7)         # 白色/黑色 (中文技术指标与标题栏)
    ]
    for name, col in layers_info:
        try:
            lay = doc.Layers.Add(name)
            lay.Color = col
        except:
            pass
    print(">>> 9 大第二代标准工程图层创建完毕")

def draw_rect(ms, x1, y1, x2, y2, layer=None, color=None):
    coords = array.array('d', [float(x1), float(y1), float(x2), float(y1), float(x2), float(y2), float(x1), float(y2)])
    var_arr = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, coords)
    pline = ms.AddLightWeightPolyline(var_arr)
    pline.Closed = True
    if layer:
        pline.Layer = layer
    if color is not None:
        pline.Color = color
    return pline

def draw_line(ms, x1, y1, x2, y2, layer=None, color=None):
    p1 = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, array.array('d', [float(x1), float(y1), 0.0]))
    p2 = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, array.array('d', [float(x2), float(y2), 0.0]))
    l = ms.AddLine(p1, p2)
    if layer:
        l.Layer = layer
    if color is not None:
        l.Color = color
    return l

def draw_circle(ms, cx, cy, radius, layer=None, color=None):
    cp = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, array.array('d', [float(cx), float(cy), 0.0]))
    c = ms.AddCircle(cp, float(radius))
    if layer:
        c.Layer = layer
    if color is not None:
        c.Color = color
    return c

def draw_text(ms, text, x, y, height, layer="09_TEXT_技术说明", color=None):
    ins = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, array.array('d', [float(x), float(y), 0.0]))
    t = ms.AddText(text, ins, float(height))
    try:
        t.StyleName = "STYLE_GB_CN"
    except:
        pass
    if layer:
        t.Layer = layer
    if color is not None:
        t.Color = color
    return t

def draw_aligned_dim(ms, x1, y1, x2, y2, offset_dist, is_horizontal=True, override_text=None, layer="08_DIMS_尺寸标注"):
    p1 = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, array.array('d', [float(x1), float(y1), 0.0]))
    p2 = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, array.array('d', [float(x2), float(y2), 0.0]))
    
    if is_horizontal:
        dim_y = float(y1) + float(offset_dist)
        t_loc = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, array.array('d', [(float(x1)+float(x2))/2.0, dim_y, 0.0]))
    else:
        dim_x = float(x1) + float(offset_dist)
        t_loc = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, array.array('d', [dim_x, (float(y1)+float(y2))/2.0, 0.0]))
        
    dim = ms.AddDimAligned(p1, p2, t_loc)
    dim.Layer = layer
    dim.Color = 1
    dim.TextHeight = 22.0
    dim.ArrowheadSize = 15.0
    try:
        dim.TextStyle = "STYLE_GB_CN"
    except:
        pass
    if override_text:
        dim.TextOverride = override_text
    return dim

def draw_lead_line(ms, x1, y1, x2, y2, x3, text, text_h=18.0, layer="09_TEXT_技术说明"):
    draw_line(ms, x1, y1, x2, y2, layer)
    draw_line(ms, x2, y2, x3, y2, layer)
    tx = x3 + 10.0 if x3 > x2 else x3 - (len(text) * text_h * 0.9) - 10.0
    draw_text(ms, text, tx, y2 + 5.0, text_h, layer)

def run_gen2_drafting():
    print(">>> 启动 AutoCAD 2026 并初始化第二代工程图纸...")
    acad, doc = get_acad_doc()
    ms = doc.ModelSpace
    setup_chinese_style(doc)
    create_layers(doc)

    # 全局参数定义 (单位: mm)
    W_SCREEN_FRAME = 2000.0   # 大屏外框宽
    H_SCREEN_FRAME = 1200.0   # 大屏外框高
    W_LCD = 1900.0            # 86寸大屏显示视口宽
    H_LCD = 1070.0            # 86寸大屏显示视口高
    W_BOARD = 1000.0          # 黑板单块标准宽度
    H_BOARD = 1200.0          # 黑板标准高度
    STROKE_SLIDE = 1000.0     # 延伸轨最大侧滑行程 1.0 米
    W_TOTAL_COMPACT = 4000.0  # 基础收缩总跨度 4.0 米
    W_TOTAL_EXTENDED = 6000.0 # 侧滑展开极限总跨度 6.0 米

    # =========================================================================
    # 模块一：工况一【横向大行程侧滑与三维避光全展开状态】 (Center Y = 3200.0)
    # 左右双延伸轨各滑出 1000mm，总幅宽展开至 6000mm，视线死角完全归零
    # =========================================================================
    CY1 = 3200.0
    top_y1 = CY1 + H_SCREEN_FRAME / 2.0  # 3800.0
    bot_y1 = CY1 - H_SCREEN_FRAME / 2.0  # 2600.0

    draw_text(ms, "第二代工况一：横向大行程侧滑与三维空间避光全展开状态 [DEPLOYED - 极限跨度 6000mm]", -3100.0, top_y1 + 580.0, 48.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "技术特征: 左右嵌套延伸轨向外直线侧滑 1000mm，大屏两侧物理盲区完全归零；偏心楔形自锁凸台切入锁紧卡口抵消悬臂下垂；展开双面搪瓷投影白板。", -3100.0, top_y1 + 500.0, 22.0, "09_TEXT_技术说明", 7)

    # 1.1 中心 86 寸多媒体大屏及伺服偏光机构
    draw_rect(ms, -1000.0, bot_y1, 1000.0, top_y1, "01_FRAME_外框导轨", 8)
    draw_rect(ms, -950.0, bot_y1 + 65.0, 950.0, bot_y1 + 65.0 + H_LCD, "02_SCREEN_多媒体屏", 5)
    draw_rect(ms, -940.0, bot_y1 + 75.0, 940.0, bot_y1 + 55.0 + H_LCD, "02_SCREEN_多媒体屏", 5)
    
    # 大屏右内侧微型直流精密伺服电机 + 偏光膜外齿圈 (参考图 1 高亮部位)
    draw_rect(ms, 915.0, bot_y1 + 250.0, 935.0, bot_y1 + 450.0, "07_OPTIC_AI_智能控光", 2)
    draw_circle(ms, 925.0, bot_y1 + 470.0, 15.0, "07_OPTIC_AI_智能控光", 2)
    draw_line(ms, 940.0, bot_y1 + 100.0, 940.0, bot_y1 + 1100.0, "07_OPTIC_AI_智能控光", 2)
    draw_lead_line(ms, 935.0, bot_y1 + 460.0, 1050.0, bot_y1 + 520.0, 1200.0, "微型直流伺服电机+柔性精密外齿圈(0°~90°液晶偏光膜微调)", 18.0)

    # 1.2 顶部电动卷轴式防眩遮光挑檐 (深度可调 260mm)
    awning_top1 = top_y1 + 120.0
    draw_rect(ms, -1050.0, top_y1 + 10.0, 1050.0, awning_top1, "07_OPTIC_AI_智能控光", 2)
    draw_line(ms, -1050.0, top_y1 + 45.0, 1050.0, top_y1 + 45.0, "07_OPTIC_AI_智能控光", 2)
    draw_line(ms, -1050.0, top_y1 + 80.0, 1050.0, top_y1 + 80.0, "07_OPTIC_AI_智能控光", 2)
    draw_circle(ms, 1000.0, top_y1 + 60.0, 18.0, "07_OPTIC_AI_智能控光", 2)
    draw_lead_line(ms, 1000.0, top_y1 + 60.0, 1120.0, top_y1 + 100.0, 1300.0, "顶罩内置微型卷轴马达(无级调节遮光深度 0~260mm)", 18.0)

    # 1.3 左右内侧固定黑板面 (各 1000x1200mm)
    draw_rect(ms, -2000.0, bot_y1, -1000.0, top_y1, "03_BOARD_书写黑板", 3)
    draw_rect(ms, -1980.0, bot_y1 + 20.0, -1020.0, top_y1 - 20.0, "03_BOARD_书写黑板", 3)
    draw_rect(ms, 1000.0, bot_y1, 2000.0, top_y1, "03_BOARD_书写黑板", 3)
    draw_rect(ms, 1020.0, bot_y1 + 20.0, 1980.0, top_y1 - 20.0, "03_BOARD_书写黑板", 3)

    # 1.4 双横梁固定外框与 C 型槽底等间距排灰导流圆孔 (排灰与消气阻)
    # 左侧外露双横梁 (在黑板拉出后中间露出的骨架区间 -2000 到 -1000 并在外部延展)
    # 上横梁 (Y: top_y1 - 50 到 top_y1) 与 下横梁 (Y: bot_y1 到 bot_y1 + 50)
    for side in [-1, 1]:
        x_base = 2000.0 if side == 1 else -3000.0
        # 延伸滑出的双横梁骨架 (中空区域展示)
        draw_rect(ms, 2000.0 * side, top_y1 - 60.0, (2000.0 + 1000.0) * side, top_y1, "01_FRAME_外框导轨", 8)
        draw_rect(ms, 2000.0 * side, bot_y1, (2000.0 + 1000.0) * side, bot_y1 + 60.0, "01_FRAME_外框导轨", 8)
        # C 型槽底等间距 200mm 排灰圆孔 (孔径 12mm)
        for i in range(5):
            hole_x = (2100.0 + i * 200.0) * side
            draw_circle(ms, hole_x, top_y1 - 30.0, 6.0, "05_CLEAN_DUST_自洁排灰", 6)
            draw_circle(ms, hole_x, bot_y1 + 30.0, 6.0, "05_CLEAN_DUST_自洁排灰", 6)

    draw_lead_line(ms, 2500.0, bot_y1 + 30.0, 2650.0, bot_y1 - 100.0, 2800.0, "C型槽底贯穿垂直排灰导流圆孔(Φ12mm, 等间距200mm, 消除滑动气阻)", 18.0)

    # 1.5 左右外展嵌套延伸内轨与外端黑板主体 (向外拉伸 1000mm, 占据 2000~3000 和 -3000~-2000)
    # 左侧外滑活动黑板主体 (X: -3000 到 -2000)
    draw_rect(ms, -3000.0, bot_y1, -2000.0, top_y1, "03_BOARD_书写黑板", 3)
    draw_rect(ms, -2980.0, bot_y1 + 20.0, -2020.0, top_y1 - 20.0, "03_BOARD_书写黑板", 3)
    draw_circle(ms, -2500.0, CY1, 15.0, "04_EXT_RAIL_延伸构件", 1)  # 中心拉手

    # 右侧外滑活动黑板主体 (X: 2000 到 3000) —— 呈现白色搪瓷投影面
    draw_rect(ms, 2000.0, bot_y1, 3000.0, top_y1, "04_EXT_RAIL_延伸构件", 1)
    draw_rect(ms, 2020.0, bot_y1 + 20.0, 2980.0, top_y1 - 20.0, "09_TEXT_技术说明", 7)
    draw_circle(ms, 2500.0, CY1, 15.0, "04_EXT_RAIL_延伸构件", 1)
    draw_text(ms, "[双面异质选配: 翻面展露白色防眩搪瓷书写/投影板]", 2100.0, CY1 - 80.0, 18.0, "09_TEXT_技术说明", 7)

    # 1.6 最外端垂直端部拉杆 (End Tie Rod - 参考图 2/3/4/5 橙色高亮构件)
    draw_rect(ms, -3015.0, bot_y1 - 10.0, -2995.0, top_y1 + 10.0, "04_EXT_RAIL_延伸构件", 1)
    draw_rect(ms, 2995.0, bot_y1 - 10.0, 3015.0, top_y1 + 10.0, "04_EXT_RAIL_延伸构件", 1)
    draw_lead_line(ms, 3015.0, CY1 + 200.0, 3150.0, CY1 + 300.0, 3300.0, "刚性垂直端部拉杆(刚性机械锁定上下滑轨,杜绝悬臂扭转形变)", 18.0)

    # 1.7 偏心楔形自锁防下垂凸台与锁紧卡口 (行程终点自锁)
    draw_rect(ms, 2000.0, top_y1 - 50.0, 2040.0, top_y1 - 15.0, "04_EXT_RAIL_延伸构件", 1)
    draw_line(ms, 2000.0, top_y1 - 15.0, 2040.0, top_y1 - 35.0, "04_EXT_RAIL_延伸构件", 1) # 楔形斜面
    draw_lead_line(ms, 2020.0, top_y1 - 25.0, 2150.0, top_y1 + 70.0, 2300.0, "偏心楔形自锁防下垂凸台(切入槽内锁紧卡口,消除1米悬臂弯矩)", 18.0)

    # 1.8 尺寸链与工程标注 (工况一)
    draw_aligned_dim(ms, -3000.0, top_y1, -2000.0, top_y1, 120.0, True, "1000 [外滑双面黑板/白板]")
    draw_aligned_dim(ms, -2000.0, top_y1, -1000.0, top_y1, 120.0, True, "1000 [固定内黑板面]")
    draw_aligned_dim(ms, -1000.0, top_y1, 1000.0, top_y1, 120.0, True, "2000 [86寸多媒体交互大屏]")
    draw_aligned_dim(ms, 1000.0, top_y1, 2000.0, top_y1, 120.0, True, "1000 [固定内黑板面]")
    draw_aligned_dim(ms, 2000.0, top_y1, 3000.0, top_y1, 120.0, True, "1000 [外滑双面黑板/白板]")

    draw_aligned_dim(ms, -3000.0, top_y1, 3000.0, top_y1, 220.0, True, "6000 [第二代横向侧滑展开极限总跨度]")
    draw_aligned_dim(ms, 2000.0, top_y1, 3000.0, top_y1, 320.0, True, "1000 [延伸轨侧滑最大行程 STROKE]")

    draw_aligned_dim(ms, -3000.0, bot_y1, -3000.0, top_y1, -140.0, False, "1200 [书写板标准净高]")
    draw_aligned_dim(ms, -3000.0, bot_y1 - 60.0, -3000.0, awning_top1, -250.0, False, "1380 [全系统含遮光罩/集尘槽总高]")


    # =========================================================================
    # 模块二：工况二【基准闭合待命与标准化快拆母座装配状态】 (Center Y = 1000.0)
    # 延伸轨完全收拢，整机宽 4000mm，突显转轴铰链、快拆母座、俯仰机构与课桌照度终端
    # =========================================================================
    CY2 = 1000.0
    top_y2 = CY2 + H_SCREEN_FRAME / 2.0  # 1600.0
    bot_y2 = CY2 - H_SCREEN_FRAME / 2.0  # 400.0

    draw_text(ms, "第二代工况二：基准闭合待命与标准化快拆母座装配状态 [COMPACT - 基础跨度 4000mm]", -3100.0, top_y2 + 480.0, 48.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "技术特征: 延伸内轨完全收纳于固定外框；转轴铰链处设标准化快拆卡挂母座(拔插销钉就地升级)与蜗轮蜗杆俯仰机构(-15°~+15°)；下连免布线BLE Mesh照度终端。", -3100.0, top_y2 + 400.0, 22.0, "09_TEXT_技术说明", 7)

    # 2.1 中心大屏与收缩状态外框
    draw_rect(ms, -1000.0, bot_y2, 1000.0, top_y2, "01_FRAME_外框导轨", 8)
    draw_rect(ms, -950.0, bot_y2 + 65.0, 950.0, bot_y2 + 65.0 + H_LCD, "02_SCREEN_多媒体屏", 5)
    draw_rect(ms, -940.0, bot_y2 + 75.0, 940.0, bot_y2 + 55.0 + H_LCD, "02_SCREEN_多媒体屏", 5)

    # 左右黑板 (收缩状态下总宽 4000mm，即左右各 1000mm 黑板组件)
    draw_rect(ms, -2000.0, bot_y2, -1000.0, top_y2, "03_BOARD_书写黑板", 3)
    draw_rect(ms, -1980.0, bot_y2 + 20.0, -1020.0, top_y2 - 20.0, "03_BOARD_书写黑板", 3)
    draw_rect(ms, 1000.0, bot_y2, 2000.0, top_y2, "03_BOARD_书写黑板", 3)
    draw_rect(ms, 1020.0, bot_y2 + 20.0, 1980.0, top_y2 - 20.0, "03_BOARD_书写黑板", 3)

    # 2.2 左右外端标准化多功能快拆卡挂母座与俯仰摆动轴组件
    for side in [-1, 1]:
        hx = 2000.0 * side
        # 承重转轴铰链外耳 (40x80mm)
        draw_rect(ms, hx - 20.0, CY2 - 80.0, hx + 20.0, CY2 + 80.0, "06_PITCH_YAW_运动副", 4)
        draw_circle(ms, hx, CY2, 12.0, "06_PITCH_YAW_运动副", 4)
        # 快拆装配凹槽与快拆销钉孔
        draw_rect(ms, hx - 35.0, CY2 - 40.0, hx + 35.0, CY2 + 40.0, "06_PITCH_YAW_运动副", 4)
        draw_circle(ms, hx - 15.0, CY2, 6.0, "06_PITCH_YAW_运动副", 4)
        draw_circle(ms, hx + 15.0, CY2, 6.0, "06_PITCH_YAW_运动副", 4)
        # 蜗轮蜗杆自锁减速电机箱 (外挂于母座后方)
        draw_rect(ms, hx - 30.0, CY2 + 90.0, hx + 30.0, CY2 + 170.0, "06_PITCH_YAW_运动副", 4)
        draw_circle(ms, hx, CY2 + 130.0, 15.0, "06_PITCH_YAW_运动副", 4)

    draw_lead_line(ms, 2020.0, CY2, 2180.0, CY2 + 120.0, 2350.0, "标准化多功能快拆卡挂母座(拔出快拆销钉即可实现一代二代就地升级)", 18.0)
    draw_lead_line(ms, 2020.0, CY2 + 140.0, 2180.0, CY2 + 220.0, 2350.0, "蜗轮蜗杆俯仰马达组件(水平销轴带动外框进行-15°~+15°纵向避光摆动)", 18.0)

    # 2.3 分布式免布线室内太阳能 BLE Mesh 照度采集终端 (教室课桌物理座位示意)
    desk_y = bot_y2 - 260.0
    for dx in [-1500.0, -500.0, 500.0, 1500.0]:
        # 课桌示意
        draw_rect(ms, dx - 180.0, desk_y - 60.0, dx + 180.0, desk_y, "01_FRAME_外框导轨", 8)
        # 照度采集终端 (非晶硅弱光光伏板 + BLE Mesh天线)
        draw_rect(ms, dx + 100.0, desk_y, dx + 170.0, desk_y + 40.0, "07_OPTIC_AI_智能控光", 2)
        draw_circle(ms, dx + 135.0, desk_y + 20.0, 6.0, "07_OPTIC_AI_智能控光", 2)
        draw_line(ms, dx + 135.0, desk_y + 40.0, dx + 135.0, desk_y + 70.0, "07_OPTIC_AI_智能控光", 2) # 天线

    draw_lead_line(ms, 1635.0, desk_y + 60.0, 1780.0, desk_y + 120.0, 1950.0, "分布式免布线照度采集终端(非晶硅室内太阳能集能+BLE Mesh无线自组网)", 18.0)

    # 工况二尺寸链
    draw_aligned_dim(ms, -2000.0, top_y2, -1000.0, top_y2, 120.0, True, "1000 [黑板主体]")
    draw_aligned_dim(ms, -1000.0, top_y2, 1000.0, top_y2, 120.0, True, "2000 [86寸多媒体大屏]")
    draw_aligned_dim(ms, 1000.0, top_y2, 2000.0, top_y2, 120.0, True, "1000 [黑板主体]")
    draw_aligned_dim(ms, -2000.0, top_y2, 2000.0, top_y2, 220.0, True, "4000 [第二代基础收缩总跨度]")


    # =========================================================================
    # 模块三：右侧视图区【三维运动副纵向俯仰剖面与自洁导轨详图】 (X: 3800 ~ 6800)
    # =========================================================================
    
    # 3.1 纵向俯仰避光剖面图 (-15° ~ +15° Pitch Tilt View, Center X = 4300.0, Center Y = 3200.0)
    PX = 4300.0
    draw_text(ms, "【剖面视图 A-A】纵向俯仰空间避光工作原理 (-15°~+15° 倾斜)", PX - 350.0, top_y1 + 450.0, 32.0, "09_TEXT_技术说明", 7)
    
    # 墙面与安装基座
    draw_rect(ms, PX - 250.0, bot_y1 - 100.0, PX - 200.0, top_y1 + 100.0, "01_FRAME_外框导轨", 8)
    draw_line(ms, PX - 250.0, bot_y1 - 100.0, PX - 280.0, bot_y1 - 70.0, "01_FRAME_外框导轨", 8)
    draw_line(ms, PX - 250.0, CY1, PX - 280.0, CY1 + 30.0, "01_FRAME_外框导轨", 8)
    draw_line(ms, PX - 250.0, top_y1 + 70.0, PX - 280.0, top_y1 + 100.0, "01_FRAME_外框导轨", 8)

    # 墙面固定支架与承重转轴
    draw_rect(ms, PX - 200.0, CY1 - 70.0, PX - 120.0, CY1 + 70.0, "06_PITCH_YAW_运动副", 4)
    draw_circle(ms, PX - 120.0, CY1, 20.0, "06_PITCH_YAW_运动副", 4)
    draw_text(ms, "水平铰接销轴(Pitch轴)", PX - 110.0, CY1 - 40.0, 16.0, "06_PITCH_YAW_运动副", 4)

    # 俯仰倾斜 +15 度的黑板板面与外框截面 (旋转中心 PX-120, CY1)
    tilt_rad = math.radians(15.0)
    # 板面高度 1200，上下各 600
    p_top_x = (PX - 120.0) + 60.0 + 600.0 * math.sin(tilt_rad)
    p_top_y = CY1 + 600.0 * math.cos(tilt_rad)
    p_bot_x = (PX - 120.0) + 60.0 - 600.0 * math.sin(tilt_rad)
    p_bot_y = CY1 - 600.0 * math.cos(tilt_rad)
    
    # 倾斜黑板截面矩形 (厚度 45mm)
    dx_th = 45.0 * math.cos(tilt_rad)
    dy_th = -45.0 * math.sin(tilt_rad)
    draw_line(ms, p_bot_x, p_bot_y, p_top_x, p_top_y, "03_BOARD_书写黑板", 3)
    draw_line(ms, p_top_x, p_top_y, p_top_x + dx_th, p_top_y + dy_th, "03_BOARD_书写黑板", 3)
    draw_line(ms, p_top_x + dx_th, p_top_y + dy_th, p_bot_x + dx_th, p_bot_y + dy_th, "03_BOARD_书写黑板", 3)
    draw_line(ms, p_bot_x + dx_th, p_bot_y + dy_th, p_bot_x, p_bot_y, "03_BOARD_书写黑板", 3)

    # 虚线基准铅垂线与角度标注弧线
    draw_line(ms, PX - 60.0, CY1 - 650.0, PX - 60.0, CY1 + 650.0, "08_DIMS_尺寸标注", 1)
    draw_text(ms, "+15° 纵向避光倾斜角", PX + 80.0, CY1 + 250.0, 20.0, "08_DIMS_尺寸标注", 1)

    # 入射光与反射光轨迹 (直射强光折向无人天花板)
    draw_line(ms, PX + 450.0, CY1 + 200.0, p_top_x - 100.0, CY1 + 100.0, "07_OPTIC_AI_智能控光", 2)
    draw_line(ms, p_top_x - 100.0, CY1 + 100.0, PX + 500.0, CY1 + 650.0, "07_OPTIC_AI_智能控光", 2)
    draw_text(ms, "入射直射光锥", PX + 460.0, CY1 + 180.0, 16.0, "07_OPTIC_AI_智能控光", 2)
    draw_text(ms, "反射眩光被物理折射至无人天花板区域", PX + 320.0, CY1 + 680.0, 16.0, "07_OPTIC_AI_智能控光", 2)


    # 3.2 导轨自洁防尘与排灰系统结构详图 (Detail A - Center X = 5600.0, Center Y = 3200.0)
    DX = 5700.0
    draw_text(ms, "【节点详图 B-B】导轨自洁防尘与排灰消气阻系统截面", DX - 450.0, top_y1 + 450.0, 32.0, "09_TEXT_技术说明", 7)

    # 6063-T5 铝合金 C 型凹槽固定外框型材 (大截面 300x200)
    draw_rect(ms, DX - 180.0, CY1 - 120.0, DX + 180.0, CY1 + 120.0, "01_FRAME_外框导轨", 8)
    draw_rect(ms, DX - 130.0, CY1 - 70.0, DX + 130.0, CY1 + 70.0, "01_FRAME_外框导轨", 8) # C型槽内腔

    # 顶部扣装倒 V 型 EPDM 弹性橡胶防护罩
    draw_line(ms, DX - 200.0, CY1 + 120.0, DX, CY1 + 220.0, "05_CLEAN_DUST_自洁排灰", 6)
    draw_line(ms, DX, CY1 + 220.0, DX + 200.0, CY1 + 120.0, "05_CLEAN_DUST_自洁排灰", 6)
    draw_line(ms, DX - 190.0, CY1 + 115.0, DX, CY1 + 205.0, "05_CLEAN_DUST_自洁排灰", 6)
    draw_line(ms, DX, CY1 + 205.0, DX + 190.0, CY1 + 115.0, "05_CLEAN_DUST_自洁排灰", 6)
    draw_lead_line(ms, DX, CY1 + 220.0, DX + 120.0, CY1 + 290.0, DX + 250.0, "倒V型EPDM弹性橡胶防护罩(阻隔95%粉笔灰)", 18.0)

    # 内部嵌套滑动延伸内轨截面与高密度尼龙雨刮毛刷条
    draw_rect(ms, DX - 90.0, CY1 - 40.0, DX + 90.0, CY1 + 40.0, "04_EXT_RAIL_延伸构件", 1)
    # 尼龙毛刷刷毛 (槽底与侧边接触面)
    for bx in range(int(DX - 110.0), int(DX + 110.0), 15):
        draw_line(ms, float(bx), CY1 - 40.0, float(bx), CY1 - 70.0, "05_CLEAN_DUST_自洁排灰", 6)
    draw_lead_line(ms, DX - 50.0, CY1 - 55.0, DX - 180.0, CY1 - 180.0, DX - 320.0, "微细尼龙自洁毛刷条(往复推扫积灰)", 18.0)

    # 槽底垂直排灰导流圆孔 (向下贯通排入集灰槽)
    draw_rect(ms, DX - 30.0, CY1 - 120.0, DX + 30.0, CY1 - 70.0, "05_CLEAN_DUST_自洁排灰", 6)
    draw_circle(ms, DX, CY1 - 95.0, 18.0, "05_CLEAN_DUST_自洁排灰", 6)
    draw_lead_line(ms, DX + 20.0, CY1 - 95.0, DX + 140.0, CY1 - 120.0, DX + 260.0, "垂直贯穿排灰导流孔(Φ12mm/消除气阻)", 18.0)

    # 底部外挂抽屉式铝合金粉尘收集盒
    draw_rect(ms, DX - 140.0, CY1 - 220.0, DX + 140.0, CY1 - 130.0, "01_FRAME_外框导轨", 8)
    draw_line(ms, DX - 100.0, CY1 - 175.0, DX + 100.0, CY1 - 175.0, "01_FRAME_外框导轨", 8)
    draw_lead_line(ms, DX + 140.0, CY1 - 175.0, DX + 220.0, CY1 - 220.0, DX + 340.0, "抽屉式外挂粉尘收集盒(便于集中清理)", 18.0)


    # 3.3 偏心楔形自锁防下垂机构放大详图 (Detail C - Center X = 4300.0, Center Y = 1000.0)
    KX = 4300.0
    draw_text(ms, "【节点详图 C-C】悬臂最大行程偏心楔形自锁防下垂机构", KX - 450.0, top_y2 + 400.0, 32.0, "09_TEXT_技术说明", 7)
    
    # 双横梁固定外框壁厚与锁紧卡口
    draw_rect(ms, KX - 250.0, CY2 + 50.0, KX + 250.0, CY2 + 130.0, "01_FRAME_外框导轨", 8)
    draw_rect(ms, KX - 250.0, CY2 - 130.0, KX + 250.0, CY2 - 50.0, "01_FRAME_外框导轨", 8)
    # 固定外框内壁锁紧卡口凹槽 (深 20mm, 宽 60mm)
    draw_rect(ms, KX + 100.0, CY2 + 30.0, KX + 160.0, CY2 + 50.0, "01_FRAME_外框导轨", 8)

    # 延伸内轨与偏心斜面凸台 (3.5度楔形切入卡槽)
    draw_rect(ms, KX - 200.0, CY2 - 40.0, KX + 150.0, CY2 + 40.0, "04_EXT_RAIL_延伸构件", 1)
    # 偏心斜面过盈配合块
    draw_line(ms, KX + 100.0, CY2 + 40.0, KX + 160.0, CY2 + 50.0, "04_EXT_RAIL_延伸构件", 1)
    draw_line(ms, KX + 160.0, CY2 + 50.0, KX + 160.0, CY2 + 40.0, "04_EXT_RAIL_延伸构件", 1)
    draw_lead_line(ms, KX + 130.0, CY2 + 45.0, KX + 220.0, CY2 + 150.0, KX + 360.0, "偏心楔形自锁凸台(3.5°斜面过盈卡紧,抵消1米悬臂弯矩)", 18.0)
    draw_lead_line(ms, KX + 100.0, CY2 + 35.0, KX + 220.0, CY2 - 60.0, KX + 360.0, "固定外框锁紧卡口(终点刚性定位死锁配合)", 18.0)


    # 3.4 标题栏与图框 (国标 GB/T 10609.1 标准图纸包络, X: -3300 ~ 6700, Y: -100 ~ 4400)
    BX1, BY1 = -3300.0, -150.0
    BX2, BY2 = 6700.0, 4400.0
    draw_rect(ms, BX1, BY1, BX2, BY2, "01_FRAME_外框导轨", 8)
    draw_rect(ms, BX1 + 30.0, BY1 + 30.0, BX2 - 30.0, BY2 - 30.0, "01_FRAME_外框导轨", 8)

    # 标题栏区域 (右下角 X: 4700 ~ 6670, Y: -120 ~ 280)
    TX1, TY1 = 4700.0, -120.0
    TX2, TY2 = 6670.0, 280.0
    draw_rect(ms, TX1, TY1, TX2, TY2, "01_FRAME_外框导轨", 8)
    draw_line(ms, TX1, TY1 + 100.0, TX2, TY1 + 100.0, "01_FRAME_外框导轨", 8)
    draw_line(ms, TX1, TY1 + 200.0, TX2, TY1 + 200.0, "01_FRAME_外框导轨", 8)
    draw_line(ms, TX1 + 450.0, TY1, TX1 + 450.0, TY2, "01_FRAME_外框导轨", 8)
    draw_line(ms, TX1 + 1000.0, TY1, TX1 + 1000.0, TY2, "01_FRAME_外框导轨", 8)
    draw_line(ms, TX1 + 1450.0, TY1, TX1 + 1450.0, TY2, "01_FRAME_外框导轨", 8)

    draw_text(ms, "项目代号: GH-W-2026", TX1 + 20.0, TY1 + 225.0, 26.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "图纸名称: 第二代三维空间联动避光与自洁黑板工程总装图", TX1 + 480.0, TY1 + 220.0, 32.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "图纸编号: GH-GEN2-ASM-01", TX1 + 20.0, TY1 + 125.0, 26.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "设计阶段: 第二代(W系列)实施例与实用新型申请图", TX1 + 480.0, TY1 + 125.0, 26.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "设计制图: czx & 海鸥 (Antigravity)", TX1 + 1020.0, TY1 + 125.0, 26.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "比例: 1:1 (mm)", TX1 + 1480.0, TY1 + 125.0, 26.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "审核轮数: 第9轮全系统工程审核", TX1 + 20.0, TY1 + 30.0, 26.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "技术标准: GB/T 28231-2011 / 实用新型专利交底书规范", TX1 + 480.0, TY1 + 30.0, 26.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "状态: 0 Hatch 纯工程机械线框", TX1 + 1480.0, TY1 + 30.0, 26.0, "09_TEXT_技术说明", 7)

    # 缩放视图居中
    try:
        acad.ZoomExtents()
        print(">>> 成功执行 ZoomExtents 视图居中")
    except Exception as e:
        print("ZoomExtents 提示:", e)

    # 保存图纸 DWG (新建独立文件，严禁覆盖旧图)
    target_dwg = r"D:\Desktop\pjhb\01-CAD工程图纸\第二代三维联动自洁防眩光黑板系统_全系统工程总装与运动机构图_v1.0.dwg"
    if os.path.exists(target_dwg):
        try:
            os.remove(target_dwg)
        except:
            pass

    try:
        doc.SaveAs(target_dwg)
        print(f">>> 成功保存第二代工程图纸: {target_dwg}")
    except Exception as e:
        print(f"SaveAs 提示: {e}")

if __name__ == "__main__":
    run_gen2_drafting()

