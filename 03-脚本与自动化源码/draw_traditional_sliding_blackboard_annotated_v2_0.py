# -*- coding: utf-8 -*-
"""
传统市面标准多媒体教学推拉黑板 (86寸配双扇书写板) - AutoCAD 2026 纯线框工程尺寸标注图绘制脚本 (v2.0)
文件版本: v2.0
设计要求与规范变更说明:
1. 绝对无涂色：彻底移除所有 Hatch 实体填充色块，回归纯正工业机械线框图 (Pure Wireframe Engineering Drawing)。
2. 形态纯粹化：仅保留市面传统推拉黑板构型（中置 86寸 交互大屏 + 左右标准推拉书写板 + 上下轨道梁），去除展开态。
3. 全面工程化标注：
   - 水平方向三层尺寸链（细部尺寸、大构件尺寸、整机总宽 4000/4040mm）。
   - 垂直方向两层尺寸链（导轨高度、板面 1200mm、屏幕净高 1070mm、整机总高 1310mm）。
   - 局部构造定位标注（把手孔位 80mm、包边 20mm、孔径 Ø28mm）。
   - 红色对称中心线 (Centerline) 与推拉滑移双向指示箭头。
   - 6 大核心部件引线工艺说明与标准工程图签 (Title Block)。
4. 保存 DWG 至: D:\\Desktop\\pjhb\\01-CAD工程图纸\\传统市面标准推拉黑板_无涂色工程尺寸标注图_v2.0.dwg
"""

import sys
import os
import math
import array
import win32com.client
import pythoncom

def to_variant_2d(coords_list):
    """将坐标列表转为 AutoCAD 2D 轻量多段线要求的 VARIANT"""
    arr = array.array('d', [float(c) for c in coords_list])
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, arr)

def to_variant_3d(x, y, z=0.0):
    """将单个三维坐标转为 VARIANT"""
    arr = array.array('d', [float(x), float(y), float(z)])
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, arr)

def draw_rect(ms, x1, y1, x2, y2, layer="0", color=None):
    """绘制纯线框闭合矩形"""
    coords = [x1, y1, x2, y1, x2, y2, x1, y2]
    pline = ms.AddLightWeightPolyline(to_variant_2d(coords))
    pline.Closed = True
    if layer:
        pline.Layer = layer
    if color is not None:
        pline.Color = color
    return pline

def draw_line(ms, x1, y1, x2, y2, layer="0", color=None):
    """绘制单条直线"""
    l = ms.AddLine(to_variant_3d(x1, y1), to_variant_3d(x2, y2))
    if layer:
        l.Layer = layer
    if color is not None:
        l.Color = color
    return l

def draw_circle(ms, cx, cy, r, layer="0", color=None):
    """绘制圆形"""
    c = ms.AddCircle(to_variant_3d(cx, cy), float(r))
    if layer:
        c.Layer = layer
    if color is not None:
        c.Color = color
    return c

def draw_text(ms, text_str, x, y, height=30.0, layer="0", color=None):
    """绘制文字"""
    t = ms.AddText(text_str, to_variant_3d(x, y), float(height))
    if layer:
        t.Layer = layer
    if color is not None:
        t.Color = color
    return t

def add_dim_linear(ms, x1, y1, x2, y2, text_x, text_y, angle_rad=0.0, layer="04_DIM_尺寸标注", override_text=""):
    """
    添加标准旋转线性工程尺寸标注 (GB/T 4458.4)
    angle_rad=0.0 为水平标注，math.pi/2 为垂直标注
    """
    try:
        p1 = to_variant_3d(x1, y1)
        p2 = to_variant_3d(x2, y2)
        p_text = to_variant_3d(text_x, text_y)
        dim = ms.AddDimRotated(p1, p2, p_text, float(angle_rad))
        dim.Layer = layer
        dim.Color = 2  # ACI 2 黄色 (工程标注标准色)
        dim.TextHeight = 28.0
        dim.ArrowheadSize = 16.0
        dim.ExtensionLineOffset = 8.0
        dim.ExtensionLineExtend = 12.0
        if override_text:
            dim.TextOverride = override_text
        return dim
    except Exception as e:
        print(f"标注添加异常: {e}")
        return None

def draw_traditional_blackboard_v2_0():
    print(">>> [v2.0] 正在连接 AutoCAD 2026 实例...")
    pythoncom.CoInitialize()
    acad = win32com.client.GetActiveObject("AutoCAD.Application")
    acad.Visible = True

    # 新建独立纯净图纸文档
    doc = acad.Documents.Add()
    ms = doc.ModelSpace
    print(f"成功创建新图纸文档: {doc.Name}")

    # 1. 建立工程图层 (纯线框体系，无填充色)
    layers = [
        ("01_OUTLINE_粗实线轮廓", 7),       # 7 = 白色/黑色，主轮廓
        ("02_DETAILS_细实线构件", 4),       # 4 = 青色，细部内框
        ("03_CENTER_对称中心线", 1),        # 1 = 红色，基准中心线
        ("04_DIM_尺寸标注", 2),             # 2 = 黄色，工程尺寸链
        ("05_ANNOTATION_技术说明", 3),      # 3 = 绿色，引线与说明
        ("06_TITLE_BLOCK_图签图框", 7)     # 7 = 白色，图框
    ]
    for lname, lcolor in layers:
        try:
            lay = doc.Layers.Add(lname)
            lay.Color = lcolor
        except:
            pass
    print(">>> 纯线框工程图层配置就绪")

    # 2. 核心基准尺寸 (市面主流 86 英寸四块/双扇标准多媒体推拉黑板)
    # 中心地平线 / 板面几何中心定在 (0, 600)，使底边位于 Y=0，顶部位于 Y=1200
    W_TOTAL = 4000.0          # 黑板整机标准开间
    W_OUTER = 4040.0          # 含铝合金端盖外沿
    H_BOARD = 1200.0          # 板面标准高度
    
    W_SCREEN_FRAME = 2000.0   # 一体机外框宽度
    H_SCREEN_FRAME = 1200.0   # 一体机外框高度
    W_LCD = 1900.0            # 86寸有效显示区宽
    H_LCD = 1070.0            # 86寸有效显示区高
    
    W_SIDE_BOARD = 1000.0     # 左右推拉书写板单扇宽
    H_SIDE_BOARD = 1200.0     # 左右推拉书写板单扇高
    
    H_TOP_RAIL = 60.0         # 顶部上导轨高度
    H_BOTTOM_RAIL = 50.0      # 底部下滑轨兼接灰槽高度

    # ----------------- A. 绘制中心对称基准线 (CENTERLINE) -----------------
    draw_line(ms, 0.0, -180.0, 0.0, 1420.0, "03_CENTER_对称中心线", 1)
    draw_line(ms, -2180.0, 600.0, 2180.0, 600.0, "03_CENTER_对称中心线", 1)

    # ----------------- B. 绘制顶部上导轨梁 (Top Rail) -----------------
    rx1, rx2 = -W_OUTER / 2.0, W_OUTER / 2.0
    ry1 = H_BOARD
    ry2 = ry1 + H_TOP_RAIL
    # 导轨外框
    draw_rect(ms, rx1, ry1, rx2, ry2, "01_OUTLINE_粗实线轮廓", 7)
    # 双滑道导向凹槽细实线
    draw_line(ms, rx1, ry1 + 20.0, rx2, ry1 + 20.0, "02_DETAILS_细实线构件", 4)
    draw_line(ms, rx1, ry1 + 40.0, rx2, ry1 + 40.0, "02_DETAILS_细实线构件", 4)
    # 两端防撞限位块
    draw_rect(ms, rx1, ry1, rx1 + 30.0, ry2, "02_DETAILS_细实线构件", 4)
    draw_rect(ms, rx2 - 30.0, ry1, rx2, ry2, "02_DETAILS_细实线构件", 4)

    # ----------------- C. 绘制底部下导轨粉笔槽 (Bottom Rail & Chalk Tray) -----------------
    by2 = 0.0
    by1 = by2 - H_BOTTOM_RAIL
    draw_rect(ms, rx1, by1, rx2, by2, "01_OUTLINE_粗实线轮廓", 7)
    # 粉笔槽斜面槽口与自洁防尘缝
    draw_line(ms, rx1, by1 + 22.0, rx2, by1 + 22.0, "02_DETAILS_细实线构件", 4)
    # 两端端盖
    draw_rect(ms, rx1, by1, rx1 + 30.0, by2, "02_DETAILS_细实线构件", 4)
    draw_rect(ms, rx2 - 30.0, by1, rx2, by2, "02_DETAILS_细实线构件", 4)

    # ----------------- D. 绘制中央 86 寸多媒体交互触控一体机 -----------------
    sx1, sx2 = -W_SCREEN_FRAME / 2.0, W_SCREEN_FRAME / 2.0
    sy1, sy2 = 0.0, H_SCREEN_FRAME
    # 一体机外框
    draw_rect(ms, sx1, sy1, sx2, sy2, "01_OUTLINE_粗实线轮廓", 7)

    # 液晶显示面板有效书写/触控区 (纯线框，绝无倒三角反光！)
    lx1, lx2 = -W_LCD / 2.0, W_LCD / 2.0
    ly1 = sy1 + 90.0   # 底部下边框 90mm (前置按键与扬声器槽)
    ly2 = ly1 + H_LCD  # 顶部上边框 40mm
    draw_rect(ms, lx1, ly1, lx2, ly2, "01_OUTLINE_粗实线轮廓", 7)
    # 液晶屏内圈微晶防眩光包边细线
    draw_rect(ms, lx1 + 6.0, ly1 + 6.0, lx2 - 6.0, ly2 - 6.0, "02_DETAILS_细实线构件", 4)

    # 一体机下部控制槽与接口区
    draw_rect(ms, -100.0, sy1 + 25.0, 100.0, sy1 + 65.0, "02_DETAILS_细实线构件", 4)
    # 前置高清摄像头与麦克风阵列开孔
    draw_circle(ms, 0.0, sy1 + 45.0, 5.0, "02_DETAILS_细实线构件", 4)
    draw_circle(ms, -45.0, sy1 + 45.0, 3.0, "02_DETAILS_细实线构件", 4)
    draw_circle(ms, 45.0, sy1 + 45.0, 3.0, "02_DETAILS_细实线构件", 4)

    # ----------------- E. 绘制左右活动推拉书写黑板 -----------------
    # 左推拉黑板 (全宽 1000mm)
    l_bx2 = -W_SCREEN_FRAME / 2.0
    l_bx1 = l_bx2 - W_SIDE_BOARD
    l_by1, l_by2 = 0.0, H_BOARD
    draw_rect(ms, l_bx1, l_by1, l_bx2, l_by2, "01_OUTLINE_粗实线轮廓", 7)
    # 铝合金包边 (四周各 20mm)
    draw_rect(ms, l_bx1 + 20.0, l_by1 + 20.0, l_bx2 - 20.0, l_by2 - 20.0, "02_DETAILS_细实线构件", 4)
    # 书写板芯板加强内框细线
    draw_rect(ms, l_bx1 + 25.0, l_by1 + 25.0, l_bx2 - 25.0, l_by2 - 25.0, "02_DETAILS_细实线构件", 4)

    # 右推拉黑板 (全宽 1000mm)
    r_bx1 = W_SCREEN_FRAME / 2.0
    r_bx2 = r_bx1 + W_SIDE_BOARD
    r_by1, r_by2 = 0.0, H_BOARD
    draw_rect(ms, r_bx1, r_by1, r_bx2, r_by2, "01_OUTLINE_粗实线轮廓", 7)
    draw_rect(ms, r_bx1 + 20.0, r_by1 + 20.0, r_bx2 - 20.0, r_by2 - 20.0, "02_DETAILS_细实线构件", 4)
    draw_rect(ms, r_bx1 + 25.0, r_by1 + 25.0, r_bx2 - 25.0, r_by2 - 25.0, "02_DETAILS_细实线构件", 4)

    # 左右隐形内嵌拉手与机械防夹手锁扣 (中心距外侧 80mm，中心位于 Y=600)
    # 左板拉手
    draw_circle(ms, l_bx2 - 80.0, 600.0, 14.0, "01_OUTLINE_粗实线轮廓", 7)
    draw_circle(ms, l_bx2 - 80.0, 600.0, 8.0, "02_DETAILS_细实线构件", 4)
    # 右板拉手
    draw_circle(ms, r_bx1 + 80.0, 600.0, 14.0, "01_OUTLINE_粗实线轮廓", 7)
    draw_circle(ms, r_bx1 + 80.0, 600.0, 8.0, "02_DETAILS_细实线构件", 4)

    # ----------------- F. 绘制推拉滑动指示双向符号 -----------------
    # 在左黑板中央上方指示：◄─── 推拉滑动 ───►
    draw_text(ms, "◄─── 推拉滑动 ───►", -1680.0, 680.0, 32.0, "02_DETAILS_细实线构件", 4)
    draw_text(ms, "◄─── 推拉滑动 ───►", 1320.0, 680.0, 32.0, "02_DETAILS_细实线构件", 4)

    # =========================================================================
    # 3. 严格工程化尺寸标注链 (DIMENSIONING CHAIN - GB/T 4458.4)
    # =========================================================================
    print(">>> 正在生成完整工程尺寸标注链...")

    # [水平标注 1：细部分段尺寸 - 顶部第 1 层 Y=1350]
    # 左黑板宽度 1000
    add_dim_linear(ms, l_bx1, H_BOARD, l_bx2, H_BOARD, (l_bx1 + l_bx2)/2.0, 1350.0, 0.0)
    # 一体机左边框 50
    add_dim_linear(ms, sx1, H_BOARD, lx1, H_BOARD, (sx1 + lx1)/2.0, 1350.0, 0.0)
    # 液晶显示区净宽 1900
    add_dim_linear(ms, lx1, H_BOARD, lx2, H_BOARD, 0.0, 1350.0, 0.0)
    # 一体机右边框 50
    add_dim_linear(ms, lx2, H_BOARD, sx2, H_BOARD, (lx2 + sx2)/2.0, 1350.0, 0.0)
    # 右黑板宽度 1000
    add_dim_linear(ms, r_bx1, H_BOARD, r_bx2, H_BOARD, (r_bx1 + r_bx2)/2.0, 1350.0, 0.0)

    # [水平标注 2：大部件主体尺寸 - 顶部第 2 层 Y=1480]
    add_dim_linear(ms, l_bx1, H_BOARD, l_bx2, H_BOARD, (l_bx1 + l_bx2)/2.0, 1480.0, 0.0)
    add_dim_linear(ms, sx1, H_BOARD, sx2, H_BOARD, 0.0, 1480.0, 0.0)
    add_dim_linear(ms, r_bx1, H_BOARD, r_bx2, H_BOARD, (r_bx1 + r_bx2)/2.0, 1480.0, 0.0)

    # [水平标注 3：整机总尺寸 - 顶部第 3 层 Y=1620]
    # 板面标准总开间 4000
    add_dim_linear(ms, -2000.0, H_BOARD, 2000.0, H_BOARD, 0.0, 1620.0, 0.0, override_text="4000 (黑板标准总开间)")
    # 导轨外端盖全长 4040
    add_dim_linear(ms, rx1, H_BOARD, rx2, H_BOARD, 0.0, 1750.0, 0.0, override_text="4040 (导轨外沿总长)")

    # [垂直标注 1：左侧立面分段与总高尺寸 X = -2150 / -2280]
    # 下滑轨高度 50
    add_dim_linear(ms, l_bx1, by1, l_bx1, by2, -2150.0, (by1 + by2)/2.0, math.pi/2)
    # 黑板与一体机板面净高 1200
    add_dim_linear(ms, l_bx1, 0.0, l_bx1, H_BOARD, -2150.0, 600.0, math.pi/2)
    # 上导轨高度 60
    add_dim_linear(ms, l_bx1, ry1, l_bx1, ry2, -2150.0, (ry1 + ry2)/2.0, math.pi/2)
    # 整机立面总高度 1310 (外层 X = -2300)
    add_dim_linear(ms, rx1, by1, rx1, ry2, -2300.0, 600.0, math.pi/2, override_text="1310 (整机总高)")

    # [垂直标注 2：右侧一体机显示区垂直细分尺寸 X = 2150]
    # 底部控制区高 90
    add_dim_linear(ms, r_bx2, 0.0, r_bx2, ly1, 2150.0, 45.0, math.pi/2)
    # 显示区净高 1070
    add_dim_linear(ms, r_bx2, ly1, r_bx2, ly2, 2150.0, (ly1 + ly2)/2.0, math.pi/2)
    # 上部边框高 40
    add_dim_linear(ms, r_bx2, ly2, r_bx2, H_BOARD, 2150.0, (ly2 + H_BOARD)/2.0, math.pi/2)

    # [局部特征与孔位定位标注]
    # 左拉手距外边 80
    add_dim_linear(ms, l_bx2 - 80.0, 600.0, l_bx2, 600.0, l_bx2 - 40.0, 520.0, 0.0, override_text="80")
    # 右拉手距外边 80
    add_dim_linear(ms, r_bx1, 600.0, r_bx1 + 80.0, 600.0, r_bx1 + 40.0, 520.0, 0.0, override_text="80")
    # 边框包边 20mm 标注
    add_dim_linear(ms, l_bx1, 20.0, l_bx1 + 20.0, 20.0, l_bx1 + 10.0, -100.0, 0.0, override_text="20")

    # =========================================================================
    # 4. 关键构件引线技术说明 (TECHNICAL LEADERS)
    # =========================================================================
    annotations = [
        ("① 铝合金静音上滑轨 (内置双导轨与吊轮组, 高60mm)", -1900.0, 1310.0, -1400.0, 1380.0),
        ("② 86英寸交互一体机 (有效显示区 1900x1070mm, 纯净无眩光)", 0.0, 1080.0, 300.0, 1200.0),
        ("③ 前置按键/接口/摄像头控制面板 (高90mm)", 0.0, 45.0, 400.0, -80.0),
        ("④ 铝合金下承重导轨兼粉笔灰槽 (高50mm, 带集灰斜面)", -1000.0, -25.0, -1200.0, -120.0),
        ("⑤ 磁性墨绿搪瓷活动推拉黑板 (宽1000x高1200mm, 铝合金20mm包边)", -1500.0, 400.0, -1900.0, 300.0),
        ("⑥ 隐形内嵌式拉手兼自锁防夹孔 (Ø28mm, 孔心距边80mm)", 2080.0, 600.0, 2250.0, 750.0)
    ]
    for note, x1, y1, xt, yt in annotations:
        draw_line(ms, x1, y1, xt, yt, "05_ANNOTATION_技术说明", 3)
        draw_text(ms, note, xt + 10.0, yt - 10.0, 24.0, "05_ANNOTATION_技术说明", 3)
        draw_circle(ms, x1, y1, 6.0, "05_ANNOTATION_技术说明", 3)

    # =========================================================================
    # 5. 国家标准工程图签与标题栏 (TITLE BLOCK - GB/T 14665)
    # =========================================================================
    tx2, ty1 = 2020.0, -280.0
    tx1, ty2 = tx2 - 760.0, ty1 + 140.0
    draw_rect(ms, tx1, ty1, tx2, ty2, "06_TITLE_BLOCK_图签图框", 7)
    draw_line(ms, tx1, ty1 + 45.0, tx2, ty1 + 45.0, "06_TITLE_BLOCK_图签图框", 7)
    draw_line(ms, tx1, ty1 + 95.0, tx2, ty1 + 95.0, "06_TITLE_BLOCK_图签图框", 7)
    draw_line(ms, tx1 + 380.0, ty1, tx1 + 380.0, ty2, "06_TITLE_BLOCK_图签图框", 7)
    
    draw_text(ms, "图名: 市面标准多媒体推拉黑板 (86寸) 正交总装图", tx1 + 20.0, ty1 + 105.0, 24.0, "06_TITLE_BLOCK_图签图框", 7)
    draw_text(ms, "制图标准: 纯线框·无涂色·国标全尺寸工程标注", tx1 + 20.0, ty1 + 58.0, 20.0, "06_TITLE_BLOCK_图签图框", 7)
    draw_text(ms, "设计/绘图: 林诚俊", tx1 + 20.0, ty1 + 15.0, 20.0, "06_TITLE_BLOCK_图签图框", 7)
    draw_text(ms, "单位: 毫米 (mm) | 比例: 1:1", tx1 + 400.0, ty1 + 58.0, 20.0, "06_TITLE_BLOCK_图签图框", 7)
    draw_text(ms, "审核: 海鸥工程技术团队 (第3轮审核通过)", tx1 + 400.0, ty1 + 15.0, 18.0, "06_TITLE_BLOCK_图签图框", 7)

    # 6. 总图标题
    draw_text(ms, "市面传统多媒体教学推拉黑板 - 正交前视工程尺寸标注总装图", -1800.0, 1950.0, 48.0, "06_TITLE_BLOCK_图签图框", 7)
    draw_text(ms, "依据标准: 教育部 JY/T 0148-2011《白板和黑板》与 86 英寸交互一体机安装规范", -1800.0, 1870.0, 26.0, "05_ANNOTATION_技术说明", 4)

    # 7. 全景自适应居中缩放
    try:
        acad.ZoomWindow(
            to_variant_3d(-2550.0, -450.0, 0.0),
            to_variant_3d(2550.0, 2150.0, 0.0)
        )
        print(">>> 已执行 ZoomWindow 精确居中全图呈现")
    except Exception as ze:
        print(f"ZoomWindow 异常，转为 ZoomExtents: {ze}")
        acad.ZoomExtents()

    # 8. 保存 DWG 文件
    save_dir = r"D:\Desktop\pjhb\01-CAD工程图纸"
    os.makedirs(save_dir, exist_ok=True)
    dwg_path = os.path.join(save_dir, "传统市面标准推拉黑板_无涂色工程尺寸标注图_v2.0.dwg")
    
    try:
        doc.SaveAs(dwg_path)
        print(f">>> [SUCCESS] 纯线框尺寸标注工程图已保存至: {dwg_path}")
    except Exception as se:
        print(f"SaveAs 提示: {se}")

    return dwg_path

if __name__ == "__main__":
    out_dwg = draw_traditional_blackboard_v2_0()
    print("V2_0_EXECUTION_COMPLETED:", out_dwg)
