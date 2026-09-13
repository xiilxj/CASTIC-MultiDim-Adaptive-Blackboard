# -*- coding: utf-8 -*-
import win32com.client
import pythoncom
import os
import time

pythoncom.CoInitialize()
acad = win32com.client.GetActiveObject("AutoCAD.Application")
doc = acad.ActiveDocument
print("Current Document:", doc.Name)

target_path = r"D:\Desktop\pjhb\01-CAD工程图纸\第二代三维联动自洁防眩光黑板系统_全系统工程总装与运动机构图_v1.0.dwg"
print("Target save path:", target_path)

if os.path.exists(target_path):
    try:
        os.remove(target_path)
    except:
        pass

# 缩放全图居中
acad.ZoomExtents()
print("ZoomExtents executed.")

try:
    doc.SaveAs(target_path)
    print(">>> doc.SaveAs succeeded!")
except Exception as e:
    print("doc.SaveAs failed, trying SendCommand saveas:", e)
    cmd = f'_-SAVEAS\n\n"{target_path}"\n'
    doc.SendCommand(cmd)
    time.sleep(1.0)

time.sleep(0.5)
if os.path.exists(target_path):
    print(">>> Verified DWG file exists! Size:", os.path.getsize(target_path), "bytes")
else:
    print(">>> Warning: target file not found on disk yet.")

