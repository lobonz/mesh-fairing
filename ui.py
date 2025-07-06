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

import bpy
from . import moduleutil
from . import operators


class MESH_PT_mesh_fairing_panel(bpy.types.Panel):
    """Mesh Fairing tools panel for the N-Panel"""
    bl_label = "Mesh Fairing"
    bl_idname = "MESH_PT_mesh_fairing_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"
    bl_context = "mesh_edit"
    
    @classmethod
    def poll(cls, context):
        return (context.object and 
                context.object.type == 'MESH' and 
                context.mode in {'EDIT_MESH', 'SCULPT'})
    
    def draw(self, context):
        layout = self.layout
        
        # Main mesh fairing section
        col = layout.column(align=True)
        col.label(text="Mesh Fairing Tools:")
        
        if context.mode == 'EDIT_MESH':
            # Edit mode tools
            row = col.row(align=True)
            row.operator(operators.MESH_OT_fair_vertices.bl_idname, 
                        text="Fair Vertices", icon='MESH_DATA')
            
            # Quick settings section
            box = layout.box()
            box.label(text="Quick Settings:", icon='SETTINGS')
            
            # Continuity settings
            box.prop(context.scene, 'mesh_fairing_continuity')
            box.prop(context.scene, 'mesh_fairing_triangulate')
            
            # Quick action button with current settings
            row = box.row()
            row.scale_y = 1.2
            op = row.operator(operators.MESH_OT_fair_vertices_internal.bl_idname, 
                            text="Quick Fair", icon='PLAY')
            op.continuity = context.scene.mesh_fairing_continuity
            op.triangulate = context.scene.mesh_fairing_triangulate
        
        elif context.mode == 'SCULPT':
            # Sculpt mode tools
            row = col.row(align=True)
            row.operator(operators.SCULPT_OT_fair_vertices.bl_idname, 
                        text="Fair Vertices", icon='SCULPTMODE_HLT')
            
            # Quick settings for sculpt mode
            box = layout.box()
            box.label(text="Sculpt Settings:", icon='SETTINGS')
            
            box.prop(context.scene, 'sculpt_fairing_continuity')
            box.prop(context.scene, 'sculpt_fairing_invert_mask')
            
            # Quick action button for sculpt mode
            row = box.row()
            row.scale_y = 1.2
            op = row.operator(operators.SCULPT_OT_fair_vertices_internal.bl_idname, 
                            text="Quick Fair", icon='PLAY')
            op.continuity = context.scene.sculpt_fairing_continuity
            op.invert_mask = context.scene.sculpt_fairing_invert_mask
        
        # Dependencies section
        layout.separator()
        deps_box = layout.box()
        deps_box.label(text="Dependencies:", icon='SCRIPTPLUGINS')
        draw_numpy_ui(context, deps_box)
        draw_scipy_ui(context, deps_box)
        
        # Quick Actions section
        layout.separator()
        qa_box = layout.box()
        qa_box.label(text="Quick Actions:", icon='FORWARD')
        
        row = qa_box.row()
        row.operator("wm.call_menu", text="Add to Quick Favorites", 
                    icon='SOLO_ON').name = "MESH_MT_mesh_fairing_quick_menu"


class MESH_MT_mesh_fairing_quick_menu(bpy.types.Menu):
    """Quick menu for mesh fairing operations"""
    bl_label = "Mesh Fairing Quick Menu"
    bl_idname = "MESH_MT_mesh_fairing_quick_menu"
    
    def draw(self, context):
        layout = self.layout
        
        if context.mode == 'EDIT_MESH':
            layout.operator(operators.MESH_OT_fair_vertices.bl_idname, 
                          text="Fair Vertices", icon='MESH_DATA')
        elif context.mode == 'SCULPT':
            layout.operator(operators.SCULPT_OT_fair_vertices.bl_idname, 
                          text="Fair Vertices", icon='SCULPTMODE_HLT')


def display_popup(message: str, title: str = '', icon: str = ''):
    def draw(self, context):
        self.layout.label(text = message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


def draw_vertex_menu(menu: bpy.types.Menu, context: bpy.types.Context):
    layout = menu.layout
    layout.operator_context = 'INVOKE_DEFAULT'
    layout.separator()
    layout.operator(operators.MESH_OT_fair_vertices.bl_idname,
                    text = 'Fair Vertices')


def draw_sculpt_menu(menu: bpy.types.Menu, context: bpy.types.Context):
    layout = menu.layout
    layout.separator()
    layout.operator(operators.SCULPT_OT_fair_vertices.bl_idname,
                    text = 'Fair Vertices')


def draw_numpy_ui(context: bpy.types.Context, layout: bpy.types.UILayout):
    numpy_is_installed = moduleutil.is_installed('numpy')

    col = layout.column(align = True)

    if numpy_is_installed:
        col.label(text = 'NumPy is already installed', icon = 'INFO')
    else:
        col.label(text = 'NumPy is not installed', icon = 'ERROR')

    row = col.row()
    row.enabled = not numpy_is_installed

    op = row.operator(operators.SCRIPT_OT_install_module.bl_idname,
                      text = 'Install NumPy')
    op.name = 'numpy'
    op.reload_scripts = True


def draw_scipy_ui(context: bpy.types.Context, layout: bpy.types.UILayout):
    numpy_is_installed = moduleutil.is_installed('numpy')
    scipy_is_installed = moduleutil.is_installed('scipy')

    col = layout.column(align = True)

    if scipy_is_installed:
        col.label(text = 'SciPy is already installed', icon = 'INFO')
    else:
        col.label(text = 'SciPy is not installed', icon = 'ERROR')

    row = col.row()
    row.enabled = numpy_is_installed and not scipy_is_installed

    op = row.operator(operators.SCRIPT_OT_install_module.bl_idname,
                      text = 'Install SciPy')
    op.name = 'scipy'
    op.options = '--no-deps'
    op.reload_scripts = True

