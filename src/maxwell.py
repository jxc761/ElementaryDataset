import addlib
import editmxs
import applymxm
import buildframes
import os

# get data path
script_dir = os.path.abspath(os.path.dirname(__file__))
root_dir = os.path.dirname(script_dir)
dn_data = os.path.join(root_dir, "data")


# edit sky and ground setting
print("Editing original studio file")
fn_origin_studio = os.path.join(dn_data, "studio", "studio.mxs")
fn_edited_studio = os.path.join(dn_data, "studio", "studio_edit.mxs")
fn_sky = os.path.join(dn_data, "confs", "default.sky")
fn_ground_mxm = os.path.join(dn_data, "confs", "default.mxm")
editmxs.edit_mxs(fn_origin_studio, fn_sky, fn_ground_mxm, fn_edited_studio)

# generate mxs for different materials
print("Applying materials to studio")
fn_mxs = fn_edited_studio
dn_mxm = os.path.join(dn_data, "mxm")
dn_mxs_mxm = os.path.join(dn_data, "mxs_with_mxm")
applymxm.generate_mxs_with_different_mxm(fn_mxs, dn_mxm, dn_mxs_mxm)

# generate frames
print("generate frames")
fn_camera_conf = os.path.join(dn_data, "confs", "mxcamera.conf.json")
dn_shoot_script = os.path.join(dn_data, "shootscript")
dn_frame_mxs = os.path.join(dn_data, "mxs")
buildframes.build_all(fn_camera_conf, dn_shoot_script, dn_mxs_mxm, dn_frame_mxs)