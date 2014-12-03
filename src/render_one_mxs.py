import addlib
from pymaxwell import *
import sys
import os
import time
import shutil

def get_mxi_sl(fn_mxi):
	mxi = CmaxwellMxi()
	ok = mxi.read(fn_mxi)
	
	if not ok:
		print("Cannot open {0}!".format(fn_mxi))
		return -1
	
	sl = mxi.getSamplingLevel()
	return sl
	
	

def render_one_file(fn_mxs, dn_output, sl, image_width, image_height):
	
	basename = os.path.basename(fn_mxs)
	name, ext = os.path.splitext(basename)
	
	fn_mxi = os.path.join(dn_output, "{0}.mxi".format(name))
	fn_img = os.path.join(dn_output, "{0}.png".format(name))
	
	dn_sl  = os.path.join(dn_output, "SL{0}".format(sl))
	dst_mxi = os.path.join(dn_sl, "{0}.mxi".format(name))
	dst_img = os.path.join(dn_sl, "{0}.png".format(name))
	
	
	# display information
	print("Input MXS     : {0}".format(fn_mxs))
	print("MXI file      : {0}".format(fn_mxi))
	print("Image file    : {0}".format(fn_img))
	
	print("Output Dir    : {0}".format(dn_output))
	print("Output MXI    : {0}".format(dst_mxi))
	print("Output PNG    : {0}".format(dst_img))
	
	print("Resolution    : {0}x{1}".format(image_width, image_height))	
	print("Sample Level  : {0}".format(sl))
	
	
	# check inputs
	if not os.path.exists(fn_mxs):
		print("Error	: file doesn't exists")
		print("Message	: {0}".format(fn_mxs))
		return False
	
	# check output
	if not os.path.isdir(dn_output):
		os.mkdir(dn_output)
	
	if not os.path.isdir(dn_sl):
		os.mkdir(dn_sl)
	
	if os.path.isfile(dst_img) and os.path.isfile(dst_mxi):
		current_sl = get_mxi_sl(dn_mxi)
		if current_sl > sl:
			print("This {0} have been reached....".format(sl))
			return False
		
		
	# use maxwell render to render mxs 
	start = time.time()
	
	params=['-nogui', '-nowait', '-trytoresume', '-dep:"/usr/local/maxwell-3.0/materials database/textures"']
	params.append('-mxs:"{0}"'.format(fn_mxs))
	params.append('-mxi:"{0}"'.format(fn_mxi))
	params.append('-o:{0}'.format(fn_img))
	params.append('-res:{0}x{1}'.format(image_width, image_height))
	params.append('-sl:{0}'.format(sl))

	runMaxwell(params)
    
	end = time.time()
	elapsed = end - start
	print("Time taken(s) : {0}", elapsed)
		
	# copy files
	if os.path.isfile(dst_img):
		os.remove(dst_img)
		
	if  os.path.isfile(dst_mxi):
		os.remove(dst_mxi)
		
	shutil.copyfile(fn_mxi, dst_mxi)
	shutil.copyfile(fn_img, dst_img)
	
	return True
	

if __name__=="__main__":
	
	if len(sys.argv) < 3 :
		print("usage: render_one_mxs.py <fn_mxs> <dn_output> [<sl> <image_width> <image_height>]")
		sys.exit(-1)
	
	fn_mxs = sys.argv[1]
	dn_output = sys.argv[2]
	
	sl = 24
	if len(sys.argv) > 3 :
		sl = sys.argv[3]
	
	image_width = 128
	if len(sys.argv) > 4:
		image_width = sys.argv[4]
	
	image_height=image_width	
	if len(sys.argv) > 5:
		image_height = sys.argv[5]
		
	ok = render_one_file(fn_mxs, dn_output, sl, image_width, image_height)
	sys.exit(ok)

	