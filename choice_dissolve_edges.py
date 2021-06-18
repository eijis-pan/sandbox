import bpy
from bpy import ops
import bmesh

def choice_dissolve_edges(
  arg_objectname='Default'
  ):
      
  object=bpy.context.scene.objects[arg_objectname]
  ops.object.mode_set(mode='EDIT')
  
  meshdata = bmesh.from_edit_mesh(object.data)
  meshdata.select_mode = {'EDGE'}

  ops.mesh.select_all(action = 'DESELECT')
  ops.object.mode_set(mode = 'OBJECT')
  
  rectLoopDict = {}
  for ed in object.data.edges:
    first_hops = []
    for ed1 in object.data.edges:
      if ed.index == ed1.index:
        continue
      if ed.vertices[0] == ed1.vertices[0] or ed.vertices[0] == ed1.vertices[1] \
      or ed.vertices[1] == ed1.vertices[0] or ed.vertices[1] == ed1.vertices[1]:
        first_hops.append(ed1)
        
    second_hops = []
    for ed2 in object.data.edges:
      if ed.index == ed2.index:
        continue
      for ed1 in first_hops:
        if ed1.index == ed2.index:
          continue
        if ed2.vertices[0] == ed1.vertices[0] or ed2.vertices[0] == ed1.vertices[1] \
        or ed2.vertices[1] == ed1.vertices[0] or ed2.vertices[1] == ed1.vertices[1]:
          if ed2 in second_hops:
            if ed.index in rectLoopDict:
              rectLoopDict[ed.index].append(ed2.index)
            else:
              rectLoopDict[ed.index] = [ed2.index]
          else:
            second_hops.append(ed2)

  linkListCollection = []
  for edIndexMid in rectLoopDict:    
    rectLoopEdges = rectLoopDict[edIndexMid]
    if 2 == len(rectLoopEdges):        
      edIndexStart = rectLoopEdges[0]
      edIndexEnd = rectLoopEdges[1]

      existStartLinkList = None
      existEndLinkList = None
      existEndLinkListIndex = -1
      for index, existLinkList in enumerate(linkListCollection):
        if edIndexStart in existLinkList:
          existStartLinkList = existLinkList
        if edIndexEnd in existLinkList:
          existEndLinkList = existLinkList
          existEndLinkListIndex = index
        if existStartLinkList and existEndLinkList:
          break

      if (not existStartLinkList) and (not existEndLinkList):
        newLinkList = [edIndexStart, edIndexMid, edIndexEnd]
        linkListCollection.append(newLinkList)
        continue

      if existStartLinkList and (not existEndLinkList):
        if edIndexStart == existStartLinkList[0]:
          existStartLinkList[0:0] = [edIndexEnd, edIndexMid]
        elif edIndexStart == existStartLinkList[1] and edIndexMid == existStartLinkList[0]:
          existStartLinkList.insert(0, edIndexEnd)
        elif edIndexStart == existStartLinkList[-1]:
          existStartLinkList.extend([edIndexMid, edIndexEnd])
        elif edIndexStart == existStartLinkList[-2] and edIndexMid == existStartLinkList[-1]:
          existStartLinkList.append(edIndexEnd)
        continue
      elif (not existStartLinkList) and existEndLinkList:
        if edIndexEnd == existEndLinkList[0]:
          existEndLinkList[0:0] = [edIndexStart, edIndexMid]
        elif edIndexEnd == existEndLinkList[1] and edIndexMid == existEndLinkList[0]:
          existEndLinkList.insert(0, edIndexStart)
        elif edIndexEnd == existEndLinkList[-1]:
          existEndLinkList.extend([edIndexMid, edIndexStart])
        elif edIndexEnd == existEndLinkList[-2] and edIndexMid == existEndLinkList[-1]:
          existEndLinkList.append(edIndexStart) 
        continue
      
      if existStartLinkList is existEndLinkList:
        existLinkList = existStartLinkList
        if (edIndexStart == existLinkList[0] and edIndexEnd == existLinkList[-1]) \
        or (edIndexStart == existLinkList[-1] and edIndexEnd == existLinkList[0]):
          if not edIndexMid in existLinkList:
            existLinkList.append(edIndexMid)
        continue
        
      if (edIndexStart == existStartLinkList[0] or (edIndexStart == existStartLinkList[1] and edIndexMid == existStartLinkList[0])) \
      and (edIndexEnd == existEndLinkList[0] or (edIndexEnd == existEndLinkList[1] and edIndexMid == existEndLinkList[0])):
        existStartLinkList.reverse()
      elif (edIndexStart == existStartLinkList[-1] or (edIndexStart == existStartLinkList[-2] and edIndexMid == existStartLinkList[-1])) \
      and (edIndexEnd == existEndLinkList[-1] or (edIndexEnd == existEndLinkList[-2] and edIndexMid == existEndLinkList[-1])):
        existEndLinkList.reverse()
      
      if (not edIndexMid in existStartLinkList) and (not edIndexMid in existEndLinkList):
        existStartLinkList.append(edIndexMid)
      
      existStartLinkList.extend(existEndLinkList)
      del linkListCollection[existEndLinkListIndex]
      
  oddEven = False
  for linkList in linkListCollection:
    for index in linkList:
      oddEven = not oddEven
      if oddEven:
        continue
      object.data.edges[index].select = True
    
  ops.object.mode_set(mode='EDIT')
  return

choice_dissolve_edges(arg_objectname=bpy.context.active_object.name)
