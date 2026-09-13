# -*- coding: utf-8 -*-
import win32com.client
import pythoncom
import array

acad = win32com.client.GetActiveObject('AutoCAD.Application')
doc = acad.ActiveDocument
ms = doc.ModelSpace

# 检查当前 TextStyle
ts = doc.TextStyles.Add('STYLE_CHINESE')
# 使用 SetFont 设置黑体，字符集 134 (GB2312)
try:
    ts.SetFont('黑体', False, False, 134, 0)
    print('SetFont succeeded: 黑体, charset 134')
except Exception as e:
    print('SetFont failed:', e)
    ts.fontFile = r'C:\Windows\Fonts\simhei.ttf'

doc.ActiveTextStyle = ts

# 同时修改 Standard 样式，避免默认样式产生问号
try:
    std = doc.TextStyles.Item('Standard')
    std.SetFont('黑体', False, False, 134, 0)
    print('Standard SetFont succeeded')
except Exception as e:
    print('Standard SetFont fallback to fontFile:', e)
    std.fontFile = r'C:\Windows\Fonts\simhei.ttf'

# 测试写入几个带中文的文本
def pt(x, y, z=0.0):
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, array.array('d', [x, y, z]))

t1 = ms.AddText('【工况一：开启状态（86寸液晶屏外露）】', pt(0, 500, 0), 40)
t1.StyleName = 'STYLE_CHINESE'

t2 = ms.AddText('【工况二：完全覆盖状态（双扇闭合·屏幕完全遮蔽）】', pt(0, 400, 0), 40)
t2.StyleName = 'STYLE_CHINESE'

print('Text added successfully with TextString:', t1.TextString, t2.TextString)
doc.Regen(1)
