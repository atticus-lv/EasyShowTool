import bpy
from typing import Optional
from ..public_path import get_pref
from .functions import has_edit_tree, has_active_node

NOTE_DATA_NAME: str = '.NodeNote'  # use . to hide the text data


# noinspection PyPep8Naming
class EST_OT_add_note(bpy.types.Operator):
    bl_idname = "est.add_note"
    bl_label = "Add Note"
    bl_description = "Add a note"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return has_edit_tree(context)

    def execute(self, context):
        title: str = get_pref().note.title
        width: int = get_pref().note.width
        height: int = get_pref().note.height
        label_size: int = get_pref().note.label_size
        node_tree: bpy.types.NodeTree = context.space_data.edit_tree
        frame_node: bpy.types.Node = node_tree.nodes.new('NodeFrame')

        frame_node.label = title
        frame_node.label_size = label_size
        frame_node.location = context.space_data.cursor_location
        frame_node.width = width
        frame_node.height = height
        frame_node.shrink = False
        text_data = bpy.data.texts.new(name=NOTE_DATA_NAME)
        frame_node.text = text_data
        self.move_node(frame_node)
        return {'FINISHED'}

    @staticmethod
    def move_node(node: bpy.types.Node):
        bpy.ops.node.select_all(action='DESELECT')
        bpy.context.space_data.edit_tree.nodes.active = node
        node.select = True
        bpy.ops.transform.translate('INVOKE_DEFAULT')


# noinspection PyPep8Naming
class EST_OT_edit_note(bpy.types.Operator):
    bl_idname = "est.edit_note"
    bl_label = "Edit Note"
    bl_description = "Edit the note"

    @classmethod
    def poll(cls, context):
        if not has_edit_tree(context):
            return False
        if not has_active_node(context, 'NodeFrame'):
            return False
        if context.space_data.edit_tree.nodes.active.text is None:
            return False
        if context.space_data.edit_tree.nodes.active.select is False:
            return False
        return True

    def execute(self, context):
        self.node_tree: bpy.types.NodeTree = context.space_data.edit_tree
        frame_node: bpy.types.Node = self.node_tree.nodes.active
        text: bpy.types.Text = frame_node.text

        bpy.ops.screen.userpref_show("INVOKE_AREA")
        screen = bpy.context.window_manager.windows[-1].screen
        area: bpy.types.Area = screen.areas[0]
        area.ui_type = 'TEXT_EDITOR'
        area.spaces[0].text = text
        area.spaces[0].show_syntax_highlight = False
        area.spaces[0].show_region_header = False
        return {'FINISHED'}


def header_menu(self, context):
    layout = self.layout
    layout.operator(EST_OT_add_note.bl_idname, icon='TEXT')
    # layout.operator(EST_OT_edit_note.bl_idname, icon='CURRENT_FILE')


def register():
    from bpy.utils import register_class

    register_class(EST_OT_add_note)
    register_class(EST_OT_edit_note)

    bpy.types.NODE_HT_header.append(header_menu)


def unregister():
    from bpy.utils import unregister_class
    bpy.types.NODE_HT_header.remove(header_menu)

    unregister_class(EST_OT_add_note)
    unregister_class(EST_OT_edit_note)
