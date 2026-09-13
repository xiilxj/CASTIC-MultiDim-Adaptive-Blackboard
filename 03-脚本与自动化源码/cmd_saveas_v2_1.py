# -*- coding: utf-8 -*-
import win32com.client
import time

acad = win32com.client.GetActiveObject('AutoCAD.Application')
doc = acad.ActiveDocument

target_path = "D:/Desktop/pjhb/01-CAD工程图纸/传统市面标准推拉黑板_双状态全覆盖与尺寸标注工程图_v2.1.dwg"
# AutoCAD 命令行 _SAVEAS
doc.SendCommand("_-SAVEAS\n\n" + target_path + "\n")
time.sleep(1.0)
print("ActiveDoc after saveas:", acad.ActiveDocument.Name)
