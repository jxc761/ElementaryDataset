
from pymaxwell import *
from mx_shoot import CMxShooter
import shutil
import json

def build_mx_shooter(fn_camera_conf, fn_shoot_script):
	camera_parameters = {}

	with open(fn_camera_conf) as json_data:
		camera_parameters = json.load(json_data)

	shoot_script = {}

	with open(fn_shoot_script) as json_data:
		shoot_script = json.load(json_data)
	
	
	shooter = CMxShooter(camera_parameters, shoot_script)
	
	return shooter
	

def build_seqence(fn_studio, fn_shoot_script, fn_camera_conf, dn_output):
	# load shoot script in
	
	dn_input = os.path.dirname(fn_studio)

	# open file
	scene = Cmaxwell(mwcallback)
	scene.readMXS(fn_studio)
	
	# copy dependencies to dn_output
	copy_dependencies(scene, dn_output)
	
	# delete all cameras in current studio
	delete_all_cameras(scene)	

	# build maxwell shooter 
	shooter = build_mx_shooter(fn_camera_conf, fn_shoot_script):
	
	numb_of_frames = shooter.numb_of_frames()
	
	# build frames
	for iframe in range(numb_of_frames):
		camera = shooter.create_mx_camera(iframe)
		
		# save 
		fn_output = os.path.join(dn_output, "frame{0}.mxs".format(iframe))
		scene.writeMXS(fn_output)
	
		# free camera
		camera.free()
	
	scene.freeObject()

	
	
def copy_dependencies(scene, dn_dst):
	
	file_list = scene.getDependencies()
	for fn_src in file_list:
		fn_dst = os.path.join(dn_dst, os.path.basename(file))
		shutil.copyfile(fn_src, fn_dst)

def delete_all_cameras(scene)	
	it = CmaxwellCameraIterator()
	camera = it.first( scene )
	names = []
	while not camera.isNull():
		# Do something with the camera.
		name, ok = camera.getName()
		names << name 
		camera = it.next()
	
	for name in names:
		camera = scene.getCamera(name)
		camera.free()
		