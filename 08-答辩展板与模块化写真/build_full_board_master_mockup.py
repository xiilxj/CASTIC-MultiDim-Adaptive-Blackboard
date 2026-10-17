#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
第42届瑞安市青少年科技创新大赛 (CASTIC选拔赛)
答辩展板全尺寸总装 Mockup 生成引擎 (1:1 毫米级装配 · 终极紧凑高信息密度版)
物理规格: 高 1.2m (1200mm) x 宽 0.9m (900mm)
设计重构亮点:
  1. 顶栏极限紧凑 (75mm高)，让渡 105mm 垂直宝贵空间；
  2. 前三代演进紧凑并列 (180mm高)，彻底消除空洞多余白边；
  3. 第三代 AutoCAD 5800x4000 工业大图作为【全场核心主角 C位】极限放大至 530mm高！
  4. 彻底剔除大黄圈光线追踪图，全面引入高精度无损矢量全链路闭环流程图与双轨架构图 (360mm高)；
  5. 严格毫米级装配: 15mm顶距 + 75mm + 7mm缝 + 180mm + 7mm缝 + 530mm + 7mm缝 + 360mm + 19mm底距 = 1200mm。
==============================================================================
"""

import os
import sys
import fitz
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(BASE_DIR, "pdf_output")
PREVIEW_DIR = os.path.join(BASE_DIR, "previews")
os.makedirs(PREVIEW_DIR, exist_ok=True)

# 4大核心模块重构配置清单 (净尺寸 mm)
MODULES = [
    {
        "id": "MOD-01_02",
        "name": "第一区：紧凑型顶栏官方大赛页眉与主标题楣头",
        "pdf": os.path.join(PDF_DIR, "MOD_01_02_顶栏一体化主标题楣头_860x75mm.pdf"),
        "net_w_mm": 860,
        "net_h_mm": 75,
        "bleed_mm": 3,
        "desc": "官方楣头 + 28pt 加粗大标题 + 5大技术胶囊 + 2025.09-2026.10 学籍名牌 (极限紧凑)"
    },
    {
        "id": "MOD-GEN12",
        "name": "第二区：前三代CAD演进与失效机理紧凑对比区",
        "pdf": os.path.join(PDF_DIR, "MOD_GEN12_前三代紧凑演进_860x180mm.pdf"),
        "net_w_mm": 860,
        "net_h_mm": 180,
        "bleed_mm": 3,
        "desc": "市面三大原罪 ❌ vs 一代悬臂挠度 ❌ vs 二代同轴干涉 ❌ (紧凑三列·零冗余白边)"
    },
    {
        "id": "MOD-GEN3",
        "name": "第三区：【全场核心重点】第三代终极总装工业图纸与数字孪生",
        "pdf": os.path.join(PDF_DIR, "MOD_GEN3_核心主角工程图纸_860x530mm.pdf"),
        "net_w_mm": 860,
        "net_h_mm": 530,
        "bleed_mm": 3,
        "desc": "AutoCAD 5800x4000 工业大图独占 540mm 宽 (极度放大) + 铰链特写 + 6000mm 展开 + 矢量时序图"
    },
    {
        "id": "MOD-VLM-FLOW",
        "name": "第四区：端侧智能双矢量流程图架构与官方底栏通栏",
        "pdf": os.path.join(PDF_DIR, "MOD_VLM_双流程图与官方底栏_860x360mm.pdf"),
        "net_w_mm": 860,
        "net_h_mm": 360,
        "bleed_mm": 3,
        "desc": "真机活体交互全链路闭环流程图 + 端侧VLM双轨制造架构流程图 + 真实HUD + 国标实测表"
    }
]

# 画布基准参数 (像素标定: 4 px/mm, 即 40 px/cm, ~101.6 DPI)
PX_PER_MM = 4.0
BOARD_W_MM = 900
BOARD_H_MM = 1200

BOARD_W_PX = int(BOARD_W_MM * PX_PER_MM)   # 3600 px
BOARD_H_PX = int(BOARD_H_MM * PX_PER_MM)   # 4800 px

MARGIN_X_MM = 20      # 左右边距 20mm
MARGIN_TOP_MM = 15    # 顶边距 15mm
GAP_Y_MM = 7          # 模块间呼吸微缝 7mm
MARGIN_BOTTOM_MM = 19 # 底边距 19mm

MARGIN_X_PX = int(MARGIN_X_MM * PX_PER_MM) # 80 px
MARGIN_TOP_PX = int(MARGIN_TOP_MM * PX_PER_MM) # 60 px
GAP_Y_PX = int(GAP_Y_MM * PX_PER_MM) # 28 px

def load_fonts():
    """加载中文字体"""
    font_paths = [
        "/mnt/c/Windows/Fonts/msyhbd.ttc",
        "/mnt/c/Windows/Fonts/msyh.ttc",
        "/mnt/c/Windows/Fonts/simhei.ttf"
    ]
    bold_font_path = None
    reg_font_path = None
    for p in font_paths:
        if os.path.exists(p):
            if not bold_font_path and "bd" in p:
                bold_font_path = p
            elif not reg_font_path:
                reg_font_path = p
    if not bold_font_path:
        bold_font_path = reg_font_path
    return bold_font_path, reg_font_path

def render_pdf_strip(mod_info):
    """
    通过 PyMuPDF 高精度渲染单张背胶写真 PDF，并裁切掉四周 3mm 出血位，
    得到纯净的 860mm x net_h_mm 印刷成品图像。
    """
    pdf_path = mod_info["pdf"]
    print(f"[*] 正在渲染模块: {mod_info['name']}")
    doc = fitz.open(pdf_path)
    page = doc[0]
    
    # 渲染缩放系数: 将 PDF (72 pt/inch) 缩放到 PX_PER_MM (4 px/mm)
    scale = PX_PER_MM * 25.4 / 72.0
    mat = fitz.Matrix(scale, scale)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    
    # 转为 PIL Image
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    # 计算并裁切 3mm 出血位 (四周各裁切 3mm * 4 px/mm = 12 px)
    bleed_px = int(mod_info["bleed_mm"] * PX_PER_MM)
    net_w_px = int(mod_info["net_w_mm"] * PX_PER_MM)
    net_h_px = int(mod_info["net_h_mm"] * PX_PER_MM)
    
    crop_box = (
        bleed_px,
        bleed_px,
        bleed_px + net_w_px,
        bleed_px + net_h_px
    )
    cropped_img = img.crop(crop_box)
    print(f"    -> 原始渲染尺寸: {img.size}, 裁切出血后净尺寸: {cropped_img.size}")
    return cropped_img

def build_full_board_mockup():
    """构建整板 900x1200mm 1:1 实装全景 Mockup"""
    print(f"\n[+] 开始构建 900x1200mm 展板全景 Mockup (分辨率: {BOARD_W_PX}x{BOARD_H_PX} px)...")
    
    # 1. 创建 KT 展板底板画布 (极净工程白)
    board_img = Image.new("RGB", (BOARD_W_PX, BOARD_H_PX), "#FFFFFF")
    draw = ImageDraw.Draw(board_img)
    
    # 2. 依次贴装 4 大模块
    current_y_px = MARGIN_TOP_PX
    rendered_strips = []
    
    for idx, mod in enumerate(MODULES):
        strip_img = render_pdf_strip(mod)
        rendered_strips.append((mod, strip_img, current_y_px))
        
        # 模拟写真背胶真实贴装质感 (微柔和纸张边缘阴影)
        shadow_box = [
            MARGIN_X_PX - 2,
            current_y_px - 1,
            MARGIN_X_PX + strip_img.width + 2,
            current_y_px + strip_img.height + 2
        ]
        draw.rectangle(shadow_box, fill="#E2E8F0")
        
        # 贴入背胶成品
        board_img.paste(strip_img, (MARGIN_X_PX, current_y_px))
        
        # 勾勒极细的写真裁切线
        draw.rectangle(
            [MARGIN_X_PX, current_y_px, MARGIN_X_PX + strip_img.width, current_y_px + strip_img.height],
            outline="#94A3B8",
            width=1
        )
        
        # 累加 Y 坐标 (模块高度 + 间隙)
        current_y_px += strip_img.height + GAP_Y_PX
        
    final_output_path = os.path.join(PREVIEW_DIR, "FULL_BOARD_MASTER_FINAL_MOCKUP.png")
    board_img.save(final_output_path, "PNG", quality=95)
    print(f"[✓] 展板实装渲染图已成功输出至: {final_output_path} (文件大小: {os.path.getsize(final_output_path)/1024/1024:.2f} MB)")
    
    # 3. 构建带专业工程尺寸链的工程架构蓝图
    build_engineering_dimensioned_mockup(board_img, rendered_strips)

def build_engineering_dimensioned_mockup(board_img, rendered_strips):
    """在展板四周扩展并绘制国标标准工程尺寸链与技术图签"""
    print("\n[+] 开始绘制带标准工程尺寸链的 Master Engineering Mockup...")
    
    PAD_LEFT = 240   # 左侧标注各模块垂直高度尺寸链
    PAD_RIGHT = 340  # 右侧标注功能分区与技术指标卡
    PAD_TOP = 140    # 顶部标注总宽 900mm 与净宽 860mm
    PAD_BOTTOM = 160 # 底部标注工艺说明与防代做技术图签
    
    TOTAL_W = BOARD_W_PX + PAD_LEFT + PAD_RIGHT
    TOTAL_H = BOARD_H_PX + PAD_TOP + PAD_BOTTOM
    
    canvas = Image.new("RGB", (TOTAL_W, TOTAL_H), "#0B1522") # 纯正 AutoCAD 钛青工程蓝底
    draw = ImageDraw.Draw(canvas)
    
    # 粘贴展板本体居中
    board_pos_x = PAD_LEFT
    board_pos_y = PAD_TOP
    canvas.paste(board_img, (board_pos_x, board_pos_y))
    
    # 展板外轮廓高亮发光线
    draw.rectangle(
        [board_pos_x - 2, board_pos_y - 2, board_pos_x + BOARD_W_PX + 1, board_pos_y + BOARD_H_PX + 1],
        outline="#38BDF8",
        width=2
    )
    
    bold_font_path, reg_font_path = load_fonts()
    font_large = ImageFont.truetype(bold_font_path, 28)
    font_mid = ImageFont.truetype(bold_font_path, 20)
    font_small = ImageFont.truetype(reg_font_path, 16)
    font_dim = ImageFont.truetype(bold_font_path, 18)
    font_tag = ImageFont.truetype(bold_font_path, 14)
    
    # ---------------- 1. 顶部水平尺寸链 ----------------
    dim_y = board_pos_y - 60
    draw.line([board_pos_x, dim_y, board_pos_x + BOARD_W_PX, dim_y], fill="#38BDF8", width=2)
    draw.line([board_pos_x, dim_y - 12, board_pos_x, dim_y + 12], fill="#38BDF8", width=2)
    draw.line([board_pos_x + BOARD_W_PX, dim_y - 12, board_pos_x + BOARD_W_PX, dim_y + 12], fill="#38BDF8", width=2)
    txt = "900 mm (展板官方总宽)"
    draw.text((board_pos_x + BOARD_W_PX // 2 - 120, dim_y - 35), txt, fill="#38BDF8", font=font_dim)
    
    dim_y2 = board_pos_y - 20
    strip_x1 = board_pos_x + MARGIN_X_PX
    strip_x2 = strip_x1 + int(860 * PX_PER_MM)
    draw.line([strip_x1, dim_y2, strip_x2, dim_y2], fill="#A855F7", width=2)
    draw.line([strip_x1, dim_y2 - 8, strip_x1, dim_y2 + 8], fill="#A855F7", width=2)
    draw.line([strip_x2, dim_y2 - 8, strip_x2, dim_y2 + 8], fill="#A855F7", width=2)
    txt2 = "860 mm (写真背胶净宽 · 左右各留 20mm 边距)"
    draw.text((board_pos_x + BOARD_W_PX // 2 - 190, dim_y2 - 25), txt2, fill="#C084FC", font=font_small)
    
    # ---------------- 2. 左侧垂直尺寸链 ----------------
    dim_x = board_pos_x - 160
    draw.line([dim_x, board_pos_y, dim_x, board_pos_y + BOARD_H_PX], fill="#38BDF8", width=2)
    draw.line([dim_x - 12, board_pos_y, dim_x + 12, board_pos_y], fill="#38BDF8", width=2)
    draw.line([dim_x - 12, board_pos_y + BOARD_H_PX, dim_x + 12, board_pos_y + BOARD_H_PX], fill="#38BDF8", width=2)
    draw.text((dim_x - 65, board_pos_y + BOARD_H_PX // 2 - 20), "1200 mm", fill="#38BDF8", font=font_dim)
    draw.text((dim_x - 75, board_pos_y + BOARD_H_PX // 2 + 10), "(展位总高)", fill="#94A3B8", font=font_small)
    
    dim_sub_x = board_pos_x - 60
    for mod, strip_img, cur_y in rendered_strips:
        y1 = board_pos_y + cur_y
        y2 = y1 + strip_img.height
        draw.line([dim_sub_x, y1, dim_sub_x, y2], fill="#10B981", width=2)
        draw.line([dim_sub_x - 8, y1, dim_sub_x + 8, y1], fill="#10B981", width=2)
        draw.line([dim_sub_x - 8, y2, dim_sub_x + 8, y2], fill="#10B981", width=2)
        
        lbl = f"{mod['net_h_mm']}mm"
        draw.text((dim_sub_x - 70, (y1 + y2) // 2 - 10), lbl, fill="#34D399", font=font_dim)
        
    draw.text((dim_sub_x - 85, board_pos_y + MARGIN_TOP_PX // 2 - 10), "15mm顶距", fill="#94A3B8", font=font_tag)
    draw.text((dim_sub_x - 85, board_pos_y + BOARD_H_PX - 35), "19mm底距", fill="#94A3B8", font=font_tag)
    
    # ---------------- 3. 右侧各模块工程解析卡片 ----------------
    for idx, (mod, strip_img, cur_y) in enumerate(rendered_strips):
        card_x = board_pos_x + BOARD_W_PX + 30
        card_y = board_pos_y + cur_y + 10
        
        draw.line([board_pos_x + BOARD_W_PX, board_pos_y + cur_y + strip_img.height // 2,
                   card_x - 10, card_y + 30], fill="#38BDF8", width=1)
        draw.rectangle([card_x - 14, card_y + 26, card_x - 6, card_y + 34], fill="#38BDF8")
        
        card_w = 290
        card_h = 95 if idx == 0 else (120 if idx == 1 else 160)
        draw.rectangle([card_x, card_y, card_x + card_w, card_y + card_h],
                       fill="#0F2238", outline="#1E4976", width=1)
        
        draw.text((card_x + 12, card_y + 8), mod["id"], fill="#38BDF8", font=font_mid)
        draw.text((card_x + 12, card_y + 32), f"物理净尺寸: 860x{mod['net_h_mm']}mm", fill="#E2E8F0", font=font_tag)
        draw.text((card_x + 12, card_y + 50), f"印刷出血位: 866x{mod['net_h_mm']+6}mm", fill="#94A3B8", font=font_tag)
        
        desc = mod["desc"]
        lines = []
        while len(desc) > 18:
            lines.append(desc[:18])
            desc = desc[18:]
        lines.append(desc)
        for l_idx, l_txt in enumerate(lines[:5]):
            draw.text((card_x + 12, card_y + 70 + l_idx * 16), l_txt, fill="#FBBF24", font=font_tag)

    # ---------------- 4. 底部工程说明与标题图签 ----------------
    foot_y = board_pos_y + BOARD_H_PX + 40
    draw.text((board_pos_x, foot_y),
              "工程施工说明: 1. 采用 5mm 高密度冷板 KT 板为底板; 2. 写真背胶采用 300DPI 哑光抗眩光写真膜; 3. 严格留出 7mm 模块呼吸微缝消除累积张贴形变;",
              fill="#94A3B8", font=font_tag)
    draw.text((board_pos_x, foot_y + 24),
              "红线合规审查: 本展板 100% 杜绝导师姓名、专家信息、专利授权号及既往获奖记录; 研发周期规范标定: 2025.09 - 2026.10 (初三至高一完整演进);",
              fill="#34D399", font=font_tag)
    draw.text((board_pos_x, foot_y + 48),
              "评审合规指令: 第42届瑞安市青少年科技创新大赛 (CASTIC选拔赛) 高中组发明工程学类 · 终极紧凑高信息密度 Master Mockup",
              fill="#38BDF8", font=font_mid)
              
    eng_output_path = os.path.join(PREVIEW_DIR, "FULL_BOARD_MASTER_ENGINEERING_MOCKUP.png")
    canvas.save(eng_output_path, "PNG", quality=95)
    print(f"[✓] 标准工程尺寸链图已成功输出至: {eng_output_path} (文件大小: {os.path.getsize(eng_output_path)/1024/1024:.2f} MB)")

if __name__ == "__main__":
    build_full_board_mockup()
