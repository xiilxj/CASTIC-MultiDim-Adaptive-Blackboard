# -*- coding: utf-8 -*-
import win32com.client
import pythoncom

pythoncom.CoInitialize()
acad = win32com.client.GetActiveObject("AutoCAD.Application")
doc = acad.ActiveDocument
print("Active Doc:", doc.Name)
print("Layers count:", doc.Layers.Count)
for lay in doc.Layers:
    print(" - Layer:", lay.Name)
print("Total entities in ModelSpace:", doc.ModelSpace.Count)

