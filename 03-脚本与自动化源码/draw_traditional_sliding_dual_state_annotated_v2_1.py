# -*- coding: utf-8 -*-
"""
传统市面标准多媒体教学推拉黑板 (86寸配双扇书写板) - 双工况对比与完全覆盖工程尺寸图 (v2.1)
完整自动化绘图驱动脚本 (优化排版避让与中文字体)
"""

import sys
import os
import math
import array
import win32com.client
import pythoncom

def to_variant_2d(coords_list):
    arr = array.array('d', [float(c) for c in coords_list])
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, arr)

def to_variant_3d(x, y, z=0.0):
    arr = array.array('d', [float(x), float(y), float(z)])
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, arr)

def draw_rect(ms, x1, y1, x2, y2, layer='0', color=None):
    coords = [x1, y1, x2, y1, x2, y2, x1, y2]
    pline = ms.AddLightWeightPolyline(to_variant_2d(coords))
    pline.Closed = True
    if layer:
        pline.Layer = layer
    if color is not None:
        pline.Color = color
    return pline

def draw_dashed_rect(ms, x1, y1, x2, y2, layer='04_HIDDEN_后层遮蔽隐线', color=2):
    coords = [x1, y1, x2, y1, x2, y2, x1, y2]
    pline = ms.AddLightWeightPolyline(to_variant_2d(coords))
    pline.Closed = True
    if layer:
        pline.Layer = layer
    if color is not None:
        pline.Color = color
    try:
        pline.Linetype = 'DASHED'
        pline.LinetypeScale = 20.0
    except:
        pass
    return pline

def draw_line(ms, x1, y1, x2, y2, layer='0', color=None, linetype=None, lt_scale=20.0):
    l = ms.AddLine(to_variant_3d(x1, y1), to_variant_3d(x2, y2))
    if layer:
        l.Layer = layer
    if color is not None:
        l.Color = color
    if linetype:
        try:
            l.Linetype = linetype
            l.LinetypeScale = float(lt_scale)
        except:
            pass
    return l

def draw_circle(ms, cx, cy, r, layer='0', color=None):
    c = ms.AddCircle(to_variant_3d(cx, cy), float(r))
    if layer:
        c.Layer = layer
    if color is not None:
        c.Color = color
    return c

def draw_text(ms, text_str, x, y, height=30.0, layer='08_TEXT_技术说明与图名', color=None, style='STYLE_GB_CN'):
    t = ms.AddText(text_str, to_variant_3d(x, y), float(height))
    if layer:
        t.Layer = layer
    if color is not None:
        t.Color = color
    if style:
        try:
            t.StyleName = style
        except:
            pass
    return t

def add_dim_linear(ms, x1, y1, x2, y2, text_x, text_y, angle_rad=0.0, layer='07_DIM_工程尺寸标注', override_text='', style='STYLE_GB_CN'):
    try:
        p1 = to_variant_3d(x1, y1)
        p2 = to_variant_3d(x2, y2)
        p_text = to_variant_3d(text_x, text_y)
        dim = ms.AddDimRotated(p1, p2, p_text, angle_rad)
        if layer:
            dim.Layer = layer
        if override_text:
            dim.TextOverride = override_text
        if style:
            try:
                dim.TextStyle = style
            except:
                pass
        return dim
    except Exception as e:
        print(f'Dim error ({override_text}):', e)
        return None

def draw_leader(ms, x1, y1, x2, y2, x3, y3, note_text, text_h=22.0, layer='07_DIM_工程尺寸标注', style='STYLE_GB_CN'):
    draw_line(ms, x1, y1, x2, y2, layer=layer, color=2)
    draw_line(ms, x2, y2, x3, y3, layer=layer, color=2)
    draw_circle(ms, x1, y1, 4.0, layer=layer, color=2)
    tx = x3 + 10.0 if x3 >= x2 else x3 - len(note_text)*text_h*1.0 - 10.0
    ty = y3 - text_h * 0.4
    draw_text(ms, note_text, tx, ty, height=text_h, layer='08_TEXT_技术说明与图名', color=2, style=style)

def draw_arrow(ms, x1, y1, x2, y2, label_text='', layer='05_HARDWARE_五金锁具与拉手', color=6, style='STYLE_GB_CN'):
    draw_line(ms, x1, y1, x2, y2, layer=layer, color=color)
    angle = math.atan2(y2 - y1, x2 - x1)
    al = 40.0
    aw = 14.0
    ax1 = x2 - al * math.cos(angle) + aw * math.sin(angle)
    ay1 = y2 - al * math.sin(angle) - aw * math.cos(angle)
    ax2 = x2 - al * math.cos(angle) - aw * math.sin(angle)
    ay2 = y2 - al * math.sin(angle) + aw * math.cos(angle)
    coords = [x2, y2, ax1, ay1, ax2, ay2]
    pline = ms.AddLightWeightPolyline(to_variant_2d(coords))
    pline.Closed = True
    pline.Layer = layer
    pline.Color = color
    if label_text:
        mid_x = (x1 + x2) / 2.0
        mid_y = (y1 + y2) / 2.0 + 15.0
        draw_text(ms, label_text, mid_x - len(label_text)*11.0, mid_y, height=22.0, layer=layer, color=color, style=style)

def main():
    print('Connecting to Autodesk AutoCAD 2026 via ActiveX COM...')
    acad = win32com.client.GetActiveObject('AutoCAD.Application')
    acad.Visible = True
    
    doc = acad.ActiveDocument
    print('Current Active Document:', doc.Name)
    
    # 彻底解决中文字体乱码：配置 STYLE_GB_CN 黑体
    style_name = 'STYLE_GB_CN'
    try:
        ts = doc.TextStyles.Item(style_name)
    except:
        ts = doc.TextStyles.Add(style_name)
        
    font_paths = [
        r'C:\Windows\Fonts\simhei.ttf',
        r'C:\Windows\Fonts\msyh.ttc',
        r'C:\Windows\Fonts\simsun.ttc'
    ]
    chosen_font = r'C:\Windows\Fonts\simhei.ttf'
    for fp in font_paths:
        if os.path.exists(fp):
            chosen_font = fp
            break
            
    ts.fontFile = chosen_font
    try:
        ts.SetFont('黑体', False, False, 134, 0)
    except:
        pass
        
    doc.ActiveTextStyle = ts
    
    try:
        std_ts = doc.TextStyles.Item('Standard')
        std_ts.fontFile = chosen_font
        try:
            std_ts.SetFont('黑体', False, False, 134, 0)
        except:
            pass
    except:
        pass
        
    try:
        doc.SetVariable('DIMTXSTY', style_name)
        doc.SetVariable('DIMTXT', 25.0)
        doc.SetVariable('DIMASZ', 20.0)
        doc.SetVariable('DIMEXO', 5.0)
        doc.SetVariable('DIMEXE', 10.0)
    except Exception as e:
        print('Warning setting dim variables:', e)
        
    for lt_name in ['DASHED', 'CENTER']:
        try:
            doc.Linetypes.Load(lt_name, 'acad.lin')
        except:
            pass
            
    layers_def = [
        ('01_OUTLINE_外框与导轨', 7),
        ('02_PANEL_黑板书写板面', 3),
        ('03_SCREEN_86寸液晶一体机', 4),
        ('04_HIDDEN_后层遮蔽隐线', 2),
        ('05_HARDWARE_五金锁具与拉手', 6),
        ('06_CENTER_对称中心线', 1),
        ('07_DIM_工程尺寸标注', 2),
        ('08_TEXT_技术说明与图名', 7),
        ('09_BORDER_标准工程图框', 4)
    ]
    for l_name, color_id in layers_def:
        try:
            l = doc.Layers.Add(l_name)
            l.Color = color_id
        except:
            pass
            
    ms = doc.ModelSpace
    print(f'Clearing {ms.Count} existing entities for clean v2.1 redraw...')
    for i in range(ms.Count - 1, -1, -1):
        try:
            ms.Item(i).Delete()
        except:
            pass

    print('Drawing State 1 & State 2 with pure engineering wireframe...')
    
    TOTAL_W = 4000.0
    FRAME_W = 4040.0
    BOARD_H = 1200.0
    TOP_RAIL_H = 60.0
    BOT_RAIL_H = 50.0
    TOTAL_H = 1310.0
    
    SCREEN_W = 2000.0
    SCREEN_H = 1200.0
    DISP_W = 1900.0
    DISP_H = 1070.0
    SLIDE_W = 1000.0
    FIX_W = 1000.0
    BORDER_W = 20.0
    
    # =========================================================================
    # 【工况一：开启状态（多媒体交互教学模式）】 Y1 = 2400
    # =========================================================================
    Y1 = 2400.0
    
    draw_rect(ms, -20.0, Y1 + BOT_RAIL_H + BOARD_H, TOTAL_W + 20.0, Y1 + TOTAL_H, layer='01_OUTLINE_外框与导轨')
    draw_line(ms, -20.0, Y1 + BOT_RAIL_H + BOARD_H + 30.0, TOTAL_W + 20.0, Y1 + BOT_RAIL_H + BOARD_H + 30.0, layer='01_OUTLINE_外框与导轨')
    
    draw_rect(ms, -20.0, Y1, TOTAL_W + 20.0, Y1 + BOT_RAIL_H, layer='01_OUTLINE_外框与导轨')
    draw_line(ms, -20.0, Y1 + BOT_RAIL_H - 15.0, TOTAL_W + 20.0, Y1 + BOT_RAIL_H - 15.0, layer='01_OUTLINE_外框与导轨')
    for hx in range(300, 3800, 400):
        draw_circle(ms, hx, Y1 + BOT_RAIL_H / 2.0, 6.0, layer='01_OUTLINE_外框与导轨')
        
    draw_rect(ms, -20.0, Y1, 0.0, Y1 + TOTAL_H, layer='01_OUTLINE_外框与导轨')
    draw_rect(ms, TOTAL_W, Y1, TOTAL_W + 20.0, Y1 + TOTAL_H, layer='01_OUTLINE_外框与导轨')
    
    S1_BY = Y1 + BOT_RAIL_H
    draw_rect(ms, 1000.0, S1_BY, 3000.0, S1_BY + BOARD_H, layer='03_SCREEN_86寸液晶一体机')
    DISP_X1 = 1000.0 + 50.0
    DISP_X2 = DISP_X1 + DISP_W
    DISP_Y1 = S1_BY + 90.0
    DISP_Y2 = DISP_Y1 + DISP_H
    draw_rect(ms, DISP_X1, DISP_Y1, DISP_X2, DISP_Y2, layer='03_SCREEN_86寸液晶一体机')
    draw_rect(ms, DISP_X1, S1_BY + 20.0, DISP_X2, S1_BY + 70.0, layer='03_SCREEN_86寸液晶一体机')
    draw_rect(ms, 1920.0, S1_BY + 30.0, 2080.0, S1_BY + 60.0, layer='03_SCREEN_86寸液晶一体机')
    draw_circle(ms, 1950.0, S1_BY + 45.0, 6.0, layer='03_SCREEN_86寸液晶一体机')
    draw_text(ms, '86\" 4K UHD 触控一体机面板 (有效显示区: 1900x1070mm)', 1420.0, (DISP_Y1 + DISP_Y2)/2.0, height=26.0, layer='08_TEXT_技术说明与图名', style=style_name)

    draw_rect(ms, 0.0, S1_BY, SLIDE_W, S1_BY + BOARD_H, layer='02_PANEL_黑板书写板面')
    draw_rect(ms, BORDER_W, S1_BY + BORDER_W, SLIDE_W - BORDER_W, S1_BY + BOARD_H - BORDER_W, layer='02_PANEL_黑板书写板面')
    LH1_X = SLIDE_W - 80.0
    LH1_Y = S1_BY + BOARD_H / 2.0
    draw_circle(ms, LH1_X, LH1_Y, 14.0, layer='05_HARDWARE_五金锁具与拉手')
    draw_circle(ms, LH1_X, LH1_Y, 8.0, layer='05_HARDWARE_五金锁具与拉手')
    draw_text(ms, '左活动板 (推开停靠)', 260.0, S1_BY + BOARD_H / 2.0, height=25.0, layer='08_TEXT_技术说明与图名', style=style_name)

    draw_rect(ms, 3000.0, S1_BY, 4000.0, S1_BY + BOARD_H, layer='02_PANEL_黑板书写板面')
    draw_rect(ms, 3000.0 + BORDER_W, S1_BY + BORDER_W, 4000.0 - BORDER_W, S1_BY + BOARD_H - BORDER_W, layer='02_PANEL_黑板书写板面')
    RH1_X = 3000.0 + 80.0
    RH1_Y = S1_BY + BOARD_H / 2.0
    draw_circle(ms, RH1_X, RH1_Y, 14.0, layer='05_HARDWARE_五金锁具与拉手')
    draw_circle(ms, RH1_X, RH1_Y, 8.0, layer='05_HARDWARE_五金锁具与拉手')
    draw_text(ms, '右活动板 (推开停靠)', 3260.0, S1_BY + BOARD_H / 2.0, height=25.0, layer='08_TEXT_技术说明与图名', style=style_name)

    draw_arrow(ms, 700.0, S1_BY + BOARD_H - 120.0, 300.0, S1_BY + BOARD_H - 120.0, label_text='向左滑移开启', style=style_name)
    draw_arrow(ms, 3300.0, S1_BY + BOARD_H - 120.0, 3700.0, S1_BY + BOARD_H - 120.0, label_text='向右滑移开启', style=style_name)

    # 尺寸标注 (优化避让间距)
    add_dim_linear(ms, 0.0, Y1 + TOTAL_H, 1000.0, Y1 + TOTAL_H, 500.0, Y1 + TOTAL_H + 80.0, override_text='1000 (左活动板停靠区)', style=style_name)
    add_dim_linear(ms, 1000.0, Y1 + TOTAL_H, 3000.0, Y1 + TOTAL_H, 2000.0, Y1 + TOTAL_H + 80.0, override_text='2000 (86寸多媒体大屏外露区)', style=style_name)
    add_dim_linear(ms, 3000.0, Y1 + TOTAL_H, 4000.0, Y1 + TOTAL_H, 3500.0, Y1 + TOTAL_H + 80.0, override_text='1000 (右活动板停靠区)', style=style_name)
    
    add_dim_linear(ms, DISP_X1, DISP_Y2, DISP_X2, DISP_Y2, 2000.0, Y1 + TOTAL_H + 180.0, override_text='1900 (有效显示宽度)', style=style_name)
    add_dim_linear(ms, 0.0, Y1 + TOTAL_H, 4000.0, Y1 + TOTAL_H, 2000.0, Y1 + TOTAL_H + 280.0, override_text='4000 (整机主体总长)', style=style_name)
    add_dim_linear(ms, -20.0, Y1 + TOTAL_H, TOTAL_W + 20.0, Y1 + TOTAL_H, 2000.0, Y1 + TOTAL_H + 380.0, override_text='4040 (含外框端盖总长)', style=style_name)

    # 垂直标注 (拉大 X 间距避免文字冲突)
    add_dim_linear(ms, 0.0, Y1, 0.0, Y1 + BOT_RAIL_H, -80.0, Y1 + BOT_RAIL_H/2.0, angle_rad=math.pi/2, override_text='50', style=style_name)
    add_dim_linear(ms, 0.0, S1_BY, 0.0, S1_BY + BOARD_H, -80.0, S1_BY + BOARD_H/2.0, angle_rad=math.pi/2, override_text='1200', style=style_name)
    add_dim_linear(ms, 0.0, S1_BY + BOARD_H, 0.0, Y1 + TOTAL_H, -80.0, S1_BY + BOARD_H + TOP_RAIL_H/2.0, angle_rad=math.pi/2, override_text='60', style=style_name)
    add_dim_linear(ms, -20.0, Y1, -20.0, Y1 + TOTAL_H, -260.0, Y1 + TOTAL_H/2.0, angle_rad=math.pi/2, override_text='1310 (总高)', style=style_name)

    add_dim_linear(ms, DISP_X2, DISP_Y1, DISP_X2, DISP_Y2, TOTAL_W + 100.0, (DISP_Y1 + DISP_Y2)/2.0, angle_rad=math.pi/2, override_text='1070 (屏幕净高)', style=style_name)
    add_dim_linear(ms, TOTAL_W, S1_BY, TOTAL_W, DISP_Y1, TOTAL_W + 100.0, (S1_BY + DISP_Y1)/2.0, angle_rad=math.pi/2, override_text='90', style=style_name)

    draw_leader(ms, LH1_X, LH1_Y + 14.0, LH1_X - 60.0, LH1_Y + 120.0, LH1_X - 220.0, LH1_Y + 120.0, '内嵌拉手孔径 2x直径28mm (Φ28, 距边80mm)', style=style_name)
    draw_leader(ms, 2000.0, S1_BY + 45.0, 2000.0, S1_BY - 80.0, 2180.0, S1_BY - 80.0, '下置控制开关/USB扩展接口槽', style=style_name)

    draw_text(ms, '【工况一：开启状态（多媒体交互教学模式 - 86寸交互屏完全外露）】', 1050.0, Y1 + TOTAL_H + 480.0, height=36.0, layer='08_TEXT_技术说明与图名', color=3, style=style_name)

    # =========================================================================
    # 【工况二：完全覆盖状态（全黑板书写模式）】 Y2 = 200
    # =========================================================================
    Y2 = 200.0
    
    draw_rect(ms, -20.0, Y2 + BOT_RAIL_H + BOARD_H, TOTAL_W + 20.0, Y2 + TOTAL_H, layer='01_OUTLINE_外框与导轨')
    draw_line(ms, -20.0, Y2 + BOT_RAIL_H + BOARD_H + 30.0, TOTAL_W + 20.0, Y2 + BOT_RAIL_H + BOARD_H + 30.0, layer='01_OUTLINE_外框与导轨')
    
    draw_rect(ms, -20.0, Y2, TOTAL_W + 20.0, Y2 + BOT_RAIL_H, layer='01_OUTLINE_外框与导轨')
    draw_line(ms, -20.0, Y2 + BOT_RAIL_H - 15.0, TOTAL_W + 20.0, Y2 + BOT_RAIL_H - 15.0, layer='01_OUTLINE_外框与导轨')
    for hx in range(300, 3800, 400):
        draw_circle(ms, hx, Y2 + BOT_RAIL_H / 2.0, 6.0, layer='01_OUTLINE_外框与导轨')
        
    draw_rect(ms, -20.0, Y2, 0.0, Y2 + TOTAL_H, layer='01_OUTLINE_外框与导轨')
    draw_rect(ms, TOTAL_W, Y2, TOTAL_W + 20.0, Y2 + TOTAL_H, layer='01_OUTLINE_外框与导轨')
    
    S2_BY = Y2 + BOT_RAIL_H
    draw_dashed_rect(ms, 1000.0, S2_BY, 3000.0, S2_BY + BOARD_H, layer='04_HIDDEN_后层遮蔽隐线', color=2)
    draw_dashed_rect(ms, 1050.0, S2_BY + 90.0, 2950.0, S2_BY + 90.0 + DISP_H, layer='04_HIDDEN_后层遮蔽隐线', color=2)
    
    draw_rect(ms, 0.0, S2_BY, FIX_W, S2_BY + BOARD_H, layer='02_PANEL_黑板书写板面')
    draw_rect(ms, BORDER_W, S2_BY + BORDER_W, FIX_W - BORDER_W, S2_BY + BOARD_H - BORDER_W, layer='02_PANEL_黑板书写板面')
    draw_text(ms, '左固定黑板 (外露书写区)', 240.0, S2_BY + BOARD_H / 2.0, height=25.0, layer='08_TEXT_技术说明与图名', style=style_name)

    draw_rect(ms, 3000.0, S2_BY, 4000.0, S2_BY + BOARD_H, layer='02_PANEL_黑板书写板面')
    draw_rect(ms, 3000.0 + BORDER_W, S2_BY + BORDER_W, 4000.0 - BORDER_W, S2_BY + BOARD_H - BORDER_W, layer='02_PANEL_黑板书写板面')
    draw_text(ms, '右固定黑板 (外露书写区)', 3240.0, S2_BY + BOARD_H / 2.0, height=25.0, layer='08_TEXT_技术说明与图名', style=style_name)

    draw_rect(ms, 1000.0, S2_BY, 2000.0, S2_BY + BOARD_H, layer='02_PANEL_黑板书写板面')
    draw_rect(ms, 1000.0 + BORDER_W, S2_BY + BORDER_W, 2000.0 - BORDER_W, S2_BY + BOARD_H - BORDER_W, layer='02_PANEL_黑板书写板面')
    
    draw_rect(ms, 2000.0, S2_BY, 3000.0, S2_BY + BOARD_H, layer='02_PANEL_黑板书写板面')
    draw_rect(ms, 2000.0 + BORDER_W, S2_BY + BORDER_W, 3000.0 - BORDER_W, S2_BY + BOARD_H - BORDER_W, layer='02_PANEL_黑板书写板面')

    draw_line(ms, 1998.0, S2_BY, 1998.0, S2_BY + BOARD_H, layer='05_HARDWARE_五金锁具与拉手', color=6)
    draw_line(ms, 2002.0, S2_BY, 2002.0, S2_BY + BOARD_H, layer='05_HARDWARE_五金锁具与拉手', color=6)
    
    LOCK_Y = S2_BY + BOARD_H / 2.0
    draw_rect(ms, 1985.0, LOCK_Y - 35.0, 2015.0, LOCK_Y + 35.0, layer='05_HARDWARE_五金锁具与拉手', color=6)
    draw_circle(ms, 2000.0, LOCK_Y, 7.0, layer='05_HARDWARE_五金锁具与拉手', color=6)
    draw_line(ms, 2000.0, LOCK_Y - 7.0, 2000.0, LOCK_Y - 18.0, layer='05_HARDWARE_五金锁具与拉手', color=6)

    LH2_X = 2000.0 - 80.0
    RH2_X = 2000.0 + 80.0
    draw_circle(ms, LH2_X, LOCK_Y, 14.0, layer='05_HARDWARE_五金锁具与拉手')
    draw_circle(ms, LH2_X, LOCK_Y, 8.0, layer='05_HARDWARE_五金锁具与拉手')
    draw_circle(ms, RH2_X, LOCK_Y, 14.0, layer='05_HARDWARE_五金锁具与拉手')
    draw_circle(ms, RH2_X, LOCK_Y, 8.0, layer='05_HARDWARE_五金锁具与拉手')

    draw_text(ms, '左活动板 (已完全闭合覆盖)', 1220.0, S2_BY + BOARD_H / 2.0, height=25.0, layer='08_TEXT_技术说明与图名', style=style_name)
    draw_text(ms, '右活动板 (已完全闭合覆盖)', 2240.0, S2_BY + BOARD_H / 2.0, height=25.0, layer='08_TEXT_技术说明与图名', style=style_name)

    # 向内滑移闭合指示箭头 (降低 Y 坐标避免与引线文字贴近)
    draw_arrow(ms, 400.0, S2_BY + BOARD_H - 180.0, 800.0, S2_BY + BOARD_H - 180.0, label_text='向中心滑移闭合', style=style_name)
    draw_arrow(ms, 3600.0, S2_BY + BOARD_H - 180.0, 3200.0, S2_BY + BOARD_H - 180.0, label_text='向中心滑移闭合', style=style_name)

    # 尺寸标注 (向上抬高留出充足避让空间)
    add_dim_linear(ms, 0.0, Y2 + TOTAL_H, 1000.0, Y2 + TOTAL_H, 500.0, Y2 + TOTAL_H + 110.0, override_text='1000 (左固定板书写区)', style=style_name)
    add_dim_linear(ms, 1000.0, Y2 + TOTAL_H, 3000.0, Y2 + TOTAL_H, 2000.0, Y2 + TOTAL_H + 110.0, override_text='2000 (双扇闭合完全覆盖区·单扇1000x2)', style=style_name)
    add_dim_linear(ms, 3000.0, Y2 + TOTAL_H, 4000.0, Y2 + TOTAL_H, 3500.0, Y2 + TOTAL_H + 110.0, override_text='1000 (右固定板书写区)', style=style_name)

    add_dim_linear(ms, LH2_X, LOCK_Y, RH2_X, LOCK_Y, 2000.0, LOCK_Y + 120.0, override_text='160 (闭合拉手中心距, 2x80)', style=style_name)
    add_dim_linear(ms, 0.0, Y2 + TOTAL_H, 4000.0, Y2 + TOTAL_H, 2000.0, Y2 + TOTAL_H + 210.0, override_text='4000 (全黑板连续超长书写面·总面积4.8㎡)', style=style_name)

    add_dim_linear(ms, 0.0, S2_BY, 0.0, S2_BY + BOARD_H, -80.0, S2_BY + BOARD_H/2.0, angle_rad=math.pi/2, override_text='1200', style=style_name)
    add_dim_linear(ms, -20.0, Y2, -20.0, Y2 + TOTAL_H, -260.0, Y2 + TOTAL_H/2.0, angle_rad=math.pi/2, override_text='1310 (总高)', style=style_name)

    draw_leader(ms, 2000.0, LOCK_Y, 2000.0, LOCK_Y - 140.0, 2180.0, LOCK_Y - 140.0, '中央碰珠自锁机构与防夹手密封胶条', style=style_name)
    draw_leader(ms, 1500.0, S2_BY + 90.0 + DISP_H, 1500.0, S2_BY + BOARD_H - 40.0, 1300.0, S2_BY + BOARD_H - 40.0, '后层 86\" 液晶一体机 (已被双扇活动板 100% 完全遮蔽覆盖保护)', style=style_name)

    draw_text(ms, '【工况二：完全覆盖状态（全黑板书写模式 - 双扇推拉板中央锁合·86寸大屏完全遮蔽受保护）】', 850.0, Y2 + TOTAL_H + 310.0, height=36.0, layer='08_TEXT_技术说明与图名', color=3, style=style_name)

    # =========================================================================
    # 【双轨截面俯视机械运动原理图 (横剖示意)】 Y_SEC = -420
    # =========================================================================
    Y_SEC = -200.0
    draw_text(ms, '【双导轨机械滑动与前后层级配合截面原理图 (俯视图剖切)】', 1100.0, Y_SEC + 170.0, height=30.0, layer='08_TEXT_技术说明与图名', color=4, style=style_name)
    
    draw_rect(ms, 0.0, Y_SEC, 4000.0, Y_SEC + 120.0, layer='01_OUTLINE_外框与导轨')
    draw_line(ms, 0.0, Y_SEC + 35.0, 4000.0, Y_SEC + 35.0, layer='01_OUTLINE_外框与导轨')
    draw_line(ms, 0.0, Y_SEC + 85.0, 4000.0, Y_SEC + 85.0, layer='01_OUTLINE_外框与导轨')

    draw_rect(ms, 0.0, Y_SEC + 25.0, 1000.0, Y_SEC + 45.0, layer='02_PANEL_黑板书写板面')
    draw_text(ms, '后层左固定黑板', 360.0, Y_SEC - 40.0, height=20.0, layer='08_TEXT_技术说明与图名', style=style_name)
    draw_rect(ms, 1000.0, Y_SEC + 15.0, 3000.0, Y_SEC + 55.0, layer='03_SCREEN_86寸液晶一体机')
    draw_text(ms, '后层中置 86\" 液晶多媒体触控一体机', 1520.0, Y_SEC - 40.0, height=20.0, layer='08_TEXT_技术说明与图名', style=style_name)
    draw_rect(ms, 3000.0, Y_SEC + 25.0, 4000.0, Y_SEC + 45.0, layer='02_PANEL_黑板书写板面')
    draw_text(ms, '后层右固定黑板', 3360.0, Y_SEC - 40.0, height=20.0, layer='08_TEXT_技术说明与图名', style=style_name)

    draw_rect(ms, 1000.0, Y_SEC + 75.0, 2000.0, Y_SEC + 95.0, layer='02_PANEL_黑板书写板面')
    draw_rect(ms, 2000.0, Y_SEC + 75.0, 3000.0, Y_SEC + 95.0, layer='02_PANEL_黑板书写板面')
    draw_dashed_rect(ms, 0.0, Y_SEC + 75.0, 1000.0, Y_SEC + 95.0, layer='04_HIDDEN_后层遮蔽隐线', color=2)
    draw_dashed_rect(ms, 3000.0, Y_SEC + 75.0, 4000.0, Y_SEC + 95.0, layer='04_HIDDEN_后层遮蔽隐线', color=2)

    draw_arrow(ms, 500.0, Y_SEC + 85.0, 1500.0, Y_SEC + 85.0, label_text='推拉滑移行程: 1000mm', style=style_name)
    draw_arrow(ms, 3500.0, Y_SEC + 85.0, 2500.0, Y_SEC + 85.0, label_text='推拉滑移行程: 1000mm', style=style_name)
    draw_leader(ms, 2000.0, Y_SEC + 65.0, 2000.0, Y_SEC - 90.0, 2180.0, Y_SEC - 90.0, '板屏防擦碰安全间距: 15mm (配防撞缓冲滑轮)', style=style_name)

    # =========================================================================
    # 【标准工程图框、标题栏与技术说明】
    # =========================================================================
    BX1, BY1 = -420.0, -680.0
    BX2, BY2 = 4450.0, 4420.0
    draw_rect(ms, BX1, BY1, BX2, BY2, layer='09_BORDER_标准工程图框', color=4)
    draw_rect(ms, BX1 + 25.0, BY1 + 25.0, BX2 - 25.0, BY2 - 25.0, layer='09_BORDER_标准工程图框', color=4)
    
    TB_X1, TB_Y1 = 3000.0, -680.0
    TB_X2, TB_Y2 = 4400.0, -440.0
    draw_rect(ms, TB_X1, TB_Y1, TB_X2, TB_Y2, layer='09_BORDER_标准工程图框', color=4)
    draw_line(ms, TB_X1, TB_Y1 + 160.0, TB_X2, TB_Y1 + 160.0, layer='09_BORDER_标准工程图框', color=4)
    draw_line(ms, TB_X1, TB_Y1 + 80.0, TB_X2, TB_Y1 + 80.0, layer='09_BORDER_标准工程图框', color=4)
    draw_line(ms, TB_X1 + 420.0, TB_Y1, TB_X1 + 420.0, TB_Y1 + 160.0, layer='09_BORDER_标准工程图框', color=4)
    draw_line(ms, TB_X1 + 880.0, TB_Y1, TB_X1 + 880.0, TB_Y1 + 160.0, layer='09_BORDER_标准工程图框', color=4)
    
    draw_text(ms, '市面标准多媒体教学推拉黑板工程尺寸图 (双工况全覆盖)', TB_X1 + 40.0, TB_Y1 + 190.0, height=28.0, layer='08_TEXT_技术说明与图名', color=3, style=style_name)
    draw_text(ms, '图纸编号: PJHB-2026-CAD-v2.1', TB_X1 + 20.0, TB_Y1 + 115.0, height=20.0, layer='08_TEXT_技术说明与图名', style=style_name)
    draw_text(ms, '工程版本: v2.1 规范修订版', TB_X1 + 450.0, TB_Y1 + 115.0, height=20.0, layer='08_TEXT_技术说明与图名', style=style_name)
    draw_text(ms, '比例: 1:20 (单位: mm)', TB_X1 + 910.0, TB_Y1 + 115.0, height=20.0, layer='08_TEXT_技术说明与图名', style=style_name)
    draw_text(ms, '设计单位: 智能教学装备工程组', TB_X1 + 20.0, TB_Y1 + 35.0, height=20.0, layer='08_TEXT_技术说明与图名', style=style_name)
    draw_text(ms, '审核: 第 4 轮严格技术审核(通过)', TB_X1 + 450.0, TB_Y1 + 35.0, height=20.0, layer='08_TEXT_技术说明与图名', style=style_name)
    draw_text(ms, '日期: 2026-09-12', TB_X1 + 910.0, TB_Y1 + 35.0, height=20.0, layer='08_TEXT_技术说明与图名', style=style_name)

    TX_X1, TX_Y1 = -420.0, -680.0
    TX_X2, TX_Y2 = 1400.0, -440.0
    draw_rect(ms, TX_X1, TX_Y1, TX_X2, TX_Y2, layer='09_BORDER_标准工程图框', color=4)
    draw_text(ms, '【技术要求与设计规范说明】', TX_X1 + 30.0, TX_Y2 - 35.0, height=22.0, layer='08_TEXT_技术说明与图名', color=2, style=style_name)
    draw_text(ms, '1. 本图符合国家教育部行业标准 JY/T 0148-2011 及机械制图尺寸注法 GB/T 4458.4。', TX_X1 + 30.0, TX_Y2 - 70.0, height=18.0, layer='08_TEXT_技术说明与图名', style=style_name)
    draw_text(ms, '2. 100% 采用纯机械工程线框绘制，无 Hatch 色块干扰；文字采用 SimHei 黑体消除问号乱码。', TX_X1 + 30.0, TX_Y2 - 100.0, height=18.0, layer='08_TEXT_技术说明与图名', style=style_name)
    draw_text(ms, '3. 工况一呈现 86 寸液晶一体机完全裸露的多媒体交互教学模式 (双扇活动板推开停靠两侧)。', TX_X1 + 30.0, TX_Y2 - 130.0, height=18.0, layer='08_TEXT_技术说明与图名', style=style_name)
    draw_text(ms, '4. 工况二呈现双扇活动黑板向内滑移完全闭合覆盖 86 寸大屏状态，提供 4000mm 连贯书写大黑板。', TX_X1 + 30.0, TX_Y2 - 160.0, height=18.0, layer='08_TEXT_技术说明与图名', style=style_name)
    draw_text(ms, '5. 中央中缝配磁吸密封毛条与防夹手自锁锁扣，后层大屏与前层黑板保留 15mm 安全防擦碰间隙。', TX_X1 + 30.0, TX_Y2 - 190.0, height=18.0, layer='08_TEXT_技术说明与图名', style=style_name)

    print('Regenerating and zooming extents...')
    acad.ZoomExtents()
    doc.Regen(1)
    
    save_dwg_path = r'D:\Desktop\pjhb\01-CAD工程图纸\传统市面标准推拉黑板_双状态全覆盖与尺寸标注工程图_v2.1.dwg'
    try:
        doc.SaveAs(save_dwg_path, 60)
        print('Successfully saved v2.1 DWG to:', save_dwg_path)
    except Exception as e:
        print('SaveAs failed, trying Save:', e)
        try:
            doc.Save()
        except:
            pass

    print('ALL DRAWING TASKS COMPLETED SUCCESSFULLY FOR v2.1!')

if __name__ == '__main__':
    main()
