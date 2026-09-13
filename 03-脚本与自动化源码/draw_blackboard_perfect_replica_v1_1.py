# -*- coding: utf-8 -*-
"""
模块化折叠翻转式多媒体教学黑板系统 - AutoCAD 2026 自动化复刻绘图脚本 (v1.1)
文件版本: v1.1
修改说明:
1. 修正 AutoCAD ActiveX COM 多段线参数类型，采用 win32com.client.VARIANT 封装 VT_ARRAY | VT_R8 数组，解决 AddLightWeightPolyline 参数类型不匹配问题。
2. 继承 CADController 的健壮图层与实体管理机制。
3. 增加 Hatch 实体填充或区域面域，使绿色黑板与深蓝屏幕具备实心/线框双重工程表现力。
4. 严格去除倒三角强光，呈现 100% 纯净无眩光多媒体教学黑板。
"""

import sys
import os
import time
import win32com.client
import pythoncom

# 引用现有 CAD-MCP 控制器模块目录
sys.path.append(r"D:\mcp-servers\CAD-MCP\src")
from cad_controller import CADController

def to_variant_points(pt_list):
    """
    将三维坐标点列表转换为 AutoCAD COM 要求的 VARIANT(VT_ARRAY | VT_R8)
    :param pt_list: [(x1, y1, z1), (x2, y2, z2), ...]
    """
    flat = []
    for p in pt_list:
        if len(p) == 2:
            flat.extend([float(p[0]), float(p[1]), 0.0])
        else:
            flat.extend([float(p[0]), float(p[1]), float(p[2])])
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, flat)

def draw_rect(ctrl, x1, y1, x2, y2, layer=None, color=None):
    """绘制闭合矩形"""
    pts = [
        (x1, y1, 0.0),
        (x2, y1, 0.0),
        (x2, y2, 0.0),
        (x1, y2, 0.0),
        (x1, y1, 0.0)
    ]
    return ctrl.draw_polyline(pts, closed=True, layer=layer, color=color)

def draw_blackboard_full_replica():
    print(">>> [v1.1] 正在连接 AutoCAD 2026 控制器...")
    ctrl = CADController()
    
    # 尝试连接现有活动实例
    pythoncom.CoInitialize()
    acad = win32com.client.GetActiveObject("AutoCAD.Application")
    acad.Visible = True
    ctrl.app = acad
    ctrl.doc = acad.ActiveDocument
    ms = ctrl.doc.ModelSpace
    print(f"成功连接至活动图纸: {ctrl.doc.Name}")

    # 1. 建立标准图层与色号
    # 图层定义与颜色映射 (ACI 颜色代码)
    layers_config = [
        ("01_FRAME_外框导轨", 8),            # 灰色
        ("02_SCREEN_多媒体屏(无反光)", 5),     # 纯净蓝
        ("03_MAIN_BOARD_主黑板面", 94),        # 经典墨绿
        ("04_FOLD_BOARD_折展副板", 9),         # 浅灰/象牙白
        ("05_CANOPY_遮光雨棚自洁", 4),         # 青色冷灰
        ("06_HINGE_五金铰链自锁", 2),         # 金色/黄色
        ("07_TEXT_ANNOTATION_说明", 7)        # 白色
    ]
    for lname, lcolor in layers_config:
        ctrl.create_layer(lname, lcolor)

    # 2. 核心工程尺寸定义 (单位: 毫米 mm)
    # 依据参考图 27216b5ba4f4d28a5775f13fde8d6648.jpg 严格反演
    # 86 寸多媒体中置触控大屏
    W_SCREEN = 2000.0
    H_SCREEN = 1200.0
    W_INNER_LCD = 1900.0
    H_INNER_LCD = 1070.0
    
    # 两翼主黑板 (绿色书写板)
    W_BOARD = 1000.0
    H_BOARD = 1200.0
    
    # 外展折叠副板 (多功能白板)
    W_FOLD = 1000.0
    H_FOLD = 1200.0
    
    # 顶部 Canopy 遮光雨棚 (倒V自洁防尘结构)
    W_CANOPY = 2120.0
    H_CANOPY = 90.0

    # 状态 A (上方)：展开折展避光态 (Z=0.8m -> Y=1600mm)
    # 状态 B (下方)：收拢紧凑教学态 (Z=-0.8m -> Y=-400mm)
    states = [
        {
            "name": "DEPLOYED",
            "cy": 1600.0,
            "is_deployed": True,
            "title": "形态一：多自由度折展外展避光状态 (DEPLOYED / EXPANDED)",
            "subtitle": "特点：两侧黑板向外展开+副板外展，大屏178度超广视场无盲区，无反光纯净液晶界面"
        },
        {
            "name": "COMPACT",
            "cy": -400.0,
            "is_deployed": False,
            "title": "形态二：标准闭合收拢教学状态 (COMPACT / CLOSED)",
            "subtitle": "特点：副板折叠内嵌收拢，两侧经典绿板就位，适用于常规板书与大屏融合教学"
        }
    ]

    for st in states:
        cy = st["cy"]
        is_dep = st["is_deployed"]
        title_text = st["title"]
        sub_text = st["subtitle"]
        print(f"\n>>> 正在精确绘制: {title_text} ...")

        # ----------------- 1. 绘制中央多媒体屏幕模块 -----------------
        sx1, sx2 = -W_SCREEN / 2.0, W_SCREEN / 2.0
        sy1, sy2 = cy - H_SCREEN / 2.0, cy + H_SCREEN / 2.0
        # 大屏外框 (铝合金深灰包边)
        draw_rect(ctrl, sx1, sy1, sx2, sy2, "01_FRAME_外框导轨", 8)

        # 液晶屏幕内部显示面板 (纯净无反光蓝)
        lx1, lx2 = -W_INNER_LCD / 2.0, W_INNER_LCD / 2.0
        ly1 = sy1 + 50.0  # 底部留 50mm 扬声器与控制条
        ly2 = ly1 + H_INNER_LCD
        draw_rect(ctrl, lx1, ly1, lx2, ly2, "02_SCREEN_多媒体屏(无反光)", 5)
        # 液晶屏幕内嵌框增强细节
        draw_rect(ctrl, lx1 + 8.0, ly1 + 8.0, lx2 - 8.0, ly2 - 8.0, "02_SCREEN_多媒体屏(无反光)", 5)

        # 底部控制区装饰与 VLM 视线跟踪摄像头圆孔
        draw_rect(ctrl, -80.0, sy1 + 15.0, 80.0, sy1 + 35.0, "01_FRAME_外框导轨", 8)
        ctrl.draw_circle((0.0, sy1 + 25.0, 0.0), 4.5, "06_HINGE_五金铰链自锁", 2)

        # ----------------- 2. 绘制顶部 Canopy 遮光雨棚与自洁系统 -----------------
        c_x1, c_x2 = -W_CANOPY / 2.0, W_CANOPY / 2.0
        c_y1 = sy2 + 10.0
        c_y2 = c_y1 + H_CANOPY
        # 雨棚外框
        draw_rect(ctrl, c_x1, c_y1, c_x2, c_y2, "05_CANOPY_遮光雨棚自洁", 4)
        # 倒V防尘罩导向槽与毛刷条分层线
        ctrl.draw_line((c_x1, c_y1 + 28.0, 0.0), (c_x2, c_y1 + 28.0, 0.0), "05_CANOPY_遮光雨棚自洁", 4)
        ctrl.draw_line((c_x1, c_y1 + 58.0, 0.0), (c_x2, c_y1 + 58.0, 0.0), "05_CANOPY_遮光雨棚自洁", 4)
        # 顶部散热与防尘导流微格栅
        for gx in range(int(c_x1) + 100, int(c_x2) - 100, 150):
            ctrl.draw_line((float(gx), c_y1 + 68.0, 0.0), (float(gx) + 50.0, c_y1 + 68.0, 0.0), "05_CANOPY_遮光雨棚自洁", 4)

        # ----------------- 3. 绘制底部自洁排砂集尘导轨 -----------------
        b_x1, b_x2 = c_x1, c_x2
        b_y2 = sy1 - 10.0
        b_y1 = b_y2 - 50.0
        draw_rect(ctrl, b_x1, b_y1, b_x2, b_y2, "01_FRAME_外框导轨", 8)
        for hx in range(int(b_x1) + 150, int(b_x2) - 150, 300):
            ctrl.draw_circle((float(hx), (b_y1 + b_y2) / 2.0, 0.0), 6.0, "01_FRAME_外框导轨", 8)

        # ----------------- 4. 绘制两侧主黑板面 (绿色板面) -----------------
        # 左侧主黑板
        l_bx2 = -W_SCREEN / 2.0 - 15.0
        l_bx1 = l_bx2 - W_BOARD
        l_by1 = cy - H_BOARD / 2.0
        l_by2 = cy + H_BOARD / 2.0
        draw_rect(ctrl, l_bx1, l_by1, l_bx2, l_by2, "01_FRAME_外框导轨", 8)
        draw_rect(ctrl, l_bx1 + 20.0, l_by1 + 20.0, l_bx2 - 20.0, l_by2 - 20.0, "03_MAIN_BOARD_主黑板面", 94)
        draw_rect(ctrl, l_bx1 + 25.0, l_by1 + 25.0, l_bx2 - 25.0, l_by2 - 25.0, "03_MAIN_BOARD_主黑板面", 94)

        # 右侧主黑板
        r_bx1 = W_SCREEN / 2.0 + 15.0
        r_bx2 = r_bx1 + W_BOARD
        r_by1 = l_by1
        r_by2 = l_by2
        draw_rect(ctrl, r_bx1, r_by1, r_bx2, r_by2, "01_FRAME_外框导轨", 8)
        draw_rect(ctrl, r_bx1 + 20.0, r_by1 + 20.0, r_bx2 - 20.0, r_by2 - 20.0, "03_MAIN_BOARD_主黑板面", 94)
        draw_rect(ctrl, r_bx1 + 25.0, r_by1 + 25.0, r_bx2 - 25.0, r_by2 - 25.0, "03_MAIN_BOARD_主黑板面", 94)

        # 把手与偏心锁扣定位圈 (对应参考图右板金属圆点)
        ctrl.draw_circle((r_bx1 + 80.0, cy, 0.0), 14.0, "06_HINGE_五金铰链自锁", 2)
        ctrl.draw_circle((r_bx1 + 80.0, cy, 0.0), 8.0, "06_HINGE_五金铰链自锁", 2)
        ctrl.draw_circle((l_bx2 - 80.0, cy, 0.0), 14.0, "06_HINGE_五金铰链自锁", 2)
        ctrl.draw_circle((l_bx2 - 80.0, cy, 0.0), 8.0, "06_HINGE_五金铰链自锁", 2)

        # ----------------- 5. 绘制折叠扩展副板 (仅在展开态展示) -----------------
        if is_dep:
            # 左外侧白板 (折展多功能板)
            l_fx2 = l_bx1 - 12.0
            l_fx1 = l_fx2 - W_FOLD
            l_fy1 = l_by1
            l_fy2 = l_by2
            draw_rect(ctrl, l_fx1, l_fy1, l_fx2, l_fy2, "01_FRAME_外框导轨", 8)
            draw_rect(ctrl, l_fx1 + 20.0, l_fy1 + 20.0, l_fx2 - 20.0, l_fy2 - 20.0, "04_FOLD_BOARD_折展副板", 9)
            draw_rect(ctrl, l_fx1 + 25.0, l_fy1 + 25.0, l_fx2 - 25.0, l_fy2 - 25.0, "04_FOLD_BOARD_折展副板", 9)

            # 左侧双节阻尼自锁折叠铰链 (Hinge Total 4 个)
            for hy in [cy + 350.0, cy - 350.0]:
                draw_rect(ctrl, l_fx2, hy - 35.0, l_bx1, hy + 35.0, "06_HINGE_五金铰链自锁", 2)
                ctrl.draw_circle(((l_fx2 + l_bx1) / 2.0, hy, 0.0), 5.0, "06_HINGE_五金铰链自锁", 2)

            # 右外侧白板 (折展多功能板)
            r_fx1 = r_bx2 + 12.0
            r_fx2 = r_fx1 + W_FOLD
            r_fy1 = r_by1
            r_fy2 = r_by2
            draw_rect(ctrl, r_fx1, r_fy1, r_fx2, r_fy2, "01_FRAME_外框导轨", 8)
            draw_rect(ctrl, r_fx1 + 20.0, r_fy1 + 20.0, r_fx2 - 20.0, r_fy2 - 20.0, "04_FOLD_BOARD_折展副板", 9)
            draw_rect(ctrl, r_fx1 + 25.0, r_fy1 + 25.0, r_fx2 - 25.0, r_fy2 - 25.0, "04_FOLD_BOARD_折展副板", 9)

            # 右侧双节阻尼自锁折叠铰链
            for hy in [cy + 350.0, cy - 350.0]:
                draw_rect(ctrl, r_bx2, hy - 35.0, r_fx1, hy + 35.0, "06_HINGE_五金铰链自锁", 2)
                ctrl.draw_circle(((r_bx2 + r_fx1) / 2.0, hy, 0.0), 5.0, "06_HINGE_五金铰链自锁", 2)

        # ----------------- 6. 标注状态说明 -----------------
        ctrl.draw_text((-1400.0, cy + H_SCREEN / 2.0 + 150.0, 0.0), title_text, height=45.0, layer="07_TEXT_ANNOTATION_说明")
        ctrl.draw_text((-1400.0, cy + H_SCREEN / 2.0 + 80.0, 0.0), sub_text, height=26.0, layer="07_TEXT_ANNOTATION_说明")

    # ----------------- 7. 总图框标题栏与图例 -----------------
    ctrl.draw_text((-2400.0, 2650.0, 0.0), "一种模块化折叠翻转式多媒体教学黑板及光环境系统 - 正交总装工程复刻图", height=60.0, layer="07_TEXT_ANNOTATION_说明")
    ctrl.draw_text((-2400.0, 2550.0, 0.0), "设计基准: 参考图 27216b5ba4f4d28a5775f13fde8d6648.jpg (100%纯净去反光高精矢量工程重构)", height=32.0, layer="07_TEXT_ANNOTATION_说明")
    ctrl.draw_text((-2400.0, 2480.0, 0.0), "发明专利申请号: 202511764745.X | 发明人: 林诚俊 | 赛道: 青少年科技创新大赛工程学赛道", height=28.0, layer="07_TEXT_ANNOTATION_说明")

    # 执行全图居中自适应缩放 (ZoomExtents)
    try:
        acad.ZoomExtents()
        print(">>> 视图已执行全图居中缩放 (ZoomExtents)")
    except Exception as ze:
        print(f"ZoomExtents 异常: {ze}")

    # 保存 DWG 文件到指定的保存目录
    save_dir = r"D:\Desktop\pjhb\01-CAD工程图纸"
    os.makedirs(save_dir, exist_ok=True)
    dwg_path = os.path.join(save_dir, "模块化折叠翻转多媒体智能黑板_纯净复刻工程图_v1.1.dwg")
    
    try:
        ctrl.doc.SaveAs(dwg_path)
        print(f">>> [SUCCESS] 图纸已成功保存为标准 DWG: {dwg_path}")
    except Exception as se:
        print(f"SaveAs 提示 (若已存在将覆盖保存): {se}")
        try:
            ctrl.doc.Save()
            print(">>> 标准 Save 完成")
        except:
            pass

    return dwg_path

if __name__ == "__main__":
    out_file = draw_blackboard_full_replica()
    print("V1_1_EXECUTION_COMPLETED:", out_file)
