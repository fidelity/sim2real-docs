# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0
"""
The script generates variations for the parameters using configuration file and stores them in respective named tuple
"""
import math
import random
from collections import namedtuple

import numpy as np

# configuration parameters
scene_options = [
    "aspect_ratio",
    "color_mode",
    "exposure_value",
    "contrast",
    "crop_min_x",
    "crop_max_x",
    "crop_min_y",
    "crop_max_y",
    "resolution_x",
    "resolution_y",
    "resolution_percentage",
    "render_engine",
]
Scene_tuple = namedtuple(
    "SceneParameters", scene_options, defaults=[None] * len(scene_options)
)
light_options = [
    "light_energies",
    "light_x_location",
    "light_y_location",
    "light_z_location",
    "color_hue",
    "color_saturation",
    "color_value",
    "light_type",
]
Light_tuple = namedtuple(
    "LightParameters", light_options, defaults=[None] * len(light_options)
)
camera_options = [
    "camera_x_location",
    "camera_y_location",
    "camera_z_location",
    "camera_x_rotation",
    "camera_y_rotation",
    "camera_z_rotation",
    "camera_focal_length",
]
Camera_tuple = namedtuple(
    "CameraParameters", camera_options, defaults=[None] * len(camera_options)
)
image_options = [
    "image_x_scale",
    "image_y_scale",
    "image_z_scale",
    "image_x_rotation",
    "image_y_rotation",
    "image_z_rotation",
    "image_bbs",
    "background_image_name",
    "image_name",
]
Image_tuple = namedtuple(
    "ImageParameters", image_options, defaults=[None] * len(image_options)
)
other_options = ["render_device_type"]
other_parameter_tuple = namedtuple(
    "OtherBlenderParameters", other_options, defaults=[None] * len(other_options)
)


def random_range(configs, variable, variations):
    """
    Generate random values for the variable in continous scale
    """

    random_values = np.random.uniform(
        configs[variable]["range"][0], configs[variable]["range"][1], variations
    )
    return random_values


def random_categorical_values(configs, variable, variations):
    """
    Generate random values for the variable (e.g aspect ratio etc)
    If weights values are not given, the function assign equal weight to all the values
    """
    try:
        weight_values = configs[variable]["weights"]
    except:
        weight_values = [1.0] * len(configs[variable]["range"])

    random_values = random.choices(
        configs[variable]["range"], k=variations, weights=weight_values
    )
    return random_values


def get_image_parameters(
    n_variations: int, image_configs: dict, image_files: list, bg_list: list
):
    """
    Generate scene variations based on random values in config file and creates a named tuple for each variation
    """
    # sampling background images from background image files
    if len(bg_list) == 0:
        bg_images = [""] * len(image_files)
    else:
        bg_images = [random.choice(bg_list) for i in range(len(image_files))]
    image_parameters_list = [Image_tuple for i in range(n_variations)]
    image_scale_x_values = random_range(image_configs, "image_x_scale", n_variations)
    image_scale_y_values = random_range(image_configs, "image_y_scale", n_variations)
    image_scale_z_values = random_range(image_configs, "image_z_scale", n_variations)
    image_rotation_x_values = random_range(
        image_configs, "image_x_rotation", n_variations
    )
    image_rotation_y_values = random_range(
        image_configs, "image_y_rotation", n_variations
    )
    image_rotation_z_values = random_range(
        image_configs, "image_z_rotation", n_variations
    )
    for index, _ in enumerate(image_parameters_list):
        image_parameters_list[index] = image_parameters_list[index](
            image_x_scale=image_scale_x_values[index],
            image_y_scale=image_scale_y_values[index],
            image_z_scale=image_scale_z_values[index],
            image_x_rotation=image_rotation_x_values[index],
            image_y_rotation=image_rotation_y_values[index],
            image_z_rotation=image_rotation_z_values[index],
            image_bbs=[],
            image_name=image_files[index],
            background_image_name=bg_images[index],
        )
    return image_parameters_list


def get_other_blender_parameters(other_parameters: dict):
    other_parameter_tuple_value = other_parameter_tuple(
        render_device_type=other_parameters["render_device_type"]
    )
    return other_parameter_tuple_value


def get_camera_parameters(n_variations: int, camera_configs: dict):
    """
    Generate camera variations based on random values in config file and creates a named tuple for each variation
    """
    camera_parameters_list = [Camera_tuple for i in range(n_variations)]

    camera_focal_length_values = random_range(
        camera_configs, "camera_focal_length", n_variations
    )
    camera_x_location_values = random_range(
        camera_configs, "camera_x_location", n_variations
    )
    camera_y_location_values = random_range(
        camera_configs, "camera_y_location", n_variations
    )
    camera_z_location_values = random_range(
        camera_configs, "camera_z_location", n_variations
    )
    camera_x_rotation_values = random_range(
        camera_configs, "camera_x_rotation", n_variations
    )
    camera_y_rotation_values = random_range(
        camera_configs, "camera_y_rotation", n_variations
    )
    camera_z_rotation_values = random_range(
        camera_configs, "camera_z_rotation", n_variations
    )
    for index, _ in enumerate(camera_parameters_list):
        camera_parameters_list[index] = camera_parameters_list[index](
            camera_x_location=camera_x_location_values[index],
            camera_y_location=camera_y_location_values[index],
            camera_z_location=camera_z_location_values[index],
            camera_focal_length=camera_focal_length_values[index],
            camera_x_rotation=math.radians(camera_x_rotation_values[index]),
            camera_y_rotation=math.radians(camera_y_rotation_values[index]),
            camera_z_rotation=math.radians(camera_z_rotation_values[index]),
        )
    return camera_parameters_list


def get_light_parameters(n_variations: int, light_configs: dict):
    """
    Generate light variations based on random values in config file and creates a named tuple for each variation
    """
    light_parameters_list = [Light_tuple for i in range(n_variations)]
    light_energies = random_range(light_configs, "light_energy", n_variations)
    light_type_values = random_categorical_values(
        light_configs, "light_types", n_variations
    )
    hue = random_range(light_configs, "hue", n_variations)
    saturation = random_range(light_configs, "saturation", n_variations)
    value = random_range(light_configs, "value", n_variations)
    light_x_values = random_range(light_configs, "light_x_location", n_variations)
    light_y_values = random_range(light_configs, "light_x_location", n_variations)
    light_z_values = random_range(light_configs, "light_x_location", n_variations)
    for index, _ in enumerate(light_parameters_list):
        light_parameters_list[index] = light_parameters_list[index](
            light_energies=light_energies[index],
            light_x_location=light_x_values[index],
            light_y_location=light_y_values[index],
            light_z_location=light_z_values[index],
            color_hue=hue[index],
            color_saturation=saturation[index],
            color_value=value[index],
            light_type=light_type_values[index],
        )
    return light_parameters_list


def get_scene_parameters(n_variations: int, scene_config: dict):
    """
    Generate scene variations based on random values in config file and creates a named tuple for each variation
    """
    scene_parameters_list = [Scene_tuple for i in range(n_variations)]
    aspect_ratio_values = random_categorical_values(
        scene_config, "aspect_ratio", n_variations
    )
    color_mode_values = random_categorical_values(
        scene_config, "color_modes", n_variations
    )
    resolution_values = random_categorical_values(
        scene_config, "resolution", n_variations
    )
    contrast_values = random_categorical_values(scene_config, "contrast", n_variations)
    render_engine_values = random_categorical_values(
        scene_config, "render_engine", n_variations
    )
    exposure_value_values = random_range(scene_config, "exposure", n_variations)
    crop_min_x_values = random_range(scene_config, "crop_min_x", n_variations)
    crop_max_x_values = random_range(scene_config, "crop_max_x", n_variations)
    crop_min_y_values = random_range(scene_config, "crop_min_y", n_variations)
    crop_max_y_values = random_range(scene_config, "crop_max_y", n_variations)
    resolution_percentage_values = random_range(
        scene_config, "resolution_percentage", n_variations
    )
    for index, _ in enumerate(scene_parameters_list):
        scene_parameters_list[index] = scene_parameters_list[index](
            aspect_ratio=aspect_ratio_values[index],
            color_mode=color_mode_values[index],
            exposure_value=exposure_value_values[index],
            contrast=contrast_values[index],
            crop_min_x=crop_min_x_values[index],
            crop_max_x=crop_max_x_values[index],
            crop_min_y=crop_min_y_values[index],
            crop_max_y=crop_max_y_values[index],
            resolution_x=resolution_values[index][0],
            resolution_y=resolution_values[index][1],
            resolution_percentage=resolution_percentage_values[index],
            render_engine=render_engine_values[index],
        )
    return scene_parameters_list
