// ==============================================================================
// MOD-GEN3-HERO: 第三区 【全场核心主角 C位】第三代终极总装工业蓝图与四大工况大图 (580mm高)
// 物理净尺寸: 860mm x 580mm (含四周 3mm 印刷出血位: 866mm x 586mm)
// 设计哲学: 依用户命令：
//           1. 裁掉蓝图底部3个多余小卡片，空间完全释放给 AutoCAD 蓝图顶格放大！
//           2. 右侧四大工况图不改结构，直接放大充满，裁切无用灰边，黑板饱满居中！
// ==============================================================================

#set page(
  width: 866mm,
  height: 586mm,
  margin: (x: 3mm, y: 3mm), // 3mm 印刷出血位
  fill: rgb("#F8FAFC") // 极简纯净工程白底
)

#set text(
  font: ("Microsoft YaHei", "SimHei"),
  fill: rgb("#0F172A")
)

// 净尺寸裁切外边框 (860mm x 580mm)
#rect(
  width: 860mm,
  height: 580mm,
  radius: 3pt,
  stroke: 1.2pt + rgb("#059669"),
  fill: white
)[
  #pad(x: 6mm, top: 4.5mm, bottom: 4.5mm)[
    #grid(
      columns: (1fr),
      rows: (12mm, 1fr),
      row-gutter: 3mm,
      
      // ------------------------------------------------------------------------
      // 模块深钛青工程大标题
      // ------------------------------------------------------------------------
      rect(
        width: 100%,
        height: 12mm,
        radius: 2pt,
        fill: rgb("#064E3B"),
        stroke: 0.8pt + rgb("#10B981")
      )[
        #pad(x: 5mm)[
          #align(horizon)[
            #grid(
              columns: (1fr, auto),
              align: (left + horizon, right + horizon),
              
              stack(
                dir: ltr,
                spacing: 3mm,
                text(size: 10.5pt, weight: "black", fill: white, tracking: 0.8pt)[
                  【全场核心重点 · 第三代机构学总装】对角线正交解耦全系统工业尺寸链与数字孪生实证
                ],
                text(size: 7.8pt, weight: "medium", fill: rgb("#6EE7B7"))[
                  Orthogonal Diagonal Decoupling Master Assembly · AutoCAD 4K Blueprint vs. Z-Series 4-State 4K Twin
                ]
              ),
              
              rect(
                stroke: 0.8pt + rgb("#34D399"),
                fill: rgb("#065F46"),
                radius: 2pt,
                inset: (x: 5pt, y: 2pt)
              )[
                #text(size: 7.2pt, weight: "bold", fill: rgb("#A7F3D0"))[自由度 F = 4 · 4000~6000mm 空间正交解耦终极构型]
              ]
            )
          ]
        ]
      ],
      
      // ------------------------------------------------------------------------
      // 主体结构：左侧 535mm AutoCAD 超清巨图【绝对主角】 vs 右侧 305mm 四大工况图
      // ------------------------------------------------------------------------
      grid(
        columns: (535mm, 305mm),
        gutter: 6mm,
        
        // ======================================================================
        // 左侧：第三代核心蓝图 (彻底裁掉底部3个小框，空间完全还给蓝图！)
        // ======================================================================
        rect(
          width: 100%,
          height: 550mm,
          radius: 2pt,
          stroke: 1pt + rgb("#0284C7"),
          fill: rgb("#060C16")
        )[
          #pad(x: 4mm, top: 3.5mm, bottom: 3.5mm)[
            #grid(
              columns: (1fr),
              rows: (11mm, 1fr),
              row-gutter: 2.5mm,
              
              // 蓝图标头
              grid(
                columns: (auto, 1fr, auto),
                align: (horizon, horizon, horizon),
                gutter: 3mm,
                rect(width: 3.5pt, height: 11pt, fill: rgb("#38BDF8")),
                text(size: 9.5pt, weight: "bold", fill: rgb("#E0F2FE"))[
                  第三代多维叠合翻转全覆盖黑板系统 AutoCAD 1:1 标准工程装配蓝图 (5800mm x 4000mm)
                ],
                text(size: 7.5pt, fill: rgb("#38BDF8"), weight: "bold")[
                  dwg图纸像素级渲染 · 毫米级尺寸链对齐
                ]
              ),
              
              // 极度拉大的巨幅蓝图图像 (顶格充满 532mm)
              rect(
                width: 100%,
                height: 528mm,
                radius: 1.5pt,
                stroke: 0.6pt + rgb("#0284C7"),
                fill: rgb("#030712")
              )[
                #image(
                  "../assets/cad_sheet_4.png",
                  width: 100%,
                  height: 100%,
                  fit: "contain"
                )
              ]
            )
          ]
        ],
        
        // ======================================================================
        // 右侧：四大工况图——结构不改，图片饱满放大，消除多余灰边！
        // ======================================================================
        rect(
          width: 100%,
          height: 550mm,
          radius: 2pt,
          stroke: 1pt + rgb("#059669"),
          fill: rgb("#F0FDF4")
        )[
          #pad(x: 3mm, top: 3mm, bottom: 3mm)[
            #grid(
              columns: (1fr),
              rows: (132mm, 132mm, 132mm, 132mm),
              row-gutter: 2.5mm,
              
              // ----------------------------------------------------------------
              // 工况 1：Z1 全覆盖封屏形态 (4000mm)
              // ----------------------------------------------------------------
              rect(
                width: 100%,
                height: 132mm,
                radius: 1.5pt,
                stroke: 0.7pt + rgb("#059669"),
                fill: rgb("#060C16")
              )[
                #stack(
                  dir: ttb,
                  spacing: 0mm,
                  rect(
                    width: 100%,
                    height: 7.5mm,
                    fill: rgb("#064E3B"),
                    stroke: none
                  )[
                    #pad(x: 3mm)[
                      #align(horizon)[
                        #grid(
                          columns: (1fr, auto),
                          text(size: 8.2pt, weight: "bold", fill: rgb("#A7F3D0"))[
                            【工况一】全覆盖封屏形态 (4000mm)
                          ],
                          text(size: 7pt, fill: rgb("#6EE7B7"), weight: "bold")[大屏完全遮蔽 · 纯书写保护态]
                        )
                      ]
                    ]
                  ],
                  // 图片饱满放大，黑板居中突出 (净高度扩展至 114.5mm)
                  rect(
                    width: 100%,
                    height: 114.5mm,
                    stroke: none,
                    fill: rgb("#0A0F1D")
                  )[
                    #image(
                      "../../05-三维建模与Blender渲染/Z系列/Z1_工况一_全覆盖封屏形态_4000mm_4K.png",
                      width: 100%,
                      height: 100%,
                      fit: "cover"
                    )
                  ],
                  rect(
                    width: 100%,
                    height: 10mm,
                    fill: rgb("#042F2E"),
                    stroke: none
                  )[
                    #pad(x: 3mm)[
                      #align(horizon)[
                        #text(size: 7.5pt, fill: rgb("#CCFBF1"))[
                          *状态特征*：主副黑板双层贴合完全遮蔽中置 86 寸智能大屏，物理阻隔外力碰撞；提供 4000mm 连贯纯黑板书写工作面。
                        ]
                      ]
                    ]
                  ]
                )
              ],
              
              // ----------------------------------------------------------------
              // 工况 2：Z2 常态大屏露显双层叠合形态 (4000mm)
              // ----------------------------------------------------------------
              rect(
                width: 100%,
                height: 132mm,
                radius: 1.5pt,
                stroke: 0.7pt + rgb("#0284C7"),
                fill: rgb("#060C16")
              )[
                #stack(
                  dir: ttb,
                  spacing: 0mm,
                  rect(
                    width: 100%,
                    height: 7.5mm,
                    fill: rgb("#0C4A6E"),
                    stroke: none
                  )[
                    #pad(x: 3mm)[
                      #align(horizon)[
                        #grid(
                          columns: (1fr, auto),
                          text(size: 8.2pt, weight: "bold", fill: rgb("#BAE6FD"))[
                            【工况二】常态大屏露显双层叠合形态 (4000mm)
                          ],
                          text(size: 7pt, fill: rgb("#7DD3FC"), weight: "bold")[大屏100%露显 · 教学交互态]
                        )
                      ]
                    ]
                  ],
                  rect(
                    width: 100%,
                    height: 114.5mm,
                    stroke: none,
                    fill: rgb("#0A0F1D")
                  )[
                    #image(
                      "../../05-三维建模与Blender渲染/Z系列/Z2_工况二_常态大屏露显双层叠合形态_4000mm_4K.png",
                      width: 100%,
                      height: 100%,
                      fit: "cover"
                    )
                  ],
                  rect(
                    width: 100%,
                    height: 10mm,
                    fill: rgb("#082F49"),
                    stroke: none
                  )[
                    #pad(x: 3mm)[
                      #align(horizon)[
                        #text(size: 7.5pt, fill: rgb("#E0F2FE"))[
                          *状态特征*：主板向两侧平推叠合，中置 86 寸液晶屏幕 100% 无遮挡露显；贴合厚度仅 26mm，两侧提供即时补充板书面。
                        ]
                      ]
                    ]
                  ]
                )
              ],
              
              // ----------------------------------------------------------------
              // 工况 3-1：Z3_1 平移侧滑极限展开与避光偏航形态 (6000mm)
              // ----------------------------------------------------------------
              rect(
                width: 100%,
                height: 132mm,
                radius: 1.5pt,
                stroke: 0.7pt + rgb("#D97706"),
                fill: rgb("#060C16")
              )[
                #stack(
                  dir: ttb,
                  spacing: 0mm,
                  rect(
                    width: 100%,
                    height: 7.5mm,
                    fill: rgb("#78350F"),
                    stroke: none
                  )[
                    #pad(x: 3mm)[
                      #align(horizon)[
                        #grid(
                          columns: (1fr, auto),
                          text(size: 8.2pt, weight: "bold", fill: rgb("#FDE68A"))[
                            【工况三】两翼侧滑外展与避光偏航形态 (8000mm)
                          ],
                          text(size: 7pt, fill: rgb("#FCD34D"), weight: "bold")[两翼展出4000mm · 核心受光板微偏避光]
                        )
                      ]
                    ]
                  ],
                  rect(
                    width: 100%,
                    height: 114.5mm,
                    stroke: none,
                    fill: rgb("#0A0F1D")
                  )[
                    #image(
                      "../assets/vi7_exported_stage3_yaw.png",
                      width: 100%,
                      height: 100%,
                      fit: "contain"
                    )
                  ],
                  rect(
                    width: 100%,
                    height: 10mm,
                    fill: rgb("#451A03"),
                    stroke: none
                  )[
                    #pad(x: 3mm)[
                      #align(horizon)[
                        #text(size: 7.5pt, fill: rgb("#FEF3C7"))[
                          *状态特征*：左右两翼各2块衍生板沿双横梁套杆外滑，总跨度达8000mm！核心受光板微偏4.5°将侧窗眩光折射至天花板无人区。
                        ]
                      ]
                    ]
                  ]
                )
              ],
              
              // ----------------------------------------------------------------
              // 工况 4：Z3_2 极限全景全展平铺回填形态 (8000mm)
              // ----------------------------------------------------------------
              rect(
                width: 100%,
                height: 132mm,
                radius: 1.5pt,
                stroke: 0.7pt + rgb("#7C3AED"),
                fill: rgb("#060C16")
              )[
                #stack(
                  dir: ttb,
                  spacing: 0mm,
                  rect(
                    width: 100%,
                    height: 7.5mm,
                    fill: rgb("#4C1D95"),
                    stroke: none
                  )[
                    #pad(x: 3mm)[
                      #align(horizon)[
                        #grid(
                          columns: (1fr, auto),
                          text(size: 8.2pt, weight: "bold", fill: rgb("#DDD6FE"))[
                            【工况四】两翼完全平铺回填超长全展形态 (8000mm)
                          ],
                          text(size: 7pt, fill: rgb("#C4B5FD"), weight: "bold")[8米全景纯平巨幕 · 彻底释放复杂理科板书]
                        )
                      ]
                    ]
                  ],
                  rect(
                    width: 100%,
                    height: 114.5mm,
                    stroke: none,
                    fill: rgb("#0A0F1D")
                  )[
                    #image(
                      "../assets/vi7_exported_stage4_full.png",
                      width: 100%,
                      height: 100%,
                      fit: "contain"
                    )
                  ],
                  rect(
                    width: 100%,
                    height: 10mm,
                    fill: rgb("#2E1065"),
                    stroke: none
                  )[
                    #pad(x: 3mm)[
                      #align(horizon)[
                        #text(size: 7.5pt, fill: rgb("#F5F3FF"))[
                          *状态特征*：两翼衍生板完全展平回填，形成左衍生2m+左固定1m+中置大屏2m+右固定1m+右衍生2m的8000mm纯平巨幕，板书面积成倍扩充。
                        ]
                      ]
                    ]
                  ]
                )
              ]
            )
          ]
        ]
      )
    )
  ]
]
