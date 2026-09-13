# -*- coding: utf-8 -*-
"""
第三代多维叠合翻转全覆盖与三维自洁侧滑智能黑板系统 - 全系统工程总装与运动机构图 (v1.0)
5800x4000 4K 超高清纯工程机械线框尺寸图渲染器 (Python Pillow)
输出路径: /mnt/d/Desktop/pjhb/01-CAD工程图纸/第三代多维叠合翻转全覆盖与三维自洁侧滑黑板系统_全系统工程总装与运动机构图_4K.png
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

def main():
    IMG_W = 5800
    IMG_H = 4000
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

    f_title = get_font(38)
    f_subtitle = get_font(20)
    f_subhead = get_font(23)
    f_dim = get_font(18)
    f_callout = get_font(17)
    f_tb_title = get_font(26)
    f_tb_text = get_font(18)

    # 经典工程 CAD 图层色彩
    C_FRAME = (180, 180, 180)        # 外框、型材
    C_SCREEN = (60, 160, 240)        # 多媒体屏
    C_OUTER_BOARD = (50, 205, 100)   # 外层主黑板 (绿色)
    C_INNER_BOARD = (245, 200, 35)   # 内层附加超薄黑板 (黄色)
    C_INNER_HINGE = (220, 80, 220)   # 内缘铺开铰链 (品红)
    C_EXT = (235, 60, 60)            # 延伸轨、自锁凸台、端部拉杆 (红色)
    C_PITCH = (40, 220, 220)         # 俯仰转轴、母座、蜗轮蜗杆 (青色)
    C_DIM = (230, 80, 80)            # 尺寸链 (红色)
    C_TEXT = (230, 230, 230)         # 说明文字与标题栏 (白色)
    C_WHITE_BOARD = (220, 225, 230)  # 白色搪瓷投影板

    # 世界坐标系映射范围 (涵盖三工况纵向排列)
    WORLD_X1 = -3500.0
    WORLD_X2 = 6800.0
    WORLD_Y1 = -350.0
    WORLD_Y2 = 5450.0

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
            draw.text((cx - len(text)*5.2, p1_dim[1] - 20), text, font=f_dim, fill=C_DIM)
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
            draw.text((p1_dim[0] - len(text)*12 - 10, cy - 10), text, font=f_dim, fill=C_DIM)

    # 绘制外层标准图框 (X: -3300 ~ 6600, Y: -200 ~ 5350)
    draw_wrect(-3300.0, -200.0, 6600.0, 5350.0, C_FRAME, 3)
    draw_wrect(-3270.0, -170.0, 6570.0, 5320.0, C_FRAME, 1)

    # =========================================================================
    # 工况一：初始闭合·市面主流全覆盖封屏形态 (Center Y = 4600.0)
    # =========================================================================
    CY1 = 4600.0
    top_y1 = CY1 + 600.0  # 5200
    bot_y1 = CY1 - 600.0  # 4000
    H_LCD = 1070.0

    draw_wtext("第三代工况一：初始闭合·市面主流全覆盖封屏形态 [COVERED - 传统主流全封闭 4000mm]", -3050.0, top_y1 + 420.0, f_title, C_TEXT)
    draw_wtext("技术特征: 左右黑板成二分层(外层主板12mm+内层附加板12mm)；靠大屏内侧增设内缘铰链向中心铺开180°对撞自锁，100%遮蔽86寸大屏，呈现主流全覆盖形态。", -3050.0, top_y1 + 365.0, f_subtitle, C_TEXT)

    # 后方大屏被封锁虚线示意
    draw_wrect(-1000.0, bot_y1, 1000.0, top_y1, C_SCREEN, 2)
    draw_wtext("[86寸多媒体大屏被100%封闭在背后保护防撞]", -650.0, CY1 + 220.0, f_callout, C_SCREEN)

    # 左右外层主板 (X: -2000~-1000, 1000~2000)
    draw_wrect(-2000.0, bot_y1, -1000.0, top_y1, C_OUTER_BOARD, 2)
    draw_wrect(-1980.0, bot_y1 + 20.0, -1020.0, top_y1 - 20.0, C_OUTER_BOARD, 1)
    draw_wrect(1000.0, bot_y1, 2000.0, top_y1, C_OUTER_BOARD, 2)
    draw_wrect(1020.0, bot_y1 + 20.0, 1980.0, top_y1 - 20.0, C_OUTER_BOARD, 1)

    # 铺开在大屏正前方的左右内层附加板 (X: -1000~0, 0~1000)
    draw_wrect(-1000.0, bot_y1, 0.0, top_y1, C_INNER_BOARD, 2)
    draw_wrect(-980.0, bot_y1 + 20.0, -20.0, top_y1 - 20.0, C_INNER_BOARD, 1)
    draw_wrect(0.0, bot_y1, 1000.0, top_y1, C_INNER_BOARD, 2)
    draw_wrect(20.0, bot_y1 + 20.0, 980.0, top_y1 - 20.0, C_INNER_BOARD, 1)

    # 内缘铺开铰链 (设于 X=-1000 和 X=1000)
    for hx in [-1000.0, 1000.0]:
        draw_wrect(hx - 15.0, CY1 - 250.0, hx + 15.0, CY1 - 150.0, C_INNER_HINGE, 2)
        draw_wcircle(hx, CY1 - 200.0, 8.0, C_INNER_HINGE, 2)
        draw_wrect(hx - 15.0, CY1 + 150.0, hx + 15.0, CY1 + 250.0, C_INNER_HINGE, 2)
        draw_wcircle(hx, CY1 + 200.0, 8.0, C_INNER_HINGE, 2)

    draw_wlead(-1000.0, CY1 + 200.0, -1120.0, CY1 + 260.0, -1250.0, "多维内缘铺开铰链(大屏内侧竖边,向内铺展180°封屏)", C_INNER_HINGE)
    draw_wlead(0.0, CY1, 120.0, CY1 + 80.0, 250.0, "中央碰珠式磁吸机械对撞锁紧缝(全覆盖平整拼接)", C_INNER_BOARD)

    # 尺寸标注 (工况一)
    draw_wdim(-2000.0, top_y1, -1000.0, top_y1, 100.0, True, "1000 [外层主板]")
    draw_wdim(-1000.0, top_y1, 0.0, top_y1, 100.0, True, "1000 [铺开内板A]")
    draw_wdim(0.0, top_y1, 1000.0, top_y1, 100.0, True, "1000 [铺开内板B]")
    draw_wdim(1000.0, top_y1, 2000.0, top_y1, 100.0, True, "1000 [外层主板]")
    draw_wdim(-2000.0, top_y1, 2000.0, top_y1, 170.0, True, "4000 [主流全覆盖纯板书总跨度]")
    draw_wdim(-1000.0, top_y1, 1000.0, top_y1, 240.0, True, "2000 [全覆盖完全遮蔽大屏跨度]")


    # =========================================================================
    # 工况二：常态多媒体·大屏露显双层叠合形态 (Center Y = 2800.0)
    # =========================================================================
    CY2 = 2800.0
    top_y2 = CY2 + 600.0  # 3400
    bot_y2 = CY2 - 600.0  # 2200

    draw_wtext("第三代工况二：常态多媒体·大屏露显双层叠合形态 [COMPACT - 黄金视域 4000mm]", -3050.0, top_y2 + 420.0, f_title, C_TEXT)
    draw_wtext("技术特征: 内缘铰链折回，内层附加板与外层主板附加叠合为一体(叠合厚度仅26mm)；86寸多媒体屏完全露显；大屏右内侧配置伺服驱动偏光膜机构。", -3050.0, top_y2 + 365.0, f_subtitle, C_TEXT)

    # 中心大屏完全露显
    draw_wrect(-1000.0, bot_y2, 1000.0, top_y2, C_FRAME, 2)
    draw_wrect(-950.0, bot_y2 + 65.0, 950.0, bot_y2 + 65.0 + H_LCD, C_SCREEN, 2)
    draw_wrect(-940.0, bot_y2 + 75.0, 940.0, bot_y2 + 55.0 + H_LCD, C_SCREEN, 1)

    # 大屏右内侧微型伺服电机与偏光膜齿圈
    draw_wrect(915.0, bot_y2 + 250.0, 935.0, bot_y2 + 450.0, C_INNER_BOARD, 2)
    draw_wcircle(925.0, bot_y2 + 470.0, 15.0, C_INNER_BOARD, 2)
    draw_wline(940.0, bot_y2 + 100.0, 940.0, bot_y2 + 1100.0, C_INNER_BOARD, 2)

    # 左右双层附加叠合板
    for side in [-1, 1]:
        bx1 = 1000.0 * side
        bx2 = 2000.0 * side
        draw_wrect(bx1, bot_y2, bx2, top_y2, C_OUTER_BOARD, 2)
        draw_wrect(bx1 + (20.0*side), bot_y2 + 20.0, bx2 - (20.0*side), top_y2 - 20.0, C_OUTER_BOARD, 1)
        draw_wrect(bx1 + (10.0*side), bot_y2 + 10.0, bx2 - (10.0*side), top_y2 - 10.0, C_INNER_BOARD, 2)

    draw_wlead(-1500.0, CY2, -1650.0, CY2 + 100.0, -1800.0, "双层附加叠合黑板(外层主板12mm+内层附加板12mm叠合收拢)", C_INNER_BOARD)

    # 左右承重主铰链、快拆母座与蜗轮蜗杆俯仰马达
    for side in [-1, 1]:
        hx = 2000.0 * side
        draw_wrect(hx - 20.0, CY2 - 80.0, hx + 20.0, CY2 + 80.0, C_PITCH, 2)
        draw_wcircle(hx, CY2, 12.0, C_PITCH, 2)
        draw_wrect(hx - 30.0, CY2 + 90.0, hx + 30.0, CY2 + 170.0, C_PITCH, 2)
        draw_wcircle(hx, CY2 + 130.0, 15.0, C_PITCH, 2)

    draw_wlead(2020.0, CY2, 2150.0, CY2 + 70.0, 2280.0, "标准化快拆卡挂母座(拔插销钉一二三代就地互换)", C_PITCH)

    # 尺寸标注 (工况二)
    draw_wdim(-2000.0, top_y2, -1000.0, top_y2, 100.0, True, "1000 [双层叠合板]")
    draw_wdim(-1000.0, top_y2, 1000.0, top_y2, 100.0, True, "2000 [86寸多媒体大屏]")
    draw_wdim(1000.0, top_y2, 2000.0, top_y2, 100.0, True, "1000 [双层叠合板]")
    draw_wdim(-2000.0, top_y2, 2000.0, top_y2, 170.0, True, "4000 [常态多媒体教学总跨度]")


    # =========================================================================
    # 工况三：大视野与三维空间避光极限展开形态 (Center Y = 1000.0)
    # =========================================================================
    CY3 = 1000.0
    top_y3 = CY3 + 600.0  # 1600
    bot_y3 = CY3 - 600.0  # 400

    draw_wtext("第三代工况三：大视野与三维空间避光极限展开形态 [DEPLOYED - 盲区归零 6000mm]", -3050.0, top_y3 + 420.0, f_title, C_TEXT)
    draw_wtext("技术特征: 双层叠合板沿双横梁自洁延伸轨外滑1000mm，总幅宽展开至6000mm；偏心楔形自锁消除悬臂弯矩；联动俯仰轴-15°~+15°纵向折射避光。", -3050.0, top_y3 + 365.0, f_subtitle, C_TEXT)

    # 中心大屏露显
    draw_wrect(-1000.0, bot_y3, 1000.0, top_y3, C_FRAME, 2)
    draw_wrect(-950.0, bot_y3 + 65.0, 950.0, bot_y3 + 65.0 + H_LCD, C_SCREEN, 2)

    # 露出双横梁固定外框与槽底每隔 200mm 排灰孔
    for side in [-1, 1]:
        draw_wrect(2000.0 * side, top_y3 - 60.0, (2000.0 + 1000.0) * side, top_y3, C_FRAME, 2)
        draw_wrect(2000.0 * side, bot_y3, (2000.0 + 1000.0) * side, bot_y3 + 60.0, C_FRAME, 2)
        for i in range(5):
            hx = (2100.0 + i * 200.0) * side
            draw_wcircle(hx, top_y3 - 30.0, 6.0, C_INNER_HINGE, 2)
            draw_wcircle(hx, bot_y3 + 30.0, 6.0, C_INNER_HINGE, 2)

    # 外展 1.0 米的黑板主体 (X: -3000~-2000, 2000~3000)
    draw_wrect(-3000.0, bot_y3, -2000.0, top_y3, C_OUTER_BOARD, 2)
    draw_wrect(-2980.0, bot_y3 + 20.0, -2020.0, top_y3 - 20.0, C_OUTER_BOARD, 1)

    draw_wrect(2000.0, bot_y3, 3000.0, top_y3, C_EXT, 2)
    draw_wrect(2020.0, bot_y3 + 20.0, 2980.0, top_y3 - 20.0, C_WHITE_BOARD, 2)
    draw_wtext("[异质选配: 翻面展露白色防眩搪瓷书写/投影板]", 2060.0, CY3 - 80.0, f_callout, C_WHITE_BOARD)

    # 最外端垂直端部拉杆
    draw_wrect(-3015.0, bot_y3 - 10.0, -2995.0, top_y3 + 10.0, C_EXT, 3)
    draw_wrect(2995.0, bot_y3 - 10.0, 3015.0, top_y3 + 10.0, C_EXT, 3)
    draw_wlead(3015.0, CY3 + 200.0, 3120.0, CY3 + 260.0, 3250.0, "刚性垂直端部拉杆(刚性机械锁定上下滑轨)", C_EXT)

    # 尺寸标注 (工况三)
    draw_wdim(-3000.0, top_y3, -2000.0, top_y3, 100.0, True, "1000 [外滑黑板主体]")
    draw_wdim(-2000.0, top_y3, -1000.0, top_y3, 100.0, True, "1000 [外露自洁滑槽]")
    draw_wdim(-1000.0, top_y3, 1000.0, top_y3, 100.0, True, "2000 [86寸多媒体大屏]")
    draw_wdim(1000.0, top_y3, 2000.0, top_y3, 100.0, True, "1000 [外露自洁滑槽]")
    draw_wdim(2000.0, top_y3, 3000.0, top_y3, 100.0, True, "1000 [外滑黑板主体]")
    draw_wdim(-3000.0, top_y3, 3000.0, top_y3, 170.0, True, "6000 [侧滑平移推拉展开极限总跨度]")
    draw_wdim(2000.0, top_y3, 3000.0, top_y3, 240.0, True, "1000 [延伸滑轨最大侧移行程]")


    # =========================================================================
    # 模块四：右侧剖面与详图区 (X: 3800 ~ 6800)
    # =========================================================================

    # 4.1 剖面 A-A：多维内缘铺开铰链双层叠合与翻转运动原理 (Center X = 4300, Center Y = 4600)
    PX1 = 4300.0
    draw_wtext("【剖面视图 A-A】内缘铰链双层叠合与铺开翻折运动原理", PX1 - 320.0, top_y1 + 420.0, f_subhead, C_TEXT)
    draw_wrect(PX1 - 200.0, CY1 - 80.0, PX1 - 140.0, CY1 + 80.0, C_FRAME, 2)
    draw_wrect(PX1 - 140.0, CY1 - 400.0, PX1 - 110.0, CY1 + 400.0, C_OUTER_BOARD, 2)
    draw_wtext("外层主板(12mm)", PX1 - 135.0, CY1 - 440.0, f_callout, C_OUTER_BOARD)

    draw_wcircle(PX1 - 110.0, CY1, 16.0, C_INNER_HINGE, 2)
    draw_wcircle(PX1 - 110.0, CY1, 8.0, C_INNER_HINGE, 2)
    draw_wlead(PX1 - 110.0, CY1 + 16.0, PX1 - 40.0, CY1 + 90.0, PX1 + 80.0, "内缘铺开铰链枢轴(回转角0°~180°)", C_INNER_HINGE)

    draw_wrect(PX1 - 105.0, CY1 - 390.0, PX1 - 75.0, CY1 + 390.0, C_INNER_BOARD, 2)
    draw_wtext("叠合态(厚26mm)", PX1 - 100.0, CY1 + 410.0, f_callout, C_INNER_BOARD)
    draw_wrect(PX1 - 110.0, CY1 - 15.0, PX1 + 350.0, CY1 + 15.0, C_INNER_BOARD, 2)
    draw_wtext("180° 铺开封屏态(覆盖在86寸大屏正前方)", PX1 + 20.0, CY1 + 40.0, f_callout, C_INNER_BOARD)

    # 4.2 剖面 B-B：纵向俯仰避光原理 (Center X = 4300, Center Y = 2800)
    PX2 = 4300.0
    draw_wtext("【剖面视图 B-B】纵向俯仰避光与光锥折射原理 (-15°~+15°)", PX2 - 320.0, top_y2 + 420.0, f_subhead, C_TEXT)
    draw_wrect(PX2 - 240.0, CY2 - 300.0, PX2 - 190.0, CY2 + 300.0, C_FRAME, 2)
    draw_wrect(PX2 - 190.0, CY2 - 60.0, PX2 - 110.0, CY2 + 60.0, C_PITCH, 2)
    draw_wcircle(PX2 - 110.0, CY2, 18.0, C_PITCH, 2)
    draw_wtext("水平铰接销轴(Pitch轴)", PX2 - 100.0, CY2 - 35.0, f_callout, C_PITCH)

    tilt_rad = math.radians(15.0)
    p_top_x = (PX2 - 110.0) + 50.0 + 580.0 * math.sin(tilt_rad)
    p_top_y = CY2 + 580.0 * math.cos(tilt_rad)
    p_bot_x = (PX2 - 110.0) + 50.0 - 580.0 * math.sin(tilt_rad)
    p_bot_y = CY2 - 580.0 * math.cos(tilt_rad)
    dx_th = 40.0 * math.cos(tilt_rad)
    dy_th = -40.0 * math.sin(tilt_rad)

    draw_wline(p_bot_x, p_bot_y, p_top_x, p_top_y, C_OUTER_BOARD, 2)
    draw_wline(p_top_x, p_top_y, p_top_x + dx_th, p_top_y + dy_th, C_OUTER_BOARD, 2)
    draw_wline(p_top_x + dx_th, p_top_y + dy_th, p_bot_x + dx_th, p_bot_y + dy_th, C_OUTER_BOARD, 2)
    draw_wline(p_bot_x + dx_th, p_bot_y + dy_th, p_bot_x, p_bot_y, C_OUTER_BOARD, 2)

    draw_wline(PX2 + 420.0, CY2 + 180.0, p_top_x - 90.0, CY2 + 90.0, C_INNER_BOARD, 2)
    draw_wline(p_top_x - 90.0, CY2 + 90.0, PX2 + 460.0, CY2 + 620.0, C_INNER_BOARD, 2)
    draw_wtext("入射直射强光", PX2 + 430.0, CY2 + 160.0, f_callout, C_INNER_BOARD)
    draw_wtext("反射眩光折射至天花板无人区", PX2 + 280.0, CY2 + 640.0, f_callout, C_INNER_BOARD)

    # 4.3 节点详图 C-C：导轨自洁截面 (Center X = 5600, Center Y = 1000)
    DX = 5600.0
    draw_wtext("【节点详图 C-C】自洁排灰导轨与悬臂防下垂自锁截面", DX - 380.0, top_y3 + 420.0, f_subhead, C_TEXT)
    draw_wrect(DX - 160.0, CY3 - 110.0, DX + 160.0, CY3 + 110.0, C_FRAME, 2)
    draw_wrect(DX - 120.0, CY3 - 65.0, DX + 120.0, CY3 + 65.0, C_FRAME, 1)
    draw_wline(DX - 180.0, CY3 + 110.0, DX, CY3 + 200.0, C_INNER_HINGE, 2)
    draw_wline(DX, CY3 + 200.0, DX + 180.0, CY3 + 110.0, C_INNER_HINGE, 2)
    draw_wlead(DX, CY3 + 200.0, DX + 100.0, CY3 + 260.0, DX + 220.0, "倒V型EPDM弹性橡胶防护罩", C_INNER_HINGE)
    draw_wcircle(DX, CY3 - 88.0, 16.0, C_INNER_HINGE, 2)
    draw_wlead(DX + 18.0, CY3 - 88.0, DX + 120.0, CY3 - 110.0, DX + 240.0, "垂直贯穿排灰孔(Φ12mm,等距200mm)", C_INNER_HINGE)


    # =========================================================================
    # 模块五：标准图框、参数矩阵表与标题栏 (GB/T 10609.1)
    # =========================================================================
    # 参数表
    TAB_X1, TAB_X2 = -3200.0, 1300.0
    TAB_Y1, TAB_Y2 = -180.0, 320.0
    draw_wrect(TAB_X1, TAB_Y1, TAB_X2, TAB_Y2, C_FRAME, 2)
    draw_wline(TAB_X1, TAB_Y2 - 55.0, TAB_X2, TAB_Y2 - 55.0, C_FRAME, 2)
    draw_wtext("【第三代多维叠合全覆盖与三维自洁侧滑避光黑板系统 - 核心工程参数矩阵】", TAB_X1 + 25.0, TAB_Y2 - 40.0, f_tb_title, C_TEXT)

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
        draw_wtext(s, TAB_X1 + 20.0, sy, f_tb_text, C_TEXT)
        sy -= 42.0

    # 标题栏
    TB_X1, TB_X2 = 1450.0, 6600.0
    TB_Y1, TB_Y2 = -180.0, 320.0
    draw_wrect(TB_X1, TB_Y1, TB_X2, TB_Y2, C_FRAME, 2)
    draw_wline(TB_X1, TB_Y2 - 70.0, TB_X2, TB_Y2 - 70.0, C_FRAME, 2)
    draw_wline(TB_X1, TB_Y1 + 85.0, TB_X2, TB_Y1 + 85.0, C_FRAME, 2)
    draw_wline(TB_X1 + 1050.0, TB_Y1, TB_X1 + 1050.0, TB_Y2, C_FRAME, 2)
    draw_wline(TB_X1 + 2650.0, TB_Y1, TB_X1 + 2650.0, TB_Y2, C_FRAME, 2)
    draw_wline(TB_X1 + 3850.0, TB_Y1, TB_X1 + 3850.0, TB_Y2, C_FRAME, 2)

    draw_wtext("系统代号: GH-Z-2026", TB_X1 + 30.0, TB_Y2 - 48.0, f_tb_title, C_TEXT)
    draw_wtext("图纸名称: 第三代多维叠合全覆盖与自洁侧滑黑板工程总装图", TB_X1 + 1080.0, TB_Y2 - 48.0, f_tb_title, C_TEXT)
    draw_wtext("图号: GH-GEN3-ASM-01", TB_X1 + 3880.0, TB_Y2 - 48.0, f_tb_title, C_TEXT)

    draw_wtext("设计阶段: 第三代(Z系列)终极实施例工程图", TB_X1 + 30.0, TB_Y2 - 125.0, f_tb_text, C_TEXT)
    draw_wtext("设计制图: czx & 海鸥 (Antigravity)", TB_X1 + 1080.0, TB_Y2 - 125.0, f_tb_text, C_TEXT)
    draw_wtext("比例: 1:1 (标准机械毫米制)", TB_X1 + 2680.0, TB_Y2 - 125.0, f_tb_text, C_TEXT)
    draw_wtext("出图规范: 0 Hatch 纯工程机械线框", TB_X1 + 3880.0, TB_Y2 - 125.0, f_tb_text, C_TEXT)

    draw_wtext("审核结论: 第 10 轮全系统工程审核·参数完全吻合通过", TB_X1 + 30.0, TB_Y1 + 30.0, f_tb_text, C_TEXT)
    draw_wtext("适用标准: GB/T 28231-2011 / JY/T 0148-2011 教学黑板标准", TB_X1 + 1080.0, TB_Y1 + 30.0, f_tb_text, C_TEXT)
    draw_wtext("状态: 生产试制与专利附图工程终结版", TB_X1 + 3880.0, TB_Y1 + 30.0, f_tb_text, C_TEXT)

    # 保存图片
    out_path = "/mnt/d/Desktop/pjhb/01-CAD工程图纸/第三代多维叠合翻转全覆盖与三维自洁侧滑黑板系统_全系统工程总装与运动机构图_4K.png"
    img.save(out_path, "PNG")
    print(">>> [成功] 第三代 4K 超高清纯工程机械线框图已生成:", out_path)
    print(">>> 文件大小:", os.path.getsize(out_path), "bytes")

if __name__ == "__main__":
    main()
