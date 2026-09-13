# -*- coding: utf-8 -*-
"""
模块化折叠翻转式多媒体教学黑板系统 - AutoCAD 2026 自动化复刻绘图脚本 (v1.2)
文件版本: v1.2
修改说明:
1. 修正 create_layer 单参数调用规范，颜色通过实体层级传递。
2. 严格按 CAD-MCP 模块签名调用 draw_line, draw_circle, draw_text 与 draw_polyline。
3. 确保 100% 纯净无反光：去除参考图中多媒体屏幕倒三角反光阴影，还原平整高质感液晶面板。
4. 绘制完成后执行 ZoomExtents 并保存 DWG 工程文件至 01-CAD工程图纸 目录。
"""

import sys
import os
import win32com.client
import pythoncom

# 引用 CAD-MCP 服务目录
sys.path.append(r"D:\mcp-servers\CAD-MCP\src")
from cad_controller import CADController

def draw_rect(ctrl, x1, y1, x2, y2, layer=None, color=None, lineweight=None):
    """绘制闭合矩形"""
    pts = [
        (float(x1), float(y1), 0.0),
        (float(x2), float(y1), 0.0),
        (float(x2), float(y2), 0.0),
        (float(x1), float(y2), 0.0),
        (float(x1), float(y1), 0.0)
    ]
    return ctrl.draw_polyline(pts, closed=True, layer=layer, color=color, lineweight=lineweight)

def draw_blackboard_full_replica():
    print(">>> [v1.2] 正在连接 AutoCAD 2026 控制器...")
    ctrl = CADController()
    
    # 连接当前正在运行的 AutoCAD 实例
    pythoncom.CoInitialize()
    acad = win32com.client.GetActiveObject("AutoCAD.Application")
    acad.Visible = True
    ctrl.app = acad
    ctrl.doc = acad.ActiveDocument
    print(f"成功连接至活动图纸: {ctrl.doc.Name}")

    # 1. 创建规范工程图层
    layers = [
        "01_FRAME_外框导轨",
        "02_SCREEN_多媒体屏_纯净无反光",
        "03_MAIN_BOARD_主黑板面",
        "04_FOLD_BOARD_折展副板",
        "05_CANOPY_遮光雨棚自洁",
        "06_HINGE_五金铰链自锁",
        "07_TEXT_ANNOTATION_说明"
    ]
    for lname in layers:
        ctrl.create_layer(lname)
    print(">>> 图层初始化完成")

    # 2. 颜色配置 (ACI 标准色: 1=红, 2=黄, 3=绿, 4=青, 5=蓝, 6=洋红, 7=白, 8=灰, 9=浅灰, 94=墨绿, 140=中蓝)
    C_FRAME = 8       # 边框导轨: 灰色
    C_SCREEN = 5      # 屏幕面板: 纯净蓝 (绝对无反光)
    C_GREEN = 94      # 主板黑板面: 墨绿
    C_WHITE = 9       # 副板折叠面: 象牙浅灰/白
    C_CANOPY = 4      # 雨棚: 青色冷灰
    C_HINGE = 2       # 五金锁扣: 金黄
    C_TEXT = 7        # 文字说明: 白色

    # 3. 核心工程尺寸 (单位: 毫米 mm，以真实 86 寸智能黑板工业规格 1:1 标准绘制)
    W_SCREEN = 2000.0
    H_SCREEN = 1200.0
    W_INNER_LCD = 1900.0
    H_INNER_LCD = 1070.0
    
    W_BOARD = 1000.0
    H_BOARD = 1200.0
    
    W_FOLD = 1000.0
    H_FOLD = 1200.0
    
    W_CANOPY = 2120.0
    H_CANOPY = 90.0

    # 状态定义 (上下双工作态展示)
    states = [
        {
            "name": "DEPLOYED",
            "cy": 1600.0,
            "is_deployed": True,
            "title": "形态一：多自由度折展外展避光状态 (DEPLOYED / EXPANDED)",
            "subtitle": "特点：两侧黑板双节外展展开，大屏178度超广视场无死角，表面纯净无直射眩光"
        },
        {
            "name": "COMPACT",
            "cy": -400.0,
            "is_deployed": False,
            "title": "形态二：标准闭合收拢教学状态 (COMPACT / CLOSED)",
            "subtitle": "特点：副板隐形内嵌收纳，两侧经典绿板归位，适用于常规大屏与板书融合教学"
        }
    ]

    for st in states:
        cy = st["cy"]
        is_dep = st["is_deployed"]
        title_text = st["title"]
        sub_text = st["subtitle"]
        print(f">>> 正在精确绘制: {title_text} ...")

        # ----------------- A. 中央多媒体显示屏模块 -----------------
        sx1, sx2 = -W_SCREEN / 2.0, W_SCREEN / 2.0
        sy1, sy2 = cy - H_SCREEN / 2.0, cy + H_SCREEN / 2.0
        # 外框
        draw_rect(ctrl, sx1, sy1, sx2, sy2, layer="01_FRAME_外框导轨", color=C_FRAME)

        # 液晶屏幕 (纯净无反光蓝，去除倒三角杂光)
        lx1, lx2 = -W_INNER_LCD / 2.0, W_INNER_LCD / 2.0
        ly1 = sy1 + 50.0  # 底部留 50mm 音响按键条
        ly2 = ly1 + H_INNER_LCD
        draw_rect(ctrl, lx1, ly1, lx2, ly2, layer="02_SCREEN_多媒体屏_纯净无反光", color=C_SCREEN)
        draw_rect(ctrl, lx1 + 8.0, ly1 + 8.0, lx2 - 8.0, ly2 - 8.0, layer="02_SCREEN_多媒体屏_纯净无反光", color=C_SCREEN)

        # 底部中央控制面板与 VLM 视线跟踪探针
        draw_rect(ctrl, -90.0, sy1 + 15.0, 90.0, sy1 + 35.0, layer="01_FRAME_外框导轨", color=C_FRAME)
        ctrl.draw_circle((0.0, sy1 + 25.0, 0.0), 4.5, layer="06_HINGE_五金铰链自锁", color=C_HINGE)

        # ----------------- B. 顶部 Canopy 遮光雨棚自洁防尘系统 -----------------
        c_x1, c_x2 = -W_CANOPY / 2.0, W_CANOPY / 2.0
        c_y1 = sy2 + 10.0
        c_y2 = c_y1 + H_CANOPY
        draw_rect(ctrl, c_x1, c_y1, c_x2, c_y2, layer="05_CANOPY_遮光雨棚自洁", color=C_CANOPY)
        # 防尘倒V导向与微米毛刷条结构槽
        ctrl.draw_line((c_x1, c_y1 + 28.0, 0.0), (c_x2, c_y1 + 28.0, 0.0), layer="05_CANOPY_遮光雨棚自洁", color=C_CANOPY)
        ctrl.draw_line((c_x1, c_y1 + 58.0, 0.0), (c_x2, c_y1 + 58.0, 0.0), layer="05_CANOPY_遮光雨棚自洁", color=C_CANOPY)
        # 顶部防尘导流散热格栅条
        for gx in range(int(c_x1) + 100, int(c_x2) - 100, 150):
            ctrl.draw_line((float(gx), c_y1 + 68.0, 0.0), (float(gx) + 50.0, c_y1 + 68.0, 0.0), layer="05_CANOPY_遮光雨棚自洁", color=C_CANOPY)

        # ----------------- C. 底部自洁排砂集尘导轨 -----------------
        b_x1, b_x2 = c_x1, c_x2
        b_y2 = sy1 - 10.0
        b_y1 = b_y2 - 50.0
        draw_rect(ctrl, b_x1, b_y1, b_x2, b_y2, layer="01_FRAME_外框导轨", color=C_FRAME)
        for hx in range(int(b_x1) + 150, int(b_x2) - 150, 300):
            ctrl.draw_circle((float(hx), (b_y1 + b_y2) / 2.0, 0.0), 6.0, layer="01_FRAME_外框导轨", color=C_FRAME)

        # ----------------- D. 两侧主黑板 (墨绿色板面) -----------------
        # 左侧主黑板
        l_bx2 = -W_SCREEN / 2.0 - 15.0
        l_bx1 = l_bx2 - W_BOARD
        l_by1 = cy - H_BOARD / 2.0
        l_by2 = cy + H_BOARD / 2.0
        draw_rect(ctrl, l_bx1, l_by1, l_bx2, l_by2, layer="01_FRAME_外框导轨", color=C_FRAME)
        draw_rect(ctrl, l_bx1 + 20.0, l_by1 + 20.0, l_bx2 - 20.0, l_by2 - 20.0, layer="03_MAIN_BOARD_主黑板面", color=C_GREEN)
        draw_rect(ctrl, l_bx1 + 25.0, l_by1 + 25.0, l_bx2 - 25.0, l_by2 - 25.0, layer="03_MAIN_BOARD_主黑板面", color=C_GREEN)

        # 右侧主黑板
        r_bx1 = W_SCREEN / 2.0 + 15.0
        r_bx2 = r_bx1 + W_BOARD
        r_by1 = l_by1
        r_by2 = l_by2
        draw_rect(ctrl, r_bx1, r_by1, r_bx2, r_by2, layer="01_FRAME_外框导轨", color=C_FRAME)
        draw_rect(ctrl, r_bx1 + 20.0, r_by1 + 20.0, r_bx2 - 20.0, r_by2 - 20.0, layer="03_MAIN_BOARD_主黑板面", color=C_GREEN)
        draw_rect(ctrl, r_bx1 + 25.0, r_by1 + 25.0, r_bx2 - 25.0, r_by2 - 25.0, layer="03_MAIN_BOARD_主黑板面", color=C_GREEN)

        # 金属拉手与自锁孔位
        ctrl.draw_circle((r_bx1 + 80.0, cy, 0.0), 14.0, layer="06_HINGE_五金铰链自锁", color=C_HINGE)
        ctrl.draw_circle((r_bx1 + 80.0, cy, 0.0), 8.0, layer="06_HINGE_五金铰链自锁", color=C_HINGE)
        ctrl.draw_circle((l_bx2 - 80.0, cy, 0.0), 14.0, layer="06_HINGE_五金铰链自锁", color=C_HINGE)
        ctrl.draw_circle((l_bx2 - 80.0, cy, 0.0), 8.0, layer="06_HINGE_五金铰链自锁", color=C_HINGE)

        # ----------------- E. 折叠扩展副板 (仅展开态展示) -----------------
        if is_dep:
            # 左外侧白板 (折展多功能板)
            l_fx2 = l_bx1 - 12.0
            l_fx1 = l_fx2 - W_FOLD
            l_fy1 = l_by1
            l_fy2 = l_by2
            draw_rect(ctrl, l_fx1, l_fy1, l_fx2, l_fy2, layer="01_FRAME_外框导轨", color=C_FRAME)
            draw_rect(ctrl, l_fx1 + 20.0, l_fy1 + 20.0, l_fx2 - 20.0, l_fy2 - 20.0, layer="04_FOLD_BOARD_折展副板", color=C_WHITE)
            draw_rect(ctrl, l_fx1 + 25.0, l_fy1 + 25.0, l_fx2 - 25.0, l_fy2 - 25.0, layer="04_FOLD_BOARD_折展副板", color=C_WHITE)

            # 左侧双节阻尼自锁铰链
            for hy in [cy + 350.0, cy - 350.0]:
                draw_rect(ctrl, l_fx2, hy - 35.0, l_bx1, hy + 35.0, layer="06_HINGE_五金铰链自锁", color=C_HINGE)
                ctrl.draw_circle(((l_fx2 + l_bx1) / 2.0, hy, 0.0), 5.0, layer="06_HINGE_五金铰链自锁", color=C_HINGE)

            # 右外侧白板 (折展多功能板)
            r_fx1 = r_bx2 + 12.0
            r_fx2 = r_fx1 + W_FOLD
            r_fy1 = r_by1
            r_fy2 = r_by2
            draw_rect(ctrl, r_fx1, r_fy1, r_fx2, r_fy2, layer="01_FRAME_外框导轨", color=C_FRAME)
            draw_rect(ctrl, r_fx1 + 20.0, r_fy1 + 20.0, r_fx2 - 20.0, r_fy2 - 20.0, layer="04_FOLD_BOARD_折展副板", color=C_WHITE)
            draw_rect(ctrl, r_fx1 + 25.0, r_fy1 + 25.0, r_fx2 - 25.0, r_fy2 - 25.0, layer="04_FOLD_BOARD_折展副板", color=C_WHITE)

            # 右侧双节阻尼自锁铰链
            for hy in [cy + 350.0, cy - 350.0]:
                draw_rect(ctrl, r_bx2, hy - 35.0, r_fx1, hy + 35.0, layer="06_HINGE_五金铰链自锁", color=C_HINGE)
                ctrl.draw_circle(((r_bx2 + r_fx1) / 2.0, hy, 0.0), 5.0, layer="06_HINGE_五金铰链自锁", color=C_HINGE)

        # ----------------- F. 标注状态说明 -----------------
        ctrl.draw_text((-1400.0, cy + H_SCREEN / 2.0 + 150.0, 0.0), title_text, height=45.0, layer="07_TEXT_ANNOTATION_说明", color=C_TEXT)
        ctrl.draw_text((-1400.0, cy + H_SCREEN / 2.0 + 80.0, 0.0), sub_text, height=26.0, layer="07_TEXT_ANNOTATION_说明", color=C_TEXT)

    # ----------------- 4. 总图框标题栏与图签 -----------------
    ctrl.draw_text((-2400.0, 2650.0, 0.0), "一种模块化折叠翻转式多媒体教学黑板及光环境系统 - 正交总装工程复刻图", height=60.0, layer="07_TEXT_ANNOTATION_说明", color=C_TEXT)
    ctrl.draw_text((-2400.0, 2550.0, 0.0), "设计基准: 参考图 27216b5ba4f4d28a5775f13fde8d6648.jpg (100%纯净去反光高精矢量工程重构)", height=32.0, layer="07_TEXT_ANNOTATION_说明", color=C_TEXT)
    ctrl.draw_text((-2400.0, 2480.0, 0.0), "发明专利申请号: 202511764745.X | 发明人: 林诚俊 | 赛道: 青少年科技创新大赛工程学赛道", height=28.0, layer="07_TEXT_ANNOTATION_说明", color=C_TEXT)

    # 5. 全图居中缩放
    try:
        acad.ZoomExtents()
        print(">>> 视图已执行全图自适应缩放 (ZoomExtents)")
    except Exception as ze:
        print(f"ZoomExtents 提示: {ze}")

    # 6. 保存 DWG 文件至 01-CAD工程图纸
    save_dir = r"D:\Desktop\pjhb\01-CAD工程图纸"
    os.makedirs(save_dir, exist_ok=True)
    dwg_path = os.path.join(save_dir, "模块化折叠翻转多媒体智能黑板_纯净复刻工程图_v1.2.dwg")
    
    try:
        ctrl.doc.SaveAs(dwg_path)
        print(f">>> [SUCCESS] 图纸已成功保存为标准 DWG: {dwg_path}")
    except Exception as se:
        print(f"SaveAs 保存提示: {se}")
        try:
            ctrl.doc.Save()
            print(">>> 标准 Save 完成")
        except Exception as se2:
            print(f"Save 提示: {se2}")

    return dwg_path

if __name__ == "__main__":
    out_file = draw_blackboard_full_replica()
    print("V1_2_EXECUTION_COMPLETED:", out_file)
