import bpy
from bpy import ops
import bmesh

def choice_disolv_vertex(
  arg_objectname='Default'
  ):
      
  object=bpy.context.scene.objects[arg_objectname]
  ops.object.mode_set(mode='EDIT')
  
  meshdata = bmesh.from_edit_mesh(object.data)
  meshdata.select_mode = {'VERT'}

  ops.mesh.select_all(action = 'DESELECT')
  ops.object.mode_set(mode = 'OBJECT')
  
  for vt in object.data.vertices:
    edge_count = 0
    for ed in object.data.edges:
      if vt.index == ed.vertices[0]:
        edge_count += 1
      if vt.index == ed.vertices[1]:
        edge_count += 1
    
    face_count = 0
    for pl in object.data.polygons:
      for vtIdxInPl in pl.vertices:
        if vt.index == vtIdxInPl:
          face_count += 1
          break

    if edge_count == 2 and face_count == 2:
      object.data.vertices[vt.index].select = True
  
  ops.object.mode_set(mode='EDIT')
  return

choice_disolv_vertex(arg_objectname=bpy.context.active_object.name)
