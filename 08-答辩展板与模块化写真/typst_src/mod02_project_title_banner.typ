// ==============================================================================
// MOD-02: 项目主标题与作者学籍名牌 (Master Project Title Banner)
// 物理净尺寸: 860mm x 135mm (含四周 3mm 印刷出血位: 866mm x 141mm)
// 视觉基底: 高精工程蓝图底图 + 钛青深蓝渐变遮罩 + 300DPI 矢量排版
// 研发周期: 2025.09 - 2026.10 (初三日常观察萌生灵感，高一系统工程深化迭代)
// 标题优化: 字号升级至 60pt 大字 (字高约 23mm)，横跨 760mm，3~5米外清晰可读
// 严格防代做与零违规: 零导师姓名、零专家、零专利号、零既往获奖
// ==============================================================================

#set page(
  width: 866mm,
  height: 141mm,
  margin: (x: 3mm, y: 3mm), // 3mm 出血位
  fill: rgb("#06121E")
)

#set text(
  font: ("Microsoft YaHei", "SimHei"),
  fill: white
)

// 底层背景图铺满出血全幅面
#place(top + left, dx: 0mm, dy: 0mm)[
  #image(
    "../assets/tech_banner_bg.jpg",
    width: 866mm,
    height: 141mm,
    fit: "cover"
  )
]

// 叠加半透明深钛青色工程滤镜，保证文字 100% 锐利高反差
#place(top + left, dx: 0mm, dy: 0mm)[
  #rect(
    width: 866mm,
    height: 141mm,
    fill: gradient.linear(
      rgb(6, 18, 30, 86%),
      rgb(10, 29, 48, 80%),
      rgb(14, 40, 68, 78%),
      rgb(6, 18, 30, 88%),
      angle: 110deg
    )
  )
]

// 净尺寸裁切参考边框 (860mm x 135mm)
#rect(
  width: 860mm,
  height: 135mm,
  radius: 4pt,
  stroke: (paint: rgb("#00E5FF").transparentize(65%), thickness: 1.2pt),
  fill: none
)[
  // 内嵌精密工艺对齐角线
  #place(top + left, dx: 4mm, dy: 4mm)[
    #rect(
      width: 852mm,
      height: 127mm,
      stroke: (paint: rgb("#38BDF8").transparentize(85%), thickness: 0.6pt),
      fill: none
    )
  ]

  // 主体排版容器
  #pad(x: 16mm, top: 10mm, bottom: 8mm)[
    #grid(
      columns: (1fr),
      rows: (auto, auto, 1fr),
      row-gutter: 3.5mm,
      
      // 1. 中文主标题 (60pt 超大加粗工程黑体，物理高度约 23mm，霸气饱满)
      [
        #grid(
          columns: (auto, 1fr),
          align: (horizon, horizon),
          gutter: 8mm,
          
          // 科技发光指标符 (高光渐变指示立柱)
          rect(
            width: 9pt,
            height: 48pt,
            radius: 2.5pt,
            fill: gradient.linear(rgb("#00E5FF"), rgb("#0284C7"), angle: 90deg)
          ),
          
          // 主标题文字 (加大字号至 58pt，强化字重与饱满度)
          text(
            size: 58pt,
            weight: "black",
            tracking: 1.2pt,
            fill: rgb("#FFFFFF")
          )[
            面向VLM赋能教室光环境的多维教学黑板机构学设计与代际拓扑演进
          ]
        )
      ],
      
      // 2. 英文副标题 (学术科技风，浅青色发光，加大字号至 19pt)
      [
        #pad(left: 11mm)[
          #text(
            size: 19pt,
            weight: "medium",
            tracking: 1.5pt,
            fill: rgb("#7DD3FC")
          )[
            Kinematic Design and Generational Topological Evolution of Multi-Dimensional Classroom Blackboard Empowered by Vision-Language Models
          ]
        ]
      ],
      
      // 3. 底部：学术工程技术标签徽章 + 参赛真实研发名牌
      [
        #align(bottom)[
          #pad(left: 11mm)[
            #grid(
              columns: (auto, 1fr),
              align: (bottom + left, bottom + right),
              gutter: 12mm,
              
              // 左侧：5 大核心技术徽章 (Badges)
              stack(
                dir: ltr,
                spacing: 3.5mm,
                
                rect(
                  stroke: 0.8pt + rgb("#00E5FF").transparentize(40%),
                  fill: rgb("#00E5FF").transparentize(90%),
                  radius: 3pt,
                  inset: (x: 8pt, y: 4.5pt)
                )[
                  #text(size: 11.5pt, weight: "bold", fill: rgb("#38BDF8"))[机构学对角线正交解耦]
                ],
                
                rect(
                  stroke: 0.8pt + rgb("#00E5FF").transparentize(40%),
                  fill: rgb("#00E5FF").transparentize(90%),
                  radius: 3pt,
                  inset: (x: 8pt, y: 4.5pt)
                )[
                  #text(size: 11.5pt, weight: "bold", fill: rgb("#38BDF8"))[4000~8000mm 4自由度演进]
                ],
                
                rect(
                  stroke: 0.8pt + rgb("#34D399").transparentize(40%),
                  fill: rgb("#34D399").transparentize(90%),
                  radius: 3pt,
                  inset: (x: 8pt, y: 4.5pt)
                )[
                  #text(size: 11.5pt, weight: "bold", fill: rgb("#34D399"))[端侧 VLM 视觉闭环自适应避光]
                ],
                
                rect(
                  stroke: 0.8pt + rgb("#FBBF24").transparentize(40%),
                  fill: rgb("#FBBF24").transparentize(90%),
                  radius: 3pt,
                  inset: (x: 8pt, y: 4.5pt)
                )[
                  #text(size: 11.5pt, weight: "bold", fill: rgb("#FBBF24"))[Blender 5.0 Cycles 光线追踪验证]
                ],
                
                rect(
                  stroke: 0.8pt + rgb("#A78BFA").transparentize(40%),
                  fill: rgb("#A78BFA").transparentize(90%),
                  radius: 3pt,
                  inset: (x: 8pt, y: 4.5pt)
                )[
                  #text(size: 11.5pt, weight: "bold", fill: rgb("#C084FC"))[基于 cad-mcp 参数化工业制图]
                ]
              ),
              
              // 右侧：防代做真实学籍与研发周期记录
              stack(
                dir: ltr,
                spacing: 6mm,
                
                rect(
                  stroke: 1pt + rgb("#D4AF37").transparentize(30%),
                  fill: rgb("#06121E").transparentize(15%),
                  radius: 3pt,
                  inset: (x: 10pt, y: 4.5pt)
                )[
                  #text(size: 11.5pt, weight: "bold", fill: rgb("#FBD38D"))[
                    真实研发周期：2025.09 - 2026.10（初三日常观察灵感萌生，高一工程深化迭代）
                  ]
                ],
                
                rect(
                  stroke: 1pt + rgb("#38BDF8").transparentize(30%),
                  fill: rgb("#06121E").transparentize(15%),
                  radius: 3pt,
                  inset: (x: 10pt, y: 4.5pt)
                )[
                  #text(size: 11.5pt, weight: "bold", fill: rgb("#E2E8F0"))[
                    高中组个人发明项目 · 独立研发
                  ]
                ]
              )
            )
          ]
        ]
      ]
    )
  ]
]
