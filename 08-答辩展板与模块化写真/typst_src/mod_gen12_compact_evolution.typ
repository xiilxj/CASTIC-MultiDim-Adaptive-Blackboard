// ==============================================================================
// MOD-GEN12-COMPACT: 第二区 代际拓扑演进与Z系列装配求解主流程 (三图紧凑连拼 + 白色流程图)
// 物理净尺寸: 860mm x 165mm (含四周 3mm 印刷出血位: 866mm x 171mm)
// 核心设计: 遵循用户命令“把右上角的三次迭代去掉不要留，把那一个流程图放在那里，用白色的”
// ==============================================================================

#set page(
  width: 866mm,
  height: 171mm,
  margin: (x: 3mm, y: 3mm), // 四周 3mm 印刷出血位
  fill: rgb("#0A111E")
)

#set text(
  font: ("Microsoft YaHei", "SimHei", "WenQuanYi Zen Hei"),
  fill: rgb("#F1F5F9")
)

// 净尺寸裁切外边框 (860mm x 165mm)
#rect(
  width: 860mm,
  height: 165mm,
  radius: 3pt,
  stroke: (paint: rgb("#1E293B"), thickness: 1.2pt),
  fill: rgb("#0B1320")
)[
  #pad(x: 7mm, top: 3.5mm, bottom: 3.5mm)[
    #grid(
      columns: (1fr),
      rows: (11mm, 1fr),
      row-gutter: 2.5mm,
      
      // ------------------------------------------------------------------------
      // 0. 区域标头
      // ------------------------------------------------------------------------
      rect(
        width: 100%,
        height: 11mm,
        radius: 2pt,
        fill: rgb("#131E30"),
        stroke: 0.8pt + rgb("#0284C7")
      )[
        #pad(x: 6mm)[
          #align(horizon)[
            #grid(
              columns: (1fr, auto),
              align: (left + horizon, right + horizon),
              
              stack(
                dir: ltr,
                spacing: 3.5mm,
                rect(width: 3.5pt, height: 10pt, fill: rgb("#38BDF8")),
                text(size: 10pt, weight: "bold", fill: white)[
                  【代际拓扑演进与端侧 VLM 赋能闭环】从传统黑板机构失效到端侧 VLM 光环境自适应逆向求解
                ],
                text(size: 7.5pt, weight: "medium", fill: rgb("#7DD3FC"))[
                  Generational Topology Evolution & Edge-VLM Adaptive Closed-Loop Kinematics (AutoCAD 4K & Algorithmic SVG)
                ]
              ),
              
              rect(
                stroke: 0.6pt + rgb("#38BDF8"),
                fill: rgb("#0284C7").transparentize(60%),
                radius: 2pt,
                inset: (x: 5pt, y: 2pt)
              )[
                #text(size: 7.2pt, weight: "bold", fill: rgb("#BAE6FD"))[端侧 Qwen2.5-VL 驱动 · 机构学逆向动力学闭环]
              ]
            )
          ]
        ]
      ],
      
      // ------------------------------------------------------------------------
      // 1. 主体：左侧 535mm 三图紧凑连拼 vs 右侧 305mm 白色装配流程图
      // ------------------------------------------------------------------------
      grid(
        columns: (535mm, 305mm),
        gutter: 5mm,
        
        // ======================================================================
        // 左侧：三张 CAD 图纸无缝连拼（市面推拉 + 第一代悬臂 + 第二代双滑轨）
        // ======================================================================
        rect(
          width: 100%,
          height: 151mm,
          radius: 2pt,
          stroke: 1pt + rgb("#1E3A5F"),
          fill: rgb("#060C16")
        )[
          #pad(x: 2mm, y: 2mm)[
            #grid(
              columns: (173mm, 173mm, 173mm),
              gutter: 2.5mm,
              
              // ----------------------------------------------------------------
              // 图纸 1：市面主流双导轨推拉黑板 (4000mm)
              // ----------------------------------------------------------------
              rect(
                width: 100%,
                height: 147mm,
                radius: 1.5pt,
                stroke: 0.8pt + rgb("#EF4444").transparentize(40%),
                fill: rgb("#030712")
              )[
                #stack(
                  dir: ttb,
                  spacing: 0mm,
                  rect(
                    width: 100%,
                    height: 7mm,
                    fill: rgb("#450A0A"),
                    stroke: none
                  )[
                    #align(center + horizon)[
                      #text(size: 6.8pt, weight: "bold", fill: rgb("#FCA5A5"))[
                        基准对照 · 市面主流推拉黑板 (4000mm)
                      ]
                    ]
                  ],
                  rect(
                    width: 100%,
                    height: 140mm,
                    stroke: none,
                    fill: none
                  )[
                    #image(
                      "../assets/cad_sheet_1.png",
                      width: 100%,
                      height: 100%,
                      fit: "contain"
                    )
                  ]
                )
              ],
              
              // ----------------------------------------------------------------
              // 图纸 2：第一代重力悬臂折叠 (初三 · 2025.09)
              // ----------------------------------------------------------------
              rect(
                width: 100%,
                height: 147mm,
                radius: 1.5pt,
                stroke: 0.8pt + rgb("#F59E0B").transparentize(40%),
                fill: rgb("#030712")
              )[
                #stack(
                  dir: ttb,
                  spacing: 0mm,
                  rect(
                    width: 100%,
                    height: 7mm,
                    fill: rgb("#451A03"),
                    stroke: none
                  )[
                    #align(center + horizon)[
                      #text(size: 6.8pt, weight: "bold", fill: rgb("#FCD34D"))[
                        第一代 · 重力悬臂折叠构型 (初三·2025.09)
                      ]
                    ]
                  ],
                  rect(
                    width: 100%,
                    height: 140mm,
                    stroke: none,
                    fill: none
                  )[
                    #image(
                      "../assets/cad_sheet_2.png",
                      width: 100%,
                      height: 100%,
                      fit: "contain"
                    )
                  ]
                )
              ],
              
              // ----------------------------------------------------------------
              // 图纸 3：第二代双滑轨推拉复合 (高一 · 2026.03)
              // ----------------------------------------------------------------
              rect(
                width: 100%,
                height: 147mm,
                radius: 1.5pt,
                stroke: 0.8pt + rgb("#EAB308").transparentize(40%),
                fill: rgb("#030712")
              )[
                #stack(
                  dir: ttb,
                  spacing: 0mm,
                  rect(
                    width: 100%,
                    height: 7mm,
                    fill: rgb("#422006"),
                    stroke: none
                  )[
                    #align(center + horizon)[
                      #text(size: 6.8pt, weight: "bold", fill: rgb("#FEF08A"))[
                        第二代 · 双滑轨推拉复合构型 (高一·2026.03)
                      ]
                    ]
                  ],
                  rect(
                    width: 100%,
                    height: 140mm,
                    stroke: none,
                    fill: none
                  )[
                    #image(
                      "../assets/cad_sheet_3.png",
                      width: 100%,
                      height: 100%,
                      fit: "contain"
                    )
                  ]
                )
              ]
            )
          ]
        ],
        
        // ======================================================================
        // 右侧：端侧 VLM 赋能教室光环境全闭环决策与机构学逆向求解流程图
        // ======================================================================
        rect(
          width: 100%,
          height: 151mm,
          radius: 2pt,
          stroke: 1.2pt + rgb("#0284C7"),
          fill: rgb("#FFFFFF")
        )[
          #pad(x: 2mm, y: 2mm)[
            #image(
              "../assets/05_vlm_empowered_classroom_optics_closed_loop_white.svg",
              width: 100%,
              height: 100%,
              fit: "contain"
            )
          ]
        ]
      )
    )
  ]
]
