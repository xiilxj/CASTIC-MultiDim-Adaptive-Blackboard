import bpy
import time

t0 = time.time()
blend_path = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control\vi7_anti_glare_simulation_v2.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'

# Enable oneAPI GPU
cprefs = bpy.context.preferences.addons['cycles'].preferences
try:
    cprefs.compute_device_type = 'ONEAPI'
    cprefs.get_devices()
    for d in cprefs.devices:
        if d.type == 'ONEAPI':
            d.use = True
            print(f"Enabled oneAPI device: {d.name}")
    scene.cycles.device = 'GPU'
except Exception as e:
    print(f"oneAPI setup error (fallback to CPU): {e}")
    scene.cycles.device = 'CPU'

scene.cycles.samples = 16
scene.cycles.adaptive_threshold = 0.1
scene.render.resolution_x = 2048
scene.render.resolution_y = 1024
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'

# Camera setup
cam_name = "Camera_360_Panorama"
cam_obj = bpy.data.objects.get(cam_name)
if not cam_obj:
    cam_data = bpy.data.cameras.new(name=cam_name)
    cam_obj = bpy.data.objects.new(name=cam_name, object_data=cam_data)
    scene.collection.objects.link(cam_obj)

cam_data = cam_obj.data
cam_data.type = 'PANO'
cam_data.panorama_type = 'EQUIRECTANGULAR'
cam_data.clip_start = 0.05
cam_data.clip_end = 200.0
cam_obj.location = (0.0, -4.2, 0.20)
cam_obj.rotation_mode = 'XYZ'
cam_obj.rotation_euler = (1.5707963, 0.0, 0.0)

scene.camera = cam_obj

# We want to render Frame 1 and Frame 480
for frame_num in [1, 480]:
    t_start = time.time()
    scene.frame_set(frame_num)
    out_file = fr"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control\blender_classroom_360_frame{frame_num:03d}.png"
    scene.render.filepath = out_file
    print(f"--- Rendering 360 Pano Frame {frame_num} to {out_file} ---")
    bpy.ops.render.render(write_still=True)
    print(f"Frame {frame_num} completed in {time.time() - t_start:.2f}s!")

print(f"All keyframe panos completed in {time.time() - t0:.2f}s total!")
