# -*- coding: utf-8 -*-
import win32com.client
import os
import time

acad = win32com.client.GetActiveObject("AutoCAD.Application")
target_name = "第一代翻转式多媒体黑板_全系统标准工程参数与尺寸标注工程图_v1.4.dwg"
target_path = r"D:\Desktop\pjhb\01-CAD工程图纸\第一代翻转式多媒体黑板_全系统标准工程参数与尺寸标注工程图_v1.4.dwg"

# 找到旧的 v1.4 文档并关闭
for doc in list(acad.Documents):
    if "v1.4" in doc.Name:
        print("Closing existing v1.4 doc:", doc.Name)
        doc.Close(False)
        time.sleep(0.5)

# 此时活动文档为最新的 Drawing5
active_doc = acad.ActiveDocument
print("Active Document to save:", active_doc.Name)
active_doc.SaveAs(target_path)
print("Saved to target_path successfully!")
acad.ZoomExtents()
print("ZoomExtents done.")
