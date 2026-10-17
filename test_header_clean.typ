
#set page(width: 860mm, height: 160mm, margin: (x: 10mm, y: 6mm))
#set text(font: ("SimHei", "Microsoft YaHei"))

#grid(
  columns: (1fr),
  rows: (14mm, 1fr, 16mm),
  row-gutter: 3mm,
  
  // 1. 页眉
  grid(
    columns: (1fr, auto),
    align: (left + horizon, right + horizon),
    text(size: 16pt, weight: "black", fill: rgb("#f59e0b"))[★ 第 42 届瑞安市青少年科技创新大赛科技创新项目],
    text(size: 10pt, weight: "bold", fill: rgb("#38bdf8"))[学科代码: ENGI (工程学)]
  ),
  
  // 2. 核心双行大标题
  align(horizon)[
    #grid(
      columns: (auto, 1fr),
      gutter: 6mm,
      rect(width: 8pt, height: 100%, fill: rgb("#38bdf8"), radius: 3pt),
      
      stack(
        dir: ttb,
        spacing: 0mm,
        
        block(height: 48mm)[
          #align(horizon)[
            #text(size: 120pt, weight: "black", fill: rgb("#ffffff"))[面向 VLM 赋能教室光环境的]
          ]
        ],
        v(4mm),
        block(height: 48mm)[
          #align(horizon)[
            #text(size: 120pt, weight: "black", fill: rgb("#ffffff"))[多维教学黑板机构学设计与代际拓扑演进]
          ]
        ],
        v(5mm),
        text(size: 12pt, weight: "medium", fill: rgb("#94a3b8"), tracking: 1.8pt)[
          Kinematic Design and Generational Topological Evolution of Multi-Dimensional Classroom Blackboard Empowered by Vision-Language Models
        ]
      )
    )
  ],
  
  // 3. 底部胶囊
  grid(
    columns: (1fr, auto),
    align: (left + horizon, right + horizon),
    text(size: 10pt, fill: rgb("#bae6fd"))[对角线双铰链正交解耦 · 4000~6000mm 4自由度机构 · 端侧 VLM 视觉闭环自适应避光],
    text(size: 10pt, fill: rgb("#fde68a"))[真实研发周期: 2025.09 - 2026.10 (独立研发)]
  )
)
