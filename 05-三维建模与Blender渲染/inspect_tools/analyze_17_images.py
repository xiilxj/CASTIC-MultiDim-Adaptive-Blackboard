import os
from PIL import Image
import numpy as np

img_dir = "/mnt/d/Desktop/CASTICpjhb/17"
out_dir = "/mnt/d/Desktop/CASTICpjhb/05-三维建模与Blender渲染/inspect_tools/thumbs"
os.makedirs(out_dir, exist_ok=True)

files = sorted([f for f in os.listdir(img_dir) if f.endswith('.png')])

for f in files:
    path = os.path.join(img_dir, f)
    with Image.open(path) as img:
        w, h = img.size
        mode = img.mode
        print(f"File: {f}, Size: {w}x{h}, Mode: {mode}")
        
        # 转换为 RGB 后保存缩略图
        thumb = img.convert('RGB')
        thumb.thumbnail((640, 480))
        thumb_path = os.path.join(out_dir, f"thumb_{f}.jpg")
        thumb.save(thumb_path, "JPEG", quality=85)
        print(f"  Saved thumb to: {thumb_path}")

