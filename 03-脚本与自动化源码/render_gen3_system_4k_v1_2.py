# -*- coding: utf-8 -*-
"""
第三代多维叠合翻转全覆盖与三维自洁侧滑智能黑板系统 - 全系统工程总装与运动机构图 (v1.2 对角线双铰链拓扑版)
5800x4000 4K 超高清纯工程机械线框尺寸图渲染器 (Python Pillow)
核心升级：
1. 主视图中青色翻转铰链、快拆母座与俯仰马达精准布置在外侧黑板边缘 (x = ±2000)；
2. 主视图中品红色折叠铰链设于靠近大屏的内侧边缘 (x = ±1000)；
3. 右侧重点增设【俯视截面详图 A-A：双层黑板模块对角线双铰链拓扑原理 (Top View)】：
   清晰呈现贴合的双层黑板，“里面的外侧是用于翻转的铰链，外面的内侧是用于折叠的铰链，呈对角线分布”；
4. 包含工况三外露滑槽中双横梁高刚性不锈钢伸缩内套杆(两边伸缩的杆)、排灰孔与外端刚性垂直拉杆；
5. 严格 0 Hatch 纯工程机械线框制图，尺寸链与引线全要素避让排版。
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

    # 经典工程 CAD 图层色彩 (严格 0 Hatch 线框)
    C_FRAME = (180, 180, 180)        # 外框、型材
    C_SCREEN = (60, 160, 240)        # 多媒体屏 (蓝色)
    C_OUTER_BOARD = (50, 205, 100)   # 靠墙内层主黑板 (绿色)
    C_INNER_BOARD = (245, 200, 35)   # 朝外外层折叠黑板 (黄色)
    C_FOLD_HINGE = (220, 80, 220)    # 外面的内侧：折叠铺开铰链 (品红)
    C_PITCH_HINGE = (40, 220, 220)   # 里面的外侧：翻转主铰链/快拆母座/俯仰马达 (青色)
    C_EXT = (235, 60, 60)            # 延伸轨、自锁凸台、端部拉杆 (红色)
    C_DIM = (230, 80, 80)            # 尺寸链 (红色)
    C_TEXT = (230, 230, 230)         # 说明文字与标题栏 (白色)
    C_ROD = (255, 140, 0)            # 伸缩套杆与导向套 (高亮橙黄)
    C_DIAG = (0, 255, 255)           # 对角线拓扑连接辅助线 (亮青)

    # 世界坐标系映射范围
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

    def draw_wlead(x1, y1, x2, y2, x3, text, color=C_TEXT, text_offset_y=-11):
        p1 = to_px(x1, y1)
        p2 = to_px(x2, y2)
        p3 = to_px(x3, y2)
        draw.line([p1, p2], fill=color, width=2)
        draw.line([p2, p3], fill=color, width=2)
        draw_wcircle(x1, y1, 4.0, color, width=2)
        tx = p3[0] + 8 if p3[0] > p2[0] else p3[0] - (len(text) * 15) - 8
        draw.text((tx, p3[1] + text_offset_y), text, font=f_callout, fill=color)

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
            draw.text((p1_dim[0] - len(text)*11 - 10, cy - 9), text, font=f_dim, fill=C_DIM)

    # 翻转主铰链与快拆母座绘制函数 (位于里面的外侧 x = ±2000)
    def draw_outer_pitch_hardware(hx, cy_val, side_sign):
        # 承重铰链外耳
        draw_wrect(hx - 20.0, cy_val - 70.0, hx + 20.0, cy_val + 70.0, C_PITCH_HINGE, 2)
        draw_wcircle(hx, cy_val, 12.0, C_PITCH_HINGE, 2)
        # 快拆装配卡挂母座
        draw_wrect(hx - 15.0 * side_sign, cy_val - 35.0, hx + 35.0 * side_sign, cy_val + 35.0, C_PITCH_HINGE, 2)
        draw_wcircle(hx + 15.0 * side_sign, cy_val, 6.0, C_PITCH_HINGE, 2)
        # 蜗轮蜗杆自锁俯仰电机箱
        draw_wrect(hx - 25.0 * side_sign, cy_val + 80.0, hx + 25.0 * side_sign, cy_val + 160.0, C_PITCH_HINGE, 2)
        draw_wcircle(hx, cy_val + 120.0, 14.0, C_PITCH_HINGE, 2)

    # 折叠铺开铰链绘制函数 (位于外面的内侧 x = ±1000)
    def draw_inner_fold_hinge(hx, cy_val):
        draw_wrect(hx - 15.0, cy_val - 250.0, hx + 15.0, cy_val - 150.0, C_FOLD_HINGE, 2)
        draw_wcircle(hx, cy_val - 200.0, 8.0, C_FOLD_HINGE, 2)
        draw_wrect(hx - 15.0, cy_val + 150.0, hx + 15.0, cy_val + 250.0, C_FOLD_HINGE, 2)
        draw_wcircle(hx, cy_val + 200.0, 8.0, C_FOLD_HINGE, 2)

    H_SCREEN_FRAME = 1200.0
    H_LCD = 1070.0

    # =========================================================================
    # 模块一：工况一【初始闭合·市面主流全覆盖封屏形态】 (Center Y = 4600.0)
    # 里面的外侧设翻转主铰链，外面的内侧设折叠铰链向中心铺开展平180°合拢封屏
    # =========================================================================
    CY1 = 4600.0
    top_y1 = CY1 + 600.0
    bot_y1 = CY1 - 600.0

    draw_wtext("第三代工况一：初始闭合·市面主流全覆盖封屏形态 [COVERED - 传统主流全封闭 4000mm]", -3050.0, top_y1 + 420.0, f_title, C_TEXT)
    draw_wtext("技术特征: 左右黑板成二分层；靠大屏内侧设折叠铰链向中心铺开180°并对撞合拢，100%完全遮蔽86寸大屏；外侧保留翻转承重铰链与快拆母座。", -3050.0, top_y1 + 365.0, f_subtitle, C_TEXT)

    # 后方被完全遮蔽的 86 寸大屏 (虚线勾勒)
    draw_wrect(-1000.0, bot_y1, 1000.0, top_y1, C_SCREEN, 1)
    draw_wline(-1000.0, bot_y1, 1000.0, top_y1, C_SCREEN, 1, dashed=True)
    draw_wline(-1000.0, top_y1, 1000.0, bot_y1, C_SCREEN, 1, dashed=True)
    draw_wtext("[86寸多媒体大屏被100%封闭在背后保护防撞]", -700.0, CY1 + 250.0, f_callout, C_SCREEN)

    # 左右靠墙内层主板 (在原位 X: -2000~-1000, 1000~2000)
    draw_wrect(-2000.0, bot_y1, -1000.0, top_y1, C_OUTER_BOARD, 2)
    draw_wrect(-1980.0, bot_y1 + 20.0, -1020.0, top_y1 - 20.0, C_OUTER_BOARD, 1)
    draw_wrect(1000.0, bot_y1, 2000.0, top_y1, C_OUTER_BOARD, 2)
    draw_wrect(1020.0, bot_y1 + 20.0, 1980.0, top_y1 - 20.0, C_OUTER_BOARD, 1)

    # 铺开在大屏正前方朝外的左右外层折叠板 (X: -1000~0, 0~1000)
    draw_wrect(-1000.0, bot_y1, 0.0, top_y1, C_INNER_BOARD, 2)
    draw_wrect(-980.0, bot_y1 + 20.0, -20.0, top_y1 - 20.0, C_INNER_BOARD, 1)
    draw_wrect(0.0, bot_y1, 1000.0, top_y1, C_INNER_BOARD, 2)
    draw_wrect(20.0, bot_y1 + 20.0, 980.0, top_y1 - 20.0, C_INNER_BOARD, 1)

    # 【里面的外侧 x = ±2000】：翻转承重铰链、快拆母座与俯仰电机
    draw_outer_pitch_hardware(-2000.0, CY1, -1)
    draw_outer_pitch_hardware(2000.0, CY1, 1)

    # 【外面的内侧 x = ±1000】：折叠铺开铰链
    draw_inner_fold_hinge(-1000.0, CY1)
    draw_inner_fold_hinge(1000.0, CY1)

    # 引线说明 (外开排版)
    draw_wlead(-2020.0, CY1, -2180.0, CY1 + 100.0, -2350.0, "里面的外侧: 翻转主铰链与快拆母座(水平翻转/俯仰避光)", C_PITCH_HINGE)
    draw_wlead(-1000.0, CY1 + 200.0, -1180.0, CY1 + 270.0, -1320.0, "外面的内侧: 折叠铺开铰链(向内铺展180°封屏)", C_FOLD_HINGE)
    draw_wlead(0.0, CY1, 180.0, CY1 + 80.0, 320.0, "中央碰珠式磁吸机械对撞锁紧缝(全覆盖平整拼接)", C_INNER_BOARD)

    # 尺寸标注 (工况一：严密三层尺寸链)
    draw_wdim(-2000.0, top_y1, -1000.0, top_y1, 100.0, True, "1000 [内层主板]")
    draw_wdim(-1000.0, top_y1, 0.0, top_y1, 100.0, True, "1000 [铺开折叠板A]")
    draw_wdim(0.0, top_y1, 1000.0, top_y1, 100.0, True, "1000 [铺开折叠板B]")
    draw_wdim(1000.0, top_y1, 2000.0, top_y1, 100.0, True, "1000 [内层主板]")
    draw_wdim(-1000.0, top_y1, 1000.0, top_y1, 180.0, True, "2000 [全覆盖完全遮蔽大屏跨度]")
    draw_wdim(-2000.0, top_y1, 2000.0, top_y1, 260.0, True, "4000 [主流全覆盖纯板书总跨度]")


    # =========================================================================
    # 模块二：工况二【常态多媒体·大屏露显双层叠合形态】 (Center Y = 2800.0)
    # 两板贴合收拢，外面的内侧铰链折回贴合，里面的外侧铰链挂载，露显 86 寸大屏
    # =========================================================================
    CY2 = 2800.0
    top_y2 = CY2 + 600.0
    bot_y2 = CY2 - 600.0

    draw_wtext("第三代工况二：常态多媒体·大屏露显双层叠合形态 [COMPACT - 黄金视域 4000mm]", -3050.0, top_y2 + 420.0, f_title, C_TEXT)
    draw_wtext("技术特征: 内缘折叠铰链折回180°，两块黑板紧密贴合(叠合厚度仅26mm)；86寸多媒体屏完全露显；里面的外侧为翻转铰链，外面的内侧为折叠铰链。", -3050.0, top_y2 + 365.0, f_subtitle, C_TEXT)

    # 中心大屏完全露显
    draw_wrect(-1000.0, bot_y2, 1000.0, top_y2, C_FRAME, 2)
    draw_wrect(-950.0, bot_y2 + 65.0, 950.0, bot_y2 + 65.0 + H_LCD, C_SCREEN, 2)
    draw_wrect(-940.0, bot_y2 + 75.0, 940.0, bot_y2 + 55.0 + H_LCD, C_SCREEN, 1)

    # 大屏右内侧微型伺服电机与偏光膜齿圈
    draw_wrect(915.0, bot_y2 + 250.0, 935.0, bot_y2 + 450.0, C_INNER_BOARD, 2)
    draw_wcircle(925.0, bot_y2 + 470.0, 15.0, C_INNER_BOARD, 2)
    draw_wline(940.0, bot_y2 + 100.0, 940.0, bot_y2 + 1100.0, C_INNER_BOARD, 2)

    # 左右双层附加叠合板 (内层主板 + 外层折叠板紧密贴合)
    for side in [-1, 1]:
        bx1 = 1000.0 * side
        bx2 = 2000.0 * side
        draw_wrect(bx1, bot_y2, bx2, top_y2, C_OUTER_BOARD, 2)
        draw_wrect(bx1 + (20.0*side), bot_y2 + 20.0, bx2 - (20.0*side), top_y2 - 20.0, C_OUTER_BOARD, 1)
        draw_wrect(bx1 + (10.0*side), bot_y2 + 10.0, bx2 - (10.0*side), top_y2 - 10.0, C_INNER_BOARD, 2)

    # 【里面的外侧 x = ±2000】：设置青色翻转主铰链与快拆母座/俯仰马达
    draw_outer_pitch_hardware(-2000.0, CY2, -1)
    draw_outer_pitch_hardware(2000.0, CY2, 1)

    # 【外面的内侧 x = ±1000】：设置品红色折叠铰链
    draw_inner_fold_hinge(-1000.0, CY2)
    draw_inner_fold_hinge(1000.0, CY2)

    # 板面文字标注 (排版在板面内部，清晰无干涉)
    draw_wtext("双层附加叠合黑板面", -1780.0, CY2 + 50.0, f_subhead, C_INNER_BOARD)
    draw_wtext("(内层主板12mm + 外层折叠板12mm 紧密贴合)", -1960.0, CY2 - 10.0, f_callout, C_INNER_BOARD)

    # 引线标注 (引向外侧与屏幕空旷区)
    draw_wlead(-2020.0, CY2, -2180.0, CY2 + 100.0, -2350.0, "里面的外侧: 标准化快拆卡挂母座与俯仰马达", C_PITCH_HINGE)
    draw_wlead(-1000.0, CY2 + 200.0, -850.0, CY2 + 270.0, -680.0, "外面的内侧: 折叠铰链(回折180°紧密贴合)", C_FOLD_HINGE)
    draw_wlead(2020.0, CY2, 2180.0, CY2 + 100.0, 2350.0, "里面的外侧: 翻转主铰链轴(支持全模块水平偏航避光翻转)", C_PITCH_HINGE)

    # 尺寸标注 (工况二)
    draw_wdim(-2000.0, top_y2, -1000.0, top_y2, 100.0, True, "1000 [双层叠合黑板]")
    draw_wdim(-1000.0, top_y2, 1000.0, top_y2, 100.0, True, "2000 [86寸多媒体大屏]")
    draw_wdim(1000.0, top_y2, 2000.0, top_y2, 100.0, True, "1000 [双层叠合黑板]")
    draw_wdim(-2000.0, top_y2, 2000.0, top_y2, 180.0, True, "4000 [常态多媒体教学总跨度]")


    # =========================================================================
    # 模块三：工况三【大视野与三维空间避光极限展开形态】 (Center Y = 1000.0)
    # 双层黑板沿自洁滑轨向外侧滑1.0米，双梁高刚性伸缩内套杆承托，幅宽展至6000mm
    # =========================================================================
    CY3 = 1000.0
    top_y3 = CY3 + 600.0
    bot_y3 = CY3 - 600.0

    draw_wtext("第三代工况三：大视野与三维空间避光极限展开形态 [DEPLOYED - 盲区归零 6000mm]", -3050.0, top_y3 + 420.0, f_title, C_TEXT)
    draw_wtext("技术特征: 双层叠合板沿双横梁自洁导轨外滑1000mm；高刚性不锈钢伸缩套杆承托；外端刚性垂直拉杆闭环锁定上下滑轨；翻转铰链随动外展。", -3050.0, top_y3 + 365.0, f_subtitle, C_TEXT)

    # 中心大屏露显
    draw_wrect(-1000.0, bot_y3, 1000.0, top_y3, C_FRAME, 2)
    draw_wrect(-950.0, bot_y3 + 65.0, 950.0, bot_y3 + 65.0 + H_LCD, C_SCREEN, 2)

    # 中间 1000mm 外露自洁滑槽与双横梁固定外框 (左侧 -2000~-1000，右侧 1000~2000)
    for side in [-1, 1]:
        gap_x1 = 1000.0 * side
        gap_x2 = 2000.0 * side
        draw_wrect(gap_x1, top_y3 - 65.0, gap_x2, top_y3, C_FRAME, 2)
        draw_wrect(gap_x1, bot_y3, gap_x2, bot_y3 + 65.0, C_FRAME, 2)

        # C型槽底 5 组贯穿垂直排灰孔
        for i in range(5):
            hole_x = gap_x1 + (100.0 + i * 200.0) * (1 if side > 0 else -1)
            draw_wcircle(hole_x, top_y3 - 32.5, 6.0, C_FOLD_HINGE, 2)
            draw_wcircle(hole_x, bot_y3 + 32.5, 6.0, C_FOLD_HINGE, 2)

        # 高刚性不锈钢伸缩内套杆 (两边伸缩的杆：上、下各一根 Φ28x2.5mm SUS304)
        rod_top_y = top_y3 - 32.5
        draw_wline(gap_x1, rod_top_y, gap_x2 + 300.0 * side, rod_top_y, C_ROD, 4)
        draw_wrect(gap_x1, rod_top_y - 8.0, gap_x1 + 120.0 * side, rod_top_y + 8.0, C_ROD, 2)
        draw_wrect(gap_x2 - 120.0 * side, rod_top_y - 8.0, gap_x2, rod_top_y + 8.0, C_ROD, 2)

        rod_bot_y = bot_y3 + 32.5
        draw_wline(gap_x1, rod_bot_y, gap_x2 + 300.0 * side, rod_bot_y, C_ROD, 4)
        draw_wrect(gap_x1, rod_bot_y - 8.0, gap_x1 + 120.0 * side, rod_bot_y + 8.0, C_ROD, 2)
        draw_wrect(gap_x2 - 120.0 * side, rod_bot_y - 8.0, gap_x2, rod_bot_y + 8.0, C_ROD, 2)

        draw_wline(gap_x1, CY3, gap_x2, CY3, C_ROD, 2, dashed=True)
        draw_wcircle(gap_x1 + 500.0 * side, CY3, 10.0, C_ROD, 2)

    # 左右外滑活动黑板主体 (位置扩展至 -3000~-2000, 2000~3000)
    draw_wrect(-3000.0, bot_y3, -2000.0, top_y3, C_OUTER_BOARD, 2)
    draw_wrect(-2980.0, bot_y3 + 20.0, -2020.0, top_y3 - 20.0, C_OUTER_BOARD, 1)
    draw_wrect(-2990.0, bot_y3 + 10.0, -2010.0, top_y3 - 10.0, C_INNER_BOARD, 2)
    draw_wcircle(-2500.0, CY3, 15.0, C_EXT, 2)

    draw_wrect(2000.0, bot_y3, 3000.0, top_y3, C_EXT, 2)
    draw_wrect(2020.0, bot_y3 + 20.0, 2980.0, top_y3 - 20.0, C_FRAME, 1)
    draw_wcircle(2500.0, CY3, 15.0, C_EXT, 2)
    draw_wtext("[异质选配: 翻面展露白色防眩搪瓷书写/投影板]", 2060.0, CY3 - 80.0, f_callout, C_TEXT)

    # 随板外移的【里面的外侧翻转铰链与母座】(外展至 x = ±3000)
    draw_outer_pitch_hardware(-3000.0, CY3, -1)
    draw_outer_pitch_hardware(3000.0, CY3, 1)

    # 随板外移的【外面的内侧折叠铰链】(外展至 x = ±2000)
    draw_inner_fold_hinge(-2000.0, CY3)
    draw_inner_fold_hinge(2000.0, CY3)

    # 两端刚性垂直端部拉杆 (End Tie Rods)
    draw_wrect(-3018.0, bot_y3 - 15.0, -2995.0, top_y3 + 15.0, C_EXT, 3)
    draw_wcircle(-3006.5, top_y3, 5.0, C_EXT, 2)
    draw_wcircle(-3006.5, bot_y3, 5.0, C_EXT, 2)

    draw_wrect(2995.0, bot_y3 - 15.0, 3018.0, top_y3 + 15.0, C_EXT, 3)
    draw_wcircle(3006.5, top_y3, 5.0, C_EXT, 2)
    draw_wcircle(3006.5, bot_y3, 5.0, C_EXT, 2)

    # 偏心自锁卡扣
    for side in [-1, 1]:
        wx = 2000.0 * side
        draw_wrect(wx - 25.0 * side, top_y3 - 55.0, wx + 25.0 * side, top_y3 - 15.0, C_EXT, 2)
        draw_wline(wx - 25.0 * side, top_y3 - 15.0, wx + 25.0 * side, top_y3 - 40.0, C_EXT, 2)
        draw_wrect(wx - 25.0 * side, bot_y3 + 15.0, wx + 25.0 * side, bot_y3 + 55.0, C_EXT, 2)
        draw_wline(wx - 25.0 * side, bot_y3 + 40.0, wx + 25.0 * side, bot_y3 + 15.0, C_EXT, 2)

    # 引线安全避让标注
    draw_wlead(-1500.0, top_y3 - 32.5, -1500.0, CY3 + 120.0, -1950.0, "横向双横梁高刚性不锈钢伸缩套杆(Φ28x2.5mm,承托1.0m滑移悬臂)", C_ROD)
    draw_wlead(1500.0, bot_y3 + 32.5, 1500.0, CY3 - 100.0, 1080.0, "C型槽底垂直排灰孔(Φ12mm,等间距200mm,消气阻)", C_FOLD_HINGE)
    draw_wlead(1980.0, top_y3 - 35.0, 1820.0, CY3 + 160.0, 1150.0, "偏心楔形自锁防下垂凸台与锁紧卡口(3.5°斜面消隙)", C_EXT)
    draw_wlead(3018.0, CY3 + 150.0, 3180.0, CY3 + 240.0, 3350.0, "刚性垂直端部拉杆(双端机械闭环锁定上下滑轨)", C_EXT)
    draw_wlead(-3018.0, CY3 + 150.0, -3160.0, CY3 + 240.0, -3320.0, "刚性垂直端部拉杆(闭环锁紧)", C_EXT)

    # 规范尺寸链 (工况三)
    draw_wdim(-3000.0, top_y3, -2000.0, top_y3, 100.0, True, "1000 [外展叠合黑板]")
    draw_wdim(-2000.0, top_y3, -1000.0, top_y3, 100.0, True, "1000 [伸缩套杆与外露滑槽]")
    draw_wdim(-1000.0, top_y3, 1000.0, top_y3, 100.0, True, "2000 [86寸多媒体大屏]")
    draw_wdim(1000.0, top_y3, 2000.0, top_y3, 100.0, True, "1000 [伸缩套杆与外露滑槽]")
    draw_wdim(2000.0, top_y3, 3000.0, top_y3, 100.0, True, "1000 [外展叠合黑板]")
    draw_wdim(-3000.0, top_y3, 3000.0, top_y3, 180.0, True, "6000 [侧滑平移推拉展开极限总跨度]")


    # =========================================================================
    # 模块四：右侧专业剖面与详图
    # 【核心新增】详图 A-A：双层贴合黑板模块对角线双铰链拓扑俯视图 (Top View)
    # 里面的外侧是翻转铰链，外面的内侧是折叠铰链，两者成对角线分布！
    # =========================================================================
    PX1 = 4900.0

    draw_wtext("【俯视机构详图 A-A】双层叠合黑板模块对角线双铰链拓扑原理 (Top View)", 3550.0, 5140.0, f_subhead, C_TEXT)
    draw_wtext("机构核心: 里面板的外侧设翻转主铰链，外面板的内侧设折叠铺开铰链，空间成对角线正交排布，两组运动副完全解耦零干涉。", 3550.0, 5090.0, f_subtitle, C_TEXT)

    # 1. 建筑墙体基准线与上滑轨截面
    wall_y = 5000.0
    draw_wline(3400.0, wall_y, 6500.0, wall_y, C_FRAME, 1, dashed=True)
    draw_wtext("【建筑承重墙体基准面 (Wall Datum)】", 3450.0, wall_y + 35.0, f_dim, C_FRAME)

    # 上滑轨型材截面 (双槽截面，高强铝合金)
    draw_wrect(3400.0, wall_y - 40.0, 6500.0, wall_y - 12.0, C_FRAME, 2)
    draw_wtext("双滑槽重载铝合金上导轨型材 (含自洁排灰槽与缓冲限位块)", 5300.0, wall_y - 32.0, f_dim, C_FRAME)

    # 2. 俯视基准：中间大屏边框截面
    screen_x1 = 3380.0
    screen_x2 = 4380.0
    screen_y_top = wall_y - 65.0
    screen_y_bot = screen_y_top - 70.0
    draw_wrect(screen_x1, screen_y_bot, screen_x2, screen_y_top, C_SCREEN, 2)
    draw_wtext("86寸多媒体大屏框体截面 (厚70mm, 挂墙安装于基准面)", screen_x1 + 60.0, screen_y_bot + 24.0, f_callout, C_SCREEN)

    # 3. 双层贴合黑板模块 (俯视：板长 1000mm，厚度各 26mm，严格层级排布)
    b_len = 1000.0
    th = 24.0

    x_inner = 4440.0                # 靠近大屏的内侧边缘
    x_outer = x_inner + b_len       # 远离大屏的外侧边缘 (5440.0)

    y_wall = screen_y_bot - 45.0    # 里面的内层主板中心 (4820.0)
    y_front = y_wall - 175.0        # 外面的外层折叠板中心 (4645.0)

    # 【里面的板】内层主板 (绿色)
    draw_wrect(x_inner, y_wall - th/2.0, x_outer, y_wall + th/2.0, C_OUTER_BOARD, 2)
    draw_wtext("【里面的主板】厚12mm·挂载于滑块与外侧翻转母座", x_inner + 40.0, y_wall + 20.0, f_callout, C_OUTER_BOARD)

    # 【外面的板】外层折叠板 (黄色) - 常态贴合
    draw_wrect(x_inner, y_front - th/2.0, x_outer, y_front + th/2.0, C_INNER_BOARD, 2)
    draw_wtext("【外面的折叠板】厚12mm·具有正反双面书写板·平时贴合", x_inner + 40.0, y_front - 32.0, f_callout, C_INNER_BOARD)

    # 4. 【关键铰链 1：里面的外侧 -> 翻转主铰链 (青色)】
    # 位置：x = x_outer (外侧 5440), y = y_wall (里面 4820)
    h_outer_x = x_outer
    h_outer_y = y_wall
    draw_wcircle(h_outer_x, h_outer_y, 24.0, C_PITCH_HINGE, 3)
    draw_wcircle(h_outer_x, h_outer_y, 10.0, C_PITCH_HINGE, 2)
    draw_wrect(h_outer_x - 14.0, h_outer_y - 28.0, h_outer_x + 36.0, h_outer_y + 28.0, C_PITCH_HINGE, 2)
    # 导向滑块法兰
    draw_wrect(h_outer_x - 16.0, h_outer_y + 28.0, h_outer_x + 28.0, wall_y - 40.0, C_FRAME, 2)
    draw_wtext("重载导向滑块", h_outer_x - 18.0, wall_y - 58.0, f_dim, C_FRAME)
    # 引线向右上方舒展引出
    draw_wlead(h_outer_x + 12.0, h_outer_y + 15.0, h_outer_x + 90.0, h_outer_y + 70.0, h_outer_x + 210.0, "①【里面的外侧】: 翻转主铰链 (承重转轴/快拆母座/偏航转动及俯仰)", C_PITCH_HINGE)

    # 5. 【关键铰链 2：外面的内侧 -> 折叠铰链 (品红色)】
    # 位置：x = x_inner (内侧 4440), y = y_front (外面 4645)
    h_inner_x = x_inner
    h_inner_y = y_front
    draw_wcircle(h_inner_x, h_inner_y, 22.0, C_FOLD_HINGE, 3)
    draw_wcircle(h_inner_x, h_inner_y, 9.0, C_FOLD_HINGE, 2)
    draw_wrect(h_inner_x - 36.0, h_inner_y - 26.0, h_inner_x + 14.0, h_inner_y + 26.0, C_FOLD_HINGE, 2)
    # 引线向左下方舒展引出
    draw_wlead(h_inner_x - 12.0, h_inner_y - 15.0, h_inner_x - 80.0, h_inner_y - 65.0, h_inner_x - 200.0, "②【外面的内侧】: 多维折叠铺开铰链 (向中心铺开180°封屏)", C_FOLD_HINGE, text_offset_y=-22)

    # 6. 【对角线分布连接指示线 (Diagonal Topology)】
    draw_wline(h_inner_x, h_inner_y, h_outer_x, h_outer_y, C_DIAG, 3, dashed=True)
    mid_diag_x = (h_inner_x + h_outer_x) / 2.0
    mid_diag_y = (h_inner_y + h_outer_y) / 2.0
    draw_wcircle(mid_diag_x, mid_diag_y, 14.0, C_DIAG, 2)
    # 对角线说明采用专用安全引线框引出至最下方纯净开阔区 (y = 4520)
    draw_wlead(mid_diag_x, mid_diag_y, mid_diag_x + 80.0, 4520.0, mid_diag_x + 220.0, "★ 成对角线分布 (Diagonal Topology): 内侧折叠轴与外侧翻转轴正交解耦，机构零干涉 ★", C_DIAG, text_offset_y=-12)

    # 7. 运动轨迹 1：外层板以【外面的内侧铰链】为轴向左铺开 180° 封屏状态虚线
    unfold_x1 = h_inner_x - b_len
    unfold_x2 = h_inner_x
    draw_wrect(unfold_x1, y_front - th/2.0, unfold_x2, y_front + th/2.0, C_FOLD_HINGE, 2)
    draw_wline(unfold_x1, y_front - th/2.0, unfold_x2, y_front + th/2.0, C_FOLD_HINGE, 1, dashed=True)
    # 文字放在展开板框内部正中央
    draw_wtext("【180°铺开展平封屏状态】紧密遮蔽86寸多媒体大屏", unfold_x1 + 100.0, y_front - 10.0, f_callout, C_FOLD_HINGE)

    # 180° 翻折轨迹圆弧
    p_hinge_px = to_px(h_inner_x, h_inner_y)
    r_sweep_px = 140.0 * SCALE
    draw.arc([p_hinge_px[0] - r_sweep_px, p_hinge_px[1] - r_sweep_px, p_hinge_px[0] + r_sweep_px, p_hinge_px[1] + r_sweep_px], start=90, end=270, fill=C_FOLD_HINGE, width=2)
    draw_wtext("180°铺发展平轨迹", h_inner_x - 140.0, y_front + 80.0, f_dim, C_FOLD_HINGE)

    # 8. 运动轨迹 2：整套双层黑板以【里面的外侧铰链】为轴水平旋转偏航避光状态虚线 (以 θ = 20° 为例)
    yaw_rad = math.radians(20.0)
    yaw_cos = math.cos(yaw_rad)
    yaw_sin = math.sin(yaw_rad)
    yaw_end_x = h_outer_x - b_len * yaw_cos
    yaw_end_y = h_outer_y - b_len * yaw_sin
    draw_wline(h_outer_x, h_outer_y, yaw_end_x, yaw_end_y, C_PITCH_HINGE, 2, dashed=True)
    draw_wtext("整机水平偏航避光旋转态 (绕外侧主铰链转动)", yaw_end_x + 60.0, yaw_end_y - 25.0, f_dim, C_PITCH_HINGE)

    # 翻转轨迹圆弧
    p_outer_px = to_px(h_outer_x, h_outer_y)
    r_yaw_px = 180.0 * SCALE
    draw.arc([p_outer_px[0] - r_yaw_px, p_outer_px[1] - r_yaw_px, p_outer_px[0] + r_yaw_px, p_outer_px[1] + r_yaw_px], start=180, end=210, fill=C_PITCH_HINGE, width=2)
    draw_wtext("水平避光回转轨迹", h_outer_x - 190.0, h_outer_y - 55.0, f_dim, C_PITCH_HINGE)



    # 4.2 剖面 B-B：纵向俯仰避光原理 (Center X = 4300, Center Y = 2800)
    PX2 = 4300.0
    draw_wtext("【剖面视图 B-B】纵向俯仰避光与光锥折射原理 (-15°~+15°)", PX2 - 320.0, top_y2 + 420.0, f_subhead, C_TEXT)
    draw_wrect(PX2 - 240.0, CY2 - 300.0, PX2 - 190.0, CY2 + 300.0, C_FRAME, 2)
    draw_wrect(PX2 - 190.0, CY2 - 60.0, PX2 - 110.0, CY2 + 60.0, C_PITCH_HINGE, 2)
    draw_wcircle(PX2 - 110.0, CY2, 18.0, C_PITCH_HINGE, 2)
    draw_wtext("水平铰接销轴(Pitch轴)", PX2 - 100.0, CY2 - 35.0, f_callout, C_PITCH_HINGE)

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


    # 4.3 节点详图 C-C：导轨自洁截面与套杆配合 (Center X = 5600, Center Y = 1000)
    DX = 5600.0
    draw_wtext("【节点详图 C-C】自洁排灰导轨与伸缩套杆/防下垂截面", DX - 380.0, top_y3 + 420.0, f_subhead, C_TEXT)
    draw_wrect(DX - 160.0, CY3 - 110.0, DX + 160.0, CY3 + 110.0, C_FRAME, 2)
    draw_wrect(DX - 120.0, CY3 - 65.0, DX + 120.0, CY3 + 65.0, C_FRAME, 1)
    draw_wcircle(DX, CY3, 35.0, C_ROD, 3)
    draw_wcircle(DX, CY3, 25.0, C_ROD, 2)
    draw_wlead(DX, CY3 + 35.0, DX + 90.0, CY3 + 90.0, DX + 200.0, "SUS304伸缩套杆(Φ28x2.5mm)", C_ROD)

    draw_wline(DX - 180.0, CY3 + 110.0, DX, CY3 + 200.0, C_FOLD_HINGE, 2)
    draw_wline(DX, CY3 + 200.0, DX + 180.0, CY3 + 110.0, C_FOLD_HINGE, 2)
    draw_wlead(DX, CY3 + 200.0, DX + 100.0, CY3 + 260.0, DX + 220.0, "倒V型EPDM弹性橡胶防护罩", C_FOLD_HINGE)
    draw_wcircle(DX, CY3 - 88.0, 16.0, C_FOLD_HINGE, 2)
    draw_wlead(DX + 18.0, CY3 - 88.0, DX + 120.0, CY3 - 110.0, DX + 240.0, "垂直贯穿排灰孔(Φ12mm,等距200mm)", C_FOLD_HINGE)


    # =========================================================================
    # 模块五：标准图框、参数矩阵表与标题栏 (GB/T 10609.1)
    # =========================================================================
    TAB_X1, TAB_X2 = -3200.0, 1300.0
    TAB_Y1, TAB_Y2 = -180.0, 320.0
    draw_wrect(TAB_X1, TAB_Y1, TAB_X2, TAB_Y2, C_FRAME, 2)
    draw_wline(TAB_X1, TAB_Y2 - 55.0, TAB_X2, TAB_Y2 - 55.0, C_FRAME, 2)
    draw_wtext("【第三代多维叠合全覆盖与三维自洁侧滑避光黑板系统 - 核心工程参数矩阵】", TAB_X1 + 25.0, TAB_Y2 - 40.0, f_tb_title, C_TEXT)

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
        draw_wtext(s, TAB_X1 + 20.0, sy, f_tb_text, C_TEXT)
        sy -= 42.0

    TB_X1, TB_X2 = 1450.0, 6600.0
    TB_Y1, TB_Y2 = -180.0, 320.0
    draw_wrect(TB_X1, TB_Y1, TB_X2, TB_Y2, C_FRAME, 2)
    draw_wline(TB_X1, TB_Y2 - 70.0, TB_X2, TB_Y2 - 70.0, C_FRAME, 2)
    draw_wline(TB_X1, TB_Y1 + 85.0, TB_X2, TB_Y1 + 85.0, C_FRAME, 2)
    draw_wline(TB_X1 + 1050.0, TB_Y1, TB_X1 + 1050.0, TB_Y2, C_FRAME, 2)
    draw_wline(TB_X1 + 2650.0, TB_Y1, TB_X1 + 2650.0, TB_Y2, C_FRAME, 2)
    draw_wline(TB_X1 + 3800.0, TB_Y1, TB_X1 + 3800.0, TB_Y2, C_FRAME, 2)

    draw_wtext("系统代号：GH-Z-2026", TB_X1 + 30.0, TB_Y2 - 45.0, f_subhead, C_TEXT)
    draw_wtext("设计阶段：第三代 (Z系列) 终极实施例工程图 v1.2", TB_X1 + 30.0, TB_Y1 + 110.0, f_callout, C_TEXT)

    draw_wtext("图纸名称：第三代多维叠合全覆盖与自洁侧滑黑板工程总装图", TB_X1 + 1080.0, TB_Y2 - 45.0, f_subhead, C_TEXT)
    draw_wtext("设计/制图：czx & 海鸥 (Antigravity)", TB_X1 + 1080.0, TB_Y1 + 110.0, f_callout, C_TEXT)

    draw_wtext("比例：1:1 (标准机械毫米制)", TB_X1 + 2680.0, TB_Y2 - 45.0, f_subhead, C_TEXT)

    draw_wtext("图号：GH-GEN3-ASM-03", TB_X1 + 3830.0, TB_Y2 - 45.0, f_subhead, C_TEXT)
    draw_wtext("出图规范：0 Hatch 纯工程机械线框", TB_X1 + 3830.0, TB_Y1 + 110.0, f_callout, C_TEXT)

    draw_wtext("审核结论：第 12 轮全系统工程复核·里面的外侧翻转铰链+外面的内侧折叠铰链(对角线拓扑俯视)闭环通过", TB_X1 + 30.0, TB_Y1 + 30.0, f_callout, C_TEXT)
    draw_wtext("通用标准：GB/T 28231-2011 / JY/T 0148-2011 教学黑板标准", TB_X1 + 1750.0, TB_Y1 + 30.0, f_callout, C_TEXT)
    draw_wtext("状态：生产试制与专利附图工程终结稿", TB_X1 + 3830.0, TB_Y1 + 30.0, f_callout, C_TEXT)

    draw_wrect(-3350.0, -280.0, 6720.0, 5350.0, C_FRAME, 3)
    draw_wrect(-3330.0, -260.0, 6700.0, 5330.0, C_FRAME, 1)

    out_png_v1_2 = "/mnt/d/Desktop/pjhb/01-CAD工程图纸/第三代多维叠合翻转全覆盖与三维自洁侧滑黑板系统_全系统工程总装与运动机构图_4K_v1.2.png"
    out_png_main = "/mnt/d/Desktop/pjhb/01-CAD工程图纸/第三代多维叠合翻转全覆盖与三维自洁侧滑黑板系统_全系统工程总装与运动机构图_4K.png"

    img.save(out_png_v1_2, "PNG")
    print("SUCCESS: 4K PNG rendered to", out_png_v1_2)
    try:
        img.save(out_png_main, "PNG")
        print("Updated main 4K.png successfully")
    except Exception as e:
        print("Notice: main 4K.png locked, v1.2 safe:", e)

if __name__ == '__main__':
    main()
