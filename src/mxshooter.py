

from pymaxwell import *

# the deafult lenght unit export by sketchup is inch, but the maxwell uses m.
def to_m(aa):
	return [ i * 0.0254 for i in aa]
	
# if (a, b, c) will be transformed to (a, -c, b) coordinate transformation, 
# i.e. the su_x_axis -> mx_x_aix, su_z_axis->mx_y	
def to_vector(a):
	return Cvector(a[0], a[2], a[1])
	
class CPosition:
	
	
	def __init__(self, d):
		
		self.origin =  to_vector(to_m(d["origin"]) )
		self.zaxis = to_vector(d["zaxis"])
		self.xaxis = to_vector(d["xaxis"])
		self.zaxis = to_vector(d["zaxis"])
	

	
	def location(self):
		return self.origin

	def up(self):
		return self.zaxis
	


class CMxShooter:
	

	'''
	Create the camera for current frame
	'''
	def instantiate_mx_camera(self, scene, iframe):
		# create a new camera
		name = "frame{0}".format(iframe)

		camera = scene.addCamera(
			name, 					self.nsteps, 			self.shutter, 
			self.film_width, 		self.film_height, 		self.iso, 
			self.diaphragm_type, 	self.angle,				self.nblades, 
			self.fps, 				self.image_height,		self.image_width, 
			self.pixel_aspect)

		# set it activated
		camera.setActive()
		
		# set the camera step by step
		for istep in range(self.nsteps): 
			origin 			= self.origin(iframe, istep)
			up 				= self.up(iframe, istep)
			focal_point 	= self.focal_point(iframe, istep)
			fstop  			= self.fstop(iframe, istep)
			focal_length 	= self.focal_length(iframe, istep)
			need_correction = self.focal_length_need_correction(iframe, istep)
			
			camera.setStep(istep, origin, focal_point, up, focal_length, fstop, need_correction)
		
		return camera
	
	
	def __init__(self, camera_parameters, shoot_script):
		
		self.init_static_camera_parameters(camera_parameters)

		#self.target = CInstance(shoot_script["target"])
		#self.camera = CInstance(shoot_script["camera"])
		self.target_id 			= shoot_script["target"]["id"]
		self.target_position   	= CPosition(shoot_script["target"]["position"])
		
		self.camera_id 			= shoot_script["camera"]["id"]
		self.camera_position    = CPosition(shoot_script["camera"]["position"])
		
		
		self.sample_rate = shoot_script["camera_trajectory"]["sample_rate"]
		self.duration    = shoot_script["camera_trajectory"]["duration"]
		
		
		self.camera_tr = []
		for position in shoot_script["camera_trajectory"]["trace"]:
			self.camera_tr.append(CPosition(position))
		
		
	def init_static_camera_parameters(self, camera_parameters):
		parameters = self.get_default_parameters()
		parameters.update(camera_parameters)
		
		self.nsteps     = parameters["nsteps"]
		self.shutter 	= parameters["shutter"]
		self.film_width = parameters["film_width"]
		self.film_height = parameters["film_height"]
		self.iso 		= parameters["iso"]		
		self.diaphragm_type = parameters["diaphragm_type"]
		
		self.angle = parameters["angle"]
		self.nblades = parameters["nblades"]
		self.fps = parameters["fps"]
		self.image_height = parameters["image_height"]
		self.image_width = parameters["image_width"]
		
		self.pixel_aspect = parameters["pixel_aspect"]
		self.lens_type = parameters["lens_type"]
		self.projection_type = parameters["projection_type"]
		
		self._focal_length= parameters["focal_length"]
		self._fstop = parameters["fstop"]
		self._focal_length_need_correction = parameters["focal_length_need_correction"]
	
	'''
	default default camera parameters
	'''	
	def get_default_parameters(self):
		params = {
			"nsteps" : 1,
			"shutter": 1.0/500,
			"film_width":0.036,
			"film_height":0.036,
			"iso":100,
			"diaphragm_type":"CIRCULAR",
			"angle":90.0,
			"nblades":0,
			"fps":30,
			"image_height":128,
			"image_width":128,
			"pixel_aspect":1,
			"lens_type":TYPE_THIN_LENS,
			"projection_type":TYPE_PERSPECTIVE,
			
			"focal_length":0.035,
			"fstop" : 8,
			"focal_length_need_correction": True
		}
		return params
	
	'''
	
	'''		
	def numb_of_frames(self):
		return len(self.camera_tr)

	'''
	--------------------------------------------
	Step setting
	--------------------------------------------
	'''
	def origin(self, frame_id, step_id):
		return self.camera_tr[frame_id].location()
		
	def up(self, frame_id, step_id):
		return self.camera_tr[frame_id].up()
	
	def focal_point(self, iframe, istep):
		return self.target_position.location()
	
	def fstop(self, iframe, istep):
		return self._fstop
		
	def focal_length(self, iframe, istep):
		return self._focal_length
	
	def focal_length_need_correction(self, iframe, istep):
		return self._focal_length_need_correction
		
				
	