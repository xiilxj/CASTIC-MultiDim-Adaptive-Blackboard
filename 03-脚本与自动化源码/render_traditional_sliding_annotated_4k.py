# -*- coding: utf-8 -*-
"""
市面传统多媒体推拉黑板 - 4K 纯线框工程尺寸标注总装图渲染脚本 (无涂色版)
依据 AutoCAD 2026 真实图元坐标生成 4000x2600 像素工业级工程蓝图/白图
"""

from PIL import Image, ImageDraw, ImageFont
import math

def render_traditional_annotated():
    width = 4000
    height = 2600
    # 经典机械 CAD 深黑/藏蓝底色
    bg_color = (22, 24, 28)
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # 视口映射范围：世界坐标 X: -2600 ~ 2600, Y: -500 ~ 2200
    w_min_x, w_max_x = -2600.0, 2600.0
    w_min_y, w_max_y = -500.0, 2200.0
    w_w = w_max_x - w_min_x
    w_h = w_max_y - w_min_y

    def to_img(wx, wy):
        ix = int((wx - w_min_x) / w_w * width)
        iy = int((w_max_y - wy) / w_h * height)
        return ix, iy

    def draw_rect(x1, y1, x2, y2, outline=(220, 225, 230), width=2):
        ix1, iy2 = to_img(x1, y1)
        ix2, iy1 = to_img(x2, y2)
        draw.rectangle([min(ix1, ix2), min(iy1, iy2), max(ix1, ix2), max(iy1, iy2)],
                       fill=None, outline=outline, width=width)

    def draw_line(x1, y1, x2, y2, color=(180, 185, 190), width=2):
        ix1, iy1 = to_img(x1, y1)
        ix2, iy2 = to_img(x2, y2)
        draw.line([ix1, iy1, ix2, iy2], fill=color, width=width)

    def draw_circle(cx, cy, r, outline=(220, 225, 230), width=2):
        icx, icy = to_img(cx, cy)
        ir = int(r / w_w * width)
        draw.ellipse([icx - ir, icy - ir, icx + ir, icy + ir], fill=None, outline=outline, width=width)

    def draw_dim_h(x1, y, x2, dim_y, text_str):
        """绘制水平工程尺寸标注 (带界线、尺寸线与箭头)"""
        C_DIM = (255, 215, 0) # 黄色
        # 尺寸界线
        draw_line(x1, y, x1, dim_y + 15.0, color=C_DIM, width=1)
        draw_line(x2, y, x2, dim_y + 15.0, color=C_DIM, width=1)
        # 尺寸线
        draw_line(x1, dim_y, x2, dim_y, color=C_DIM, width=2)
        # 箭头
        arr_size = 12.0
        # 左箭头
        ix1, iy1 = to_img(x1, dim_y)
        draw.polygon([(ix1, iy1), (ix1 + 12, iy1 - 5), (ix1 + 12, iy1 + 5)], fill=C_DIM)
        # 右箭头
        ix2, iy2 = to_img(x2, dim_y)
        draw.polygon([(ix2, iy2), (ix2 - 12, iy2 - 5), (ix2 - 12, iy2 + 5)], fill=C_DIM)
        # 尺寸数值文本
        mid_x = (x1 + x2) / 2.0
        imx, imy = to_img(mid_x, dim_y + 25.0)
        # 简易文本居中绘制
        draw.text((imx - len(text_str)*6, imy - 12), text_str, fill=C_DIM)

    def draw_dim_v(x, y1, dim_x, y2, text_str):
        """绘制垂直工程尺寸标注"""
        C_DIM = (255, 215, 0)
        draw_line(x, y1, dim_x - 15.0 if dim_x < x else dim_x + 15.0, y1, color=C_DIM, width=1)
        draw_line(x, y2, dim_x - 15.0 if dim_x < x else dim_x + 15.0, y2, color=C_DIM, width=1)
        draw_line(dim_x, y1, dim_x, y2, color=C_DIM, width=2)
        # 箭头
        ix, iy1 = to_img(dim_x, y1)
        draw.polygon([(ix, iy1), (ix - 5, iy1 - 12), (ix + 5, iy1 - 12)], fill=C_DIM)
        ix, iy2 = to_img(dim_x, y2)
        draw.polygon([(ix, iy2), (ix - 5, iy2 + 12), (ix + 5, iy2 + 12)], fill=C_DIM)
        mid_y = (y1 + y2) / 2.0
        imx, imy = to_img(dim_x - 45.0 if dim_x < x else dim_x + 15.0, mid_y)
        draw.text((imx, imy - 8), text_str, fill=C_DIM)

    # 1. 背景细微网格 (Grid)
    for gx in range(int(w_min_x), int(w_max_x), 200):
        draw_line(gx, w_min_y, gx, w_max_y, color=(28, 30, 34), width=1)
    for gy in range(int(w_min_y), int(w_max_y), 200):
        draw_line(w_min_x, gy, w_max_x, gy, color=(28, 30, 34), width=1)

    # 2. 红色对称中心基准线 (Centerline)
    C_RED = (244, 67, 54)
    draw_line(0.0, -180.0, 0.0, 1420.0, color=C_RED, width=2)
    draw_line(-2180.0, 600.0, 2180.0, 600.0, color=C_RED, width=2)

    # 3. 构件尺寸
    W_TOTAL, W_OUTER = 4000.0, 4040.0
    H_BOARD = 1200.0
    W_SCREEN, H_SCREEN = 2000.0, 1200.0
    W_LCD, H_LCD = 1900.0, 1070.0
    W_SIDE = 1000.0
    H_TOP, H_BOT = 60.0, 50.0

    C_WHITE = (235, 240, 245)
    C_CYAN = (0, 188, 212)

    # 顶部上导轨
    rx1, rx2 = -W_OUTER / 2.0, W_OUTER / 2.0
    ry1, ry2 = H_BOARD, H_BOARD + H_TOP
    draw_rect(rx1, ry1, rx2, ry2, outline=C_WHITE, width=3)
    draw_line(rx1, ry1 + 20.0, rx2, ry1 + 20.0, color=C_CYAN, width=1)
    draw_line(rx1, ry1 + 40.0, rx2, ry1 + 40.0, color=C_CYAN, width=1)
    draw_rect(rx1, ry1, rx1 + 30.0, ry2, outline=C_CYAN, width=2)
    draw_rect(rx2 - 30.0, ry1, rx2, ry2, outline=C_CYAN, width=2)

    # 底部下导轨粉笔槽
    by2 = 0.0
    by1 = by2 - H_BOT
    draw_rect(rx1, by1, rx2, by2, outline=C_WHITE, width=3)
    draw_line(rx1, by1 + 22.0, rx2, by1 + 22.0, color=C_CYAN, width=1)
    draw_rect(rx1, by1, rx1 + 30.0, by2, outline=C_CYAN, width=2)
    draw_rect(rx2 - 30.0, by1, rx2, by2, outline=C_CYAN, width=2)

    # 中央 86 寸一体机
    sx1, sx2 = -W_SCREEN / 2.0, W_SCREEN / 2.0
    draw_rect(sx1, 0.0, sx2, H_SCREEN, outline=C_WHITE, width=3)
    # 液晶显示面板 (纯线框，无倒三角反光！)
    lx1, lx2 = -W_LCD / 2.0, W_LCD / 2.0
    ly1 = 90.0
    ly2 = ly1 + H_LCD
    draw_rect(lx1, ly1, lx2, ly2, outline=C_WHITE, width=3)
    draw_rect(lx1 + 6.0, ly1 + 6.0, lx2 - 6.0, ly2 - 6.0, outline=C_CYAN, width=1)
    # 底部控制区
    draw_rect(-100.0, 25.0, 100.0, 65.0, outline=C_CYAN, width=2)
    draw_circle(0.0, 45.0, 5.0, outline=C_CYAN, width=2)
    draw_circle(-45.0, 45.0, 3.0, outline=C_CYAN, width=1)
    draw_circle(45.0, 45.0, 3.0, outline=C_CYAN, width=1)

    # 左右活动推拉黑板 (纯线框)
    l_bx2 = -W_SCREEN / 2.0
    l_bx1 = l_bx2 - W_SIDE
    draw_rect(l_bx1, 0.0, l_bx2, H_BOARD, outline=C_WHITE, width=3)
    draw_rect(l_bx1 + 20.0, 20.0, l_bx2 - 20.0, H_BOARD - 20.0, outline=C_CYAN, width=2)
    draw_rect(l_bx1 + 25.0, 25.0, l_bx2 - 25.0, H_BOARD - 25.0, outline=C_CYAN, width=1)

    r_bx1 = W_SCREEN / 2.0
    r_bx2 = r_bx1 + W_SIDE
    draw_rect(r_bx1, 0.0, r_bx2, H_BOARD, outline=C_WHITE, width=3)
    draw_rect(r_bx1 + 20.0, 20.0, r_bx2 - 20.0, H_BOARD - 20.0, outline=C_CYAN, width=2)
    draw_rect(r_bx1 + 25.0, 25.0, r_bx2 - 25.0, H_BOARD - 25.0, outline=C_CYAN, width=1)

    # 拉手孔
    draw_circle(l_bx2 - 80.0, 600.0, 14.0, outline=C_WHITE, width=2)
    draw_circle(l_bx2 - 80.0, 600.0, 8.0, outline=C_CYAN, width=1)
    draw_circle(r_bx1 + 80.0, 600.0, 14.0, outline=C_WHITE, width=2)
    draw_circle(r_bx1 + 80.0, 600.0, 8.0, outline=C_CYAN, width=1)

    # 推拉滑动文本
    draw.text(to_img(-1660.0, 680.0), "<--- 推拉滑动 --->", fill=C_CYAN)
    draw.text(to_img(1340.0, 680.0), "<--- 推拉滑动 --->", fill=C_CYAN)

    # ================= 4. 工程化标注链 =================
    # 顶部水平标注第 1 层 (Y=1340)
    draw_dim_h(l_bx1, H_BOARD, l_bx2, 1340.0, "1000")
    draw_dim_h(sx1, H_BOARD, lx1, 1340.0, "50")
    draw_dim_h(lx1, H_BOARD, lx2, 1340.0, "1900 (显示区净宽)")
    draw_dim_h(lx2, H_BOARD, sx2, 1340.0, "50")
    draw_dim_h(r_bx1, H_BOARD, r_bx2, 1340.0, "1000")

    # 顶部水平标注第 2 层 (Y=1470)
    draw_dim_h(l_bx1, H_BOARD, l_bx2, 1470.0, "1000 (左推拉板)")
    draw_dim_h(sx1, H_BOARD, sx2, 1470.0, "2000 (一体机外框)")
    draw_dim_h(r_bx1, H_BOARD, r_bx2, 1470.0, "1000 (右推拉板)")

    # 顶部水平标注第 3 层 (Y=1600 / 1730)
    draw_dim_h(-2000.0, H_BOARD, 2000.0, 1600.0, "4000 (标准总开间)")
    draw_dim_h(rx1, H_BOARD, rx2, 1730.0, "4040 (导轨总长)")

    # 左侧垂直标注 (X = -2150 / -2300)
    draw_dim_v(l_bx1, by1, -2150.0, by2, "50 (下轨)")
    draw_dim_v(l_bx1, 0.0, -2150.0, H_BOARD, "1200 (板面高度)")
    draw_dim_v(l_bx1, ry1, -2150.0, ry2, "60 (上轨)")
    draw_dim_v(rx1, by1, -2320.0, ry2, "1310 (整机总高)")

    # 右侧垂直细部分段 (X = 2150)
    draw_dim_v(r_bx2, 0.0, 2150.0, ly1, "90")
    draw_dim_v(r_bx2, ly1, 2150.0, ly2, "1070 (显示区净高)")
    draw_dim_v(r_bx2, ly2, 2150.0, H_BOARD, "40")

    # 局部孔位与边框标注
    draw_dim_h(l_bx2 - 80.0, 600.0, l_bx2, 530.0, "80")
    draw_dim_h(r_bx1, 600.0, r_bx1 + 80.0, 530.0, "80")

    # 5. 技术引线说明
    draw_line(-1900.0, 1260.0, -1450.0, 1380.0, color=(76, 175, 80), width=1)
    draw.text(to_img(-1430.0, 1390.0), "[1] 铝合金静音上滑轨 (内置双导轨与吊轮组, 高60mm)", fill=(76, 175, 80))

    draw_line(0.0, 1080.0, 250.0, 1200.0, color=(76, 175, 80), width=1)
    draw.text(to_img(260.0, 1210.0), "[2] 86英寸交互一体机 (有效显示区 1900x1070mm, 纯净抗眩光)", fill=(76, 175, 80))

    draw_line(0.0, 45.0, 350.0, -90.0, color=(76, 175, 80), width=1)
    draw.text(to_img(360.0, -80.0), "[3] 前置按键/接口/摄像头控制面板 (高90mm)", fill=(76, 175, 80))

    draw_line(-1000.0, -25.0, -1250.0, -120.0, color=(76, 175, 80), width=1)
    draw.text(to_img(-1240.0, -110.0), "[4] 铝合金下承重导轨兼粉笔灰槽 (高50mm, 带自洁斜面)", fill=(76, 175, 80))

    draw_line(-1500.0, 400.0, -1950.0, 300.0, color=(76, 175, 80), width=1)
    draw.text(to_img(-1940.0, 310.0), "[5] 磁性墨绿搪瓷活动推拉黑板 (宽1000x高1200mm, 20mm包边)", fill=(76, 175, 80))

    draw_line(2080.0, 600.0, 2220.0, 750.0, color=(76, 175, 80), width=1)
    draw.text(to_img(2230.0, 760.0), "[6] 隐形内嵌式拉手兼自锁防夹孔 (直径28mm, 孔心距边80mm)", fill=(76, 175, 80))

    # 6. 工程图签 (Title Block)
    tx1, ty1, tx2, ty2 = 1260.0, -280.0, 2020.0, -140.0
    draw_rect(tx1, ty1, tx2, ty2, outline=C_WHITE, width=2)
    draw_line(tx1, ty1 + 45.0, tx2, ty1 + 45.0, color=C_WHITE, width=1)
    draw_line(tx1, ty1 + 95.0, tx2, ty1 + 95.0, color=C_WHITE, width=1)
    draw_line(tx1 + 380.0, ty1, tx1 + 380.0, ty2, color=C_WHITE, width=1)

    draw.text(to_img(tx1 + 20.0, ty1 + 105.0), "图名: 市面标准多媒体推拉黑板 (86寸) 正交总装图", fill=C_WHITE)
    draw.text(to_img(tx1 + 20.0, ty1 + 58.0), "制图规范: 纯线框·无涂色·国标全尺寸工程标注", fill=C_WHITE)
    draw.text(to_img(tx1 + 20.0, ty1 + 15.0), "设计/绘图: 林诚俊", fill=C_WHITE)
    draw.text(to_img(tx1 + 400.0, ty1 + 58.0), "单位: 毫米 (mm) | 比例: 1:1", fill=C_WHITE)
    draw.text(to_img(tx1 + 400.0, ty1 + 15.0), "审核: 海鸥工程技术团队 (第3轮审核通过)", fill=C_WHITE)

    # 7. 主标题栏
    draw.text(to_img(-1800.0, 1950.0), "市面传统多媒体教学推拉黑板 - 正交前视工程尺寸标注总装图", fill=C_WHITE)
    draw.text(to_img(-1800.0, 1880.0), "依据标准: 教育部 JY/T 0148-2011《白板和黑板》与 86 英寸交互一体机安装规范", fill=C_CYAN)

    out_png = '/mnt/d/Desktop/pjhb/01-CAD工程图纸/传统市面标准推拉黑板_无涂色工程尺寸标注图_4K.png'
    img.save(out_png, quality=95)
    print("SUCCESS_EXPORT_4K:", out_png)
    return out_png

if __name__ == "__main__":
    render_traditional_annotated()
