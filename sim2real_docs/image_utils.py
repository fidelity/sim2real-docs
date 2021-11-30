# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0
"""
This script defines all methods that need to be applied on an image object
"""

from collections import namedtuple
import bpy
import os
import bmesh
import math


class Image:
    def __init__(self, image_configs, image_path):
        self.image_configs = image_configs
        self.image_path = image_path
        self.image_name = self.image_configs.image_name
        self.create_an_image()
        self.image_name_in_collection = self.get_image_name()
        self.image_object = self.get_object()
        self.image_object.location[2] = 0.05

    def get_object(self):
        """
        Function gets the object
        """
        collection_objects = list(bpy.data.objects)
        object = [
            i for i in collection_objects if i.name == self.image_name_in_collection
        ][0]
        return object

    def get_image_name(self):
        """
        In blender collection, name of the object can be maximum of 63.
        This function gets the file name / object name from the collection
        """
        # Maximum characters allowed for a name in blender is 63.
        name, _ = os.path.splitext(self.image_name)
        image_name = name if len(name) <= 63 else name[:63]
        return image_name

    def create_an_image(self):
        """
        This function imports an images as a plane to the scene
        """
        bpy.ops.import_image.to_plane(
            files=[{"name": self.image_name}],
            directory=self.image_path,
            relative=False,
        )

    def scale_object(self):
        """
        Function to set the scale of the images
        Scale parameters are passed from images config files
        """
        self.image_object.scale[0] = self.image_configs.image_x_scale
        self.image_object.scale[1] = self.image_configs.image_y_scale
        self.image_object.scale[2] = self.image_configs.image_z_scale
        bpy.context.view_layer.update()

    def set_image_rotation(self):
        """
        Function to set the roation of the image
        """
        self.image_object.rotation_euler[0] = math.radians(self.image_configs.image_x_rotation)
        self.image_object.rotation_euler[1] = math.radians(self.image_configs.image_y_rotation)
        self.image_object.rotation_euler[2] = math.radians(self.image_configs.image_z_rotation)
        bpy.context.view_layer.update()

    def get_image_coordinates(self):
        image_collection_name = self.get_image_name()
        image = bpy.data.objects[image_collection_name]
        bpy.ops.object.select_all(action="DESELECT")
        bpy.data.objects[image_collection_name].select_set(True)
        bpy.context.view_layer.objects.active = image
        bpy.ops.object.mode_set(mode="EDIT")
        bm = bmesh.from_edit_mesh(image.data)
        local_vertices = [e for e in bm.verts]
        gloabl_vertices = [image.matrix_world @ i.co for i in local_vertices]
        bpy.ops.object.mode_set(mode="OBJECT")
        return gloabl_vertices

    def get_segmentation_images(self, rendered_path: str, scene_variation: namedtuple):
        assert (
            scene_variation.render_engine == "CYCLES"
        ), "Render engine should be CYCLES not EEVEE"
        scene = bpy.context.scene
        scene.use_nodes = True
        image = bpy.data.objects[self.image_name_in_collection]
        image.pass_index = 255
        nodes = scene.node_tree.nodes
        links = scene.node_tree.links
        scene.view_layers["View Layer"].use_pass_object_index = True
        render_layers = nodes["Render Layers"]
        output_file = nodes.new("CompositorNodeOutputFile")
        output_file.base_path = rendered_path
        output_file.format.color_mode = "BW"
        output_file.format.color_depth = "8"
        math_node = nodes.new("CompositorNodeMath")
        math_node.operation = "DIVIDE"
        links.new(render_layers.outputs["IndexOB"], math_node.inputs["Value"])
        math_node.inputs[1].default_value = 255
        links.new(math_node.outputs["Value"], output_file.inputs["Image"])
        filename, _ = os.path.splitext(self.image_name)
        output_file.file_slots[0].path = filename
        return nodes
