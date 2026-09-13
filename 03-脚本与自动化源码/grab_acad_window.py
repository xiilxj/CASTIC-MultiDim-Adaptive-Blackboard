# -*- coding: utf-8 -*-
from PIL import ImageGrab
import win32gui
import win32con
import time

hwnd = win32gui.FindWindow('AutoCAD', None)
if not hwnd:
    # 枚举寻找包含 AutoCAD 的窗口
    def enum_cb(h, extra):
        title = win32gui.GetWindowText(h)
        if 'AutoCAD' in title and win32gui.IsWindowVisible(h):
            extra.append(h)
    hwnds = []
    win32gui.EnumWindows(enum_cb, hwnds)
    if hwnds:
        hwnd = hwnds[0]

if hwnd:
    print('Found AutoCAD HWND:', hwnd, win32gui.GetWindowText(hwnd))
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.5)
    bbox = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox)
    out_path = r'D:\Desktop\pjhb-CAD工程图纸cad_test_screenshot.png'
    img.save(out_path)
    print('Screenshot saved to:', out_path)
else:
    print('AutoCAD window not found by title')
