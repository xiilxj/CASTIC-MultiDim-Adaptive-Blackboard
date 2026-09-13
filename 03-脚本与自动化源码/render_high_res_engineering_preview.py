# -*- coding: utf-8 -*-
"""
模块化折叠翻转多媒体智能黑板系统 - 300 DPI 工业级高精工程总装渲染脚本
功能：
1. 严格复刻 27216b5ba4f4d28a5775f13fde8d6648.jpg 正交投影视角。
2. 100% 消除多媒体屏幕上的倒三角强光与虚假阴影，呈现平整均匀的高科技微晶防眩光面板。
3. 展现双状态对比：上方【形态一：多自由度折展外展避光状态 (DEPLOYED)】与下方【形态二：标准闭合收拢教学状态 (COMPACT)】。
4. 输出 300 DPI 超清图纸至 D:\\Desktop\\pjhb\\01-CAD工程图纸\\。
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# 设置高精中文字体与矢量抗锯齿
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def render_blackboard_sheet():
    fig, ax = plt.subplots(figsize=(24, 15), dpi=300)
    # AutoCAD 经典深黑/深蓝工作底色
    ax.set_facecolor('#1E1E24')
    fig.patch.set_facecolor('#18181C')

    # 核心尺寸 (mm)
    W_SCREEN, H_SCREEN = 2000.0, 1200.0
    W_INNER_LCD, H_INNER_LCD = 1900.0, 1070.0
    W_BOARD, H_BOARD = 1000.0, 1200.0
    W_FOLD, H_FOLD = 1000.0, 1200.0
    W_CANOPY, H_CANOPY = 2120.0, 90.0

    # 色彩方案 (纯净去反光)
    C_FRAME = '#3A3D40'        # 边框深灰
    C_FRAME_LINE = '#7A8088'   # 边框金属亮线
    C_SCREEN = '#1E4B82'       # 纯净液晶蓝 (无任何倒三角杂光)
    C_SCREEN_LINE = '#2D75D8'  # 屏幕边缘指示线
    C_GREEN = '#2C6343'        # 经典墨绿黑板面
    C_GREEN_LINE = '#4CAF50'   # 黑板边框高亮
    C_WHITE = '#E2E6EA'        # 象牙白多功能副板
    C_WHITE_LINE = '#CFD8DC'
    C_CANOPY = '#2E3842'       # 顶部遮光雨棚
    C_CANOPY_LINE = '#00ACC1'
    C_HINGE = '#FFA000'        # 金黄阻尼铰链

    states = [
        {
            "name": "DEPLOYED",
            "cy": 1600.0,
            "is_deployed": True,
            "title": "形态一：多自由度折展外展避光状态 (DEPLOYED / EXPANDED)",
            "subtitle": "特点：两侧黑板双节向外展开，大屏释放 178° 超广视场无死角盲区，屏幕平整均匀纯净"
        },
        {
            "name": "COMPACT",
            "cy": -350.0,
            "is_deployed": False,
            "title": "形态二：标准闭合收拢教学状态 (COMPACT / CLOSED)",
            "subtitle": "特点：副板折叠内嵌收纳，两侧经典绿板就位，适用于常规大屏演示与板书融合教学"
        }
    ]

    for st in states:
        cy = st["cy"]
        is_dep = st["is_deployed"]
        title_text = st["title"]
        sub_text = st["subtitle"]

        # 1. 顶部 Canopy 遮光雨棚自洁防尘系统
        c_x = -W_CANOPY / 2.0
        c_y = cy + H_SCREEN / 2.0 + 10.0
        canopy = patches.Rectangle((c_x, c_y), W_CANOPY, H_CANOPY,
                                   linewidth=1.5, edgecolor=C_CANOPY_LINE, facecolor=C_CANOPY, zorder=3)
        ax.add_patch(canopy)
        # 倒V防尘罩分层线
        ax.plot([c_x, c_x + W_CANOPY], [c_y + 28.0, c_y + 28.0], color=C_CANOPY_LINE, lw=1.0, zorder=4)
        ax.plot([c_x, c_x + W_CANOPY], [c_y + 58.0, c_y + 58.0], color=C_CANOPY_LINE, lw=1.0, zorder=4)
        # 散热防尘微格栅
        for gx in range(int(c_x) + 100, int(c_x + W_CANOPY) - 100, 150):
            ax.plot([gx, gx + 50], [c_y + 68.0, c_y + 68.0], color='#4DD0E1', lw=1.2, zorder=4)

        # 2. 底部自洁排砂集尘导轨
        b_x = c_x
        b_y = cy - H_SCREEN / 2.0 - 60.0
        tray = patches.Rectangle((b_x, b_y), W_CANOPY, 50.0,
                                 linewidth=1.5, edgecolor=C_FRAME_LINE, facecolor=C_FRAME, zorder=3)
        ax.add_patch(tray)
        # 漏砂孔
        for hx in range(int(b_x) + 150, int(b_x + W_CANOPY) - 150, 300):
            ax.add_patch(patches.Circle((hx, b_y + 25.0), 6.0, edgecolor='#B0BEC5', facecolor='#263238', lw=1.0, zorder=4))

        # 3. 中央多媒体显示屏模块
        s_x = -W_SCREEN / 2.0
        s_y = cy - H_SCREEN / 2.0
        screen_frame = patches.Rectangle((s_x, s_y), W_SCREEN, H_SCREEN,
                                         linewidth=1.8, edgecolor=C_FRAME_LINE, facecolor=C_FRAME, zorder=2)
        ax.add_patch(screen_frame)

        # 液晶屏幕内部显示区 (纯净显示蓝，去反光)
        l_x = -W_INNER_LCD / 2.0
        l_y = s_y + 50.0
        lcd_panel = patches.Rectangle((l_x, l_y), W_INNER_LCD, H_INNER_LCD,
                                      linewidth=1.5, edgecolor=C_SCREEN_LINE, facecolor=C_SCREEN, zorder=3)
        ax.add_patch(lcd_panel)
        # 液晶屏内嵌装饰框
        ax.add_patch(patches.Rectangle((l_x + 8.0, l_y + 8.0), W_INNER_LCD - 16.0, H_INNER_LCD - 16.0,
                                       linewidth=0.8, edgecolor='#64B5F6', facecolor='none', zorder=4))

        # 底部控制区与 VLM 视线跟踪摄像头
        ax.add_patch(patches.Rectangle((-90.0, s_y + 15.0), 180.0, 20.0,
                                       linewidth=1.0, edgecolor='#9E9E9E', facecolor='#212121', zorder=4))
        ax.add_patch(patches.Circle((0.0, s_y + 25.0), 4.5, edgecolor='#FFD54F', facecolor='#FFA000', lw=1.2, zorder=5))

        # 4. 两翼主黑板面 (墨绿色)
        # 左主黑板
        l_bx = -W_SCREEN / 2.0 - 15.0 - W_BOARD
        l_by = cy - H_BOARD / 2.0
        ax.add_patch(patches.Rectangle((l_bx, l_by), W_BOARD, H_BOARD,
                                       linewidth=1.5, edgecolor=C_FRAME_LINE, facecolor=C_FRAME, zorder=3))
        ax.add_patch(patches.Rectangle((l_bx + 20.0, l_by + 20.0), W_BOARD - 40.0, H_BOARD - 40.0,
                                       linewidth=1.2, edgecolor=C_GREEN_LINE, facecolor=C_GREEN, zorder=4))
        # 右主黑板
        r_bx = W_SCREEN / 2.0 + 15.0
        r_by = l_by
        ax.add_patch(patches.Rectangle((r_bx, r_by), W_BOARD, H_BOARD,
                                       linewidth=1.5, edgecolor=C_FRAME_LINE, facecolor=C_FRAME, zorder=3))
        ax.add_patch(patches.Rectangle((r_bx + 20.0, r_by + 20.0), W_BOARD - 40.0, H_BOARD - 40.0,
                                       linewidth=1.2, edgecolor=C_GREEN_LINE, facecolor=C_GREEN, zorder=4))

        # 金属把手与自锁孔
        ax.add_patch(patches.Circle((r_bx + 80.0, cy), 14.0, edgecolor=C_HINGE, facecolor='#263238', lw=1.5, zorder=5))
        ax.add_patch(patches.Circle((r_bx + 80.0, cy), 8.0, edgecolor=C_HINGE, facecolor=C_HINGE, lw=1.0, zorder=5))
        ax.add_patch(patches.Circle((l_bx + W_BOARD - 80.0, cy), 14.0, edgecolor=C_HINGE, facecolor='#263238', lw=1.5, zorder=5))
        ax.add_patch(patches.Circle((l_bx + W_BOARD - 80.0, cy), 8.0, edgecolor=C_HINGE, facecolor=C_HINGE, lw=1.0, zorder=5))

        # 5. 折叠扩展副板 (仅展开态)
        if is_dep:
            # 左副板 (象牙白)
            l_fx = l_bx - 12.0 - W_FOLD
            l_fy = l_by
            ax.add_patch(patches.Rectangle((l_fx, l_fy), W_FOLD, H_FOLD,
                                           linewidth=1.5, edgecolor=C_FRAME_LINE, facecolor=C_FRAME, zorder=3))
            ax.add_patch(patches.Rectangle((l_fx + 20.0, l_fy + 20.0), W_FOLD - 40.0, H_FOLD - 40.0,
                                           linewidth=1.2, edgecolor=C_WHITE_LINE, facecolor=C_WHITE, zorder=4))

            # 左双节铰链
            for hy in [cy + 350.0, cy - 350.0]:
                ax.add_patch(patches.Rectangle((l_fx + W_FOLD, hy - 35.0), 12.0, 70.0,
                                               linewidth=1.0, edgecolor=C_HINGE, facecolor='#FFA000', zorder=5))
                ax.add_patch(patches.Circle((l_fx + W_FOLD + 6.0, hy), 4.5, edgecolor='#FFFFFF', facecolor='#263238', lw=1.0, zorder=6))

            # 右副板 (象牙白)
            r_fx = r_bx + W_BOARD + 12.0
            r_fy = r_by
            ax.add_patch(patches.Rectangle((r_fx, r_fy), W_FOLD, H_FOLD,
                                           linewidth=1.5, edgecolor=C_FRAME_LINE, facecolor=C_FRAME, zorder=3))
            ax.add_patch(patches.Rectangle((r_fx + 20.0, r_fy + 20.0), W_FOLD - 40.0, H_FOLD - 40.0,
                                           linewidth=1.2, edgecolor=C_WHITE_LINE, facecolor=C_WHITE, zorder=4))

            # 右双节铰链
            for hy in [cy + 350.0, cy - 350.0]:
                ax.add_patch(patches.Rectangle((r_bx + W_BOARD, hy - 35.0), 12.0, 70.0,
                                               linewidth=1.0, edgecolor=C_HINGE, facecolor='#FFA000', zorder=5))
                ax.add_patch(patches.Circle((r_bx + W_BOARD + 6.0, hy), 4.5, edgecolor='#FFFFFF', facecolor='#263238', lw=1.0, zorder=6))

        # 标注状态说明
        ax.text(0.0, cy + H_SCREEN / 2.0 + 150.0, title_text,
                color='#ECEFF1', fontsize=15, fontweight='bold', ha='center', va='bottom', zorder=7)
        ax.text(0.0, cy + H_SCREEN / 2.0 + 115.0, sub_text,
                color='#90A4AE', fontsize=11, ha='center', va='bottom', zorder=7)

    # 总标题栏与工程署名
    ax.text(0.0, 2600.0, "一种模块化折叠翻转式多媒体教学黑板及光环境系统 - 正交前视工程总装图",
            color='#FFFFFF', fontsize=21, fontweight='heavy', ha='center', va='center')
    ax.text(0.0, 2520.0, "设计基准: 参考图 27216b5ba4f4d28a5775f13fde8d6648.jpg | 纯净无反光高精矢量工程重构",
            color='#81D4FA', fontsize=12, ha='center', va='center')
    ax.text(0.0, 2460.0, "发明专利申请号: 202511764745.X | 发明人: 林诚俊 | 赛道: 全国青少年科技创新大赛工程学赛道",
            color='#B0BEC5', fontsize=11, ha='center', va='center')

    # 视口范围设定
    ax.set_xlim(-3600, 3600)
    ax.set_ylim(-1250, 2800)
    ax.set_aspect('equal')
    ax.axis('off')

    # 输出高精度 PNG 图纸
    save_path = r"D:\Desktop\pjhb\01-CAD工程图纸\模块化折叠翻转多媒体智能黑板_工程设计渲染总装图_300DPI.png"
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f">>> [SUCCESS] 300 DPI 工业工程图已导出: {save_path}")
    return save_path

if __name__ == "__main__":
    render_blackboard_sheet()
