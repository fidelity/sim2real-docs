# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0
"""
This script defines all methods that need to be applied on an light object
"""
import bpy
from mathutils import Color


class Light:
    def __init__(self, light_configs):
        self.light_configs = light_configs
        light_data = bpy.data.lights.new(
            name="light", type=self.light_configs.light_type
        )
        light_object = bpy.data.objects.new(name="light", object_data=light_data)
        bpy.context.collection.objects.link(light_object)
        self.light_object = light_object

    def set_light_location(self):
        """
        The method sets light location
        """
        self.light_object.location[0] = self.light_configs.light_x_location
        self.light_object.location[1] = self.light_configs.light_y_location
        self.light_object.location[2] = self.light_configs.light_z_location

    def set_light_energy(self):
        self.light_object.data.energy = self.light_configs.light_energies

    def set_light_color(self):
        """
        "Blender RGB values ranges from 0,1 instead of 255. Therefore using hsv values"
        selecting the HSV values of a light
        """
        bpy.ops.object.select_all(action="DESELECT")
        bpy.data.objects[self.light_object.name].select_set(True)
        bpy.context.view_layer.objects.active = self.light_object
        color_object = Color()
        color_object.hsv = (
            self.light_configs.color_hue,
            self.light_configs.color_saturation,
            self.light_configs.color_value,
        )
        bpy.context.object.color = (color_object.r, color_object.g, color_object.b, 1.0)
        bpy.ops.object.select_all(action="DESELECT")
        return color_object
