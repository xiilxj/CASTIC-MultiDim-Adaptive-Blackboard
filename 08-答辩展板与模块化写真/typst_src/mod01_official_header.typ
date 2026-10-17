// ==============================================================================
// MOD-01: 大赛官方页眉楣头 (Banner Header)
// 官方规定内容: "第42届瑞安市青少年科技创新大赛科技创新项目"
// 物理净尺寸: 860mm x 45mm (含四周 3mm 印刷出血位: 866mm x 51mm)
// 色彩模式: CMYK/高对比度科技工程深蓝金线装裱
// ==============================================================================

#set page(
  width: 866mm,
  height: 51mm,
  margin: (x: 3mm, y: 3mm), // 3mm 出血安全线
  fill: rgb("#06121E") // 极深钛青暗底
)

#set text(
  font: ("Microsoft YaHei", "SimHei"),
  fill: white
)

// 外层出血裁剪辅助框 (净尺寸 860mm x 45mm)
#rect(
  width: 860mm,
  height: 45mm,
  radius: 3pt,
  stroke: (paint: rgb("#1E3E62"), thickness: 1.5pt),
  fill: gradient.linear(
    rgb("#091E36"),
    rgb("#0E2D52"),
    rgb("#133B6B"),
    rgb("#0E2D52"),
    rgb("#091E36"),
    angle: 90deg
  )
)[
  // 内嵌金色/青色双重科技精密修饰线
  #place(top + left, dx: 6mm, dy: 3.5mm)[
    #rect(
      width: 848mm,
      height: 38mm,
      stroke: (paint: rgb("#D4AF37").lighten(30%), thickness: 0.8pt),
      fill: none
    )
  ]

  // 主体内容弹性布局
  #pad(x: 18mm, y: 0mm)[
    #align(horizon)[
      #grid(
        columns: (1fr, auto),
        align: (left + horizon, right + horizon),
        gutter: 20mm,
        
        // 左侧：官方强制规定的页眉主标题
        stack(
          dir: ltr,
          spacing: 12mm,
          
          // 官方科技星徽装饰
          circle(
            radius: 11pt,
            fill: rgb("#D4AF37"),
            stroke: 1.5pt + white
          )[
            #align(center + horizon)[
              #text(size: 13pt, fill: rgb("#06121E"), weight: "bold")[★]
            ]
          ],
          
          // 核心文字
          text(
            size: 26pt,
            weight: "bold",
            tracking: 3.5pt,
            fill: rgb("#FFFFFF")
          )[
            第42届瑞安市青少年科技创新大赛科技创新项目
          ]
        ),
        
        // 右侧：专业学术竞赛属性标注
        stack(
          dir: ltr,
          spacing: 8mm,
          
          rect(
            stroke: 1pt + rgb("#00E5FF").transparentize(40%),
            fill: rgb("#00E5FF").transparentize(88%),
            radius: 3pt,
            inset: (x: 10pt, y: 5pt)
          )[
            #text(size: 13pt, weight: "bold", fill: rgb("#00E5FF"))[
              高中组 · 科技创新发明类
            ]
          ],
          
          rect(
            stroke: 1pt + rgb("#D4AF37").transparentize(40%),
            fill: rgb("#D4AF37").transparentize(88%),
            radius: 3pt,
            inset: (x: 10pt, y: 5pt)
          )[
            #text(size: 13pt, weight: "bold", fill: rgb("#FBD38D"))[
              学科代码：ENGI（工程学）
            ]
          ]
        )
      )
    ]
  ]
]
