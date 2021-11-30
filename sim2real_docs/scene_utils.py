# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0
"""
This script defines all methods that sets the scene to render an image
"""

import bpy


class Scene:
    def __init__(self, scene_configs):
        self.scene_configs = scene_configs

    def clear_images(self):
        """
        The function clears the images in the data
        """
        for img in bpy.data.images:
            bpy.data.images.remove(img)

    def clear_meshes(self):
        """
        The function clears the meshes in the data
        """
        for mesh in list(bpy.data.meshes):
            bpy.data.meshes.remove(mesh)

    def clear_material(self):
        """
        The function clears the materials
        """
        for material in list(bpy.data.materials):
            bpy.data.materials.remove(material)

    def clear_scene(self):
        """
        Blender scene starts with a cube camera and a light object.
        Type of light is a parameter and will change on every iteration. Therefore the initial light objects are removed
        Cube object is deleted as it is not required.
        """
        initial_objects = []
        for collection in bpy.data.collections:
            for obj in collection.all_objects:
                initial_objects.append(obj.name)
        for o in bpy.data.objects:
            if o.name in initial_objects:
                o.select_set(True)
        # deleting all the selected objects
        bpy.ops.object.delete(use_global=False)
        self.clear_images()
        self.clear_light_points()
        self.clear_meshes()
        self.clear_material()
        # resetting the scene borders
        bpy.context.scene.render.border_min_x = 0
        bpy.context.scene.render.border_min_y = 0
        bpy.context.scene.render.border_max_x = 1
        bpy.context.scene.render.border_max_y = 1
        bpy.context.scene.render.use_crop_to_border = False
        bpy.context.scene.view_settings.exposure = 1.0
        bpy.context.scene.render.use_border = False
        bpy.context.scene.view_settings.look = "High Contrast"

    def clear_light_points(self):
        """
        The function clears the light points in the data
        """
        lights = list(bpy.data.lights)
        for light in lights:
            bpy.data.lights.remove(light)

    def set_resolution(self):
        """
        Setting the resolution of the scene
        """
        bpy.context.scene.render.resolution_x = self.scene_configs.resolution_x
        bpy.context.scene.render.resolution_y = self.scene_configs.resolution_y
        bpy.context.scene.render.resolution_percentage = (
            self.scene_configs.resolution_percentage
        )

    def set_render_engine(self):
        bpy.context.scene.render.engine = self.scene_configs.render_engine

    def set_color_mode(self):
        """
        Setting final image color mode - RGB, RGBA, BW
        """
        scene = bpy.context.scene
        render = scene.render
        render.image_settings.color_mode = self.scene_configs.color_mode

    def set_aspect_ratio(self):
        """
        Setting aspect ratio of the scene.
        """
        scene = bpy.context.scene
        render = scene.render
        render.pixel_aspect_x = self.scene_configs.aspect_ratio[0]
        render.pixel_aspect_y = self.scene_configs.aspect_ratio[1]

    def set_scene_crop(self):
        """
        Setting scene crop paramaters
        """
        bpy.context.scene.render.use_border = True
        bpy.context.scene.render.border_min_x = self.scene_configs.crop_min_x
        bpy.context.scene.render.border_min_y = self.scene_configs.crop_min_y
        bpy.context.scene.render.border_max_x = self.scene_configs.crop_max_x
        bpy.context.scene.render.border_max_y = self.scene_configs.crop_max_y
        bpy.context.scene.render.use_crop_to_border = True

    def set_contrast(self):
        bpy.context.scene.view_settings.look = self.scene_configs.contrast
