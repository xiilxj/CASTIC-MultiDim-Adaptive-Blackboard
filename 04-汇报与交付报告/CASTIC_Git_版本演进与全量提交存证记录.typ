#set page(
  paper: "a4",
  margin: (x: 1.5cm, top: 1.4cm, bottom: 1.4cm),
  header: context {
    if counter(page).get().first() > 0 [
      #grid(
        columns: (1fr, auto),
        align(left)[#text(size: 8.5pt, fill: rgb("#334155"), weight: "bold")[CASTIC 2026 · 光衡 (GH-VI-2026) GitHub 研发版本演进存证档案]],
        align(right)[#text(size: 8.5pt, fill: rgb("#475569"))[官方真实性与三自原则存证 · 第 #counter(page).display() 页]]
      )
      #v(-2pt)
      #line(length: 100%, stroke: 0.5pt + rgb("#cbd5e1"))
    ]
  },
  footer: [
    #line(length: 100%, stroke: 0.5pt + rgb("#cbd5e1"))
    #v(-2pt)
    #grid(
      columns: (1fr, auto),
      align(left)[#text(size: 8pt, fill: rgb("#64748b"))[项目唯一官方开源仓库: https://github.com/xiilxj/CASTIC-MultiDim-Adaptive-Blackboard]],
      align(right)[#text(size: 8.5pt, weight: "bold", fill: rgb("#0f172a"))[#context counter(page).display("1 / 1", both: true)]]
    )
  ]
)

#set text(
  font: ("WenQuanYi Micro Hei", "WenQuanYi Zen Hei"),
  size: 8.5pt,
  fill: rgb("#0f172a"),
  lang: "zh"
)

#set par(leading: 0.55em, justify: true)

#rect(
  width: 100%,
  fill: rgb("#0f172a"),
  radius: 4pt,
  inset: (x: 14pt, y: 10pt)
)[
  #align(center)[
    #text(size: 8pt, fill: rgb("#94a3b8"), tracking: 1.5pt, weight: "bold")[第 42 届全国青少年科技创新大赛 · 自主研发与三自原则存证文件]\
    #v(3pt)
    #text(size: 13.5pt, fill: white, weight: "bold")[光衡 (GH-VI-2026) 源代码版本演进与全量 Git 提交官方存证记录]\
    #v(3pt)
    #text(size: 8pt, fill: rgb("#38bdf8"))[项目负责人：林诚俊 | 存证截止时间：2026-10-30 09:45:00 | 累计真实版本迭代：75+ 轮次]
  ]
]

#v(4pt)

#rect(
  width: 100%,
  fill: rgb("#f8fafc"),
  stroke: 0.5pt + rgb("#cbd5e1"),
  radius: 3pt,
  inset: (x: 8pt, y: 6pt)
)[
  #text(weight: "bold", size: 8.8pt, fill: rgb("#0f172a"))[【版本控制真实性声明】] \
  本项目所有工程图纸、动力学仿真脚本、大一统偏微分方程理论推导、Typst 答辩报告与 VLM 控制中枢代码均采用 Git 分布式版本控制系统进行全生命周期管理。以下记录直接导出自本地与 GitHub 远端主分支（`origin/main`），SHA-1 哈希值具备密码学防篡改特性，完整印证了团队从真实痛点调研、机构失效迭代、多模态算法闭环到物理数学大一统证明的真实研发轨迹。
]

#v(6pt)

#table(
  columns: (45pt, 95pt, 1fr, 45pt),
  fill: (col, row) => if row == 0 { rgb("#1e293b") } else if calc.even(row) { rgb("#f8fafc") } else { rgb("#ffffff") },
  stroke: 0.3pt + rgb("#cbd5e1"),
  align: (center + horizon, center + horizon, left + horizon, center + horizon),
  table.header(
    [*#text(fill: white)[Commit]*],
    [*#text(fill: white)[提交时间 (UTC+8)]*],
    [*#text(fill: white)[版本演进与功能里程碑日志 (Commit Message)]*],
    [*#text(fill: white)[提交者]*]
  ),
  [18e58af], [2026-10-30 09:43], [docs(readme): append unified equation theory and closed-form VLM control laws], [xiilxj],
  [fec2672], [2026-10-30 09:40], [fix(report): fix subplot mappings, contrast ceiling explanation, and normal vector sign], [xiilxj],
  [c473bcb], [2026-10-30 09:29], [docs(report): generate formal unified master equation derivation PDF report], [xiilxj],
  [1d9a9a2], [2026-10-30 09:21], [feat(optics): add unified integro-differential master equation theory and MATLAB suite], [xiilxj],
  [c5c2c92], [2026-10-29 01:55], [feat(matlab): add castic_live_demo_runner and 6-panel scientific simulation dashboard], [xiilxj],
  [ddec410], [2026-10-29 01:50], [feat(sim): 交付MATLAB R2025b物理光学与空间逆运动学仿真主引擎及四大子图全景验证图], [xiilxj],
  [d5b3094], [2026-10-29 00:28], [docs: 深度融入明眸皓齿工程、教育强国与教育均衡政策要素的专家答疑报告(最新核定版)], [xiilxj],
  [5d99242], [2026-10-28 23:52], [docs: 交付正式面向评审专家的《光衡 GH-VI-2026 关键技术质询与工程论证专家答疑报告》], [xiilxj],
  [0f1e827], [2026-10-28 23:42], [docs: 交付CASTIC-GH-VI-2026评委三十大刁钻质询与满分答辩攻防手册(直接打印版PDF)], [xiilxj],
  [ee7c3ed], [2026-10-24 11:14], [fix(launcher): 统一根目录启动器入口至 v3.0 旗舰版 (自动联动 Qwen2.5-VL 本地模型)], [xiilxj],
  [22b3b4b], [2026-10-23 09:54], [docs(castic): 提交 GitHub 全量 67 次 Git 研发提交记录官方存证档案 (单页 A4 高精全景版)], [xiilxj],
  [bae7c4e], [2026-10-23 09:45], [docs(castic): 提交 GH-VI-2026 数字孪生交互系统研发历程全景纪实报告 (严格5页高精A4完整收官)], [xiilxj],
  [3b77532], [2026-10-23 09:30], [fix(docs): clarify llama tag as local llama.cpp GGUF inference engine and update white SVGs], [xiilxj],
  [b086c5c], [2026-10-23 09:19], [feat(docs): add monochrome printable full lifecycle pipeline SVG/PDF and update README], [xiilxj],
  [7f6bb91], [2026-10-23 08:56], [docs: add optical student pov and multi-seat technical manual], [xiilxj],
  [1247da8], [2026-10-23 08:42], [feat(render): generate 360 panorama and clean student pov views for seat 3 and seat 5], [xiilxj],
  [e206061], [2026-10-23 05:58], [feat(matlab): add standalone castic simulation models script], [xiilxj],
  [95669b9], [2026-10-23 01:33], [docs: add castic anti-glare evidence report source and pdf], [xiilxj],
  [d654516], [2026-10-23 01:19], [feat: add targeted beam rendering and student pov realism verification scripts], [xiilxj]
)
