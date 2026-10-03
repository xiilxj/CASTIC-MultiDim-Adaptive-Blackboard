# 光衡 (GH-VI-2026) —— 基于 VLM 视觉语言大模型的 Blender 控件驱动与数字孪生闭环控制系统技术方案

> **项目名称**: 第 42 届瑞安市青少年科技创新大赛 (CASTIC)  
> **所属模块**: 05-三维建模与Blender渲染 / vlm_control  
> **技术审核标识**: 第 24 轮工程技术审核  
> **核心主题**: 构想并落地视觉语言大模型 (Vision-Language Model, VLM) 对 Blender 虚拟机构控件的端到端控制体系与数字孪生双向闭环。

---

## 一、 系统架构总览：从多模态视觉感知到 Blender 物理执行

本系统将 Blender 虚拟仿真场视为物理智能黑板的**高保真数字孪生载体（Digital Twin Platform）**。VLM 充当全教室的“视觉感知中枢与决策大脑”，Blender 控件则对应实体黑板的伺服电机驱动器、步进导轨与霍尔编码器。

```mermaid
flowchart TD
    subgraph 感知层 [1. 多模态物理环境感知]
        A1[侧窗日照光斑追踪相机] -->|教室光场图像| VLM[VLM 端侧多模态大模型<br/>Qwen2.5-VL / Gemini-Pro]
        A2[讲台教师姿态与板书识别] -->|授课行为流| VLM
        A3[学生视角眩光监测阵列] -->|视网膜入射角分析| VLM
        A4[自然语言/语音指令] -->|"反光晃眼，展开避光"| VLM
    end

    subgraph 决策层 [2. 认知推理与机构动作生成]
        VLM --> B1{多模态决策逻辑}
        B1 -->|防直射强眩光| C1[避光偏航动作策略]
        B1 -->|大板书数学/物理课| C2[6米满幅极限展开策略]
        B1 -->|多媒体视频课件| C3[大屏裸露双层叠合策略]
        B1 -->|课间自洁/护眼| C4[完全闭合封屏策略]
        C1 & C2 & C3 & C4 --> D1[生成标准化 JSON 机构动力学指令]
    end

    subgraph 桥接层 [3. 网桥与通信协议]
        D1 --> E1[Blender MCP / TCP Socket 桥接中枢]
    end

    subgraph 虚拟执行层 [4. Blender 3D 控件拓扑体系]
        E1 --> F1[Ctrl_Rod_Inward: 绳索杆内伸碰头 0~1000mm]
        E1 --> F2[Ctrl_Slide: 双层黑板沿轨滑动 0~1000mm]
        E1 --> F3[Ctrl_Flip: 外侧主铰链偏航角 -18°~+18°]
        E1 --> F4[Ctrl_Rod_Outward: 金属框架外衍生 0~1000mm]
        E1 --> F5[Ctrl_Fold: 前层内铰链翻折 0°~180°]
        E1 --> F6[Sun / Area Lights: 光环境联动调光]
    end

    subgraph 验证闭环 [5. 视觉渲染闭环校验]
        F3 & F5 --> G1[Blender 虚拟相机即时渲染学生视角]
        G1 -->|无头回传分析图| VLM
        VLM -->|对比反光率是否<5%| H1{达标判定}
        H1 -->|达标| I1[下发实体黑板执行]
        H1 -->|未达标| J1[微调偏航角 ±2° 循环收敛]
```

---

## 二、 Blender 中对应的真实控件体系定义

在 Blender 的 `vi1.blend` / `vi2.blend` 工程中，所有机械部件均通过父子级关系挂载在 5 对标准化控制器（Empty Controls）上。VLM 无需操纵复杂的底层网格顶点，仅需通过操作这 5 个控制器的 Transform 属性即可驱动全局机械联动：

| 控制器名称 | 对象类型 | 运动自由度 | 物理含义与行程范围 | 驱动的实际机构部件 |
| :--- | :--- | :--- | :--- | :--- |
| `Ctrl_Rod_Inward_L/R` | Empty (Cube/Axes) | 本地 X 轴位移 | $\pm 1000\text{mm}$ (向中心碰头) | 阶段一初内伸绳索杆、防下垂柔性支撑导向轨 |
| `Ctrl_Slide_L/R` | Empty (Arrows) | 本地 X 轴位移 | $\pm 1000\text{mm}$ (沿主梁/外轨滑动) | 阶段一闭合滑块、阶段四滑至外端边界滑靴 |
| `Ctrl_Flip_L/R` | Empty (Sphere) | 本地 Z 轴旋转 | $-18^\circ \sim +18^\circ$ (外向偏航) | 阶段二偏航翻转主轴、青色五金转轴、活动框架 |
| `Ctrl_Rod_Outward_L/R` | Empty (Single Arrow) | 本地 X 轴位移 | $\pm 1000\text{mm}$ (向外横向衍生) | 阶段三金属外挂延伸导轨、伸缩套杆 |
| `Ctrl_Fold_L/R` | Empty (Circle) | 本地 Z 轴旋转 | $0^\circ \sim 180^\circ$ (朝镜头向内翻开) | 阶段四 B 最前层黑板内侧竖边铰链、6米满幅回填板 |
| `Sun_VI` & `Fill_Area_VI` | Light | 旋转/能量 | 太阳高度角、洗墙灯功率 | 教室动态光环境、自适应补光灯阵列 |

---

## 三、 VLM 控制 Blender 控件的三大落地实现路径

### 路径 1：官方 Blender MCP (Model Context Protocol) 实时注入（当前原生支持）
- **实现原理**:
  - 当前工作环境中已加载并运行 `mcp-for-blender` 服务；
  - VLM 大模型作为客户端，通过 MCP 工具标准调用 `execute_blender_code`；
  - 动态生成并注入一段经过安全校验的 Python 代码，直接对 Blender 内部的 `bpy.data.objects['Ctrl_xxx']` 赋值并调用 `keyframe_insert` 或实时平移。
- **优点**: 零安装零侵入，开箱即用，支持复杂的即时装配与材质属性变更。

### 路径 2：TCP / WebSocket 双向流式数字孪生桥接（低延迟高频实时控制）
- **实现原理**:
  - 在 Blender 内加载一个常驻后台插件（基于 `bpy.app.timers` 定时器）；
  - Blender 开放端口（如 `localhost:9876`）；
  - VLM 边缘端通过 Python WebSocket 客户端将结构化控制帧流式推入；
  - Blender 端定时器在每一帧通过阻尼插值（Lerp 平滑插值，公式为 $x_{t} = x_{t-1} + (x_{\text{target}} - x_{t-1}) \times \alpha$）推动控件运动，模拟真实的电机加减速 S 曲线，彻底避免瞬间突变跳动。
- **优点**: 达到 60 FPS 流畅实时交互，适合展台现场教师体态/手势实时追踪演示。

### 路径 3：根节点自定义属性 (Custom Properties) + 内部 Driver 联动驱动
- **实现原理**:
  - 在场景根节点 `GH_VI_System_Root` 上定义高级抽象属性：
    - `prop_deploy_state` (0: 封屏, 1: 露屏, 2: 偏航避光, 3: 6米满幅)
    - `prop_sun_azimuth` (太阳方位角)
    - `prop_glare_intensity` (眩光强度)
  - 为 5 对控制器设置 Blender Drivers 驱动器表达式；
  - VLM 只需要输出一个极简标量（例如 `prop_deploy_state = 3`），Blender 底层自动通过数学表达式将 10 个子机构精准联动到目标几何解。
- **优点**: 逻辑内聚在 .blend 文件内，极其鲁棒，外部只需修改单一参数。

---

## 四、 闭环端到端视觉校验机制 (Vision Feedback Loop)

为体现本次参赛在“智能性”上的真正突破，VLM 与 Blender 的交互不应仅仅是单向开环输出，而应具备**“感知 $\rightarrow$ 决策 $\rightarrow$ 驱动 $\rightarrow$ 仿真渲染 $\rightarrow$ 视觉回传 $\rightarrow$ 结果复核”**的真正具身闭环：

1. **动作执行**: VLM 计算出左侧黑板偏航 $18^\circ$ 并滑移 $1.0\text{m}$；
2. **虚拟视角抓取**: Blender 在无头模式下，切换至 `Student_Eye_Camera`（模拟反光最严重的左侧靠窗前排同学视点），在 0.2 秒内渲染出一张 512×288 的快速视网膜视图；
3. **视觉多模态判定**: 将该渲染帧作为多模态图片重新输入 VLM，Prompt 为：
   > “分析当前学生视角图像中的黑板区域是否存在窗户高光倒影？黑板板书字体对比度是否大于 85%？”
4. **决策确认**: VLM 确认反光消除，下发指令写入正式运行日志并向实体硬件下发 CAN 总线电机报文。
