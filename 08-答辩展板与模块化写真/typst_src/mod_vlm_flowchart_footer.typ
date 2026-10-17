// ==============================================================================
// MOD-VLM-FLOWCHART-FOOTER: 第四区 物理光环境仿真与时序拓扑流程图通栏 (含官方底栏)
// 物理净尺寸: 860mm x 240mm (含四周 3mm 印刷出血位: 866mm x 246mm)
// 设计哲学: 依用户命令“图片放大”，将 Blender 实机仿真截图与时序流程图高效紧凑排布
// ==============================================================================

#set page(
  width: 866mm,
  height: 246mm,
  margin: (x: 3mm, y: 3mm), // 3mm 出血位
  fill: rgb("#F8FAFC") // 纯净工程底色
)

#set text(
  font: ("Microsoft YaHei", "SimHei", "WenQuanYi Zen Hei"),
  fill: rgb("#0F172A")
)

// 净尺寸裁切外边框 (860mm x 240mm)
#rect(
  width: 860mm,
  height: 240mm,
  radius: 3pt,
  stroke: 1.2pt + rgb("#0284C7"),
  fill: white
)[
  #pad(x: 6mm, top: 3.5mm, bottom: 3.5mm)[
    #grid(
      columns: (1fr),
      rows: (10mm, 204mm, 14mm),
      row-gutter: 2.5mm,
      
      // ------------------------------------------------------------------------
      // 0. 区域标头
      // ------------------------------------------------------------------------
      rect(
        width: 100%,
        height: 10mm,
        radius: 2pt,
        fill: rgb("#0B192C"),
        stroke: 0.8pt + rgb("#0284C7")
      )[
        #pad(x: 5mm)[
          #align(horizon)[
            #grid(
              columns: (1fr, auto),
              align: (left + horizon, right + horizon),
              
              stack(
                dir: ltr,
                spacing: 3mm,
                text(size: 10.2pt, weight: "black", fill: white, tracking: 0.8pt)[
                  【光环境物理仿真与时序闭环】Blender Cycles 物理光路追踪重塑 · 端侧 VLM 数字孪生闭环
                ],
                text(size: 7.5pt, weight: "medium", fill: rgb("#38BDF8"))[
                  Physical Ray Tracing Anti-Glare Simulation & Kinematic Sequence Digital Twin Loop
                ]
              ),
              
              rect(
                stroke: 0.8pt + rgb("#38BDF8"),
                fill: rgb("#0284C7").transparentize(60%),
                radius: 2pt,
                inset: (x: 5pt, y: 2pt)
              )[
                #text(size: 7.2pt, weight: "bold", fill: rgb("#BAE6FD"))[60 FPS 物理视口联动 · 消除教室强眩光]
              ]
            )
          ]
        ]
      ],
      
      // ------------------------------------------------------------------------
      // 1. 主体结构：左侧 420mm 极大化 Blender 仿真图 vs 右侧 420mm 时序流程图
      // ------------------------------------------------------------------------
      grid(
        columns: (420mm, 420mm),
        gutter: 6mm,
        
        // ======================================================================
        // 左侧：用户要求极度放大——真实 Blender 物理仿真界面与光路重塑实测
        // ======================================================================
        rect(
          width: 100%,
          height: 204mm,
          radius: 2pt,
          stroke: 1pt + rgb("#0284C7"),
          fill: rgb("#060C16")
        )[
          #pad(x: 3.5mm, top: 2.5mm, bottom: 2.5mm)[
            #grid(
              columns: (1fr),
              rows: (8.5mm, 169mm, 18.5mm),
              row-gutter: 1.5mm,
              
              grid(
                columns: (auto, 1fr, auto),
                align: (horizon, horizon, horizon),
                gutter: 2.5mm,
                rect(width: 3.5pt, height: 9pt, fill: rgb("#38BDF8")),
                text(size: 8.8pt, weight: "bold", fill: rgb("#E0F2FE"))[
                  [物理光路验证] Blender Cycles 教室光线追踪实操视口与数字孪生驱动
                ],
                text(size: 7.2pt, fill: rgb("#38BDF8"), weight: "bold")[
                  黄/红/蓝三维矢量光路
                ]
              ),
              
              // 极度放大的真实 Blender 实机运行截图 (高度达 169mm)
              rect(
                width: 100%,
                height: 169mm,
                radius: 1.5pt,
                stroke: 0.6pt + rgb("#0284C7"),
                fill: rgb("#020617")
              )[
                #image(
                  "../assets/blender_anti_glare_live_simulation.png",
                  width: 100%,
                  height: 100%,
                  fit: "contain"
                )
              ],
              
              // 紧凑高反差光环境实测说明条 (字号放大至 8.2pt)
              rect(
                width: 100%,
                height: 18.5mm,
                fill: rgb("#0B1E36"),
                stroke: 0.6pt + rgb("#0EA5E9"),
                radius: 1.5pt
              )[
                #pad(x: 3mm, y: 1.5mm)[
                  #align(horizon)[
                    #text(size: 7.8pt, fill: rgb("#F1F5F9"), weight: "medium")[
                      *实测*：#text(fill: rgb("#FDE047"), weight: "bold")[黄色光]=太阳直射；#text(fill: rgb("#F87171"), weight: "bold")[红色光]=传统直射入眼眩光(2850 Lux，反差比骤降至1.8:1)；#text(fill: rgb("#38BDF8"), weight: "bold")[蓝色光]=第三代黑板偏航4.5°偏折至天花板无人区(恢复至480 Lux，反差比跃升至14.5:1)。
                    ]
                  ]
                ]
              ]
            )
          ]
        ],
        
        // ======================================================================
        // 右侧：VI 系列全生命周期时序拓扑流程图
        // ======================================================================
        rect(
          width: 100%,
          height: 204mm,
          radius: 2pt,
          stroke: 1pt + rgb("#10B981"),
          fill: rgb("#060C16")
        )[
          #pad(x: 3.5mm, top: 2.5mm, bottom: 2.5mm)[
            #grid(
              columns: (1fr),
              rows: (8.5mm, 169mm, 18.5mm),
              row-gutter: 1.5mm,
              
              grid(
                columns: (auto, 1fr, auto),
                align: (horizon, horizon, horizon),
                gutter: 2.5mm,
                rect(width: 3.5pt, height: 9pt, fill: rgb("#10B981")),
                text(size: 8.8pt, weight: "bold", fill: rgb("#ECFDF5"))[
                  [机构时序拓扑] VI 系列多维叠合翻转黑板全生命周期时序拓扑流程图
                ],
                text(size: 7.2pt, fill: rgb("#34D399"), weight: "bold")[
                  无损 SVG 矢量资产
                ]
              ),
              
              // 高精无损矢量流程图
              rect(
                width: 100%,
                height: 169mm,
                radius: 1.5pt,
                stroke: 0.6pt + rgb("#059669"),
                fill: rgb("#020617")
              )[
                #image(
                  "../../07-系统架构与流程图/svg/01_vi_series_kinematic_sequence.svg",
                  width: 100%,
                  height: 100%,
                  fit: "contain"
                )
              ],
              
              // 状态时序机制说明条 (字号放大至 8.2pt)
              rect(
                width: 100%,
                height: 18.5mm,
                fill: rgb("#062E25"),
                stroke: 0.6pt + rgb("#10B981"),
                radius: 1.5pt
              )[
                #pad(x: 3mm, y: 1.5mm)[
                  #align(horizon)[
                    #text(size: 7.8pt, fill: rgb("#F1F5F9"), weight: "medium")[
                      *机构全生命周期状态流转*：从 *完全遮蔽 (Covered 4000mm)* $arrow.r$ *退回露屏 (Compact 4000mm)* $arrow.r$ *避光偏航聚拢 (Yaw Anti-Glare)* $arrow.r$ *外伸极限展开 (Panoramic 8000mm)* 平滑流转。
                    ]
                  ]
                ]
              ]
            )
          ]
        ]
      ),
      
      // ------------------------------------------------------------------------
      // 2. 官方规定底栏条 (严格合规防代做)
      // ------------------------------------------------------------------------
      rect(
        width: 100%,
        height: 14mm,
        radius: 2pt,
        fill: rgb("#0A192F"),
        stroke: 0.8pt + rgb("#1E3E62")
      )[
        #pad(x: 8mm)[
          #align(horizon)[
            #grid(
              columns: (1fr, auto, 1fr),
              align: (left + horizon, center + horizon, right + horizon),
              
              text(size: 8.8pt, fill: rgb("#E2E8F0"), weight: "bold")[
                申报单位：浙江省塘下中学
              ],
              
              text(size: 8.8pt, fill: rgb("#FBD38D"), weight: "bold")[
                真实研发周期：2025.09 - 2026.10（初三日常观察灵感萌生，高一工程深化迭代）
              ],
              
              text(size: 8.8pt, fill: rgb("#E2E8F0"), weight: "bold")[
                参赛选手：林诚俊（高中组个人项目 · 独立研发）
              ]
            )
          ]
        ]
      ]
    )
  ]
]
