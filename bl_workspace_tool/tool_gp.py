import bpy
from ..public_path import get_tool_icon
from ..bl_operator.ops_gp_modal import EST_OT_gp_set_active_layer, EST_OT_gp_drag_modal, EST_OT_add_gp_modal, \
    EST_OT_move_gp_modal, EST_OT_rotate_gp_modal, EST_OT_scale_gp_modal, EST_OT_drag_add_gp_modal
from ..bl_operator.ops_gp_basic import EST_OT_remove_gp, EST_OT_scale_gp, \
    EST_OT_gp_drop_layer_color
from ..bl_operator.ops_gp_align import EST_MT_align_menu, EST_MT_distribution_menu, AlignIcon


class EST_TL_gp_add(bpy.types.WorkSpaceTool):
    bl_idname = "est.gp_add_tool"
    bL_idname_fallback = "node.select_box"
    bl_space_type = 'NODE_EDITOR'
    bl_context_mode = None
    bl_label = "Add"
    bl_icon = get_tool_icon('gp_add_tool')
    bl_keymap = (
        # drag add
        (EST_OT_drag_add_gp_modal.bl_idname,
         {"type": 'LEFTMOUSE', "value": 'CLICK_DRAG', "shift": False, "ctrl": False},
         # {"properties": [('use_mouse_pos', True)]}
         {"properties": []}
         ),
        (EST_OT_drag_add_gp_modal.bl_idname,
         {"type": 'LEFTMOUSE', "value": 'CLICK_DRAG', "shift": True, "ctrl": False},
         # {"properties": [('use_mouse_pos', True)]}
         {"properties": []}
         ),
        (EST_OT_drag_add_gp_modal.bl_idname,
         {"type": 'LEFTMOUSE', "value": 'CLICK_DRAG', "shift": False, "ctrl": False, "alt": True},
         # {"properties": [('use_mouse_pos', True)]}
         {"properties": []}
         ),
        # add
        (EST_OT_add_gp_modal.bl_idname,
         {"type": 'LEFTMOUSE', "value": 'DOUBLE_CLICK', "shift": False, "ctrl": False},
         # {"properties": [('use_mouse_pos', True)]}
         {"properties": []}
         ),
        # select click
        (EST_OT_gp_set_active_layer.bl_idname,
         {"type": "LEFTMOUSE", "value": "CLICK", "shift": False, "ctrl": False},
         {"properties": []},  # [("deselect_all", True)]
         ),
        # scale/rotate/move: GSR
        (EST_OT_move_gp_modal.bl_idname,
         {"type": 'G', "value": 'PRESS', "shift": False, "ctrl": False},
         {"properties": []}),
        (EST_OT_rotate_gp_modal.bl_idname,
         {"type": 'R', "value": 'PRESS', "shift": False, "ctrl": False},
         {"properties": []}),
        (EST_OT_scale_gp_modal.bl_idname,
         {"type": 'S', "value": 'PRESS', "shift": False, "ctrl": False},
         {"properties": []}),
        # delete
        (EST_OT_remove_gp.bl_idname,
         {"type": 'X', "value": 'PRESS', "ctrl": False, "alt": False, "shift": False},
         {"properties": []}),
    )

    def draw_settings(self, layout, tool):
        scene = bpy.context.scene

        box = layout.box()
        box.label(text="Palette", icon='COLOR')

        col = box.column(align=True)
        row = col.row(align=True)
        row.prop(scene, 'est_palette_color', text='Color')
        row.popover(panel='EST_PT_palette_viewer', text='Preset', icon='COLOR')
        col.prop(scene, "est_gp_opacity", slider=True)
        col.prop(scene, "est_gp_thickness", slider=True)

        box = layout.box()
        box.label(text="New", icon='ADD')
        row = box.row()
        row.prop(scene, "est_gp_drag_add_type", text='Type', expand=True)

        if scene.est_gp_drag_add_type == 'OTHER':
            row = box.row()
            row.prop(scene, "est_gp_add_type", text='Source', expand=True)
            # box.prop(scene, "est_gp_size")

            if scene.est_gp_add_type == 'TEXT':
                box.template_ID(scene, "est_gp_text_font", open="font.open", unlink="font.unlink")
                box.prop(scene, "est_gp_text")
            elif scene.est_gp_add_type == 'OBJECT':
                box.prop(scene, "est_gp_obj")
                box.prop(scene, "est_gp_obj_shot_angle")
            elif scene.est_gp_add_type == 'BL_ICON':
                row = box.row()
                row.alignment = 'RIGHT'
                try:
                    row.label(text=bpy.context.scene.est_gp_icon, icon=bpy.context.scene.est_gp_icon)
                except TypeError:
                    pass


class EST_TL_gp_color(bpy.types.WorkSpaceTool):
    bl_idname = "est.gp_color_tool"
    bL_idname_fallback = "node.select_box"
    bl_space_type = 'NODE_EDITOR'
    bl_context_mode = None
    bl_label = "Color"
    bl_icon = get_tool_icon('gp_color_tool')
    # bl_widget = "PH_GZG_place_tool"
    bl_keymap = (
        (EST_OT_gp_drop_layer_color.bl_idname,
         {"type": "LEFTMOUSE", "value": "CLICK"},
         {"properties": []},  # [("deselect_all", True)]
         ),
    )


class EST_MT_tool_context_menu(bpy.types.Menu):
    bl_idname = "EST_MT_tool_context_menu"
    bl_label = "Context Menu"

    def draw(self, context):
        layout = self.layout
        # flip
        layout.operator(EST_OT_scale_gp.bl_idname, text="Horizontal Flip",
                        icon_value=AlignIcon.get_icon_id('FlipX')).scale_vector = (-1, 1)
        layout.operator(EST_OT_scale_gp.bl_idname, text="Vertical Flip",
                        icon_value=AlignIcon.get_icon_id('FlipY')).scale_vector = (1, -1)
        layout.separator()

        EST_MT_align_menu.draw_layout(self, context, layout)
        layout.separator()

        EST_MT_distribution_menu.draw_layout(self, context, layout)
        layout.separator()


class EST_PT_gp_op_menu(bpy.types.Menu):
    bl_idname = "EST_PT_gp_op_menu"
    bl_label = "Operation Menu"

    def draw(self, context):
        layout = self.layout
        row = layout.row()


# noinspection PyPep8Naming
class EST_TL_gp_edit(bpy.types.WorkSpaceTool):
    bl_idname = "est.gp_edit_tool"
    bL_idname_fallback = "node.select_box"
    bl_space_type = 'NODE_EDITOR'
    bl_context_mode = None
    bl_label = "Tweak"
    bl_icon = get_tool_icon('gp_edit_tool')
    bl_keymap = (
        # scale/rotate/move: GSR
        (EST_OT_move_gp_modal.bl_idname,
         {"type": 'G', "value": 'PRESS', "shift": False, "ctrl": False},
         {"properties": []}),
        (EST_OT_rotate_gp_modal.bl_idname,
         {"type": 'R', "value": 'PRESS', "shift": False, "ctrl": False},
         {"properties": []}),
        (EST_OT_scale_gp_modal.bl_idname,
         {"type": 'S', "value": 'PRESS', "shift": False, "ctrl": False},
         {"properties": []}),
        # right click: context menu
        ('wm.call_menu',
         {"type": 'RIGHTMOUSE', "value": 'PRESS'},
         {"properties": [("name", EST_MT_tool_context_menu.bl_idname)]},
         ),
        # select click
        (EST_OT_gp_set_active_layer.bl_idname,
         {"type": "LEFTMOUSE", "value": "CLICK", "shift": False, "ctrl": False},
         {"properties": []},  # [("deselect_all", True)]
         ),
        (EST_OT_gp_set_active_layer.bl_idname,
         {"type": "LEFTMOUSE", "value": "CLICK", "shift": True, "ctrl": False},
         {"properties": []},  # [("deselect_all", True)]
         ),
        (EST_OT_gp_set_active_layer.bl_idname,
         {"type": "LEFTMOUSE", "value": "CLICK", "ctrl": True, "shift": False},
         {"properties": []},  # [("deselect_all", True)]
         ),

        # color
        (EST_OT_gp_drop_layer_color.bl_idname,
         {"type": "C", "value": "PRESS"},
         {"properties": []},  # [("deselect_all", True)]
         ),
        # normal mode drag
        (EST_OT_gp_drag_modal.bl_idname,
         {"type": 'LEFTMOUSE', "value": 'CLICK_DRAG', "shift": False, "ctrl": False},
         {"properties": []}),
        # copy mode drag
        (EST_OT_gp_drag_modal.bl_idname,
         {"type": 'LEFTMOUSE', "value": 'CLICK_DRAG', "shift": False, "ctrl": False, "alt": True},
         {"properties": []}),
        # different enter event with drag
        (EST_OT_gp_drag_modal.bl_idname,
         {"type": 'LEFTMOUSE', "value": 'CLICK_DRAG', "shift": True, "ctrl": False},
         {"properties": []}),
        (EST_OT_gp_drag_modal.bl_idname,
         {"type": 'LEFTMOUSE', "value": 'CLICK_DRAG', "shift": False, "ctrl": True},
         {"properties": []}),
        (EST_OT_gp_drag_modal.bl_idname,
         {"type": 'LEFTMOUSE', "value": 'CLICK_DRAG', "shift": True, "ctrl": True},
         {"properties": []}),
        # delete
        (EST_OT_remove_gp.bl_idname,
         {"type": 'X', "value": 'PRESS', "ctrl": False, "alt": False, "shift": False},
         {"properties": []}),
    )

    def draw_settings(self, layout, tool):
        scene = bpy.context.scene

        box = layout.box()
        box.label(text="Palette", icon='COLOR')

        col = box.column(align=True)
        row = col.row(align=True)
        row.prop(scene, 'est_palette_color', text='Color')
        row.popover(panel='EST_PT_palette_viewer', text='Preset', icon='COLOR')
        col.prop(scene, "est_gp_opacity", slider=True)
        col.prop(scene, "est_gp_thickness", slider=True)



def reigster():
    from bpy.utils import register_tool, register_class

    register_class(EST_MT_tool_context_menu)
    register_tool(EST_TL_gp_add, separator=True)
    register_tool(EST_TL_gp_edit, separator=False)
    # register_tool(EST_TL_gp_color, separator=False)


def unregister():
    from bpy.utils import unregister_tool, unregister_class

    unregister_class(EST_MT_tool_context_menu)
    unregister_tool(EST_TL_gp_add)
    unregister_tool(EST_TL_gp_edit)
    # unregister_tool(EST_TL_gp_color)
