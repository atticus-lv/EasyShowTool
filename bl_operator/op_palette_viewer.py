import bpy
import re
from bpy.props import StringProperty
from ..model.model_color import ColorPaletteModel
from ..public_path import get_color_palettes
from .functions import get_icons, has_edit_tree, is_valid_workspace_tool
from ..model.utils import ColorTool

ICONS = []


class EST_OT_set_color(bpy.types.Operator):
    bl_idname = "est.color"
    bl_label = "Set Color"
    bl_options = {'UNDO'}

    hex: StringProperty()

    def execute(self, context):
        context.scene.est_palette_color = ColorTool.hex_2_rgb(self.hex)
        context.area.tag_redraw()
        return {'FINISHED'}


class EST_OT_set_gp_active_color(bpy.types.Operator):
    bl_idname = "est.set_gp_active_color"
    bl_label = "Set GP Active Color"
    bl_options = {'UNDO'}

    hex: StringProperty()

    def execute(self, context):
        gp_data = context.space_data.edit_tree.grease_pencil
        if gp_data is None:
            return {'CANCELLED'}
        gp_data.layers.active.color = ColorTool.hex_2_rgb(self.hex)
        return {'FINISHED'}


def draw_palette(context, layout, bl_idname: str):
    colors: dict[str, list[str]] = get_color_palettes()
    # sort_dir, 'SocketColor' first
    for directory, color_list in colors.items():
        col = layout.box().column(align=True)
        col.label(text=directory)
        row = col.row(align=True)
        row.alignment = 'CENTER'
        gird = row.grid_flow(row_major=False, even_columns=True, even_rows=True, align=True)
        gird.scale_x = 0.65
        for color in color_list:
            gird.operator(bl_idname, text='', icon_value=ColorPaletteModel.get_color_icon_id(color),
                          emboss=False).hex = color


class EST_PT_palette_viewer(bpy.types.Panel):
    bl_idname = "EST_PT_palette_viewer"
    bl_label = "Color Palette"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'HEADER'
    bl_options = {'HEADER_LAYOUT_EXPAND'}

    @classmethod
    def poll(cls, context):
        return has_edit_tree(context) and is_valid_workspace_tool(context)

    def draw(self, context):
        layout = self.layout
        draw_palette(context, layout, EST_OT_set_color.bl_idname)


class EST_PT_palette_viewer_active(bpy.types.Panel):
    bl_idname = "EST_PT_palette_viewer_active"
    bl_label = "Active Color"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'HEADER'
    bl_options = {'HEADER_LAYOUT_EXPAND'}

    @classmethod
    def poll(cls, context):
        return has_edit_tree(context) and is_valid_workspace_tool(context)

    def draw(self, context):
        layout = self.layout
        draw_palette(context, layout, EST_OT_set_gp_active_color.bl_idname)


def register():
    bpy.utils.register_class(EST_OT_set_color)
    bpy.utils.register_class(EST_OT_set_gp_active_color)
    bpy.utils.register_class(EST_PT_palette_viewer)
    bpy.utils.register_class(EST_PT_palette_viewer_active)


def unregister():
    bpy.utils.unregister_class(EST_OT_set_color)
    bpy.utils.unregister_class(EST_OT_set_gp_active_color)
    bpy.utils.unregister_class(EST_PT_palette_viewer)
    bpy.utils.unregister_class(EST_PT_palette_viewer_active)
