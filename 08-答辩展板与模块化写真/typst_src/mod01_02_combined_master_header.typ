// ==============================================================================
// MOD-01_02: 顶栏一体化官方大赛页眉与主标题总成 (Master Header Banner)
// 物理净尺寸: 860mm x 180mm (含四周 3mm 印刷出血位: 866mm x 186mm)
// 架构整合: 融合原 MOD-01 官方大赛页眉 + 原 MOD-02 项目主标题与防代做学籍名牌
// 视觉基底: 8K 极简钛青工程蓝图背景 + 深钛青渐变滤镜 + 300DPI 印刷级矢量排版
// 研发周期: 2025.09 - 2026.10 (初三日常观察灵感萌生，高一工程深化迭代)
// 红线合规: 严格依照通知第7页规定，零导师姓名、零专家、零专利号、零既往获奖
// ==============================================================================

#set page(
  width: 866mm,
  height: 186mm,
  margin: (x: 3mm, y: 3mm), // 四周 3mm 印刷出血位
  fill: rgb("#06121E")
)

#set text(
  font: ("Microsoft YaHei", "SimHei"),
  fill: white
)

// 1. 底层高精度工程蓝图背景铺满整个出血幅面
#place(top + left, dx: 0mm, dy: 0mm)[
  #image(
    "../assets/tech_banner_bg.jpg",
    width: 866mm,
    height: 186mm,
    fit: "cover"
  )
]

// 2. 叠加半透明深钛青色工程滤镜，保证文字 100% 锐利高反差
#place(top + left, dx: 0mm, dy: 0mm)[
  #rect(
    width: 866mm,
    height: 186mm,
    fill: gradient.linear(
      rgb(6, 18, 30, 88%),
      rgb(10, 29, 48, 82%),
      rgb(14, 40, 68, 80%),
      rgb(6, 18, 30, 90%),
      angle: 110deg
    )
  )
]

// 3. 净尺寸裁切参考外边框 (860mm x 180mm)
#rect(
  width: 860mm,
  height: 180mm,
  radius: 4pt,
  stroke: (paint: rgb("#00E5FF").transparentize(60%), thickness: 1.5pt),
  fill: none
)[
  // 内嵌精密工艺装裱边线
  #place(top + left, dx: 4mm, dy: 4mm)[
    #rect(
      width: 852mm,
      height: 172mm,
      stroke: (paint: rgb("#38BDF8").transparentize(85%), thickness: 0.6pt),
      fill: none
    )
  ]

  // 主体内容分层容器
  #pad(x: 18mm, top: 10mm, bottom: 8mm)[
    #grid(
      columns: (1fr),
      rows: (36mm, 1fr, 32mm),
      row-gutter: 0mm,
      
      // ------------------------------------------------------------------------
      // 第一层: 官方大赛页眉楣头栏 (符合通知第7页强制规定)
      // ------------------------------------------------------------------------
      [
        #grid(
          columns: (1fr, auto),
          align: (left + horizon, right + horizon),
          gutter: 15mm,
          
          // 左侧：官方核心规定标题与科技星徽
          stack(
            dir: ltr,
            spacing: 8mm,
            
            // 科技金星徽章
            align(horizon)[
              #circle(
                radius: 11pt,
                fill: rgb("#D4AF37"),
                stroke: 1.5pt + white
              )[
                #align(center + horizon)[
                  #text(size: 13pt, fill: rgb("#06121E"), weight: "bold")[★]
                ]
              ]
            ],
            
            // 官方规定字样
            align(horizon)[
              #text(
                size: 24pt,
                weight: "bold",
                tracking: 3pt,
                fill: rgb("#FFFFFF")
              )[
                第42届瑞安市青少年科技创新大赛科技创新项目
              ]
            ]
          ),
          
          // 右侧：学科分类与组别徽章
          stack(
            dir: ltr,
            spacing: 8mm,
            
            rect(
              stroke: 1pt + rgb("#00E5FF").transparentize(40%),
              fill: rgb("#00E5FF").transparentize(88%),
              radius: 3pt,
              inset: (x: 9pt, y: 4.5pt)
            )[
              #text(size: 12pt, weight: "bold", fill: rgb("#00E5FF"))[
                高中组 · 科技创新发明类
              ]
            ],
            
            rect(
              stroke: 1pt + rgb("#D4AF37").transparentize(40%),
              fill: rgb("#D4AF37").transparentize(88%),
              radius: 3pt,
              inset: (x: 9pt, y: 4.5pt)
            )[
              #text(size: 12pt, weight: "bold", fill: rgb("#FBD38D"))[
                学科代码：ENGI（工程学）
              ]
            ]
          )
        )
        
        // 区域分隔细线 (科技渐变光线)
        #pad(top: 8mm)[
          #line(
            length: 100%,
            stroke: (paint: gradient.linear(rgb("#00E5FF").transparentize(80%), rgb("#00E5FF"), rgb("#D4AF37"), rgb("#D4AF37").transparentize(80%)), thickness: 1pt)
          )
        ]
      ],
      
      // ------------------------------------------------------------------------
      // 第二层: 项目主标题与英文副标题核心展示区 (全场视觉焦点)
      // ------------------------------------------------------------------------
      [
        #align(horizon)[
          #pad(top: 4mm, bottom: 4mm)[
            #grid(
              columns: (auto, 1fr),
              align: (horizon, horizon),
              gutter: 9mm,
              
              // 垂直高光渐变指示立柱
              rect(
                width: 9pt,
                height: 52pt,
                radius: 2.5pt,
                fill: gradient.linear(rgb("#00E5FF"), rgb("#0284C7"), angle: 90deg)
              ),
              
              // 标题文字垂直组合
              stack(
                dir: ttb,
                spacing: 3.5mm,
                
                // 主标题文字 (58pt 超大加粗大字，字高 2.76cm，3~5米外一眼看清)
                text(
                  size: 58pt,
                  weight: "black",
                  tracking: 1.2pt,
                  fill: rgb("#FFFFFF")
                )[
                  面向VLM赋能教室光环境的多维教学黑板机构学设计与代际拓扑演进
                ],
                
                // 英文副标题 (学术国际感，浅青发光)
                text(
                  size: 18.5pt,
                  weight: "medium",
                  tracking: 1.4pt,
                  fill: rgb("#7DD3FC")
                )[
                  Kinematic Design and Generational Topological Evolution of Multi-Dimensional Classroom Blackboard Empowered by Vision-Language Models
                ]
              )
            )
          ]
        ]
      ],
      
      // ------------------------------------------------------------------------
      // 第三层: 5大核心技术胶囊徽章 + 防代做学籍与真实研发周期记录
      // ------------------------------------------------------------------------
      [
        #align(bottom)[
          #grid(
            columns: (auto, 1fr),
            align: (bottom + left, bottom + right),
            gutter: 12mm,
            
            // 左侧：5 大核心技术胶囊徽章 (Badges)
            stack(
              dir: ltr,
              spacing: 3.5mm,
              
              rect(
                stroke: 0.8pt + rgb("#00E5FF").transparentize(40%),
                fill: rgb("#00E5FF").transparentize(90%),
                radius: 3pt,
                inset: (x: 8pt, y: 4.5pt)
              )[
                #text(size: 11pt, weight: "bold", fill: rgb("#38BDF8"))[机构学对角线正交解耦]
              ],
              
              rect(
                stroke: 0.8pt + rgb("#00E5FF").transparentize(40%),
                fill: rgb("#00E5FF").transparentize(90%),
                radius: 3pt,
                inset: (x: 8pt, y: 4.5pt)
              )[
                #text(size: 11pt, weight: "bold", fill: rgb("#38BDF8"))[4000~6000mm 4自由度演进]
              ],
              
              rect(
                stroke: 0.8pt + rgb("#34D399").transparentize(40%),
                fill: rgb("#34D399").transparentize(90%),
                radius: 3pt,
                inset: (x: 8pt, y: 4.5pt)
              )[
                #text(size: 11pt, weight: "bold", fill: rgb("#34D399"))[端侧 VLM 视觉闭环自适应避光]
              ],
              
              rect(
                stroke: 0.8pt + rgb("#FBBF24").transparentize(40%),
                fill: rgb("#FBBF24").transparentize(90%),
                radius: 3pt,
                inset: (x: 8pt, y: 4.5pt)
              )[
                #text(size: 11pt, weight: "bold", fill: rgb("#FBBF24"))[Blender 5.0 Cycles 光线追踪验证]
              ],
              
              rect(
                stroke: 0.8pt + rgb("#A78BFA").transparentize(40%),
                fill: rgb("#A78BFA").transparentize(90%),
                radius: 3pt,
                inset: (x: 8pt, y: 4.5pt)
              )[
                #text(size: 11pt, weight: "bold", fill: rgb("#C084FC"))[基于 cad-mcp 参数化工业制图]
              ]
            ),
            
            // 右侧：防代做真实学籍与研发周期名牌
            stack(
              dir: ltr,
              spacing: 6mm,
              
              rect(
                stroke: 1pt + rgb("#D4AF37").transparentize(30%),
                fill: rgb("#06121E").transparentize(15%),
                radius: 3pt,
                inset: (x: 9pt, y: 4.5pt)
              )[
                #text(size: 11pt, weight: "bold", fill: rgb("#FBD38D"))[
                  真实研发周期：2025.09 - 2026.10（初三日常观察灵感萌生，高一工程深化迭代）
                ]
              ],
              
              rect(
                stroke: 1pt + rgb("#38BDF8").transparentize(30%),
                fill: rgb("#06121E").transparentize(15%),
                radius: 3pt,
                inset: (x: 9pt, y: 4.5pt)
              )[
                #text(size: 11pt, weight: "bold", fill: rgb("#E2E8F0"))[
                  高中组个人发明项目 · 独立研发
                ]
              ]
            )
          )
        ]
      ]
    )
  ]
]
