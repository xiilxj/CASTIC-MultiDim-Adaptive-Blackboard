# -*- coding: utf-8 -*-
import os, sys
script_dir = os.path.dirname(os.path.abspath(__file__))
target_script = os.path.join(script_dir, "03-脚本与自动化源码", "draw_gen3_blackboard_system_v1_1.py")
with open(target_script, "r", encoding="utf-8") as f:
    code = f.read()
exec(code, {"__name__": "__main__", "__file__": target_script})
