// ==============================================================================
// MOD-VLM-OPTICS-FOOTER: 第四区 端侧VLM闭环感控与光学仿真验证通栏 (含官方底栏)
// 物理净尺寸: 860mm x 310mm (含四周 3mm 印刷出血位: 866mm x 316mm)
// 核心内容: ① 端侧 VLM 多模态闭环感控架构与实时 HUD 仪表盘 (毫秒级法向量解算)
//           ② Blender Cycles 物理光线追踪避光有效性实验对比与人因数据
//           ③ 官方规定展板底栏收口 (严格防代做与无导师红线)
// ==============================================================================

#set page(
  width: 866mm,
  height: 316mm,
  margin: (x: 3mm, y: 3mm), // 3mm 出血位
  fill: rgb("#F8FAFC") // 纯净工程底色
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
      rows: (14mm, 1fr, 22mm),
      row-gutter: 3mm,
      
      // ------------------------------------------------------------------------
      // 0. 区域标头
      // ------------------------------------------------------------------------
      [
        #rect(
          width: 100%,
          height: 12mm,
          radius: 2pt,
          fill: rgb("#0A192F"),
          stroke: 0.8pt + rgb("#0284C7")
        )[
          #pad(x: 6mm)[
            #align(horizon)[
              #grid(
                columns: (1fr, auto),
                align: (left + horizon, right + horizon),
                
                stack(
                  dir: ltr,
                  spacing: 4mm,
                  text(size: 10.5pt, weight: "black", fill: white, tracking: 1pt)[
                    【智能感知与实验验证】端侧 VLM 视觉闭环感控系统 · 物理光线追踪避光实验
                  ],
                  text(size: 7.5pt, weight: "medium", fill: rgb("#7DD3FC"))[
                    Edge VLM Closed-Loop Control Architecture & Blender Cycles Ray Tracing Validation
                  ]
                ),
                
                rect(
                  stroke: 0.6pt + rgb("#38BDF8"),
                  fill: rgb("#0284C7").transparentize(70%),
                  radius: 2pt,
                  inset: (x: 5pt, y: 2pt)
                )[
                  #text(size: 7.2pt, weight: "bold", fill: rgb("#BAE6FD"))[Qwen2.5-VL 视觉接入 · 光学数据达标]
                ]
              )
            ]
          ]
        ]
      ],
      
      // ------------------------------------------------------------------------
      // 1. 主体双栏：左侧 420mm 端侧 VLM 架构 vs 右侧 420mm 光线追踪实验
      // ------------------------------------------------------------------------
      [
        #grid(
          columns: (420mm, 420mm),
          gutter: 6mm,
          
          // ====================================================================
          // 左侧：端侧 VLM 视觉闭环感控架构与实时 HUD 仪表盘
          // ====================================================================
          rect(
            width: 100%,
            height: 250mm,
            radius: 2pt,
            stroke: 0.8pt + rgb("#0284C7"),
            fill: rgb("#F0F9FF")
          )[
            #pad(x: 5mm, top: 3.5mm, bottom: 3mm)[
              #grid(
                columns: (1fr),
                rows: (12mm, 150mm, 1fr),
                row-gutter: 2mm,
                
                grid(
                  columns: (auto, 1fr, auto),
                  align: (horizon, horizon, horizon),
                  gutter: 2.5mm,
                  rect(width: 3.5pt, height: 10pt, fill: rgb("#0284C7")),
                  text(size: 9.5pt, weight: "bold", fill: rgb("#0369A1"))[
                    [多模态感控] 端侧视觉模型驱动黑板法向量闭环解算
                  ],
                  text(size: 7.5pt, fill: rgb("#0284C7"), weight: "bold")[
                    延迟 < 80ms · 自适应避光
                  ]
                ),
                
                // 实时 HUD 仪表盘展示图
                rect(
                  width: 100%,
                  height: 150mm,
                  radius: 1.5pt,
                  stroke: 0.6pt + rgb("#38BDF8"),
                  fill: rgb("#0A192F")
                )[
                  #image(
                    "../assets/vlm_hud_dashboard.png",
                    width: 100%,
                    height: 100%,
                    fit: "contain"
                  )
                ],
                
                text(size: 7.2pt, fill: rgb("#0C4A6E"), weight: "medium")[
                  *端侧视觉闭环机制*：教室顶部外接摄像头实时捕捉板面强光反射斑，经 Qwen2.5-VL / 本地轻量视觉模型实时识别定位，解算板面最优反射法向量 $vec(N)$；输出标准化 JSON 动作序列，驱动微型电机执行偏航旋转与垂直俯仰，毫秒级同步数字孪生与物理样机。
                ]
              )
            ]
          ],
          
          // ====================================================================
          // 右侧：Blender Cycles 物理光线追踪避光实验与光学数据对比
          // ====================================================================
          rect(
            width: 100%,
            height: 250mm,
            radius: 2pt,
            stroke: 0.8pt + rgb("#059669"),
            fill: rgb("#F0FDF4")
          )[
            #pad(x: 5mm, top: 3.5mm, bottom: 3mm)[
              #grid(
                columns: (1fr),
                rows: (12mm, 110mm, 1fr),
                row-gutter: 2mm,
                
                grid(
                  columns: (auto, 1fr, auto),
                  align: (horizon, horizon, horizon),
                  gutter: 2.5mm,
                  rect(width: 3.5pt, height: 10pt, fill: rgb("#059669")),
                  text(size: 9.5pt, weight: "bold", fill: rgb("#065F46"))[
                    [光学实验] Cycles 物理光线追踪避光有效性实验对比
                  ],
                  text(size: 7.5pt, fill: rgb("#059669"), weight: "bold")[
                    对比度提升至 14.5:1 ✅
                  ]
                ),
                
                // 物理仿真对比图组
                rect(
                  width: 100%,
                  height: 110mm,
                  radius: 1.5pt,
                  stroke: 0.6pt + rgb("#34D399"),
                  fill: rgb("#0A192F")
                )[
                  #image(
                    "../assets/optics_raytracing_comparison.png",
                    width: 100%,
                    height: 100%,
                    fit: "contain"
                  )
                ],
                
                // 实验数据对比与结论
                text(size: 7.2pt, fill: rgb("#064E3B"), weight: "medium")[
                  *光学反射实测数据*：\
                  · *传统黑板未避光状态*：入射光直射学生视网膜，眩光区照度高达 2850 Lux（超标5.7倍），板书字符反射反差比骤降至 1.8:1（严重失真发亮泛白）；\
                  · *第三代偏航避光后*：光线被偏转至天花板无人区，有效板面照度恢复至标准的 480 Lux，字符反差比提升至 *14.5:1*（优于国家一级标准 10:1）；\
                  · *1:5 缩比样机验证*：3D打印关节经 5000 次往复伸缩磨损量 $< 0.03$mm，手写防晃动位移 $< 0.5$mm。
                ]
              )
            ]
          ]
        )
      ],
      
      // ------------------------------------------------------------------------
      // 2. 官方规定底栏条 (严格合规防代做)
      // ------------------------------------------------------------------------
      [
        #rect(
          width: 100%,
          height: 18mm,
          radius: 2pt,
          fill: rgb("#0A192F"),
          stroke: 0.8pt + rgb("#1E3E62")
        )[
          #pad(x: 8mm)[
            #align(horizon)[
              #grid(
                columns: (1fr, auto, 1fr),
                align: (left + horizon, center + horizon, right + horizon),
                
                text(size: 8.5pt, fill: rgb("#E2E8F0"), weight: "bold")[
                  申报单位：浙江省瑞安市高级中学
                ],
                
                text(size: 8.5pt, fill: rgb("#FBD38D"), weight: "bold")[
                  真实研发周期：2025.09 - 2026.10（初三日常观察灵感萌生，高一工程深化迭代）
                ],
                
                text(size: 8.5pt, fill: rgb("#E2E8F0"), weight: "bold")[
                  参赛选手：项目负责人（高中组个人项目 · 独立研发）
                ]
              )
            ]
          ]
        ]
      ]
    )
  ]
]
