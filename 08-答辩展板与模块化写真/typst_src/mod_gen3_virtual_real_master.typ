// ==============================================================================
// MOD-GEN3-3D: 第三代终极总装全宽幅虚实双拼大区 (Virtual-Real Digital Twin Section)
// 物理净尺寸: 860mm x 340mm (含四周 3mm 印刷出血位: 866mm x 346mm)
// 全场主角: 左侧 470mm AutoCAD 5800x4000 完整尺寸线框工程图
//           右侧 370mm Blender 5.0 真实 PBR 4K 超清实体渲染 + 四大工况对比
// 美学标准: 纯工程硬核高反差，线框与实体并驾齐驱，数字孪生终极震撼！
// ==============================================================================

#set page(
  width: 866mm,
  height: 346mm,
  margin: (x: 3mm, y: 3mm), // 3mm 印刷出血位
  fill: rgb("#F8FAFC") // 极简纯净工程白底
)

#set text(
  font: ("Microsoft YaHei", "SimHei"),
  fill: rgb("#0F172A")
)

// 净尺寸裁切外边框 (860mm x 340mm)
#rect(
  width: 860mm,
  height: 340mm,
  radius: 3pt,
  stroke: (paint: rgb("#0F294A"), thickness: 1.5pt),
  fill: rgb("#FFFFFF")
)[
  #pad(x: 6mm, top: 5mm, bottom: 5mm)[
    #grid(
      columns: (1fr),
      rows: (16mm, 1fr),
      row-gutter: 3mm,
      
      // ------------------------------------------------------------------------
      // 0. 横贯标头：全场 C 位主角标志条
      // ------------------------------------------------------------------------
      [
        #rect(
          width: 100%,
          height: 14mm,
          radius: 2pt,
          fill: rgb("#0A192F"),
          stroke: 1pt + rgb("#10B981")
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
                    【第三代终极构型突破】对角线正交解耦全系统工程总装与动力学数字孪生（虚实双拼）
                  ],
                  text(size: 8pt, weight: "medium", fill: rgb("#34D399"))[
                    Orthogonal Diagonal Decoupling Assembly · AutoCAD 4K Blueprint vs. Blender 5.0 PBR Physical Digital Twin
                  ]
                ),
                
                rect(
                  stroke: 0.8pt + rgb("#34D399"),
                  fill: rgb("#064E3B").transparentize(15%),
                  radius: 2pt,
                  inset: (x: 5pt, y: 2.5pt)
                )[
                  #text(size: 7.5pt, weight: "bold", fill: rgb("#6EE7B7"))[自由度 F = 4 · 4000~6000mm 终极闭环]
                ]
              )
            ]
          ]
        ]
      ],
      
      // ------------------------------------------------------------------------
      // 1. 虚实双拼主体：左侧 475mm CAD 线框工程总装 vs 右侧 365mm 3D 实体渲染
      // ------------------------------------------------------------------------
      [
        #grid(
          columns: (475mm, 365mm),
          gutter: 6mm,
          
          // ====================================================================
          // 左侧：第三代 AutoCAD 5800x4000 终极工程总装线框大图
          // ====================================================================
          rect(
            width: 100%,
            height: 305mm,
            radius: 2pt,
            stroke: 1.2pt + rgb("#059669"),
            fill: rgb("#F0FDF4")
          )[
            #pad(x: 5mm, top: 4mm, bottom: 3mm)[
              #grid(
                columns: (1fr),
                rows: (13mm, 230mm, 1fr),
                row-gutter: 2mm,
                
                // 标头
                grid(
                  columns: (auto, 1fr, auto),
                  align: (horizon, horizon, horizon),
                  gutter: 2.5mm,
                  rect(width: 3.5pt, height: 11pt, fill: rgb("#059669")),
                  text(size: 10pt, weight: "bold", fill: rgb("#065F46"))[
                    [虚·工程图纸] AutoCAD 5800×4000 工业标准尺寸链与机构总装工程图
                  ],
                  text(size: 8pt, fill: rgb("#059669"), weight: "bold")[
                    对角线正交解耦 · 零干涉 ✅
                  ]
                ),
                
                // 230mm 宽幅完整工程图纸 (宽达 465mm，GB/T 工业图框与尺寸公差纤毫毕现！)
                rect(
                  width: 100%,
                  height: 230mm,
                  radius: 1.5pt,
                  stroke: 0.8pt + rgb("#059669").transparentize(60%),
                  fill: white
                )[
                  #image(
                    "../assets/cad_sheet_4.png",
                    width: 100%,
                    height: 100%,
                    fit: "contain"
                  )
                ],
                
                // 正交解耦数学模型与技术交底
                text(size: 7.5pt, fill: rgb("#064E3B"), weight: "bold")[
                  *空间对角线正交解耦*：内侧展开铰链轴（$X_1 = plus.minus 1000$mm）与外侧偏航铰链轴（$X_2 = plus.minus 2000$mm，侧滑时 $plus.minus 3000$mm）在空间对角线正交分布，轴向跨度隔离 $Delta X = 1000$mm；内侧 180° 折叠封屏与外侧 30° 避光偏航在机构学上完全解耦，彻底消除了第二代的运动副死锁干涉。
                ]
              )
            ]
          ],
          
          // ====================================================================
          // 右侧：第三代 Blender 5.0 真实 PBR 4K 超清实体渲染 + 四大工况对比
          // ====================================================================
          rect(
            width: 100%,
            height: 305mm,
            radius: 2pt,
            stroke: 1.2pt + rgb("#0284C7"),
            fill: rgb("#F0F9FF")
          )[
            #pad(x: 5mm, top: 4mm, bottom: 3mm)[
              #grid(
                columns: (1fr),
                rows: (13mm, 135mm, 105mm, 1fr),
                row-gutter: 2.5mm,
                
                // 标头
                grid(
                  columns: (auto, 1fr, auto),
                  align: (horizon, horizon, horizon),
                  gutter: 2.5mm,
                  rect(width: 3.5pt, height: 11pt, fill: rgb("#0284C7")),
                  text(size: 10pt, weight: "bold", fill: rgb("#0369A1"))[
                    [实·数字孪生] Blender 5.0 真实 PBR 实体渲染与四大运动工况
                  ],
                  text(size: 8pt, fill: rgb("#0284C7"), weight: "bold")[
                    金属PBR材质 · 动力学闭环
                  ]
                ),
                
                // 实体总装大特写 (真实阳极氧化铝合金、墨绿纳米板面、双横梁金属高光)
                rect(
                  width: 100%,
                  height: 135mm,
                  radius: 1.5pt,
                  stroke: 0.6pt + rgb("#38BDF8"),
                  fill: rgb("#0A192F")
                )[
                  #image(
                    "../assets/gen3_render_master_close.png",
                    width: 100%,
                    height: 100%,
                    fit: "cover"
                  )
                ],
                
                // 四大运动工况对比四联图组
                rect(
                  width: 100%,
                  height: 105mm,
                  radius: 1.5pt,
                  stroke: 0.6pt + rgb("#38BDF8"),
                  fill: rgb("#0A192F")
                )[
                  #image(
                    "../assets/gen3_four_kinematics_grid.png",
                    width: 100%,
                    height: 100%,
                    fit: "contain"
                  )
                ],
                
                // 工况硬核说明
                text(size: 7.2pt, fill: rgb("#075985"), weight: "medium")[
                  *工况①* 全覆盖封屏 (4000mm) | *工况②* 常态大屏露显 (双侧板书) | *工况③* 侧滑极限拓展 (6000mm) | *工况④* 自适应避光偏航 (-15°~+15° 俯仰)。
                ]
              )
            ]
          ]
        )
      ]
    )
  ]
]
