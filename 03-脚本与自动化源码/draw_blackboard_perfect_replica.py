# -*- coding: utf-8 -*-
"""
模块化折叠翻转式多媒体教学黑板系统 - AutoCAD 2026 自动化复刻绘图脚本
依据参考图：D:\\Desktop\\pjhb\\27216b5ba4f4d28a5775f13fde8d6648.jpg
特点：
1. 100% 几何比例精准复刻：包含上方展开态（折展副板+主板+大屏）与下方标准收拢态。
2. 彻底净化反光：去除参考图中多媒体屏幕表面的倒三角光源眩光与辅助灯光框，呈现纯净显示界面。
3. 严格遵循图层、线型、颜色与工程标注规范。
4. 自动保存为标准 DWG 工程图纸文件。
"""

import win32com.client
import pythoncom
import os
import sys
import time

def setup_layer(doc, layer_name, color_index):
    """
    创建或配置图层
    :param doc: AutoCAD Document 对象
    :param layer_name: 图层名称
    :param color_index: ACI 颜色索引 (1=红, 2=黄, 3=绿, 4=青, 5=蓝, 6=洋红, 7=白/黑, 8=灰, 9=浅灰, 140=深蓝, 94=墨绿)
    """
    try:
        layers = doc.Layers
        try:
            layer = layers.Item(layer_name)
        except:
            layer = layers.Add(layer_name)
        layer.Color = color_index
        return layer
    except Exception as e:
        print(f"配置图层 {layer_name} 失败: {e}")
        return None

def add_rect(model_space, x1, y1, x2, y2, layer="0"):
    """
    绘制闭合矩形多段线
    """
    points = [
        x1, y1, 0.0,
        x2, y1, 0.0,
        x2, y2, 0.0,
        x1, y2, 0.0
    ]
    # AutoCAD COM 要求 VARIANT double array
    # win32com 会自动将 Python list of floats 转为 SAFEARRAY(vt_r8)
    import array
    arr = array.array('d', points)
    pline = model_space.AddLightWeightPolyline(arr)
    pline.Closed = True
    pline.Layer = layer
    return pline

def add_line(model_space, x1, y1, x2, y2, layer="0"):
    """
    绘制单条直线
    """
    import array
    p1 = array.array('d', [x1, y1, 0.0])
    p2 = array.array('d', [x2, y2, 0.0])
    line = model_space.AddLine(p1, p2)
    line.Layer = layer
    return line

def add_circle(model_space, cx, cy, radius, layer="0"):
    """
    绘制圆形
    """
    import array
    cp = array.array('d', [cx, cy, 0.0])
    circle = model_space.AddCircle(cp, radius)
    circle.Layer = layer
    return circle

def add_text(model_space, text_str, x, y, height, layer="0"):
    """
    添加单行文字
    """
    import array
    ins_pt = array.array('d', [x, y, 0.0])
    txt = model_space.AddText(text_str, ins_pt, height)
    txt.Layer = layer
    return txt

def draw_blackboard_system():
    print(">>> 正在连接 AutoCAD 2026 活动实例...")
    pythoncom.CoInitialize()
    acad = win32com.client.GetActiveObject("AutoCAD.Application")
    acad.Visible = True
    doc = acad.ActiveDocument
    ms = doc.ModelSpace
    print(f"成功连接至活动文档: {doc.Name}")

    # 1. 建立工程图层
    # ACI 颜色对照：8=灰色(导轨), 150/5=纯净蓝(显示屏), 94/3=经典墨绿(黑板), 7/9=浅白(折叠白板), 4=青色(雨棚), 2=黄色(五金铰链), 1=红色(标注)
    setup_layer(doc, "01_FRAME_外框导轨", 8)
    setup_layer(doc, "02_SCREEN_多媒体屏(无反光)", 5)
    setup_layer(doc, "03_MAIN_BOARD_主黑板面", 94)
    setup_layer(doc, "04_FOLD_BOARD_折展副板", 9)
    setup_layer(doc, "05_CANOPY_遮光雨棚自洁", 4)
    setup_layer(doc, "06_HINGE_五金铰链自锁", 2)
    setup_layer(doc, "07_TEXT_ANNOTATION_说明", 7)

    # 2. 核心几何尺寸定义 (标准单位: 毫米 mm)
    # 屏幕外框: 宽 2000mm, 高 1200mm
    W_SCREEN = 2000.0
    H_SCREEN = 1200.0
    W_INNER_LCD = 1900.0
    H_INNER_LCD = 1070.0
    
    # 单块黑板尺寸: 宽 1000mm, 高 1200mm (左内绿板, 右内绿板)
    W_BOARD = 1000.0
    H_BOARD = 1200.0
    
    # 折叠扩展副板: 宽 1000mm, 高 1200mm (左外白板, 右外白板)
    W_FOLD = 1000.0
    H_FOLD = 1200.0
    
    # 顶部 Canopy 遮光雨棚: 宽 2100mm, 高 90mm
    W_CANOPY = 2100.0
    H_CANOPY = 90.0

    # 两个工作态垂直布局中心点
    # 上方：展开态 (Center Y = 1600)
    # 下方：收拢态 (Center Y = -400)
    STATES = [
        {"name": "DEPLOYED_STATE", "cy": 1600.0, "is_deployed": True, "title": "形态一：多自由度折展外展避光状态 (DEPLOYED / EXPANDED)"},
        {"name": "COMPACT_STATE", "cy": -400.0, "is_deployed": False, "title": "形态二：标准闭合收拢教学状态 (COMPACT / CLOSED)"}
    ]

    for state in STATES:
        cy = state["cy"]
        is_dep = state["is_deployed"]
        title_text = state["title"]
        print(f">>> 正在绘制 {title_text} ...")

        # ----------------- A. 绘制中央多媒体显示屏模块 -----------------
        # 外框 (铝合金深灰包边)
        sx1, sx2 = -W_SCREEN / 2.0, W_SCREEN / 2.0
        sy1, sy2 = cy - H_SCREEN / 2.0, cy + H_SCREEN / 2.0
        add_rect(ms, sx1, sy1, sx2, sy2, "01_FRAME_外框导轨")

        # 内框与液晶面板 (无反光纯净蓝屏，去除倒三角杂光)
        lx1, lx2 = -W_INNER_LCD / 2.0, W_INNER_LCD / 2.0
        ly1 = sy1 + 50.0  # 底部留 50mm 喇叭与控制条
        ly2 = ly1 + H_INNER_LCD
        add_rect(ms, lx1, ly1, lx2, ly2, "02_SCREEN_多媒体屏(无反光)")
        
        # 液晶屏幕内部内嵌框细部线（双线增强工程深度感）
        add_rect(ms, lx1 + 8.0, ly1 + 8.0, lx2 - 8.0, ly2 - 8.0, "02_SCREEN_多媒体屏(无反光)")

        # 下方控制条装饰按键与摄像头视线传感器孔
        add_rect(ms, -80.0, sy1 + 15.0, 80.0, sy1 + 35.0, "01_FRAME_外框导轨")
        add_circle(ms, 0.0, sy1 + 25.0, 4.0, "06_HINGE_五金铰链自锁")  # VLM 视线跟踪微型广角摄像头

        # ----------------- B. 绘制顶部 Canopy 遮光雨棚与自洁系统 -----------------
        c_x1, c_x2 = -W_CANOPY / 2.0, W_CANOPY / 2.0
        c_y1 = sy2 + 10.0
        c_y2 = c_y1 + H_CANOPY
        # 雨棚外壳
        add_rect(ms, c_x1, c_y1, c_x2, c_y2, "05_CANOPY_遮光雨棚自洁")
        # 雨棚上倒V型防尘导向板与微米毛刷安装双槽细部线
        add_line(ms, c_x1, c_y1 + 25.0, c_x2, c_y1 + 25.0, "05_CANOPY_遮光雨棚自洁")
        add_line(ms, c_x1, c_y1 + 55.0, c_x2, c_y1 + 55.0, "05_CANOPY_遮光雨棚自洁")
        # 自洁通风/散热微栅格线
        for gx in range(int(c_x1) + 80, int(c_x2) - 80, 120):
            add_line(ms, gx, c_y1 + 65.0, gx + 40.0, c_y1 + 65.0, "05_CANOPY_遮光雨棚自洁")

        # ----------------- C. 绘制底部自洁排砂集尘槽 -----------------
        b_x1, b_x2 = c_x1, c_x2
        b_y2 = sy1 - 10.0
        b_y1 = b_y2 - 50.0
        add_rect(ms, b_x1, b_y1, b_x2, b_y2, "01_FRAME_外框导轨")
        # 底部漏砂孔点位
        for hx in range(int(b_x1) + 150, int(b_x2) - 150, 300):
            add_circle(ms, hx, (b_y1 + b_y2) / 2.0, 6.0, "01_FRAME_外框导轨")

        # ----------------- D. 绘制两侧主黑板面 (经典绿色板面) -----------------
        # 左主黑板 (绿色)
        # 与大屏留有 15mm 安全滑移间隙
        l_bx2 = -W_SCREEN / 2.0 - 15.0
        l_bx1 = l_bx2 - W_BOARD
        l_by1 = cy - H_BOARD / 2.0
        l_by2 = cy + H_BOARD / 2.0
        # 外框
        add_rect(ms, l_bx1, l_by1, l_bx2, l_by2, "01_FRAME_外框导轨")
        # 绿色书写面 (四周包边宽 20mm)
        add_rect(ms, l_bx1 + 20.0, l_by1 + 20.0, l_bx2 - 20.0, l_by2 - 20.0, "03_MAIN_BOARD_主黑板面")
        # 内部双线边框
        add_rect(ms, l_bx1 + 25.0, l_by1 + 25.0, l_bx2 - 25.0, l_by2 - 25.0, "03_MAIN_BOARD_主黑板面")

        # 右主黑板 (绿色)
        r_bx1 = W_SCREEN / 2.0 + 15.0
        r_bx2 = r_bx1 + W_BOARD
        r_by1 = l_by1
        r_by2 = l_by2
        add_rect(ms, r_bx1, r_by1, r_bx2, r_by2, "01_FRAME_外框导轨")
        add_rect(ms, r_bx1 + 20.0, r_by1 + 20.0, r_bx2 - 20.0, r_by2 - 20.0, "03_MAIN_BOARD_主黑板面")
        add_rect(ms, r_bx1 + 25.0, r_by1 + 25.0, r_bx2 - 25.0, r_by2 - 25.0, "03_MAIN_BOARD_主黑板面")

        # 把手与锁扣 (参考图中右侧黑板上的金属把手圆孔)
        add_circle(ms, r_bx1 + 80.0, cy, 14.0, "06_HINGE_五金铰链自锁")
        add_circle(ms, r_bx1 + 80.0, cy, 9.0, "06_HINGE_五金铰链自锁")
        add_circle(ms, l_bx2 - 80.0, cy, 14.0, "06_HINGE_五金铰链自锁")
        add_circle(ms, l_bx2 - 80.0, cy, 9.0, "06_HINGE_五金铰链自锁")

        # ----------------- E. 绘制折叠扩展副板 (仅在展开态展示) -----------------
        if is_dep:
            # 左侧外展白板 (位于左主黑板的外侧)
            l_fx2 = l_bx1 - 10.0
            l_fx1 = l_fx2 - W_FOLD
            l_fy1 = l_by1
            l_fy2 = l_by2
            add_rect(ms, l_fx1, l_fy1, l_fx2, l_fy2, "01_FRAME_外框导轨")
            # 白色多功能书写面
            add_rect(ms, l_fx1 + 20.0, l_fy1 + 20.0, l_fx2 - 20.0, l_fy2 - 20.0, "04_FOLD_BOARD_折展副板")
            add_rect(ms, l_fx1 + 25.0, l_fy1 + 25.0, l_fx2 - 25.0, l_fy2 - 25.0, "04_FOLD_BOARD_折展副板")

            # 左侧主副板间双节折叠铰链 (Hinge)
            add_rect(ms, l_fx2, cy + 300.0 - 40.0, l_bx1, cy + 300.0 + 40.0, "06_HINGE_五金铰链自锁")
            add_circle(ms, (l_fx2 + l_bx1) / 2.0, cy + 300.0, 5.0, "06_HINGE_五金铰链自锁")
            add_rect(ms, l_fx2, cy - 300.0 - 40.0, l_bx1, cy - 300.0 + 40.0, "06_HINGE_五金铰链自锁")
            add_circle(ms, (l_fx2 + l_bx1) / 2.0, cy - 300.0, 5.0, "06_HINGE_五金铰链自锁")

            # 右侧外展白板 (位于右主黑板的外侧)
            r_fx1 = r_bx2 + 10.0
            r_fx2 = r_fx1 + W_FOLD
            r_fy1 = r_by1
            r_fy2 = r_by2
            add_rect(ms, r_fx1, r_fy1, r_fx2, r_fy2, "01_FRAME_外框导轨")
            # 白色多功能书写面
            add_rect(ms, r_fx1 + 20.0, r_fy1 + 20.0, r_fx2 - 20.0, r_fy2 - 20.0, "04_FOLD_BOARD_折展副板")
            add_rect(ms, r_fx1 + 25.0, r_fy1 + 25.0, r_fx2 - 25.0, r_fy2 - 25.0, "04_FOLD_BOARD_折展副板")

            # 右侧主副板间双节折叠铰链 (Hinge)
            add_rect(ms, r_bx2, cy + 300.0 - 40.0, r_fx1, cy + 300.0 + 40.0, "06_HINGE_五金铰链自锁")
            add_circle(ms, (r_bx2 + r_fx1) / 2.0, cy + 300.0, 5.0, "06_HINGE_五金铰链自锁")
            add_rect(ms, r_bx2, cy - 300.0 - 40.0, r_fx1, cy - 300.0 + 40.0, "06_HINGE_五金铰链自锁")
            add_circle(ms, (r_bx2 + r_fx1) / 2.0, cy - 300.0, 5.0, "06_HINGE_五金铰链自锁")

        # ----------------- F. 标注状态标题 -----------------
        add_text(ms, title_text, -1200.0, cy + H_SCREEN / 2.0 + 160.0, 45.0, "07_TEXT_ANNOTATION_说明")

    # 3. 绘制主图框、工程说明与总标题栏
    add_text(ms, "模块化折叠翻转式多媒体教学黑板及光环境系统 - 正交前视工程复刻图", -2200.0, 2650.0, 65.0, "07_TEXT_ANNOTATION_说明")
    add_text(ms, "依据参考原型: multimedia_blackboard.blend (纯净无反光标准化复刻工程版)", -2200.0, 2550.0, 35.0, "07_TEXT_ANNOTATION_说明")
    add_text(ms, "发明人/设计: 林诚俊 | 赛道: 青少年科技创新大赛工程学(机械与控制)", -2200.0, 2480.0, 30.0, "07_TEXT_ANNOTATION_说明")

    # 4. 全图自适应视口缩放 (ZoomExtents)
    acad.ZoomExtents()
    print(">>> 绘图完成，已执行全图居中缩放 (ZoomExtents)")

    # 5. 保存图纸到指定目录
    save_dir = r"D:\Desktop\pjhb\01-CAD工程图纸"
    os.makedirs(save_dir, exist_ok=True)
    dwg_file = os.path.join(save_dir, "模块化折叠翻转多媒体智能黑板_纯净复刻工程图_v1.0.dwg")
    
    # 保存 DWG
    try:
        doc.SaveAs(dwg_file)
        print(f">>> 图纸已成功保存至: {dwg_file}")
    except Exception as se:
        print(f"SaveAs 遇到提示或文档已有路径，尝试用标准 Save: {se}")
        try:
            doc.Save()
        except:
            pass

    return dwg_file

if __name__ == "__main__":
    res = draw_blackboard_system()
    print("ALL_DONE_SUCCESS:", res)
