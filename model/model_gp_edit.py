from math import radians, degrees
import bpy
import numpy as np
from mathutils import Vector, Matrix
from typing import Literal

from .model_gp_bbox import GPencilLayerBBox
from .model_gp_property import GPencilStroke


# below Edit Class is all in 3d space

class EditGreasePencilStroke(GPencilStroke):
    """Grease Pencil Stroke, easy to manipulate Stroke data."""

    def _move_stroke(self, stroke: bpy.types.GPencilStroke, v: Vector):
        """Move the grease pencil data."""
        with self.stroke_points(stroke) as points:
            points += v
            stroke.points.foreach_set('co', points.ravel())

    def _scale_stroke(self, stroke: bpy.types.GPencilStroke, scale: Vector, pivot: Vector):
        """Scale the grease pencil data."""
        with self.stroke_points(stroke) as points:
            points = (points - pivot) * scale + pivot
            stroke.points.foreach_set('co', points.ravel())

    def _rotate_stroke(self, stroke: bpy.types.GPencilStroke, angle: int, pivot: Vector):
        """Rotate the grease pencil data around the pivot point."""
        with self.stroke_points(stroke) as points:
            # use numpy to calculate the rotation
            points = ((points - pivot) @ np.array([[np.cos(angle), -np.sin(angle), 0],
                                                   [np.sin(angle), np.cos(angle), 0],
                                                   [0, 0, 1]]) + pivot)

            stroke.points.foreach_set('co', points.ravel())

    def _scale_stroke_local(self, strokes: bpy.types.GPencilStroke, scale: Vector, angle: float, pivot: Vector):
        """rotate around the pivot point. before scale, then rotate back"""
        with self.stroke_points(strokes) as points:
            points = ((points - pivot) @ np.array([[np.cos(angle), -np.sin(angle), 0],
                                                   [np.sin(angle), np.cos(angle), 0],
                                                   [0, 0, 1]]) + pivot)
            points = (points - pivot) * scale + pivot
            points = ((points - pivot) @ np.array([[np.cos(-angle), -np.sin(-angle), 0],
                                                   [np.sin(-angle), np.cos(-angle), 0],
                                                   [0, 0, 1]]) + pivot)
            strokes.points.foreach_set('co', points.ravel())


class EditGreasePencilLayer(EditGreasePencilStroke):
    """Grease Pencil Layer, easy to manipulate Layer data."""

    def get_layer_points(self, layer: bpy.types.GPencilLayer) -> dict[bpy.types.GPencilStroke, np.ndarray]:
        """Return all the points in the layer."""

        return {stroke: self.get_stroke_points(stroke) for frame in layer.frames for stroke in frame.strokes}

    def set_layer_points(self, layer: bpy.types.GPencilLayer, points: dict[bpy.types.GPencilStroke, np.ndarray]):
        """Set all the points in the layer."""
        for frame in layer.frames:
            for stroke in frame.strokes:
                stroke.points.foreach_set('co', points[stroke].ravel())

    def move_layer(self, layer: bpy.types.GPencilLayer, v: Vector):
        v_3d = v.to_3d()
        for frame in layer.frames:
            for stroke in frame.strokes:
                self._move_stroke(stroke, v_3d)

    def rotate_layer(self, layer: bpy.types.GPencilLayer, degree: int, pivot: Vector):
        angle = radians(degree)
        pivot_3d = pivot.to_3d()
        for frame in layer.frames:
            for stroke in frame.strokes:
                self._rotate_stroke(stroke, angle, pivot_3d)

        # store rotation in layer.rotation, but inverse the rotation
        # because rotate from z up view in 3d clockwise, value is negative
        # so store the inverse value, to make it always looks straight in 3d view, easy to debug
        layer.rotation[2] += angle

    def scale_layer(self, layer: bpy.types.GPencilLayer, scale: Vector, pivot: Vector, local=False):
        """Scale the grease pencil data. Local scale will rotate the data first, then scale, then rotate back."""
        pivot_3d = pivot.to_3d()
        scale_3d = scale.to_3d()
        if local:
            angle = -layer.rotation[2]  # since the rotation is stored in the layer, we need to inverse it
            for frame in layer.frames:
                for stroke in frame.strokes:
                    self._scale_stroke_local(stroke, scale_3d, angle, pivot_3d)
        else:
            for frame in layer.frames:
                for stroke in frame.strokes:
                    self._scale_stroke(stroke, scale_3d, pivot_3d)

    def display_in_2d(self, layer: bpy.types.GPencilLayer):
        self._set_display_mode(layer, '2DSPACE')

    def display_in_3d(self, layer: bpy.types.GPencilLayer):
        self._set_display_mode(layer, '3DSPACE')

    def is_in_2d(self, layer: bpy.types.GPencilLayer) -> bool:
        return self._get_display_mode(layer) == '2DSPACE'

    @staticmethod
    def _set_display_mode(layer: bpy.types.GPencilLayer, mode: Literal['2DSPACE', '3DSPACE']):
        for frame in layer.frames:
            for stroke in frame.strokes:
                if stroke.display_mode != mode:
                    stroke.display_mode = mode

    @staticmethod
    def _get_display_mode(layer: bpy.types.GPencilLayer) -> Literal['2DSPACE', '3DSPACE']:
        if not layer.frames or not layer.frames[0].strokes:
            return '3DSPACE'
        return layer.frames[0].strokes[0].display_mode
