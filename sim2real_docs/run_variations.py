# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0
from collections import namedtuple
from .light_utils import Light
from .image_utils import Image
from .scene_utils import Scene
from .camera_utils import Camera
from .utils import image_3d_to_2d_coords


def run_camera_settings(camera_variation: namedtuple, collection_name: str):
    """
    Creates a camera object and applies required variations
    """
    camera_object = Camera(camera_variation, collection_name)
    camera_object.set_focal_length()
    camera_object.set_camera_location()
    camera_object.set_camera_rotation()
    return camera_object


def run_scene_settings(scene_variation: namedtuple):
    """
    Sets a scene for required image rendering.
    Scene object is created from scene_utils file and scene variations are applied
    """
    scene_object = Scene(scene_variation)
    scene_object.clear_scene()
    scene_object.set_resolution()
    scene_object.set_render_engine()
    scene_object.set_color_mode()
    scene_object.set_aspect_ratio()
    scene_object.set_contrast()
    scene_object.set_scene_crop()
    return scene_object


def run_light_settings(light_variation: namedtuple):
    """
    Creates a light object and applies required variations
    """
    light_object = Light(light_variation)
    light_object.set_light_location()
    light_object.set_light_energy()
    light_object.set_light_color()
    return light_object


def run_image_settings(
    image_variation: namedtuple, path: str, scene_variations: namedtuple
):
    """
    This fuction creates an images and applies required variations to it.
    Images are added to the scene as planes.
    It is advised to add camera to the scene before image/document is added and is placed at (0.0,0.0,3.0) to get a top angle view
    """
    # image settings
    image_object = Image(image_variation, path)
    image_object.scale_object()
    image_object.set_image_rotation()
    image_3d_coords = image_object.get_image_coordinates()
    image_2d_coords = image_3d_to_2d_coords(image_3d_coords, scene_variations)
    return image_2d_coords, image_object
