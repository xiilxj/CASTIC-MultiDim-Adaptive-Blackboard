# -*- coding: utf-8 -*-
import win32com.client
import os

acad = win32com.client.GetActiveObject('AutoCAD.Application')
doc = acad.ActiveDocument
print("Active Document:", doc.Name)

target_path = r"D:\Desktop\pjhb\01-CAD工程图纸\第一代翻转式多媒体黑板_全系统标准工程参数与尺寸标注工程图_v1.4.dwg"
try:
    doc.SaveAs(target_path)
    print("doc.SaveAs(target_path) succeeded!")
except Exception as e:
    print("doc.SaveAs(target_path) failed:", e)

