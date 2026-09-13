# -*- coding: utf-8 -*-
import win32com.client
import os

acad = win32com.client.GetActiveObject('AutoCAD.Application')
doc = acad.ActiveDocument

target_file = r"D:\Desktop\pjhb\01-CAD工程图纸\传统市面标准推拉黑板_双状态全覆盖与尺寸标注工程图_v2.1.dwg"
print("Attempting SaveAs:", target_file)

try:
    # 尝试传递 60 (acNative)
    doc.SaveAs(target_file, 60)
    print("SaveAs with 60 succeeded!")
except Exception as e:
    print("SaveAs 60 failed:", e)
    try:
        # 尝试传递无参数
        doc.SaveAs(target_file)
        print("SaveAs without type succeeded!")
    except Exception as e2:
        print("SaveAs without type failed:", e2)
        try:
            # 尝试通过 SendCommand 发送正确流程的 _SAVEAS
            # ESC ESC _SAVEAS \n \n target_path \n
            acad.ActiveDocument.SendCommand("\x1b\x1b_-SAVEAS\n\n" + target_file.replace("\\", "/") + "\n")
            print("SendCommand SAVEAS sent")
        except Exception as e3:
            print("SendCommand failed:", e3)

