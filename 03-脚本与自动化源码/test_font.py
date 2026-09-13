# -*- coding: utf-8 -*-
import win32com.client
import os

try:
    acad = win32com.client.GetActiveObject('AutoCAD.Application')
    doc = acad.ActiveDocument
    print('AutoCAD Active Document:', doc.Name)
    
    styles = [s.Name for s in doc.TextStyles]
    print('Existing TextStyles:', styles)
    
    font_paths = [
        r'C:\Windows\Fonts\simhei.ttf',
        r'C:\Windows\Fonts\msyh.ttc',
        r'C:\Windows\Fonts\simsun.ttc'
    ]
    chosen_font = None
    for fp in font_paths:
        if os.path.exists(fp):
            chosen_font = fp
            print('Found font file:', fp)
            break
            
    style_name = 'ENGINEERING_CN'
    try:
        ts = doc.TextStyles.Item(style_name)
    except:
        ts = doc.TextStyles.Add(style_name)
        
    ts.fontFile = chosen_font if chosen_font else 'simhei.ttf'
    doc.ActiveTextStyle = ts
    print('Successfully set ActiveTextStyle to:', style_name, 'with font:', ts.fontFile)
    
    try:
        std_ts = doc.TextStyles.Item('Standard')
        std_ts.fontFile = chosen_font if chosen_font else 'simhei.ttf'
        print('Updated Standard TextStyle fontFile to:', std_ts.fontFile)
    except Exception as e:
        print('Error updating Standard TextStyle:', e)
        
    doc.Regen(1)
    print('Regen completed successfully.')

except Exception as e:
    import traceback
    traceback.print_exc()
