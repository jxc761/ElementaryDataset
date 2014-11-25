from pymaxwell import *
import shutil
import glob
import os


import utils


def generate_mxs_with_different_mxm(fn_mxs, dn_root_mxm, dn_output):
	
	# copy all mxm to output
	print("generate_mxs_with_different_mxm")
	print("fn_mxs		:{0}".format(fn_mxs))
	print("dn_root_mxm	:{0}".format(dn_root_mxm))
	print("dn_output	:{0}".format(dn_output))
	
	if os.path.exists(dn_output):
		shutil.rmtree(dn_output)
	shutil.copytree(dn_root_mxm, dn_output)
	
	# get all directories under dn_output
	dir_list = [ os.path.join(dn_output, name) 
					for name in os.listdir(dn_output)
						if os.path.isdir(os.path.join(dn_output, name)) ]
	
	for cur_dir in dir_list:
		
		fn_cur_mxs = os.path.join(cur_dir, "studio.mxs")
		
		# copy all dependences to cur_idr
		utils.copy_dependencies(fn_mxs, cur_dir)
		
		# copy scene to cur_dir
		shutil.copyfile(fn_mxs, fn_cur_mxs)
		
		# open .mxs file
		scene = Cmaxwell(mwcallback)
		ok = scene.readMXS(fn_cur_mxs)
		if not ok:
			print("Cannot open file : {0}".format(fn_mxs))
			exit(-1)
		
		# get the path of current mxm
		mxms = glob.glob(os.path.join(cur_dir, "*.mxm") )
		if len(mxms) != 1:
			print("configuration error!")
			exit(-1)
		fn_mxm = mxms[0]
		
		# set material
		target_material_name = "target"
		target_material=scene.getMaterial(target_material_name)
		target_material.read(fn_mxm)
		target_material.setReference(0, fn_mxm)
		
		
		scene.writeMXS(fn_cur_mxs)
		scene.freeScene()
