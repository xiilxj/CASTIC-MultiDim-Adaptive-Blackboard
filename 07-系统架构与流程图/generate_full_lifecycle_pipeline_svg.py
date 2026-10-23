#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CASTIC GH-VI-2026 全生命周期系统架构与全流程矢量图生成器 (白底黑字高对比度学校黑白打印机特制版)
专为学校黑白激光打印机与学术报告排版优化设计：
1. 彻底消除实心黑色色块，杜绝黑白激光打印机碳粉结块、拉丝或反白字发虚；
2. 纯白背景 (#FFFFFF) + 纯黑线框与高对比度文字 (#000000)，全图平均亮度 > 240，极致清爽锐利；
3. 严格按用户批注拓扑顺序：S系列 ➔ Z系列 ➔ VI系列 ➔ VLMC系列 (GH-VI-2026 旗舰版)；
4. 严格标明 8000mm 满幅极限展开跨度；
5. 深度融合 6 大核心生态标签：matlab2025b, arch linux, linux, Gemini, Antigravity, llama 及 Qwen2.5-VL；
6. 自动输出无损 SVG 并调用 rsvg-convert 编译为独立高保真矢量 PDF。
"""

import os
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SVG_DIR = os.path.join(SCRIPT_DIR, "svg")
os.makedirs(SVG_DIR, exist_ok=True)

SVG_PATH = os.path.join(SVG_DIR, "06_gh_vi_full_lifecycle_system_pipeline.svg")
SVG_WHITE_PATH = os.path.join(SVG_DIR, "06_gh_vi_full_lifecycle_system_pipeline_white.svg")
PDF_PATH = os.path.join(SCRIPT_DIR, "GH-VI-2026_Full_Lifecycle_System_Pipeline_White.pdf")
REPORT_PDF_PATH = os.path.join(SCRIPT_DIR, "..", "04-汇报与交付报告", "GH-VI-2026_全生命周期全流程架构图_白底黑字打印版.pdf")

W = 2560
H = 1440

svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">
  <defs>
    <!-- 纯黑矢量箭头 -->
    <marker id="arr-black" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#000000" />
    </marker>
    <marker id="arr-heavy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#000000" />
    </marker>
  </defs>

  <!-- 纯白背景底板与最外层 2.5px 纯黑外框 -->
  <rect width="100%" height="100%" fill="#ffffff" />
  <rect x="15" y="15" width="{W-30}" height="{H-30}" fill="none" stroke="#000000" stroke-width="2.5" rx="8" />

  <!-- ======================== 顶部主标题横幅栏 ======================== -->
  <g transform="translate(45, 35)">
    <!-- 标题线框 (双线工整工业风) -->
    <rect x="0" y="0" width="2470" height="105" rx="6" fill="#ffffff" stroke="#000000" stroke-width="2.5" />
    
    <!-- 标徽区 (白底黑字加粗轮廓，适合黑白打印) -->
    <rect x="20" y="18" width="135" height="32" rx="4" fill="#ffffff" stroke="#000000" stroke-width="2" />
    <text x="87" y="40" font-family="'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="13.5" font-weight="900" fill="#000000" text-anchor="middle">CASTIC 2026</text>

    <rect x="165" y="18" width="180" height="32" rx="4" fill="#ffffff" stroke="#000000" stroke-width="2" />
    <text x="255" y="40" font-family="'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="13.5" font-weight="900" fill="#000000" text-anchor="middle">GH-VI-2026 旗舰版</text>

    <!-- 主标题文字 (纯黑大字号) -->
    <text x="365" y="42" font-family="'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="27" font-weight="900" fill="#000000" letter-spacing="1">
      光衡 (GH-VI-2026) · 多模态智能教学黑板系统全生命周期工程架构与研发链路图
    </text>
    <text x="20" y="85" font-family="'Segoe UI', 'PingFang SC', sans-serif" font-size="13.5" font-weight="bold" fill="#000000">
      FULL-LIFECYCLE PIPELINE: FROM CLASSROOM OPTICAL SENSING TO KINEMATIC TOPOLOGY (S➔Z➔VI➔VLMC, 8000mm), AI REASONING &amp; DIGITAL TWIN CLOSED-LOOP
    </text>

    <!-- 顶部技术标签矩阵 (用户指定 6 大核心标签 + 核心工具链，纯白底黑边框) -->
    <g transform="translate(1540, 20)">
      <rect x="0" y="0" width="128" height="28" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <text x="64" y="19" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">matlab2025b</text>

      <rect x="138" y="0" width="112" height="28" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <text x="194" y="19" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">arch linux</text>

      <rect x="260" y="0" width="85" height="28" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <text x="302" y="19" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">linux</text>

      <rect x="355" y="0" width="138" height="28" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <text x="424" y="19" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">Google Gemini</text>

      <rect x="503" y="0" width="128" height="28" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <text x="567" y="19" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">Antigravity</text>

      <rect x="641" y="0" width="118" height="28" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <text x="700" y="19" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">llama.cpp</text>

      <rect x="769" y="0" width="135" height="28" rx="4" fill="#ffffff" stroke="#000000" stroke-width="2.2" />
      <text x="836" y="19" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="900" fill="#000000" text-anchor="middle">Qwen2.5-VL</text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 5 大阶段泳道布局 (彻底白底，线框与高对比纯黑字体，黑白打印零结块) -->
  <!-- Col 1: 物理痛点与双模感知 (X: 45, W: 460) -->
  <!-- Col 2: 四代拓扑演进 S➔Z➔VI➔VLMC, 8000mm (X: 535, W: 485) -->
  <!-- Col 3: 多模态 AI 大模型中枢 (X: 1045, W: 475) -->
  <!-- Col 4: MATLAB 2025b 物理光学与定向相消 (X: 1545, W: 465) -->
  <!-- Col 5: 360°数字孪生、8席位学生POV与样机 (X: 2035, W: 480) -->
  <!-- ========================================================================= -->

  <!-- ======================== 阶段 1: 物理痛点与双模态感知 ======================== -->
  <g transform="translate(45, 160)">
    <rect x="0" y="0" width="465" height="1225" rx="8" fill="#ffffff" stroke="#000000" stroke-width="2" />
    
    <!-- 泳道标头 (白底黑粗框，醒目大字) -->
    <rect x="0" y="0" width="465" height="58" rx="8" fill="#ffffff" stroke="#000000" stroke-width="2" />
    <circle cx="32" cy="29" r="16" fill="#ffffff" stroke="#000000" stroke-width="2" />
    <text x="32" y="36" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="900" fill="#000000" text-anchor="middle">1</text>
    <text x="64" y="27" font-family="'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="17" font-weight="900" fill="#000000">阶段一 · 现实教学痛点与双模感知</text>
    <text x="64" y="47" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#000000">REAL-WORLD PAIN POINTS &amp; SENSING INPUT</text>

    <!-- 卡片 1.1: 传统黑板三大致命痛点 -->
    <g transform="translate(18, 75)">
      <rect x="0" y="0" width="429" height="340" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <rect x="12" y="12" width="140" height="26" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="82" y="30" font-family="'PingFang SC', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">课堂实测三大痛点</text>
      <text x="164" y="31" font-family="'PingFang SC', sans-serif" font-size="14.5" font-weight="900" fill="#000000">高中教学现场真实测量数据</text>

      <g transform="translate(12, 50)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#000000">
        <!-- 痛点1 -->
        <rect x="0" y="0" width="405" height="80" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.2" />
        <line x1="0" y1="0" x2="0" y2="80" stroke="#000000" stroke-width="5" />
        <text x="14" y="22" font-weight="900" font-size="12.5">⚠️ 痛点 1: 窗侧太阳日光反射“失能眩光盲区”</text>
        <text x="14" y="42" fill="#000000">· 教室窗侧斜射日光导致靠窗与对侧 35%~40% 学生板书失真</text>
        <text x="14" y="62" font-weight="bold">· 动态对比度骤降至 1:1.15 (严重死白)，引起持续眯眼疲劳</text>

        <!-- 痛点2 -->
        <rect x="0" y="92" width="405" height="80" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.2" />
        <line x1="0" y1="0" x2="0" y2="80" stroke="#000000" stroke-width="5" />
        <text x="14" y="114" font-weight="900" font-size="12.5">⚠️ 痛点 2: 86寸交互大屏与物理板书面积互斥</text>
        <text x="14" y="134" fill="#000000">· 传统推拉黑板推开时板书折损 50% 以上，合拢则遮挡大屏</text>
        <text x="14" y="154" font-weight="bold">· 无法同时兼顾“全幅沉浸板书”与“数字化多媒体教学协同”</text>

        <!-- 痛点3 -->
        <rect x="0" y="184" width="405" height="80" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.2" />
        <line x1="0" y1="0" x2="0" y2="80" stroke="#000000" stroke-width="5" />
        <text x="14" y="206" font-weight="900" font-size="12.5">⚠️ 痛点 3: 粉笔灰沉降堆积与机械滑道“活塞卡阻”</text>
        <text x="14" y="226" fill="#000000">· 长期粉笔粉尘堆积下部导轨形成气压密封活塞效应</text>
        <text x="14" y="246" font-weight="bold">· 传统滑道推拉干涩沉重、机构卡滞、机械构件快速磨损</text>
      </g>
    </g>

    <!-- 卡片 1.2: 双模态物理感知采集输入 -->
    <g transform="translate(18, 435)">
      <rect x="0" y="0" width="429" height="360" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <rect x="12" y="12" width="145" height="26" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="84" y="30" font-family="'PingFang SC', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">多传感器输入流</text>
      <text x="169" y="31" font-family="'PingFang SC', sans-serif" font-size="14.5" font-weight="900" fill="#000000">双流物理特征融合捕获</text>

      <g transform="translate(12, 50)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#000000">
        <!-- 流 1: 学生人脸 -->
        <rect x="0" y="0" width="405" height="138" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.2" />
        <text x="12" y="22" font-weight="900" font-size="12.5">📷 真实世界学生视觉感知 (CAM 1 / DJI Osmo 广角)</text>
        <text x="12" y="44" fill="#000000">· 边缘轻量端侧 YuNet 人脸检测器 (60 FPS 稳定追踪)</text>
        <text x="12" y="66" fill="#000000">· 68 点人脸关键特征拓扑精确定位双眼轮廓点 (P1~P6)</text>
        <text x="12" y="88" font-weight="bold">· 眼裂长宽比公式: EAR = (|p2-p6| + |p3-p5|) / (2|p1-p4|)</text>
        <text x="12" y="112" font-weight="900">· 阈值触发: 当 EAR &lt; 0.20 持续 300ms 判定为眯眼避光应激！</text>

        <!-- 流 2: 虚拟强光 -->
        <rect x="0" y="150" width="405" height="138" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.2" />
        <text x="12" y="172" font-weight="900" font-size="12.5">🔦 3D 虚拟光源手电筒物理反射流 (Virtual Flashlight)</text>
        <text x="12" y="194" fill="#000000">· 视口实时鼠标交互：移动光斑中心坐标 (X_fl, Y_fl)</text>
        <text x="12" y="216" fill="#000000">· 光照强度连续可调：0 ~ 5000 Lux 动态演进</text>
        <text x="12" y="238" font-weight="bold">· 空间法向偏角: θ_inc = arccos(N · L) 镜面反射光路</text>
        <text x="12" y="260" font-weight="900">· 8 席位反射落点追踪: 动态映射激光直射的受灾学生座位</text>
      </g>
    </g>

    <!-- 卡片 1.3: 48 席位空间人体工学模型 -->
    <g transform="translate(18, 815)">
      <rect x="0" y="0" width="429" height="385" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <rect x="12" y="12" width="135" height="26" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="79" y="30" font-family="'PingFang SC', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">空间人体工学</text>
      <text x="159" y="31" font-family="'PingFang SC', sans-serif" font-size="14.5" font-weight="900" fill="#000000">48 席位标准教室三维网格</text>

      <g transform="translate(12, 50)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#000000">
        <text x="6" y="18" fill="#000000">· 教室标准体量: 10.0m × 7.5m × 3.6m 标准中学普通教室</text>
        <text x="6" y="38" fill="#000000">· 席位网格: 6 列 × 8 排 = 48 个三维独立人体工学坐标席位</text>
        <text x="6" y="58" font-weight="bold">· 核心观测席位 8 点透视矩阵 (Seats #1 ~ #8):</text>
        <text x="16" y="78">- 席位#1: 前排左侧深区 (Yaw: -24°, Pitch: -5.0°)</text>
        <text x="16" y="98">- 席位#2: 前排正中标准席 (Yaw: 0.0°, Pitch: -4.0°)</text>
        <text x="16" y="118">- 席位#3: 前排右侧深区 (Yaw: +24°, Pitch: -5.0°)</text>
        <text x="16" y="138">- 席位#4/#5: 中排左右观察席 (Yaw: ±14°, Pitch: -3.5°)</text>
        <text x="16" y="158">- 席位#6/#8: 后排左右广角席 (Yaw: ±32°, Pitch: -3.0°)</text>
        <text x="16" y="178">- 席位#7: 后排正中俯瞰席 (Yaw: 0.0°, Pitch: -2.5°)</text>
        
        <!-- 重点结论线框 (双线白底黑字) -->
        <rect x="0" y="196" width="405" height="115" rx="4" fill="#ffffff" stroke="#000000" stroke-width="2" />
        <text x="14" y="224" font-weight="900" font-size="13">🎯 视网膜光线相交判定定理</text>
        <text x="14" y="248" font-size="12">若反射光束向量 R 与学生眼睛观察向量 E 夹角 &lt; 8.5°:</text>
        <text x="14" y="272" font-weight="900" font-size="13">➔ 判定该席位发生失能强眩光 (Disability Glare Strike!)</text>
        <text x="14" y="294" font-size="12" font-weight="bold">自动触发系统多模态推理机进入定向相消调控状态</text>
      </g>
    </g>
  </g>

  <!-- ======================== 阶段 2: 机械机构学四代拓扑演进 ======================== -->
  <!-- 严格按照用户确认顺序: S -> Z -> VI -> VLMC，最大跨度 8000mm -->
  <g transform="translate(535, 160)">
    <rect x="0" y="0" width="485" height="1225" rx="8" fill="#ffffff" stroke="#000000" stroke-width="2" />
    
    <!-- 泳道标头 -->
    <rect x="0" y="0" width="485" height="58" rx="8" fill="#ffffff" stroke="#000000" stroke-width="2" />
    <circle cx="32" cy="29" r="16" fill="#ffffff" stroke="#000000" stroke-width="2" />
    <text x="32" y="36" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="900" fill="#000000" text-anchor="middle">2</text>
    <text x="64" y="27" font-family="'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="17" font-weight="900" fill="#000000">阶段二 · 四代机构拓扑演进 (S➔Z➔VI➔VLMC)</text>
    <text x="64" y="47" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#000000">MECHANICAL TOPOLOGY: S➔Z➔VI➔VLMC (8000mm MAX)</text>

    <!-- 卡片 2.1: S系列初代 -->
    <g transform="translate(18, 75)">
      <rect x="0" y="0" width="449" height="235" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <rect x="12" y="12" width="135" height="26" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="79" y="30" font-family="'PingFang SC', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">第一代 · S系列</text>
      <text x="159" y="31" font-family="'PingFang SC', sans-serif" font-size="14" font-weight="900" fill="#000000">阻尼偏心单铰链 178° 翻折机构</text>

      <g transform="translate(12, 50)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#000000">
        <text x="0" y="18" font-weight="bold">· 核心拓扑: 偏心单回转副 (Single Hinge 178° Folding)</text>
        <text x="0" y="38">· 解决目标: 初步实现中置大屏遮蔽保护与物理板面简单翻开</text>
        <text x="0" y="58" font-weight="bold">· 系统跨度: 固定 4000mm 刚性跨度</text>
        <text x="0" y="80" font-weight="900">· 代际技术局限与痛点 (促成下一代演进):</text>
        <text x="10" y="100">- 仅能单向横向翻开，无法适应三维教室不同席位光路偏转</text>
        <text x="10" y="120">- 双层折叠时外凸严重 (厚度>85mm)，书写手感悬空振动大</text>
        <text x="10" y="140">- 无落灰防尘结构，下导轨极易被粉笔灰粉尘卡死故障</text>
      </g>
    </g>

    <!-- 连接箭头 1 -->
    <path d="M 242 320 L 242 345" stroke="#000000" stroke-width="2.5" marker-end="url(#arr-black)" />

    <!-- 卡片 2.2: Z系列第二代 -->
    <g transform="translate(18, 350)">
      <rect x="0" y="0" width="449" height="235" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <rect x="12" y="12" width="135" height="26" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="79" y="30" font-family="'PingFang SC', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">第二代 · Z系列</text>
      <text x="159" y="31" font-family="'PingFang SC', sans-serif" font-size="14" font-weight="900" fill="#000000">对角线双铰链两折叠并成拓扑</text>

      <g transform="translate(12, 50)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#000000">
        <text x="0" y="18" font-weight="bold">· 核心拓扑: 对角线双铰链正交解耦 (Z-Fold Topology)</text>
        <text x="0" y="38">· 突破创新: 将内侧折叠副与外侧回转副在俯视截面对角分离</text>
        <text x="0" y="58" font-weight="900">· 厚度极限压缩: 双层贴合总厚度极限压至 26mm (超薄致密)</text>
        <text x="0" y="78">· 系统跨度: 4000mm 初始闭合 ➔ 4000mm 露屏贴合</text>
        <text x="0" y="100" font-weight="900">· 代际技术局限与痛点:</text>
        <text x="10" y="120">- 缺乏三维空间俯仰与横向大跨度动态延展机构</text>
        <text x="10" y="140">- 仍停留在纯机械被动调节，未结合智能光敏与人因视网膜闭环</text>
      </g>
    </g>

    <!-- 连接箭头 2 -->
    <path d="M 242 595 L 242 620" stroke="#000000" stroke-width="2.5" marker-end="url(#arr-black)" />

    <!-- 卡片 2.3: VI系列第三代 -->
    <g transform="translate(18, 625)">
      <rect x="0" y="0" width="449" height="245" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <rect x="12" y="12" width="135" height="26" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="79" y="30" font-family="'PingFang SC', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">第三代 · VI系列</text>
      <text x="159" y="31" font-family="'PingFang SC', sans-serif" font-size="14" font-weight="900" fill="#000000">三维空间逆向光路追溯避光机构</text>

      <g transform="translate(12, 50)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#000000">
        <text x="0" y="18" font-weight="bold">· 核心拓扑: 空间三自由度避光联动 (偏航 Yaw + 俯仰 Pitch + 侧滑)</text>
        <text x="0" y="38">· 光学机理: 建立教室 48 席位高程反射模型，反弹强光至吸光顶棚</text>
        <text x="0" y="58" font-weight="900">· 避光偏转角: 支持黑板朝向外偏转 +8.0° ~ +18.0°</text>
        <text x="0" y="78">· 视野改善: 靠窗学生视线 IMAX 夹角由 28° 提升至 44.5°</text>
        <text x="0" y="100" font-weight="900">· 代际技术局限与痛点:</text>
        <text x="10" y="120">- 最大展开跨度受限，黑板边缘仍存在局部反光溢出</text>
        <text x="10" y="140">- 缺乏端侧大模型认知大脑与洗墙灯主动定向相消能力</text>
      </g>
    </g>

    <!-- 连接箭头 3 -->
    <path d="M 242 880 L 242 905" stroke="#000000" stroke-width="2.5" marker-end="url(#arr-black)" />

    <!-- 卡片 2.4: VLMC系列第四代终极旗舰 (8000mm 展开大一统) -->
    <g transform="translate(18, 910)">
      <rect x="0" y="0" width="449" height="280" rx="6" fill="#ffffff" stroke="#000000" stroke-width="2.5" />
      <rect x="12" y="12" width="175" height="26" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <text x="99" y="30" font-family="'PingFang SC', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">第四代旗舰 · VLMC系列</text>
      <text x="199" y="31" font-family="'PingFang SC', sans-serif" font-size="13.5" font-weight="900" fill="#000000">GH-VI-2026 大模型多模态闭环系统</text>

      <g transform="translate(12, 50)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#000000">
        <text x="0" y="18" font-weight="900" font-size="12.5">🌟 8000mm 满幅极限展开大一统三大工况:</text>
        <text x="10" y="38" font-weight="bold">1. 工况一【4000mm 全覆盖封屏态】: 外层副板180°合拢锁死 (F1)</text>
        <text x="10" y="58" font-weight="bold">2. 工况二【4000mm 致密叠合露屏态】: 露86寸屏，叠合厚26mm (F200)</text>
        <text x="10" y="78" font-weight="900">3. 工况三【8000mm 极限满幅全景展开态】: 套杆极限外伸超宽黑板 (F480)</text>
        <text x="0" y="104" font-weight="bold">🛡️ 双横梁自洁防卡阻专利导轨:</text>
        <text x="10" y="124">· 倒 V 型 EPDM 弹性遮尘罩，物理隔绝 92% 直落粉笔灰</text>
        <text x="10" y="144">· 轴向 Φ12mm 垂直落灰孔 + 尼龙刮尘毛刷自洁，消除活塞气阻</text>
        <text x="0" y="168" font-weight="bold">🔄 驱动联动: 步进电机 + 伺服舵机 + 4 组自适应相消洗墙灯</text>
        <text x="10" y="188" font-weight="900">· 响应闭环时间 &lt; 850ms，数字孪生 60FPS 双向投屏映射</text>
      </g>
    </g>
  </g>

  <!-- ======================== 阶段 3: 多模态 AI 大模型与调度中枢 ======================== -->
  <g transform="translate(1045, 160)">
    <rect x="0" y="0" width="475" height="1225" rx="8" fill="#ffffff" stroke="#000000" stroke-width="2" />
    
    <!-- 泳道标头 (高亮显示 Linux, Arch Linux, Gemini, Antigravity, Llama, Qwen2.5-VL) -->
    <rect x="0" y="0" width="475" height="58" rx="8" fill="#ffffff" stroke="#000000" stroke-width="2" />
    <circle cx="32" cy="29" r="16" fill="#ffffff" stroke="#000000" stroke-width="2" />
    <text x="32" y="36" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="900" fill="#000000" text-anchor="middle">3</text>
    <text x="64" y="27" font-family="'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="17" font-weight="900" fill="#000000">阶段三 · 多模态 AI 认知大脑与大模型矩阵</text>
    <text x="64" y="47" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#000000">AI AGENT MATRIX &amp; MULTIMODAL LLM REASONING</text>

    <!-- 卡片 3.1: 基础设施底座与操作系统 (Arch Linux / Linux) -->
    <g transform="translate(18, 75)">
      <rect x="0" y="0" width="439" height="215" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <rect x="12" y="12" width="165" height="26" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="94" y="30" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">Linux / Arch Linux</text>
      <text x="188" y="31" font-family="'PingFang SC', sans-serif" font-size="14" font-weight="900" fill="#000000">高性能端侧系统运行底座</text>

      <g transform="translate(12, 50)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#000000">
        <text x="0" y="18" font-weight="bold">🐧 Arch Linux 滚动更新生产研发环境:</text>
        <text x="10" y="38">· Linux 6.x 高性能微内核，原生 POSIX 纳秒级高精度任务调度</text>
        <text x="10" y="58">· 跨系统协同: WSL2 Arch Linux ⟷ Windows 11 双栖调度</text>
        <text x="10" y="78">· 现代化依赖管理工具链与本地极速 Python 3.10/3.12 运行时</text>
        <text x="0" y="104" font-weight="bold">⚡ 硬件抽象与加速层 (Hardware HAL):</text>
        <text x="10" y="124">· Intel Arc GPU oneAPI SyCL / Level-Zero 高性能渲染加速</text>
        <text x="10" y="144">· OpenCV VideoCapture V4L2 低延迟多相机流硬件直通</text>
      </g>
    </g>

    <!-- 卡片 3.2: 调度中枢与多智能体编排 (Google Antigravity Agent) -->
    <g transform="translate(18, 310)">
      <rect x="0" y="0" width="439" height="215" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <rect x="12" y="12" width="165" height="26" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="94" y="30" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">Google Antigravity</text>
      <text x="188" y="31" font-family="'PingFang SC', sans-serif" font-size="14" font-weight="900" fill="#000000">智能体编排与闭环自动化中枢</text>

      <g transform="translate(12, 50)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#000000">
        <text x="0" y="18" font-weight="bold">🚀 Antigravity Agentic Workflow 编排框架:</text>
        <text x="10" y="38">· 自动化全生命周期监控: 研发、测试、仿真、报告一键闭环</text>
        <text x="10" y="58">· 跨模型工作流编排: 统筹调度 Gemini、Llama、Qwen2.5-VL</text>
        <text x="10" y="78">· 严苛审计日志与自愈机制: 75 轮严苛闭环验证无死角追踪</text>
        <text x="0" y="104" font-weight="bold">📡 MCP (Model Context Protocol) 扩展协议:</text>
        <text x="10" y="124">· 原生控制 Blender 3D 视口、Windows 系统总线与 MATLAB 仿真</text>
        <text x="10" y="144">· 实时感知流毫秒级分发至各决策子智能体</text>
      </g>
    </g>

    <!-- 卡片 3.3: 顶层多模态认知研判 (Google Gemini & Meta Llama) -->
    <g transform="translate(18, 545)">
      <rect x="0" y="0" width="439" height="245" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <rect x="12" y="12" width="175" height="26" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="99" y="30" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">Gemini ⟷ llama.cpp</text>
      <text x="199" y="31" font-family="'PingFang SC', sans-serif" font-size="14" font-weight="900" fill="#000000">云端长视域与边缘本地协同推理</text>

      <g transform="translate(12, 50)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#000000">
        <text x="0" y="18" font-weight="bold">🧠 Google Gemini 多模态全局空间因果研判:</text>
        <text x="10" y="38">· 2M+ 超长上下文理解全天候教室光环境时空转移拓扑</text>
        <text x="10" y="58">· 评估太阳高度角变化与多学生席位遮蔽的最优策略解</text>
        <text x="0" y="84" font-weight="bold">🦙 llama.cpp 本地端侧高性能轻量推理引擎:</text>
        <text x="10" y="104">· 本地化纯离线安全部署，无需外网依赖，极速响应</text>
        <text x="10" y="124">· 将高级语义策略解析为低级机构动作状态机</text>
        <text x="10" y="144" font-weight="900">· 双脑协同: Gemini 负责宏观因果研判，llama.cpp 负责本地毫秒级推理分发</text>
      </g>
    </g>

    <!-- 卡片 3.4: 端侧实时视觉语言推理机 (Qwen2.5-VL) 与工具调用 -->
    <g transform="translate(18, 810)">
      <rect x="0" y="0" width="439" height="385" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <rect x="12" y="12" width="165" height="26" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="94" y="30" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">Qwen2.5-VL Edge</text>
      <text x="188" y="31" font-family="'PingFang SC', sans-serif" font-size="14" font-weight="900" fill="#000000">端侧视觉语言推理与 Tool Call</text>

      <g transform="translate(12, 50)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#000000">
        <text x="0" y="18" font-weight="bold">🔍 端侧实时视觉感知与因果链推理 (Causal Logic):</text>
        <text x="10" y="38">· 输入帧合成: 学生摄像头面部特写 + 3D 虚拟黑板反光视口</text>
        <text x="10" y="58" font-weight="bold">· 毫秒级因果解释输出 (Terminal Output):</text>
        <text x="16" y="78">"识别到前排右侧学生持续眯眼 (EAR=0.18)，黑板右半区存在</text>
        <text x="16" y="98"> 强光斑(2200 Lux)，判定为失能眩光，必须执行定向相消！"</text>

        <rect x="0" y="115" width="415" height="205" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
        <text x="12" y="138" font-weight="900">⚙️ 结构化自主工具分发 (Agent Tool Calling):</text>
        
        <text x="12" y="162" font-family="'Consolas', monospace" font-size="11.5" font-weight="bold">1. api_adjust_blackboard(mode=3, yaw=18.0, span=8000)</text>
        <text x="22" y="179" font-size="11" font-weight="bold">➔ 驱动黑板展开至 8000mm 满幅形态并偏航 18° 避光</text>

        <text x="12" y="201" font-family="'Consolas', monospace" font-size="11.5" font-weight="bold">2. api_steer_washlight(lamp_id=2, pan=-14.2, tilt=18.5, P=220W)</text>
        <text x="22" y="218" font-size="11" font-weight="bold">➔ 驱动 #2 号洗墙灯定向偏转射向反射点，开启 220W 高能相消</text>

        <text x="12" y="240" font-family="'Consolas', monospace" font-size="11.5" font-weight="bold">3. api_set_smart_blinds(level=65%, angle=35.0)</text>
        <text x="22" y="257" font-size="11" font-weight="bold">➔ 调控侧窗百叶帘偏折外部直射日光</text>

        <text x="12" y="279" font-family="'Consolas', monospace" font-size="11.5" font-weight="bold">4. api_notify_student_pov(track_seat=3, counter_active=True)</text>
        <text x="22" y="296" font-size="11" font-weight="bold">➔ 驱动数字孪生自动切换至受灾席位#3，呈现相消对比</text>
      </g>
    </g>
  </g>

  <!-- ======================== 阶段 4: MATLAB 2025b 物理光学与定向相消 ======================== -->
  <g transform="translate(1545, 160)">
    <rect x="0" y="0" width="465" height="1225" rx="8" fill="#ffffff" stroke="#000000" stroke-width="2" />
    
    <!-- 泳道标头 (高亮显示用户指定：MATLAB 2025b 物理光学仿真) -->
    <rect x="0" y="0" width="465" height="58" rx="8" fill="#ffffff" stroke="#000000" stroke-width="2" />
    <circle cx="32" cy="29" r="16" fill="#ffffff" stroke="#000000" stroke-width="2" />
    <text x="32" y="36" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="900" fill="#000000" text-anchor="middle">4</text>
    <text x="64" y="27" font-family="'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="17" font-weight="900" fill="#000000">阶段四 · MATLAB 2025b 物理光学与相消算法</text>
    <text x="64" y="47" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#000000">MATLAB 2025b OPTICAL SIMULATION &amp; COUNTER-BEAM</text>

    <!-- 卡片 4.1: MATLAB 2025b 蒙特卡洛与菲涅尔反射计算 -->
    <g transform="translate(18, 75)">
      <rect x="0" y="0" width="429" height="340" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <rect x="12" y="12" width="165" height="26" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="94" y="30" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">MATLAB 2025b</text>
      <text x="188" y="31" font-family="'PingFang SC', sans-serif" font-size="14" font-weight="900" fill="#000000">蒙特卡洛光线追踪数理模型</text>

      <g transform="translate(12, 50)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#000000">
        <text x="0" y="18" font-weight="bold">📐 菲涅尔空间镜面高程反射公式 (Fresnel Reflection):</text>
        <text x="10" y="38" font-family="'Consolas', monospace" font-weight="bold">R_spec(θ) = 0.5 * (|r_s|^2 + |r_p|^2)</text>
        <text x="10" y="58">其中 r_s, r_p 由折射率 n1(空气=1.0) 与 n2(黑板漆=1.52) 决定</text>
        
        <text x="0" y="86" font-weight="bold">📊 双向反射分布函数 (BRDF) 分解:</text>
        <text x="10" y="106" font-family="'Consolas', monospace" font-weight="bold">f_r(θ_i, θ_r) = k_d * (1/π) + k_s * D(h) * F * G / (4 cosθ_i cosθ_r)</text>
        <text x="10" y="126">· 漫反射项 k_d = 0.88，高光镜面项 k_s = 0.12</text>
        
        <rect x="0" y="145" width="405" height="135" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
        <text x="12" y="167" font-weight="900">📈 MATLAB 2025b 10,000 条光线追迹实测数据:</text>
        <text x="14" y="188">· 初始未调节态: 强眩光光斑照度峰值 E_peak = 3850 Lux</text>
        <text x="14" y="208" font-weight="bold">· 视网膜光强比值: 强反射光 / 漫反射板书 = 11.4:1 (严重过曝)</text>
        <text x="14" y="228" font-weight="bold">· 黑板机构偏航 18° 后: 镜面反射光路向上偏转 36.0° 射向吸光顶棚</text>
        <text x="14" y="248" font-weight="900">· 盲区直接切除率: 48 席位盲区覆盖率从 38.5% 骤降至 0.0%！</text>
      </g>
    </g>

    <!-- 卡片 4.2: 单灯高能自适应洗墙射束相消算子 -->
    <g transform="translate(18, 435)">
      <rect x="0" y="0" width="429" height="360" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <rect x="12" y="12" width="165" height="26" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="94" y="30" font-family="'PingFang SC', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">光路定向相消</text>
      <text x="188" y="31" font-family="'PingFang SC', sans-serif" font-size="14" font-weight="900" fill="#000000">4组洗墙灯自适应光束算法</text>

      <g transform="translate(12, 50)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#000000">
        <text x="0" y="18" font-weight="bold">💡 4 组自适应偏转洗墙灯拓扑 (Lamps #1 ~ #4):</text>
        <text x="10" y="38">· 安装于天花板距黑板 1.2m 导轨处，均布于 X = [-3.0m, +3.0m]</text>
        <text x="10" y="58">· 功率范围: 140W ~ 220W 线性动态可调；发散角: 38° ~ 48°</text>

        <text x="0" y="86" font-weight="bold">🎯 最优偏转角与主灯选定反算函数 (Targeted Steering):</text>
        <text x="10" y="108" font-family="'Consolas', monospace" font-weight="bold">lamp_id = argmin_i |X_lamp(i) - X_glare|</text>
        <text x="10" y="128" font-family="'Consolas', monospace" font-weight="bold">Pan_deg = arctan2(X_glare - X_lamp, Y_glare - Y_lamp)</text>
        <text x="10" y="148" font-family="'Consolas', monospace" font-weight="bold">Tilt_deg = arctan2(Z_lamp - Z_glare, D_horizontal)</text>

        <rect x="0" y="165" width="405" height="140" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
        <text x="12" y="187" font-weight="900">⚡ 定向补光相消物理机理 (Contrast Recovery):</text>
        <text x="14" y="208">· 拒绝“满屋全亮粗暴平铺”，实行精准“单灯高能定向射束”</text>
        <text x="14" y="228">· 高亮白光光锥覆盖黑板反光区，均匀提高字迹周围漫反射照度</text>
        <text x="14" y="248" font-weight="bold">· 动态对比度恢复公式: C = (L_board - L_chalk) / L_board</text>
        <text x="14" y="268" font-weight="900">➔ 实测对比度从 1:1.15 完美恢复至 1:11.8 (国标黄金反差！)</text>
      </g>
    </g>

    <!-- 卡片 4.3: 动态闭环控制时序与收敛判据 -->
    <g transform="translate(18, 815)">
      <rect x="0" y="0" width="429" height="385" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <rect x="12" y="12" width="165" height="26" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="94" y="30" font-family="'PingFang SC', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">闭环稳定性控制</text>
      <text x="188" y="31" font-family="'PingFang SC', sans-serif" font-size="14" font-weight="900" fill="#000000">毫秒级闭环收敛判据</text>

      <g transform="translate(12, 50)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#000000">
        <text x="0" y="18" font-weight="bold">⏱️ 闭环控制响应时序全链路剖析:</text>
        <text x="10" y="38">· t0 (0ms): 摄像头捕获学生眯眼 (EAR &lt; 0.20) / 手电筒开启</text>
        <text x="10" y="58">· t1 (45ms): YuNet 特征提取与光斑反光几何计算完成</text>
        <text x="10" y="78">· t2 (120ms): Qwen2.5-VL 视觉语言大模型推理完成 ToolCall</text>
        <text x="10" y="98">· t3 (180ms): MATLAB 相消功率与偏航角度参数写入 IPC 总线</text>
        <text x="10" y="118">· t4 (420ms): 步进电机与舵机旋转至目标角度 (平滑 S 曲线阻尼)</text>
        <text x="10" y="138">· t5 (780ms): 洗墙灯调光功率升至 220W，光锥完全覆盖</text>
        <text x="10" y="158" font-weight="900">· 全链路总耗时 &lt; 850ms，完全消除人眼延迟感</text>

        <rect x="0" y="178" width="405" height="135" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
        <text x="12" y="202" font-weight="900">🛑 双重收敛退出判据 (Safety &amp; Hysteresis):</text>
        <text x="14" y="224">1. 学生双眼 EAR 恢复至 &gt; 0.25 (眯眼应激解除)</text>
        <text x="14" y="244">2. 视网膜动态对比度稳定在 1:10 以上持续超过 2 秒</text>
        <text x="14" y="264" font-weight="bold">3. 滞后比较器 (Hysteresis): 防止光强微扰引起机构频繁抖动</text>
      </g>
    </g>
  </g>

  <!-- ======================== 阶段 5: 动力学数字孪生、8席位学生POV与样机闭环 ======================== -->
  <g transform="translate(2035, 160)">
    <rect x="0" y="0" width="480" height="1225" rx="8" fill="#ffffff" stroke="#000000" stroke-width="2" />
    
    <!-- 泳道标头 -->
    <rect x="0" y="0" width="480" height="58" rx="8" fill="#ffffff" stroke="#000000" stroke-width="2" />
    <circle cx="32" cy="29" r="16" fill="#ffffff" stroke="#000000" stroke-width="2" />
    <text x="32" y="36" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="900" fill="#000000" text-anchor="middle">5</text>
    <text x="64" y="27" font-family="'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="17" font-weight="900" fill="#000000">阶段五 · 360°数字孪生、8席位POV与样机</text>
    <text x="64" y="47" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#000000">DIGITAL TWIN, 8-SEAT STUDENT POV &amp; PROTOTYPE</text>

    <!-- 卡片 5.1: 3D Blender 5.0 动力学与 360° 自由拖拽视口 -->
    <g transform="translate(18, 75)">
      <rect x="0" y="0" width="444" height="340" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <rect x="12" y="12" width="165" height="26" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="94" y="30" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">Blender 5.0 Cycles</text>
      <text x="188" y="31" font-family="'PingFang SC', sans-serif" font-size="14" font-weight="900" fill="#000000">360° 自由拖拽与高锐度光路</text>

      <g transform="translate(12, 50)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#000000">
        <text x="0" y="18" font-weight="bold">🌐 360° 空间全景环视 (水平/俯仰自由旋转):</text>
        <text x="10" y="38">· 杜绝局限于固定死板机位，支持鼠标左键全向拖拽环视</text>
        <text x="10" y="58">· 清晰查看天花板 4 组光源源头、下射洗墙光锥与相消光路</text>
        <text x="10" y="78" font-weight="900">· 多形态无缝插值: 偏转任意角度下，黑板均可平滑开合变形！</text>

        <rect x="0" y="98" width="420" height="180" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
        <text x="12" y="120" font-weight="900">📐 宏观视口高锐度光学重构 (去虚化，显光路):</text>
        <text x="14" y="142">· 彻底剥除三维黑板视口上的浑浊漫反射高斯模糊层</text>
        <text x="14" y="162" font-weight="bold">· 拉普拉斯锐度达 2096.41，保持墨绿色黑板与白字高反差</text>
        <text x="14" y="182" font-weight="bold">· 鲜明激光光路: 清晰展示入射激光束、靶心准星与反射光线</text>
        <text x="14" y="202" font-weight="bold">· 有形洗墙光锥: 真实展现天花板洗墙灯高能覆盖射束</text>
        <text x="14" y="224" font-weight="900">· 快捷键支持: 按 'V' 键实现 3D 宏观视口与学生微观画中画互换</text>
      </g>
    </g>

    <!-- 卡片 5.2: 8 席位学生第一人称视网膜人因视界 (Student POV) -->
    <g transform="translate(18, 435)">
      <rect x="0" y="0" width="444" height="420" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <rect x="12" y="12" width="165" height="26" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="94" y="30" font-family="'PingFang SC', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">人因视网膜视界</text>
      <text x="188" y="31" font-family="'PingFang SC', sans-serif" font-size="14" font-weight="900" fill="#000000">8席位第一人称失能眩光仿真</text>

      <g transform="translate(12, 50)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#000000">
        <text x="0" y="18" font-weight="bold">👁️ 真实人眼失能眩光模型 (Disability Glare Model):</text>
        <text x="10" y="38">· 彻底解决“学生视角太简陋/不刺眼”痛点，精确模拟角膜散射</text>
        
        <!-- 对比状态 -->
        <rect x="0" y="52" width="420" height="145" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
        <line x1="0" y1="52" x2="0" y2="197" stroke="#000000" stroke-width="5" />
        <text x="14" y="74" font-weight="900">⚠️ 受反射直射态 (刺眼白灼 | 对比度 1:1.15):</text>
        <text x="14" y="94">1. 死白饱和核心 (Specular Core): 中心像素强制死白冲顶</text>
        <text x="14" y="114">2. 8 向睫状晶状体衍射星芒: 模拟睫毛瞳孔高动态刺眼发散</text>
        <text x="14" y="134">3. 眼内光幕前向散射模糊 (Veiling Luminance): 板书被光晕淹没</text>
        <text x="14" y="154" font-weight="900">➔ 学生眼部持续眯眼 (EAR &lt; 0.20)，板书文字完全无法辨识！</text>

        <rect x="0" y="210" width="420" height="120" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
        <line x1="0" y1="210" x2="0" y2="330" stroke="#000000" stroke-width="5" />
        <text x="14" y="232" font-weight="900">⚡ 洗墙相消生效态 (字迹清晰 | 对比度 1:11.8):</text>
        <text x="14" y="252">1. 洗墙灯射束覆盖后，刺眼白灼衰减 90%，高光晕斑彻底消散</text>
        <text x="14" y="272">2. 漫反射均匀度补偿完成，墨绿色黑板与白字反差锐利清晰</text>
        <text x="14" y="292" font-weight="900">➔ 学生双眼自然舒展睁开 (EAR &gt; 0.28)，教学用眼恢复舒适健康</text>

        <text x="0" y="348" font-weight="bold">🎮 席位多维切换控制: 键盘 'S' 键循环切换 8 席位视角</text>
        <text x="10" y="368">· 自动跟踪: 光斑击中哪个席位，画中画自动切至该座位展示</text>
      </g>
    </g>

    <!-- 卡片 5.3: 物理样机试制与闭环验证 (1:10 拓竹 3MF) -->
    <g transform="translate(18, 875)">
      <rect x="0" y="0" width="444" height="325" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <rect x="12" y="12" width="165" height="26" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="94" y="30" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">实物工程验证</text>
      <text x="188" y="31" font-family="'PingFang SC', sans-serif" font-size="14" font-weight="900" fill="#000000">拓竹3D打印样机与电机闭环</text>

      <g transform="translate(12, 50)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#000000">
        <text x="0" y="18" font-weight="bold">🖨️ 1:10 物理微缩实验样机 (Bambu Studio 3MF):</text>
        <text x="10" y="38">· 采用 PETG-CF 碳纤维增强复合耗材，保证铰链刚度与耐磨性</text>
        <text x="10" y="58">· 实物验证对角线双铰链在双层贴合(2.6mm)下的无干涉转动</text>
        <text x="10" y="78">· 倒 V 型导轨配合粉笔灰喷洒实验，实测自洁防卡阻率达 92%</text>

        <text x="0" y="106" font-weight="bold">🔌 硬件机电控制闭环 (ESP32 / 步进电机 / 舵机):</text>
        <text x="10" y="126">· 串口 / WiFi 无线通信接收来自上位机 Python 进程的控制指令</text>
        <text x="10" y="146">· 驱动左/右翻转机构精准偏航避光，驱动洗墙灯舵机精确偏转</text>
        <text x="0" y="174" font-weight="900">🏆 软硬件大一统: 形成集“感知-决策-计算-孪生-实操”于一体的</text>
        <text x="10" y="196" font-weight="900">完整闭环！斩获全国创新大赛工程学硬核技术壁垒！</text>
      </g>
    </g>
  </g>

  <!-- 阶段之间的贯通纯黑实心大箭头 (连接 1->2->3->4->5) -->
  <g stroke="#000000" stroke-width="3" fill="none">
    <!-- 1 -> 2 -->
    <path d="M 510 650 L 535 650" marker-end="url(#arr-black)" />
    <!-- 2 -> 3 -->
    <path d="M 1020 650 L 1045 650" marker-end="url(#arr-black)" />
    <!-- 3 -> 4 -->
    <path d="M 1520 650 L 1545 650" marker-end="url(#arr-black)" />
    <!-- 4 -> 5 -->
    <path d="M 2010 650 L 2035 650" marker-end="url(#arr-black)" />
  </g>

  <!-- 底部闭环反馈大虚线箭头 (5 反馈回 1，形成大闭环) -->
  <g stroke="#000000" stroke-width="2.5" stroke-dasharray="8 6" fill="none">
    <path d="M 2275 1395 L 2275 1415 L 275 1415 L 275 1395" marker-end="url(#arr-black)" />
    <text x="1275" y="1410" font-family="'PingFang SC', sans-serif" font-size="12.5" font-weight="900" fill="#000000" text-anchor="middle">
      🔄 物理光环境自适应相消与学生视网膜健康闭环重构 (FEEDBACK CLOSED-LOOP: EAR RESTORED &gt; 0.28, CONTRAST 1:11.8)
    </text>
  </g>
</svg>
"""

with open(SVG_PATH, "w", encoding="utf-8") as f:
    f.write(svg_content)
with open(SVG_WHITE_PATH, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"[OK] SVG generated at: {SVG_PATH}")
print(f"[OK] SVG white copy at: {SVG_WHITE_PATH}")

# 调用 rsvg-convert 编译为黑白高清矢量 PDF (带文件锁自动重试与版本容错)
target_pdfs = [
    PDF_PATH,
    os.path.join(SCRIPT_DIR, "GH-VI-2026_Full_Lifecycle_Pipeline_v2.pdf"),
    REPORT_PDF_PATH,
    os.path.join(SCRIPT_DIR, "..", "04-汇报与交付报告", "GH-VI-2026_全生命周期流程图_最新版.pdf")
]

for p in target_pdfs:
    try:
        cmd = ["rsvg-convert", "-f", "pdf", "-o", p, SVG_PATH]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"[OK] PDF compiled successfully at: {p}")
    except Exception as e:
        print(f"[SKIP/LOCKED] Could not write {os.path.basename(p)} (may be opened in WPS): {e}")
