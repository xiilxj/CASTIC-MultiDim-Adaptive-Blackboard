# -*- coding: utf-8 -*-
"""
第二代三维联动自洁防眩光智能教学黑板系统 - 全系统工程总装与运动机构图 (v1.0 完美排版版)
5600x3800 4K 超高清纯工程机械线框尺寸图渲染器 (Python Pillow)
输出路径: /mnt/d/Desktop/pjhb/01-CAD工程图纸/第二代三维联动自洁防眩光黑板系统_全系统工程总装与运动机构图_4K.png
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

def main():
    IMG_W = 5600
    IMG_H = 3800
    BG_COLOR = (20, 24, 30)  # 经典暗色工程 CAD 底色

    img = Image.new("RGB", (IMG_W, IMG_H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 载入中文字体
    font_path = "/mnt/c/Windows/Fonts/simhei.ttf"
    if not os.path.exists(font_path):
        font_path = "/usr/share/fonts/wenquanyi/wqy-microhei/wqy-microhei.ttc"
    
    def get_font(size):
        try:
            return ImageFont.truetype(font_path, size)
        except:
            return ImageFont.load_default()

    f_title = get_font(40)
    f_subtitle = get_font(21)
    f_subhead = get_font(24)
    f_dim = get_font(19)
    f_callout = get_font(17)
    f_tb_title = get_font(26)
    f_tb_text = get_font(18)

    # 经典工程 CAD 图层色彩
    C_FRAME = (180, 180, 180)     # 外框、型材
    C_SCREEN = (60, 160, 240)     # 多媒体屏
    C_BOARD = (50, 205, 100)      # 书写黑板
    C_EXT = (235, 60, 60)         # 延伸轨、自锁凸台、端部拉杆
    C_DUST = (220, 80, 220)       # 自洁排灰系统、EPDM罩
    C_PITCH = (40, 220, 220)      # 俯仰转轴、母座、蜗轮蜗杆
    C_OPTIC = (245, 200, 35)      # 伺服偏光膜、遮光挑檐、BLE终端
    C_DIM = (230, 80, 80)         # 尺寸链
    C_TEXT = (230, 230, 230)      # 说明文字与标题栏
    C_WHITE_BOARD = (220, 225, 230) # 异质白色搪瓷投影板

    # 世界坐标系映射范围
    WORLD_X1 = -3500.0
    WORLD_X2 = 6800.0
    WORLD_Y1 = -350.0
    WORLD_Y2 = 4350.0

    PAD_X = 50
    PAD_Y = 50
    DRAW_W = IMG_W - 2 * PAD_X
    DRAW_H = IMG_H - 2 * PAD_Y

    SCALE_X = DRAW_W / (WORLD_X2 - WORLD_X1)
    SCALE_Y = DRAW_H / (WORLD_Y2 - WORLD_Y1)
    SCALE = min(SCALE_X, SCALE_Y)

    OFFSET_X = PAD_X + (DRAW_W - (WORLD_X2 - WORLD_X1) * SCALE) / 2.0
    OFFSET_Y = PAD_Y + (DRAW_H - (WORLD_Y2 - WORLD_Y1) * SCALE) / 2.0

    def to_px(wx, wy):
        px = OFFSET_X + (wx - WORLD_X1) * SCALE
        py = IMG_H - (OFFSET_Y + (wy - WORLD_Y1) * SCALE)
        return px, py

    def draw_wrect(x1, y1, x2, y2, color, width=2):
        p1 = to_px(x1, y1)
        p2 = to_px(x2, y2)
        xmin, xmax = min(p1[0], p2[0]), max(p1[0], p2[0])
        ymin, ymax = min(p1[1], p2[1]), max(p1[1], p2[1])
        draw.rectangle([xmin, ymin, xmax, ymax], outline=color, width=width)

    def draw_wline(x1, y1, x2, y2, color, width=2, dashed=False):
        p1 = to_px(x1, y1)
        p2 = to_px(x2, y2)
        if not dashed:
            draw.line([p1, p2], fill=color, width=width)
        else:
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            dist = math.hypot(dx, dy)
            if dist < 1:
                return
            dash_len = 10
            gap_len = 8
            step = dash_len + gap_len
            steps = int(dist // step)
            ux, uy = dx / dist, dy / dist
            for i in range(steps):
                s_px = p1[0] + i * step * ux
                s_py = p1[1] + i * step * uy
                e_px = s_px + dash_len * ux
                e_py = s_py + dash_len * uy
                draw.line([(s_px, s_py), (e_px, e_py)], fill=color, width=width)

    def draw_wcircle(cx, cy, r, color, width=2):
        p = to_px(cx, cy)
        pr = r * SCALE
        draw.ellipse([p[0] - pr, p[1] - pr, p[0] + pr, p[1] + pr], outline=color, width=width)

    def draw_wtext(text, wx, wy, font, color):
        p = to_px(wx, wy)
        draw.text(p, text, font=font, fill=color)

    def draw_wlead(x1, y1, x2, y2, x3, text, color=C_TEXT):
        p1 = to_px(x1, y1)
        p2 = to_px(x2, y2)
        p3 = to_px(x3, y2)
        draw.line([p1, p2], fill=color, width=2)
        draw.line([p2, p3], fill=color, width=2)
        tx = p3[0] + 8 if p3[0] > p2[0] else p3[0] - (len(text) * 15) - 8
        draw.text((tx, p3[1] - 11), text, font=f_callout, fill=color)

    def draw_wdim(x1, y1, x2, y2, offset, is_h=True, text=""):
        if is_h:
            dy = y1 + offset
            p1_dim = to_px(x1, dy)
            p2_dim = to_px(x2, dy)
            draw_wline(x1, y1 + (15 if offset>0 else -15), x1, dy + (15 if offset>0 else -15), C_DIM, 1)
            draw_wline(x2, y2 + (15 if offset>0 else -15), x2, dy + (15 if offset>0 else -15), C_DIM, 1)
            draw_wline(x1, dy, x2, dy, C_DIM, 2)
            aw = 8
            draw.polygon([(p1_dim[0], p1_dim[1]), (p1_dim[0] + aw, p1_dim[1] - 4), (p1_dim[0] + aw, p1_dim[1] + 4)], fill=C_DIM)
            draw.polygon([(p2_dim[0], p2_dim[1]), (p2_dim[0] - aw, p2_dim[1] - 4), (p2_dim[0] - aw, p2_dim[1] + 4)], fill=C_DIM)
            cx = (p1_dim[0] + p2_dim[0]) / 2.0
            draw.text((cx - len(text)*5.5, p1_dim[1] - 22), text, font=f_dim, fill=C_DIM)
        else:
            dx = x1 + offset
            p1_dim = to_px(dx, y1)
            p2_dim = to_px(dx, y2)
            draw_wline(x1 + (15 if offset>0 else -15), y1, dx + (15 if offset>0 else -15), y1, C_DIM, 1)
            draw_wline(x2 + (15 if offset>0 else -15), y2, dx + (15 if offset>0 else -15), y2, C_DIM, 1)
            draw_wline(dx, y1, dx, y2, C_DIM, 2)
            aw = 8
            draw.polygon([(p1_dim[0], p1_dim[1]), (p1_dim[0] - 4, p1_dim[1] - aw), (p1_dim[0] + 4, p1_dim[1] - aw)], fill=C_DIM)
            draw.polygon([(p2_dim[0], p2_dim[1]), (p2_dim[0] - 4, p2_dim[1] + aw), (p2_dim[0] + 4, p2_dim[1] + aw)], fill=C_DIM)
            cy = (p1_dim[1] + p2_dim[1]) / 2.0
            draw.text((p1_dim[0] - len(text)*12 - 12, cy - 10), text, font=f_dim, fill=C_DIM)

    # 绘制外层标准图框
    draw_wrect(-3300.0, -200.0, 6600.0, 4200.0, C_FRAME, 3)
    draw_wrect(-3270.0, -170.0, 6570.0, 4170.0, C_FRAME, 1)

    # =========================================================================
    # 工况一：横向大行程侧滑与三维避光全展开状态 (Center Y = 3050.0)
    # =========================================================================
    CY1 = 3050.0
    top_y1 = CY1 + 600.0  # 3650
    bot_y1 = CY1 - 600.0  # 2450
    H_LCD = 1070.0

    draw_wtext("第二代工况一：横向大行程侧滑与三维空间避光全展开状态 [DEPLOYED - 极限跨度 6000mm]", -3050.0, top_y1 + 470.0, f_title, C_TEXT)
    draw_wtext("技术特征: 左右嵌套延伸轨向外直线侧滑 1000mm，大屏两侧物理盲区完全归零；偏心楔形自锁凸台切入锁紧卡口抵消悬臂下垂；展开双面搪瓷投影白板。", -3050.0, top_y1 + 415.0, f_subtitle, C_TEXT)

    # 中心 86 寸大屏
    draw_wrect(-1000.0, bot_y1, 1000.0, top_y1, C_FRAME, 2)
    draw_wrect(-950.0, bot_y1 + 65.0, 950.0, bot_y1 + 65.0 + H_LCD, C_SCREEN, 2)
    draw_wrect(-940.0, bot_y1 + 75.0, 940.0, bot_y1 + 55.0 + H_LCD, C_SCREEN, 1)
    
    # 大屏右内侧微型伺服电机与偏光膜外齿圈 (参考图 1 橙色高亮部位)
    draw_wrect(915.0, bot_y1 + 250.0, 935.0, bot_y1 + 450.0, C_OPTIC, 2)
    draw_wcircle(925.0, bot_y1 + 470.0, 15.0, C_OPTIC, 2)
    draw_wline(940.0, bot_y1 + 100.0, 940.0, bot_y1 + 1100.0, C_OPTIC, 2)
    # 调整引线：向左引，避免与右侧板面冲突
    draw_wlead(925.0, bot_y1 + 350.0, 780.0, bot_y1 + 400.0, 350.0, "微型直流伺服电机+柔性精密外齿圈(0°~90°偏光微调)", C_OPTIC)

    # 顶部卷轴遮光挑檐
    awning_top1 = top_y1 + 120.0
    draw_wrect(-1050.0, top_y1 + 10.0, 1050.0, awning_top1, C_OPTIC, 2)
    draw_wline(-1050.0, top_y1 + 45.0, 1050.0, top_y1 + 45.0, C_OPTIC, 1)
    draw_wline(-1050.0, top_y1 + 80.0, 1050.0, top_y1 + 80.0, C_OPTIC, 1)
    draw_wcircle(1000.0, top_y1 + 60.0, 18.0, C_OPTIC, 2)
    draw_wlead(1000.0, top_y1 + 60.0, 1150.0, top_y1 + 90.0, 1320.0, "顶罩内置微型卷轴马达(无级调节遮光深度 0~260mm)", C_OPTIC)

    # 左右内侧固定黑板面 (各 1000x1200mm)
    draw_wrect(-2000.0, bot_y1, -1000.0, top_y1, C_BOARD, 2)
    draw_wrect(-1980.0, bot_y1 + 20.0, -1020.0, top_y1 - 20.0, C_BOARD, 1)
    draw_wrect(1000.0, bot_y1, 2000.0, top_y1, C_BOARD, 2)
    draw_wrect(1020.0, bot_y1 + 20.0, 1980.0, top_y1 - 20.0, C_BOARD, 1)

    # 双横梁固定外框与 C 型槽底等间距排灰圆孔
    for side in [-1, 1]:
        draw_wrect(2000.0 * side, top_y1 - 60.0, (2000.0 + 1000.0) * side, top_y1, C_FRAME, 2)
        draw_wrect(2000.0 * side, bot_y1, (2000.0 + 1000.0) * side, bot_y1 + 60.0, C_FRAME, 2)
        for i in range(5):
            hx = (2100.0 + i * 200.0) * side
            draw_wcircle(hx, top_y1 - 30.0, 6.0, C_DUST, 2)
            draw_wcircle(hx, bot_y1 + 30.0, 6.0, C_DUST, 2)

    draw_wlead(2500.0, bot_y1 + 30.0, 2620.0, bot_y1 - 80.0, 2750.0, "C型槽底贯穿垂直排灰导流圆孔(Φ12mm, 等间距200mm, 消除滑动气阻)", C_DUST)

    # 左右外滑活动黑板主体
    draw_wrect(-3000.0, bot_y1, -2000.0, top_y1, C_BOARD, 2)
    draw_wrect(-2980.0, bot_y1 + 20.0, -2020.0, top_y1 - 20.0, C_BOARD, 1)
    draw_wcircle(-2500.0, CY1, 15.0, C_EXT, 2)

    draw_wrect(2000.0, bot_y1, 3000.0, top_y1, C_EXT, 2)
    draw_wrect(2020.0, bot_y1 + 20.0, 2980.0, top_y1 - 20.0, C_WHITE_BOARD, 2)
    draw_wcircle(2500.0, CY1, 15.0, C_EXT, 2)
    draw_wtext("[双面异质选配: 翻面展露白色防眩搪瓷书写/投影板]", 2060.0, CY1 - 120.0, f_callout, C_WHITE_BOARD)

    # 最外端垂直端部拉杆
    draw_wrect(-3015.0, bot_y1 - 10.0, -2995.0, top_y1 + 10.0, C_EXT, 3)
    draw_wrect(2995.0, bot_y1 - 10.0, 3015.0, top_y1 + 10.0, C_EXT, 3)
    draw_wlead(3015.0, CY1 + 200.0, 3120.0, CY1 + 260.0, 3250.0, "刚性垂直端部拉杆(刚性机械锁定上下滑轨,杜绝扭转形变)", C_EXT)

    # 偏心楔形自锁防下垂凸台与锁紧卡口
    draw_wrect(2000.0, top_y1 - 50.0, 2040.0, top_y1 - 15.0, C_EXT, 2)
    draw_wline(2000.0, top_y1 - 15.0, 2040.0, top_y1 - 35.0, C_EXT, 2)
    draw_wlead(2020.0, top_y1 - 25.0, 2120.0, top_y1 + 60.0, 2250.0, "偏心楔形自锁防下垂凸台(切入槽内锁紧卡口,消除1米悬臂弯矩)", C_EXT)

    # 工况一尺寸链 (三层尺寸清晰排列)
    draw_wdim(-3000.0, top_y1, -2000.0, top_y1, 100.0, True, "1000 [外滑双面黑板/白板]")
    draw_wdim(-2000.0, top_y1, -1000.0, top_y1, 100.0, True, "1000 [固定内黑板面]")
    draw_wdim(-1000.0, top_y1, 1000.0, top_y1, 100.0, True, "2000 [86寸多媒体交互大屏]")
    draw_wdim(1000.0, top_y1, 2000.0, top_y1, 100.0, True, "1000 [固定内黑板面]")
    draw_wdim(2000.0, top_y1, 3000.0, top_y1, 100.0, True, "1000 [外滑双面黑板/白板]")
    
    draw_wdim(-3000.0, top_y1, 3000.0, top_y1, 180.0, True, "6000 [第二代横向侧滑展开极限总跨度]")
    draw_wdim(2000.0, top_y1, 3000.0, top_y1, 260.0, True, "1000 [延伸轨侧滑最大行程 STROKE]")

    draw_wdim(-3000.0, bot_y1, -3000.0, top_y1, -150.0, False, "1200 [书写板标准净高]")
    draw_wdim(-3000.0, bot_y1 - 60.0, -3000.0, awning_top1, -280.0, False, "1380 [全系统含遮光罩总高]")


    # =========================================================================
    # 工况二：基准闭合待命与标准化快拆母座装配状态 (Center Y = 1100.0)
    # =========================================================================
    CY2 = 1100.0
    top_y2 = CY2 + 600.0  # 1700
    bot_y2 = CY2 - 600.0  # 500

    draw_wtext("第二代工况二：基准闭合待命与标准化快拆母座装配状态 [COMPACT - 基础跨度 4000mm]", -3050.0, top_y2 + 420.0, f_title, C_TEXT)
    draw_wtext("技术特征: 延伸内轨完全收纳于固定外框；转轴铰链处设标准化快拆卡挂母座(拔插销钉就地升级)与蜗轮蜗杆俯仰机构(-15°~+15°)；下连免布线BLE Mesh照度终端。", -3050.0, top_y2 + 365.0, f_subtitle, C_TEXT)

    # 中心大屏与收缩状态黑板
    draw_wrect(-1000.0, bot_y2, 1000.0, top_y2, C_FRAME, 2)
    draw_wrect(-950.0, bot_y2 + 65.0, 950.0, bot_y2 + 65.0 + H_LCD, C_SCREEN, 2)
    draw_wrect(-940.0, bot_y2 + 75.0, 940.0, bot_y2 + 55.0 + H_LCD, C_SCREEN, 1)

    draw_wrect(-2000.0, bot_y2, -1000.0, top_y2, C_BOARD, 2)
    draw_wrect(-1980.0, bot_y2 + 20.0, -1020.0, top_y2 - 20.0, C_BOARD, 1)
    draw_wrect(1000.0, bot_y2, 2000.0, top_y2, C_BOARD, 2)
    draw_wrect(1020.0, bot_y2 + 20.0, 1980.0, top_y2 - 20.0, C_BOARD, 1)

    # 左右外端标准化快拆卡挂母座与俯仰电机
    for side in [-1, 1]:
        hx = 2000.0 * side
        draw_wrect(hx - 20.0, CY2 - 80.0, hx + 20.0, CY2 + 80.0, C_PITCH, 2)
        draw_wcircle(hx, CY2, 12.0, C_PITCH, 2)
        draw_wrect(hx - 35.0, CY2 - 40.0, hx + 35.0, CY2 + 40.0, C_PITCH, 2)
        draw_wcircle(hx - 15.0, CY2, 6.0, C_PITCH, 2)
        draw_wcircle(hx + 15.0, CY2, 6.0, C_PITCH, 2)
        draw_wrect(hx - 30.0, CY2 + 90.0, hx + 30.0, CY2 + 170.0, C_PITCH, 2)
        draw_wcircle(hx, CY2 + 130.0, 15.0, C_PITCH, 2)

    draw_wlead(2020.0, CY2, 2150.0, CY2 + 80.0, 2280.0, "标准化多功能快拆卡挂母座(拔出快拆销钉即可实现一代二代就地升级)", C_PITCH)
    draw_wlead(2020.0, CY2 + 140.0, 2150.0, CY2 + 190.0, 2280.0, "蜗轮蜗杆俯仰马达组件(水平销轴带动外框进行-15°~+15°纵向避光摆动)", C_PITCH)

    # 课桌照度采集终端
    desk_y = bot_y2 - 220.0
    for dx in [-1500.0, -500.0, 500.0, 1500.0]:
        draw_wrect(dx - 160.0, desk_y - 50.0, dx + 160.0, desk_y, C_FRAME, 2)
        draw_wrect(dx + 90.0, desk_y, dx + 150.0, desk_y + 35.0, C_OPTIC, 2)
        draw_wcircle(dx + 120.0, desk_y + 18.0, 5.0, C_OPTIC, 2)
        draw_wline(dx + 120.0, desk_y + 35.0, dx + 120.0, desk_y + 60.0, C_OPTIC, 2)

    draw_wlead(1620.0, desk_y + 50.0, 1750.0, desk_y + 100.0, 1900.0, "分布式免布线照度采集终端(非晶硅室内太阳能集能+BLE Mesh无线自组网)", C_OPTIC)

    # 工况二尺寸链
    draw_wdim(-2000.0, top_y2, -1000.0, top_y2, 100.0, True, "1000 [黑板主体]")
    draw_wdim(-1000.0, top_y2, 1000.0, top_y2, 100.0, True, "2000 [86寸多媒体大屏]")
    draw_wdim(1000.0, top_y2, 2000.0, top_y2, 100.0, True, "1000 [黑板主体]")
    draw_wdim(-2000.0, top_y2, 2000.0, top_y2, 180.0, True, "4000 [第二代基础收缩总跨度]")


    # =========================================================================
    # 模块三：右侧视图区【三维运动副纵向俯仰剖面与自洁导轨详图】 (X: 3400 ~ 6500)
    # =========================================================================

    # 3.1 纵向俯仰避光剖面图 (Center X = 3950.0, Center Y = 3050.0)
    PX = 3950.0
    draw_wtext("【剖面视图 A-A】纵向俯仰避光原理 (-15°~+15°)", PX - 280.0, top_y1 + 440.0, f_subhead, C_TEXT)
    draw_wrect(PX - 240.0, bot_y1 - 80.0, PX - 190.0, top_y1 + 80.0, C_FRAME, 2)
    draw_wline(PX - 240.0, bot_y1 - 80.0, PX - 270.0, bot_y1 - 50.0, C_FRAME, 1)
    draw_wline(PX - 240.0, CY1, PX - 270.0, CY1 + 30.0, C_FRAME, 1)
    draw_wline(PX - 240.0, top_y1 + 50.0, PX - 270.0, top_y1 + 80.0, C_FRAME, 1)

    draw_wrect(PX - 190.0, CY1 - 60.0, PX - 110.0, CY1 + 60.0, C_PITCH, 2)
    draw_wcircle(PX - 110.0, CY1, 18.0, C_PITCH, 2)
    draw_wtext("水平铰接销轴(Pitch轴)", PX - 100.0, CY1 - 35.0, f_callout, C_PITCH)

    tilt_rad = math.radians(15.0)
    p_top_x = (PX - 110.0) + 50.0 + 580.0 * math.sin(tilt_rad)
    p_top_y = CY1 + 580.0 * math.cos(tilt_rad)
    p_bot_x = (PX - 110.0) + 50.0 - 580.0 * math.sin(tilt_rad)
    p_bot_y = CY1 - 580.0 * math.cos(tilt_rad)
    dx_th = 40.0 * math.cos(tilt_rad)
    dy_th = -40.0 * math.sin(tilt_rad)

    draw_wline(p_bot_x, p_bot_y, p_top_x, p_top_y, C_BOARD, 2)
    draw_wline(p_top_x, p_top_y, p_top_x + dx_th, p_top_y + dy_th, C_BOARD, 2)
    draw_wline(p_top_x + dx_th, p_top_y + dy_th, p_bot_x + dx_th, p_bot_y + dy_th, C_BOARD, 2)
    draw_wline(p_bot_x + dx_th, p_bot_y + dy_th, p_bot_x, p_bot_y, C_BOARD, 2)

    draw_wline(PX - 60.0, CY1 - 620.0, PX - 60.0, CY1 + 620.0, C_DIM, 1, dashed=True)
    draw_wtext("+15° 纵向避光倾斜角", PX + 70.0, CY1 + 220.0, f_dim, C_DIM)

    draw_wline(PX + 420.0, CY1 + 180.0, p_top_x - 90.0, CY1 + 90.0, C_OPTIC, 2)
    draw_wline(p_top_x - 90.0, CY1 + 90.0, PX + 460.0, CY1 + 620.0, C_OPTIC, 2)
    draw_wtext("入射直射强光锥", PX + 430.0, CY1 + 160.0, f_callout, C_OPTIC)
    draw_wtext("反射眩光被物理折射至天花板无人区", PX + 280.0, CY1 + 640.0, f_callout, C_OPTIC)


    # 3.2 导轨自洁防尘与排灰系统截面详图 (Detail B-B, Center X = 5400.0, Center Y = 3050.0)
    DX = 5400.0
    draw_wtext("【节点详图 B-B】导轨自洁防尘与排灰消气阻截面", DX - 350.0, top_y1 + 440.0, f_subhead, C_TEXT)
    draw_wrect(DX - 160.0, CY1 - 110.0, DX + 160.0, CY1 + 110.0, C_FRAME, 2)
    draw_wrect(DX - 120.0, CY1 - 65.0, DX + 120.0, CY1 + 65.0, C_FRAME, 1)

    # 倒 V 型 EPDM 橡胶防护罩
    draw_wline(DX - 180.0, CY1 + 110.0, DX, CY1 + 200.0, C_DUST, 2)
    draw_wline(DX, CY1 + 200.0, DX + 180.0, CY1 + 110.0, C_DUST, 2)
    draw_wline(DX - 170.0, CY1 + 105.0, DX, CY1 + 185.0, C_DUST, 1)
    draw_wline(DX, CY1 + 185.0, DX + 170.0, CY1 + 105.0, C_DUST, 1)
    draw_wlead(DX, CY1 + 200.0, DX + 100.0, CY1 + 260.0, DX + 220.0, "倒V型EPDM弹性橡胶防护罩(阻隔95%粉笔灰)", C_DUST)

    # 延伸内轨与尼龙毛刷
    draw_wrect(DX - 80.0, CY1 - 35.0, DX + 80.0, CY1 + 35.0, C_EXT, 2)
    for bx in range(int(DX - 100.0), int(DX + 100.0), 14):
        draw_wline(float(bx), CY1 - 35.0, float(bx), CY1 - 65.0, C_DUST, 1)
    draw_wlead(DX - 50.0, CY1 - 50.0, DX - 160.0, CY1 - 160.0, DX - 290.0, "微细尼龙自洁毛刷条(往复推扫积灰)", C_DUST)

    # 垂直排灰圆孔
    draw_wrect(DX - 25.0, CY1 - 110.0, DX + 25.0, CY1 - 65.0, C_DUST, 2)
    draw_wcircle(DX, CY1 - 88.0, 16.0, C_DUST, 2)
    draw_wlead(DX + 18.0, CY1 - 88.0, DX + 120.0, CY1 - 110.0, DX + 240.0, "垂直贯穿排灰导流孔(Φ12mm/消除气阻)", C_DUST)

    # 底部集尘盒
    draw_wrect(DX - 130.0, CY1 - 200.0, DX + 130.0, CY1 - 120.0, C_FRAME, 2)
    draw_wline(DX - 90.0, CY1 - 160.0, DX + 90.0, CY1 - 160.0, C_FRAME, 1)
    draw_wlead(DX + 130.0, CY1 - 160.0, DX + 200.0, CY1 - 200.0, DX + 310.0, "抽屉式外挂粉尘收集盒(便于集中清理)", C_FRAME)


    # 3.3 偏心自锁防下垂详图 (Detail C-C, Center X = 4300.0, Center Y = 1100.0)
    KX = 4300.0
    draw_wtext("【节点详图 C-C】悬臂偏心楔形自锁防下垂机构", KX - 320.0, top_y2 + 380.0, f_subhead, C_TEXT)
    draw_wrect(KX - 220.0, CY2 + 45.0, KX + 220.0, CY2 + 115.0, C_FRAME, 2)
    draw_wrect(KX - 220.0, CY2 - 115.0, KX + 220.0, CY2 - 45.0, C_FRAME, 2)
    draw_wrect(KX + 80.0, CY2 + 25.0, KX + 140.0, CY2 + 45.0, C_FRAME, 2)

    draw_wrect(KX - 180.0, CY2 - 35.0, KX + 130.0, CY2 + 35.0, C_EXT, 2)
    draw_wline(KX + 80.0, CY2 + 35.0, KX + 140.0, CY2 + 45.0, C_EXT, 2)
    draw_wline(KX + 140.0, CY2 + 45.0, KX + 140.0, CY2 + 35.0, C_EXT, 2)
    draw_wlead(KX + 110.0, CY2 + 40.0, KX + 190.0, CY2 + 130.0, KX + 310.0, "偏心楔形自锁凸台(3.5°斜面过盈卡紧,抵消1米悬臂弯矩)", C_EXT)
    draw_wlead(KX + 80.0, CY2 + 30.0, KX + 190.0, CY2 - 50.0, KX + 310.0, "固定外框锁紧卡口(终点刚性定位死锁配合)", C_FRAME)


    # =========================================================================
    # 底部技术参数表与标准工程标题栏 (GB/T 10609.1)
    # =========================================================================
    # 参数表格 (X: -3200 ~ 1200, Y: -140 ~ 360)
    TAB_X1, TAB_X2 = -3200.0, 1200.0
    TAB_Y1, TAB_Y2 = -140.0, 360.0
    draw_wrect(TAB_X1, TAB_Y1, TAB_X2, TAB_Y2, C_FRAME, 2)
    draw_wline(TAB_X1, TAB_Y2 - 55.0, TAB_X2, TAB_Y2 - 55.0, C_FRAME, 2)
    draw_wtext("【第二代三维联动自洁防眩光智能教学黑板系统 - 核心工程参数与技术指标矩阵】", TAB_X1 + 25.0, TAB_Y2 - 40.0, f_tb_title, C_TEXT)

    specs = [
        "1. 三维空间运动自由度: 偏航水平旋转 0°~90°；纵向垂直俯仰 -15°~+15° (蜗轮蜗杆物理自锁抗下坠)；横向直线侧滑 0~1000mm (行程极限 6000mm)。",
        "2. 悬臂防下垂自锁机构: 延伸滑轨滑入端设 3.5° 偏心楔形自锁凸台，1.0m 极限行程切入外框锁紧卡口，过盈卡紧彻底抵消 1 米悬臂重力弯矩与公差。",
        "3. 刚性端部机械锁定: 上、下延伸滑轨外展端部通过实心竖直端部拉杆做刚性锁定连接，杜绝悬臂重载下上下轨动作不同步与结构扭转形变。",
        "4. 轨道重载自洁排灰系统: 上部倒 V 型 EPDM 弹性橡胶密封罩 (阻隔 95% 直落粉尘)；槽底以 200mm 等间距开设 Φ12mm 垂直排灰导流圆孔消除气阻。",
        "5. 标准化快拆升级母座: 带有锁紧销钉孔的装配凹槽，拔出快拆销钉即可在一代固定架与二代伸缩外框之间就地替换，锁死升级商业链路。",
        "6. 双面同质/异质磁吸选配: 对称布置钕铁硼标准化磁吸座，支持正面高附着绿板、反面超平整搪瓷投影白板 5 秒无工具快速翻转替换。",
        "7. AI 多模态主动控光闭环: 大屏外置电控偏光膜 (微型伺服 0°~90° 无级旋转过滤反光) + 免布线非晶硅太阳能 BLE Mesh 照度终端 (突变中断秒级唤醒)。"
    ]
    sy = TAB_Y2 - 95.0
    for s in specs:
        draw_wtext(s, TAB_X1 + 20.0, sy, f_tb_text, C_TEXT)
        sy -= 45.0

    # 标题栏 (X: 1350 ~ 6550, Y: -140 ~ 360)
    TB_X1, TB_X2 = 1350.0, 6550.0
    TB_Y1, TB_Y2 = -140.0, 360.0
    draw_wrect(TB_X1, TB_Y1, TB_X2, TB_Y2, C_FRAME, 2)
    draw_wline(TB_X1, TB_Y2 - 70.0, TB_X2, TB_Y2 - 70.0, C_FRAME, 2)
    draw_wline(TB_X1, TB_Y1 + 90.0, TB_X2, TB_Y1 + 90.0, C_FRAME, 2)

    draw_wline(TB_X1 + 1000.0, TB_Y1, TB_X1 + 1000.0, TB_Y2, C_FRAME, 2)
    draw_wline(TB_X1 + 2600.0, TB_Y1, TB_X1 + 2600.0, TB_Y2, C_FRAME, 2)
    draw_wline(TB_X1 + 3800.0, TB_Y1, TB_X1 + 3800.0, TB_Y2, C_FRAME, 2)

    draw_wtext("系统代号: GH-W-2026", TB_X1 + 30.0, TB_Y2 - 50.0, f_tb_title, C_TEXT)
    draw_wtext("图纸名称: 第二代三维空间联动避光与自洁黑板工程总装图", TB_X1 + 1030.0, TB_Y2 - 50.0, f_tb_title, C_TEXT)
    draw_wtext("图号: GH-GEN2-ASM-01", TB_X1 + 3830.0, TB_Y2 - 50.0, f_tb_title, C_TEXT)

    draw_wtext("设计阶段: 第二代实施例与实用新型申请图", TB_X1 + 30.0, TB_Y2 - 130.0, f_tb_text, C_TEXT)
    draw_wtext("设计制图: czx & 海鸥 (Antigravity)", TB_X1 + 1030.0, TB_Y2 - 130.0, f_tb_text, C_TEXT)
    draw_wtext("比例: 1:1 (标准机械毫米制)", TB_X1 + 2630.0, TB_Y2 - 130.0, f_tb_text, C_TEXT)
    draw_wtext("出图规范: 0 Hatch 纯工程机械线框", TB_X1 + 3830.0, TB_Y2 - 130.0, f_tb_text, C_TEXT)

    draw_wtext("审核结论: 第 9 轮全系统工程审核·参数完全吻合通过", TB_X1 + 30.0, TB_Y1 + 30.0, f_tb_text, C_TEXT)
    draw_wtext("适用标准: GB/T 28231-2011 / 专利交底书 (20260703132200)", TB_X1 + 1030.0, TB_Y1 + 30.0, f_tb_text, C_TEXT)
    draw_wtext("状态: 生产试制与专利附图工程冻结版", TB_X1 + 3830.0, TB_Y1 + 30.0, f_tb_text, C_TEXT)

    # 保存图片
    out_path = "/mnt/d/Desktop/pjhb/01-CAD工程图纸/第二代三维联动自洁防眩光黑板系统_全系统工程总装与运动机构图_4K.png"
    img.save(out_path, "PNG")
    print(">>> [成功] 第二代 4K 超高清纯工程机械线框图已更新:", out_path)

if __name__ == "__main__":
    main()
