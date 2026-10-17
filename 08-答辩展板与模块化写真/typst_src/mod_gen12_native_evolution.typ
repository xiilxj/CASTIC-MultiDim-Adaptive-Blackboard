// ==============================================================================
// MOD-GEN12: 前三代CAD原生几何咬合演进区 (Native Geometry Evolution Section)
// 物理净尺寸: 860mm x 310mm (含四周 3mm 印刷出血位: 866mm x 316mm)
// 美学与几何哲学: 彻底打破等大死框框！
// 左侧顺应市面图纸 1:1 正方形原生宽高比铺开 (宽 380mm x 高 310mm)
// 右侧顺应一代二代 1.47:1 宽屏原生宽高比上下叠放 (宽 460mm x 高 148mm 每个)
// 左右严密咬合，零无效白边，真实4K图纸尺寸链纤毫毕现！
// ==============================================================================

#set page(
  width: 866mm,
  height: 316mm,
  margin: (x: 3mm, y: 3mm), // 3mm 印刷出血位
  fill: rgb("#F8FAFC") // 极简纯净工程白底
)

#set text(
  font: ("Microsoft YaHei", "SimHei"),
  fill: rgb("#0F172A")
)

// 净尺寸裁切外边框 (860mm x 310mm)
#rect(
  width: 860mm,
  height: 310mm,
  radius: 3pt,
  stroke: (paint: rgb("#0F294A"), thickness: 1.2pt),
  fill: rgb("#FFFFFF")
)[
  #pad(x: 6mm, top: 5mm, bottom: 5mm)[
    #grid(
      columns: (1fr),
      rows: (16mm, 1fr),
      row-gutter: 3mm,
      
      // ------------------------------------------------------------------------
      // 0. 横贯标头：纯正工程黑白/深蓝微标题条
      // ------------------------------------------------------------------------
      [
        #rect(
          width: 100%,
          height: 14mm,
          radius: 2pt,
          fill: rgb("#0A192F"),
          stroke: 0.8pt + rgb("#00E5FF")
        )[
          #pad(x: 6mm)[
            #align(horizon)[
              #grid(
                columns: (1fr, auto),
                align: (left + horizon, right + horizon),
                
                stack(
                  dir: ltr,
                  spacing: 4mm,
                  text(size: 11pt, weight: "black", fill: white, tracking: 1pt)[
                    【代际拓扑演进 · 前期机理与试错】从市面推拉黑板测绘到一、二代构型实证
                  ],
                  text(size: 8pt, weight: "medium", fill: rgb("#7DD3FC"))[
                    Baseline Measurement & Generational Failure Analysis (AutoCAD 4K Native Views)
                  ]
                ),
                
                rect(
                  stroke: 0.6pt + rgb("#D4AF37"),
                  fill: rgb("#06121E").transparentize(15%),
                  radius: 2pt,
                  inset: (x: 5pt, y: 2.5pt)
                )[
                  #text(size: 7.5pt, weight: "bold", fill: rgb("#FBD38D"))[初三日常观察灵感 -> 高一初期工程深化]
                ]
              )
            ]
          ]
        ]
      ],
      
      // ------------------------------------------------------------------------
      // 1. 左右原生几何咬合主体 (左侧 375mm 方形 vs 右侧 465mm 双层宽屏)
      // ------------------------------------------------------------------------
      [
        #grid(
          columns: (375mm, 465mm),
          gutter: 6mm,
          
          // ====================================================================
          // 左侧：市面标准双推拉黑板 (4000mm 测绘，顺应 1:1 方形比例自然舒展)
          // ====================================================================
          rect(
            width: 100%,
            height: 275mm,
            radius: 2pt,
            stroke: 0.8pt + rgb("#94A3B8"),
            fill: rgb("#F8FAFC")
          )[
            #pad(x: 4.5mm, top: 3.5mm, bottom: 3mm)[
              #grid(
                columns: (1fr),
                rows: (13mm, 215mm, 1fr),
                row-gutter: 1.5mm,
                
                // 标头
                grid(
                  columns: (auto, 1fr, auto),
                  align: (horizon, horizon, horizon),
                  gutter: 2.5mm,
                  rect(width: 3.5pt, height: 11pt, fill: rgb("#64748B")),
                  text(size: 9.5pt, weight: "bold", fill: rgb("#1E293B"))[
                    [基准工程图] 市面标准推拉黑板 (4000mm) · 4K 测绘
                  ],
                  text(size: 7.5pt, fill: rgb("#DC2626"), weight: "bold")[
                    三大机械原罪 ❌
                  ]
                ),
                
                // 215mm 大幅方形图纸展示 (370x215mm，黑板主体极大化呈现！)
                rect(
                  width: 100%,
                  height: 215mm,
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
                
                // 缺陷机理硬核参数
                text(size: 7.2pt, fill: rgb("#334155"), weight: "medium")[
                  *缺陷测绘*：推开露大屏板书折损 50%；敞开式下滑轨积灰致摩擦阻力 $mu$ 飙升 $280\%$ 卡死；板面单平面固定，避光自由度 $F = 0$。
                ]
              )
            ]
          ],
          
          // ====================================================================
          // 右侧：一代与二代横向宽屏上下并置 (顺应 1.47:1 宽屏大图铺开)
          // ====================================================================
          grid(
            columns: (1fr),
            rows: (134.5mm, 134.5mm),
            row-gutter: 6mm,
            
            // ------------------------------------------------------------------
            // 右上：第一代重力悬臂外展折叠式 (初三萌生 · 5000x3400 宽屏图)
            // ------------------------------------------------------------------
            rect(
              width: 100%,
              height: 134.5mm,
              radius: 2pt,
              stroke: 0.8pt + rgb("#94A3B8"),
              fill: rgb("#F8FAFC")
            )[
              #pad(x: 4.5mm, top: 3mm, bottom: 2.5mm)[
                #grid(
                  columns: (1fr),
                  rows: (12mm, 96mm, 1fr),
                  row-gutter: 1.5mm,
                  
                  grid(
                    columns: (auto, 1fr, auto),
                    align: (horizon, horizon, horizon),
                    gutter: 2.5mm,
                    rect(width: 3.5pt, height: 10pt, fill: rgb("#D97706")),
                    text(size: 9.2pt, weight: "bold", fill: rgb("#1E293B"))[
                      [第一代构型] 重力悬臂外展折叠式 (初三萌生 · 2025.09)
                    ],
                    text(size: 7.2pt, fill: rgb("#D97706"), weight: "bold")[
                      大跨度悬臂梁端部重力挠度超限 (delta = 18mm) ❌
                    ]
                  ),
                  
                  // 宽幅 450mm 大图直接铺开！
                  rect(
                    width: 100%,
                    height: 96mm,
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
                  
                  text(size: 7pt, fill: rgb("#334155"), weight: "medium")[
                    *力学失效推导*：悬臂外展呈大跨度外伸受力，端部挠度 $delta = (q L^4)/(8 E I) + (F L^3)/(3 E I) approx 18.2"mm"$；铰链承受 $360"N"dot"m"$ 巨大剪切弯矩塑性形变卡死。
                  ]
                )
              ]
            ],
            
            // ------------------------------------------------------------------
            // 右下：第二代双滑轨推拉复合旋转式 (高一初期 · 5600x3800 宽屏图)
            // ------------------------------------------------------------------
            rect(
              width: 100%,
              height: 134.5mm,
              radius: 2pt,
              stroke: 0.8pt + rgb("#94A3B8"),
              fill: rgb("#F8FAFC")
            )[
              #pad(x: 4.5mm, top: 3mm, bottom: 2.5mm)[
                #grid(
                  columns: (1fr),
                  rows: (12mm, 96mm, 1fr),
                  row-gutter: 1.5mm,
                  
                  grid(
                    columns: (auto, 1fr, auto),
                    align: (horizon, horizon, horizon),
                    gutter: 2.5mm,
                    rect(width: 3.5pt, height: 10pt, fill: rgb("#EA580C")),
                    text(size: 9.2pt, weight: "bold", fill: rgb("#1E293B"))[
                      [第二代构型] 双滑轨推拉复合自洁防眩光系统 (高一初期 · 2026.03)
                    ],
                    text(size: 7.2pt, fill: rgb("#EA580C"), weight: "bold")[
                      滑动副与转动副同轴空间干涉死锁 ❌
                    ]
                  ),
                  
                  // 宽幅 450mm 大图直接铺开！
                  rect(
                    width: 100%,
                    height: 96mm,
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
                  
                  text(size: 7pt, fill: rgb("#334155"), weight: "medium")[
                    *干涉机理推导*：滑动移动副 $P$ 与偏航转动副 $R$ 同轴布局，极限平移时端板与主边框刚性干涉碰撞，产生 200mm 机械盲区无法实现 86 寸大屏 100% 完整封屏。
                  ]
                )
              ]
            ]
          )
        )
      ]
    )
  ]
]
