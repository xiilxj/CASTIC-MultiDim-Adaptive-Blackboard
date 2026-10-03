#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CASTIC GH-VI-2026 核心流程图与架构图高精度 SVG 矢量图生成器
将所有 Plan 中的时序图、拓扑图、双轨工程图、数字孪生闭环图导出为独立无损 SVG
"""

import os

SVG_DIR = r"/mnt/d/Desktop/CASTICpjhb/07-系统架构与流程图/svg"
os.makedirs(SVG_DIR, exist_ok=True)

# -------------------------------------------------------------------------
# 图 1: VI系列多维叠合翻转黑板全生命周期时序拓扑 (Sequence Diagram)
# -------------------------------------------------------------------------
svg_1 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0e17" />
      <stop offset="100%" stop-color="#121826" />
    </linearGradient>
    <linearGradient id="cyanGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00d2ff" />
      <stop offset="100%" stop-color="#00f2fe" />
    </linearGradient>
    <linearGradient id="purpleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#7f00ff" />
      <stop offset="100%" stop-color="#e100ff" />
    </linearGradient>
    <linearGradient id="greenGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#11998e" />
      <stop offset="100%" stop-color="#38ef7d" />
    </linearGradient>
    <linearGradient id="orangeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#f857a6" />
      <stop offset="100%" stop-color="#ff5858" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#00e5ff" />
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#d04aff" />
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#00ff88" />
    </marker>
    <marker id="arrow-orange" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#ff7675" />
    </marker>
  </defs>

  <rect width="100%" height="100%" fill="url(#bgGrad)" />
  <rect x="2" y="2" width="1196" height="896" fill="none" stroke="#202b40" stroke-width="2" rx="12" />

  <!-- Title -->
  <g transform="translate(60, 45)">
    <text font-family="'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="24" font-weight="bold" fill="#ffffff">
      VI 系列多维叠合翻转黑板全生命周期时序拓扑
    </text>
    <text y="25" font-family="'Segoe UI', sans-serif" font-size="13" fill="#00d2ff" letter-spacing="1">
      SEQUENCE DIAGRAM · CASTIC GH-VI-2026 KINEMATIC LIFECYCLE
    </text>
  </g>

  <!-- Lifeline Columns -->
  <!-- Col 1: Fixed (140) -->
  <!-- Col 2: Rods (380) -->
  <!-- Col 3: Frame (620) -->
  <!-- Col 4: DualBoard (860) -->
  <!-- Col 5: FrontBoard (1080) -->

  <!-- Lifeline Headers -->
  <g font-family="'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="13" font-weight="600" text-anchor="middle">
    <!-- Col 1 -->
    <rect x="60" y="95" width="160" height="42" rx="6" fill="#182234" stroke="#00d2ff" stroke-width="1.5" />
    <text x="140" y="121" fill="#ffffff">墙面基底 (固定板+大屏)</text>
    <line x1="140" y1="137" x2="140" y2="840" stroke="#25354e" stroke-dasharray="5 5" stroke-width="1.5" />

    <!-- Col 2 -->
    <rect x="300" y="95" width="160" height="42" rx="6" fill="#182234" stroke="#a29bfe" stroke-width="1.5" />
    <text x="380" y="121" fill="#ffffff">伸缩衍生绳索杆</text>
    <line x1="380" y1="137" x2="380" y2="840" stroke="#25354e" stroke-dasharray="5 5" stroke-width="1.5" />

    <!-- Col 3 -->
    <rect x="540" y="95" width="160" height="42" rx="6" fill="#182234" stroke="#fdcb6e" stroke-width="1.5" />
    <text x="620" y="121" fill="#ffffff">活动支撑框架</text>
    <line x1="620" y1="137" x2="620" y2="840" stroke="#25354e" stroke-dasharray="5 5" stroke-width="1.5" />

    <!-- Col 4 -->
    <rect x="780" y="95" width="160" height="42" rx="6" fill="#182234" stroke="#00b894" stroke-width="1.5" />
    <text x="860" y="121" fill="#ffffff">双层黑板模块(贴合态)</text>
    <line x1="860" y1="137" x2="860" y2="840" stroke="#25354e" stroke-dasharray="5 5" stroke-width="1.5" />

    <!-- Col 5 -->
    <rect x="1000" y="95" width="160" height="42" rx="6" fill="#182234" stroke="#ff7675" stroke-width="1.5" />
    <text x="1080" y="121" fill="#ffffff">最前层可翻折板</text>
    <line x1="1080" y1="137" x2="1080" y2="840" stroke="#25354e" stroke-dasharray="5 5" stroke-width="1.5" />
  </g>

  <!-- Stage 1 Init: COVERED -->
  <g transform="translate(0, 160)">
    <rect x="80" y="0" width="1040" height="30" rx="4" fill="rgba(0, 210, 255, 0.08)" stroke="#00d2ff" stroke-width="1" stroke-dasharray="3 3" />
    <text x="95" y="20" font-family="'PingFang SC', sans-serif" font-size="13" font-weight="bold" fill="#00e5ff">
      阶段 1 初：完全遮蔽形态 (COVERED 4000mm) · 纯板书全覆盖保护大屏
    </text>

    <!-- Message 1 -->
    <path d="M 380 50 C 440 30, 440 70, 390 70" fill="none" stroke="#00e5ff" stroke-width="2" marker-end="url(#arrow)" />
    <text x="450" y="55" font-family="'PingFang SC', sans-serif" font-size="12" fill="#d2f5ff">1. 绳索杆向内侧延伸展开，两端在正中央碰撞对接</text>

    <!-- Message 2 -->
    <line x1="860" y1="95" x2="148" y2="95" stroke="#00e5ff" stroke-width="2" marker-end="url(#arrow)" />
    <text x="500" y="88" font-family="'PingFang SC', sans-serif" font-size="12" fill="#d2f5ff" text-anchor="middle">2. 双层黑板沿内伸杆向中心滑动(保持贴合)，100% 遮蔽中置大屏</text>
  </g>

  <!-- Stage 1 End: COMPACT -->
  <g transform="translate(0, 305)">
    <rect x="80" y="0" width="1040" height="30" rx="4" fill="rgba(162, 155, 254, 0.08)" stroke="#a29bfe" stroke-width="1" stroke-dasharray="3 3" />
    <text x="95" y="20" font-family="'PingFang SC', sans-serif" font-size="13" font-weight="bold" fill="#a29bfe">
      阶段 1 末：退回露屏常态 (COMPACT 4000mm) · 86寸交互大屏露显
    </text>

    <!-- Message 3 -->
    <line x1="860" y1="48" x2="628" y2="48" stroke="#a29bfe" stroke-width="2" marker-end="url(#arrow-purple)" />
    <text x="740" y="40" font-family="'PingFang SC', sans-serif" font-size="12" fill="#e4e0ff" text-anchor="middle">3. 双层黑板向两侧外滑，退至固定黑板正前方</text>

    <!-- Message 4 -->
    <line x1="380" y1="80" x2="612" y2="80" stroke="#a29bfe" stroke-width="2" marker-end="url(#arrow-purple)" />
    <text x="500" y="73" font-family="'PingFang SC', sans-serif" font-size="12" fill="#e4e0ff" text-anchor="middle">4. 绳索杆向外完全缩回，大屏居中完整露出</text>
  </g>

  <!-- Stage 2: YAW/ANTIGLARE -->
  <g transform="translate(0, 440)">
    <rect x="80" y="0" width="1040" height="30" rx="4" fill="rgba(253, 203, 110, 0.08)" stroke="#fdcb6e" stroke-width="1" stroke-dasharray="3 3" />
    <text x="95" y="20" font-family="'PingFang SC', sans-serif" font-size="13" font-weight="bold" fill="#fdcb6e">
      阶段 2：整体多维避光翻动 (YAW +8.0°~+18.0°) · 阳光漫反射重定向至吸光天花板
    </text>

    <!-- Message 5 -->
    <line x1="620" y1="50" x2="148" y2="50" stroke="#fdcb6e" stroke-width="2" marker-end="url(#arrow)" />
    <text x="380" y="42" font-family="'PingFang SC', sans-serif" font-size="12" fill="#ffeaa7" text-anchor="middle">5. 活动框架连同黑板与导轨绕外侧转轴向外偏航翻转，切断学生视网膜眩光</text>
  </g>

  <!-- Stage 3: EXTEND OUT -->
  <g transform="translate(0, 565)">
    <rect x="80" y="0" width="1040" height="30" rx="4" fill="rgba(0, 184, 148, 0.08)" stroke="#00b894" stroke-width="1" stroke-dasharray="3 3" />
    <text x="95" y="20" font-family="'PingFang SC', sans-serif" font-size="13" font-weight="bold" fill="#00b894">
      阶段 3：双梁套杆外伸 (EXTEND OUT +1000mm) · 门式刚架跨度延展
    </text>

    <!-- Message 6 -->
    <line x1="380" y1="50" x2="612" y2="50" stroke="#00b894" stroke-width="2" marker-end="url(#arrow-green)" />
    <text x="500" y="42" font-family="'PingFang SC', sans-serif" font-size="12" fill="#a8ffeb" text-anchor="middle">6. 具有高刚性金属框架的衍生杆从主滑槽横向外伸 1000mm</text>
  </g>

  <!-- Stage 4: PANORAMIC 6M -->
  <g transform="translate(0, 690)">
    <rect x="80" y="0" width="1040" height="30" rx="4" fill="rgba(255, 118, 117, 0.08)" stroke="#ff7675" stroke-width="1" stroke-dasharray="3 3" />
    <text x="95" y="20" font-family="'PingFang SC', sans-serif" font-size="13" font-weight="bold" fill="#ff7675">
      阶段 4：外滑边界与向内翻折补缺 (PANORAMIC 6000mm 终极展开形态)
    </text>

    <!-- Message 7 -->
    <line x1="860" y1="50" x2="388" y2="50" stroke="#ff7675" stroke-width="2" marker-end="url(#arrow-orange)" />
    <text x="620" y="42" font-family="'PingFang SC', sans-serif" font-size="12" fill="#ffd3d3" text-anchor="middle">7. 双层黑板沿外侧衍生杆向外滑动至最外侧限位卡槽边界</text>

    <!-- Message 8 -->
    <line x1="1080" y1="85" x2="868" y2="85" stroke="#ff7675" stroke-width="2" marker-end="url(#arrow-orange)" />
    <text x="970" y="77" font-family="'PingFang SC', sans-serif" font-size="12" fill="#ffd3d3" text-anchor="middle">8. 最前层副板绕内侧铰链向镜头方向朝内翻开 180°，无缝填补中央大屏与侧板空缺！</text>
  </g>
</svg>
"""

# -------------------------------------------------------------------------
# 图 2: Z 系列多维叠合黑板物理拓扑装配与运动学求解主流程 (Graph TD)
# -------------------------------------------------------------------------
svg_2 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 820" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0c101d" />
      <stop offset="100%" stop-color="#141c2c" />
    </linearGradient>
    <linearGradient id="nodeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1a2538" />
      <stop offset="100%" stop-color="#24334d" />
    </linearGradient>
    <filter id="glow2" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <marker id="arrow2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#00d2ff" />
    </marker>
  </defs>

  <rect width="100%" height="100%" fill="url(#bgGrad2)" />
  <rect x="2" y="2" width="996" height="816" fill="none" stroke="#23324d" stroke-width="2" rx="12" />

  <!-- Title -->
  <g transform="translate(50, 45)">
    <text font-family="'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="22" font-weight="bold" fill="#ffffff">
      第三代 Z 系列多维叠合黑板物理拓扑装配与运动学求解主流程
    </text>
    <text y="24" font-family="'Segoe UI', sans-serif" font-size="12" fill="#00d2ff" letter-spacing="1">
      TOPOLOGY ASSEMBLY &amp; KINEMATIC SIMULATION PIPELINE · Z-SERIES MASTER
    </text>
  </g>

  <!-- Flowchart Nodes (Centered vertically) -->
  <!-- Nodes from Y=105 to Y=740, 8 steps -->
  <!-- Box: W=760, H=56, X=120 -->

  <g font-family="'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="13" font-weight="500">
    <!-- Step 1 -->
    <g transform="translate(120, 105)">
      <rect width="760" height="56" rx="8" fill="url(#nodeGrad)" stroke="#00d2ff" stroke-width="1.5" />
      <circle cx="36" cy="28" r="16" fill="#00d2ff" />
      <text x="36" y="33" fill="#0c101d" font-weight="bold" text-anchor="middle">1</text>
      <text x="70" y="28" fill="#ffffff" font-weight="bold">新建独立工程目录体系</text>
      <text x="70" y="46" fill="#8da2c0" font-size="12">05-三维建模与Blender渲染/Z系列/ · 严格执行防覆盖与部件拆解命名规范</text>
    </g>
    <line x1="500" y1="161" x2="500" y2="183" stroke="#00d2ff" stroke-width="2" marker-end="url(#arrow2)" />

    <!-- Step 2 -->
    <g transform="translate(120, 185)">
      <rect width="760" height="56" rx="8" fill="url(#nodeGrad)" stroke="#00d2ff" stroke-width="1.5" />
      <circle cx="36" cy="28" r="16" fill="#00d2ff" />
      <text x="36" y="33" fill="#0c101d" font-weight="bold" text-anchor="middle">2</text>
      <text x="70" y="28" fill="#ffffff" font-weight="bold">构建参数化总装拓扑装配驱动脚本</text>
      <text x="70" y="46" fill="#8da2c0" font-size="12">build_z_series_master.py · 纯数学矩阵装配，零手动错位，可重复参数化生成</text>
    </g>
    <line x1="500" y1="241" x2="500" y2="263" stroke="#00d2ff" stroke-width="2" marker-end="url(#arrow2)" />

    <!-- Step 3 -->
    <g transform="translate(120, 265)">
      <rect width="760" height="56" rx="8" fill="url(#nodeGrad)" stroke="#38ef7d" stroke-width="1.5" />
      <circle cx="36" cy="28" r="16" fill="#38ef7d" />
      <text x="36" y="33" fill="#0c101d" font-weight="bold" text-anchor="middle">3</text>
      <text x="70" y="28" fill="#ffffff" font-weight="bold">建立双层贴合超薄板面系统</text>
      <text x="70" y="46" fill="#8da2c0" font-size="12">内主板 12mm + 外折叠板 12mm + 2mm气隙 = 26mm 超致密空间贴合</text>
    </g>
    <line x1="500" y1="321" x2="500" y2="343" stroke="#38ef7d" stroke-width="2" marker-end="url(#arrow2)" />

    <!-- Step 4 -->
    <g transform="translate(120, 345)">
      <rect width="760" height="56" rx="8" fill="url(#nodeGrad)" stroke="#a29bfe" stroke-width="1.5" />
      <circle cx="36" cy="28" r="16" fill="#a29bfe" />
      <text x="36" y="33" fill="#0c101d" font-weight="bold" text-anchor="middle">4</text>
      <text x="70" y="28" fill="#ffffff" font-weight="bold">装配对角线双铰链正交解耦机构 (Diagonal Topology)</text>
      <text x="70" y="46" fill="#8da2c0" font-size="12">里面的外侧翻转主轴 (X=±2000~3000) + 外面的内侧折叠轴 (X=±1000) 彻底消除运动死点</text>
    </g>
    <line x1="500" y1="401" x2="500" y2="423" stroke="#a29bfe" stroke-width="2" marker-end="url(#arrow2)" />

    <!-- Step 5 -->
    <g transform="translate(120, 425)">
      <rect width="760" height="56" rx="8" fill="url(#nodeGrad)" stroke="#fdcb6e" stroke-width="1.5" />
      <circle cx="36" cy="28" r="16" fill="#fdcb6e" />
      <text x="36" y="33" fill="#0c101d" font-weight="bold" text-anchor="middle">5</text>
      <text x="70" y="28" fill="#ffffff" font-weight="bold">生成双横梁自洁延伸轨、Φ28mm 伸缩套杆与垂直拉杆</text>
      <text x="70" y="46" fill="#8da2c0" font-size="12">倒V排灰孔 + 端面刮尘毛刷 + 门式闭环刚架设计，确保极限展开 6000mm 下沉量 &lt; 1.5mm</text>
    </g>
    <line x1="500" y1="481" x2="500" y2="503" stroke="#fdcb6e" stroke-width="2" marker-end="url(#arrow2)" />

    <!-- Step 6 -->
    <g transform="translate(120, 505)">
      <rect width="760" height="56" rx="8" fill="url(#nodeGrad)" stroke="#ff7675" stroke-width="1.5" />
      <circle cx="36" cy="28" r="16" fill="#ff7675" />
      <text x="36" y="33" fill="#0c101d" font-weight="bold" text-anchor="middle">6</text>
      <text x="70" y="28" fill="#ffffff" font-weight="bold">校准真实工业物理色彩与 PBR 材质参数</text>
      <text x="70" y="46" fill="#8da2c0" font-size="12">大屏蓝天渐变 #5182aa、沉稳深墨绿 #416951、亚光铝合金拉丝 #d0d0d0</text>
    </g>
    <line x1="500" y1="561" x2="500" y2="583" stroke="#ff7675" stroke-width="2" marker-end="url(#arrow2)" />

    <!-- Step 7 -->
    <g transform="translate(120, 585)">
      <rect width="760" height="56" rx="8" fill="url(#nodeGrad)" stroke="#00f2fe" stroke-width="1.5" />
      <circle cx="36" cy="28" r="16" fill="#00f2fe" />
      <text x="36" y="33" fill="#0c101d" font-weight="bold" text-anchor="middle">7</text>
      <text x="70" y="28" fill="#ffffff" font-weight="bold">编写运动学姿态控制器与批量自动化渲染引擎</text>
      <text x="70" y="46" fill="#8da2c0" font-size="12">render_z_series_states.py · 驱动工况一全覆盖、工况二大屏露显、工况三极限避光形态求解</text>
    </g>
    <line x1="500" y1="641" x2="500" y2="663" stroke="#00f2fe" stroke-width="2" marker-end="url(#arrow2)" />

    <!-- Step 8 -->
    <g transform="translate(120, 665)">
      <rect width="760" height="66" rx="8" fill="url(#nodeGrad)" stroke="#2ed573" stroke-width="2" />
      <circle cx="36" cy="33" r="18" fill="#2ed573" />
      <text x="36" y="39" fill="#0c101d" font-weight="bold" font-size="15" text-anchor="middle">✓</text>
      <text x="70" y="30" fill="#2ed573" font-weight="bold">输出三大工况 4K 高保真渲染图集与开发审计记录</text>
      <text x="70" y="52" fill="#8da2c0" font-size="12">交付 Z1~Z5 关键姿态高精成果，记录全流程研发日志，形成严谨参赛实证资产</text>
    </g>
  </g>
</svg>
"""

# -------------------------------------------------------------------------
# 图 3: 端侧 VLM 智能闭环与 Bambu Studio 物理样机制造双轨工程总架构 (Dual-Track Architecture)
# -------------------------------------------------------------------------
svg_3 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 950" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0d17" />
      <stop offset="100%" stop-color="#121724" />
    </linearGradient>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#334155" />
    </linearGradient>
    <marker id="arrow3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#00f2fe" />
    </marker>
    <marker id="arrow-bambu" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#00ae42" />
    </marker>
  </defs>

  <rect width="100%" height="100%" fill="url(#bgGrad3)" />
  <rect x="2" y="2" width="1196" height="946" fill="none" stroke="#222f47" stroke-width="2" rx="12" />

  <!-- Title -->
  <g transform="translate(60, 42)">
    <text font-family="'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="24" font-weight="bold" fill="#ffffff">
      端侧 VLM 智能闭环与 Bambu 物理样机制造双轨工程总架构图
    </text>
    <text y="24" font-family="'Segoe UI', sans-serif" font-size="13" fill="#00f2fe" letter-spacing="1">
      DUAL-TRACK ENGINEERING ARCHITECTURE · EDGE VLM DIGITAL TWIN &amp; BAMBU 3D FABRICATION
    </text>
  </g>

  <!-- Top Hub: Core Decision Layer -->
  <g transform="translate(150, 95)">
    <rect width="900" height="70" rx="10" fill="#152136" stroke="#00f2fe" stroke-width="2" />
    <text x="450" y="32" font-family="'PingFang SC', sans-serif" font-size="16" font-weight="bold" fill="#00f2fe" text-anchor="middle">
      【前置核心】端侧视觉语言大模型 (Edge VLM) 动态多任务中枢 (Intel Ultra 9)
    </text>
    <text x="450" y="54" font-family="'PingFang SC', sans-serif" font-size="12" fill="#94a3b8" text-anchor="middle">
      实时多相机视频流采集 (OpenCV) · 人类自然语言动态指令解构 · 多 Agent 协同仲裁调度
    </text>
  </g>
  <line x1="600" y1="165" x2="600" y2="198" stroke="#00f2fe" stroke-width="2.5" marker-end="url(#arrow3)" />

  <!-- Center Hub: 3D Master Assembly -->
  <g transform="translate(200, 200)">
    <rect width="800" height="66" rx="10" fill="#1e293b" stroke="#38bdf8" stroke-width="2" />
    <text x="400" y="30" font-family="'PingFang SC', sans-serif" font-size="15" font-weight="bold" fill="#ffffff" text-anchor="middle">
      【三维机械母本】Blender 5.0 高精度机构学绑定与动力学装配体
    </text>
    <text x="400" y="50" font-family="'PingFang SC', sans-serif" font-size="12" fill="#38bdf8" text-anchor="middle">
      对角线双铰链正交解耦 · 双横梁伸缩套杆 · 48 席现代人体工学教室光环境
    </text>
  </g>

  <!-- Split Lines to Two Subgraphs -->
  <!-- Left Split to X=310, Y=330 -->
  <path d="M 400 266 L 400 300 L 310 300 L 310 330" fill="none" stroke="#00d2ff" stroke-width="2.5" marker-end="url(#arrow3)" />
  <!-- Right Split to X=890, Y=330 -->
  <path d="M 800 266 L 800 300 L 890 300 L 890 330" fill="none" stroke="#00ae42" stroke-width="2.5" marker-end="url(#arrow-bambu)" />

  <!-- Subgraph 1: Left (VLM Digital Twin Track) -->
  <g transform="translate(50, 335)">
    <rect width="520" height="570" rx="12" fill="#0f172a" stroke="#00d2ff" stroke-width="1.5" stroke-dasharray="4 4" />
    <rect x="0" y="0" width="520" height="36" rx="12" fill="#1e293b" />
    <text x="260" y="23" font-family="'PingFang SC', sans-serif" font-size="14" font-weight="bold" fill="#00f2fe" text-anchor="middle">
      分支一：VLM 数字孪生活体闭环 (Digital Twin Track)
    </text>

    <!-- Node L1: Perception Input -->
    <g transform="translate(30, 60)">
      <rect width="460" height="75" rx="8" fill="#1a2538" stroke="#38bdf8" stroke-width="1" />
      <text x="20" y="28" font-family="'PingFang SC', sans-serif" font-size="13" font-weight="bold" fill="#ffffff">1. 视觉感知输入层 (Perception Input)</text>
      <text x="20" y="48" font-family="'PingFang SC', sans-serif" font-size="11" fill="#94a3b8">摄像头 0 (内置 Webcam) / 1 (外接高清 USB) / 2 (运动相机 UVC) / Sim</text>
      <text x="20" y="65" font-family="'PingFang SC', sans-serif" font-size="11" fill="#38bdf8">毫秒级特征提取：眼裂长宽比 EAR 计算 + 高光强过曝光斑面积轮廓判定</text>
    </g>
    <line x1="260" y1="135" x2="260" y2="160" stroke="#00d2ff" stroke-width="2" marker-end="url(#arrow3)" />

    <!-- Node L2: VLM Core Reasoning -->
    <g transform="translate(30, 162)">
      <rect width="460" height="85" rx="8" fill="#1a2538" stroke="#00f2fe" stroke-width="1" />
      <text x="20" y="28" font-family="'PingFang SC', sans-serif" font-size="13" font-weight="bold" fill="#00f2fe">2. 端侧轻量 VLM 认知推理中枢 (Cognitive Engine)</text>
      <text x="20" y="48" font-family="'PingFang SC', sans-serif" font-size="11" fill="#ffffff">端侧 Qwen2.5-VL-3B / OpenVINO / OpenCV 混合推理</text>
      <text x="20" y="65" font-family="'PingFang SC', sans-serif" font-size="11" fill="#94a3b8">动态多任务响应：眼部用眼疲劳 · 黑板眩光直射 · 百叶窗拉下 · 洗墙灯补光</text>
      <text x="20" y="78" font-family="'PingFang SC', sans-serif" font-size="11" fill="#e2e8f0">人类意图对齐：严格执行自然语言 Prompt 设定的避光策略约束</text>
    </g>
    <line x1="260" y1="247" x2="260" y2="272" stroke="#00d2ff" stroke-width="2" marker-end="url(#arrow3)" />

    <!-- Node L3: Multi-Objective Arbitration -->
    <g transform="translate(30, 274)">
      <rect width="460" height="75" rx="8" fill="#1a2538" stroke="#a78bfa" stroke-width="1" />
      <text x="20" y="28" font-family="'PingFang SC', sans-serif" font-size="13" font-weight="bold" fill="#a78bfa">3. 多目标博弈仲裁与 Agent 工具调用 (Tool Calling)</text>
      <text x="20" y="48" font-family="'PingFang SC', sans-serif" font-size="11" fill="#ffffff">>>> TOOL CALL: api_adjust_blackboard(yaw=18.0 deg)</text>
      <text x="20" y="65" font-family="'PingFang SC', sans-serif" font-size="11" fill="#a78bfa">>>> TOOL CALL: api_set_smart_blinds(65%) | api_set_light(220W)</text>
    </g>
    <line x1="260" y1="349" x2="260" y2="374" stroke="#00d2ff" stroke-width="2" marker-end="url(#arrow3)" />

    <!-- Node L4: Blender Live Actuation -->
    <g transform="translate(30, 376)">
      <rect width="460" height="85" rx="8" fill="#1a2538" stroke="#22c55e" stroke-width="1.5" />
      <text x="20" y="28" font-family="'PingFang SC', sans-serif" font-size="13" font-weight="bold" fill="#22c55e">4. Blender 60 FPS 物理活体驱动 (Viewport Driver)</text>
      <text x="20" y="48" font-family="'PingFang SC', sans-serif" font-size="11" fill="#ffffff">IPC 共享状态文件 live_control_state.json 毫秒级轮询</text>
      <text x="20" y="65" font-family="'PingFang SC', sans-serif" font-size="11" fill="#94a3b8">S 曲线平滑动力学阻尼：活动黑板转动 18° + 红光切除 + 绿光射向天花板</text>
      <text x="20" y="78" font-family="'PingFang SC', sans-serif" font-size="11" fill="#22c55e">3D 视口 tag_redraw() 强制重绘，实现双手脱机 60 FPS 游戏级伪 VR 联动！</text>
    </g>
    <line x1="260" y1="461" x2="260" y2="486" stroke="#00d2ff" stroke-width="2" marker-end="url(#arrow3)" />

    <!-- Output L5 -->
    <g transform="translate(30, 488)">
      <rect width="460" height="55" rx="8" fill="#064e3b" stroke="#10b981" stroke-width="1.5" />
      <text x="230" y="25" font-family="'PingFang SC', sans-serif" font-size="13" font-weight="bold" fill="#34d399" text-anchor="middle">
        【交付物】全国创新大赛赛场“伪 VR”真机活体互动演示系统
      </text>
      <text x="230" y="44" font-family="'PingFang SC', sans-serif" font-size="11" fill="#a7f3d0" text-anchor="middle">
        1280x720 决策 HUD 终端 + 实时三维视口客观测控，彻底终结静态 PPT 答辩
      </text>
    </g>
  </g>

  <!-- Subgraph 2: Right (Bambu 3D Fabrication Track) -->
  <g transform="translate(630, 335)">
    <rect width="520" height="570" rx="12" fill="#0f172a" stroke="#00ae42" stroke-width="1.5" stroke-dasharray="4 4" />
    <rect x="0" y="0" width="520" height="36" rx="12" fill="#1b3a24" />
    <text x="260" y="23" font-family="'PingFang SC', sans-serif" font-size="14" font-weight="bold" fill="#00ae42" text-anchor="middle">
      分支二：Bambu Studio 物理样机制造链路 (Fabrication Track)
    </text>

    <!-- Node R1: Geometric Scaling -->
    <g transform="translate(30, 60)">
      <rect width="460" height="75" rx="8" fill="#16291c" stroke="#22c55e" stroke-width="1" />
      <text x="20" y="28" font-family="'PingFang SC', sans-serif" font-size="13" font-weight="bold" fill="#ffffff">1. 1:10 物理缩比与构件空间拆解 (Decomposition)</text>
      <text x="20" y="48" font-family="'PingFang SC', sans-serif" font-size="11" fill="#86efac">总跨度 6000mm 原型等比缩放至 600mm 桌面级演示样机</text>
      <text x="20" y="65" font-family="'PingFang SC', sans-serif" font-size="11" fill="#94a3b8">结构拆解：外框架/滑槽导轨/滑动滚轮/铰链销轴/双层板面/舵机舱</text>
    </g>
    <line x1="260" y1="135" x2="260" y2="160" stroke="#00ae42" stroke-width="2" marker-end="url(#arrow-bambu)" />

    <!-- Node R2: Tolerance Optimization -->
    <g transform="translate(30, 162)">
      <rect width="460" height="85" rx="8" fill="#16291c" stroke="#4ade80" stroke-width="1" />
      <text x="20" y="28" font-family="'PingFang SC', sans-serif" font-size="13" font-weight="bold" fill="#4ade80">2. FDM 制造公差与装配补偿 (Tolerance Optimization)</text>
      <text x="20" y="48" font-family="'PingFang SC', sans-serif" font-size="11" fill="#ffffff">运动副装配间隙精调为 0.20mm ~ 0.25mm，避免热胀冷缩卡滞</text>
      <text x="20" y="65" font-family="'PingFang SC', sans-serif" font-size="11" fill="#94a3b8">榫卯定位销 + M3 沉头内六角不锈钢螺栓预埋孔定位</text>
      <text x="20" y="78" font-family="'PingFang SC', sans-serif" font-size="11" fill="#86efac">关键受力受剪构件采用 45° 打印走向以最大化层间剪切强度</text>
    </g>
    <line x1="260" y1="247" x2="260" y2="272" stroke="#00ae42" stroke-width="2" marker-end="url(#arrow-bambu)" />

    <!-- Node R3: Bambu 3MF Multi-plate -->
    <g transform="translate(30, 274)">
      <rect width="460" height="75" rx="8" fill="#16291c" stroke="#22c55e" stroke-width="1" />
      <text x="20" y="28" font-family="'PingFang SC', sans-serif" font-size="13" font-weight="bold" fill="#86efac">3. 拓竹多色多盘工程生成 (Bambu 3MF Pipeline)</text>
      <text x="20" y="48" font-family="'PingFang SC', sans-serif" font-size="11" fill="#ffffff">盘 1: 哑光碳灰框架 | 盘 2: 深墨绿亚光板面 | 盘 3: 机械亮橙铰链</text>
      <text x="20" y="65" font-family="'PingFang SC', sans-serif" font-size="11" fill="#94a3b8">自动化 Python 批处理导出 STL 与 Bambu Studio 3MF 工程</text>
    </g>
    <line x1="260" y1="349" x2="260" y2="374" stroke="#00ae42" stroke-width="2" marker-end="url(#arrow-bambu)" />

    <!-- Node R4: Micro Servo Hardware Sync -->
    <g transform="translate(30, 376)">
      <rect width="460" height="85" rx="8" fill="#16291c" stroke="#10b981" stroke-width="1.5" />
      <text x="20" y="28" font-family="'PingFang SC', sans-serif" font-size="13" font-weight="bold" fill="#34d399">4. 物理电机执行器与嵌入式驱动 (Hardware Actuation)</text>
      <text x="20" y="48" font-family="'PingFang SC', sans-serif" font-size="11" fill="#ffffff">微型总线金属齿轮舵机 / 步进电机挂载在铰链转轴原点</text>
      <text x="20" y="65" font-family="'PingFang SC', sans-serif" font-size="11" fill="#94a3b8">ESP32 / 串口通信与上位机 IPC 接收相同 target_yaw 角度指令</text>
      <text x="20" y="78" font-family="'PingFang SC', sans-serif" font-size="11" fill="#86efac">实现三维屏幕视口与现实物理桌面样机 1:1 同步旋转避光！</text>
    </g>
    <line x1="260" y1="461" x2="260" y2="486" stroke="#00ae42" stroke-width="2" marker-end="url(#arrow-bambu)" />

    <!-- Output R5 -->
    <g transform="translate(30, 488)">
      <rect width="460" height="55" rx="8" fill="#064e3b" stroke="#10b981" stroke-width="1.5" />
      <text x="230" y="25" font-family="'PingFang SC', sans-serif" font-size="13" font-weight="bold" fill="#34d399" text-anchor="middle">
        【交付物】全国创新大赛问辩现场高精度实体可动样机模型
      </text>
      <text x="230" y="44" font-family="'PingFang SC', sans-serif" font-size="11" fill="#a7f3d0" text-anchor="middle">
        评委可亲手拨动检验机构自锁、自洁排灰与对角线铰链零干涉
      </text>
    </g>
  </g>
</svg>
"""

# -------------------------------------------------------------------------
# 图 4: GH-VI-2026 伪 VR 沉浸式真机活体交互数字孪生系统全链路闭环图
# -------------------------------------------------------------------------
svg_4 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad4" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0e1a" />
      <stop offset="100%" stop-color="#141a29" />
    </linearGradient>
    <linearGradient id="cyberBlue" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f2fe" />
      <stop offset="100%" stop-color="#4facfe" />
    </linearGradient>
    <marker id="arrow4" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#00f2fe" />
    </marker>
  </defs>

  <rect width="100%" height="100%" fill="url(#bgGrad4)" />
  <rect x="2" y="2" width="1196" height="796" fill="none" stroke="#23334d" stroke-width="2" rx="12" />

  <!-- Title -->
  <g transform="translate(60, 45)">
    <text font-family="'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="24" font-weight="bold" fill="#ffffff">
      GH-VI-2026 伪 VR 沉浸式真机活体交互数字孪生系统全链路闭环
    </text>
    <text y="24" font-family="'Segoe UI', sans-serif" font-size="13" fill="#00f2fe" letter-spacing="1">
      FULL CLOSED-LOOP PIPELINE · LIVE SENSING &lt;--&gt; AGENT REASONING &lt;--&gt; 60FPS BLENDER VIEWPORT
    </text>
  </g>

  <!-- 4 Main Stages in Circular / Pipeline Form -->
  <!-- Box: W=240, H=320 -->

  <!-- Card 1: 物理感知采集 -->
  <g transform="translate(60, 110)">
    <rect width="250" height="420" rx="10" fill="#131d2e" stroke="#38bdf8" stroke-width="1.5" />
    <rect x="0" y="0" width="250" height="40" rx="10" fill="#1e293b" />
    <text x="125" y="25" font-family="'PingFang SC', sans-serif" font-size="14" font-weight="bold" fill="#38bdf8" text-anchor="middle">
      ① 视觉多相机采集
    </text>
    <g transform="translate(20, 60)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#94a3b8">
      <text y="0" font-weight="bold" fill="#ffffff">硬件捕获源：</text>
      <text y="20">• 笔记本自带 Webcam</text>
      <text y="38">• USB 高清广角相机</text>
      <text y="56">• 运动相机 (Action Cam UVC)</text>
      <text y="74">• 数字孪生仿真流 (sim)</text>

      <text y="115" font-weight="bold" fill="#ffffff">几何形态学特征提取：</text>
      <text y="135">• 面部主视区自适应定位</text>
      <text y="153">• 眼裂开合比 EAR 计算</text>
      <text y="171">  正常睁眼: EAR ≈ 0.38</text>
      <text y="189" fill="#ff7675">  眯眼应激: EAR &lt; 0.20</text>
      <text y="215">• 强光直射过曝检测</text>
      <text y="233">  手机手电筒斑 &gt; 1500px</text>

      <rect x="-5" y="270" width="220" height="65" rx="6" fill="#0c1726" stroke="#38bdf8" stroke-width="1" />
      <text x="5" y="290" fill="#00f2fe" font-size="11" font-weight="bold">单帧计算延迟: &lt; 2.5ms</text>
      <text x="5" y="308" fill="#64748b" font-size="11">极轻量纯数学几何运算</text>
      <text x="5" y="324" fill="#64748b" font-size="11">显存占用: 0MB · CPU &lt; 3%</text>
    </g>
  </g>
  <line x1="310" y1="320" x2="350" y2="320" stroke="#00f2fe" stroke-width="2.5" marker-end="url(#arrow4)" />

  <!-- Card 2: VLM Agent 认知决策 -->
  <g transform="translate(350, 110)">
    <rect width="250" height="420" rx="10" fill="#131d2e" stroke="#00f2fe" stroke-width="1.5" />
    <rect x="0" y="0" width="250" height="40" rx="10" fill="#1e293b" />
    <text x="125" y="25" font-family="'PingFang SC', sans-serif" font-size="14" font-weight="bold" fill="#00f2fe" text-anchor="middle">
      ② 智能决策与工具调用
    </text>
    <g transform="translate(20, 60)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#94a3b8">
      <text y="0" font-weight="bold" fill="#ffffff">自然语言指令注入：</text>
      <text y="20" fill="#38ef7d">“若靠窗学生眯眼或黑板强</text>
      <text y="38" fill="#38ef7d">反光，自动偏航18度避光，</text>
      <text y="56" fill="#38ef7d">降百叶窗65%，洗墙灯220W”</text>

      <text y="100" font-weight="bold" fill="#ffffff">Agent 动态工具分发链：</text>
      <text y="122" fill="#e2e8f0">>>> api_adjust_blackboard</text>
      <text y="138" fill="#00f2fe">    yaw = +18.0 deg</text>
      <text y="158" fill="#e2e8f0">>>> api_set_smart_blinds</text>
      <text y="174" fill="#00f2fe">    level = 65%</text>
      <text y="194" fill="#e2e8f0">>>> api_set_wash_light</text>
      <text y="210" fill="#00f2fe">    power = 220W</text>

      <rect x="-5" y="270" width="220" height="65" rx="6" fill="#0c1726" stroke="#00f2fe" stroke-width="1" />
      <text x="5" y="290" fill="#00f2fe" font-size="11" font-weight="bold">决策透明度: 100% 回显</text>
      <text x="5" y="308" fill="#64748b" font-size="11">调了什么 / 调了多少度</text>
      <text x="5" y="324" fill="#64748b" font-size="11">怎样识别 / 为什么调节</text>
    </g>
  </g>
  <line x1="600" y1="320" x2="640" y2="320" stroke="#00f2fe" stroke-width="2.5" marker-end="url(#arrow4)" />

  <!-- Card 3: IPC 共享状态纽带 -->
  <g transform="translate(640, 110)">
    <rect width="210" height="420" rx="10" fill="#131d2e" stroke="#a78bfa" stroke-width="1.5" />
    <rect x="0" y="0" width="210" height="40" rx="10" fill="#1e293b" />
    <text x="105" y="25" font-family="'PingFang SC', sans-serif" font-size="14" font-weight="bold" fill="#a78bfa" text-anchor="middle">
      ③ IPC 毫秒级状态总线
    </text>
    <g transform="translate(15, 60)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#94a3b8">
      <text y="0" font-weight="bold" fill="#ffffff">共享状态载体：</text>
      <text y="20" fill="#a78bfa">live_control_state.json</text>

      <text y="60" font-weight="bold" fill="#ffffff">工业级进程解耦：</text>
      <text y="80">• 进程 A (Python 感知端)</text>
      <text y="98">• 进程 B (Blender 渲染端)</text>
      <text y="116">• 双向无阻塞读写</text>
      <text y="134">• 文件 mtime 变更探测</text>

      <rect x="-5" y="170" width="190" height="165" rx="6" fill="#0c1726" stroke="#a78bfa" stroke-width="1" />
      <text x="5" y="190" fill="#c4b5fd" font-size="10" font-family="monospace">{</text>
      <text x="15" y="208" fill="#c4b5fd" font-size="10" font-family="monospace">"is_squinting": true,</text>
      <text x="15" y="226" fill="#c4b5fd" font-size="10" font-family="monospace">"target_yaw": 18.0,</text>
      <text x="15" y="244" fill="#c4b5fd" font-size="10" font-family="monospace">"blinds_pct": 65.0,</text>
      <text x="15" y="262" fill="#c4b5fd" font-size="10" font-family="monospace">"light_w": 220.0,</text>
      <text x="15" y="280" fill="#c4b5fd" font-size="10" font-family="monospace">"reason": "避光偏转"</text>
      <text x="5" y="298" fill="#c4b5fd" font-size="10" font-family="monospace">}</text>
      <text x="5" y="322" fill="#22c55e" font-size="10" font-weight="bold">IPC 通信抖动: &lt; 0.8ms</text>
    </g>
  </g>
  <line x1="850" y1="320" x2="890" y2="320" stroke="#00f2fe" stroke-width="2.5" marker-end="url(#arrow4)" />

  <!-- Card 4: Blender 60 FPS 物理驱动 -->
  <g transform="translate(890, 110)">
    <rect width="250" height="420" rx="10" fill="#131d2e" stroke="#22c55e" stroke-width="1.5" />
    <rect x="0" y="0" width="250" height="40" rx="10" fill="#1e293b" />
    <text x="125" y="25" font-family="'PingFang SC', sans-serif" font-size="14" font-weight="bold" fill="#22c55e" text-anchor="middle">
      ④ 3D 视口伪 VR 联动
    </text>
    <g transform="translate(20, 60)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#94a3b8">
      <text y="0" font-weight="bold" fill="#ffffff">真实机构物理偏航：</text>
      <text y="20" fill="#4ade80">• Ctrl_Flip_Left 铰链转动</text>
      <text y="38">  带动整套黑板系统转 18°</text>
      <text y="56">• S 曲线平滑步进电机阻尼</text>

      <text y="95" font-weight="bold" fill="#ffffff">光学射线与光环境：</text>
      <text y="115" fill="#f87171">• 危险直射红光瞬间切除</text>
      <text y="133" fill="#4ade80">• 安全绿光射向吸光天花板</text>
      <text y="151">• 侧窗丁达尔强光减弱 64%</text>

      <text y="185" font-weight="bold" fill="#ffffff">前墙 3D 浮动发光 HUD：</text>
      <text y="205" fill="#38bdf8">• 实时刷新文字状态看板</text>
      <text y="223">• tag_redraw() 强制重绘</text>
      <text y="241" fill="#22c55e">  双手脱机 60 FPS 丝滑运行</text>

      <rect x="-5" y="270" width="220" height="65" rx="6" fill="#0c1726" stroke="#22c55e" stroke-width="1" />
      <text x="5" y="290" fill="#22c55e" font-size="11" font-weight="bold">渲染引擎: Blender 5.0</text>
      <text x="5" y="308" fill="#64748b" font-size="11">视口刷新率: 60 FPS</text>
      <text x="5" y="324" fill="#64748b" font-size="11">零插件依赖 · 原生 API 驱动</text>
    </g>
  </g>

  <!-- Bottom Evaluation Banner -->
  <g transform="translate(60, 560)">
    <rect width="1080" height="190" rx="10" fill="#111827" stroke="#374151" stroke-width="1.5" />
    <text x="30" y="35" font-family="'PingFang SC', sans-serif" font-size="16" font-weight="bold" fill="#facc15">
      ★ 全国青少年科技创新大赛 (CASTIC) 赛场真实客观演示评价优势
    </text>
    
    <g transform="translate(30, 65)" font-family="'PingFang SC', sans-serif" font-size="12" fill="#cbd5e1">
      <rect x="0" y="0" width="320" height="95" rx="6" fill="#1f2937" stroke="#4b5563" stroke-width="1" />
      <text x="15" y="25" font-weight="bold" fill="#38bdf8">【真实人机交互 · 拒绝录屏】</text>
      <text x="15" y="48">评委走到电脑前对准摄像头，眯眼或拿</text>
      <text x="15" y="68">手电筒照光，屏幕里的 3D 黑板当场动，</text>
      <text x="15" y="88">具有如临其境的“伪 VR”活体科技感！</text>

      <rect x="350" y="0" width="320" height="95" rx="6" fill="#1f2937" stroke="#4b5563" stroke-width="1" />
      <text x="15" y="25" font-weight="bold" fill="#a78bfa">【AI 决策透明 · 拒绝黑盒】</text>
      <text x="15" y="48">屏幕 HUD 透明化回显识别指标(EAR)、</text>
      <text x="15" y="68">调节部件、调节角度与天花板吸光机理，</text>
      <text x="15" y="88">体现极高的科学探究深度与工科严谨性！</text>

      <rect x="700" y="0" width="320" height="95" rx="6" fill="#1f2937" stroke="#4b5563" stroke-width="1" />
      <text x="15" y="25" font-weight="bold" fill="#34d399">【全班 48 席安全 · 拒绝一刀切】</text>
      <text x="15" y="48">基于真实 8 列 × 6 行空间测算，反射光</text>
      <text x="15" y="68">抬升至 Z=2.8m 高空吸光层，绝不误伤</text>
      <text x="15" y="88">中间和对侧学生，IMAX 视角由 28° 拓至 44.5°！</text>
    </g>
  </g>
</svg>
"""

# 写入文件
svg_files = {
    "01_vi_series_kinematic_sequence.svg": svg_1,
    "02_z_series_assembly_pipeline.svg": svg_2,
    "03_vlm_bambu_dual_track_architecture.svg": svg_3,
    "04_gh_vi_live_digital_twin_closed_loop.svg": svg_4
}

for name, content in svg_files.items():
    path = os.path.join(SVG_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"[OK] Generated SVG: {path} ({len(content)} bytes)")

print("\n[SUCCESS] 全部 Plan 核心流程图与架构图已成功导出为独立矢量 SVG！")
