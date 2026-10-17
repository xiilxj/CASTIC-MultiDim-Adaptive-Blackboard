// ==============================================================================
// MOD-03_05 v2: 左侧列高信息密度·四代CAD拓扑演进与工具链一体化大长条
// 物理净尺寸: 270mm x 920mm (含四周 3mm 印刷出血位: 276mm x 926mm)
// 核心优化: 彻底消除大彩框与无效留白，2x2 紧凑四象限矩阵放大 CAD 黑板图元
// 内容三段式: ① 教室反光痛点纪实照片+实测数据表 -> ② 四代CAD演进矩阵 -> ③ 跨平台Python制图实证
// ==============================================================================

#set page(
  width: 276mm,
  height: 926mm,
  margin: (x: 3mm, y: 3mm), // 3mm 印刷出血位
  fill: rgb("#F8FAFC") // 极简工程冷白底色
)

#set text(
  font: ("Microsoft YaHei", "SimHei"),
  fill: rgb("#0F172A")
)

// 净尺寸裁切外边框 (270mm x 920mm)
#rect(
  width: 270mm,
  height: 920mm,
  radius: 3pt,
  stroke: (paint: rgb("#CBD5E1"), thickness: 1.2pt),
  fill: rgb("#FFFFFF")
)[
  #pad(x: 6mm, top: 6mm, bottom: 6mm)[
    #grid(
      columns: (1fr),
      rows: (18mm, 260mm, 320mm, 1fr),
      row-gutter: 0mm,
      
      // ========================================================================
      // 0. 栏目主头部：科技钛青深蓝标头
      // ========================================================================
      [
        #rect(
          width: 100%,
          height: 16mm,
          radius: 2.5pt,
          fill: gradient.linear(rgb("#0F294A"), rgb("#1E3E62"), angle: 90deg),
          stroke: (paint: rgb("#00E5FF").transparentize(60%), thickness: 0.8pt)
        )[
          #pad(x: 5mm)[
            #align(horizon)[
              #grid(
                columns: (1fr, auto),
                align: (left + horizon, right + horizon),
                
                stack(
                  dir: ttb,
                  spacing: 1mm,
                  text(size: 13pt, weight: "black", fill: white, tracking: 0.8pt)[
                    【模块一】研究背景 · 拓扑演进 · 数字化制图
                  ],
                  text(size: 7.5pt, weight: "medium", fill: rgb("#7DD3FC"))[
                    Problem Origin · Generational Evolution · Parametric Toolchain
                  ]
                ),
                
                rect(
                  stroke: 0.8pt + rgb("#D4AF37"),
                  fill: rgb("#06121E").transparentize(20%),
                  radius: 2pt,
                  inset: (x: 4.5pt, y: 2.5pt)
                )[
                  #text(size: 7.5pt, weight: "bold", fill: rgb("#FBD38D"))[初三观察·高一攻坚]
                ]
              )
            ]
          ]
        ]
      ],
      
      // ========================================================================
      // 1. 第一板块：教室光环境痛点实测与反光测绘 (纪实图 + 测绘数据表)
      // ========================================================================
      [
        #pad(top: 2.5mm, bottom: 2mm)[
          #rect(
            width: 100%,
            height: 255mm,
            radius: 2.5pt,
            stroke: 0.8pt + rgb("#E2E8F0"),
            fill: rgb("#F8FAFC")
          )[
            #pad(x: 4.5mm, top: 3.5mm, bottom: 3mm)[
              #grid(
                columns: (1fr),
                rows: (16mm, 105mm, 1fr),
                row-gutter: 2mm,
                
                // 小标头
                grid(
                  columns: (auto, 1fr, auto),
                  align: (horizon, horizon, horizon),
                  gutter: 2.5mm,
                  rect(width: 3.5pt, height: 13pt, fill: rgb("#0284C7"), radius: 1pt),
                  text(size: 10.5pt, weight: "bold", fill: rgb("#0F172A"))[
                    1. 教室反光痛点纪实与光学测绘数据
                  ],
                  text(size: 7.5pt, fill: rgb("#DC2626"), weight: "bold")[
                    [实测超标 5.7 倍]
                  ]
                ),
                
                // 痛点实景照片展示
                rect(
                  width: 100%,
                  height: 105mm,
                  radius: 2pt,
                  stroke: 0.6pt + rgb("#CBD5E1"),
                  fill: black
                )[
                  #image(
                    "../assets/classroom_glare_pain.jpg",
                    width: 100%,
                    height: 100%,
                    fit: "cover"
                  )
                ],
                
                // 实测数据对比表 (紧凑硬核)
                pad(top: 1mm)[
                  #table(
                    columns: (1.2fr, 1fr, 1.2fr, 1.6fr),
                    align: (left, center, center, left),
                    stroke: 0.5pt + rgb("#CBD5E1"),
                    fill: (col, row) => if row == 0 { rgb("#E2E8F0") } else { white },
                    inset: (x: 3pt, y: 3pt),
                    
                    [#text(size: 7pt, weight: "bold")[测绘物理量]],
                    [#text(size: 7pt, weight: "bold")[国标 GB7793]],
                    [#text(size: 7pt, weight: "bold")[现场实测值]],
                    [#text(size: 7pt, weight: "bold")[人因危害评估]],
                    
                    [#text(size: 6.8pt)[黑板眩光照度]],
                    [#text(size: 6.8pt)[$<= 500$ Lux]],
                    [#text(size: 6.8pt, weight: "bold", fill: rgb("#DC2626"))[2850 Lux]],
                    [#text(size: 6.8pt, fill: rgb("#B91C1C"))[超标 5.7 倍，视网膜致盲]],
                    
                    [#text(size: 6.8pt)[字符反射对比度]],
                    [#text(size: 6.8pt)[$>= 10:1$]],
                    [#text(size: 6.8pt, weight: "bold", fill: rgb("#DC2626"))[1.8 : 1]],
                    [#text(size: 6.8pt, fill: rgb("#B91C1C"))[板书泛白发亮完全不可读]],
                    
                    [#text(size: 6.8pt)[推拉黑板机械死结]],
                    table.cell(colspan: 3)[#text(size: 6.8pt)[①大屏露显板书折损50%  ②滑轨积灰卡死  ③固定单平面无避光能力]]
                  )
                ]
              )
            ]
          ]
        ]
      ],
      
      // ========================================================================
      // 2. 第二板块：四代黑板机构拓扑演进 (2x2 紧凑四象限矩阵，占高仅310mm)
      // ========================================================================
      [
        #pad(top: 1mm, bottom: 2mm)[
          #rect(
            width: 100%,
            height: 315mm,
            radius: 2.5pt,
            stroke: 0.8pt + rgb("#0284C7"),
            fill: rgb("#F0F9FF")
          )[
            #pad(x: 4mm, top: 3.5mm, bottom: 2.5mm)[
              #grid(
                columns: (1fr),
                rows: (16mm, 1fr, 12mm),
                row-gutter: 1.5mm,
                
                // 标头
                grid(
                  columns: (auto, 1fr, auto),
                  align: (horizon, horizon, horizon),
                  gutter: 2.5mm,
                  rect(width: 3.5pt, height: 13pt, fill: rgb("#0284C7"), radius: 1pt),
                  text(size: 10.5pt, weight: "bold", fill: rgb("#0369A1"))[
                    2. 四代黑板机构拓扑演进 (2×2 紧凑工程矩阵)
                  ],
                  text(size: 7.5pt, fill: rgb("#0284C7"), weight: "bold")[
                    [实测图纸对比]
                  ]
                ),
                
                // 2x2 紧凑四象限矩阵 (每格宽约 124mm，高约 132mm)
                grid(
                  columns: (1fr, 1fr),
                  rows: (132mm, 132mm),
                  gutter: 2.5mm,
                  
                  // 格子 1: 市面基线推拉
                  rect(
                    stroke: 0.6pt + rgb("#EF4444"),
                    radius: 2pt,
                    fill: white,
                    inset: 2.5pt
                  )[
                    #grid(
                      columns: (1fr),
                      rows: (12mm, 92mm, 1fr),
                      [
                        #grid(
                          columns: (1fr, auto),
                          text(size: 7.5pt, weight: "bold", fill: rgb("#991B1B"))[【市面基线】标准推拉],
                          text(size: 6.5pt, fill: rgb("#EF4444"), weight: "bold")[原罪缺陷 ❌]
                        )
                      ],
                      [
                        #image("../assets/cad_2x2_1_baseline.png", width: 100%, height: 100%, fit: "contain")
                      ],
                      [
                        #text(size: 6.5pt, fill: rgb("#7F1D1D"))[
                          大屏露显遮挡板书50%；下导轨积灰受潮推拉卡死异响。
                        ]
                      ]
                    )
                  ],
                  
                  // 格子 2: 第一代重力悬臂
                  rect(
                    stroke: 0.6pt + rgb("#F59E0B"),
                    radius: 2pt,
                    fill: white,
                    inset: 2.5pt
                  )[
                    #grid(
                      columns: (1fr),
                      rows: (12mm, 92mm, 1fr),
                      [
                        #grid(
                          columns: (1fr, auto),
                          text(size: 7.5pt, weight: "bold", fill: rgb("#92400E"))[【第一代】重力悬臂外展],
                          text(size: 6.5pt, fill: rgb("#F59E0B"), weight: "bold")[挠度超限 ❌]
                        )
                      ],
                      [
                        #image("../assets/cad_2x2_2_gen1.png", width: 100%, height: 100%, fit: "contain")
                      ],
                      [
                        #text(size: 6.5pt, fill: rgb("#78350F"))[
                          悬臂梁端部挠度过大（实测 $delta approx 18$mm），铰链拉扯下垂卡死。
                        ]
                      ]
                    )
                  ],
                  
                  // 格子 3: 第二代双滑轨推拉
                  rect(
                    stroke: 0.6pt + rgb("#EA580C"),
                    radius: 2pt,
                    fill: white,
                    inset: 2.5pt
                  )[
                    #grid(
                      columns: (1fr),
                      rows: (12mm, 92mm, 1fr),
                      [
                        #grid(
                          columns: (1fr, auto),
                          text(size: 7.5pt, weight: "bold", fill: rgb("#9A3412"))[【第二代】双滑轨推拉复合],
                          text(size: 6.5pt, fill: rgb("#EA580C"), weight: "bold")[运动干涉 ❌]
                        )
                      ],
                      [
                        #image("../assets/cad_2x2_3_gen2.png", width: 100%, height: 100%, fit: "contain")
                      ],
                      [
                        #text(size: 6.5pt, fill: rgb("#7C2D12"))[
                          滑动副与转动副同轴空间干涉死锁，存在200mm机械盲区。
                        ]
                      ]
                    )
                  ],
                  
                  // 格子 4: 第三代正交解耦终极
                  rect(
                    stroke: 0.8pt + rgb("#10B981"),
                    radius: 2pt,
                    fill: rgb("#F0FDF4"),
                    inset: 2.5pt
                  )[
                    #grid(
                      columns: (1fr),
                      rows: (12mm, 92mm, 1fr),
                      [
                        #grid(
                          columns: (1fr, auto),
                          text(size: 7.5pt, weight: "bold", fill: rgb("#065F46"))[【第三代】对角线正交解耦],
                          text(size: 6.5pt, fill: rgb("#059669"), weight: "bold")[终极突破 ✅]
                        )
                      ],
                      [
                        #image("../assets/cad_2x2_4_gen3.png", width: 100%, height: 100%, fit: "contain")
                      ],
                      [
                        #text(size: 6.5pt, fill: rgb("#064E3B"), weight: "bold")[
                          对角线双铰链跨度隔离 $Delta X=1000$mm，零干涉4000~8000mm自由拓展。
                        ]
                      ]
                    )
                  ]
                ),
                
                // 引导提示条
                rect(
                  width: 100%,
                  height: 10mm,
                  fill: rgb("#0284C7"),
                  radius: 2pt,
                  inset: (x: 4pt, y: 2pt)
                )[
                  #align(center + horizon)[
                    #text(size: 7.5pt, weight: "bold", fill: white)[
                      ▶ 第三代核心总装 4K 超清实体渲染与四大运动工况见中间 C 位
                    ]
                  ]
                ]
              )
            ]
          ]
        ]
      ],
      
      // ========================================================================
      // 3. 第三板块：基于 cad-mcp 跨平台参数化智能制图 (代码与三自实证)
      // ========================================================================
      [
        #pad(top: 1mm)[
          #rect(
            width: 100%,
            height: 300mm,
            radius: 2.5pt,
            stroke: 0.8pt + rgb("#6366F1"),
            fill: rgb("#EEF2FF")
          )[
            #pad(x: 4.5mm, top: 3.5mm, bottom: 3mm)[
              #grid(
                columns: (1fr),
                rows: (16mm, 1fr, 35mm),
                row-gutter: 2mm,
                
                // 标头
                grid(
                  columns: (auto, 1fr, auto),
                  align: (horizon, horizon, horizon),
                  gutter: 2.5mm,
                  rect(width: 3.5pt, height: 13pt, fill: rgb("#4F46E5"), radius: 1pt),
                  text(size: 10.5pt, weight: "bold", fill: rgb("#3730A3"))[
                    3. 基于 cad-mcp 参数化制图与“三自”实证
                  ],
                  text(size: 7.5pt, fill: rgb("#4F46E5"), weight: "bold")[
                    [跨平台自主研发]
                  ]
                ),
                
                // Python 核心参数化驱动代码框
                rect(
                  width: 100%,
                  radius: 2pt,
                  stroke: 0.5pt + rgb("#C7D2FE"),
                  fill: rgb("#1E1B4B"),
                  inset: (x: 5pt, y: 4pt)
                )[
                  #text(font: "Consolas", size: 6.8pt, fill: rgb("#E0E7FF"))[
                    ```python
                    # WSL2 Linux 算法中枢通过 COM RPC 驱动 Windows AutoCAD 2026
                    import win32com.client as win32
                    acad = win32.Dispatch("AutoCAD.Application").ActiveDocument
                    # 1. 对角线双铰链与导轨参数化定位点计算
                    hinge_in = (±1000.0, 0.0, 0.0)   # 内侧 180° 翻折轴心
                    hinge_out = (±2000.0, -85.0, 0.0) # 外侧 30° 偏航避光轴心
                    # 2. 自动化生成 GB/T 工业标准尺寸链与对齐标注
                    dim1 = acad.ModelSpace.AddDimAligned(p_start, p_end, text_pos)
                    dim1.TextOverride = "8000 [极限展开跨度]"
                    dim1.ToleranceDisplay = 1 # 严格标注工业级机械配合公差
                    ```
                  ]
                ],
                
                // 三自原则自述总结
                rect(
                  width: 100%,
                  fill: white,
                  radius: 2pt,
                  stroke: 0.5pt + rgb("#C7D2FE"),
                  inset: (x: 5pt, y: 3.5pt)
                )[
                  #text(size: 7.5pt, fill: rgb("#312E81"), weight: "medium")[
                    *“三自原则”真实自证*：作者初三日常观察发现反光痛点并画出第一代草图，高一利用现代开源 Agent 与 MCP 数字化工具链，自主编写 Python 算法跨系统精确驱动 AutoCAD 绘制 4K 标准图纸，彻底消除手工制图误差。
                  ]
                ]
              )
            ]
          ]
        ]
      ]
    )
  ]
]
