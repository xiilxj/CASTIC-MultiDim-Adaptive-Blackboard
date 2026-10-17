// ==============================================================================
// MOD-03: 左大栏【纯工程硬核蓝图风】四代CAD机构学拓扑演进实证 (420x920mm)
// 物理净尺寸: 420mm x 920mm (含四周 3mm 印刷出血位: 426mm x 926mm)
// 美学风格: 彻底剔除生活照片与花哨色块，纯粹高冷工业工程制图规范
// 核心特征: 400mm 宽幅超大图纸完整舒展呈现，GB/T图框与尺寸链纤毫毕现
// ==============================================================================

#set page(
  width: 426mm,
  height: 926mm,
  margin: (x: 3mm, y: 3mm), // 3mm 出血位
  fill: rgb("#F8FAFC") // 极简纯净工程白底
)

#set text(
  font: ("Microsoft YaHei", "SimHei"),
  fill: rgb("#0F172A")
)

// 净尺寸裁切外边框 (420mm x 920mm)
#rect(
  width: 420mm,
  height: 920mm,
  radius: 3pt,
  stroke: (paint: rgb("#0F294A"), thickness: 1.5pt),
  fill: rgb("#FFFFFF")
)[
  #pad(x: 8mm, top: 7mm, bottom: 6mm)[
    #grid(
      columns: (1fr),
      rows: (22mm, 200mm, 200mm, 200mm, 1fr),
      row-gutter: 0mm,
      
      // ------------------------------------------------------------------------
      // 0. 左大栏标头：纯正工业工程标题栏
      // ------------------------------------------------------------------------
      [
        #rect(
          width: 100%,
          height: 18mm,
          radius: 2pt,
          fill: rgb("#0A192F"),
          stroke: 1pt + rgb("#00E5FF")
        )[
          #pad(x: 6mm)[
            #align(horizon)[
              #grid(
                columns: (1fr, auto),
                align: (left + horizon, right + horizon),
                
                stack(
                  dir: ttb,
                  spacing: 1.5mm,
                  text(size: 14pt, weight: "black", fill: white, tracking: 1.2pt)[
                    【机构学拓扑演进】四代 AutoCAD 标准工程图纸与机理实证
                  ],
                  text(size: 8.5pt, weight: "medium", fill: rgb("#38BDF8"))[
                    Four-Generation Kinematic Topology & AutoCAD Engineering Parametric Blueprints
                  ]
                ),
                
                rect(
                  stroke: 0.8pt + rgb("#D4AF37"),
                  fill: rgb("#06121E").transparentize(10%),
                  radius: 2pt,
                  inset: (x: 6pt, y: 3pt)
                )[
                  #text(size: 8.5pt, weight: "bold", fill: rgb("#FBD38D"))[自主工程制图 · 三自原则]
                ]
              )
            ]
          ]
        ]
      ],
      
      // ------------------------------------------------------------------------
      // 1. 基准图纸：市面主流标准双推拉黑板 (4000mm 跨度基线测绘)
      // ------------------------------------------------------------------------
      [
        #pad(top: 3mm, bottom: 2mm)[
          #rect(
            width: 100%,
            height: 195mm,
            radius: 2pt,
            stroke: 0.8pt + rgb("#94A3B8"),
            fill: rgb("#F8FAFC")
          )[
            #pad(x: 5mm, top: 3.5mm, bottom: 3mm)[
              #grid(
                columns: (1fr),
                rows: (14mm, 150mm, 1fr),
                row-gutter: 1.5mm,
                
                grid(
                  columns: (auto, 1fr, auto),
                  align: (horizon, horizon, horizon),
                  gutter: 3mm,
                  rect(width: 4pt, height: 12pt, fill: rgb("#64748B")),
                  text(size: 10.5pt, weight: "bold", fill: rgb("#1E293B"))[
                    [基线工程图] 市面标准双导轨推拉黑板 (4000mm) · 传统构型机理缺陷测绘
                  ],
                  text(size: 8pt, fill: rgb("#DC2626"), weight: "bold")[
                    自由度 F = 2 · 存在空间与避光死区
                  ]
                ),
                
                // 超大图纸展示区 (宽幅 395mm 大图直接舒展展开！)
                rect(
                  width: 100%,
                  height: 150mm,
                  radius: 1.5pt,
                  stroke: 0.5pt + rgb("#CBD5E1"),
                  fill: white
                )[
                  #image(
                    "../assets/cad_sheet_1.png",
                    width: 100%,
                    height: 100%,
                    fit: "contain"
                  )
                ],
                
                // 硬核技术参数与缺陷力学剖析
                text(size: 7.5pt, fill: rgb("#334155"), weight: "medium")[
                  *测绘工程参数*：跨度 4000mm，中置 86 寸液晶大屏（1980mm），双扇 1000mm 滑动黑板；\
                  *机械缺陷机理*：①推开黑板露大屏时有效板书面积折损 50%；②下导轨槽呈敞开式，粉笔灰沉积致阻力系数 $mu$ 飙升 $280\%$ 频繁卡顿；③板面共面固定，避光自由度 $F_{"glare"} = 0$。
                ]
              )
            ]
          ]
        ]
      ],
      
      // ------------------------------------------------------------------------
      // 2. 第一代图纸：重力悬臂外展折叠式 (初三萌生 · 挠度失效分析)
      // ------------------------------------------------------------------------
      [
        #pad(top: 1mm, bottom: 2mm)[
          #rect(
            width: 100%,
            height: 195mm,
            radius: 2pt,
            stroke: 0.8pt + rgb("#94A3B8"),
            fill: rgb("#F8FAFC")
          )[
            #pad(x: 5mm, top: 3.5mm, bottom: 3mm)[
              #grid(
                columns: (1fr),
                rows: (14mm, 150mm, 1fr),
                row-gutter: 1.5mm,
                
                grid(
                  columns: (auto, 1fr, auto),
                  align: (horizon, horizon, horizon),
                  gutter: 3mm,
                  rect(width: 4pt, height: 12pt, fill: rgb("#D97706")),
                  text(size: 10.5pt, weight: "bold", fill: rgb("#1E293B"))[
                    [第一代构型] 重力悬臂外展折叠式多媒体黑板 (初三萌生 · 2025.09)
                  ],
                  text(size: 8pt, fill: rgb("#D97706"), weight: "bold")[
                    悬臂梁端部重力挠度超限 (delta = 18mm) ❌
                  ]
                ),
                
                rect(
                  width: 100%,
                  height: 150mm,
                  radius: 1.5pt,
                  stroke: 0.5pt + rgb("#CBD5E1"),
                  fill: white
                )[
                  #image(
                    "../assets/cad_sheet_2.png",
                    width: 100%,
                    height: 100%,
                    fit: "contain"
                  )
                ],
                
                text(size: 7.5pt, fill: rgb("#334155"), weight: "medium")[
                  *构想机制*：在两侧设立 1000mm 主板，外侧通过阻尼自锁铰链外展 1000mm 副板拓展板书；\
                  *失效力学推导*：外展后黑板呈大跨度外伸悬臂梁受力，端部挠度 $delta = (q L^4)/(8 E I) + (F L^3)/(3 E I) approx 18.2"mm"$；铰链承受巨大剪切弯矩 $M = 360"N"dot"m"$，长期使用轴系塑性扭曲下垂卡死。
                ]
              )
            ]
          ]
        ]
      ],
      
      // ------------------------------------------------------------------------
      // 3. 第二代图纸：双滑轨水平推拉+单侧旋转式 (高一初期 · 运动副干涉分析)
      // ------------------------------------------------------------------------
      [
        #pad(top: 1mm, bottom: 2mm)[
          #rect(
            width: 100%,
            height: 195mm,
            radius: 2pt,
            stroke: 0.8pt + rgb("#94A3B8"),
            fill: rgb("#F8FAFC")
          )[
            #pad(x: 5mm, top: 3.5mm, bottom: 3mm)[
              #grid(
                columns: (1fr),
                rows: (14mm, 150mm, 1fr),
                row-gutter: 1.5mm,
                
                grid(
                  columns: (auto, 1fr, auto),
                  align: (horizon, horizon, horizon),
                  gutter: 3mm,
                  rect(width: 4pt, height: 12pt, fill: rgb("#EA580C")),
                  text(size: 10.5pt, weight: "bold", fill: rgb("#1E293B"))[
                    [第二代构型] 双滑轨推拉复合自洁防眩光黑板系统 (高一初期 · 2026.03)
                  ],
                  text(size: 8pt, fill: rgb("#EA580C"), weight: "bold")[
                    滑动副与转动副同轴空间干涉死锁 ❌
                  ]
                ),
                
                rect(
                  width: 100%,
                  height: 150mm,
                  radius: 1.5pt,
                  stroke: 0.5pt + rgb("#CBD5E1"),
                  fill: white
                )[
                  #image(
                    "../assets/cad_sheet_3.png",
                    width: 100%,
                    height: 100%,
                    fit: "contain"
                  )
                ],
                
                text(size: 7.5pt, fill: rgb("#334155"), weight: "medium")[
                  *构想机制*：引入闭环双横梁消除悬臂受力，端部滑块串联偏航转动副做多维避光；\
                  *干涉失效机理*：滑动移动副 $P$ 与偏航转动副 $R$ 空间同轴布局，极限平移时端板与主边框产生刚性干涉碰撞，导致内侧出现 200mm 机械死区，无法实现 86 寸大屏 100% 完整全覆盖。
                ]
              )
            ]
          ]
        ]
      ],
      
      // ------------------------------------------------------------------------
      // 4. 第三代图纸：对角线正交解耦全系统工程总装图 (高一成熟攻坚突破)
      // ------------------------------------------------------------------------
      [
        #pad(top: 1mm)[
          #rect(
            width: 100%,
            height: 250mm,
            radius: 2pt,
            stroke: 1.2pt + rgb("#059669"),
            fill: rgb("#F0FDF4")
          )[
            #pad(x: 5mm, top: 3.5mm, bottom: 3mm)[
              #grid(
                columns: (1fr),
                rows: (14mm, 180mm, 1fr),
                row-gutter: 2mm,
                
                grid(
                  columns: (auto, 1fr, auto),
                  align: (horizon, horizon, horizon),
                  gutter: 3mm,
                  rect(width: 4pt, height: 12pt, fill: rgb("#059669")),
                  text(size: 11pt, weight: "bold", fill: rgb("#065F46"))[
                    [第三代终极构型] 对角线正交解耦全覆盖与自洁侧滑系统 (高一攻坚 · 2026.10)
                  ],
                  text(size: 8.5pt, fill: rgb("#059669"), weight: "bold")[
                    对角线空间解耦 · 自由度 F = 4 完美闭环 ✅
                  ]
                ),
                
                // 180mm 超大图纸展示完整 GB/T 工业图框与 4000~6000mm 标注
                rect(
                  width: 100%,
                  height: 180mm,
                  radius: 1.5pt,
                  stroke: 0.8pt + rgb("#059669"),
                  fill: white
                )[
                  #image(
                    "../assets/cad_sheet_4.png",
                    width: 100%,
                    height: 100%,
                    fit: "contain"
                  )
                ],
                
                // 终极机构学突破参数
                text(size: 7.8pt, fill: rgb("#064E3B"), weight: "bold")[
                  *正交解耦数学模型*：内侧展开铰链轴（$X_1 = plus.minus 1000$mm）与外侧偏航铰链轴（$X_2 = plus.minus 2000$mm，侧滑时 $plus.minus 3000$mm）呈对角线分布，空间跨度隔离 $Delta X = 1000$mm，两组运动副三维正交，零机械干涉；\
                  *自洁伸缩导轨*：双横梁 $Phi 28 times 2.5$mm SUS304 高刚性内套杆，集成往复聚氨酯刮灰条；跨平台 Python 跨系统驱动 AutoCAD 2026 精确出图。
                ]
              )
            ]
          ]
        ]
      ]
    )
  ]
]
