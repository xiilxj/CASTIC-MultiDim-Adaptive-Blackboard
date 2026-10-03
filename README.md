# 光衡 (GH-VI-2026) · 基于多维叠合翻转与自适应避光的多模态智能教学黑板系统
### 第 42 届全国青少年科技创新大赛 (CASTIC) · 工程学 (机械工程 / 智能制造) 参赛重点攻坚工程

<p align="left">
  <img src="https://img.shields.io/badge/Competition-CASTIC%202026%20National-orange.svg?style=flat-square&logo=target" alt="CASTIC 2026" />
  <img src="https://img.shields.io/badge/Project-GH--VI--2026%20LightBalance-blue.svg?style=flat-square" alt="GH-VI-2026" />
  <img src="https://img.shields.io/badge/Blender-5.0.1%20Cycles%20GPU-E87D0D.svg?style=flat-square&logo=blender" alt="Blender 5.0" />
  <img src="https://img.shields.io/badge/AutoCAD-2026%20COM%20Automation-red.svg?style=flat-square&logo=autodesk" alt="AutoCAD 2026" />
  <img src="https://img.shields.io/badge/Typst-0.15.1%20Academic%20Report-239dad.svg?style=flat-square" alt="Typst" />
  <img src="https://img.shields.io/badge/OpenCV-5.0.0%20Live%20Vision-5C3EE8.svg?style=flat-square&logo=opencv" alt="OpenCV 5.0" />
  <img src="https://img.shields.io/badge/VLM-Qwen2.5--VL%20Agent%20ToolCall-8A2BE2.svg?style=flat-square" alt="Edge VLM" />
  <img src="https://img.shields.io/badge/Python-3.10%20%7C%203.12-3776AB.svg?style=flat-square&logo=python" alt="Python" />
  <img src="https://img.shields.io/badge/Fabrication-Bambu%20Studio%203MF-00AE42.svg?style=flat-square" alt="Bambu Studio" />
  <img src="https://img.shields.io/badge/Digital%20Twin-60%20FPS%20Realtime%20IPC-00C853.svg?style=flat-square" alt="Digital Twin" />
  <img src="https://img.shields.io/badge/Classroom-48%20Seats%20Ergonomics-FF6D00.svg?style=flat-square" alt="48 Seats" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="MIT License" />
</p>

---

## 📖 一、 项目背景与中学生身边真实痛点 (Real Classroom Problem)

本项目源于高中生在日常教室学习中的亲身体验与客观测量：传统推拉黑板与多媒体互动教学长期面临三大工程与光环境痛点：
1. **窗侧强光反射“眩光致盲盲区”**：强日光斜射下，教室靠窗与对侧前排多达 **35%~40% 的学生**无法看清黑板板书或大屏内容，引起强烈的眯眼应激（$EAR < 0.20$）与视疲劳；
2. **大尺寸交互屏幕与大面积物理板书不可兼得**：市面传统推拉黑板在露显 86 寸中置屏幕时，有效书写面积折损过半；若完全封闭大屏，则无法进行信息化多媒体协同；
3. **粉笔灰堆积与滑道卡阻**：长期粉笔灰沉降堵塞下部机械滑道，形成“活塞卡阻”，导致推拉沉重受阻、结构易磨损损坏。

针对上述难题，本项目历经 **S 系列（单偏心铰链）**、**VI 系列（三维避光光路仿真）** 与 **Z 系列（对角线双铰链两折叠并成）** 三代拓扑演进，最终形成了集**“对角线双铰链空间正交解耦机构”**与**“端侧多模态视觉语言大模型 (Edge VLM) 活体数字孪生闭环”**于一体的全新解决方案。

```
【第一代翻转黑板 (S系列)】         【第二代三维联动黑板 (VI系列)】         【第三代多维叠合黑板 (Z系列 / GH-VI-2026)】
阻尼偏心单铰链 178°翻折    ──►   三维空间光路逆向溯源 (偏航+俯仰+侧滑)   ──►   对角线双铰链正交解耦 + 60FPS 活体数字孪生
视场横向扩展、大屏简单露显         48席空间光强分布、高程反射分层               三大工况大一统 (4000~6000mm) + 真机闭环控制
```

---

## 🌟 二、 核心机构学创新与机械拓扑 (Mechanical Innovations)

### 1. 对角线双铰链正交解耦机构 (Diagonal Topology)
- **外层内侧折叠铰链 ($X = \pm 1000\text{mm}$)**：驱动外层 12mm 超薄副板向黑板中心 180° 翻开合拢，形成 4000mm 全覆盖封屏形态；
- **内层外侧翻转主轴 ($X = \pm 2000\text{mm} \to \pm 3000\text{mm}$)**：驱动双层贴合后的整体黑板模组向外侧偏航 $+8.0^\circ \sim +18.0^\circ$ 避光；
- **空间几何解耦**：两组旋转铰链在俯视截面上呈**对角线分离**，彻底消除双层板贴合（总厚度仅 26mm）时的空间运动干涉与运动学死点。

### 2. 三大核心使用工况大一统
| 使用工况 | 系统跨度 | 机构空间形态 | 教学应用场景 |
| :--- | :--- | :--- | :--- |
| **工况一【初始闭合·全覆盖封屏】** | **4000mm** | 外层副板向内 180° 展开合拢，双板锁死封屏 | 100% 遮蔽保护 86 寸液晶大屏，提供纯物理板书沉浸教学 |
| **工况二【常态露屏·双层致密叠合】** | **4000mm** | 外层副板向后 180° 折叠贴合于内主板前方 | 露出 86 寸中置交互大屏，叠合总厚度仅 26mm，板书大屏协同 |
| **工况三【大视野展开·多维避光偏航】** | **6000mm** | $\Phi 28\text{mm}$ 双横梁套杆外伸 1000mm，副板翻开展开 | 形成 6000mm 终极全景视界，并支持黑板偏航 18° 实现自适应避光 |

### 3. 双横梁自洁防卡阻导轨
- 倒 V 型 EPDM 弹性密封导流罩，隔绝 92% 直落粉笔尘；
- 滑槽轴向每隔 200mm 开设 $\Phi 12\text{mm}$ 垂直落灰孔，消除活塞气阻；
- 滑块端面高密度尼龙刮尘毛刷往复自洁，实现长期免维护。

---

## 👁️ 三、 伪 VR 沉浸式真机活体数字孪生系统 (Digital Twin System)

> **拒绝静态 PPT 与预录视频！** 本项目在第 35~39 轮工程攻坚中，构建了面向比赛答辩现场的**客观活体真机互动演示系统**：评委坐在或站在电脑摄像头前，系统实时捕获面部、计算眼裂长宽比 $EAR$ 或手机照光，旁边的 Blender 5.0 视口里的 3D 黑板、百叶窗、光路当场发生 60 FPS 物理级联动！

```
                     【GH-VI-2026 数字孪生真机交互全链路闭环】
                      
 [物理摄像头/运动相机] ──(实时视频流 30FPS)──► [进程A: 上位机多相机感知中枢 (Python)]
                                                            │
                                             毫秒级计算: EAR < 0.20 (眯眼) / 强光斑 > 1500px
                                                            │
                                             Agent 自然语言工具分发 (Tool Calling)
                                             >>> api_adjust_blackboard(yaw=18.0 deg)
                                             >>> api_set_smart_blinds(level=65%)
                                                            │
                                             IPC 状态总线 (live_control_state.json)
                                                            │
                                                            ▼
 [3D视口 60FPS 伪VR呈现] ◄──(S曲线平滑阻尼动力学)── [进程B: Blender 5.0 活体驱动引擎]
   * 黑板机构偏航 18° 转动
   * 危险红色直射光束切除消除
   * 青绿色安全激光射向天花板
   * 3D 前墙浮动发光 HUD 实时变字
```

### 决策透明度四大回显看板 (Transparent Reasoning)
1. **怎样识别出来 (How Identified)**：眼裂长宽比 $EAR < 0.22$（判定为眯眼避光应激），强光斑面积 $> 1500\text{px}$；
2. **调节了什么部件 (What Adjusted)**：左侧活动黑板主铰链 (`Ctrl_Flip_Left`)、侧窗百叶帘、自适应洗墙灯；
3. **调节了多少度 (How Much Adjusted)**：黑板偏航 $+18.0^\circ$、百叶帘降下 $65\%$、洗墙灯功率调至 $220\text{W}$；
4. **为什么调节 (Why Adjusted)**：将眩光向上反射至教室天花板吸光层 ($Z=2.8\text{m}$)，全班 48 席无二次光污染，IMAX 视线夹角由 28° 提升至 44.5°！

---

## 📁 四、 规范化工程目录导航 (Repository Structure)

```
CASTIC-MultiDim-Adaptive-Blackboard/
├── 01-CAD工程图纸/               # AutoCAD 2026 工业级矢量图纸 (DWG) 与 4K 纯线框图
├── 02-设计规格与部件文档/        # 历代技术规格书、物理参数数据集与运动学分析报告
├── 03-脚本与自动化源码/          # AutoCAD COM 自动化参数化绘图与批量图纸导出脚本
├── 04-汇报与交付报告/            # 学术级阶段技术测验报告 (Typst / PDF) 与问辩备忘录
├── 05-三维建模与Blender渲染/     # Blender 5.0 原生三维动力学模型与数字孪生工程
│   ├── S系列/                   # 第一代单铰链翻转黑板工程与渲染集
│   ├── VI系列/                  # 第二代三维空间光路仿真与 39 轮工程开发记录
│   │   └── VI系列开发记录.md    # 详尽记录第 1 至第 39 轮全部开发、修改与实测日志
│   ├── Z系列/                   # 第三代对角线双铰链多维叠合黑板工程母本
│   └── vlm_control/             # 活体数字孪生控制中枢与真机联动代码
│       ├── vi7_anti_glare_simulation_v2.blend # 48席人体工学教室 3D 物理母本
│       ├── blender_live_viewport_addon.py     # Blender 5.0 原生 60FPS 视口驱动引擎
│       ├── vlm_interactive_live_operator.py   # 多相机视觉感知与 Agent 工具调用上位机
│       ├── run_live_system.py                 # 双模自动化系统启动调度器
│       ├── START_LIVE.bat                     # 子目录极速双击运行脚本
│       └── live_control_state.json            # 毫秒级 IPC 跨进程共享状态文件
├── 06-物理样机与3D打印工程/      # 1:10 拓竹 Bambu Studio 3MF 工程与 STL 模型
├── 07-系统架构与流程图/          # 高精度 SVG 矢量架构图库与生成器
│   ├── svg/                     # 独立无损 SVG 矢量图资产 (时序图/流程图/双轨架构图)
│   ├── generate_all_plan_svgs.py# 矢量图自动构建脚本
│   └── README.md                # 流程图资产索引与技术说明
├── START_GH_VI.bat               # 根目录纯 ASCII 安全极速启动批处理 (推荐双击)
├── 启动GH-VI数字孪生交互系统.bat # 根目录 GBK 兼容双击批处理
├── run_live_system.py            # 根目录 Python 自适应引导调度桥接
└── README.md                     # 本说明文档
```

---

## 🚀 五、 快速上手与真机复现 (Quick Start)

### 1. 启动真机活体数字孪生系统 (Windows 推荐)
在 Windows 环境下，你可以使用以下任意一种方式瞬间拉起系统：
- **方式一（最推荐，纯 ASCII 防乱码）**：
  直接在根目录下双击 **`START_GH_VI.bat`**；
- **方式二（命令行单行执行）**：
  ```cmd
  cd /d D:\Desktop\CASTICpjhb
  py -3.10 run_live_system.py
  ```

### 2. Blender 视口联动挂载
1. 双击打开 `05-三维建模与Blender渲染\vlm_control\vi7_anti_glare_simulation_v2.blend`；
2. 切换至顶部的 **`Scripting`** 工作区；
3. 在右侧代码窗口中按快捷键 **`Alt + P`**（或点击右上角 **`▶` Run Script**）；
4. 视口前墙上方亮起青色 3D 看板 `GH-VI-2026 LIVE AGENT HUD`，系统即可全自动以 60 FPS 接收外部摄像头感知指令！

### 3. 编译正式学术交付报告 (PDF)
本项目报告使用现代学术级排版系统 [Typst](https://typst.app/) 编写：
```bash
typst compile "04-汇报与交付报告/面向VLM赋能教室光环境的多维教学黑板机构学设计与代际拓扑演进_第一阶段技术测验报告_v1.0.typ"
```

---

## 📜 六、 竞赛规范与“三自原则”声明 (CASTIC Compliance)

本项目严格恪守全国青少年科技创新大赛章程与评审规则，郑重声明遵循**“三自原则”**：
1. **自己选题 (Self-Topic Selection)**：选题源于团队成员在高中真实教室中的第一手用眼痛点调查与光照度实测，非商业外包或导师课题移植；
2. **自己设计与制作 (Self-Design & Fabrication)**：AutoCAD 2026 工业工程图纸、Blender 5.0 动力学建模、Python 算法中枢与拓竹 3D 打印样机切片均由团队成员独立完成；
3. **自己撰写 (Self-Authoring)**：本仓库所有研发日志（1~39 轮）、研究论文与演示答辩系统均由作者亲笔撰写，保留完整 Git 版本演进存证。

---

<p align="center">
  <b>CASTIC 2026 全国青少年科技创新大赛参赛作品 · 版权所有 © 2026 光衡研发团队</b>
</p>
