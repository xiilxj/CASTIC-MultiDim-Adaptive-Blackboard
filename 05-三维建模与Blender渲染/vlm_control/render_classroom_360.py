import bpy
import time

t0 = time.time()
blend_path = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control\vi7_anti_glare_simulation_v2.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 16
scene.cycles.adaptive_threshold = 0.1
scene.render.resolution_x = 2048
scene.render.resolution_y = 1024
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'

# Create or reuse 360 Panorama camera at center of classroom
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

# Set camera location to center aisle of classroom at human standing eye height
# Classroom X spans -4.2 to 4.2 (center aisle 0.0), Y spans 0.0 (blackboard) to -8.0 (back wall)
# Middle seating center Y = -4.2, standing eye height Z = 0.20 (1.6m above floor Z=-1.4)
cam_obj.location = (0.0, -4.2, 0.20)
cam_obj.rotation_mode = 'XYZ'
cam_obj.rotation_euler = (1.5707963, 0.0, 0.0) # Look forward towards +Y blackboard

scene.camera = cam_obj
scene.frame_set(200)

out_path = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control\blender_classroom_360_panorama.png"
scene.render.filepath = out_path

print(f"Starting 360 Cycles render to {out_path} ...")
bpy.ops.render.render(write_still=True)
print(f"Render finished in {time.time() - t0:.2f} seconds!")
