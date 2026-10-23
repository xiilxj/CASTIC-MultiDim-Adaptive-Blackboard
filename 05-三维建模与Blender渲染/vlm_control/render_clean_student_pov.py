import bpy
import time

blend_path = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control\vi7_anti_glare_simulation_v2.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

scene = bpy.context.scene

# Hide all artificial beam meshes so student POV is completely clean!
for obj in bpy.data.objects:
    if "Beam_Danger" in obj.name or "Beam_Sun" in obj.name or "Beam_Safe" in obj.name:
        obj.hide_render = True
        obj.hide_viewport = True
        print(f"Hidden mesh: {obj.name}")

# Set camera to Camera_Student_POV_v2
cam = bpy.data.objects.get("Camera_Student_POV_v2")
scene.camera = cam

# Render settings
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'

# We can use EEVEE or Cycles for high fidelity
scene.render.engine = 'BLENDER_EEVEE'
scene.frame_set(200)

out_file = r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control\preview_sim_v2_student_pov.png"
scene.render.filepath = out_file

print(f"Starting clean student POV render to {out_file} ...")
t0 = time.time()
bpy.ops.render.render(write_still=True)
print(f"Clean student POV render completed in {time.time() - t0:.2f}s!")

# Also copy to preview_sim_student_pov.png
import shutil
shutil.copyfile(out_file, r"D:\Desktop\CASTICpjhb\05-三维建模与Blender渲染\vlm_control\preview_sim_student_pov.png")
print("Copied to preview_sim_student_pov.png successfully!")
