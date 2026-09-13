# -*- coding: utf-8 -*-
import win32com.client

acad = win32com.client.GetActiveObject('AutoCAD.Application')
doc = acad.ActiveDocument
print("Current ActiveDoc:", doc.Name)
acad.ZoomExtents()
doc.Regen(1)
doc.Save()
print("Saved and regenerated view successfully.")
