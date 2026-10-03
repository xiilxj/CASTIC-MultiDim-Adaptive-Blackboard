#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证 vi1.blend 中动画关键帧与控制器数据的完整性
"""
import bpy
import sys

def verify():
    print("=" * 60)
    print(">> [Verify] 开始校验 vi1.blend 动画关键帧完整性...")
    print("=" * 60)
    
    controllers = [
        "Ctrl_Rod_Inward_Left", "Ctrl_Rod_Inward_Right",
        "Ctrl_Slide_Left", "Ctrl_Slide_Right",
        "Ctrl_Flip_Left", "Ctrl_Flip_Right",
        "Ctrl_Rod_Outward_Left", "Ctrl_Rod_Outward_Right",
        "Ctrl_Fold_Left", "Ctrl_Fold_Right",
        "Camera_VI_Main"
    ]
    
    missing_objs = []
    keyframes_summary = {}
    
    for c_name in controllers:
        obj = bpy.data.objects.get(c_name)
        if not obj:
            missing_objs.append(c_name)
            continue
        
        frames = set()
        if obj.animation_data and obj.animation_data.action:
            act = obj.animation_data.action
            # 遍历 fcurves
            fcurves = getattr(act, 'fcurves', None)
            if fcurves:
                for fc in fcurves:
                    for kp in fc.keyframe_points:
                        frames.add(int(round(kp.co[0])))
            # 如果是 Blender 5.0 layers/curves
            elif hasattr(act, 'curves'):
                for c in act.curves:
                    for kp in c.keyframe_points:
                        frames.add(int(round(kp.co[0])))
        keyframes_summary[c_name] = sorted(list(frames))
        
    print(f">> 缺失控制器数量: {len(missing_objs)}")
    if missing_objs:
        print(f">> 缺失列表: {missing_objs}")
        
    for name, f_list in keyframes_summary.items():
        print(f"  - 控制器 [{name}]: 关键帧点位数量={len(f_list)}, 关键帧分布={f_list}")
        
    scene = bpy.context.scene
    print(f">> 场景总帧区间: Start={scene.frame_start}, End={scene.frame_end}, FPS={scene.render.fps}")
    print("=" * 60)
    print(">> [Verify] 校验完成！")

if __name__ == '__main__':
    verify()
