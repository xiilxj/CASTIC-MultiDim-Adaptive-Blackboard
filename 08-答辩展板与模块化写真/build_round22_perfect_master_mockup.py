#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
第42届瑞安市青少年科技创新大赛 (CASTIC选拔赛)
答辩展板全尺寸总装 Mockup 生成引擎 (第22轮 深度重构·全景工程复核版)
物理规格: 高 1.2m (1200mm) x 宽 0.9m (900mm)
核心重构实现:
  1. 顶栏主标题强化至 44pt 加粗纯白，高度回弹至 92mm，3米外震撼辨识；
  2. 第二区代际演进紧凑三图无缝并列，彻底消除冗余边框与留白，右侧集中写代记录；
  3. 第三区 AutoCAD 4K 蓝图绝对主角霸屏，右侧替换为 Z 系列四大核心工况 4K 渲染图；
  4. 第四区左侧放入用户指定的真实 Blender 物理仿真图，右侧放入时序拓扑矢量流程图；
  5. 严格毫米级物理装配闭环: 14 + 92 + 12 + 180 + 12 + 580 + 12 + 288 + 10 = 1200mm。
==============================================================================
"""

import os
import sys
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(BASE_DIR, "pdf_output")
PREVIEW_DIR = os.path.join(BASE_DIR, "previews")
os.makedirs(PREVIEW_DIR, exist_ok=True)

# 4大核心重构模块参数表 (净尺寸 mm)
MODULES = [
    {
        "id": "MOD-01_02",
        "name": "第一区：官方大赛页眉与44pt超大主标题楣头",
        "pdf": os.path.join(PDF_DIR, "MOD-01_02_MASTER_HEADER_92MM.pdf"),
        "net_w_mm": 860,
        "net_h_mm": 92,
        "bleed_mm": 3,
        "desc": "官方页眉 + 44pt 加粗纯白主标题 + 5大技术胶囊 + 独立研发合规名牌"
    },
    {
        "id": "MOD-GEN12",
        "name": "第二区：代际拓扑演进与失效机理 (三图紧凑连拼+右侧记录)",
        "pdf": os.path.join(PDF_DIR, "MOD-GEN12_COMPACT_EVOLUTION_180MM.pdf"),
        "net_w_mm": 860,
        "net_h_mm": 180,
        "bleed_mm": 3,
        "desc": "市面推拉 ❌ vs 一代悬臂 ❌ vs 二代同轴 ❌ (三图无缝紧凑并列·右侧参数实测)"
    },
    {
        "id": "MOD-GEN3",
        "name": "第三区：【全场核心重点】第三代机构学总装蓝图与四大工况孪生",
        "pdf": os.path.join(PDF_DIR, "MOD-GEN3_HERO_BLUEPRINT_580MM.pdf"),
        "net_w_mm": 860,
        "net_h_mm": 580,
        "bleed_mm": 3,
        "desc": "AutoCAD 4K 蓝图绝对主角 (535mm霸屏) + Z1/Z2/Z3_1/Z3_2 四大工况 4K 原生渲染"
    },
    {
        "id": "MOD-VLM-OPTICS",
        "name": "第四区：Blender 物理光线追踪避光实测与时序闭环流程图",
        "pdf": os.path.join(PDF_DIR, "MOD-VLM_FLOWCHART_FOOTER_288MM_v2.pdf"),
        "net_w_mm": 860,
        "net_h_mm": 288,
        "bleed_mm": 3,
        "desc": "Blender 实机仿真 (黄红蓝光路) + VI 系列时序拓扑矢量流程图 + 官方合规底栏"
    }
]

# 画布基准参数 (像素标定: 4 px/mm -> 3600 x 4800 px, ~101.6 DPI)
PX_PER_MM = 4.0
BOARD_W_MM = 900
BOARD_H_MM = 1200

BOARD_W_PX = int(BOARD_W_MM * PX_PER_MM)   # 3600 px
BOARD_H_PX = int(BOARD_H_MM * PX_PER_MM)   # 4800 px

MARGIN_X_MM = 20      # 左右各 20mm
MARGIN_TOP_MM = 14    # 顶边距 14mm
GAP_Y_MM = 12         # 模块间均匀呼吸微缝 12mm

MARGIN_X_PX = int(MARGIN_X_MM * PX_PER_MM)     # 80 px
MARGIN_TOP_PX = int(MARGIN_TOP_MM * PX_PER_MM) # 56 px
GAP_Y_PX = int(GAP_Y_MM * PX_PER_MM)           # 48 px

def load_fonts():
    """加载中文字体"""
    font_paths = [
        "/mnt/c/Windows/Fonts/msyhbd.ttc",
        "/mnt/c/Windows/Fonts/msyh.ttc",
        "/mnt/c/Windows/Fonts/simhei.ttf"
    ]
    bold_path = None
    reg_path = None
    for p in font_paths:
        if os.path.exists(p):
            if not bold_path and "bd" in p:
                bold_path = p
            elif not reg_path:
                reg_path = p
    if not bold_path:
        bold_path = reg_path
    
    def get_font(size, bold=False):
        p = bold_path if bold else reg_path
        if p and os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
        return ImageFont.load_default()
    
    return get_font

def render_pdf_exact_net(pdf_path, bleed_mm=3):
    """
    使用 PyMuPDF 高精渲染 PDF 第一页，并精确裁切四周 3mm 印刷出血位
    返回裁切出血位后的纯净净尺寸图像 (PIL Image)
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF 文件未找到: {pdf_path}")
    
    doc = fitz.open(pdf_path)
    page = doc[0]
    
    # 渲染倍率计算 (目标 4 px/mm，PDF 原始 72 DPI 即 72/25.4 = 2.8346 pt/mm)
    # scale = 4.0 / (72 / 25.4) ≈ 1.4111
    # 为保证超清，采用 2.5 倍超采样渲染后高质量缩放
    zoom = 2.5
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    
    # 计算出血位在渲染图上的像素占比
    page_w_pt = page.rect.width
    page_h_pt = page.rect.height
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    doc.close()
    
    page_w_mm = page_w_pt * 25.4 / 72.0
    page_h_mm = page_h_pt * 25.4 / 72.0
    
    # 计算左右上下裁切像素
    crop_x_ratio = bleed_mm / page_w_mm
    crop_y_ratio = bleed_mm / page_h_mm
    
    left = int(img.width * crop_x_ratio)
    top = int(img.height * crop_y_ratio)
    right = int(img.width * (1.0 - crop_x_ratio))
    bottom = int(img.height * (1.0 - crop_y_ratio))
    
    net_img = img.crop((left, top, right, bottom))
    return net_img

def build_full_board():
    print("=" * 70)
    print(">>> 启动第22轮答辩展板全尺寸总装 Mockup 装配流水线...")
    print(f">>> 展板物理目标: {BOARD_W_MM}mm x {BOARD_H_MM}mm | 分辨率标定: {BOARD_W_PX} x {BOARD_H_PX} px")
    print("=" * 70)
    
    get_font = load_fonts()
    
    # 1. 创建两张底图：纯净成品展板 & 带工程标注展板
    board_final = Image.new("RGB", (BOARD_W_PX, BOARD_H_PX), (255, 255, 255))
    
    # 工程标注图带有外围 120px 的标注标尺扩展区
    EXT_X = 140
    EXT_Y = 100
    eng_w_px = BOARD_W_PX + EXT_X * 2
    eng_h_px = BOARD_H_PX + EXT_Y * 2
    board_eng = Image.new("RGB", (eng_w_px, eng_h_px), (15, 23, 42))  # 深色工程工作台底色
    
    # 在工程图上画出 900x1200 的白色展板物理边界
    board_eng_paste_x = EXT_X
    board_eng_paste_y = EXT_Y
    
    current_y_mm = MARGIN_TOP_MM
    draw_eng = ImageDraw.Draw(board_eng)
    
    # 逐个模块进行高精裁切与贴合装配
    for idx, mod in enumerate(MODULES):
        print(f"\n[{idx+1}/4] 处理模块: {mod['name']}")
        print(f"      PDF源文件: {os.path.basename(mod['pdf'])}")
        print(f"      净尺寸: {mod['net_w_mm']}mm x {mod['net_h_mm']}mm (出血: {mod['bleed_mm']}mm)")
        
        # 渲染并剔除出血位
        net_img = render_pdf_exact_net(mod["pdf"], bleed_mm=mod["bleed_mm"])
        
        # 缩放至总装标准物理像素
        target_w_px = int(mod["net_w_mm"] * PX_PER_MM)
        target_h_px = int(mod["net_h_mm"] * PX_PER_MM)
        net_img_scaled = net_img.resize((target_w_px, target_h_px), Image.Resampling.LANCZOS)
        
        # 计算当前模块的粘贴坐标
        paste_x_px = MARGIN_X_PX
        paste_y_px = int(current_y_mm * PX_PER_MM)
        
        # 贴到纯净展板上
        board_final.paste(net_img_scaled, (paste_x_px, paste_y_px))
        
        # 贴到工程标注图上
        board_eng.paste(net_img_scaled, (board_eng_paste_x + paste_x_px, board_eng_paste_y + paste_y_px))
        
        # 绘制工程标注辅助线与标尺
        # 右侧标注线
        line_y_mid = board_eng_paste_y + paste_y_px + target_h_px // 2
        line_x_start = board_eng_paste_x + paste_x_px + target_w_px + 10
        line_x_end = board_eng_paste_x + BOARD_W_PX + 30
        
        draw_eng.line([(line_x_start, line_y_mid), (line_x_end, line_y_mid)], fill=(56, 189, 248), width=2)
        draw_eng.rectangle(
            [line_x_end + 10, line_y_mid - 25, line_x_end + 340, line_y_mid + 25],
            fill=(14, 116, 144),
            outline=(56, 189, 248),
            width=2
        )
        
        # 标注文本
        dim_text = f"{mod['id']}: {mod['net_w_mm']}x{mod['net_h_mm']}mm"
        sub_text = f"高度占比: {mod['net_h_mm']/1200.0*100:.1f}%"
        draw_eng.text((line_x_end + 20, line_y_mid - 20), dim_text, fill=(255, 255, 255), font=get_font(18, bold=True))
        draw_eng.text((line_x_end + 20, line_y_mid + 3), sub_text, fill=(186, 230, 253), font=get_font(14))
        
        # 累计 Y 坐标
        current_y_mm += mod["net_h_mm"] + GAP_Y_MM
    
    # 绘制外围展板 900x1200mm 轮廓线与出血裁切标记
    draw_eng.rectangle(
        [board_eng_paste_x, board_eng_paste_y, board_eng_paste_x + BOARD_W_PX, board_eng_paste_y + BOARD_H_PX],
        outline=(239, 68, 68),
        width=3
    )
    
    # 顶部工程大标题
    eng_title = "第42届瑞安市青创赛 · 答辩展板全尺寸总装审定图 (900mm x 1200mm 模块化写真背胶)"
    eng_sub = "重构成果: ①顶栏44pt超大标题 | ②前三代无缝紧凑并列 | ③第三代4K蓝图霸屏+4大工况 | ④Blender物理仿真+时序流程图"
    draw_eng.text((board_eng_paste_x + 20, 25), eng_title, fill=(255, 255, 255), font=get_font(32, bold=True))
    draw_eng.text((board_eng_paste_x + 20, 68), eng_sub, fill=(148, 163, 184), font=get_font(20))
    
    # 保存输出文件
    final_mockup_path = os.path.join(PREVIEW_DIR, "FULL_BOARD_MASTER_FINAL_MOCKUP.png")
    eng_mockup_path = os.path.join(PREVIEW_DIR, "FULL_BOARD_MASTER_ENGINEERING_MOCKUP.png")
    
    print("\n>>> 正在写入全景 Mockup 渲染图文件 (高保真压缩)...")
    board_final.save(final_mockup_path, "PNG", optimize=True)
    board_eng.save(eng_mockup_path, "PNG", optimize=True)
    
    # 同步复制到 artifacts 目录供交互查看
    artifact_dir = "/home/maker/.gemini/antigravity/brain/e3902037-47a7-471b-900e-ab539e91d649"
    os.system(f"cp {final_mockup_path} {artifact_dir}/full_board_master_final_mockup.png")
    os.system(f"cp {eng_mockup_path} {artifact_dir}/full_board_master_engineering_mockup.png")
    
    print("=" * 70)
    print(f"✅ 全尺寸成品总装图生成成功: {final_mockup_path}")
    print(f"✅ 全景工程标注审定图生成成功: {eng_mockup_path}")
    print(f"✅ 已同步至 Artifact 预览目录！")
    print("=" * 70)

if __name__ == "__main__":
    build_full_board()
