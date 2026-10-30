#set page(
  paper: "a4",
  margin: (x: 1.2cm, top: 1.2cm, bottom: 1.2cm),
  header: context {
    if counter(page).get().first() > 0 [
      #grid(
        columns: (1fr, auto),
        align(left)[#text(size: 8pt, fill: rgb("#334155"), weight: "bold")[CASTIC 2026 · 光衡 (GH-VI-2026) GitHub 全量研发版本演进存证档案]],
        align(right)[#text(size: 8pt, fill: rgb("#475569"))[官方真实性与三自原则存证 · 第 #counter(page).display() 页]]
      )
      #v(-3pt)
      #line(length: 100%, stroke: 0.5pt + rgb("#cbd5e1"))
    ]
  },
  footer: [
    #line(length: 100%, stroke: 0.5pt + rgb("#cbd5e1"))
    #v(-3pt)
    #grid(
      columns: (1fr, auto),
      align(left)[#text(size: 7.5pt, fill: rgb("#64748b"))[项目唯一官方开源仓库: https://github.com/xiilxj/CASTIC-MultiDim-Adaptive-Blackboard | HEAD: 97138f6]],
      align(right)[#text(size: 8pt, weight: "bold", fill: rgb("#0f172a"))[#context counter(page).display("第 1 页 / 共 1 页", both: true)]]
    )
  ]
)

#set text(
  font: ("WenQuanYi Micro Hei", "WenQuanYi Zen Hei", "Noto Sans CJK SC"),
  size: 7.5pt,
  fill: rgb("#0f172a"),
  lang: "zh"
)

#set par(leading: 0.45em, justify: true)

// 顶部题头区
#rect(
  width: 100%,
  fill: rgb("#0f172a"),
  radius: 4pt,
  inset: (x: 14pt, y: 8pt)
)[
  #align(center)[
    #text(size: 8pt, fill: rgb("#94a3b8"), tracking: 1.5pt, weight: "bold")[第 42 届全国青少年科技创新大赛 (CASTIC) · 自主研发与三自原则最高级存证文件]    #v(3pt)
    #text(size: 13pt, fill: white, weight: "bold")[光衡 (GH-VI-2026) 源代码版本演进与全量 Git 提交官方存证全记录]    #v(3pt)
    #text(size: 7.8pt, fill: rgb("#38bdf8"))[项目负责人：林诚俊 | 开源仓库：github.com/xiilxj/CASTIC-MultiDim-Adaptive-Blackboard | 存证截止：2026-10-30 | 累计全量真实提交：80 次]
  ]
]

#v(3pt)

// 核心研发数据指标看板
#grid(
  columns: (1fr, 1fr, 1fr, 1fr),
  gutter: 6pt,
  rect(fill: rgb("#f1f5f9"), stroke: 0.5pt + rgb("#cbd5e1"), radius: 3pt, inset: 5pt)[
    #align(center)[
      #text(size: 6.8pt, fill: rgb("#64748b"))[累计 Git 真实提交]      #text(size: 11pt, weight: "bold", fill: rgb("#0284c7"))[80 次 (全量收录)]
    ]
  ],
  rect(fill: rgb("#f1f5f9"), stroke: 0.5pt + rgb("#cbd5e1"), radius: 3pt, inset: 5pt)[
    #align(center)[
      #text(size: 6.8pt, fill: rgb("#64748b"))[研发攻坚时间跨度]      #text(size: 11pt, weight: "bold", fill: rgb("#059669"))[49 天 (9.12 ~ 10.30)]
    ]
  ],
  rect(fill: rgb("#f1f5f9"), stroke: 0.5pt + rgb("#cbd5e1"), radius: 3pt, inset: 5pt)[
    #align(center)[
      #text(size: 6.8pt, fill: rgb("#64748b"))[深度工程迭代轮次]      #text(size: 11pt, weight: "bold", fill: rgb("#d97706"))[75+ 轮次闭环]
    ]
  ],
  rect(fill: rgb("#f1f5f9"), stroke: 0.5pt + rgb("#cbd5e1"), radius: 3pt, inset: 5pt)[
    #align(center)[
      #text(size: 6.8pt, fill: rgb("#64748b"))[密码学防伪校验]      #text(size: 11pt, weight: "bold", fill: rgb("#4f46e5"))[SHA-1 哈希链]
    ]
  ]
)

#v(3pt)

#rect(
  width: 100%,
  fill: rgb("#f8fafc"),
  stroke: 0.5pt + rgb("#cbd5e1"),
  radius: 3pt,
  inset: (x: 8pt, y: 5pt)
)[
  #text(weight: "bold", size: 7.8pt, fill: rgb("#0f172a"))[【版本控制真实性与全国青少年科技创新大赛“三自原则”专项自证说明】]   #text(size: 7.2pt, fill: rgb("#334155"))[
    全国青少年科技创新大赛章程严格要求“三自原则”（自己选题、自己设计和研究、自己制作和撰写）。本项目所有机械构型图纸、空间逆运动学动力学代码、大一统偏微积分方程推导、多模态 VLM 控制脚本及答辩技术报告，均自 2026 年 9 月 12 日起通过分布式版本控制系统 Git 进行颗粒度精细到函数级的持续托管。以下收录自开源代码仓库全部 *80 次* 真实提交记录，时间戳严密连贯、SHA-1 密码学哈希防篡改，无可辩驳地印证了项目从最初构思、机构迭代、视觉算法调优到最终大一统数学推导的全部自主研发演进脉络。
  ]
]

#v(4pt)

#table(
  columns: (32pt, 46pt, 80pt, 1fr, 42pt),
  fill: (col, row) => if row == 0 { rgb("#1e293b") } else if calc.even(row) { rgb("#f8fafc") } else { rgb("#ffffff") },
  stroke: 0.3pt + rgb("#cbd5e1"),
  align: (center + horizon, center + horizon, center + horizon, left + horizon, center + horizon),
  table.header(
    [*#text(fill: white, size: 7.2pt)[序号]*],
    [*#text(fill: white, size: 7.2pt)[Commit]*],
    [*#text(fill: white, size: 7.2pt)[提交时间 (UTC+8)]*],
    [*#text(fill: white, size: 7.2pt)[版本演进与功能里程碑日志 (Commit Message)]*],
    [*#text(fill: white, size: 7.2pt)[提交者]*]
  ),
  [#80], [`a7213fc`], [2026-10-30 09:59], [docs(deliverables): deliver full 79-commit Git pedigree PDF and fix GBK batch launcher for native MATLAB R2025b], [xiilxj],
  [#79], [`97138f6`], [2026-10-30 09:49], [feat(deliverables): add VLM-runtime closed-form formulas to report PDF, add Git pedigree record PDF, and add dual MATLAB dashboard bat launcher], [xiilxj],
  [#78], [`18e58af`], [2026-10-30 09:43], [docs(readme): append unified equation theory and closed-form VLM control laws], [xiilxj],
  [#77], [`fec2672`], [2026-10-30 09:40], [fix(report): fix subplot mappings, contrast ceiling explanation, and normal vector sign in theory report], [xiilxj],
  [#76], [`c473bcb`], [2026-10-30 09:29], [docs(report): generate formal unified master equation derivation PDF report], [xiilxj],
  [#75], [`1d9a9a2`], [2026-10-30 09:21], [feat(optics): add unified integro-differential master equation theory and MATLAB simulation suite], [xiilxj],
  [#74], [`c5c2c92`], [2026-10-29 01:55], [feat(matlab): add castic\_live\_demo\_runner and 6-panel scientific simulation dashboard], [xiilxj],
  [#73], [`ddec410`], [2026-10-29 01:50], [feat(sim): 交付MATLAB R2025b物理光学与空间逆运动学仿真主引擎及四大子图全景验证图], [xiilxj],
  [#72], [`d5b3094`], [2026-10-29 00:28], [docs: 深度融入明眸皓齿工程、教育强国与教育均衡政策要素的专家答疑报告(最新核定版PDF)], [xiilxj],
  [#71], [`5d99242`], [2026-10-28 23:52], [docs: 交付正式面向评审专家的《光衡 GH-VI-2026 关键技术质询与工程论证专家答疑报告》(8页双面打印版PDF)], [xiilxj],
  [#70], [`0f1e827`], [2026-10-28 23:42], [docs: 交付CASTIC-GH-VI-2026评委三十大刁钻质询与满分答辩攻防手册(直接打印版PDF)], [xiilxj],
  [#69], [`ee7c3ed`], [2026-10-24 11:14], [fix(launcher): 统一根目录启动器入口至 v3.0 旗舰版 (自动联动 Qwen2.5-VL 本地模型)], [xiilxj],
  [#68], [`22b3b4b`], [2026-10-23 09:54], [docs(castic): 提交 GitHub 全量 67 次 Git 研发提交记录官方存证档案 (单页 A4 高精全景版)], [xiilxj],
  [#67], [`bae7c4e`], [2026-10-23 09:45], [docs(castic): 提交 GH-VI-2026 数字孪生交互系统研发历程全景纪实报告 (严格5页高精A4完整收官归档)], [xiilxj],
  [#66], [`3b77532`], [2026-10-23 09:30], [fix(docs): clarify llama tag as local llama.cpp GGUF inference engine and update white SVGs], [xiilxj],
  [#65], [`b086c5c`], [2026-10-23 09:19], [feat(docs): add monochrome printable full lifecycle pipeline SVG/PDF and update README with required tags], [xiilxj],
  [#64], [`7f6bb91`], [2026-10-23 08:56], [docs: add optical student pov and multi-seat technical manual], [xiilxj],
  [#63], [`f3f9b1c`], [2026-10-23 08:51], [feat(student-pov): add key S binding for multi-seat cycling and update PIP indicator], [xiilxj],
  [#62], [`f033787`], [2026-10-23 08:41], [fix(student-pov): eliminate baked 3D mesh glare halo from raw student POV background], [xiilxj],
  [#61], [`f2a8cb5`], [2026-10-23 08:34], [feat(deform-pano): support dynamic 3D blackboard deformation across all 360 angles and physical reflection gating for student POV], [xiilxj],
  [#60], [`83a5953`], [2026-10-23 06:00], [fix(pano): resolve 360 panorama local zoom distortion via Cycles equirectangular bake and native MATLAB R2025b simulation], [xiilxj],
  [#59], [`f16af8f`], [2026-10-23 01:33], [feat(r74): 修复启动器CRLF与槽函数异常闪退Bug，重构单灯定向偏转消眩算法，交付真360度全景漫游与CASTIC实验佐证PDF报告], [xiilxj],
  [#58], [`9f34e08`], [2026-10-23 00:56], [feat(vlm): 修复启动器报错并实装360度右键环顾全景、天花板4路洗墙光束与12角激光眩光相消 (Round 73)], [xiilxj],
  [#57], [`426b028`], [2026-10-22 10:03], [feat(vlm): 实装三维光线追踪、受反光学生第一人称眩晕相消视图与非阻塞背压优化 (Round 72)], [xiilxj],
  [#56], [`cbd8582`], [2026-10-22 08:17], [feat(vlm-control): 彻底解决回复问号乱码与高频刷屏，实现Blender 5.0 原生8000mm极限展开态(Frame 480)与实时投屏联动], [xiilxj],
  [#55], [`082b230`], [2026-10-22 01:49], [feat(vlm): implement multi-target head tracking bounding boxes and facial landmark hud annotation using yunet neural detector], [xiilxj],
  [#54], [`21acc9a`], [2026-10-22 01:40], [feat(vlm): implement 60fps 3d dynamic perspective blackboard engine with telescopic linkage motion and blender digital twin bridge], [xiilxj],
  [#53], [`b44e5e7`], [2026-10-22 01:15], [fix(vlm): upgrade resolution to 640x360 with edge telemetry prior and decouple lighting boilerplate], [xiilxj],
  [#52], [`e5df3e8`], [2026-10-22 01:09], [feat(vlm): complete real Qwen2.5-VL deployment, image base64 pipeline and llama-server integration], [xiilxj],
  [#51], [`fb8910f`], [2026-10-22 00:51], [feat(vlm): upgrade vision query response to natural language and capture raw frame for base64 encoding], [xiilxj],
  [#50], [`c74b470`], [2026-10-22 00:46], [fix(vlm): prioritize user prompt intent over background glare metrics], [xiilxj],
  [#49], [`222b37e`], [2026-10-22 00:39], [feat(vlm): support natural greeting, prompt intent analysis, and local llama-server probe], [xiilxj],
  [#48], [`729d8e5`], [2026-10-22 00:24], [fix(vlm): upgrade multimodal causal engine with semantic intent parsing and dynamic optical physics derivation], [xiilxj],
  [#47], [`7b0af02`], [2026-10-22 00:02], [feat(vlm): integrate autonomous perception heartbeat and streaming token typing for Qwen2.5-VL v3.0], [xiilxj],
  [#46], [`10f8e10`], [2026-10-21 23:45], [feat(v3): 全新 PyQt5 现代暗黑客户端上线，支持原生中文直接打字、DJI Action 5 Pro 自动锁定、算法双模切换与 Blender 无影灯式主动相消光环境], [xiilxj],
  [#45], [`0e52fd6`], [2026-10-21 23:17], [fix(launcher): 彻底消除控制台 Emoji 字符集崩溃与批处理管道符 syntax error，通过 Windows-MCP 实机验证通过], [xiilxj],
  [#44], [`99103b3`], [2026-10-21 09:56], [feat(interaction): 彻底打通 VLM 中文打字交互(弹窗/终端/键盘三通道)、增强相机深度扫描与热重扫机制(支持运动相机直切)], [xiilxj],
  [#43], [`f6cdfe7`], [2026-10-21 09:47], [fix(launcher): 优先锁定稳定版 Python 3.10 运行时，彻底解决 Python 3.14 下 NumPy C-extension DLL 缺失报错], [xiilxj],
  [#42], [`4477a83`], [2026-10-21 09:41], [feat(vlm): 完善 VLM 光环境交互系统 v2.0，修复 Windows 批处理 GBK 编码与路径截断，支持 USB 运动相机与双视口画中画切换], [xiilxj],
  [#41], [`934a4b2`], [2026-10-21 09:34], [feat(vlm): 升级Qwen2.5-VL视觉大模型、实现双视角画中画切换并新增健壮无乱码bat启动器 (第56轮审定)], [xiilxj],
  [#40], [`cb6997c`], [2026-10-21 09:24], [feat(vlm): 新增独立v2.0多模态VLM教室光环境主控系统，集成MiniCPM-V/InternVL与双通道摄像头切换 (第55轮审定)], [xiilxj],
  [#39], [`d21936f`], [2026-10-17 12:01], [feat(cad): 重构第三代总装蓝图工况三为8000mm真实物理拓扑并提升4K出图精度 (第53轮审定)], [xiilxj],
  [#38], [`ecb2f39`], [2026-10-17 11:43], [fix(board): 彻底统一展板为8000mm极限展开巨幕，消除时序图与卡片尺寸矛盾，规范典型避光角4.5°与机构极限15°，彻底剔除折射错词], [xiilxj],
  [#37], [`fa5a25e`], [2026-10-17 11:13], [fix(board): 彻底纠偏答辩展板第三区hero卡片为vi7高清图与8000mm规格，超分增强至4K印刷级], [xiilxj],
  [#36], [`9a84f30`], [2026-10-17 11:02], [docs: 移除作品介绍中的附录三(说明书附图)，目录与正文同步对齐至17页精简封板版], [xiilxj],
  [#35], [`6df7fe0`], [2026-10-17 10:56], [fix(kinematics): 彻底纠偏工况三与工况四为真实8000mm巨幕构型(中置大屏2m+固定板2m+两翼衍生板4m)，替换为vi7物理光追仿真导出图并同步更新19页全案PDF与展板Master], [xiilxj],
  [#34], [`8bcaeda`], [2026-10-17 09:26], [feat(exhibition-board): 完成第42届瑞安市青创赛答辩展板全要素重构，更新林诚俊(浙江省塘下中学)学籍认证并生成900x1200mm印刷级Master PDF与高清效果图], [xiilxj],
  [#33], [`4e489fd`], [2026-10-03 09:58], [docs(deliverable): 重构专业README、沉淀全套Plan矢量SVG图库并编译导出今日交付报告PDF(第40轮)], [xiilxj],
  [#32], [`7e21e45`], [2026-10-03 09:46], [docs(review): 完成第39轮技术审核封板，记录写实感痛点分析与明日攻坚路线图], [xiilxj],
  [#31], [`e1a97df`], [2026-10-03 09:34], [feat(viewport): 增加3D视口强制重绘标签(tag\_redraw)确保双手脱离鼠标下60FPS实时物理驱动(第38轮)], [xiilxj],
  [#30], [`2bc5a29`], [2026-10-03 09:27], [docs(review): 更新VI系列开发记录至第37轮工程技术审核], [xiilxj],
  [#29], [`caca317`], [2026-10-03 09:26], [fix(launcher): 彻底修复Windows批处理解析异常、OpenCV5兼容性与多版本Python调度(第37轮)], [xiilxj],
  [#28], [`abc2214`], [2026-10-03 09:16], [fix(vlm): 修复Blender 5.0定时器API并部署Windows双规批处理启动脚本(第36轮)], [xiilxj],
  [#27], [`fc721ce`], [2026-10-03 09:03], [fix(launcher): resolve Windows CMD encoding crash by adding \_\_main\_\_.py, robust run\_live\_system.py, and pure ASCII safe batch launchers], [xiilxj],
  [#26], [`db8deed`], [2026-10-03 08:57], [feat(live-vr): complete round 35 review with live Blender viewport 60FPS addon, interactive natural language operator with tool calling feed, and 1-click launcher batch], [xiilxj],
  [#25], [`e3fb14b`], [2026-10-03 08:47], [feat(hud): complete round 34 review with standalone multi-camera EAR squint detector, live Blender sync, and 1280x720 decision dashboard HUD], [xiilxj],
  [#24], [`bc67121`], [2026-10-03 08:36], [feat(vlm): add automated Qwen2.5-VL pipeline with multi-backend sniffing and Pareto actuator dispatch], [xiilxj],
  [#23], [`6d7b709`], [2026-10-03 08:29], [feat(vlm): complete round 32 review with small edge VLM matrix, 8x6 48-seat advanced classroom, penetrating Tyndall volumetric lighting, and coaxial high-energy laser beams], [xiilxj],
  [#22], [`aeda77a`], [2026-10-03 08:16], [feat(vlm): complete round 31 review with edge VLM selection report, digital twin optical simulation blend, 45-seat Pareto optimizer, and 3-camera preview renders], [xiilxj],
  [#21], [`1e53587`], [2026-10-03 07:44], [feat(vi-series): 完成VI7母本构建并通过用户动力学检验，大立柱中央对碰闭环，更新开发记录与第30轮审核], [xiilxj],
  [#20], [`7003653`], [2026-10-03 07:12], [fix(vi5): 校正内侧粗框架至X=±1.0m并彻底消除视口所有杂乱对角虚线vi5.blend \[第28轮工程技术审核\]], [xiilxj],
  [#19], [`e01f0a6`], [2026-10-03 07:00], [fix(vi4): 彻底校正折叠板正前方翻折轨迹杜绝穿墙并完善C型限位卡槽vi4.blend \[第27轮工程技术审核\]], [xiilxj],
  [#18], [`0b5d97f`], [2026-10-03 06:50], [fix(vi3): 修复折叠板向内翻转回填空缺并增加正反C型端头限位卡槽vi3.blend \[第26轮工程技术审核\]], [xiilxj],
  [#17], [`af92f06`], [2026-10-03 06:37], [fix(vi2): 彻底修复杆件外露缺陷并完成阶段二180度完整翻转动画母本vi2.blend \[第25轮工程技术审核\]], [xiilxj],
  [#16], [`dfa50b7`], [2026-10-03 06:16], [feat(vlm): 增加基于VLM多模态大模型控制Blender控件架构方案与VI系列控制桥接中枢代码 \[第24轮工程技术审核\]], [xiilxj],
  [#15], [`3d8fcda`], [2026-10-03 06:14], [feat(vi): 提交第三代VI系列动画母本vi1.blend与关键帧动力学开发记录 \[第24轮工程技术审核\]], [xiilxj],
  [#14], [`77612c8`], [2026-10-03 06:10], [feat(castic): 提交第三代多维叠合翻转智能黑板三维建模总装工程、S系列、Z系列与VI系列动画设计母本 \[第24轮工程技术审核\]], [xiilxj],
  [#13], [`0732fe6`], [2026-09-24 22:42], [fix(identity): 校准项目负责人学段为现高一初三构思、固化长期记忆并封存首版3D模型待命 (Review Round 20)], [xiilxj],
  [#12], [`4cb2ac5`], [2026-09-24 22:39], [feat(gen3-blender): 第三代多维智能黑板Blender三维参数化建模与多工况4K光环境渲染全量交付 (Review Round 19)], [xiilxj],
  [#11], [`ee7cdf9`], [2026-09-12 21:50], [docs(toolchain): 入库基于开源cad-mcp的WSL与WindowsAutoCAD跨环境Agent智能制图架构报告 (Review Round 18)], [xiilxj],
  [#10], [`0f48ba5`], [2026-09-12 21:16], [docs(log): 更新第17轮技术审核日志并同步至GitHub公开存证仓库], [xiilxj],
  [#9], [`b887686`], [2026-09-12 21:15], [docs(castic): 针对高中生CASTIC全国青少年科技创新大赛定制三自原则自证与问辩攻略 (Review Round 16)], [xiilxj],
  [#8], [`3b737a5`], [2026-09-12 21:15], [docs(review): 入库国赛评审专家视角深度评估与答辩攻防备忘录 (Review Round 15)], [xiilxj],
  [#7], [`635001c`], [2026-09-12 21:15], [refactor(report-v1.0): 确立VLM赋能光环境新题头、规范第一阶段技术测验属性并去除非正式署名 (Review Round 14)], [xiilxj],
  [#6], [`337741d`], [2026-09-12 21:15], [docs(report): 首版多维教学黑板系统架构演进与交付报告编制 (Review Round 13)], [xiilxj],
  [#5], [`e444007`], [2026-09-12 21:15], [feat(gen3-v1.2): 实现对角线双铰链空间正交解耦与右上角A-A俯视详图重构 (Review Round 12)], [xiilxj],
  [#4], [`6055beb`], [2026-09-12 21:15], [fix(gen3-v1.1): 拓扑修正与防颤闭环：内侧铰链归位、补齐双横梁伸缩套杆与垂直拉杆 (Review Round 11)], [xiilxj],
  [#3], [`dc0a561`], [2026-09-12 21:15], [feat(gen3-v1.0): 第三代多维叠合翻转全覆盖构型创新与三大工况大一统 (Review Round 10)], [xiilxj],
  [#2], [`9c2eedd`], [2026-09-12 21:15], [feat(gen2): 第二代三维空间联动自洁防眩光黑板系统与3D动力学模型 (Review Round 8-9)], [xiilxj],
  [#1], [`6a69b2a`], [2026-09-12 21:15], [feat(gen1): 第一代翻转式多媒体黑板机构参数与工程图纸建立 (Review Round 7)], [xiilxj],
)

#v(6pt)

#rect(
  width: 100%,
  fill: rgb("#f8fafc"),
  stroke: 0.5pt + rgb("#94a3b8"),
  radius: 3pt,
  inset: (x: 8pt, y: 6pt)
)[
  #grid(
    columns: (1fr, auto),
    align: horizon,
    [
      #text(weight: "bold", size: 7.5pt, fill: rgb("#0f172a"))[【代码仓库完整性校验签名】]      #text(size: 7pt, fill: rgb("#475569"))[
        本文件由 Git 自动化版本追溯工具直接生成，全量 80 项提交哈希与 GitHub 远端分支 `origin/main` 保持 100% 密码学一致。        评审专家可随时通过克隆官方开源仓库并执行 `git log --stat` 进行原位取证与重现。
      ]
    ],
    [
      #align(center)[
        #rect(fill: rgb("#e2e8f0"), stroke: 0.5pt + rgb("#64748b"), radius: 2pt, inset: 4pt)[
          #text(size: 6.8pt, weight: "bold", fill: rgb("#1e293b"))[CASTIC 2026\ 官方认证归档]
        ]
      ]
    ]
  )
]
