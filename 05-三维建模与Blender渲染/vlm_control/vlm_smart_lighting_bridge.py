# -*- coding: utf-8 -*-
"""
========================================================================================
第42届瑞安市青少年科技创新大赛 (CASTIC) 参赛重点攻坚工程
模块名称: 端侧多模态 VLM (Qwen2.5-VL) 与 Blender 数字孪生光环境动态控光桥接中枢
审核标识: 第 21 轮工程技术审核
========================================================================================
功能定位:
  1. 接收来自教师/管理人员的自然语言控制指令 (如 "右后方同学被反光晃眼，调整黑板并调暗侧窗")；
  2. 模拟端侧 VLM (如 Qwen2.5-VL-3B-Instruct) 对教室内实时视频流的视觉分析推理结果；
  3. 计算最佳抗眩光与视线聚拢决策，并通过 Blender Python 驱动接口毫秒级操控三维机构与光场。
========================================================================================
"""

import json
import math
import time

class VLMClassroomControlBridge:
    def __init__(self):
        self.state = {
            "canopy_angle": 0.0,       # 遮阳挑檐顶盖开合角 (0°~45°)
            "screen_yaw": 0.0,          # 86寸大屏偏航避光角 (-15°~+15°)
            "sub_board_tilt": 0.0,      # 外侧副板向前聚拢角 (0°~35°)
            "sunblind_level": 0.0,      # 智能电动卷帘放下程度 (0%~100%)
            "wallwasher_power": 120.0,  # 防眩漫反射洗墙灯功率 (W)
            "glare_risk": "LOW"
        }
        
    def process_natural_language_intent(self, text_prompt: str) -> dict:
        """
        解析自然语言控光指令并映射为多模态推理决策
        """
        print(f"\n[VLM Bridge] 收到自然语言控制请求: '{text_prompt}'")
        decision = {}
        
        if "反光" in text_prompt or "眩光" in text_prompt or "看不清" in text_prompt or "眯眼" in text_prompt:
            decision = {
                "intent": "GLARE_AVOIDANCE_RECONFIGURATION",
                "canopy_angle": 38.0,
                "screen_yaw": 5.0,
                "sub_board_tilt": 28.0,
                "sunblind_level": 75.0,
                "wallwasher_power": 240.0,
                "glare_risk": "HIGH_MITIGATED",
                "reasoning": "检测到强烈侧窗入射日光与学生视觉眩光反馈，执行四阶复合避光: 顶挑遮阳罩+大屏5°偏航+副板向内聚拢28°+卷帘降至75%+洗墙灯240W漫射洗平。"
            }
        elif "板书" in text_prompt or "写字" in text_prompt or "平展" in text_prompt:
            decision = {
                "intent": "MAXIMUM_WRITING_SURFACE_DEPLOY",
                "canopy_angle": 0.0,
                "screen_yaw": 0.0,
                "sub_board_tilt": 0.0,
                "sunblind_level": 30.0,
                "wallwasher_power": 160.0,
                "glare_risk": "LOW",
                "reasoning": "教师需求大面积板书书写，两翼副板与主绿板水平展开锁定，洗墙灯开启高显色护眼模式。"
            }
        elif "投影" in text_prompt or "看视频" in text_prompt or "大屏" in text_prompt:
            decision = {
                "intent": "CINEMATIC_DISPLAY_FOCUS",
                "canopy_angle": 42.0,
                "screen_yaw": 0.0,
                "sub_board_tilt": 15.0,
                "sunblind_level": 90.0,
                "wallwasher_power": 60.0,
                "glare_risk": "VERY_LOW",
                "reasoning": "进入多媒体大屏授课模式，卷帘下放90%阻断室外眩光，顶部遮阳罩极限展开阻绝顶灯杂散光。"
            }
        else:
            decision = {
                "intent": "DEFAULT_ENERGY_SAVING",
                "canopy_angle": 0.0,
                "screen_yaw": 0.0,
                "sub_board_tilt": 0.0,
                "sunblind_level": 0.0,
                "wallwasher_power": 120.0,
                "glare_risk": "NORMAL",
                "reasoning": "维持全自动自适应基准工作状态。"
            }
            
        self.state.update({k: v for k, v in decision.items() if k in self.state})
        return decision

    def generate_blender_driver_script(self, decision: dict) -> str:
        """
        生成可直接注入到 Blender 后台运行时的指令片段
        """
        script = f"""
# 动态注入 Blender 控制命令
import bpy, math
top = bpy.data.objects.get("Top_System_AvoidGlare")
if top:
    canopy = bpy.data.objects.get("Top_System_AvoidGlare_Display_Canopy_Pivot")
    screen = bpy.data.objects.get("Top_System_AvoidGlare_Display")
    left_sub = bpy.data.objects.get("Top_System_AvoidGlare_SubBoard_Left")
    right_sub = bpy.data.objects.get("Top_System_AvoidGlare_SubBoard_Right")
    washer = bpy.data.lights.get("VLM_Wallwasher_Area")
    
    if canopy: canopy.rotation_euler.x = math.radians(-{decision.get('canopy_angle', 0.0)})
    if screen: screen.rotation_euler.y = math.radians({decision.get('screen_yaw', 0.0)})
    if left_sub: left_sub.rotation_euler.y = math.radians({decision.get('sub_board_tilt', 0.0)})
    if right_sub: right_sub.rotation_euler.y = math.radians(-{decision.get('sub_board_tilt', 0.0)})
    if washer: washer.energy = {decision.get('wallwasher_power', 120.0)}
print("[Blender Twin] 机构与光场姿态已根据 VLM 决策实时同步！")
"""
        return script

if __name__ == "__main__":
    bridge = VLMClassroomControlBridge()
    test_queries = [
        "靠窗第3排有同学眯着眼睛看不清中间屏幕，反光太严重了！",
        "现在要开始全黑板板书推导演算，把副板全部平铺展开",
        "切换到大屏电影教学课件模式，降低室内光线"
    ]
    for q in test_queries:
        res = bridge.process_natural_language_intent(q)
        print("决策输出:", json.dumps(res, ensure_ascii=False, indent=2))
        time.sleep(0.5)
