# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0
"""
Below functions are defined in the scripts 
    1) Add-on installations 
    2) Setting rendering device - GPU/CPU
    3) Rendering scene
    4) Setting viewport - as renderview mode
    5) Finding document bounding boxes in final rendered image
    6) Adding background image to scene
"""
import os
import math
from collections import namedtuple

import bpy
import numpy as np
from bpy_extras.object_utils import world_to_camera_view

def install_addons(add_on_filepaths: dict = None):
    """
    Install add-ons provided by the user as well as some default add ons
    add_on_filepaths is a dict and where key is the add on name and value is the path in local directory
    {"add_on_name":"add_on_value"}
    """
    if add_on_filepaths != None:
        for addon, addon_path in add_on_filepaths.items():
            bpy.ops.preferences.addon_install(filepath=addon_path)
            bpy.ops.preferences.addon_enable(module=addon)
    # default add ons
    bpy.ops.preferences.addon_enable(module="io_import_images_as_planes")
    addons = [addon.module for addon in bpy.context.preferences.addons]
    print("Add-ons installed are {}".format(addons))


def set_render_device(device_type):
    """
    Sets the rendering device type. sim2real_docs currently accepts only CUDA devices for GPUs
    """
    if device_type == "GPU":
        bpy.context.scene.cycles.device = "GPU"
        bpy.context.preferences.addons[
            "cycles"
        ].preferences.compute_device_type = "CUDA"
        prefs = bpy.context.preferences.addons["cycles"].preferences
        print("The computing device is {}".format(prefs.compute_device_type))
        for device in prefs.devices:
            device.use = True
        bpy.context.scene.cycles.feature_set = "SUPPORTED"
    else:
        bpy.context.scene.cycles.device = "CPU"


def render_scene(save_path: str, image_name: str, camera_name: str):
    """
    Renders the entire scene.
    """
    bpy.ops.object.select_all(action="DESELECT")
    bpy.data.objects[camera_name].select_set(True)
    bpy.context.scene.render.filepath = os.path.join(save_path, image_name)
    bpy.ops.render.render(write_still=True)


def set_render_viewport():
    """
    There are different viewport available in blender. Display in solid mode, wire edges, render preview and meterial preview mode.
    Render preview mode is set as viewport
    """
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            area.spaces[0].shading.type = "RENDERED"


def image_3d_to_2d_coords(vertices, scene_configs):
    """
    This function converts 3d coordinates of an image object to 2d coordinates (pixel space)
    """
    # aranging the coordinates according in the direction of top left, bottom left, bottom right, top right
    # vertex_indices
    # 0 bottom left
    # 1 bottom right
    # 2 top left
    # 3 top right
    re_order = [2, 0, 3, 1]
    vertices = [vertices[i] for i in re_order]
    render = bpy.context.scene.render
    render_scale = render.resolution_percentage / 100
    # image size before cropping
    render_size = (
        int(render.resolution_x * render_scale),
        int(render.resolution_y * render_scale),
    )
    # getting relative coordinates
    bbox = [
        world_to_camera_view(bpy.context.scene, bpy.context.scene.camera, coord)[:2]
        for coord in vertices
    ]
    # find the relative width and height of final rendered image
    relative_crop_width = scene_configs.crop_max_x - scene_configs.crop_min_x
    relative_crop_height = scene_configs.crop_max_y - scene_configs.crop_min_y
    rendered_width = relative_crop_width * render_size[0]
    rendered_height = relative_crop_height * render_size[1]
    # With image relative coordinates in scene and final rendered image, bounding boxes are identified in final rendered image calculations are made
    # There might be negative values for bounding boxes as we are applying scene cropping paramteres.
    bbox_px = [
        (
            (rendered_width * (i[0] - scene_configs.crop_min_x)) / relative_crop_width,
            (rendered_height * (i[1] - scene_configs.crop_min_y))
            / relative_crop_height,
        )
        for i in bbox
    ]
    bbox_px = [(coord[0], rendered_height - coord[1]) for coord in bbox_px]
    return bbox_px


def add_n_scale_background_image(image_variation: namedtuple, bg_image_path: str):
    """
    This function adds a background image to the scene.
    The image added here is scaled to a fixed dimensions for it to appear as background images
    The assumption is that original image dimension is not greater than (4,0,4.0, 4.0). The dimensions here are in meters
    """
    bg_image_name = image_variation.background_image_name
    bg_scale_x, bg_scale_y, bg_scale_z = (4.0, 4.0, 0.010)
    bpy.ops.import_image.to_plane(
        files=[
            {
                "name": "{}".format(bg_image_name),
            }
        ],
        directory=bg_image_path,
        relative=False,
    )
    bg_object_name = bpy.context.view_layer.objects.active.name
    bg_image = bpy.data.objects[bg_object_name]
    bg_image.scale[0] = bg_scale_x
    bg_image.scale[1] = bg_scale_y
    bg_image.scale[2] = bg_scale_z
    bpy.ops.object.select_all(action="DESELECT")
    return bg_image_name


def get_collection_name():
    """
    Blender scene has collections and objects are added to those collections. For document rendering the code is using a single collections.
    For example, to add the camera object to the collection, this function gets the collection name
    """
    scene_collections = [i.name for i in bpy.data.collections]
    assert len(scene_collections) == 1, "There should be only one collections"
    collection_name = scene_collections[0]
    return collection_name


def create_dir(path: str):
    """
    This function creates a directory for the path specified
    """
    if not os.path.exists(path):
        os.mkdir(path)


def check_path_exists(path: str):
    """
    Function to check if input path exists
    """
    assert isinstance(path, str), "Input path should be a string"
    try:
        if os.path.exists(path):
            print("Input path exists")
    except:
        print("Provided input path does not exists")


def clear_segmentation_nodes(segmentation_path: str, comp_nodes):
    for node in list(comp_nodes):
        if node.name not in ["Composite", "Render Layers"]:
            comp_nodes.remove(node)
