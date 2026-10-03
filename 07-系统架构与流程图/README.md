# 07-系统架构与流程图 (System Architecture & Flowcharts)

本目录为 CASTIC 全国青少年科技创新大赛 · 光衡 (GH-VI-2026) 项目的**高精度矢量流程图与架构图资产库**。
所有图表均由各阶段核心技术规划方案（Plan）与工程实现拓扑导出为独立、无损、自包含的现代化 SVG 矢量图文件。

---

## 📊 核心图表资产索引

| 序号 | 图表名称 | 对应规划文档 (Plan) | 矢量文件路径 | 核心内容与技术拓扑 |
| :--- | :--- | :--- | :--- | :--- |
| **01** | **VI 系列多维叠合翻转黑板全生命周期时序拓扑** | `castic_blender_gen3_vi_series_animation_plan.md` | [`svg/01_vi_series_kinematic_sequence.svg`](file:///mnt/d/Desktop/CASTICpjhb/07-系统架构与流程图/svg/01_vi_series_kinematic_sequence.svg) | 时序图：完全遮蔽形态 (Covered) $\to$ 退回露屏常态 (Compact) $\to$ 避光偏航 (Yaw) $\to$ 外伸极限展开 (6000mm Panoramic) 四大阶段状态流转 |
| **02** | **第三代 Z 系列多维叠合黑板物理拓扑装配与运动学求解主流程** | `castic_blender_gen3_z_series_master_plan.md` | [`svg/02_z_series_assembly_pipeline.svg`](file:///mnt/d/Desktop/CASTICpjhb/07-系统架构与流程图/svg/02_z_series_assembly_pipeline.svg) | 流程图：参数化装配、26mm 双层贴合板、对角线双铰链正交解耦、自洁滑槽、PBR 材质校准到 4K 批量渲染的全流水线 |
| **03** | **端侧 VLM 智能闭环与 Bambu 物理样机制造双轨工程总架构** | `castic_blender_vlm_bambu_implementation_plan.md` | [`svg/03_vlm_bambu_dual_track_architecture.svg`](file:///mnt/d/Desktop/CASTICpjhb/07-系统架构与流程图/svg/03_vlm_bambu_dual_track_architecture.svg) | 架构图：端侧 Qwen2.5-VL 多任务中枢赋能，分支一驱动 Blender 3D 活体视口数字孪生，分支二指导 1:10 拓竹 3D 打印物理实体样机制造 |
| **04** | **GH-VI-2026 伪 VR 沉浸式真机活体交互数字孪生系统全链路闭环图** | `VI系列开发记录.md` (第 35~39 轮) | [`svg/04_gh_vi_live_digital_twin_closed_loop.svg`](file:///mnt/d/Desktop/CASTICpjhb/07-系统架构与流程图/svg/04_gh_vi_live_digital_twin_closed_loop.svg) | 全链路闭环图：多相机输入 $\to$ 眯眼/强光毫秒级特征提取 $\to$ Agent 自然语言工具调用 $\to$ IPC 共享状态 $\to$ Blender 60 FPS 物理视口联动 |

---

## 🛠️ 重新生成与维护说明

本目录下所有矢量图可通过同目录下的 Python 脚本无依赖快速重新构建：
```bash
python generate_all_plan_svgs.py
```
生成的 SVG 文件支持在任何现代浏览器、Markdown 查看器、Inkscape、Illustrator 或 Typst 学术排版系统中无损导入与印刷级排版。
