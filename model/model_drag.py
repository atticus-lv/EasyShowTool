from dataclasses import dataclass
from mathutils import Vector
from math import degrees
from .model_gp import VecTool, GreasePencilLayerBBox, BuildGreasePencilData


@dataclass
class DragGreasePencilModel:
    gp_data_bbox: GreasePencilLayerBBox
    gp_data_builder: BuildGreasePencilData
    # mouse
    mouse_pos: tuple[int, int]
    mouse_pos_prev: tuple[int, int]
    delta_vec: Vector
    # state / on points
    on_edge_center: Vector = None
    on_corner: Vector = None
    on_corner_extrude: Vector = None
    # state
    in_drag_area: bool = False

    def handle_drag(self, event):
        """Handle the drag event in the modal."""
        # scale mode
        if self.on_edge_center or self.on_corner:  # scale only when near point
            self.on_drag_scale(event)

        # rotate mode
        elif self.on_corner_extrude:
            self.on_drag_rotate()
        # move mode
        elif self.in_drag_area:
            self.on_drag_move()

    def handle_mouse_move_event(self, context, event):
        """Handle the mouse move event in the modal."""
        self.mouse_pos_prev = self.mouse_pos
        self.mouse_pos = event.mouse_region_x, event.mouse_region_y
        self.update_gp_data(context)

        pre_v2d = VecTool.r2d_2_v2d(self.mouse_pos_prev)
        cur_v2d = VecTool.r2d_2_v2d(self.mouse_pos)
        self.delta_vec = Vector((cur_v2d[0] - pre_v2d[0], cur_v2d[1] - pre_v2d[1]))

    def on_drag_scale(self, event):
        """Scale the active layer of the Grease Pencil Object when near the edge center or corner."""
        pivot = self.gp_data_bbox.center
        pivot_r2d = self.gp_data_bbox.center_r2d
        size_x_v2d, size_y_v2d = self.gp_data_bbox.size_v2d

        delta_x, delta_y = (self.delta_vec * 2).xy
        if self.mouse_pos[0] < pivot_r2d[0]:  # if on the left side
            delta_x = -delta_x
        if self.mouse_pos[1] < pivot_r2d[1]:  # if on the bottom side
            delta_y = -delta_y

        if self.on_edge_center:  # scale only one axis

            scale_x = 1 + delta_x / size_x_v2d
            scale_y = 1 + delta_y / size_y_v2d

            if self.on_edge_center[0] == pivot_r2d[0]:
                vec_scale = Vector((1, scale_y, 0))
            else:
                vec_scale = Vector((scale_x, 1, 0))
        else:  # scale both axis
            if self.on_corner[0] == self.gp_data_bbox.min_x:
                delta_x = -delta_x
            if self.on_corner[1] == self.gp_data_bbox.min_y:
                delta_y = -delta_y

            scale_x = 1 + delta_x / size_x_v2d / 2
            scale_y = 1 + delta_y / size_y_v2d / 2

            unit_scale = scale_x if abs(delta_x) > abs(delta_y) else scale_y  # scale by the larger delta
            vec_scale = Vector((unit_scale, unit_scale, 0)) if event.shift else Vector(
                (scale_x, scale_y, 0))

        self.gp_data_builder.scale_active(vec_scale, pivot, space='v2d')

    def on_drag_rotate(self):
        """Rotate the active layer of the Grease Pencil Object when near the corner extrude point."""
        pivot = self.gp_data_bbox.center
        pivot_r2d = self.gp_data_bbox.center_r2d

        vec_1 = (Vector(self.mouse_pos) - Vector(pivot_r2d))
        vec_2 = Vector(self.mouse_pos_prev) - Vector(pivot_r2d)
        # clockwise or counterclockwise
        angle = VecTool.rotation_direction(vec_1, vec_2) * vec_1.angle(vec_2)
        self.gp_data_builder.rotate_active(degrees(angle), pivot)

    def on_drag_move(self):
        # move only when in drag area
        self.gp_data_builder.move_active(self.delta_vec, space='v2d')

    def update_mouse_pos(self):
        """Update the mouse position and the near points."""
        detect = self.gp_data_bbox.detect_model
        self.on_edge_center = detect.near_edge_center(self.mouse_pos, radius=20)
        self.on_corner = detect.near_corners(self.mouse_pos, radius=20)
        self.on_corner_extrude = detect.near_corners_extrude(self.mouse_pos, extrude=20, radius=15)
        self.in_drag_area = detect.in_area(self.mouse_pos, feather=0)

    def update_gp_data(self, context):
        """Update the Grease Pencil Data."""
        self.gp_data_bbox.calc_active_layer_bbox()
        _ = self.gp_data_bbox.bbox_points_3d