# -*- coding: utf-8 -*-
"""
第一代翻转式多媒体智能黑板系统 - AutoCAD 2026 自动化标准工程参数与尺寸标注绘图脚本 (v1.4 终极完美版)
文件版本: v1.4
"""

import sys
import os
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
        ("01_FRAME_外框导轨", 8),
        ("02_SCREEN_多媒体屏", 5),
        ("03_MAIN_BOARD_主黑板", 3),
        ("04_FOLD_BOARD_折展副板", 7),
        ("05_CANOPY_遮光雨棚", 4),
        ("06_HINGE_五金铰链", 2),
        ("07_DIMS_尺寸标注", 1),
        ("08_TEXT_技术说明", 7)
    ]
    for name, col in layers_info:
        try:
            lay = doc.Layers.Add(name)
            lay.Color = col
        except:
            pass
    print(">>> 8 大标准工程图层创建完毕")

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

def draw_text(ms, text, x, y, height, layer="08_TEXT_技术说明", color=None):
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

def draw_aligned_dim(ms, x1, y1, x2, y2, offset_dist, is_horizontal=True, override_text=None, layer="07_DIMS_尺寸标注"):
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

def draw_hinge(ms, cx, cy, layer="06_HINGE_五金铰链"):
    hx1, hx2 = cx - 40.0, cx + 40.0
    hy1, hy2 = cy - 35.0, cy + 35.0
    draw_rect(ms, hx1, hy1, hx2, hy2, layer, 2)
    draw_circle(ms, cx - 20.0, cy, 5.0, layer, 2)
    draw_circle(ms, cx + 20.0, cy, 5.0, layer, 2)
    draw_line(ms, cx - 20.0, cy - 20.0, cx + 20.0, cy - 20.0, layer, 2)
    draw_line(ms, cx - 20.0, cy + 20.0, cx + 20.0, cy + 20.0, layer, 2)

def draw_canopy_and_tray(ms, cx, top_y, bot_y, W_CANOPY=2120.0, H_CANOPY=90.0, H_TRAY=50.0):
    cx1, cx2 = cx - W_CANOPY / 2.0, cx + W_CANOPY / 2.0
    cy1 = top_y + 10.0
    cy2 = cy1 + H_CANOPY
    draw_rect(ms, cx1, cy1, cx2, cy2, "05_CANOPY_遮光雨棚", 4)
    draw_line(ms, cx1, cy1 + 30.0, cx2, cy1 + 30.0, "05_CANOPY_遮光雨棚", 4)
    draw_line(ms, cx1, cy1 + 60.0, cx2, cy1 + 60.0, "05_CANOPY_遮光雨棚", 4)
    for gx in range(int(cx1) + 120, int(cx2) - 120, 160):
        draw_line(ms, float(gx), cy1 + 68.0, float(gx) + 40.0, cy1 + 68.0, "05_CANOPY_遮光雨棚", 4)

    by2 = bot_y - 10.0
    by1 = by2 - H_TRAY
    draw_rect(ms, cx1, by1, cx2, by2, "01_FRAME_外框导轨", 8)
    draw_line(ms, cx1, by1 + 15.0, cx2, by1 + 15.0, "01_FRAME_外框导轨", 8)
    holes_x = [cx - 900.0, cx - 600.0, cx - 300.0, cx, cx + 300.0, cx + 600.0, cx + 900.0]
    for hx in holes_x:
        draw_circle(ms, hx, by1 + 25.0, 6.0, "01_FRAME_外框导轨", 7)
    return (cy2, by1)

def run_gen1_annotated_v1_4():
    print(">>> 启动 AutoCAD 2026 并初始化图纸...")
    acad, doc = get_acad_doc()
    ms = doc.ModelSpace
    setup_chinese_style(doc)
    create_layers(doc)

    W_SCREEN = 2000.0
    H_SCREEN = 1200.0
    W_LCD = 1900.0
    H_LCD = 1070.0
    W_CANOPY = 2120.0
    H_CANOPY = 90.0

    # =========================================================================
    # 工况一：多自由度折展外展避光状态 (Center Y = 1600.0)
    # =========================================================================
    CY1 = 1600.0
    top_y1 = CY1 + H_SCREEN / 2.0  # 2200
    bot_y1 = CY1 - H_SCREEN / 2.0  # 1000

    draw_text(ms, "第一代工况一：多自由度折展外展避光状态 [DEPLOYED - 展开极限跨度 6000mm]", -3000.0, top_y1 + 550.0, 48.0, "08_TEXT_技术说明", 7)
    draw_text(ms, "技术特征: 两侧副板经双节阻尼铰链 180° 外展平铺，整板跨度拓展至 6000mm (+50%)，消除两侧盲区；顶部雨棚 15° 挑檐物理切断吊灯反射眩光。", -3000.0, top_y1 + 480.0, 24.0, "08_TEXT_技术说明", 7)

    # 屏幕、雨棚、底槽
    draw_rect(ms, -1000.0, bot_y1, 1000.0, top_y1, "01_FRAME_外框导轨", 8)
    draw_rect(ms, -950.0, bot_y1 + 50.0, 950.0, bot_y1 + 50.0 + H_LCD, "02_SCREEN_多媒体屏", 5)
    draw_rect(ms, -940.0, bot_y1 + 60.0, 940.0, bot_y1 + 40.0 + H_LCD, "02_SCREEN_多媒体屏", 5)
    draw_rect(ms, -90.0, bot_y1 + 15.0, 90.0, bot_y1 + 35.0, "01_FRAME_外框导轨", 8)
    draw_circle(ms, 0.0, bot_y1 + 25.0, 4.5, "06_HINGE_五金铰链", 2)
    c_top1, t_bot1 = draw_canopy_and_tray(ms, 0.0, top_y1, bot_y1, W_CANOPY, H_CANOPY)

    # 左右主黑板 (1000x1200)
    draw_rect(ms, -2000.0, bot_y1, -1000.0, top_y1, "03_MAIN_BOARD_主黑板", 3)
    draw_rect(ms, -1980.0, bot_y1 + 20.0, -1020.0, top_y1 - 20.0, "03_MAIN_BOARD_主黑板", 3)
    draw_circle(ms, -1080.0, CY1, 14.0, "01_FRAME_外框导轨", 8)

    draw_rect(ms, 1000.0, bot_y1, 2000.0, top_y1, "03_MAIN_BOARD_主黑板", 3)
    draw_rect(ms, 1020.0, bot_y1 + 20.0, 1980.0, top_y1 - 20.0, "03_MAIN_BOARD_主黑板", 3)
    draw_circle(ms, 1080.0, CY1, 14.0, "01_FRAME_外框导轨", 8)

    # 左右外展副板 (1000x1200)
    draw_rect(ms, -3000.0, bot_y1, -2000.0, top_y1, "04_FOLD_BOARD_折展副板", 7)
    draw_rect(ms, -2980.0, bot_y1 + 20.0, -2020.0, top_y1 - 20.0, "04_FOLD_BOARD_折展副板", 7)

    draw_rect(ms, 2000.0, bot_y1, 3000.0, top_y1, "04_FOLD_BOARD_折展副板", 7)
    draw_rect(ms, 2020.0, bot_y1 + 20.0, 2980.0, top_y1 - 20.0, "04_FOLD_BOARD_折展副板", 7)

    # 4 组双节阻尼自锁铰链
    draw_hinge(ms, -2000.0, bot_y1 + 200.0)
    draw_hinge(ms, -2000.0, bot_y1 + 1000.0)
    draw_hinge(ms, 2000.0, bot_y1 + 200.0)
    draw_hinge(ms, 2000.0, bot_y1 + 1000.0)

    # 尺寸链
    draw_aligned_dim(ms, -3000.0, top_y1, -2000.0, top_y1, 140.0, True, "1000 [外展副板]")
    draw_aligned_dim(ms, -2000.0, top_y1, -1000.0, top_y1, 140.0, True, "1000 [主黑板面]")
    draw_aligned_dim(ms, -1000.0, top_y1, 1000.0, top_y1, 140.0, True, "2000 [86寸多媒体大屏]")
    draw_aligned_dim(ms, 1000.0, top_y1, 2000.0, top_y1, 140.0, True, "1000 [主黑板面]")
    draw_aligned_dim(ms, 2000.0, top_y1, 3000.0, top_y1, 140.0, True, "1000 [外展副板]")

    draw_aligned_dim(ms, -3000.0, top_y1, 3000.0, top_y1, 240.0, True, "6000 [第一代展开极限总跨度]")
    draw_aligned_dim(ms, -1060.0, c_top1, 1060.0, c_top1, 70.0, True, "2120 [顶部Canopy遮光雨棚]")

    draw_aligned_dim(ms, -3000.0, bot_y1, -3000.0, top_y1, -140.0, False, "1200 [书写板净高]")
    draw_aligned_dim(ms, -3000.0, t_bot1, -3000.0, c_top1, -250.0, False, "1380 [含雨棚底槽总高]")
    draw_aligned_dim(ms, 1060.0, top_y1 + 10.0, 1060.0, c_top1, 120.0, False, "90 [挑檐]")
    draw_aligned_dim(ms, 1060.0, t_bot1, 1060.0, bot_y1 - 10.0, 120.0, False, "50 [排砂槽]")

    draw_text(ms, "▲ 4组 双节阻尼自锁铰链 (80x70mm, SUS304 Ø10销轴, 扭矩3.5N·m, 0°~180°随动悬停自锁)", -2950.0, bot_y1 - 70.0, 20.0, "08_TEXT_技术说明", 2)
    draw_text(ms, "底部排砂集尘导轨槽 (5°双向导流坡, 7xØ12mm落砂孔, 间距300mm)", -750.0, t_bot1 - 50.0, 20.0, "08_TEXT_技术说明", 7)

    # =========================================================================
    # 工况二：标准闭合收拢教学状态 (Center Y = -150.0)
    # =========================================================================
    CY2 = -150.0
    top_y2 = CY2 + H_SCREEN / 2.0  # 450
    bot_y2 = CY2 - H_SCREEN / 2.0  # -750

    draw_text(ms, "第一代工况二：标准闭合收拢教学状态 [COMPACT - 常规教学总跨度 4000mm]", -2200.0, top_y2 + 370.0, 48.0, "08_TEXT_技术说明", 7)
    draw_text(ms, "技术特征: 外展副板已平整翻转内嵌于主板背侧收纳，整机恢复 4000mm 黄金包络；中间 86 寸大屏与两侧墨绿主板形成无缝教学协同界面。", -2200.0, top_y2 + 300.0, 24.0, "08_TEXT_技术说明", 7)

    draw_rect(ms, -2020.0, bot_y2, 2020.0, top_y2, "01_FRAME_外框导轨", 8)
    draw_rect(ms, -1000.0, bot_y2, 1000.0, top_y2, "01_FRAME_外框导轨", 8)
    draw_rect(ms, -950.0, bot_y2 + 50.0, 950.0, bot_y2 + 50.0 + H_LCD, "02_SCREEN_多媒体屏", 5)
    draw_rect(ms, -940.0, bot_y2 + 60.0, 940.0, bot_y2 + 40.0 + H_LCD, "02_SCREEN_多媒体屏", 5)
    draw_rect(ms, -90.0, bot_y2 + 15.0, 90.0, bot_y2 + 35.0, "01_FRAME_外框导轨", 8)
    draw_circle(ms, 0.0, bot_y2 + 25.0, 4.5, "06_HINGE_五金铰链", 2)
    c_top2, t_bot2 = draw_canopy_and_tray(ms, 0.0, top_y2, bot_y2, W_CANOPY, H_CANOPY)

    draw_rect(ms, -2000.0, bot_y2, -1000.0, top_y2, "03_MAIN_BOARD_主黑板", 3)
    draw_rect(ms, -1980.0, bot_y2 + 20.0, -1020.0, top_y2 - 20.0, "03_MAIN_BOARD_主黑板", 3)
    draw_circle(ms, -1080.0, CY2, 14.0, "01_FRAME_外框导轨", 8)

    draw_rect(ms, 1000.0, bot_y2, 2000.0, top_y2, "03_MAIN_BOARD_主黑板", 3)
    draw_rect(ms, 1020.0, bot_y2 + 20.0, 1980.0, top_y2 - 20.0, "03_MAIN_BOARD_主黑板", 3)
    draw_circle(ms, 1080.0, CY2, 14.0, "01_FRAME_外框导轨", 8)

    draw_hinge(ms, -2000.0, bot_y2 + 200.0)
    draw_hinge(ms, -2000.0, bot_y2 + 1000.0)
    draw_hinge(ms, 2000.0, bot_y2 + 200.0)
    draw_hinge(ms, 2000.0, bot_y2 + 1000.0)

    draw_aligned_dim(ms, -2000.0, top_y2, -1000.0, top_y2, 110.0, True, "1000 [主板+内折副板]")
    draw_aligned_dim(ms, -1000.0, top_y2, 1000.0, top_y2, 110.0, True, "2000 [86寸多媒体中置屏]")
    draw_aligned_dim(ms, 1000.0, top_y2, 2000.0, top_y2, 110.0, True, "1000 [主板+内折副板]")
    draw_aligned_dim(ms, -2000.0, top_y2, 2000.0, top_y2, 190.0, True, "4000 [闭合主体总宽]")
    draw_aligned_dim(ms, -2020.0, top_y2, 2020.0, top_y2, 260.0, True, "4040 [含双侧防撞端盖总宽]")

    draw_aligned_dim(ms, -2020.0, bot_y2, -2020.0, top_y2, -140.0, False, "1200 [书写板高度]")
    draw_aligned_dim(ms, -2020.0, t_bot2, -2020.0, c_top2, -250.0, False, "1380 [整机安装总高]")

    # =========================================================================
    # 图框与参数矩阵表
    # =========================================================================
    draw_rect(ms, -3550.0, -1550.0, 3550.0, 2850.0, "01_FRAME_外框导轨", 7)
    draw_rect(ms, -3520.0, -1520.0, 3520.0, 2820.0, "01_FRAME_外框导轨", 7)

    # 底部技术参数表
    TAB_X1, TAB_X2 = -3400.0, 950.0
    TAB_Y1, TAB_Y2 = -1480.0, -920.0
    draw_rect(ms, TAB_X1, TAB_Y1, TAB_X2, TAB_Y2, "01_FRAME_外框导轨", 8)
    draw_line(ms, TAB_X1, TAB_Y2 - 60.0, TAB_X2, TAB_Y2 - 60.0, "01_FRAME_外框导轨", 8)
    draw_text(ms, "【第一代翻转式多媒体智能黑板系统 - 全系统核心技术与工程参数矩阵】", TAB_X1 + 30.0, TAB_Y2 - 45.0, 28.0, "08_TEXT_技术说明", 7)

    notes = [
        "1. 几何包络与跨度: 闭合状态 4000x1380x180mm；展开极限 6000x1380x180mm (左右双翼各外展拓展 1000mm)；制造安装公差 ±2.0mm。",
        "2. 86寸微晶AG触控大屏: 3840x2160 4K 超高清，莫氏硬度 7H，雾度 8%，镜面反射率 <1.0%，彻底消除倒三角与吊灯眩光；触控精度 ±1.0mm，延迟 ≤8ms。",
        "3. 搪瓷墨绿主黑板: 0.40mm 进口微晶搪瓷烤漆钢板 (RAL 6005)，光泽度 ≤10 GU，粗糙度 Ra 1.6~3.2μm，17.2mm 阻燃高强度铝蜂窝夹芯，平整度误差 <0.8mm/㎡。",
        "4. 外展多功能白板: 0.35mm 高分子聚合物哑光白板面，漫反射率 ≥82%，0°~180° 无级自由旋转，教室侧向学生有效视场由 120° 拓宽至 178° 消除死角。",
        "5. 双节阻尼自锁铰链: ADC12 铝合金基座，SUS304 Ø10mm 转轴销钉，扭矩 3.5±0.3 N·m，任意角度随动悬停，0° 强磁锁闭与 180° 偏心机械自锁，50000次寿命。",
        "6. 顶部Canopy遮光雨棚: 宽 2120mm，挑檐前伸 120mm，向下倾斜 15° 物理遮断 35°~75° 吊顶灯射光；内部嵌倒V弹性PVC防尘密封罩与导电尼龙微米清扫刷。",
        "7. 底部排砂集尘导轨: 宽 2120mm，槽内双向 5° 导灰坡度，每隔 300mm 开设 Ø12mm 落砂通孔 (共7处)，下方模块化磁吸抽屉集尘盒 (清理周期 180课时/次)。",
        "8. 动力学与环保安全: 滑动启动力 ≤14.5N，匀速推力 ≤7.8N，运行噪音 ≤38.5 dB(A)；完全符合 JY/T 0148-2011、GB 40070-2021 防控近视强制卫生要求。"
    ]
    cur_y = TAB_Y2 - 105.0
    for n in notes:
        draw_text(ms, n, TAB_X1 + 25.0, cur_y, 18.0, "08_TEXT_技术说明", 7)
        cur_y -= 53.0

    # 右下角标准工程标题栏
    TB_X1, TB_X2 = 1100.0, 3400.0
    TB_Y1, TB_Y2 = -1480.0, -920.0
    draw_rect(ms, TB_X1, TB_Y1, TB_X2, TB_Y2, "01_FRAME_外框导轨", 8)
    draw_line(ms, TB_X1, TB_Y2 - 80.0, TB_X2, TB_Y2 - 80.0, "01_FRAME_外框导轨", 8)
    draw_text(ms, "工程装配与标准参数图纸 (v1.4)", TB_X1 + 40.0, TB_Y2 - 55.0, 32.0, "08_TEXT_技术说明", 7)

    tb_fields = [
        ("项目名称", "模块化折叠翻转多媒体教学黑板系统"),
        ("产品代际", "第一代 (Generation 1 - 翻转折叠展开避光系统)"),
        ("发明专利", "202511764745.X (发明) / 202522523482.5 (实用新型)"),
        ("设计发明人", "林诚俊"),
        ("图纸编号", "PJHB-GEN1-CAD-v1.4"),
        ("绘图标准", "GB/T 4458.4 / JY/T 0148-2011 / GB 40070-2021"),
        ("审核结论", "第 5 轮严格技术审核·参数数据 100% 完整补齐通过")
    ]
    ty = TB_Y2 - 130.0
    for k, v in tb_fields:
        draw_text(ms, f"{k}: {v}", TB_X1 + 40.0, ty, 20.0, "08_TEXT_技术说明", 7)
        ty -= 52.0

    try:
        acad.ZoomExtents()
        print(">>> 视口缩放 ZoomExtents 成功")
    except:
        pass

    # 保存
    target_path = r"D:\Desktop\pjhb\01-CAD工程图纸\第一代翻转式多媒体黑板_全系统标准工程参数与尺寸标注工程图_v1.4.dwg"
    try:
        doc.SaveAs(target_path)
        print(">>> [成功] v1.4 DWG 图纸已保存至:", target_path)
    except Exception as e:
        print("SaveAs failed:", e)

if __name__ == "__main__":
    run_gen1_annotated_v1_4()
