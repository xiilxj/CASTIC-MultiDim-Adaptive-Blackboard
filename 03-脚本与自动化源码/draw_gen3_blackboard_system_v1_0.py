# -*- coding: utf-8 -*-
"""
第三代多维叠合翻转全覆盖与三维自洁侧滑智能教学黑板系统 - AutoCAD 2026 自动化工程总装绘图脚本 (v1.0)
文件版本: v1.0
核心特性:
1. 0 Hatch 纯工程机械线框制图；
2. 呈现第三代核心三工况：
   - 工况一【初始闭合·市面主流全覆盖封屏形态 (COVERED 4000mm)】：内缘铰链铺开180°，两扇内层板在屏幕前合拢封屏，100%遮蔽大屏；
   - 工况二【常态多媒体·大屏露显双层叠合形态 (COMPACT 4000mm)】：内缘铰链回折，两块超薄板紧密附加叠合于两侧，露显86寸大屏；
   - 工况三【大视野与避光·平移侧滑极限展开形态 (DEPLOYED 6000mm)】：叠合板沿延伸轨外展1.0米，总宽达6000mm，盲区归零；
3. 包含内缘铰链翻展剖面、纵向俯仰避光剖面与自洁排灰详图；
4. 全系统标注与标准工程标题栏。
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
        ("01_FRAME_外框型材", 8),       # 灰色 (型材、导轨、框体)
        ("02_SCREEN_多媒体屏", 5),      # 蓝色 (86寸大屏、液晶偏光膜)
        ("03_OUTER_BOARD_外主板", 3),   # 绿色 (外层主黑板)
        ("04_INNER_BOARD_内附板", 2),   # 黄色 (内层附加超薄黑板)
        ("05_INNER_HINGE_内缘铰链", 6), # 品红 (内缘多维铺开铰链)
        ("06_EXT_RAIL_延伸构件", 1),    # 红色 (嵌套延伸轨、自锁凸台、端部拉杆)
        ("07_PITCH_YAW_运动副", 4),     # 青色 (快拆母座、俯仰销轴、蜗轮蜗杆)
        ("08_DIMS_尺寸标注", 1),        # 红色 (机械尺寸链、行程与公差)
        ("09_TEXT_技术说明", 7)         # 白色/黑色 (说明文字与标题栏)
    ]
    for name, col in layers_info:
        try:
            lay = doc.Layers.Add(name)
            lay.Color = col
        except:
            pass
    print(">>> 9 大第三代标准工程图层创建完毕")

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

def run_gen3_drafting():
    print(">>> 启动 AutoCAD 2026 并初始化第三代工程图纸...")
    acad, doc = get_acad_doc()
    ms = doc.ModelSpace
    setup_chinese_style(doc)
    create_layers(doc)

    H_BOARD = 1200.0
    H_LCD = 1070.0

    # =========================================================================
    # 工况一：初始闭合·市面主流全覆盖封屏形态 (Center Y = 4600.0)
    # 内缘铰链向中心铺开180°，两扇内层板在屏幕前合拢封屏，100%遮蔽大屏
    # =========================================================================
    CY1 = 4600.0
    top_y1 = CY1 + 600.0  # 5200
    bot_y1 = CY1 - 600.0  # 4000

    draw_text(ms, "第三代工况一：初始闭合·市面主流全覆盖封屏形态 [COVERED - 传统主流全封闭 4000mm]", -3050.0, top_y1 + 450.0, 42.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "技术特征: 左右黑板成二分层(两块超薄板)；靠大屏内侧增设内缘铰链向中心铺开180°并在中央合拢自锁，完全遮蔽86寸大屏，呈现主流推拉黑板纯板书全覆盖形态。", -3050.0, top_y1 + 390.0, 20.0, "09_TEXT_技术说明", 7)

    # 后方被遮蔽的 86 寸大屏外框 (虚线图示)
    draw_rect(ms, -1000.0, bot_y1, 1000.0, top_y1, "02_SCREEN_多媒体屏", 5)
    draw_text(ms, "[86寸多媒体大屏被100%封闭在背后保护防撞]", -700.0, CY1 + 250.0, 20.0, "02_SCREEN_多媒体屏", 5)

    # 左右外层主板 (X: -2000~-1000, 1000~2000)
    draw_rect(ms, -2000.0, bot_y1, -1000.0, top_y1, "03_OUTER_BOARD_外主板", 3)
    draw_rect(ms, -1980.0, bot_y1 + 20.0, -1020.0, top_y1 - 20.0, "03_OUTER_BOARD_外主板", 3)
    draw_rect(ms, 1000.0, bot_y1, 2000.0, top_y1, "03_OUTER_BOARD_外主板", 3)
    draw_rect(ms, 1020.0, bot_y1 + 20.0, 1980.0, top_y1 - 20.0, "03_OUTER_BOARD_外主板", 3)

    # 铺开在大屏正前方的左右内层附加板 (X: -1000~0, 0~1000)
    draw_rect(ms, -1000.0, bot_y1, 0.0, top_y1, "04_INNER_BOARD_内附板", 2)
    draw_rect(ms, -980.0, bot_y1 + 20.0, -20.0, top_y1 - 20.0, "04_INNER_BOARD_内附板", 2)
    draw_rect(ms, 0.0, bot_y1, 1000.0, top_y1, "04_INNER_BOARD_内附板", 2)
    draw_rect(ms, 20.0, bot_y1 + 20.0, 980.0, top_y1 - 20.0, "04_INNER_BOARD_内附板", 2)

    # 多维内缘铺开铰链 (设于 X=-1000 和 X=1000 靠近大屏内缘处)
    for hx in [-1000.0, 1000.0]:
        draw_rect(ms, hx - 15.0, CY1 - 250.0, hx + 15.0, CY1 - 150.0, "05_INNER_HINGE_内缘铰链", 6)
        draw_circle(ms, hx, CY1 - 200.0, 8.0, "05_INNER_HINGE_内缘铰链", 6)
        draw_rect(ms, hx - 15.0, CY1 + 150.0, hx + 15.0, CY1 + 250.0, "05_INNER_HINGE_内缘铰链", 6)
        draw_circle(ms, hx, CY1 + 200.0, 8.0, "05_INNER_HINGE_内缘铰链", 6)

    draw_lead_line(ms, -1000.0, CY1 + 200.0, -1120.0, CY1 + 260.0, -1250.0, "多维内缘铺开铰链(大屏内侧竖边,向内铺展180°封屏)", 18.0)
    draw_lead_line(ms, 0.0, CY1, 150.0, CY1 + 80.0, 280.0, "中央碰珠式磁吸机械对撞锁紧缝(全覆盖平整拼接)", 18.0)

    # 尺寸标注 (工况一)
    draw_aligned_dim(ms, -2000.0, top_y1, -1000.0, top_y1, 100.0, True, "1000 [外层主板]")
    draw_aligned_dim(ms, -1000.0, top_y1, 0.0, top_y1, 100.0, True, "1000 [铺开内板A]")
    draw_aligned_dim(ms, 0.0, top_y1, 1000.0, top_y1, 100.0, True, "1000 [铺开内板B]")
    draw_aligned_dim(ms, 1000.0, top_y1, 2000.0, top_y1, 100.0, True, "1000 [外层主板]")
    draw_aligned_dim(ms, -2000.0, top_y1, 2000.0, top_y1, 180.0, True, "4000 [主流全覆盖纯板书总跨度]")
    draw_aligned_dim(ms, -1000.0, top_y1, 1000.0, top_y1, 260.0, True, "2000 [全覆盖完全遮蔽大屏跨度]")


    # =========================================================================
    # 工况二：常态多媒体·大屏露显双层叠合形态 (Center Y = 2800.0)
    # 内缘铰链回折，两块超薄板紧密附加叠合于大屏两侧，大屏全景呈现
    # =========================================================================
    CY2 = 2800.0
    top_y2 = CY2 + 600.0  # 3400
    bot_y2 = CY2 - 600.0  # 2200

    draw_text(ms, "第三代工况二：常态多媒体·大屏露显双层叠合形态 [COMPACT - 黄金视域 4000mm]", -3050.0, top_y2 + 450.0, 42.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "技术特征: 内缘铰链折回，内层附加板与外层主板附加叠合为一体(叠合厚度仅26mm)；86寸多媒体屏完全露显；大屏右内侧配置伺服驱动偏光膜机构。", -3050.0, top_y2 + 390.0, 20.0, "09_TEXT_技术说明", 7)

    # 中心大屏完全露显
    draw_rect(ms, -1000.0, bot_y2, 1000.0, top_y2, "01_FRAME_外框型材", 8)
    draw_rect(ms, -950.0, bot_y2 + 65.0, 950.0, bot_y2 + 65.0 + H_LCD, "02_SCREEN_多媒体屏", 5)
    draw_rect(ms, -940.0, bot_y2 + 75.0, 940.0, bot_y2 + 55.0 + H_LCD, "02_SCREEN_多媒体屏", 5)

    # 大屏右内侧微型伺服电机与偏光膜齿圈
    draw_rect(ms, 915.0, bot_y2 + 250.0, 935.0, bot_y2 + 450.0, "07_PITCH_YAW_运动副", 2)
    draw_circle(ms, 925.0, bot_y2 + 470.0, 15.0, "07_PITCH_YAW_运动副", 2)
    draw_line(ms, 940.0, bot_y2 + 100.0, 940.0, bot_y2 + 1100.0, "07_PITCH_YAW_运动副", 2)

    # 左右双层附加叠合板 (外层主板 + 内层附加板贴合)
    for side in [-1, 1]:
        bx1 = 1000.0 * side
        bx2 = 2000.0 * side
        draw_rect(ms, bx1, bot_y2, bx2, top_y2, "03_OUTER_BOARD_外主板", 3)
        draw_rect(ms, bx1 + (20.0*side), bot_y2 + 20.0, bx2 - (20.0*side), top_y2 - 20.0, "03_OUTER_BOARD_外主板", 3)
        draw_rect(ms, bx1 + (10.0*side), bot_y2 + 10.0, bx2 - (10.0*side), top_y2 - 10.0, "04_INNER_BOARD_内附板", 2)

    draw_lead_line(ms, -1500.0, CY2, -1650.0, CY2 + 100.0, -1800.0, "双层附加叠合黑板(外层主板12mm+内层附加板12mm叠合收拢)", 18.0)

    # 左右承重主铰链、快拆母座与蜗轮蜗杆俯仰马达
    for side in [-1, 1]:
        hx = 2000.0 * side
        draw_rect(ms, hx - 20.0, CY2 - 80.0, hx + 20.0, CY2 + 80.0, "07_PITCH_YAW_运动副", 4)
        draw_circle(ms, hx, CY2, 12.0, "07_PITCH_YAW_运动副", 4)
        draw_rect(ms, hx - 30.0, CY2 + 90.0, hx + 30.0, CY2 + 170.0, "07_PITCH_YAW_运动副", 4)
        draw_circle(ms, hx, CY2 + 130.0, 15.0, "07_PITCH_YAW_运动副", 4)

    draw_lead_line(ms, 2020.0, CY2, 2150.0, CY2 + 70.0, 2280.0, "标准化快拆卡挂母座(拔插销钉一二三代就地互换)", 18.0)

    # 尺寸标注 (工况二)
    draw_aligned_dim(ms, -2000.0, top_y2, -1000.0, top_y2, 100.0, True, "1000 [双层叠合板]")
    draw_aligned_dim(ms, -1000.0, top_y2, 1000.0, top_y2, 100.0, True, "2000 [86寸多媒体大屏]")
    draw_aligned_dim(ms, 1000.0, top_y2, 2000.0, top_y2, 100.0, True, "1000 [双层叠合板]")
    draw_aligned_dim(ms, -2000.0, top_y2, 2000.0, top_y2, 180.0, True, "4000 [常态多媒体教学总跨度]")


    # =========================================================================
    # 工况三：大视野与三维空间避光极限展开形态 (Center Y = 1000.0)
    # 叠合板沿二代滑轨向外直线侧滑1.0米，跨度扩展至6000mm，视线死角归零
    # =========================================================================
    CY3 = 1000.0
    top_y3 = CY3 + 600.0  # 1600
    bot_y3 = CY3 - 600.0  # 400

    draw_text(ms, "第三代工况三：大视野与三维空间避光极限展开形态 [DEPLOYED - 盲区归零 6000mm]", -3050.0, top_y3 + 450.0, 42.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "技术特征: 双层叠合板沿双横梁自洁延伸轨外滑1000mm，总幅宽展开至6000mm；偏心楔形自锁消除悬臂弯矩；联动俯仰轴-15°~+15°纵向折射避光。", -3050.0, top_y3 + 390.0, 20.0, "09_TEXT_技术说明", 7)

    # 中心大屏露显
    draw_rect(ms, -1000.0, bot_y3, 1000.0, top_y3, "01_FRAME_外框型材", 8)
    draw_rect(ms, -950.0, bot_y3 + 65.0, 950.0, bot_y3 + 65.0 + H_LCD, "02_SCREEN_多媒体屏", 5)

    # 露出双横梁固定外框与槽底每隔 200mm 排灰孔
    for side in [-1, 1]:
        draw_rect(ms, 2000.0 * side, top_y3 - 60.0, (2000.0 + 1000.0) * side, top_y3, "01_FRAME_外框型材", 8)
        draw_rect(ms, 2000.0 * side, bot_y3, (2000.0 + 1000.0) * side, bot_y3 + 60.0, "01_FRAME_外框型材", 8)
        for i in range(5):
            hx = (2100.0 + i * 200.0) * side
            draw_circle(ms, hx, top_y3 - 30.0, 6.0, "05_INNER_HINGE_内缘铰链", 6)
            draw_circle(ms, hx, bot_y3 + 30.0, 6.0, "05_INNER_HINGE_内缘铰链", 6)

    # 外展 1.0 米的黑板主体 (X: -3000~-2000, 2000~3000)
    draw_rect(ms, -3000.0, bot_y3, -2000.0, top_y3, "03_OUTER_BOARD_外主板", 3)
    draw_rect(ms, -2980.0, bot_y3 + 20.0, -2020.0, top_y3 - 20.0, "03_OUTER_BOARD_外主板", 3)

    draw_rect(ms, 2000.0, bot_y3, 3000.0, top_y3, "06_EXT_RAIL_延伸构件", 1)
    draw_rect(ms, 2020.0, bot_y3 + 20.0, 2980.0, top_y3 - 20.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "[异质选配: 翻面展露白色防眩搪瓷书写/投影板]", 2060.0, CY3 - 80.0, 18.0, "09_TEXT_技术说明", 7)

    # 最外端垂直端部拉杆
    draw_rect(ms, -3015.0, bot_y3 - 10.0, -2995.0, top_y3 + 10.0, "06_EXT_RAIL_延伸构件", 1)
    draw_rect(ms, 2995.0, bot_y3 - 10.0, 3015.0, top_y3 + 10.0, "06_EXT_RAIL_延伸构件", 1)
    draw_lead_line(ms, 3015.0, CY3 + 200.0, 3120.0, CY3 + 260.0, 3250.0, "刚性垂直端部拉杆(刚性机械锁定上下滑轨)", 18.0)

    # 尺寸标注 (工况三)
    draw_aligned_dim(ms, -3000.0, top_y3, -2000.0, top_y3, 100.0, True, "1000 [外滑黑板主体]")
    draw_aligned_dim(ms, -2000.0, top_y3, -1000.0, top_y3, 100.0, True, "1000 [外露自洁滑槽]")
    draw_aligned_dim(ms, -1000.0, top_y3, 1000.0, top_y3, 100.0, True, "2000 [86寸多媒体大屏]")
    draw_aligned_dim(ms, 1000.0, top_y3, 2000.0, top_y3, 100.0, True, "1000 [外露自洁滑槽]")
    draw_aligned_dim(ms, 2000.0, top_y3, 3000.0, top_y3, 100.0, True, "1000 [外滑黑板主体]")
    draw_aligned_dim(ms, -3000.0, top_y3, 3000.0, top_y3, 180.0, True, "6000 [侧滑平移推拉展开极限总跨度]")
    draw_aligned_dim(ms, 2000.0, top_y3, 3000.0, top_y3, 260.0, True, "1000 [延伸滑轨最大侧移行程]")


    # =========================================================================
    # 模块四：右侧剖面与详图区 (X: 3800 ~ 6800)
    # =========================================================================

    # 4.1 剖面 A-A：多维内缘铺开铰链双层叠合与翻转运动机构 (Center X = 4300, Center Y = 4600)
    PX1 = 4300.0
    draw_text(ms, "【剖面视图 A-A】内缘铰链双层叠合与铺开翻折运动原理", PX1 - 320.0, top_y1 + 450.0, 30.0, "09_TEXT_技术说明", 7)
    draw_rect(ms, PX1 - 200.0, CY1 - 80.0, PX1 - 140.0, CY1 + 80.0, "01_FRAME_外框型材", 8)
    draw_rect(ms, PX1 - 140.0, CY1 - 400.0, PX1 - 110.0, CY1 + 400.0, "03_OUTER_BOARD_外主板", 3)
    draw_text(ms, "外层主板(12mm)", PX1 - 135.0, CY1 - 440.0, 16.0, "03_OUTER_BOARD_外主板", 3)

    draw_circle(ms, PX1 - 110.0, CY1, 16.0, "05_INNER_HINGE_内缘铰链", 6)
    draw_circle(ms, PX1 - 110.0, CY1, 8.0, "05_INNER_HINGE_内缘铰链", 6)
    draw_lead_line(ms, PX1 - 110.0, CY1 + 16.0, PX1 - 40.0, CY1 + 90.0, PX1 + 80.0, "内缘铺开铰链枢轴(回转角0°~180°)", 18.0)

    draw_rect(ms, PX1 - 105.0, CY1 - 390.0, PX1 - 75.0, CY1 + 390.0, "04_INNER_BOARD_内附板", 2)
    draw_text(ms, "叠合态(厚26mm)", PX1 - 100.0, CY1 + 410.0, 16.0, "04_INNER_BOARD_内附板", 2)
    draw_rect(ms, PX1 - 110.0, CY1 - 15.0, PX1 + 350.0, CY1 + 15.0, "04_INNER_BOARD_内附板", 2)
    draw_text(ms, "180° 铺开封屏态(覆盖在86寸大屏正前方)", PX1 + 20.0, CY1 + 40.0, 18.0, "04_INNER_BOARD_内附板", 2)

    # 4.2 剖面 B-B：纵向俯仰避光原理 (-15°~+15°, Center X = 4300, Center Y = 2800)
    PX2 = 4300.0
    draw_text(ms, "【剖面视图 B-B】纵向俯仰避光与光锥折射原理 (-15°~+15°)", PX2 - 320.0, top_y2 + 450.0, 30.0, "09_TEXT_技术说明", 7)
    draw_rect(ms, PX2 - 240.0, CY2 - 300.0, PX2 - 190.0, CY2 + 300.0, "01_FRAME_外框型材", 8)
    draw_rect(ms, PX2 - 190.0, CY2 - 60.0, PX2 - 110.0, CY2 + 60.0, "07_PITCH_YAW_运动副", 4)
    draw_circle(ms, PX2 - 110.0, CY2, 18.0, "07_PITCH_YAW_运动副", 4)
    draw_text(ms, "水平铰接销轴(Pitch轴)", PX2 - 100.0, CY2 - 35.0, 16.0, "07_PITCH_YAW_运动副", 4)

    tilt_rad = math.radians(15.0)
    p_top_x = (PX2 - 110.0) + 50.0 + 580.0 * math.sin(tilt_rad)
    p_top_y = CY2 + 580.0 * math.cos(tilt_rad)
    p_bot_x = (PX2 - 110.0) + 50.0 - 580.0 * math.sin(tilt_rad)
    p_bot_y = CY2 - 580.0 * math.cos(tilt_rad)
    dx_th = 40.0 * math.cos(tilt_rad)
    dy_th = -40.0 * math.sin(tilt_rad)

    draw_line(ms, p_bot_x, p_bot_y, p_top_x, p_top_y, "03_OUTER_BOARD_外主板", 3)
    draw_line(ms, p_top_x, p_top_y, p_top_x + dx_th, p_top_y + dy_th, "03_OUTER_BOARD_外主板", 3)
    draw_line(ms, p_top_x + dx_th, p_top_y + dy_th, p_bot_x + dx_th, p_bot_y + dy_th, "03_OUTER_BOARD_外主板", 3)
    draw_line(ms, p_bot_x + dx_th, p_bot_y + dy_th, p_bot_x, p_bot_y, "03_OUTER_BOARD_外主板", 3)

    draw_line(ms, PX2 + 420.0, CY2 + 180.0, p_top_x - 90.0, CY2 + 90.0, "07_PITCH_YAW_运动副", 2)
    draw_line(ms, p_top_x - 90.0, CY2 + 90.0, PX2 + 460.0, CY2 + 620.0, "07_PITCH_YAW_运动副", 2)
    draw_text(ms, "入射直射强光", PX2 + 430.0, CY2 + 160.0, 16.0, "07_PITCH_YAW_运动副", 2)
    draw_text(ms, "反射眩光折射至天花板无人区", PX2 + 280.0, CY2 + 640.0, 16.0, "07_PITCH_YAW_运动副", 2)

    # 4.3 节点详图 C-C：导轨自洁截面 (Center X = 5600, Center Y = 1000)
    DX = 5600.0
    draw_text(ms, "【节点详图 C-C】自洁排灰导轨与悬臂防下垂自锁截面", DX - 380.0, top_y3 + 450.0, 30.0, "09_TEXT_技术说明", 7)
    draw_rect(ms, DX - 160.0, CY3 - 110.0, DX + 160.0, CY3 + 110.0, "01_FRAME_外框型材", 8)
    draw_rect(ms, DX - 120.0, CY3 - 65.0, DX + 120.0, CY3 + 65.0, "01_FRAME_外框型材", 1)
    draw_line(ms, DX - 180.0, CY3 + 110.0, DX, CY3 + 200.0, "05_INNER_HINGE_内缘铰链", 6)
    draw_line(ms, DX, CY3 + 200.0, DX + 180.0, CY3 + 110.0, "05_INNER_HINGE_内缘铰链", 6)
    draw_lead_line(ms, DX, CY3 + 200.0, DX + 100.0, CY3 + 260.0, DX + 220.0, "倒V型EPDM弹性橡胶防护罩", 18.0)
    draw_circle(ms, DX, CY3 - 88.0, 16.0, "05_INNER_HINGE_内缘铰链", 6)
    draw_lead_line(ms, DX + 18.0, CY3 - 88.0, DX + 120.0, CY3 - 110.0, DX + 240.0, "垂直贯穿排灰孔(Φ12mm,等距200mm)", 18.0)


    # =========================================================================
    # 模块五：标准图框、参数矩阵表与标题栏 (GB/T 10609.1)
    # =========================================================================
    draw_rect(ms, -3300.0, -250.0, 6700.0, 5400.0, "01_FRAME_外框型材", 8)
    draw_rect(ms, -3270.0, -220.0, 6670.0, 5370.0, "01_FRAME_外框型材", 8)

    # 参数表
    TAB_X1, TAB_X2 = -3200.0, 1300.0
    TAB_Y1, TAB_Y2 = -180.0, 320.0
    draw_rect(ms, TAB_X1, TAB_Y1, TAB_X2, TAB_Y2, "01_FRAME_外框型材", 8)
    draw_line(ms, TAB_X1, TAB_Y2 - 55.0, TAB_X2, TAB_Y2 - 55.0, "01_FRAME_外框型材", 8)
    draw_text(ms, "【第三代多维叠合全覆盖与三维自洁侧滑避光黑板系统 - 核心工程参数矩阵】", TAB_X1 + 25.0, TAB_Y2 - 40.0, 26.0, "09_TEXT_技术说明", 7)

    specs = [
        "1. 多维叠合分层架构: 左右黑板成二分层(外层主板12mm + 内层附加板12mm)，叠合装配总厚度仅26mm，完全不占用教室前台纵深。",
        "2. 内缘铰链铺开封屏自由度: 设于大屏内侧竖直边缘，回转角0°~180°；闭合时向中心完全铺开合拢，100%遮蔽大屏，呈现主流全覆盖黑板形态。",
        "3. 常态大屏露显双层叠合: 内缘铰链回折后两层板紧密附加贴合，露出中间2000mm 86寸大屏，左右各1000mm板面可用，整机总宽4000mm。",
        "4. 大行程侧滑推拉展开: 叠合黑板沿双横梁自洁延伸轨外滑1000mm，总幅宽展开至6000mm，彻底消除86寸大屏两侧物理盲区与视线死角。",
        "5. 悬臂自锁与端部刚性锁定: 延伸轨内端3.5°偏心自锁凸台切入锁紧卡口抵消1米弯矩；外端垂直刚性拉杆锁定上下滑轨杜绝扭转形变。",
        "6. 导轨重载自洁除尘防气阻: 倒V型EPDM橡胶罩阻隔95%落灰；槽底每隔200mm等间距开设Φ12mm垂直排灰导流圆孔，配尼龙雨刮毛刷条。",
        "7. AI多模态闭环主动避光: 蜗轮蜗杆自锁电机驱动垂直-15°~+15°俯仰倾斜 + 大屏外置偏光膜(0°~90°伺服无级旋转) + 免布线BLE Mesh照度终端。"
    ]
    sy = TAB_Y2 - 90.0
    for s in specs:
        draw_text(ms, s, TAB_X1 + 20.0, sy, 18.0, "09_TEXT_技术说明", 7)
        sy -= 42.0

    # 标题栏
    TB_X1, TB_X2 = 1450.0, 6600.0
    TB_Y1, TB_Y2 = -180.0, 320.0
    draw_rect(ms, TB_X1, TB_Y1, TB_X2, TB_Y2, "01_FRAME_外框型材", 8)
    draw_line(ms, TB_X1, TB_Y2 - 70.0, TB_X2, TB_Y2 - 70.0, "01_FRAME_外框型材", 8)
    draw_line(ms, TB_X1, TB_Y1 + 85.0, TB_X2, TB_Y1 + 85.0, "01_FRAME_外框型材", 8)
    draw_line(ms, TB_X1 + 1050.0, TB_Y1, TB_X1 + 1050.0, TB_Y2, "01_FRAME_外框型材", 8)
    draw_line(ms, TB_X1 + 2650.0, TB_Y1, TB_X1 + 2650.0, TB_Y2, "01_FRAME_外框型材", 8)
    draw_line(ms, TB_X1 + 3850.0, TB_Y1, TB_X1 + 3850.0, TB_Y2, "01_FRAME_外框型材", 8)

    draw_text(ms, "系统代号: GH-Z-2026", TB_X1 + 30.0, TB_Y2 - 48.0, 26.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "图纸名称: 第三代多维叠合全覆盖与自洁侧滑黑板工程总装图", TB_X1 + 1080.0, TB_Y2 - 48.0, 26.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "图号: GH-GEN3-ASM-01", TB_X1 + 3880.0, TB_Y2 - 48.0, 26.0, "09_TEXT_技术说明", 7)

    draw_text(ms, "设计阶段: 第三代(Z系列)终极实施例工程图", TB_X1 + 30.0, TB_Y2 - 125.0, 18.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "设计制图: czx & 海鸥 (Antigravity)", TB_X1 + 1080.0, TB_Y2 - 125.0, 18.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "比例: 1:1 (标准机械毫米制)", TB_X1 + 2680.0, TB_Y2 - 125.0, 18.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "出图规范: 0 Hatch 纯工程机械线框", TB_X1 + 3880.0, TB_Y2 - 125.0, 18.0, "09_TEXT_技术说明", 7)

    draw_text(ms, "审核结论: 第 10 轮全系统工程审核·参数完全吻合通过", TB_X1 + 30.0, TB_Y1 + 30.0, 18.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "适用标准: GB/T 28231-2011 / JY/T 0148-2011 教学黑板标准", TB_X1 + 1080.0, TB_Y1 + 30.0, 18.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "状态: 生产试制与专利附图工程终结版", TB_X1 + 3880.0, TB_Y1 + 30.0, 18.0, "09_TEXT_技术说明", 7)

    acad.ZoomExtents()
    print(">>> 成功执行 ZoomExtents 视图居中")

    target_dwg = r"D:\Desktop\pjhb\01-CAD工程图纸\第三代多维叠合翻转全覆盖与三维自洁侧滑黑板系统_全系统工程总装与运动机构图_v1.0.dwg"
    if os.path.exists(target_dwg):
        try:
            os.remove(target_dwg)
        except:
            pass

    doc.SaveAs(target_dwg)
    print(f">>> 成功保存第三代工程图纸: {target_dwg}")

if __name__ == "__main__":
    run_gen3_drafting()
