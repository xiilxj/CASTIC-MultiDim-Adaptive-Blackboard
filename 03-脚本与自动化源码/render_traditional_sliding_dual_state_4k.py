# -*- coding: utf-8 -*-
"""
传统市面标准多媒体教学推拉黑板 (86寸配双扇书写板) - 双工况对比与完全覆盖工程尺寸图 (v2.1)
4K 超高清纯线框工程尺寸图渲染器 (Python Pillow)
输出路径: D:\Desktop\pjhb\01-CAD工程图纸\传统市面标准推拉黑板_双状态全覆盖与尺寸标注工程图_4K.png
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

def main():
    IMG_W = 4200
    IMG_H = 4400
    BG_COLOR = (24, 26, 31)  # 经典暗色工程 CAD 底色

    img = Image.new("RGB", (IMG_W, IMG_H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 载入字体
    font_path = "/mnt/c/Windows/Fonts/simhei.ttf"
    if not os.path.exists(font_path):
        font_path = "/usr/share/fonts/wenquanyi/wqy-microhei/wqy-microhei.ttc"
    
    def get_font(size):
        try:
            return ImageFont.truetype(font_path, size)
        except:
            return ImageFont.load_default()

    f_title = get_font(44)
    f_subtitle = get_font(34)
    f_subhead = get_font(30)
    f_dim = get_font(24)
    f_note = get_font(21)
    f_small = get_font(18)

    # 坐标变换系统
    WORLD_X1 = -550.0
    WORLD_X2 = 4650.0
    WORLD_Y1 = -780.0
    WORLD_Y2 = 4520.0

    PAD_X = 80
    PAD_Y = 80
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

    def draw_line(wx1, wy1, wx2, wy2, color=(220, 220, 220), width=2, dashed=False):
        p1 = to_px(wx1, wy1)
        p2 = to_px(wx2, wy2)
        if not dashed:
            draw.line([p1, p2], fill=color, width=width)
        else:
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            dist = math.hypot(dx, dy)
            if dist == 0:
                return
            dash_len = 16.0
            gap_len = 10.0
            curr = 0.0
            while curr < dist:
                t1 = curr / dist
                t2 = min((curr + dash_len) / dist, 1.0)
                sp = (p1[0] + dx * t1, p1[1] + dy * t1)
                ep = (p1[0] + dx * t2, p1[1] + dy * t2)
                draw.line([sp, ep], fill=color, width=width)
                curr += dash_len + gap_len

    def draw_rect(wx1, wy1, wx2, wy2, color=(220, 220, 220), width=2, dashed=False):
        draw_line(wx1, wy1, wx2, wy1, color, width, dashed)
        draw_line(wx2, wy1, wx2, wy2, color, width, dashed)
        draw_line(wx2, wy2, wx1, wy2, color, width, dashed)
        draw_line(wx1, wy2, wx1, wy1, color, width, dashed)

    def draw_circle(wcx, wcy, wr, color=(220, 220, 220), width=2):
        cx, cy = to_px(wcx, wcy)
        r = wr * SCALE
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=width)

    def draw_arrow_head(px, py, angle_rad, length=18.0, width=8.0, color=(255, 220, 0)):
        p_tip = (px, py)
        p_left = (
            px - length * math.cos(angle_rad) + width * math.sin(angle_rad),
            py - length * math.sin(angle_rad) - width * math.cos(angle_rad)
        )
        p_right = (
            px - length * math.cos(angle_rad) - width * math.sin(angle_rad),
            py - length * math.sin(angle_rad) + width * math.cos(angle_rad)
        )
        draw.polygon([p_tip, p_left, p_right], fill=color)

    def draw_dim_h(wx1, wy1, wx2, wy2, w_dim_y, label, color=(241, 250, 140)):
        p1 = to_px(wx1, wy1)
        p2 = to_px(wx2, wy2)
        p_dim1 = to_px(wx1, w_dim_y)
        p_dim2 = to_px(wx2, w_dim_y)

        # 延伸线
        draw.line([p1, (p_dim1[0], p_dim1[1] - 8 if w_dim_y > wy1 else p_dim1[1] + 8)], fill=color, width=1)
        draw.line([p2, (p_dim2[0], p_dim2[1] - 8 if w_dim_y > wy2 else p_dim2[1] + 8)], fill=color, width=1)
        # 尺寸线
        draw.line([p_dim1, p_dim2], fill=color, width=2)
        # 箭头
        draw_arrow_head(p_dim1[0], p_dim1[1], 0.0, 14.0, 5.0, color)
        draw_arrow_head(p_dim2[0], p_dim2[1], math.pi, 14.0, 5.0, color)
        # 文本
        mid_x = (p_dim1[0] + p_dim2[0]) / 2.0
        mid_y = p_dim1[1] - 18
        bbox = f_dim.getbbox(label)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((mid_x - tw / 2.0, mid_y - th / 2.0), label, fill=color, font=f_dim)

    def draw_dim_v(wx1, wy1, wx2, wy2, w_dim_x, label, color=(241, 250, 140)):
        p1 = to_px(wx1, wy1)
        p2 = to_px(wx2, wy2)
        p_dim1 = to_px(w_dim_x, wy1)
        p_dim2 = to_px(w_dim_x, wy2)

        draw.line([p1, (p_dim1[0] - 8 if w_dim_x < wx1 else p_dim1[0] + 8, p_dim1[1])], fill=color, width=1)
        draw.line([p2, (p_dim2[0] - 8 if w_dim_x < wx2 else p_dim2[0] + 8, p_dim2[1])], fill=color, width=1)
        draw.line([p_dim1, p_dim2], fill=color, width=2)
        draw_arrow_head(p_dim1[0], p_dim1[1], math.pi / 2.0, 14.0, 5.0, color)
        draw_arrow_head(p_dim2[0], p_dim2[1], -math.pi / 2.0, 14.0, 5.0, color)

        mid_x = p_dim1[0] - 25
        mid_y = (p_dim1[1] + p_dim2[1]) / 2.0
        bbox = f_dim.getbbox(label)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((mid_x - tw, mid_y - th / 2.0), label, fill=color, font=f_dim)

    def draw_motion_arrow(wx1, wy1, wx2, wy2, label, color=(255, 121, 198)):
        p1 = to_px(wx1, wy1)
        p2 = to_px(wx2, wy2)
        draw.line([p1, p2], fill=color, width=3)
        angle = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
        draw_arrow_head(p2[0], p2[1], angle + math.pi, 24.0, 10.0, color)
        mid_x = (p1[0] + p2[0]) / 2.0
        mid_y = (p1[1] + p2[1]) / 2.0 - 24
        bbox = f_note.getbbox(label)
        tw = bbox[2] - bbox[0]
        draw.text((mid_x - tw / 2.0, mid_y), label, fill=color, font=f_note)

    def draw_leader(wx1, wy1, wx2, wy2, wx3, wy3, text, color=(241, 250, 140)):
        p1 = to_px(wx1, wy1)
        p2 = to_px(wx2, wy2)
        p3 = to_px(wx3, wy3)
        draw.line([p1, p2], fill=color, width=2)
        draw.line([p2, p3], fill=color, width=2)
        draw_circle(wx1, wy1, 4.0, color, width=2)
        bbox = f_note.getbbox(text)
        tw = bbox[2] - bbox[0]
        tx = p3[0] + 10 if p3[0] >= p2[0] else p3[0] - tw - 10
        ty = p3[1] - 12
        draw.text((tx, ty), text, fill=color, font=f_note)

    # =========================================================================
    # 基础几何常数
    # =========================================================================
    TOTAL_W = 4000.0
    BOARD_H = 1200.0
    TOP_RAIL_H = 60.0
    BOT_RAIL_H = 50.0
    TOTAL_H = 1310.0

    C_FRAME = (220, 225, 230)      # 铝合金外框银灰
    C_BOARD = (80, 250, 123)       # 书写黑板面纯正浅绿
    C_SCREEN = (0, 229, 255)       # 液晶一体机青蓝
    C_HIDDEN = (255, 184, 108)     # 后层遮蔽虚线亮橙
    C_HARDWARE = (255, 121, 198)   # 五金与锁具品红
    C_CENTER = (255, 85, 85)       # 对称中心线红色
    C_DIM = (241, 250, 140)        # 尺寸标注黄色
    C_BORDER = (0, 210, 255)       # 图框青色

    # =========================================================================
    # 1. 工况一：开启状态（多媒体教学模式） Y1 = 2400
    # =========================================================================
    Y1 = 2400.0
    S1_BY = Y1 + BOT_RAIL_H

    # 外框与导轨
    draw_rect(-20.0, Y1 + BOT_RAIL_H + BOARD_H, TOTAL_W + 20.0, Y1 + TOTAL_H, C_FRAME, width=3)
    draw_line(-20.0, Y1 + BOT_RAIL_H + BOARD_H + 30.0, TOTAL_W + 20.0, Y1 + BOT_RAIL_H + BOARD_H + 30.0, C_FRAME, width=2)
    draw_rect(-20.0, Y1, TOTAL_W + 20.0, Y1 + BOT_RAIL_H, C_FRAME, width=3)
    draw_line(-20.0, Y1 + BOT_RAIL_H - 15.0, TOTAL_W + 20.0, Y1 + BOT_RAIL_H - 15.0, C_FRAME, width=2)
    for hx in range(300, 3800, 400):
        draw_circle(hx, Y1 + BOT_RAIL_H / 2.0, 6.0, C_FRAME, width=2)
    draw_rect(-20.0, Y1, 0.0, Y1 + TOTAL_H, C_FRAME, width=3)
    draw_rect(TOTAL_W, Y1, TOTAL_W + 20.0, Y1 + TOTAL_H, C_FRAME, width=3)

    # 86寸一体机 (外露)
    draw_rect(1000.0, S1_BY, 3000.0, S1_BY + BOARD_H, C_SCREEN, width=3)
    DISP_X1, DISP_X2 = 1050.0, 2950.0
    DISP_Y1, DISP_Y2 = S1_BY + 90.0, S1_BY + 90.0 + 1070.0
    draw_rect(DISP_X1, DISP_Y1, DISP_X2, DISP_Y2, C_SCREEN, width=2)
    draw_rect(DISP_X1, S1_BY + 20.0, DISP_X2, S1_BY + 70.0, C_SCREEN, width=2)
    draw_rect(1920.0, S1_BY + 30.0, 2080.0, S1_BY + 60.0, C_SCREEN, width=2)
    draw_circle(1950.0, S1_BY + 45.0, 6.0, C_SCREEN, width=2)

    # 屏幕中心说明文字
    pt_screen = to_px(1380.0, (DISP_Y1 + DISP_Y2) / 2.0)
    draw.text(pt_screen, "86\" 4K UHD 触控一体机面板 (有效显示区: 1900x1070mm)", fill=C_SCREEN, font=f_subhead)

    # 左活动板 (推开停靠)
    draw_rect(0.0, S1_BY, 1000.0, S1_BY + BOARD_H, C_BOARD, width=3)
    draw_rect(20.0, S1_BY + 20.0, 980.0, S1_BY + BOARD_H - 20.0, C_BOARD, width=2)
    draw_circle(920.0, S1_BY + 600.0, 14.0, C_HARDWARE, width=3)
    draw_circle(920.0, S1_BY + 600.0, 8.0, C_HARDWARE, width=2)
    pt_lb = to_px(220.0, S1_BY + 600.0)
    draw.text(pt_lb, "左活动板 (推开停靠)", fill=C_BOARD, font=f_subhead)

    # 右活动板 (推开停靠)
    draw_rect(3000.0, S1_BY, 4000.0, S1_BY + BOARD_H, C_BOARD, width=3)
    draw_rect(3020.0, S1_BY + 20.0, 3980.0, S1_BY + BOARD_H - 20.0, C_BOARD, width=2)
    draw_circle(3080.0, S1_BY + 600.0, 14.0, C_HARDWARE, width=3)
    draw_circle(3080.0, S1_BY + 600.0, 8.0, C_HARDWARE, width=2)
    pt_rb = to_px(3220.0, S1_BY + 600.0)
    draw.text(pt_rb, "右活动板 (推开停靠)", fill=C_BOARD, font=f_subhead)

    # 滑移开启指示箭头
    draw_motion_arrow(750.0, S1_BY + BOARD_H - 120.0, 250.0, S1_BY + BOARD_H - 120.0, "向左滑移开启", C_HARDWARE)
    draw_motion_arrow(3250.0, S1_BY + BOARD_H - 120.0, 3750.0, S1_BY + BOARD_H - 120.0, "向右滑移开启", C_HARDWARE)

    # 工况一尺寸标注
    draw_dim_h(0.0, Y1 + TOTAL_H, 1000.0, Y1 + TOTAL_H, Y1 + TOTAL_H + 80.0, "1000 (左活动板停靠区)")
    draw_dim_h(1000.0, Y1 + TOTAL_H, 3000.0, Y1 + TOTAL_H, Y1 + TOTAL_H + 80.0, "2000 (86寸多媒体大屏外露区)")
    draw_dim_h(3000.0, Y1 + TOTAL_H, 4000.0, Y1 + TOTAL_H, Y1 + TOTAL_H + 80.0, "1000 (右活动板停靠区)")

    draw_dim_h(DISP_X1, DISP_Y2, DISP_X2, DISP_Y2, Y1 + TOTAL_H + 180.0, "1900 (有效显示宽度)")
    draw_dim_h(0.0, Y1 + TOTAL_H, 4000.0, Y1 + TOTAL_H, Y1 + TOTAL_H + 280.0, "4000 (整机主体总长)")
    draw_dim_h(-20.0, Y1 + TOTAL_H, TOTAL_W + 20.0, Y1 + TOTAL_H, Y1 + TOTAL_H + 380.0, "4040 (含外框端盖总长)")

    draw_dim_v(0.0, Y1, 0.0, Y1 + BOT_RAIL_H, -100.0, "50")
    draw_dim_v(0.0, S1_BY, 0.0, S1_BY + BOARD_H, -130.0, "1200")
    draw_dim_v(0.0, S1_BY + BOARD_H, 0.0, Y1 + TOTAL_H, -100.0, "60")
    draw_dim_v(-20.0, Y1, -20.0, Y1 + TOTAL_H, -340.0, "1310 (整机总高)")

    draw_dim_v(DISP_X2, DISP_Y1, DISP_X2, DISP_Y2, TOTAL_W + 100.0, "1070 (屏幕显示净高)")
    draw_dim_v(TOTAL_W, S1_BY, TOTAL_W, DISP_Y1, TOTAL_W + 100.0, "90")

    draw_leader(920.0, S1_BY + 614.0, 840.0, S1_BY + 750.0, 680.0, S1_BY + 750.0, "内嵌拉手孔径 2x直径28mm (Φ28) (孔距边框80mm)")
    draw_leader(2000.0, S1_BY + 45.0, 2000.0, S1_BY - 80.0, 2180.0, S1_BY - 80.0, "下置控制开关/USB扩展接口槽")

    # 工况一主标题
    pt_t1 = to_px(950.0, Y1 + TOTAL_H + 480.0)
    draw.text(pt_t1, "【工况一：开启状态（多媒体交互教学模式 - 86寸交互一体机完全外露）】", fill=(80, 250, 123), font=f_title)

    # =========================================================================
    # 2. 工况二：完全覆盖状态（全黑板书写模式 - 核心新增！） Y2 = 200
    # =========================================================================
    Y2 = 200.0
    S2_BY = Y2 + BOT_RAIL_H

    # 外框与导轨
    draw_rect(-20.0, Y2 + BOT_RAIL_H + BOARD_H, TOTAL_W + 20.0, Y2 + TOTAL_H, C_FRAME, width=3)
    draw_line(-20.0, Y2 + BOT_RAIL_H + BOARD_H + 30.0, TOTAL_W + 20.0, Y2 + BOT_RAIL_H + BOARD_H + 30.0, C_FRAME, width=2)
    draw_rect(-20.0, Y2, TOTAL_W + 20.0, Y2 + BOT_RAIL_H, C_FRAME, width=3)
    draw_line(-20.0, Y2 + BOT_RAIL_H - 15.0, TOTAL_W + 20.0, Y2 + BOT_RAIL_H - 15.0, C_FRAME, width=2)
    for hx in range(300, 3800, 400):
        draw_circle(hx, Y2 + BOT_RAIL_H / 2.0, 6.0, C_FRAME, width=2)
    draw_rect(-20.0, Y2, 0.0, Y2 + TOTAL_H, C_FRAME, width=3)
    draw_rect(TOTAL_W, Y2, TOTAL_W + 20.0, Y2 + TOTAL_H, C_FRAME, width=3)

    # 后层被完全遮蔽的 86寸一体机 (工程隐蔽虚线透视)
    draw_rect(1000.0, S2_BY, 3000.0, S2_BY + BOARD_H, C_HIDDEN, width=2, dashed=True)
    draw_rect(1050.0, S2_BY + 90.0, 2950.0, S2_BY + 90.0 + 1070.0, C_HIDDEN, width=2, dashed=True)

    # 左侧外露固定黑板面 (X: 0 ~ 1000)
    draw_rect(0.0, S2_BY, 1000.0, S2_BY + BOARD_H, C_BOARD, width=3)
    draw_rect(20.0, S2_BY + 20.0, 980.0, S2_BY + BOARD_H - 20.0, C_BOARD, width=2)
    pt_fix_l = to_px(220.0, S2_BY + 600.0)
    draw.text(pt_fix_l, "左固定黑板 (外露书写区)", fill=C_BOARD, font=f_subhead)

    # 右侧外露固定黑板面 (X: 3000 ~ 4000)
    draw_rect(3000.0, S2_BY, 4000.0, S2_BY + BOARD_H, C_BOARD, width=3)
    draw_rect(3020.0, S2_BY + 20.0, 3980.0, S2_BY + BOARD_H - 20.0, C_BOARD, width=2)
    pt_fix_r = to_px(3220.0, S2_BY + 600.0)
    draw.text(pt_fix_r, "右固定黑板 (外露书写区)", fill=C_BOARD, font=f_subhead)

    # 中央两扇活动推拉黑板紧密并拢 (X: 1000 ~ 3000，100% 覆盖大屏)
    # 左活动板闭合位
    draw_rect(1000.0, S2_BY, 2000.0, S2_BY + BOARD_H, C_BOARD, width=3)
    draw_rect(1020.0, S2_BY + 20.0, 1980.0, S2_BY + BOARD_H - 20.0, C_BOARD, width=2)
    # 右活动板闭合位
    draw_rect(2000.0, S2_BY, 3000.0, S2_BY + BOARD_H, C_BOARD, width=3)
    draw_rect(2020.0, S2_BY + 20.0, 2980.0, S2_BY + BOARD_H - 20.0, C_BOARD, width=2)

    # 中央拼合中缝与密封双线 (X = 2000 处，双缝间距 4mm)
    draw_line(1998.0, S2_BY, 1998.0, S2_BY + BOARD_H, C_HARDWARE, width=2)
    draw_line(2002.0, S2_BY, 2002.0, S2_BY + BOARD_H, C_HARDWARE, width=2)

    # 中央机械自锁锁扣与锁孔机构
    LOCK_Y = S2_BY + 600.0
    draw_rect(1985.0, LOCK_Y - 35.0, 2015.0, LOCK_Y + 35.0, C_HARDWARE, width=2)
    draw_circle(2000.0, LOCK_Y, 7.0, C_HARDWARE, width=2)
    draw_line(2000.0, LOCK_Y - 7.0, 2000.0, LOCK_Y - 18.0, C_HARDWARE, width=2)

    # 内移后的两扇拉手位置 (中缝左右各 80mm 处)
    LH2_X = 2000.0 - 80.0
    RH2_X = 2000.0 + 80.0
    draw_circle(LH2_X, LOCK_Y, 14.0, C_HARDWARE, width=3)
    draw_circle(LH2_X, LOCK_Y, 8.0, C_HARDWARE, width=2)
    draw_circle(RH2_X, LOCK_Y, 14.0, C_HARDWARE, width=3)
    draw_circle(RH2_X, LOCK_Y, 8.0, C_HARDWARE, width=2)

    pt_cov_l = to_px(1180.0, S2_BY + 600.0)
    draw.text(pt_cov_l, "左活动板 (已闭合覆盖)", fill=C_BOARD, font=f_subhead)
    pt_cov_r = to_px(2240.0, S2_BY + 600.0)
    draw.text(pt_cov_r, "右活动板 (已闭合覆盖)", fill=C_BOARD, font=f_subhead)

    # 向内滑移闭合指示箭头
    draw_motion_arrow(350.0, S2_BY + BOARD_H - 220.0, 850.0, S2_BY + BOARD_H - 220.0, "向中心滑移闭合", C_HARDWARE)
    draw_motion_arrow(3650.0, S2_BY + BOARD_H - 220.0, 3150.0, S2_BY + BOARD_H - 220.0, "向中心滑移闭合", C_HARDWARE)

    # 工况二尺寸标注
    draw_dim_h(0.0, Y2 + TOTAL_H, 1000.0, Y2 + TOTAL_H, Y2 + TOTAL_H + 110.0, "1000 (左固定板书写区)")
    draw_dim_h(1000.0, Y2 + TOTAL_H, 3000.0, Y2 + TOTAL_H, Y2 + TOTAL_H + 110.0, "2000 (双扇闭合完全覆盖区·单扇1000x2)")
    draw_dim_h(3000.0, Y2 + TOTAL_H, 4000.0, Y2 + TOTAL_H, Y2 + TOTAL_H + 110.0, "1000 (右固定板书写区)")

    draw_dim_h(LH2_X, LOCK_Y, RH2_X, LOCK_Y, LOCK_Y + 120.0, "160 (闭合拉手中心距, 2x80)")
    draw_dim_h(0.0, Y2 + TOTAL_H, 4000.0, Y2 + TOTAL_H, Y2 + TOTAL_H + 210.0, "4000 (全黑板连续超长书写面·总面积4.8㎡)")

    draw_dim_v(0.0, S2_BY, 0.0, S2_BY + BOARD_H, -130.0, "1200")
    draw_dim_v(-20.0, Y2, -20.0, Y2 + TOTAL_H, -340.0, "1310 (整机总高)")

    draw_leader(2000.0, LOCK_Y, 2000.0, LOCK_Y - 140.0, 2200.0, LOCK_Y - 140.0, "中央碰珠自锁机构与防夹手密封胶条")
    draw_leader(1500.0, S2_BY + 90.0 + 1070.0, 1500.0, S2_BY + BOARD_H - 60.0, 1260.0, S2_BY + BOARD_H - 60.0, "后层 86\" 液晶一体机 (已被双扇活动板 100% 完全遮蔽覆盖保护)")

    # 工况二主标题
    pt_t2 = to_px(750.0, Y2 + TOTAL_H + 310.0)
    draw.text(pt_t2, "【工况二：完全覆盖状态（全黑板书写模式 - 双扇推拉板中央锁合·86寸大屏完全遮蔽受保护）】", fill=(80, 250, 123), font=f_title)

    # =========================================================================
    # 3. 双导轨机构横向截面剖切示意图 Y_SEC = -420
    # =========================================================================
    Y_SEC = -200.0
    pt_sec_t = to_px(1050.0, Y_SEC + 170.0)
    draw.text(pt_sec_t, "【双导轨机械滑动与前后层级配合截面原理图 (俯视图剖切)】", fill=C_SCREEN, font=f_subhead)

    draw_rect(0.0, Y_SEC, 4000.0, Y_SEC + 120.0, C_FRAME, width=2)
    draw_line(0.0, Y_SEC + 35.0, 4000.0, Y_SEC + 35.0, C_FRAME, width=1)
    draw_line(0.0, Y_SEC + 85.0, 4000.0, Y_SEC + 85.0, C_FRAME, width=1)

    # 后层固定面剖切
    draw_rect(0.0, Y_SEC + 25.0, 1000.0, Y_SEC + 45.0, C_BOARD, width=2)
    draw.text(to_px(360.0, Y_SEC - 40.0), "后层左固定黑板", fill=C_BOARD, font=f_note)

    draw_rect(1000.0, Y_SEC + 15.0, 3000.0, Y_SEC + 55.0, C_SCREEN, width=2)
    draw.text(to_px(1500.0, Y_SEC - 40.0), "后层中置 86\" 液晶多媒体触控一体机", fill=C_SCREEN, font=f_note)

    draw_rect(3000.0, Y_SEC + 25.0, 4000.0, Y_SEC + 45.0, C_BOARD, width=2)
    draw.text(to_px(3360.0, Y_SEC - 40.0), "后层右固定黑板", fill=C_BOARD, font=f_note)

    # 前层滑动面剖切 (实线闭合，虚线开启)
    draw_rect(1000.0, Y_SEC + 75.0, 2000.0, Y_SEC + 95.0, C_BOARD, width=2)
    draw_rect(2000.0, Y_SEC + 75.0, 3000.0, Y_SEC + 95.0, C_BOARD, width=2)
    draw_rect(0.0, Y_SEC + 75.0, 1000.0, Y_SEC + 95.0, C_HIDDEN, width=2, dashed=True)
    draw_rect(3000.0, Y_SEC + 75.0, 4000.0, Y_SEC + 95.0, C_HIDDEN, width=2, dashed=True)

    draw_motion_arrow(500.0, Y_SEC + 85.0, 1500.0, Y_SEC + 85.0, "推拉滑移行程: 1000mm", C_HARDWARE)
    draw_motion_arrow(3500.0, Y_SEC + 85.0, 2500.0, Y_SEC + 85.0, "推拉滑移行程: 1000mm", C_HARDWARE)
    draw_leader(2000.0, Y_SEC + 65.0, 2000.0, Y_SEC - 90.0, 2180.0, Y_SEC - 90.0, "板屏防擦碰安全间距: 15mm (配防撞缓冲滑轮)")

    # =========================================================================
    # 4. 标准工程图框与标题栏
    # =========================================================================
    BX1, BY1 = -460.0, -720.0
    BX2, BY2 = 4450.0, 4420.0
    draw_rect(BX1, BY1, BX2, BY2, C_BORDER, width=4)
    draw_rect(BX1 + 25.0, BY1 + 25.0, BX2 - 25.0, BY2 - 25.0, C_BORDER, width=2)

    # 标题栏
    TB_X1, TB_Y1 = 3000.0, -680.0
    TB_X2, TB_Y2 = 4400.0, -440.0
    draw_rect(TB_X1, TB_Y1, TB_X2, TB_Y2, C_BORDER, width=3)
    draw_line(TB_X1, TB_Y1 + 160.0, TB_X2, TB_Y1 + 160.0, C_BORDER, width=2)
    draw_line(TB_X1, TB_Y1 + 80.0, TB_X2, TB_Y1 + 80.0, C_BORDER, width=2)
    draw_line(TB_X1 + 420.0, TB_Y1, TB_X1 + 420.0, TB_Y1 + 160.0, C_BORDER, width=2)
    draw_line(TB_X1 + 880.0, TB_Y1, TB_X1 + 880.0, TB_Y1 + 160.0, C_BORDER, width=2)

    draw.text(to_px(TB_X1 + 40.0, TB_Y1 + 190.0), "市面标准多媒体推拉黑板工程尺寸图 (双工况全覆盖)", fill=(80, 250, 123), font=f_subhead)
    draw.text(to_px(TB_X1 + 20.0, TB_Y1 + 115.0), "图纸编号: PJHB-2026-CAD-v2.1", fill=C_FRAME, font=f_note)
    draw.text(to_px(TB_X1 + 450.0, TB_Y1 + 115.0), "工程版本: v2.1 规范修订版", fill=C_FRAME, font=f_note)
    draw.text(to_px(TB_X1 + 910.0, TB_Y1 + 115.0), "比例: 1:20 (单位: mm)", fill=C_FRAME, font=f_note)
    draw.text(to_px(TB_X1 + 20.0, TB_Y1 + 35.0), "设计单位: 智能教学装备工程组", fill=C_FRAME, font=f_note)
    draw.text(to_px(TB_X1 + 450.0, TB_Y1 + 35.0), "审核: 第 4 轮严格技术审核(通过)", fill=(80, 250, 123), font=f_note)
    draw.text(to_px(TB_X1 + 910.0, TB_Y1 + 35.0), "日期: 2026-09-12", fill=C_FRAME, font=f_note)

    # 技术要求栏
    TX_X1, TX_Y1 = -420.0, -680.0
    TX_X2, TX_Y2 = 1400.0, -440.0
    draw_rect(TX_X1, TX_Y1, TX_X2, TX_Y2, C_BORDER, width=3)
    draw.text(to_px(TX_X1 + 30.0, TX_Y2 - 35.0), "【技术要求与设计规范说明】", fill=C_DIM, font=f_subhead)
    draw.text(to_px(TX_X1 + 30.0, TX_Y2 - 70.0), "1. 本图符合国家教育部行业标准 JY/T 0148-2011 及机械制图尺寸注法 GB/T 4458.4。", fill=C_FRAME, font=f_small)
    draw.text(to_px(TX_X1 + 30.0, TX_Y2 - 100.0), "2. 100% 采用纯机械工程线框绘制，无 Hatch 色块干扰；文字采用 SimHei 黑体消除问号乱码。", fill=C_FRAME, font=f_small)
    draw.text(to_px(TX_X1 + 30.0, TX_Y2 - 130.0), "3. 工况一呈现 86 寸液晶一体机完全裸露的多媒体交互教学模式 (双扇活动板推开停靠两侧)。", fill=C_FRAME, font=f_small)
    draw.text(to_px(TX_X1 + 30.0, TX_Y2 - 160.0), "4. 工况二呈现双扇活动黑板向内滑移完全闭合覆盖 86 寸大屏状态，提供 4000mm 连贯书写大黑板。", fill=C_FRAME, font=f_small)
    draw.text(to_px(TX_X1 + 30.0, TX_Y2 - 190.0), "5. 中央中缝配磁吸密封毛条与防夹手自锁锁扣，后层大屏与前层黑板保留 15mm 安全防擦碰间隙。", fill=C_FRAME, font=f_small)

    out_png_path = "/mnt/d/Desktop/pjhb/01-CAD工程图纸/传统市面标准推拉黑板_双状态全覆盖与尺寸标注工程图_4K.png"
    img.save(out_png_path, "PNG", quality=100)
    print("4K High-Res Preview rendered and saved successfully to:", out_png_path)

if __name__ == "__main__":
    main()
