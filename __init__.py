bl_info = {
    'name': 'Vertex Density',
    'author': 'CG Krab',
    'description': 'Calculates vertex density of the active object',
    'blender': (3, 0, 0),
    'version': (1, 0),
    'category': 'Object',
    'location': 'View3D > N-Panel',
    'support': 'COMMUNITY',
    'warning': '',
    'doc_url': 'https://github.com/CGKrab/vertex-density-tool',
    'tracker_url': 'https://github.com/CGKrab/vertex-density-tool/issues'
}


import bpy
import bmesh
from bpy.types import Operator, Panel


class VD_OT_vertex_density_checker(Operator):
    bl_idname = 'vd.vertex_density_checker'
    bl_label = 'Check'

    @classmethod
    def poll(cls, context):
        return context.object.type == 'MESH' and context.object.mode == 'OBJECT'

    def execute(self, context):

        # Apply scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        # Get the active mesh (selected object)
        mesh = context.object.data
        bm = bmesh.new()
        bm.from_mesh(mesh)

        # Get area
        area = sum(face.calc_area() for face in bm.faces) # Define var area as sum of areas for all face in bm.faces
        bm.free()

        # Get vertex count
        vertex_count = len(mesh.vertices)

        ##Get vertex density
        vertex_density = (vertex_count / area)

        # Update string property
        context.scene.vd_label = str(round(vertex_density, 4))

        self.report({'INFO'}, 'Checked: Vertex Density')
        return {'FINISHED'}


class VD_PT_vertex_density_checker(Panel):
    bl_label = 'Vertex Density'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Vertex Density'

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.scale_y = 1.6
        col.operator('vd.vertex_density_checker')

        box = layout.box()
        box.label(text=f'Density - {context.scene.vd_label} / m²')


classes = (VD_OT_vertex_density_checker, VD_PT_vertex_density_checker)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.vd_label = bpy.props.StringProperty(default='0.0')


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.vd_label 