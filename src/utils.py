from pymaxwell import *
import os
import shutil

def copy_dependencies(fn_mxs, dn_dst):
	dn_input = os.path.dirname(fn_mxs)
	dn_input_texture=os.path.join(dn_input, "textures")
	
	dn_textures = os.path.join(dn_dst, "textures")
	if not os.path.exists(dn_textures):
		os.mkdir(dn_textures)
		
	
	# open .mxs file
	scene = Cmaxwell(mwcallback)
	ok = scene.readMXS(fn_mxs)
	if not ok:
		print("Cannot open file : {0}".format(fn_mxs))
		exit(-1)
	
	# add normal searching path
	
	file_list, ok = scene.getDependencies()
	
	
	#scene.addSearchingPath(dn_input)
	#scene.addSearchingPath(os.path.join(dn_input, "textures"))
	search_paths, ok = scene.getSearchingPaths()
	
	search_paths.append(dn_input)
	search_paths.append(dn_input_texture)
	
	# print("dependencies:")
	for fn_src in file_list:
		
		# find the absolute path of fn_src
		if not os.path.exists(fn_src):
			basename = os.path.basename(fn_src)
			for search_path in search_paths:
				if os.path.exists(os.path.join(search_path, basename)):
					fn_src = os.path.join(search_path, basename)
					break
		
		if not os.path.exists(fn_src):
			print("cannot file: {0}". format(fn_src))
			continue
			
		fn_dst = os.path.join(dn_textures, os.path.basename(fn_src))
		shutil.copyfile(fn_src, fn_dst)
	
	#scene.addSearchingPath(dn_input)
	#scene.addSearchingPath(os.path.join(dn_input, "textures"))
	
	scene.freeScene()

def write_mxs(scene, fn_mxs):
	dirname = os.path.dirname(fn_mxs)
	basename = os.path.basename(fn_mxs)
	filename, ext = os.path.splitext(basename)
	
	fn_mxi = os.path.join(dirname, filename+".mxi")
	fn_img = os.path.join(dirname, filename+".png")
	
	scene.setMxsPath(fn_mxs)
	scene.setRenderParameter("MXI FULLNAME", fn_mxi )
	scene.setPath("RENDER",fn_img, 8 )
	scene.setRenderParameter("DO NOT SAVE MXI FILE", 0 )
	scene.setRenderParameter("DO NOT SAVE IMAGE FILE", 0)
	
	scene.addSearchingPath(dirname)
	scene.addSearchingPath(os.path.join(dirname, "textures"))
	scene.writeMXS(fn_mxs)
	