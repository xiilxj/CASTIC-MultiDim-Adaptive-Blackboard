# -*- coding: utf-8 -*-
import win32com.client
import pythoncom
import array
import os

acad = win32com.client.GetActiveObject('AutoCAD.Application')
doc = acad.ActiveDocument
ms = doc.ModelSpace

# 确保中文字体样式存在并激活
style_name = 'ENGINEERING_CN'
try:
    ts = doc.TextStyles.Item(style_name)
except:
    ts = doc.TextStyles.Add(style_name)

ts.fontFile = r'C:\Windows\Fonts\simhei.ttf'
doc.ActiveTextStyle = ts

def pt(x, y, z=0.0):
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, array.array('d', [x, y, z]))

# 添加一段测试文字
txt = ms.AddText('中文测试：标准推拉黑板完全覆盖状态', pt(0, -200, 0), 40)
txt.StyleName = style_name
print('Added test text successfully with style:', style_name)

# 尝试用 AddMText
mtxt = ms.AddMText(pt(0, -300, 0), 2000, '多行文本测试：86寸液晶一体机推拉覆盖机构')
mtxt.Height = 40
mtxt.StyleName = style_name
print('Added test MText successfully')

doc.Regen(1)
