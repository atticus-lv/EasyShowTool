import bpy
import time
import threading

from bpy.props import PointerProperty, IntProperty, EnumProperty, StringProperty, FloatVectorProperty, FloatProperty
from bpy.app.handlers import persistent

from ..model.model_color import ColorPaletteModel
from ..model.data_enums import ShootAngles, GPAddTypes
from ..bl_operator.functions import ensure_builtin_font


def register_later(lock, t):
    while not hasattr(bpy.context, 'scene'):
        time.sleep(5)

    # font
    ensure_builtin_font()


@persistent
def init_scene_props(noob):
    lock = threading.Lock()
    lock_holder = threading.Thread(target=register_later, args=(lock, 5), name='est_color')
    lock_holder.daemon = True
    lock_holder.start()


def register():
    ColorPaletteModel.register_color_icon()

    bpy.types.Scene.est_palette_color = FloatVectorProperty(name="Color", size=3, subtype='COLOR_GAMMA', min=0.0,
                                                            max=1.0,
                                                            default=(0.8, 0.8, 0.8))
    bpy.types.Scene.est_gp_transform_mode = EnumProperty(name="Transform Mode", items=[('LOCAL', 'Local', 'Local'),
                                                                                       ('GLOBAL', 'Global', 'Global')],
                                                         default='LOCAL')
    # add source
    bpy.types.Scene.est_gp_opacity = FloatProperty(name="Opacity", default=1.0, min=0.0, max=1.0)
    bpy.types.Scene.est_gp_thickness = IntProperty(name="Thickness", default=1, min=1, max=10)
    bpy.types.Scene.est_gp_size = IntProperty(name="Size", default=500, soft_min=200, soft_max=2000)
    bpy.types.Scene.est_gp_add_type = EnumProperty(items=lambda _, __: GPAddTypes.enum_add_type_items())
    bpy.types.Scene.est_gp_text = StringProperty(name="Text", default="Hello World")
    bpy.types.Scene.est_gp_text_font = PointerProperty(type=bpy.types.VectorFont)
    bpy.types.Scene.est_gp_obj = PointerProperty(name='Object', type=bpy.types.Object,
                                                 poll=lambda self, obj: obj.type in {'MESH', 'GPENCIL'})
    bpy.types.Scene.est_gp_obj_shot_angle = EnumProperty(name="Shot Orientation",
                                                         items=lambda _, __: ShootAngles.enum_shot_orient_items())
    bpy.types.Scene.est_gp_icon = StringProperty(name="Icon", default="BLENDER")
    bpy.app.handlers.load_post.append(init_scene_props)


def unregister():
    ColorPaletteModel.unregister_color_icon()

    bpy.app.handlers.load_post.remove(init_scene_props)
    del bpy.types.Scene.est_gp_size
    del bpy.types.Scene.est_gp_add_type
    del bpy.types.Scene.est_gp_text
    del bpy.types.Scene.est_gp_obj
    del bpy.types.Scene.est_gp_obj_shot_angle
    del bpy.types.Scene.est_gp_transform_mode
    del bpy.types.Scene.est_gp_icon
    del bpy.types.Scene.est_palette_color
