import re

typst_path = '/mnt/d/Desktop/CASTICpjhb/04-汇报与交付报告/castic_project_introduction_dossier.typ'

with open(typst_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 更新目录部分的附录标题文字
content = content.replace(
    '[#h(1.2em) 附录二：发明专利技术方案交底书与权利要求书（共 3 页）], [#text(fill: rgb("#64748B"))[15]],',
    '[#h(1.2em) 附录二：国家知识产权局专利申请受理与公布通知书（共 3 页）], [#text(fill: rgb("#64748B"))[15]],'
)

# 专利附录追加内容
patents_typst_code = """

// ==============================================================================
// 附录二：国家知识产权局专利申请受理与公布通知书 (官方扫描原件共 3 页)
// ==============================================================================
#pagebreak()
= 附录二：国家知识产权局官方专利申请受理与公布通知书

#text(size: 8.5pt, fill: rgb("#475569"))[
  *附件 2-1*：国家知识产权局《发明专利申请受理通知书》（申请号：202511764745.X · 发明创造名称：一种折叠翻转式模块化多媒体教学黑板及光环境系统 · 申请人与发明人：林诚俊）
]
#v(0.15cm)
#align(center)[
  #rect(width: 90%, stroke: 0.8pt + border-color, fill: white, radius: 3pt, inset: 2pt)[
    #image("patent_assets/patent_01_invention_accept-1.png", width: 95%, fit: "contain")
  ]
]

#pagebreak()
#text(size: 8.5pt, fill: rgb("#475569"))[
  *附件 2-2*：国家知识产权局《发明专利申请公布通知书》（经初审合格，于 2025 年 12 月 30 日在国家知识产权局第 41 卷 5301 期专利公报上正式公布 · 申请人：林诚俊）
]
#v(0.15cm)
#align(center)[
  #rect(width: 90%, stroke: 0.8pt + border-color, fill: white, radius: 3pt, inset: 2pt)[
    #image("patent_assets/patent_02_invention_publish-1.png", width: 95%, fit: "contain")
  ]
]

#pagebreak()
#text(size: 8.5pt, fill: rgb("#475569"))[
  *附件 2-3*：国家知识产权局《实用新型专利申请受理通知书》（申请号：202522523482.5 · 发明创造名称：一种折叠翻转式模块化多媒体教学黑板及光环境系统 · 申请人与发明人：林诚俊）
]
#v(0.15cm)
#align(center)[
  #rect(width: 90%, stroke: 0.8pt + border-color, fill: white, radius: 3pt, inset: 2pt)[
    #image("patent_assets/patent_03_utility_accept-1.png", width: 95%, fit: "contain")
  ]
]

// ==============================================================================
// 附录三：发明专利说明书标准工程附图集 (共 2 页)
// ==============================================================================
#pagebreak()
= 附录三：发明专利说明书标准工程附图集

#text(size: 8.5pt, fill: rgb("#475569"))[
  *说明书附图（一）*：一种折叠翻转式模块化多媒体教学黑板及光环境系统——总装配立面结构与零件公差装配蓝图（工程图号: DWG-Z3-001）
]
#v(0.15cm)
#align(center)[
  #rect(width: 90%, stroke: 0.8pt + border-color, fill: card-bg, radius: 3pt, inset: 3pt)[
    #image("../08-答辩展板与模块化写真/assets/cad_sheet_4.png", width: 96%, fit: "contain")
  ]
]

#pagebreak()
#text(size: 8.5pt, fill: rgb("#475569"))[
  *说明书附图（二）*：一种折叠翻转式模块化多媒体教学黑板及光环境系统——对角铰链三维微观结构与避光偏航空间位姿图
]
#v(0.15cm)
#align(center)[
  #grid(
    columns: (1fr, 1fr),
    gutter: 8pt,
    rect(width: 100%, stroke: 0.6pt + border-color, fill: card-bg, radius: 3pt, inset: 3pt)[
      #image("../08-答辩展板与模块化写真/assets/gen3_hinge_macro_4k.png", width: 98%, fit: "contain")
      #text(size: 7.5pt, fill: rgb("#64748B"))[附图 3：对角承重铰链与推力轴承微观装配图]
    ],
    rect(width: 100%, stroke: 0.6pt + border-color, fill: card-bg, radius: 3pt, inset: 3pt)[
      #image("../08-答辩展板与模块化写真/assets/gen3_deployed_yaw_4k.png", width: 98%, fit: "contain")
      #text(size: 7.5pt, fill: rgb("#64748B"))[附图 4：避光偏航态（Yaw 4.5°）空间位姿图]
    ]
  )
]

#v(0.3cm)
#align(center)[
  #text(size: 8.5pt, fill: rgb("#475569"), weight: "bold")[
    — 全卷十九页终 · 浙江省塘下中学 林诚俊 独立研发科技发明成果技术报告 · 2026年10月 —
  ]
]
"""

# 把附录一后面的原结尾替换并拼接上新附录
content = re.sub(r'— 正文完.*?—', '', content)
content = content.strip() + '\n' + patents_typst_code

with open(typst_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Typst 源码成功注入 3 页专利通知书与 2 页专利说明书工程附图！')
