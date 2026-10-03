#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================================================================
第42届瑞安市青少年科技创新大赛 (CASTIC) 参赛重点攻坚工程
模块名称: 第三代（Z系列）多维叠合翻转黑板与端侧 VLM 数字孪生光环境动态控光桥接中枢
审核标识: 第 22 轮工程技术审核
========================================================================================
功能定位:
  1. 接收来自教师/管理人员的自然语言控制指令 (如 "阳光直射黑板产生严重眩光，展开避光" / "需要大板书，遮蔽保护大屏")；
  2. 模拟端侧轻量化多模态视觉模型 (如 Qwen2.5-VL-3B-Instruct) 对教室内反光斑与学生视线姿态的推理；
  3. 精准映射为第三代三大标准工况与动态参数:
     - 工况一 (COVERED): Fold=180°, 100% 遮蔽保护 86寸大屏，4000mm 连续墨绿黑板；
     - 工况二 (COMPACT): Fold=0°, 双层紧密贴合(26mm)，86寸大屏全景露出；
     - 工况三 (DEPLOYED): Slide=1.0m, Yaw=14°, Pitch=-8°, Fold=0°, 整体双层板外滑并偏航俯仰避光；
  4. 生成直接驱动 Blender 运行时母本工程 (Z_Series_Master.blend) 的精确 Python 控制指令。
========================================================================================
"""

import json
import math
import sys
import os

class VLMZSeriesClassroomBridge:
    def __init__(self):
        # 第三代当前系统状态缓存
        self.state = {
            "work_mode": "COMPACT",        # "COVERED", "COMPACT", "DEPLOYED"
            "slide_m": 0.0,                # 左右外滑行程 (0.0 ~ 1.0m)
            "yaw_deg": 0.0,                # 翻转主铰链偏航角 (-20° ~ +20°)
            "pitch_deg": 0.0,              # 纵向俯仰避光角 (-15° ~ +15°)
            "fold_deg": 0.0,               # 外层折叠铺开角 (0°=贴合露屏, 180°=向内铺平封屏)
            "canopy_tilt": 0.0,            # 遮阳平檐倾角 (恒定 0.0° 平檐)
            "sunblind_level": 20.0,        # 侧窗电动卷帘遮蔽度 (0% ~ 100%)
            "board_wash_light_w": 140.0,   # 黑板漫反射专用洗墙灯功率 (W)
            "glare_risk_level": "LOW"      # 眩光风险评估
        }

    def process_natural_language_intent(self, text_prompt: str) -> dict:
        """
        接收自然语言请求或视觉传感器检测事件，输出多模态推理决策
        """
        print(f"\n[VLM Bridge] 收到输入事件: '{text_prompt}'")
        decision = {}
        
        # 1. 眩光与反光避光场景 -> 触发工况三 (大视野与空间避光)
        if any(kw in text_prompt for kw in ["反光", "眩光", "晃眼", "看不清", "眯眼", "避光", "侧滑", "大视野"]):
            decision = {
                "intent": "DEPLOYED_ANTIGLARE_MODE",
                "work_mode": "DEPLOYED",
                "slide_m": 1.0,
                "yaw_deg": 14.0,
                "pitch_deg": -8.0,
                "fold_deg": 0.0, # 双层紧密贴合
                "canopy_tilt": 0.0,
                "sunblind_level": 75.0,
                "board_wash_light_w": 220.0,
                "glare_risk_level": "HIGH_MITIGATED",
                "reasoning": "VLM检测到侧窗斜射日光在黑板产生镜面高光反射。触发工况三：双横梁外滑1.0m，整组双层黑板绕外侧铰链偏航14°并俯仰-8°，将直射光反射至天花板无人区；侧窗卷帘下放至75%，专用洗墙灯提升至220W洗平光场。"
            }
            
        # 2. 传统全黑板大板书需求 -> 触发工况一 (全覆盖封屏形态)
        elif any(kw in text_prompt for kw in ["全黑板", "封屏", "全覆盖", "遮住大屏", "保护大屏", "传统板书", "大板书"]):
            decision = {
                "intent": "FULL_COVERAGE_CHALKBOARD_MODE",
                "work_mode": "COVERED",
                "slide_m": 0.0,
                "yaw_deg": 0.0,
                "pitch_deg": 0.0,
                "fold_deg": 180.0, # 外层板绕内侧对角线铰链回转 180° 对接
                "canopy_tilt": 0.0,
                "sunblind_level": 20.0,
                "board_wash_light_w": 180.0,
                "glare_risk_level": "LOW",
                "reasoning": "教师需求大面积纯黑板书写。触发工况一：外层折叠板绕【外面的内侧铰链】向中心回转180°铺展对接，100%遮蔽保护86寸液晶大屏，全系统呈现4000mm连续无缝墨绿黑板。"
            }
            
        # 3. 多媒体标准教学 / 露大屏需求 -> 触发工况二 (常态多媒体双层叠合)
        elif any(kw in text_prompt for kw in ["大屏", "看视频", "多媒体", "课件", "常态", "露屏", "复位"]):
            decision = {
                "intent": "COMPACT_MULTIMEDIA_MODE",
                "work_mode": "COMPACT",
                "slide_m": 0.0,
                "yaw_deg": 0.0,
                "pitch_deg": 0.0,
                "fold_deg": 0.0, # 回折叠合
                "canopy_tilt": 0.0,
                "sunblind_level": 30.0,
                "board_wash_light_w": 140.0,
                "glare_risk_level": "LOW",
                "reasoning": "教师进行多媒体授课。触发工况二：外层板回折180°与内层主板磁吸贴合（总厚26mm），86寸4K大屏全景裸露显现，左右各保留1000mm双层黑板板书区。"
            }
            
        # 4. 超宽全景板书与多媒体同屏 (工况三之二：外滑1m且折叠板回填180°)
        elif any(kw in text_prompt for kw in ["回填", "掰开", "全景板书", "连贯", "填满", "6米", "超宽板书", "同屏"]):
            decision = {
                "intent": "DEPLOYED_FILLED_PANORAMIC_MODE",
                "work_mode": "DEPLOYED_FILLED",
                "slide_m": 1.0,
                "yaw_deg": 0.0,
                "pitch_deg": 0.0,
                "fold_deg": 180.0, # 外层折叠板向内回折 180° 填补 1000mm 空缺
                "canopy_tilt": 0.0,
                "sunblind_level": 30.0,
                "board_wash_light_w": 200.0,
                "glare_risk_level": "LOW",
                "reasoning": "教师进行高密度大板书与多媒体协同授课。触发工况三之二：左右双翼外滑1.0m，折叠板绕内侧对角线铰链向内回转180°填补空缺，形成左2m板书+中2m大屏+右2m板书的6000mm满幅无缝连贯教学巨幕。"
            }
            
        else:
            decision = {
                "intent": "DEFAULT_STANDBY_MODE",
                "work_mode": "COMPACT",
                "slide_m": 0.0,
                "yaw_deg": 0.0,
                "pitch_deg": 0.0,
                "fold_deg": 0.0,
                "canopy_tilt": 0.0,
                "sunblind_level": 10.0,
                "board_wash_light_w": 120.0,
                "glare_risk_level": "NORMAL",
                "reasoning": "维持常态自适应基准状态。"
            }
            
        self.state.update({k: v for k, v in decision.items() if k in self.state})
        return decision

    def generate_blender_injection_code(self, decision: dict) -> str:
        """
        生成可直接注入到 Blender 运行时的动力学控制脚本片段
        """
        slide = decision.get("slide_m", 0.0)
        yaw = decision.get("yaw_deg", 0.0)
        pitch = decision.get("pitch_deg", 0.0)
        fold = decision.get("fold_deg", 0.0)
        
        script = f"""# === VLM 动态注入控制命令: {decision.get('intent')} ===
import bpy, math

# 查找第三代机构控制器
ctrl_slide_l = bpy.data.objects.get("GuangHeng_Z_System_Ctrl_Slide_Left")
ctrl_slide_r = bpy.data.objects.get("GuangHeng_Z_System_Ctrl_Slide_Right")
ctrl_flip_l = bpy.data.objects.get("GuangHeng_Z_System_Ctrl_Flip_Left")
ctrl_flip_r = bpy.data.objects.get("GuangHeng_Z_System_Ctrl_Flip_Right")
ctrl_fold_l = bpy.data.objects.get("GuangHeng_Z_System_Ctrl_Fold_Left")
ctrl_fold_r = bpy.data.objects.get("GuangHeng_Z_System_Ctrl_Fold_Right")

screen_w = 1.98
board_w = 0.99
base_x = screen_w/2 + board_w/2 + 0.01

# 1. 侧滑滑移平移 (0.0 ~ 1.0m)
if ctrl_slide_l and ctrl_slide_r:
    ctrl_slide_l.location.x = - (base_x + {slide})
    ctrl_slide_r.location.x = + (base_x + {slide})

# 2. 对角线外侧翻转主铰链 (里面的外侧: 偏航 Yaw 与 俯仰 Pitch)
if ctrl_flip_l and ctrl_flip_r:
    ctrl_flip_l.rotation_euler = (math.radians({pitch}), 0, -math.radians({yaw}))
    ctrl_flip_r.rotation_euler = (math.radians({pitch}), 0, +math.radians({yaw}))

# 3. 对角线内侧折叠铺开铰链 (外面的内侧: 0° 叠合 / 180° 封屏)
if ctrl_fold_l and ctrl_fold_r:
    ctrl_fold_l.rotation_euler = (0, 0, math.radians({fold}))
    ctrl_fold_r.rotation_euler = (0, 0, -math.radians({fold}))

print(">> [VLM Driver] 成功同步姿态: Mode={decision.get('work_mode')}, Slide={slide}m, Yaw={yaw}°, Pitch={pitch}°, Fold={fold}°")
"""
        return script

def run_self_test():
    """桥接模块自测验证"""
    bridge = VLMZSeriesClassroomBridge()
    test_prompts = [
        "靠窗座位的同学反馈侧面太阳太刺眼，屏幕反光看不清，请执行避光",
        "老师现在要写满满一整面的大板书，需要把大屏完全盖住保护起来",
        "我们要开始看教学课件和视频了，请打开大屏",
        "黑板推出去展开后，把折叠板向内掰开回填填满空缺，开启超宽全景板书同屏教学"
    ]
    
    for prompt in test_prompts:
        decision = bridge.process_natural_language_intent(prompt)
        print("决策输出:", json.dumps(decision, ensure_ascii=False, indent=2))
        injection_code = bridge.generate_blender_injection_code(decision)
        print("生成的 Blender 注入驱动代码前 3 行:")
        print("\n".join(injection_code.splitlines()[:5]))
        print("-" * 60)

if __name__ == "__main__":
    run_self_test()
