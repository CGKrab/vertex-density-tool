bl_info = {
    "name": "Vertex Density",
    "author": "CG Krab",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > N",
    "description": "Calculates vertex density of the active object",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

import bpy
from bpy.types import (Panel, Operator)
import bmesh

## Create panel, button operator, and function##

class VDfunction(bpy.types.Operator):
    bl_idname = "example.func_1"
    bl_label = "Check Density"

    def execute(self, context):
        
        ##APPLY SCALE##
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        ##DEFINE GLOBAL VARS##
        global vdlabel
        global arealabel
        global vertexdensity
        global area
        global vertexcount
        global vertexlabel
        
        #get the active mesh (selected object)
        me = bpy.context.object.data
        #get a bmesh representation and
        bm = bmesh.new()
        #fill it in from that selected object
        bm.from_mesh(me)
        
        ##Get area
        area = sum(f.calc_area() for f in bm.faces) #define var area as sum of areas for all f in bm.faces
        arealabel = str(area)
        
        ##Get vertex count
        ob = bpy.context.object
        obdata = ob.data
        vertexcount = len(obdata.vertices)
        vertexlabel = str(vertexcount)

        ##Get vertex density
        vertexdensity = (vertexcount/area)
        vdround = round(vertexdensity,4)
        vdlabel = str(vdround)
        print(vdlabel)

        ##bm.to_mesh(me)## #write the bmesh back to the accessed mesh
        #free to the active mesh and prevent further access
        bm.free()
        
        #Report info
        self.report({'INFO'}, "Vertex density checked.")
        return {'FINISHED'}
    
## DRAW UI PANEL## 

class Panel(bpy.types.Panel):
    bl_label = "Vertex Density"
    bl_idname = "PT_TestPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Vertex Density'
    
    def draw(self, context):
        layout = self.layout
        
        #new row        
        row = layout.row()
        
        #text/icons in the row
        row.label(text="Check Active Object:", icon='GROUP_VERTEX')
        layout.operator(VDfunction.bl_idname)
        
        #Vertex Density Report
        row = layout.row()
        row.label(text="Vertex Density - Verts/M²:")
        row = layout.row()
        layout.label(text=vdlabel)

classes = (VDfunction, Panel)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
if __name__ == "__main__":
    register()

