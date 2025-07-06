# ##### BEGIN GPL LICENSE BLOCK #####
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    'name' : 'Mesh Fairing',
    'description' : 'Continuity based smoothing tool',
    'author' : 'Brett Fedack',
    'location': (
        'Sculpt mode: Sculpt menu, Edit mode: Vertex menu, N-Panel: Mesh Fairing'
    ),
    'version' : (1, 1, 0),
    'blender' : (4, 3, 0),
    'category' : 'Mesh'
}

import logging
import importlib

if 'bpy' not in locals():
    import bpy
    from . import operators
    from . import preferences
    from . import ui
    from . import linalg
else:
    importlib.reload(operators)
    importlib.reload(preferences)
    importlib.reload(ui)
    importlib.reload(linalg)

classes = (operators.MESH_OT_fair_vertices,
           operators.MESH_OT_fair_vertices_internal,
           operators.SCULPT_OT_fair_vertices,
           operators.SCULPT_OT_fair_vertices_internal,
           operators.SCULPT_OT_push_undo,
           operators.SCRIPT_OT_install_module,
           preferences.MeshFairingPreferences,
           ui.MESH_PT_mesh_fairing_panel,
           ui.MESH_MT_mesh_fairing_quick_menu)


def register():

    # Configure the logging service.
    logging_format = (
        '[%(levelname)s] ' +
        '(%(asctime)s) ' +
        '{0}.%(module)s.%(funcName)s():L%(lineno)s'.format(__package__) +
        ' - %(message)s'
    )
    logging.basicConfig(
        level = logging.DEBUG,
        format = logging_format,
        datefmt = '%Y/%m/%d %H:%M:%S'
    )

    # Initialize the linear algebra solver.
    linalg.init()

    # Register this Blender addon.
    for cls in classes:
        bpy.utils.register_class(cls)

    # Register scene properties for N-panel settings
    bpy.types.Scene.mesh_fairing_continuity = bpy.props.EnumProperty(
        name="Continuity",
        description="Continuity constraint for fairing",
        items=[
            ('SMOOTH', 'Smooth', 'Simple Laplacian smoothing that averages neighboring vertices'),
            ('POS', 'Position', 'Position continuity'),
            ('TAN', 'Tangent', 'Tangent continuity'),
            ('CURV', 'Curvature', 'Curvature continuity')
        ],
        default='SMOOTH'
    )
    
    bpy.types.Scene.mesh_fairing_triangulate = bpy.props.BoolProperty(
        name="Triangulate",
        description="Triangulates affected region to produce higher quality results",
        default=False
    )
    
    bpy.types.Scene.sculpt_fairing_continuity = bpy.props.EnumProperty(
        name="Continuity",
        description="Continuity constraint for fairing",
        items=[
            ('SMOOTH', 'Smooth', 'Simple Laplacian smoothing that averages neighboring vertices'),
            ('POS', 'Position', 'Position continuity'),
            ('TAN', 'Tangent', 'Tangent continuity'),
            ('CURV', 'Curvature', 'Curvature continuity')
        ],
        default='SMOOTH'
    )
    
    bpy.types.Scene.sculpt_fairing_invert_mask = bpy.props.BoolProperty(
        name="Invert Mask",
        description="Fair unmasked vertices instead of masked vertices",
        default=False
    )

    # Add mesh fairing operators to existing menus.
    bpy.types.VIEW3D_MT_edit_mesh_vertices.append(ui.draw_vertex_menu)
    bpy.types.VIEW3D_MT_sculpt.append(ui.draw_sculpt_menu)


def unregister():

    # Remove mesh fairing operators from existing menus.
    bpy.types.VIEW3D_MT_edit_mesh_vertices.remove(ui.draw_vertex_menu)
    bpy.types.VIEW3D_MT_sculpt.remove(ui.draw_sculpt_menu)

    # Unregister scene properties
    try:
        del bpy.types.Scene.mesh_fairing_continuity
        del bpy.types.Scene.mesh_fairing_triangulate
        del bpy.types.Scene.sculpt_fairing_continuity
        del bpy.types.Scene.sculpt_fairing_invert_mask
    except AttributeError:
        pass

    # Unregister this Blender addon.
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
