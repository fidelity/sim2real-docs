# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0
"""
The scripts create a synthetic images for documents.
"To run the script you need to install the package (package name yet to be decided), run the function get_image_rendering to get rendered images"
"""

import os
import json
from pathlib import Path

from .config import (
    get_configuration_parameters,
    parameter_file,
    run_background_check,
    get_sample_variations,
)
from .utils import (
    install_addons,
    render_scene,
    set_render_device,
    set_render_viewport,
    add_n_scale_background_image,
    get_collection_name,
    check_path_exists,
    create_dir,
    clear_segmentation_nodes,
)
from .run_variations import (
    run_camera_settings,
    run_image_settings,
    run_light_settings,
    run_scene_settings,
)

current_dir = Path(__file__).parent
default_config_path = os.path.join(current_dir, "default_config.json")


def get_configuration_file(user_configs: str, user_all_configs: str):
    """
    Decides on the configuration file to use.
    """
    if user_configs == None and user_all_configs == None:
        with open(default_config_path) as f:
            default_config = json.load(f)
        return default_config, "range"
    elif user_configs != None and user_all_configs == None:
        with open(user_configs) as f:
            user_configs_values = json.load(f)
        return user_configs_values, "range"
    elif user_configs == None and user_all_configs != None:
        with open(user_all_configs) as f:
            user_configs_values = json.load(f)
        return user_configs_values, "all"


def get_image_renderings(
    input_path: str,
    save_path: str,
    add_on_paths: dict = None,
    bg_images_path: str = None,
    seg_path: str = None,
    configs_path: str = None,
    all_configurations: str = None,
):
    """
    Runs blender rendering for the images or files present in the path
        1) identifies number of images present in the given folder
        2) create random variations - light, camera, image, scene
        3) renders an image
        4) clears the scene
        5) saves the metadata
    """
    check_path_exists(input_path)
    create_dir(save_path)
    # background images
    bg_images = run_background_check(bg_images_path)
    # determining configuration files
    configurations, config_type = get_configuration_file(
        configs_path, all_configurations
    )
    (
        image_files,
        variations_required,
        scene_variations,
        light_variations,
        camera_variations,
        image_variations,
        other_parameters,
    ) = get_configuration_parameters(
        input_path,
        configs_params=configurations,
        configuration_type=config_type,
        background_images_list=bg_images,
    )
    install_addons(add_on_paths)
    set_render_device(other_parameters.render_device_type)
    set_render_viewport()
    for i in range(variations_required):
        print("Rendering image - {}".format(image_variations[i].image_name))
        scene = run_scene_settings(scene_variation=scene_variations[i])
        scene_col = get_collection_name()
        camera = run_camera_settings(
            camera_variation=camera_variations[i], collection_name=scene_col
        )  # camera settings
        _ = run_light_settings(light_variation=light_variations[i])  # light settings
        image_2d_coords, image_obj = run_image_settings(
            image_variation=image_variations[i],
            path=input_path,
            scene_variations=scene_variations[i],
        )
        # updating the named tuple to add bounding boxes of document in the final rendered image
        image_variations[i] = image_variations[i]._replace(image_bbs=image_2d_coords)
        # segmentation check
        if seg_path != None:
            check_path_exists(seg_path)
            nodes_present = image_obj.get_segmentation_images(
                seg_path, scene_variations[i]
            )
        # background images
        if len(bg_images) > 0:
            add_n_scale_background_image(image_variations[i], bg_images_path)
        # rendering the image
        render_scene(
            save_path, image_files[i], camera.camera_object.name
        )  # render the scene
        if seg_path != None:
            clear_segmentation_nodes(seg_path, nodes_present)
        scene.clear_scene()  # clear the scene
    # saving the parameters file
    parameter_file(
        scene_params=scene_variations,
        light_params=light_variations,
        camera_params=camera_variations,
        image_params=image_variations,
        save_path=save_path,
        n_variations=variations_required,
        other_params=other_parameters,
    )


def load_config(image_path, image_name=None, bg_path=None, config_file=None):
    (
        scene_params,
        light_params,
        camera_params,
        other_params,
        image_params,
    ) = get_sample_variations(image_path, image_name, bg_path, config_file)
    index = 0
    install_addons()
    set_render_device(other_params.render_device_type)
    set_render_viewport()
    scene_col = get_collection_name()
    scene = run_scene_settings(scene_variation=scene_params[index])
    camera = run_camera_settings(
        camera_variation=camera_params[index], collection_name=scene_col
    )
    light = run_light_settings(light_variation=light_params[index])
    _, image = run_image_settings(
        image_variation=image_params[index],
        path=image_path,
        scene_variations=scene_params[index],
    )
    if image_params[index].background_image_name != "":
        add_n_scale_background_image(image_params[index], bg_path)
    return light.light_object, camera.camera_object, image.image_object
