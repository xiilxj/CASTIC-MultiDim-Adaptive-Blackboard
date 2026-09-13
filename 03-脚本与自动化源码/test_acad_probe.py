# -*- coding: utf-8 -*-
import win32com.client
import pythoncom
import time

print("Probe 1: Initializing COM...")
pythoncom.CoInitialize()
print("Probe 2: Getting ActiveObject AutoCAD.Application...")
acad = win32com.client.GetActiveObject("AutoCAD.Application")
print("Probe 3: AutoCAD Version:", acad.Version)
print("Probe 4: ActiveDocument:", acad.ActiveDocument.Name)
doc = acad.ActiveDocument
ms = doc.ModelSpace
print("Probe 5: ModelSpace Count:", ms.Count)
print("Probe OK!")
