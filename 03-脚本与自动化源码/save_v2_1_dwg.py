# -*- coding: utf-8 -*-
import win32com.client
import shutil
import os

acad = win32com.client.GetActiveObject('AutoCAD.Application')
doc = acad.ActiveDocument
doc.Save()
print('Current document saved.')

src = r'D:\Desktop\pjhb-CAD工程图纸\传统市面标准推拉黑板_无涂色工程尺寸标注图_v2.0.dwg'
dst = r'D:\Desktop\pjhb-CAD工程图纸\传统市面标准推拉黑板_双状态全覆盖与尺寸标注工程图_v2.1.dwg'

if os.path.exists(src):
    shutil.copyfile(src, dst)
    print('Copied to dst successfully:', dst)
else:
    print('Src not found:', src)
