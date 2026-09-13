# -*- coding: utf-8 -*-
import win32com.client
acad = win32com.client.GetActiveObject("AutoCAD.Application")
print("Open documents count:", acad.Documents.Count)
for doc in acad.Documents:
    print("Doc name:", doc.Name)
