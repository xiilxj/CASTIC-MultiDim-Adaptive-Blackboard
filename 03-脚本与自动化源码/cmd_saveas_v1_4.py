# -*- coding: utf-8 -*-
import win32com.client
import time
import os

acad = win32com.client.GetActiveObject('AutoCAD.Application')
doc = acad.ActiveDocument
print("Current Active Document:", doc.Name)

target_path = "D:/Desktop/pjhb/01-CAD工程图纸/第一代翻转式多媒体黑板_全系统标准工程参数与尺寸标注工程图_v1.4.dwg"
if os.path.exists(target_path):
    try:
        os.remove(target_path)
    except:
        pass

# 使用 AutoCAD 命令行 _-SAVEAS 保存
doc.SendCommand("_-SAVEAS\n\n" + target_path + "\n")
time.sleep(1.5)
print("Saved DWG. Current ActiveDoc:", acad.ActiveDocument.Name)
