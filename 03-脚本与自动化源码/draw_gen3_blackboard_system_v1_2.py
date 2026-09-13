# -*- coding: utf-8 -*-
r"""
第三代多维叠合翻转全覆盖与三维自洁侧滑智能教学黑板系统 - AutoCAD 2026 自动化工程总装绘图脚本 (v1.2 对角线双铰链拓扑版)
文件版本: v1.2
核心特性:
1. 0 Hatch 纯工程机械线框制图；
2. 主视图青色翻转主铰链、快拆母座与俯仰马达设置在外侧黑板边缘 (x=±2000，工况三外滑至 x=±3000)；
3. 主视图品红色折叠铺开铰链设于靠近大屏内侧 (x=±1000)；
4. 右侧详图 A-A 全新构建【双层黑板对角线双铰链拓扑俯视图 (Top View)】：
   - 里面的外侧为翻转主铰链，外面的内侧为折叠铺开铰链，空间成对角线分布；
   - 展现 180° 铺平展开封屏状态与水平避光旋转状态；
5. 工况三外露滑槽中双横梁高刚性伸缩套杆、排灰孔、倒V型防护罩与端部闭环拉杆全要素呈现；
6. 递进式机械尺寸链与零干涉引线排版；
7. 输出: D:\Desktop\pjhb-CAD工程图纸\第三代多维叠合翻转全覆盖与三维自洁侧滑黑板系统_全系统工程总装与运动机构图_v1.2.dwg
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
    doc = None
    try:
        if acad.Documents.Count > 0:
            doc = acad.ActiveDocument
    except Exception:
        pass
    if doc is None:
        try:
            doc = acad.Documents.Add()
            time.sleep(1.0)
        except Exception:
            try:
                doc = acad.Documents.Add("")
                time.sleep(1.0)
            except Exception:
                pass
    for _ in range(10):
        try:
            if doc is not None:
                _ = doc.ModelSpace
                return acad, doc
        except Exception:
            try:
                doc = acad.ActiveDocument
            except Exception:
                pass
        time.sleep(0.5)
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
        ("05_INNER_HINGE_内缘铰链", 6), # 品红 (外面的内侧：多维铺开铰链)
        ("06_EXT_RAIL_延伸构件", 1),    # 红色 (嵌套延伸轨、自锁凸台、伸缩套杆、端部拉杆)
        ("07_PITCH_YAW_运动副", 4),     # 青色 (里面的外侧：翻转主铰链、快拆母座、俯仰马达)
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
    p1 = array.array('d', [float(x1), float(y1), 0.0])
    p2 = array.array('d', [float(x2), float(y2), 0.0])
    var_p1 = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, p1)
    var_p2 = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, p2)
    line = ms.AddLine(var_p1, var_p2)
    if layer:
        line.Layer = layer
    if color is not None:
        line.Color = color
    return line

def draw_circle(ms, cx, cy, r, layer=None, color=None):
    cp = array.array('d', [float(cx), float(cy), 0.0])
    var_cp = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, cp)
    c = ms.AddCircle(var_cp, float(r))
    if layer:
        c.Layer = layer
    if color is not None:
        c.Color = color
    return c

def draw_text(ms, text, x, y, h=18.0, layer="09_TEXT_技术说明", color=None):
    ip = array.array('d', [float(x), float(y), 0.0])
    var_ip = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, ip)
    t = ms.AddText(text, var_ip, float(h))
    t.StyleName = "STYLE_GB_CN"
    if layer:
        t.Layer = layer
    if color is not None:
        t.Color = color
    return t

def draw_dim_horiz(ms, x1, y1, x2, y2, offset=80.0, text_override="", layer="08_DIMS_尺寸标注"):
    p1 = array.array('d', [float(x1), float(y1), 0.0])
    p2 = array.array('d', [float(x2), float(y2), 0.0])
    y_dim = max(y1, y2) + offset
    p_line = array.array('d', [(float(x1) + float(x2)) / 2.0, float(y_dim), 0.0])
    var_p1 = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, p1)
    var_p2 = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, p2)
    var_pline = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, p_line)
    dim = ms.AddDimAligned(var_p1, var_p2, var_pline)
    dim.Layer = layer
    dim.TextStyle = "STYLE_GB_CN"
    dim.ArrowheadSize = 14.0
    dim.TextHeight = 16.0
    if text_override:
        dim.TextOverride = text_override
    return dim

def draw_lead_line(ms, x1, y1, x2, y2, x3, text, h=16.0, layer="09_TEXT_技术说明", color=None):
    draw_line(ms, x1, y1, x2, y2, layer, color)
    draw_line(ms, x2, y2, x3, y2, layer, color)
    tx = x3 + 10.0 if x3 >= x2 else x3 - len(text) * h * 0.9 - 10.0
    draw_text(ms, text, tx, y2 - h * 0.4, h, layer, color)

def run_gen3_drafting():
    print(">>> 启动 AutoCAD 2026 第三代工程图 v1.2 自动化出图链路...")
    acad, doc = get_acad_doc()
    ms = doc.ModelSpace
    setup_chinese_style(doc)
    create_layers(doc)

    # 1. 标题与状态说明
    draw_text(ms, "第三代工况一：初始闭合，市面主流全覆盖封屏形态 [COVERED - 传统主流全封闭 4000mm]", -3200.0, 5020.0, 26.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "技术特征: 左右黑板各二分层；外层板绕靠近大屏的内侧铰链向内平铺180°并对缝合拢，100%遮蔽86寸大屏；里面的外侧为翻转承重铰链与快拆母座。", -3200.0, 4970.0, 16.0, "09_TEXT_技术说明", 7)

    draw_text(ms, "第三代工况二：常态多媒体，大屏幕显双层叠合形态 [COMPACT - 黄金视域 4000mm]", -3200.0, 3220.0, 26.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "技术特征: 内侧铺开铰链回折180°，两层黑板紧密贴合(总厚度仅26mm)；86寸多媒体屏幕完全显露，里面的外侧为翻转承重铰链，外面的内侧为折叠铰链。", -3200.0, 3170.0, 16.0, "09_TEXT_技术说明", 7)

    draw_text(ms, "第三代工况三：大视野与三维空间避光极限展开形态 [DEPLOYED - 盲区归零 6000mm]", -3200.0, 1420.0, 26.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "技术特征: 双横梁延伸滑轨使双层黑板各向外滑移1000mm；高刚性不锈钢伸缩套杆承托；外展黑板可绕外侧翻转母座做水平偏航及纵向避光俯仰。", -3200.0, 1370.0, 16.0, "09_TEXT_技术说明", 7)

    # 2. 工况一 (Y: 3700 ~ 4900)
    top_y1, bot_y1, CY1 = 4900.0, 3700.0, 4300.0
    draw_rect(ms, -2030.0, bot_y1 - 30.0, 2030.0, top_y1 + 30.0, "01_FRAME_外框型材", 8)
    draw_rect(ms, -1000.0, bot_y1 + 20.0, 1000.0, top_y1 - 20.0, "02_SCREEN_多媒体屏", 5)
    draw_text(ms, "[86寸多媒体大屏被100%封闭在背后保护防撞]", -450.0, CY1, 20.0, "02_SCREEN_多媒体屏", 5)

    # 铺开折叠板 (品红内侧铰链，向中心铺开封屏)
    draw_rect(ms, -1000.0, bot_y1 + 10.0, 0.0, top_y1 - 10.0, "04_INNER_BOARD_内附板", 2)
    draw_rect(ms, 0.0, bot_y1 + 10.0, 1000.0, top_y1 - 10.0, "04_INNER_BOARD_内附板", 2)
    draw_rect(ms, -2000.0, bot_y1 + 10.0, -1000.0, top_y1 - 10.0, "03_OUTER_BOARD_外主板", 3)
    draw_rect(ms, 1000.0, bot_y1 + 10.0, 2000.0, top_y1 - 10.0, "03_OUTER_BOARD_外主板", 3)

    # 翻转铰链与快拆母座 (青色，位于里面的外侧 x = ±2000)
    for hx in [-2000.0, 2000.0]:
        for hy in [top_y1 - 150.0, bot_y1 + 150.0]:
            draw_circle(ms, hx, hy, 20.0, "07_PITCH_YAW_运动副", 4)
            draw_circle(ms, hx, hy, 8.0, "07_PITCH_YAW_运动副", 4)
            draw_rect(ms, hx - 22.0, hy - 45.0, hx + 22.0, hy + 45.0, "07_PITCH_YAW_运动副", 4)
    draw_lead_line(ms, -2000.0, CY1, -2250.0, CY1 + 100.0, -2500.0, "里面的外侧: 翻转主铰链与快拆母座(承重/水平翻转/俯仰避光)", 18.0)

    # 折叠铰链 (品红色，位于外面的内侧 x = ±1000)
    for hx in [-1000.0, 1000.0]:
        for hy in [top_y1 - 220.0, bot_y1 + 220.0]:
            draw_circle(ms, hx, hy, 18.0, "05_INNER_HINGE_内缘铰链", 6)
            draw_circle(ms, hx, hy, 8.0, "05_INNER_HINGE_内缘铰链", 6)
    draw_lead_line(ms, -1000.0, CY1 + 180.0, -1250.0, CY1 + 280.0, -1450.0, "外面的内侧: 折叠铺开铰链(向内铺展180°封屏)", 18.0)

    # 中央暗扣
    draw_rect(ms, -12.0, CY1 - 80.0, 12.0, CY1 + 80.0, "01_FRAME_外框型材", 8)
    draw_lead_line(ms, 0.0, CY1, 350.0, CY1 - 100.0, 550.0, "中央缝隙式暗扣机械对接锁紧(全覆盖平整拼接)", 18.0)

    # 尺寸链 (工况一)
    draw_dim_horiz(ms, -2000.0, top_y1, -1000.0, top_y1, 80.0, "1000 [内层主板]")
    draw_dim_horiz(ms, -1000.0, top_y1, 0.0, top_y1, 80.0, "1000 [铺开折叠板A]")
    draw_dim_horiz(ms, 0.0, top_y1, 1000.0, top_y1, 80.0, "1000 [铺开折叠板B]")
    draw_dim_horiz(ms, 1000.0, top_y1, 2000.0, top_y1, 80.0, "1000 [内层主板]")
    draw_dim_horiz(ms, -1000.0, top_y1, 1000.0, top_y1, 150.0, "2000 [全覆盖完全遮蔽大屏跨度]")
    draw_dim_horiz(ms, -2000.0, top_y1, 2000.0, top_y1, 220.0, "4000 [主流全覆盖总板面长]")

    # 3. 工况二 (Y: 1900 ~ 3100)
    top_y2, bot_y2, CY2 = 3100.0, 1900.0, 2500.0
    draw_rect(ms, -2030.0, bot_y2 - 30.0, 2030.0, top_y2 + 30.0, "01_FRAME_外框型材", 8)
    draw_rect(ms, -1000.0, bot_y2 + 20.0, 1000.0, top_y2 - 20.0, "02_SCREEN_多媒体屏", 5)
    draw_text(ms, "86寸超清多媒体教学触摸大屏 (2000x1200mm, 偏光膜避光)", -600.0, CY2, 20.0, "02_SCREEN_多媒体屏", 5)

    # 双层叠合黑板
    draw_rect(ms, -2000.0, bot_y2 + 10.0, -1000.0, top_y2 - 10.0, "03_OUTER_BOARD_外主板", 3)
    draw_rect(ms, -1990.0, bot_y2 + 18.0, -1010.0, top_y2 - 18.0, "04_INNER_BOARD_内附板", 2)
    draw_rect(ms, 1000.0, bot_y2 + 10.0, 2000.0, top_y2 - 10.0, "03_OUTER_BOARD_外主板", 3)
    draw_rect(ms, 1010.0, bot_y2 + 18.0, 1990.0, top_y2 - 18.0, "04_INNER_BOARD_内附板", 2)

    # 翻转铰链 (青色，位于里面的外侧 x = ±2000)
    for hx in [-2000.0, 2000.0]:
        for hy in [top_y2 - 150.0, bot_y2 + 150.0]:
            draw_circle(ms, hx, hy, 20.0, "07_PITCH_YAW_运动副", 4)
            draw_circle(ms, hx, hy, 8.0, "07_PITCH_YAW_运动副", 4)
            draw_rect(ms, hx - 22.0, hy - 45.0, hx + 22.0, hy + 45.0, "07_PITCH_YAW_运动副", 4)
    draw_lead_line(ms, -2000.0, CY2, -2250.0, CY2, -2450.0, "里面的外侧: 标准化快拆母座与俯仰马达", 18.0)
    draw_lead_line(ms, 2000.0, CY2, 2250.0, CY2, 2450.0, "里面的外侧: 翻转主铰链(支持全模块水平偏航避光翻转)", 18.0)

    # 折叠铰链 (品红色，位于外面的内侧 x = ±1000)
    for hx in [-1000.0, 1000.0]:
        for hy in [top_y2 - 220.0, bot_y2 + 220.0]:
            draw_circle(ms, hx, hy, 18.0, "05_INNER_HINGE_内缘铰链", 6)
            draw_circle(ms, hx, hy, 8.0, "05_INNER_HINGE_内缘铰链", 6)
    draw_lead_line(ms, -1000.0, CY2 + 160.0, -780.0, CY2 + 240.0, -580.0, "外面的内侧: 折叠铰链(回折180°紧密贴合)", 18.0)

    draw_text(ms, "双层附加叠合黑板面", -1700.0, CY2 + 20.0, 18.0, "03_OUTER_BOARD_外主板", 3)
    draw_text(ms, "(内层主板12mm + 外层折叠板12mm 紧密贴合)", -1850.0, CY2 - 30.0, 15.0, "04_INNER_BOARD_内附板", 2)

    # 尺寸链 (工况二)
    draw_dim_horiz(ms, -2000.0, top_y2, -1000.0, top_y2, 80.0, "1000 [双层叠合黑板]")
    draw_dim_horiz(ms, -1000.0, top_y2, 1000.0, top_y2, 80.0, "2000 [86寸多媒体大屏]")
    draw_dim_horiz(ms, 1000.0, top_y2, 2000.0, top_y2, 80.0, "1000 [双层叠合黑板]")
    draw_dim_horiz(ms, -2000.0, top_y2, 2000.0, top_y2, 150.0, "4000 [常态多媒体教学总跨度]")

    # 4. 工况三 (Y: 100 ~ 1300)
    top_y3, bot_y3, CY3 = 1300.0, 100.0, 700.0
    draw_rect(ms, -3030.0, bot_y3 - 30.0, 3030.0, top_y3 + 30.0, "01_FRAME_外框型材", 8)
    draw_rect(ms, -1000.0, bot_y3 + 20.0, 1000.0, top_y3 - 20.0, "02_SCREEN_多媒体屏", 5)
    draw_text(ms, "86寸大屏完全露显 (支持双侧书写与板书互投联动)", -550.0, CY3, 20.0, "02_SCREEN_多媒体屏", 5)

    # 外露滑槽与高刚性双梁伸缩套杆 (x: -2000~-1000, 1000~2000)
    for x_s, x_e in [(-2000.0, -1000.0), (1000.0, 2000.0)]:
        # 伸缩内套杆
        draw_rect(ms, x_s, top_y3 - 42.0, x_e, top_y3 - 22.0, "06_EXT_RAIL_延伸构件", 1)
        draw_rect(ms, x_s, bot_y3 + 22.0, x_e, bot_y3 + 42.0, "06_EXT_RAIL_延伸构件", 1)
        # 倒V型防护罩
        draw_line(ms, x_s, top_y3 - 10.0, x_e, top_y3 - 10.0, "05_INNER_HINGE_内缘铰链", 6)
        # 排灰圆孔
        step = 200.0
        n_holes = int((x_e - x_s) / step)
        for i in range(1, n_holes):
            hx = x_s + i * step
            draw_circle(ms, hx, bot_y3 + 8.0, 8.0, "05_INNER_HINGE_内缘铰链", 6)

    # 外展黑板模块 (x: -3000~-2000, 2000~3000)
    draw_rect(ms, -3000.0, bot_y3 + 10.0, -2000.0, top_y3 - 10.0, "03_OUTER_BOARD_外主板", 3)
    draw_rect(ms, -2990.0, bot_y3 + 18.0, -2010.0, top_y3 - 18.0, "04_INNER_BOARD_内附板", 2)
    draw_rect(ms, 2000.0, bot_y3 + 10.0, 3000.0, top_y3 - 10.0, "03_OUTER_BOARD_外主板", 3)
    draw_rect(ms, 2010.0, bot_y3 + 18.0, 2990.0, top_y3 - 18.0, "04_INNER_BOARD_内附板", 2)

    # 翻转铰链随黑板外移至外侧 (x = ±3000)
    for hx in [-3000.0, 3000.0]:
        for hy in [top_y3 - 150.0, bot_y3 + 150.0]:
            draw_circle(ms, hx, hy, 20.0, "07_PITCH_YAW_运动副", 4)
            draw_circle(ms, hx, hy, 8.0, "07_PITCH_YAW_运动副", 4)
            draw_rect(ms, hx - 22.0, hy - 45.0, hx + 22.0, hy + 45.0, "07_PITCH_YAW_运动副", 4)

    # 端部刚性垂直拉杆 (x = ±3018)
    draw_rect(ms, -3025.0, bot_y3 - 25.0, -3010.0, top_y3 + 25.0, "06_EXT_RAIL_延伸构件", 1)
    draw_rect(ms, 3010.0, bot_y3 - 25.0, 3025.0, top_y3 + 25.0, "06_EXT_RAIL_延伸构件", 1)
    draw_lead_line(ms, -3018.0, CY3 + 150.0, -3160.0, CY3 + 240.0, -3320.0, "端部刚性垂直拉杆(闭环锁紧)", 18.0)
    draw_lead_line(ms, 3018.0, CY3 + 150.0, 3180.0, CY3 + 240.0, 3350.0, "刚性垂直端部拉杆(双端机械闭环锁定上下滑轨)", 18.0)

    # 偏心消隙卡口
    draw_lead_line(ms, 1980.0, top_y3 - 35.0, 1820.0, CY3 + 160.0, 1150.0, "偏心楔形自锁防下垂凸台与锁紧卡口(3.5°斜面消隙)", 18.0)
    draw_lead_line(ms, -1500.0, top_y3 - 32.0, -1500.0, CY3 + 120.0, -1950.0, "横向双横梁高刚性不锈钢伸缩套杆(Φ28x2.5mm,承托1.0m滑移悬臂)", 18.0)
    draw_lead_line(ms, 1500.0, bot_y3 + 32.0, 1500.0, CY3 - 100.0, 1080.0, "C型槽底垂直排灰孔(Φ12mm,等间距200mm,消气阻)", 18.0)

    # 尺寸链 (工况三)
    draw_dim_horiz(ms, -3000.0, top_y3, -2000.0, top_y3, 80.0, "1000 [外展叠合黑板]")
    draw_dim_horiz(ms, -2000.0, top_y3, -1000.0, top_y3, 80.0, "1000 [伸缩套杆与外露滑槽]")
    draw_dim_horiz(ms, -1000.0, top_y3, 1000.0, top_y3, 80.0, "2000 [86寸多媒体大屏]")
    draw_dim_horiz(ms, 1000.0, top_y3, 2000.0, top_y3, 80.0, "1000 [伸缩套杆与外露滑槽]")
    draw_dim_horiz(ms, 2000.0, top_y3, 3000.0, top_y3, 80.0, "1000 [外展叠合黑板]")
    draw_dim_horiz(ms, -3000.0, top_y3, 3000.0, top_y3, 160.0, "6000 [侧滑平移推拉展开极限总跨度]")

    # =========================================================================
    # 模块四：右侧专业详图
    # 【核心新增】俯视详图 A-A：双层黑板模块对角线双铰链拓扑原理 (Top View)
    # =========================================================================
    draw_text(ms, "【俯视机构详图 A-A】双层叠合黑板模块对角线双铰链拓扑原理 (Top View)", 3550.0, 5140.0, 26.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "机构核心: 里面板的外侧设翻转主铰链，外面板的内侧设折叠铺开铰链，空间成对角线正交排布，两组运动副完全解耦零干涉。", 3550.0, 5090.0, 16.0, "09_TEXT_技术说明", 7)

    # 1. 墙面与导轨型材
    wall_y = 5000.0
    draw_line(ms, 3400.0, wall_y, 6500.0, wall_y, "01_FRAME_外框型材", 8)
    draw_text(ms, "【建筑承重墙体基准面 (Wall Datum)】", 3450.0, wall_y + 35.0, 16.0, "01_FRAME_外框型材", 8)
    draw_rect(ms, 3400.0, wall_y - 40.0, 6500.0, wall_y - 12.0, "01_FRAME_外框型材", 8)
    draw_text(ms, "双滑槽重载铝合金上导轨型材 (含自洁排灰槽与缓冲限位块)", 5300.0, wall_y - 32.0, 16.0, "01_FRAME_外框型材", 8)

    # 2. 86寸大屏框体截面
    screen_x1, screen_x2 = 3380.0, 4380.0
    screen_y_top = wall_y - 65.0
    screen_y_bot = screen_y_top - 70.0
    draw_rect(ms, screen_x1, screen_y_bot, screen_x2, screen_y_top, "02_SCREEN_多媒体屏", 5)
    draw_text(ms, "86寸多媒体大屏框体截面 (厚70mm, 挂墙安装于基准面)", screen_x1 + 60.0, screen_y_bot + 24.0, 16.0, "02_SCREEN_多媒体屏", 5)

    # 3. 双层贴合黑板模块
    b_len = 1000.0
    th = 24.0
    x_inner = 4440.0
    x_outer = x_inner + b_len  # 5440.0
    y_wall_b = screen_y_bot - 45.0  # 4820.0
    y_front_b = y_wall_b - 175.0   # 4645.0

    # 里面的主板 (绿色)
    draw_rect(ms, x_inner, y_wall_b - th/2.0, x_outer, y_wall_b + th/2.0, "03_OUTER_BOARD_外主板", 3)
    draw_text(ms, "【里面的主板】厚12mm·挂载于滑块与外侧翻转母座", x_inner + 40.0, y_wall_b + 20.0, 16.0, "03_OUTER_BOARD_外主板", 3)

    # 外面的折叠板 (黄色)
    draw_rect(ms, x_inner, y_front_b - th/2.0, x_outer, y_front_b + th/2.0, "04_INNER_BOARD_内附板", 2)
    draw_text(ms, "【外面的折叠板】厚12mm·具有正反双面书写板·平时贴合", x_inner + 40.0, y_front_b - 32.0, 16.0, "04_INNER_BOARD_内附板", 2)

    # 4. 关键铰链 1: 里面的外侧 -> 翻转主铰链 (青色 x=5440, y=4820)
    h_outer_x = x_outer
    h_outer_y = y_wall_b
    draw_circle(ms, h_outer_x, h_outer_y, 24.0, "07_PITCH_YAW_运动副", 4)
    draw_circle(ms, h_outer_x, h_outer_y, 10.0, "07_PITCH_YAW_运动副", 4)
    draw_rect(ms, h_outer_x - 14.0, h_outer_y - 28.0, h_outer_x + 36.0, h_outer_y + 28.0, "07_PITCH_YAW_运动副", 4)
    draw_rect(ms, h_outer_x - 16.0, h_outer_y + 28.0, h_outer_x + 28.0, wall_y - 40.0, "01_FRAME_外框型材", 8)
    draw_text(ms, "重载导向滑块", h_outer_x - 18.0, wall_y - 58.0, 16.0, "01_FRAME_外框型材", 8)
    draw_lead_line(ms, h_outer_x + 12.0, h_outer_y + 15.0, h_outer_x + 90.0, h_outer_y + 70.0, h_outer_x + 210.0, "①【里面的外侧】: 翻转主铰链 (承重转轴/快拆母座/偏航转动及俯仰)", 18.0)

    # 5. 关键铰链 2: 外面的内侧 -> 折叠铰链 (品红色 x=4440, y=4645)
    h_inner_x = x_inner
    h_inner_y = y_front_b
    draw_circle(ms, h_inner_x, h_inner_y, 22.0, "05_INNER_HINGE_内缘铰链", 6)
    draw_circle(ms, h_inner_x, h_inner_y, 9.0, "05_INNER_HINGE_内缘铰链", 6)
    draw_rect(ms, h_inner_x - 36.0, h_inner_y - 26.0, h_inner_x + 14.0, h_inner_y + 26.0, "05_INNER_HINGE_内缘铰链", 6)
    draw_lead_line(ms, h_inner_x - 12.0, h_inner_y - 15.0, h_inner_x - 80.0, h_inner_y - 65.0, h_inner_x - 200.0, "②【外面的内侧】: 多维折叠铺开铰链 (向中心铺开180°封屏)", 18.0)

    # 6. 对角线拓扑虚线
    draw_line(ms, h_inner_x, h_inner_y, h_outer_x, h_outer_y, "07_PITCH_YAW_运动副", 4)
    mid_diag_x = (h_inner_x + h_outer_x) / 2.0
    mid_diag_y = (h_inner_y + h_outer_y) / 2.0
    draw_circle(ms, mid_diag_x, mid_diag_y, 14.0, "07_PITCH_YAW_运动副", 4)
    draw_lead_line(ms, mid_diag_x, mid_diag_y, mid_diag_x + 80.0, 4520.0, mid_diag_x + 220.0, "★ 成对角线分布 (Diagonal Topology): 内侧折叠轴与外侧翻转轴正交解耦，机构零干涉 ★", 18.0)

    # 7. 铺开封屏展开态 (向左 180° 翻折覆盖大屏)
    unfold_x1 = h_inner_x - b_len
    unfold_x2 = h_inner_x
    draw_rect(ms, unfold_x1, y_front_b - th/2.0, unfold_x2, y_front_b + th/2.0, "05_INNER_HINGE_内缘铰链", 6)
    draw_text(ms, "【180°铺开展平封屏状态】紧密遮蔽86寸多媒体大屏", unfold_x1 + 100.0, y_front_b - 10.0, 16.0, "05_INNER_HINGE_内缘铰链", 6)
    draw_text(ms, "180°铺发展平轨迹", h_inner_x - 140.0, y_front_b + 80.0, 16.0, "05_INNER_HINGE_内缘铰链", 6)

    # 8. 水平偏航旋转避光态虚线
    yaw_rad = math.radians(20.0)
    yaw_end_x = h_outer_x - b_len * math.cos(yaw_rad)
    yaw_end_y = h_outer_y - b_len * math.sin(yaw_rad)
    draw_line(ms, h_outer_x, h_outer_y, yaw_end_x, yaw_end_y, "07_PITCH_YAW_运动副", 4)
    draw_text(ms, "整机水平偏航避光旋转态 (绕外侧主铰链转动)", yaw_end_x + 60.0, yaw_end_y - 25.0, 16.0, "07_PITCH_YAW_运动副", 4)
    draw_text(ms, "水平避光回转轨迹", h_outer_x - 190.0, h_outer_y - 55.0, 16.0, "07_PITCH_YAW_运动副", 4)

    # 4.2 剖面 B-B: 纵向俯仰避光原理
    PX2 = 4300.0
    draw_text(ms, "【剖面视图 B-B】纵向俯仰避光与光锥折射原理 (-15°~+15°)", PX2 - 320.0, top_y2 + 450.0, 26.0, "09_TEXT_技术说明", 7)
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

    # 4.3 节点详图 C-C: 自洁排灰导轨与伸缩套杆
    DX = 5600.0
    draw_text(ms, "【节点详图 C-C】自洁排灰导轨与伸缩套杆/防下垂截面", DX - 380.0, top_y3 + 450.0, 26.0, "09_TEXT_技术说明", 7)
    draw_rect(ms, DX - 160.0, CY3 - 110.0, DX + 160.0, CY3 + 110.0, "01_FRAME_外框型材", 8)
    draw_rect(ms, DX - 120.0, CY3 - 65.0, DX + 120.0, CY3 + 65.0, "01_FRAME_外框型材", 1)
    draw_circle(ms, DX, CY3, 35.0, "06_EXT_RAIL_延伸构件", 1)
    draw_circle(ms, DX, CY3, 25.0, "06_EXT_RAIL_延伸构件", 1)
    draw_lead_line(ms, DX, CY3 + 35.0, DX + 90.0, CY3 + 90.0, DX + 200.0, "SUS304伸缩套杆(Φ28x2.5mm)", 18.0)

    draw_line(ms, DX - 180.0, CY3 + 110.0, DX, CY3 + 200.0, "05_INNER_HINGE_内缘铰链", 6)
    draw_line(ms, DX, CY3 + 200.0, DX + 180.0, CY3 + 110.0, "05_INNER_HINGE_内缘铰链", 6)
    draw_lead_line(ms, DX, CY3 + 200.0, DX + 100.0, CY3 + 260.0, DX + 220.0, "倒V型EPDM弹性橡胶防护罩", 18.0)
    draw_circle(ms, DX, CY3 - 88.0, 16.0, "05_INNER_HINGE_内缘铰链", 6)
    draw_lead_line(ms, DX + 18.0, CY3 - 88.0, DX + 120.0, CY3 - 110.0, DX + 240.0, "垂直贯穿排灰孔(Φ12mm,等距200mm)", 18.0)

    # =========================================================================
    # 参数表与标题栏
    # =========================================================================
    TAB_X1, TAB_X2 = -3200.0, 1300.0
    TAB_Y1, TAB_Y2 = -180.0, 320.0
    draw_rect(ms, TAB_X1, TAB_Y1, TAB_X2, TAB_Y2, "01_FRAME_外框型材", 8)
    draw_line(ms, TAB_X1, TAB_Y2 - 55.0, TAB_X2, TAB_Y2 - 55.0, "01_FRAME_外框型材", 8)
    draw_text(ms, "【第三代多维叠合全覆盖与三维自洁侧滑避光黑板系统 - 核心工程参数矩阵】", TAB_X1 + 25.0, TAB_Y2 - 40.0, 26.0, "09_TEXT_技术说明", 7)

    specs = [
        "1. 对角线双铰链架构: 里面板的外侧设翻转主铰链/快拆母座，外面板的内侧设折叠铺开铰链，成空间对角线拓扑，运动副互不干涉。",
        "2. 内缘铰链铺开封屏自由度: 位于外面的内侧竖边，回转角0°~180°；闭合时向中心完全铺开展平合拢，100%遮蔽大屏，恢复主流全覆盖板书形态。",
        "3. 外侧承重翻转与快拆升级: 位于里面的外侧竖边，快拆母座标准化拔插升级；支承整机水平偏航转动及-15°~+15°纵向避光俯仰。",
        "4. 大行程侧滑推拉展开: 叠合黑板沿双横梁自洁延伸轨外滑1000mm，总幅宽展开至6000mm，彻底消除86寸大屏两侧物理盲区与视线死角。",
        "5. 高刚性双梁伸缩套杆承托: 采用Φ28x2.5mm SUS304不锈钢高刚性伸缩套杆，内端3.5°偏心自锁凸台消隙；外端刚性垂直拉杆闭环锁定上下滑轨。",
        "6. 导轨重载自洁除尘防气阻: 倒V型EPDM橡胶罩阻隔95%落灰；槽底每隔200mm等间距开设Φ12mm垂直排灰导流圆孔，配尼龙雨刮毛刷条。",
        "7. AI多模态闭环主动避光: 蜗轮蜗杆自锁电机驱动垂直-15°~+15°俯仰倾斜 + 大屏外置偏光膜(0°~90°伺服无级旋转) + 免布线BLE Mesh照度终端。"
    ]
    sy = TAB_Y2 - 90.0
    for s in specs:
        draw_text(ms, s, TAB_X1 + 20.0, sy, 18.0, "09_TEXT_技术说明", 7)
        sy -= 42.0

    TB_X1, TB_X2 = 1450.0, 6600.0
    TB_Y1, TB_Y2 = -180.0, 320.0
    draw_rect(ms, TB_X1, TB_Y1, TB_X2, TB_Y2, "01_FRAME_外框型材", 8)
    draw_line(ms, TB_X1, TB_Y2 - 70.0, TB_X2, TB_Y2 - 70.0, "01_FRAME_外框型材", 8)
    draw_line(ms, TB_X1, TB_Y1 + 85.0, TB_X2, TB_Y1 + 85.0, "01_FRAME_外框型材", 8)
    draw_line(ms, TB_X1 + 1050.0, TB_Y1, TB_X1 + 1050.0, TB_Y2, "01_FRAME_外框型材", 8)
    draw_line(ms, TB_X1 + 2650.0, TB_Y1, TB_X1 + 2650.0, TB_Y2, "01_FRAME_外框型材", 8)
    draw_line(ms, TB_X1 + 3800.0, TB_Y1, TB_X1 + 3800.0, TB_Y2, "01_FRAME_外框型材", 8)

    draw_text(ms, "系统代号：GH-Z-2026", TB_X1 + 30.0, TB_Y2 - 45.0, 24.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "设计阶段：第三代 (Z系列) 终极实施例工程图 v1.2", TB_X1 + 30.0, TB_Y1 + 110.0, 18.0, "09_TEXT_技术说明", 7)

    draw_text(ms, "图纸名称：第三代多维叠合全覆盖与自洁侧滑黑板工程总装图", TB_X1 + 1080.0, TB_Y2 - 45.0, 24.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "设计/制图：czx & 海鸥 (Antigravity)", TB_X1 + 1080.0, TB_Y1 + 110.0, 18.0, "09_TEXT_技术说明", 7)

    draw_text(ms, "比例：1:1 (标准机械毫米制)", TB_X1 + 2680.0, TB_Y2 - 45.0, 24.0, "09_TEXT_技术说明", 7)

    draw_text(ms, "图号：GH-GEN3-ASM-03", TB_X1 + 3830.0, TB_Y2 - 45.0, 24.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "出图规范：0 Hatch 纯工程机械线框", TB_X1 + 3830.0, TB_Y1 + 110.0, 18.0, "09_TEXT_技术说明", 7)

    draw_text(ms, "审核结论：第 12 轮全系统工程复核·里面的外侧翻转铰链+外面的内侧折叠铰链(对角线拓扑俯视)闭环通过", TB_X1 + 30.0, TB_Y1 + 30.0, 18.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "通用标准：GB/T 28231-2011 / JY/T 0148-2011 教学黑板标准", TB_X1 + 1750.0, TB_Y1 + 30.0, 18.0, "09_TEXT_技术说明", 7)
    draw_text(ms, "状态：生产试制与专利附图工程终结稿", TB_X1 + 3830.0, TB_Y1 + 30.0, 18.0, "09_TEXT_技术说明", 7)

    draw_rect(ms, -3350.0, -280.0, 6720.0, 5350.0, "01_FRAME_外框型材", 8)
    draw_rect(ms, -3330.0, -260.0, 6700.0, 5330.0, "01_FRAME_外框型材", 8)

    # 居中显示全图
    try:
        acad.ZoomExtents()
    except:
        pass

    save_path = os.path.join(r"D:\Desktop\pjhb", "01-CAD工程图纸", "第三代多维叠合翻转全覆盖与三维自洁侧滑黑板系统_全系统工程总装与运动机构图_v1.2.dwg")
    print(f">>> 正在保存工程图纸至: {save_path} ...")
    doc.SaveAs(save_path)
    print(">>> [SUCCESS] 第三代工程总装与运动机构图 v1.2 绘制、居中并保存成功！")

if __name__ == '__main__':
    run_gen3_drafting()
