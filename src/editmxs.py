from pymaxwell import *

def edit_mxs(fn_mxs, fn_sky, fn_ground_mxm, fn_out_mxs):
	
	# open .mxs file
	scene = Cmaxwell(mwcallback)
	ok = scene.readMXS(fn_mxs)
	if not ok:
		print("Cannot open file : {0}".format(fn_mxs))
		exit(-1)


	# set sky
	env = scene.getEnvironment()
	env.setActiveSky("PHYSICAL")
	ok = env.loadSkyFromPreset(fn_sky)
	if not ok:
		print("error")
		exit(-1)
	
	# set ground material
	ground_mxm_name = "ground"
	ground_mxm = scene.getMaterial(ground_mxm_name)
	ground_mxm.read(fn_ground_mxm)
	ground_mxm.setReference(0, fn_ground_mxm)# 1 (referenced) or 0 (embeded in the scene, default).
	
	# save out	
	scene.writeMXS(fn_out_mxs)
	scene.freeScene()
	