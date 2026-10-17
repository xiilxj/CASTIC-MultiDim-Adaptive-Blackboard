
#set page(width: 860mm, height: 160mm, margin: (x: 10mm, y: 5mm), fill: rgb("#06121E"))
#set text(font: ("SimHei", "Microsoft YaHei"), fill: white)

#grid(
  columns: (1fr),
  rows: (12mm, 1fr, 14mm),
  row-gutter: 2mm,
  
  // 1. 页眉
  grid(
    columns: (1fr, auto),
    align: (left + horizon, right + horizon),
    stack(
      dir: ltr,
      spacing: 3mm,
      circle(radius: 4.5mm, fill: rgb("#d97706"), align(center + horizon)[#text(size: 8pt, weight: "bold")[★]]),
      text(size: 15pt, weight: "black")[第 42 届瑞安市青少年科技创新大赛科技创新项目]
    ),
    rect(stroke: 1pt + rgb("#38bdf8"), fill: rgb("#0284c7").transparentize(40%), radius: 2.5pt, inset: (x: 7pt, y: 3pt))[
      #text(size: 9pt, weight: "bold", fill: rgb("#bae6fd"))[学科代码: ENGI (工程学)]
    ]
  ),
  
  // 2. 核心双行大标题 (强制 Grid 显式物理隔离)
  align(horizon)[
    #grid(
      columns: (auto, 1fr),
      gutter: 6mm,
      align: (horizon, horizon),
      rect(width: 8pt, height: 105mm, fill: rgb("#38bdf8"), radius: 3pt),
      
      grid(
        columns: (1fr),
        rows: (auto, auto, auto),
        row-gutter: 8mm,
        
        block[#text(size: 105pt, weight: "black", fill: white, tracking: 1.2pt)[面向 VLM 赋能教室光环境的]],
        block[#text(size: 105pt, weight: "black", fill: white, tracking: 1.2pt)[多维教学黑板机构学设计与代际拓扑演进]],
        block[#text(size: 11.5pt, weight: "medium", fill: rgb("#94a3b8"), tracking: 1.8pt)[Kinematic Design and Generational Topological Evolution of Multi-Dimensional Classroom Blackboard Empowered by Vision-Language Models]]
      )
    )
  ],
  
  // 3. 底部胶囊
  grid(
    columns: (1fr, auto),
    align: (left + horizon, right + horizon),
    stack(
      dir: ltr,
      spacing: 3mm,
      ..("对角线双铰链正交解耦", "4000~6000mm 4自由度复合机构", "端侧 VLM 视觉闭环自适应避光", "Blender 5.0 Cycles 光照重构", "AutoCAD 4K 蓝图").map(t => {
        rect(stroke: 0.8pt + rgb("#0284c7"), fill: rgb("#0c2138"), radius: 2pt, inset: (x: 5pt, y: 2.5pt))[
          #text(size: 9pt, weight: "bold", fill: rgb("#bae6fd"))[#t]
        ]
      })
    ),
    rect(stroke: 0.8pt + rgb("#f59e0b"), fill: rgb("#451a03").transparentize(25%), radius: 2pt, inset: (x: 6pt, y: 2.5pt))[
      #text(size: 9pt, weight: "bold", fill: rgb("#fde68a"))[真实研发周期: 2025.09 - 2026.10 (高中组个人独立研发)]
    ]
  )
)
