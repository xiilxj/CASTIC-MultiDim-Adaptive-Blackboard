// ==============================================================================
// MOD-03_05: 左侧列代际拓扑演进一体化大长条 (Generational Evolution Pillar)
// 物理净尺寸: 270mm x 920mm (含四周 3mm 印刷出血位: 276mm x 926mm)
// 核心内容: 市面基线测绘 -> 第一代悬臂折叠 -> 第二代滑轨推拉 -> 第三代正交解耦
// 视觉基底: 工业工程明快纯白微冷灰底色，与 CAD 4K 白底工程图纸 100% 浑然一体
// 评审战略: 真实长线探究历史与试错机理实证，彻底粉碎代做质疑
// ==============================================================================

#set page(
  width: 276mm,
  height: 926mm,
  margin: (x: 3mm, y: 3mm), // 3mm 印刷出血位
  fill: rgb("#F8FAFC") // 极浅冷灰底色，CAD 图纸无缝融合
)

#set text(
  font: ("Microsoft YaHei", "SimHei"),
  fill: rgb("#0F172A")
)

// 净尺寸裁切外边框 (270mm x 920mm)
#rect(
  width: 270mm,
  height: 920mm,
  radius: 4pt,
  stroke: (paint: rgb("#CBD5E1"), thickness: 1.2pt),
  fill: rgb("#FFFFFF")
)[
  // 内衬淡雅工程网格装饰
  #pad(x: 7mm, top: 7mm, bottom: 6mm)[
    #grid(
      columns: (1fr),
      rows: (28mm, 195mm, 195mm, 195mm, 1fr),
      row-gutter: 0mm,
      
      // ------------------------------------------------------------------------
      // 0. 栏目主头部：代际拓扑演进总标题
      // ------------------------------------------------------------------------
      [
        #rect(
          width: 100%,
          height: 24mm,
          radius: 3pt,
          fill: gradient.linear(rgb("#0F294A"), rgb("#1E3E62"), angle: 90deg),
          stroke: (paint: rgb("#00E5FF").transparentize(60%), thickness: 0.8pt)
        )[
          #pad(x: 6mm, y: 0mm)[
            #align(horizon)[
              #grid(
                columns: (1fr, auto),
                align: (left + horizon, right + horizon),
                
                stack(
                  dir: ttb,
                  spacing: 1.5mm,
                  text(size: 15.5pt, weight: "black", fill: white, tracking: 1pt)[
                    【代际拓扑演进】四代机构学对比与研发轨迹
                  ],
                  text(size: 8.5pt, weight: "medium", fill: rgb("#7DD3FC"))[
                    Four-Generation Kinematic Topology & Long-term Evolution
                  ]
                ),
                
                rect(
                  stroke: 0.8pt + rgb("#D4AF37"),
                  fill: rgb("#06121E").transparentize(20%),
                  radius: 2pt,
                  inset: (x: 5pt, y: 3pt)
                )[
                  #text(size: 8pt, weight: "bold", fill: rgb("#FBD38D"))[三自原则实证]
                ]
              )
            ]
          ]
        ]
      ],
      
      // ------------------------------------------------------------------------
      // 1. 基线卡片：市面主流标准推拉黑板 (四大机械原罪)
      // ------------------------------------------------------------------------
      [
        #pad(top: 3mm, bottom: 2mm)[
          #rect(
            width: 100%,
            height: 190mm,
            radius: 3pt,
            stroke: (paint: rgb("#EF4444").transparentize(60%), thickness: 1pt),
            fill: rgb("#FEF2F2")
          )[
            #pad(x: 4mm, top: 3.5mm, bottom: 3mm)[
              #grid(
                columns: (1fr),
                rows: (18mm, 108mm, 1fr),
                row-gutter: 1.5mm,
                
                // 卡片标题栏
                grid(
                  columns: (auto, 1fr, auto),
                  align: (horizon, horizon, horizon),
                  gutter: 3mm,
                  circle(radius: 4pt, fill: rgb("#EF4444")),
                  text(size: 11pt, weight: "bold", fill: rgb("#991B1B"))[
                    基准测绘：市面主流推拉黑板 (4000mm)
                  ],
                  rect(fill: rgb("#EF4444"), radius: 2pt, inset: (x: 4pt, y: 2pt))[
                    #text(size: 7.5pt, weight: "bold", fill: white)[存在固有缺陷 ❌]
                  ]
                ),
                
                // CAD 图纸展示区
                rect(
                  width: 100%,
                  height: 108mm,
                  radius: 2pt,
                  stroke: 0.5pt + rgb("#DC2626").transparentize(70%),
                  fill: white
                )[
                  #image(
                    "../assets/cad_crop_1_traditional.png",
                    width: 100%,
                    height: 100%,
                    fit: "contain"
                  )
                ],
                
                // 痛点文字说明
                pad(top: 1mm)[
                  #text(size: 8.2pt, fill: rgb("#7F1D1D"), weight: "medium")[
                    *① 大屏板书割裂*：露显86寸大屏时板书面积折损50%；\
                    *② 轨道积灰卡死*：粉笔灰掉入下导轨致摩擦阻力剧增卡顿；\
                    *③ 固定单平面反光*：零避光自由度，靠窗座位常年反光致盲。
                  ]
                ]
              )
            ]
          ]
        ]
      ],
      
      // ------------------------------------------------------------------------
      // 2. 第一代卡片：重力悬臂外展折叠式 (初三萌生 · 挠度失效)
      // ------------------------------------------------------------------------
      [
        #pad(top: 1mm, bottom: 2mm)[
          #rect(
            width: 100%,
            height: 190mm,
            radius: 3pt,
            stroke: (paint: rgb("#F59E0B").transparentize(50%), thickness: 1pt),
            fill: rgb("#FFFBEB")
          )[
            #pad(x: 4mm, top: 3.5mm, bottom: 3mm)[
              #grid(
                columns: (1fr),
                rows: (18mm, 108mm, 1fr),
                row-gutter: 1.5mm,
                
                // 卡片标题栏
                grid(
                  columns: (auto, 1fr, auto),
                  align: (horizon, horizon, horizon),
                  gutter: 3mm,
                  circle(radius: 4pt, fill: rgb("#F59E0B")),
                  text(size: 11pt, weight: "bold", fill: rgb("#92400E"))[
                    第一代：重力悬臂外展折叠式 (初三萌生)
                  ],
                  rect(fill: rgb("#F59E0B"), radius: 2pt, inset: (x: 4pt, y: 2pt))[
                    #text(size: 7.5pt, weight: "bold", fill: white)[挠度超限下垂 ❌]
                  ]
                ),
                
                // CAD 图纸展示区
                rect(
                  width: 100%,
                  height: 108mm,
                  radius: 2pt,
                  stroke: 0.5pt + rgb("#D97706").transparentize(70%),
                  fill: white
                )[
                  #image(
                    "../assets/cad_crop_2_gen1.png",
                    width: 100%,
                    height: 100%,
                    fit: "contain"
                  )
                ],
                
                // 试错机理说明
                pad(top: 1mm)[
                  #text(size: 8.2pt, fill: rgb("#78350F"), weight: "medium")[
                    *机构构想*：大屏两侧立板，外侧铰接1000mm副板向外展出；\
                    *失效机理*：*悬臂梁端部重力挠度过大（实测 $delta approx 18$mm）*，铰链受巨大剪切力矩拉扯塑性形变，长期使用下垂刮擦卡死。
                  ]
                ]
              )
            ]
          ]
        ]
      ],
      
      // ------------------------------------------------------------------------
      // 3. 第二代卡片：双滑轨水平推拉+单侧旋转式 (高一初期 · 运动副干涉)
      // ------------------------------------------------------------------------
      [
        #pad(top: 1mm, bottom: 2mm)[
          #rect(
            width: 100%,
            height: 190mm,
            radius: 3pt,
            stroke: (paint: rgb("#F97316").transparentize(50%), thickness: 1pt),
            fill: rgb("#FFF7ED")
          )[
            #pad(x: 4mm, top: 3.5mm, bottom: 3mm)[
              #grid(
                columns: (1fr),
                rows: (18mm, 108mm, 1fr),
                row-gutter: 1.5mm,
                
                // 卡片标题栏
                grid(
                  columns: (auto, 1fr, auto),
                  align: (horizon, horizon, horizon),
                  gutter: 3mm,
                  circle(radius: 4pt, fill: rgb("#F97316")),
                  text(size: 11pt, weight: "bold", fill: rgb("#9A3412"))[
                    第二代：双滑轨推拉复合旋转式 (高一初期)
                  ],
                  rect(fill: rgb("#EA580C"), radius: 2pt, inset: (x: 4pt, y: 2pt))[
                    #text(size: 7.5pt, weight: "bold", fill: white)[运动副干涉 ❌]
                  ]
                ),
                
                // CAD 图纸展示区
                rect(
                  width: 100%,
                  height: 108mm,
                  radius: 2pt,
                  stroke: 0.5pt + rgb("#EA580C").transparentize(70%),
                  fill: white
                )[
                  #image(
                    "../assets/cad_crop_3_gen2.png",
                    width: 100%,
                    height: 100%,
                    fit: "contain"
                  )
                ],
                
                // 试错机理说明
                pad(top: 1mm)[
                  #text(size: 8.2pt, fill: rgb("#7C2D12"), weight: "medium")[
                    *机构构想*：引入双滑轨支撑平移，端部配置偏航旋转副；\
                    *失效机理*：*滑动副与转动副同轴空间干涉*，运动包络死锁，平移极限时碰撞框架，大屏产生200mm机械盲区无法全封屏。
                  ]
                ]
              )
            ]
          ]
        ]
      ],
      
      // ------------------------------------------------------------------------
      // 4. 第四代卡片：第三代对角线正交解耦与参数化制图 (高一成熟攻坚突破)
      // ------------------------------------------------------------------------
      [
        #pad(top: 1mm)[
          #rect(
            width: 100%,
            height: 270mm,
            radius: 3pt,
            stroke: (paint: rgb("#059669").transparentize(40%), thickness: 1.5pt),
            fill: rgb("#ECFDF5")
          )[
            #pad(x: 4mm, top: 3.5mm, bottom: 3mm)[
              #grid(
                columns: (1fr),
                rows: (18mm, 150mm, 1fr),
                row-gutter: 2mm,
                
                // 卡片标题栏
                grid(
                  columns: (auto, 1fr, auto),
                  align: (horizon, horizon, horizon),
                  gutter: 3mm,
                  circle(radius: 4pt, fill: rgb("#10B981")),
                  text(size: 11.5pt, weight: "bold", fill: rgb("#065F46"))[
                    第三代：对角线正交解耦终极构型 (高一攻坚)
                  ],
                  rect(fill: rgb("#059669"), radius: 2pt, inset: (x: 5pt, y: 2.5pt))[
                    #text(size: 8pt, weight: "bold", fill: white)[空间拓扑解耦突破 ✅]
                  ]
                ),
                
                // CAD 图纸展示区 (大尺寸展示完整 GB/T 工业图框与机构图)
                rect(
                  width: 100%,
                  height: 150mm,
                  radius: 2pt,
                  stroke: 0.8pt + rgb("#059669").transparentize(60%),
                  fill: white
                )[
                  #image(
                    "../assets/cad_crop_4_gen3.png",
                    width: 100%,
                    height: 100%,
                    fit: "contain"
                  )
                ],
                
                // 终极突破说明与指向中列箭头
                grid(
                  columns: (1fr),
                  rows: (auto, auto),
                  row-gutter: 2mm,
                  
                  text(size: 8.5pt, fill: rgb("#064E3B"), weight: "bold")[
                    *① 对角线正交解耦*：内侧翻折 180° + 外侧侧滑偏航，铰链轴向跨度隔离 $Delta X = 1000$mm，零干涉实现 4000~8000mm 自由拓展；\
                    *② 双横梁自洁伸缩*：$Phi 28 times 2.5$mm SUS304 高刚性套杆集成刮灰条；\
                    *③ 基于 cad-mcp 参数化智能制图*：WSL2 算法跨环境驱动 Windows AutoCAD 2026，工业级尺寸公差自主实测实画。
                  ],
                  
                  rect(
                    width: 100%,
                    fill: rgb("#064E3B"),
                    radius: 2pt,
                    inset: (x: 4pt, y: 3pt)
                  )[
                    #align(center)[
                      #text(size: 8.5pt, weight: "bold", fill: rgb("#34D399"))[
                        ▶ 核心机构总装 4K 实体渲染与四大工况动力学详见中间 C 位
                      ]
                    ]
                  ]
                )
              )
            ]
          ]
        ]
      ]
    )
  ]
]
