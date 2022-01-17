# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""
This script defines all methods that are applied to a camera object
"""

from collections import namedtuple
import bpy
import math


class Camera:
    def __init__(self, camera_configs: namedtuple, collection: str):
        camera = bpy.data.cameras.new("Camera")
        camera_object = bpy.data.objects.new("Camera", camera)
        bpy.data.collections[collection].objects.link(camera_object)
        scene = bpy.context.scene
        scene.camera = bpy.data.objects["Camera"]
        self.camera_configs = camera_configs
        self.camera_object = camera_object

    def set_camera_location(self):
        """
        Function sets the camera location
        """
        self.camera_object.location[0] = self.camera_configs.camera_x_location
        self.camera_object.location[1] = self.camera_configs.camera_y_location
        self.camera_object.location[2] = self.camera_configs.camera_z_location

    def set_camera_rotation(self):
        """
        Function sets the camera roation
        """
        self.camera_object.rotation_euler[0] = math.radians(self.camera_configs.camera_x_rotation)
        self.camera_object.rotation_euler[1] = math.radians(self.camera_configs.camera_y_rotation)
        self.camera_object.rotation_euler[2] = math.radians(self.camera_configs.camera_z_rotation)

    def set_focal_length(self):
        """
        Function sets the camera focal length
        """
        self.camera_object.data.lens = self.camera_configs.camera_focal_length
