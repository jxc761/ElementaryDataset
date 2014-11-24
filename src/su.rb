require "maxwell.rb"
require "nplab.rb"


def build_scene(fn_skp, fn_mxs)
  entities = Sketchup.active_model.entities
  materials = Sketchup.active_model.materials
  entities.clear!
  materials.purge_unused
  # target
  target_material=materials.add("target")
  target_material.color = "Magenta"

  s = 0.1.m
  pts = [[s, s, 0], [-s, s, 0], [-s, -s, 0], [s, -s, 0]];
  target = entities.add_group
  target.entities.add_face(pts).pushpull(-0.2.m)
  target.material= target_material


  # gound
  ground_material = materials.add("ground")
  ground_material.color = "YellowGreen"

  s = 1000.m
  pts = [[s, s, 0], [s, -s, 0], [-s, -s, 0], [-s, s, 0]];
  ground = entities.add_face(pts)
  ground.material = ground_material
  ground.back_material= ground_material
  Sketchup.active_model.save(fn_skp)
  Sketchup.active_model.export(fn_mxs)
end

dn_data = "#{File.dirname(__FILE__)}/data"

#generate maxwell scene
fn_skp = "#{dn_data}/studio/studio.skp"
fn_mxs = "#{dn_data}/studio/studio.mxs"
build_scene(fn_skp, fn_mxs)


# generate shoot scripts
fn_cts        = "#{dn_data}/confs/camera_target_setting.cts.json"
fn_conf       = "#{dn_data}/confs/shoot_script.conf.json"
dn_ss_output  = "#{dn_data}/shootscript"
NPLAB::ShootScriptGenerator.generate_shoot_scripts11(fn_conf, fn_cts, dn_ss_output)

#exit sketchup
exec("ps -clx | grep -i 'sketchup' | awk '{print $2}' | head -1 | xargs kill -9")