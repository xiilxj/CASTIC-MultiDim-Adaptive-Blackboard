# -*- coding: utf-8 -*-
import win32com.client
import pythoncom
import array

acad = win32com.client.GetActiveObject('AutoCAD.Application')
doc = acad.ActiveDocument
ms = doc.ModelSpace

doc.SetVariable('DIMTXSTY', 'STYLE_CHINESE')
doc.SetVariable('DIMTXT', 25.0)  # 文字高度 25
doc.SetVariable('DIMASZ', 20.0)  # 箭头大小 20

def pt(x, y, z=0.0):
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, array.array('d', [x, y, z]))

dim = ms.AddDimRotated(pt(0, 0), pt(1000, 0), pt(500, 100), 0.0)
dim.TextOverride = '1000 (左活动板)'
dim.TextStyle = 'STYLE_CHINESE'
print('Dimension text style set successfully:', dim.TextStyle, dim.TextOverride)
doc.Regen(1)
