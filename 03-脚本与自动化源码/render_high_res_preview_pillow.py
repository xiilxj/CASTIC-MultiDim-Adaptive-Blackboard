# -*- coding: utf-8 -*-
"""
模块化折叠翻转多媒体智能黑板系统 - 4K 工业级高精工程总装渲染脚本 (基于 Pillow)
"""

from PIL import Image, ImageDraw, ImageFont
import os

def render_blackboard_4k():
    width = 4000
    height = 2500
    # AutoCAD 经典工程深色底
    bg_color = (24, 24, 28)
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # 坐标系映射：世界坐标 (X: -3600~3600, Y: -1250~2850) -> 图像坐标 (0~4000, 0~2500)
    world_min_x, world_max_x = -3600.0, 3600.0
    world_min_y, world_max_y = -1250.0, 2850.0
    world_w = world_max_x - world_min_x
    world_h = world_max_y - world_min_y

    def to_img_coord(wx, wy):
        ix = int((wx - world_min_x) / world_w * width)
        iy = int((world_max_y - wy) / world_h * height)
        return ix, iy

    def draw_rect(x1, y1, x2, y2, fill=None, outline=None, width=1):
        ix1, iy2 = to_img_coord(x1, y1)
        ix2, iy1 = to_img_coord(x2, y2)
        draw.rectangle([min(ix1, ix2), min(iy1, iy2), max(ix1, ix2), max(iy1, iy2)],
                       fill=fill, outline=outline, width=width)

    def draw_circle(cx, cy, r, fill=None, outline=None, width=1):
        icx, icy = to_img_coord(cx, cy)
        ir = int(r / world_w * width)
        draw.ellipse([icx - ir, icy - ir, icx + ir, icy + ir], fill=fill, outline=outline, width=width)

    def draw_line(x1, y1, x2, y2, fill=(200, 200, 200), width=1):
        ix1, iy1 = to_img_coord(x1, y1)
        ix2, iy2 = to_img_coord(x2, y2)
        draw.line([ix1, iy1, ix2, iy2], fill=fill, width=width)

    # 颜色定义 (严格去反光)
    C_FRAME = (55, 58, 62)
    C_FRAME_LINE = (130, 136, 142)
    C_SCREEN = (30, 75, 130)        # 纯净液晶科技蓝 (100%无倒三角反光)
    C_SCREEN_LINE = (60, 140, 230)
    C_GREEN = (38, 85, 55)          # 墨绿黑板面
    C_GREEN_LINE = (76, 175, 80)
    C_WHITE = (226, 230, 234)       # 象牙白副板
    C_WHITE_LINE = (180, 190, 200)
    C_CANOPY = (45, 55, 65)         # 雨棚冷灰
    C_CANOPY_LINE = (0, 172, 193)
    C_HINGE = (255, 160, 0)         # 铰链黄

    # 绘制工程微网格背景 (Grid)
    grid_color = (32, 32, 38)
    for gx in range(int(world_min_x), int(world_max_x), 200):
        draw_line(gx, world_min_y, gx, world_max_y, fill=grid_color, width=1)
    for gy in range(int(world_min_y), int(world_max_y), 200):
        draw_line(world_min_x, gy, world_max_x, gy, fill=grid_color, width=1)

    # 尺寸参数
    W_SCREEN, H_SCREEN = 2000.0, 1200.0
    W_INNER_LCD, H_INNER_LCD = 1900.0, 1070.0
    W_BOARD, H_BOARD = 1000.0, 1200.0
    W_FOLD, H_FOLD = 1000.0, 1200.0
    W_CANOPY, H_CANOPY = 2120.0, 90.0

    states = [
        {"name": "DEPLOYED", "cy": 1600.0, "is_dep": True},
        {"name": "COMPACT", "cy": -350.0, "is_dep": False}
    ]

    for st in states:
        cy = st["cy"]
        is_dep = st["is_dep"]

        # 1. 顶部 Canopy 遮光雨棚自洁防尘系统
        cx1, cx2 = -W_CANOPY / 2.0, W_CANOPY / 2.0
        cy1 = cy + H_SCREEN / 2.0 + 10.0
        cy2 = cy1 + H_CANOPY
        draw_rect(cx1, cy1, cx2, cy2, fill=C_CANOPY, outline=C_CANOPY_LINE, width=3)
        draw_line(cx1, cy1 + 28.0, cx2, cy1 + 28.0, fill=C_CANOPY_LINE, width=2)
        draw_line(cx1, cy1 + 58.0, cx2, cy1 + 58.0, fill=C_CANOPY_LINE, width=2)
        for gx in range(int(cx1) + 100, int(cx2) - 100, 150):
            draw_line(float(gx), cy1 + 68.0, float(gx) + 50.0, cy1 + 68.0, fill=(77, 208, 225), width=2)

        # 2. 底部自洁排砂导轨
        bx1, bx2 = cx1, cx2
        by2 = cy - H_SCREEN / 2.0 - 10.0
        by1 = by2 - 50.0
        draw_rect(bx1, by1, bx2, by2, fill=C_FRAME, outline=C_FRAME_LINE, width=2)
        for hx in range(int(bx1) + 150, int(bx2) - 150, 300):
            draw_circle(float(hx), (by1 + by2) / 2.0, 7.0, fill=(38, 50, 56), outline=(176, 190, 197), width=2)

        # 3. 中央多媒体显示屏模块
        sx1, sx2 = -W_SCREEN / 2.0, W_SCREEN / 2.0
        sy1, sy2 = cy - H_SCREEN / 2.0, cy + H_SCREEN / 2.0
        draw_rect(sx1, sy1, sx2, sy2, fill=C_FRAME, outline=C_FRAME_LINE, width=3)

        # 液晶屏幕 (纯净蓝，去反光)
        lx1, lx2 = -W_INNER_LCD / 2.0, W_INNER_LCD / 2.0
        ly1 = sy1 + 50.0
        ly2 = ly1 + H_INNER_LCD
        draw_rect(lx1, ly1, lx2, ly2, fill=C_SCREEN, outline=C_SCREEN_LINE, width=3)
        draw_rect(lx1 + 8.0, ly1 + 8.0, lx2 - 8.0, ly2 - 8.0, fill=None, outline=(100, 181, 246), width=1)

        # 底部控制区与 VLM 视线跟踪探针
        draw_rect(-90.0, sy1 + 15.0, 90.0, sy1 + 35.0, fill=(33, 33, 33), outline=(158, 158, 158), width=1)
        draw_circle(0.0, sy1 + 25.0, 5.0, fill=C_HINGE, outline=(255, 213, 79), width=2)

        # 4. 两翼主黑板面 (墨绿色)
        # 左主黑板
        l_bx2 = -W_SCREEN / 2.0 - 15.0
        l_bx1 = l_bx2 - W_BOARD
        l_by1, l_by2 = cy - H_BOARD / 2.0, cy + H_BOARD / 2.0
        draw_rect(l_bx1, l_by1, l_bx2, l_by2, fill=C_FRAME, outline=C_FRAME_LINE, width=3)
        draw_rect(l_bx1 + 20.0, l_by1 + 20.0, l_bx2 - 20.0, l_by2 - 20.0, fill=C_GREEN, outline=C_GREEN_LINE, width=2)

        # 右主黑板
        r_bx1 = W_SCREEN / 2.0 + 15.0
        r_bx2 = r_bx1 + W_BOARD
        r_by1, r_by2 = l_by1, l_by2
        draw_rect(r_bx1, r_by1, r_bx2, r_by2, fill=C_FRAME, outline=C_FRAME_LINE, width=3)
        draw_rect(r_bx1 + 20.0, r_by1 + 20.0, r_bx2 - 20.0, r_by2 - 20.0, fill=C_GREEN, outline=C_GREEN_LINE, width=2)

        # 把手圆孔
        draw_circle(r_bx1 + 80.0, cy, 14.0, fill=(38, 50, 56), outline=C_HINGE, width=2)
        draw_circle(r_bx1 + 80.0, cy, 7.0, fill=C_HINGE, outline=C_HINGE, width=1)
        draw_circle(l_bx2 - 80.0, cy, 14.0, fill=(38, 50, 56), outline=C_HINGE, width=2)
        draw_circle(l_bx2 - 80.0, cy, 7.0, fill=C_HINGE, outline=C_HINGE, width=1)

        # 5. 折叠副板 (仅展开态)
        if is_dep:
            # 左副板 (象牙白)
            l_fx2 = l_bx1 - 12.0
            l_fx1 = l_fx2 - W_FOLD
            draw_rect(l_fx1, l_by1, l_fx2, l_by2, fill=C_FRAME, outline=C_FRAME_LINE, width=3)
            draw_rect(l_fx1 + 20.0, l_by1 + 20.0, l_fx2 - 20.0, l_by2 - 20.0, fill=C_WHITE, outline=C_WHITE_LINE, width=2)
            # 左铰链
            for hy in [cy + 350.0, cy - 350.0]:
                draw_rect(l_fx2, hy - 35.0, l_bx1, hy + 35.0, fill=C_HINGE, outline=(255, 224, 130), width=2)
                draw_circle((l_fx2 + l_bx1) / 2.0, hy, 4.0, fill=(38, 50, 56), outline=(255, 255, 255), width=1)

            # 右副板 (象牙白)
            r_fx1 = r_bx2 + 12.0
            r_fx2 = r_fx1 + W_FOLD
            draw_rect(r_fx1, r_by1, r_fx2, r_by2, fill=C_FRAME, outline=C_FRAME_LINE, width=3)
            draw_rect(r_fx1 + 20.0, r_by1 + 20.0, r_fx2 - 20.0, r_by2 - 20.0, fill=C_WHITE, outline=C_WHITE_LINE, width=2)
            # 右铰链
            for hy in [cy + 350.0, cy - 350.0]:
                draw_rect(r_bx2, hy - 35.0, r_fx1, hy + 35.0, fill=C_HINGE, outline=(255, 224, 130), width=2)
                draw_circle((r_bx2 + r_fx1) / 2.0, hy, 4.0, fill=(38, 50, 56), outline=(255, 255, 255), width=1)

    out_path = '/mnt/d/Desktop/pjhb/01-CAD工程图纸/模块化折叠翻转多媒体智能黑板_工程设计渲染总装图_4K.png'
    img.save(out_path, quality=95)
    print("SUCCESS_SAVED_4K_PNG:", out_path)

if __name__ == "__main__":
    render_blackboard_4k()
