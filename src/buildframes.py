
from pymaxwell import *
from mxshooter import CMxShooter
import shutil
import json
import glob
import utils

def build_mx_shooter(fn_camera_conf, fn_shoot_script):
	camera_parameters = {}

	with open(fn_camera_conf) as json_data:
		camera_parameters = json.load(json_data)

	shoot_script = {}

	with open(fn_shoot_script) as json_data:
		shoot_script = json.load(json_data)
	
	
	shooter = CMxShooter(camera_parameters, shoot_script)
	
	return shooter
	
def build_all(fn_camera_conf, dn_shoot_script, dn_mxs_mxm, dn_root_output):
	shootscripts = glob.glob(os.path.join(dn_shoot_script, "*.ss.json") )
	
	# clear dn_root_output
	if os.path.exists(dn_root_output):
		shutil.rmtree(dn_root_output)
	os.mkdir(dn_root_output)
	
	mxm_dir_list = [ os.path.join(dn_mxs_mxm, name) 
					for name in os.listdir(dn_mxs_mxm)
						if os.path.isdir(os.path.join(dn_mxs_mxm, name)) ]
						
	for fn_cur_shoot_script in shootscripts:
		basename = os.path.basename(fn_cur_shoot_script)
		ss_name, ext = os.path.splitext(basename)
		ss_name, ext = os.path.splitext(ss_name)
		
		dn_cur_output = os.path.join(dn_root_output, ss_name)
		os.mkdir(dn_cur_output)
		
		# iterate all mxm
		for cur_mxm_dir in mxm_dir_list:
			basename = os.path.basename(cur_mxm_dir)
			mxm_name, ext  =  os.path.splitext(basename)
			
			fn_studio = os.path.join(cur_mxm_dir, "studio.mxs")
			dn_output = os.path.join(dn_cur_output, mxm_name)
	
			build_seqence(fn_studio, fn_cur_shoot_script, fn_camera_conf, dn_output)
	
def build_seqence(fn_studio, fn_shoot_script, fn_camera_conf, dn_output):
	# load shoot script in
	dn_input = os.path.dirname(fn_studio)
	
	# clear dn_root_output
	if os.path.exists(dn_output):
		shutil.rmtree(dn_output)
	os.mkdir(dn_output)
	
	# build maxwell shooter 
	shooter = build_mx_shooter(fn_camera_conf, fn_shoot_script)
	numb_of_frames = shooter.numb_of_frames()
	
	# copy dependencies to dn_output
	utils.copy_dependencies(fn_studio, dn_output)
	
	# build frames
	for iframe in range(numb_of_frames):
		fn_cur_mxs = os.path.join(dn_output, "frame{0}.mxs".format(iframe))
		shutil.copyfile(fn_studio, fn_cur_mxs)
		
		# open file
		scene = Cmaxwell(mwcallback)
		scene.readMXS(fn_cur_mxs)
		
		# delete all cameras in current studio
		delete_all_cameras(scene)
		
		# create camera
		shooter.instantiate_mx_camera(scene, iframe)
		
		# save file
		# scene.writeMXS(fn_output)
		utils.write_mxs(scene, fn_cur_mxs)
		
		scene.freeScene()
		

def delete_all_cameras(scene):
	it = CmaxwellCameraIterator()
	camera = it.first( scene )
	names = []
	while not camera.isNull():
		# Do something with the camera.
		name= camera.getName()
		names.append(name) 
		camera = it.next()
	
	for name in names:
		camera = scene.getCamera(name)
		camera.free()
		