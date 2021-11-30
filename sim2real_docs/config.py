# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0
"""
The script generates variations for the parameters using configuration file and stores them in respective named tuple
"""
import json
import os
from collections import namedtuple
from .create_random_values import (
    get_camera_parameters,
    get_light_parameters,
    get_scene_parameters,
    get_other_blender_parameters,
    get_image_parameters,
    Scene_tuple,
    Camera_tuple,
    Light_tuple,
    Image_tuple,
    other_parameter_tuple,
)
from pathlib import Path
from .utils import check_path_exists
from .create_random_values import other_parameter_tuple

current_dir = Path(__file__).parent
default_config_path = os.path.join(current_dir, "default_config.json")


def get_required_files(
    path: str,
    valid_formats: list = [".jpg", ".jpeg", ".jp2", ".png", ".bmp", ".tiff", ".tif"],
):
    """
    This function determines number of iteration required.
    From the give path, it calculates number of images present
    Right now we support the image formats which are  in [".jpg", ".jpeg", ".jp2", ".png", ".bmp", ".tiff", ".tif"]
    """
    files = os.listdir(path)
    files = [image for image in files if os.path.splitext(image)[1] in valid_formats]
    files_present = len(files)
    print("Number of files present in the given path is {}".format(files_present))
    return files


def parameter_file(
    scene_params: list,
    light_params: list,
    camera_params: list,
    image_params: list,
    save_path: str,
    n_variations: int,
    other_params: namedtuple,
):
    """
    This function stores parameters used for rendering the image set in a json file.
    """
    all_parameters = []
    for i in range(n_variations):
        iteration_dict = {}
        iteration_dict.update({"scene_configs": scene_params[i]._asdict()})
        iteration_dict.update({"light_configs": light_params[i]._asdict()})
        iteration_dict.update({"camera_configs": camera_params[i]._asdict()})
        iteration_dict.update({"image_configs": image_params[i]._asdict()})
        iteration_dict.update({"other_configs": other_params._asdict()})
        all_parameters.append(iteration_dict)
    with open(os.path.join(save_path, "metadata.json"), "w") as f:
        json.dump(all_parameters, f)


def get_render_variations(config_values):
    """
    The function gets all the variation from the user configuration file and stores them in named tuple
    """
    n_variations = len(config_values)
    scene_parameters_list = [Scene_tuple for i in range(n_variations)]
    camera_parameters_list = [Camera_tuple for i in range(n_variations)]
    light_parameters_list = [Light_tuple for i in range(n_variations)]
    image_parameters_list = [Image_tuple for i in range(n_variations)]
    for index, config in enumerate(config_values):
        scene_parameters_list[index] = scene_parameters_list[index](
            aspect_ratio=config["scene_configs"]["aspect_ratio"],
            color_mode=config["scene_configs"]["color_mode"],
            exposure_value=config["scene_configs"]["exposure_value"],
            contrast=config["scene_configs"]["contrast"],
            crop_min_x=config["scene_configs"]["crop_min_x"],
            crop_max_x=config["scene_configs"]["crop_max_x"],
            crop_min_y=config["scene_configs"]["crop_min_y"],
            crop_max_y=config["scene_configs"]["crop_max_y"],
            resolution_x=config["scene_configs"]["resolution_x"],
            resolution_y=config["scene_configs"]["resolution_y"],
            resolution_percentage=config["scene_configs"]["resolution_percentage"],
            render_engine=config["scene_configs"]["render_engine"],
        )
        camera_parameters_list[index] = camera_parameters_list[index](
            camera_x_location=config["camera_configs"]["camera_x_location"],
            camera_y_location=config["camera_configs"]["camera_y_location"],
            camera_z_location=config["camera_configs"]["camera_z_location"],
            camera_focal_length=config["camera_configs"]["camera_focal_length"],
            camera_x_rotation=config["camera_configs"]["camera_x_rotation"],
            camera_y_rotation=config["camera_configs"]["camera_y_rotation"],
            camera_z_rotation=config["camera_configs"]["camera_z_rotation"],
        )
        light_parameters_list[index] = light_parameters_list[index](
            light_energies=config["light_configs"]["light_energies"],
            light_x_location=config["light_configs"]["light_x_location"],
            light_y_location=config["light_configs"]["light_y_location"],
            light_z_location=config["light_configs"]["light_z_location"],
            color_hue=config["light_configs"]["color_hue"],
            color_saturation=config["light_configs"]["color_saturation"],
            color_value=config["light_configs"]["color_value"],
            light_type=config["light_configs"]["light_type"],
        )
        image_parameters_list[index] = image_parameters_list[index](
            image_x_scale=config["image_configs"]["image_x_scale"],
            image_y_scale=config["image_configs"]["image_y_scale"],
            image_z_scale=config["image_configs"]["image_z_scale"],
            image_x_rotation=config["image_configs"]["image_x_rotation"],
            image_y_rotation=config["image_configs"]["image_y_rotation"],
            image_z_rotation=config["image_configs"]["image_z_rotation"],
            image_bbs=config["image_configs"]["image_bbs"],
            image_name=config["image_configs"]["image_name"],
            background_image_name=config["image_configs"]["background_image_name"],
        )
    return (
        n_variations,
        scene_parameters_list,
        light_parameters_list,
        camera_parameters_list,
        image_parameters_list,
    )


def get_variations(n_variations: int, config: dict, image_files: list, bg_list: list):
    scene_params = get_scene_parameters(n_variations, config["scene_configs"])
    light_params = get_light_parameters(n_variations, config["light_configs"])
    camera_params = get_camera_parameters(n_variations, config["camera_configs"])
    other_blender_params = get_other_blender_parameters(config["others"])
    image_params = get_image_parameters(
        n_variations,
        config["image_configs"],
        image_files,
        bg_list,
    )
    return scene_params, light_params, camera_params, other_blender_params, image_params


def get_configuration_parameters(
    path: str,
    configs_params: str,
    configuration_type: str,
    background_images_list: list = [],
    num_times: str = 1,
):
    """
    Get variations from configuration file.
    Configuration file can be either defining the range/list of parameter values or all variations applied to a image.
    """
    if configuration_type == "range":
        files = get_required_files(path)
        number_of_variations_required = len(files)
        print(
            "Number of rendering generated are {}".format(number_of_variations_required)
        )
        (
            scene_parameters,
            light_parameters,
            camera_parameters,
            other_blender_parameters,
            image_parameters,
        ) = get_variations(
            number_of_variations_required,
            configs_params,
            files,
            background_images_list,
        )
    else:
        (
            number_of_variations_required,
            scene_parameters,
            light_parameters,
            camera_parameters,
            image_parameters,
        ) = get_render_variations(configs_params)
        files = [i.image_name for i in image_parameters]
        render_device = [
            i["other_configs"]["render_device_type"] for i in configs_params
        ]
        assert (
            len(set(render_device)) == 1
        ), "The parameter file contains multiple render devices. Please provide either a GPU or CPU"
        other_blender_parameters = other_parameter_tuple(
            render_device_type=render_device[0]
        )
    return (
        files,
        number_of_variations_required,
        scene_parameters,
        light_parameters,
        camera_parameters,
        image_parameters,
        other_blender_parameters,
    )


def get_background_images(bg_path: str):
    bg_files = get_required_files(bg_path)
    assert len(bg_path) > 0, "No background images found"
    return bg_files


def run_background_check(bg_path: str):
    """
    Checks on background images path specified and returns background image names present in the path specified
    """
    if bg_path == None:
        return []
    else:
        assert isinstance(bg_path, str), "Background image path should be a str"
        bg_image_files = get_background_images(bg_path)
        return bg_image_files


def get_sample_variations(
    image_path,
    image_name=None,
    bg_path=None,
    config_file=None,
    number_of_variations_required: int = 1,
):
    check_path_exists(image_path)
    # background images
    if config_file == None:
        files = get_required_files(image_path)
        all_files = files * 1
        background_images_list = run_background_check(bg_path)
        with open(default_config_path) as f:
            configs_params = json.load(f)
        (
            scene_parameters,
            light_parameters,
            camera_parameters,
            other_blender_parameters,
            image_parameters,
        ) = get_variations(
            number_of_variations_required,
            configs_params,
            all_files,
            background_images_list,
        )
        if image_name != None:
            image_parameters = [
                i._replace(image_name=image_name) for i in image_parameters
            ]
        return (
            scene_parameters,
            light_parameters,
            camera_parameters,
            other_blender_parameters,
            image_parameters,
        )
    else:
        (
            _,
            scene_parameters,
            light_parameters,
            camera_parameters,
            image_parameters,
        ) = get_render_variations([config_file])
        other_blender_parameters = other_parameter_tuple(
            render_device_type=config_file["other_configs"]["render_device_type"]
        )
        return (
            scene_parameters,
            light_parameters,
            camera_parameters,
            other_blender_parameters,
            image_parameters,
        )
