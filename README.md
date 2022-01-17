# Sim2Real Docs

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)[![code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Introduction 
 Sim2Real Docs is a python framework for synthesizing datasets and performing domain randomization of documents in natural scenes. 
 It enables programmatic 3D rendering of documents using Blender, an open source tool for 3D modeling and ray-traced rendering.
 The library creates a scene and renders a document with varying light, camera and background conditions. These simulated datasets can be used to build robust machine learning models in document space. Further, these models can be iterated upon with real-world data by either fine tuning or making adjustments to domain randomization parameters. 
 
 This work was presented at the Neurips 2021 Data Centric AI Workshop - ["Sim2Real Docs: Domain Randomization for Documents in Natural Scenes using Ray-traced Rendering"](https://arxiv.org/abs/2112.09220).

# Features 
-  Create datasets of documents simulating physical interaction of light, camera and background.
-  It can be extendable by providing blender objects( light, scene, camera, image) incase if you want to add additional functionality as per your usecase.

# Examples

Original W4 on top left and rest are synthetic images with varying lighting, background and camera conditions. 

![](images/combined.png?raw=true "Examples")

# Pre-requisites 
-  Basic knowledge on blender device is recommended. 
-  The Sim2Real Docs is tested on Blender version >=2.91

# Installation instructions 

-   Download and install blender tool. Click [here](https://download.blender.org/release/) to download
-   Blender has python interpreter embedding in it and Sim2Real Docs uses the python environment in blender to render documents. Click [here](https://docs.blender.org/api/current/info_overview.html) to know more about python in blender 

- Running blender in background
    -  To start blender from terminal,set the path as mentioned [here](https://docs.blender.org/manual/en/latest/advanced/command_line/launch/macos.html). This is useful for running blender in background without opening blender tool.

    - Incase if you require elevated access for setting the path, you can create an alias in bash_profile as (blender="/Applications/Blender.app/Contents/MacOS/blender")

    - After the above steps are completed, open a new terminal and type blender. It should open blender tool. 

-   Incase if you want to run python scripts in blender tool, open blender tool, go to scripting tabs, click new or open a file to execute your script.
    Note: Refer this [link](https://docs.blender.org/api/current/info_tips_and_tricks.html)

- To install Sim2Real Docs
        
        git clone <repository>

- Go the blender folder from terminal 
- Run the below command.
        ```
        blender --background --python install.py
        ```

-  To verify if Sim2Real Docs was installed, type blender in terminal to open blender tool, go to scripting tab, click new buttom and run the below command. 

     ``` from sim2real_docs.render_docs import get_image_renderings```

## Available methods

-   All the available methods are in render_docs file. 

### get_image_renderings

-  Runs blender rendering for the images present in image path. 
    -   Sim2Real Docs uses default config file if no configuration file is provided. You can define your own configurations and provide the file path in either configs_path or all_configurations. 
    -   Configuration file provided in configs_path shoud be same as default configuration where you provide a range of values for each parameter whereas in all_configurations, you need to define image specific paramaters values. More on this in configuration section below.

-  Arguments 
    -   input_path * (str): Path where input image documents are present. 
    -   save_path *  (str): Path to save the rendered documents
    -   bg_images_path (optional) (str): Specify the background image path. 
    -   configs_path (optional)(str): user-defined configuration file(json) path. Similar to default configuration files present in sim2real_docs folder. More on this in configuration section 
    -   all_configurations (optional)(str):user-defined configuration file(json) with specific parameters to apply for each image in the input path provided. 
    -   seg_path (optional) (str): path to store the segmentation images. Note, currently blender docs supports semantic segmentation images. Examples below. To get segmentation images, render engine should be provided as CYCLES. 
-   Returns 
    -   Rendered images in save_path.
    -   A metadata file (json) which contains parameter values used to render each image. Will be present in save_path.
    -  Blender docs also provides bounding boxes (image_bbs) of document in the image. The bounding box values are available in metadata.json file

![](images/bb_original.png?raw=true "bounding box original image") ![](images/bb_original_lines.png?raw=true "bounding box displayed image") 

-   Sample Code
    ```
    from sim2real_docs.render_docs import get_image_renderings
    get_image_renderings(input_path = "./input_images",
                        save_path = "./render_images")

    ```

### load_config

-   Loads a configuration for an image and provide the blender objects which can be used for debugging, understanding domain randomization parameters and extending the functionality further. Incase only image path is given, it uses the default configuration file. If a config file is given, it load the values and provide the objects. 

-   Can be used for:
    -   If the image rendered using get_image_renderings method doesn't seems to be as expected, you can load the config values in blender tool and debugg the setting. 
    -   Incase of using configuration file similar to default configuration file, load_config can be used to understand the range of values for each parameters.
    -  Can be used to extend the functionality with the returned objects.

-  Arguments
    -   image_path * (str): Input image documents that need to be rendered
    -   image_name (optional)(str): Image name to be laoded into blender
    -   bg_path (optional)(str):Background image path
    -   config_file (optional)(dict):configuration file
-   Returns
    -  light, camera and image object.

-   Sample code

    Example - 1

    If only input path is provided, a random image from the directory is selected and default configuration is applied 

    ```
    from sim2real_docs.render_docs import load_config
    light_obj, camera_obj, img_obj = load_config(image_path = "./input_images")
     ```
    Example - 2 

    If image name is given, it selects image from the directory and blender objects are returned.  
    ```
    from sim2real_docs.render_docs import load_config
    light_obj, camera_obj, img_obj = load_config(image_path = "./input_images",image_name = "sample_image.png")
    ```

    Example - 3 
    If configuration of an image is given, it loads the image present in the input path and returns the blender objects 
    ```
    from sim2real_docs.render_docs import load_config
    light_obj, camera_obj, img_obj = load_config(image_path = "./input_images",bg_path=background_images_path,config_file = sample_config)

    ```

## Configuration file

-   Configuration file is used to provide parameter values for Sim2Real Docs to render images. It consist of 5 different sections to configure. Scene, Light, camera, Image and others. You can find the description and few examples of each parameter below. 
-   Sim2Real Docs supports user defined configuration file and it must be same as default configuration file. It is recommended to go over the default configuration file before creating your own config files. Default config files is in sim2real_docs folder.
-   Few parameters have weights which defines weightage applied to each value. It is optional and if not given, all values are equally weighted. 
        ```
        "aspect_ratio": {
            "range": [[1, 1], [16, 9], [3, 2], [4, 3], [5, 9]],
            "weights": [0.6, 0.1, 0.1, 0.1, 0.1]
        },
        ```
-   User can also provide metadata file (json) that defines image specific settings. Sim2Real Docs renders the image as per the setting provided in the parameter file. 
        ```
        [{Image_1_settings}, {Image_2_settings}, {Image_3_settings} ...{Image_n_settings}]
        ```
-   **Scene**
    -   exposure_value - exposure of the scene. 
    -   contrast - Blender supports 7 different types of contrast. You can list any of the below contrast values (Very Low Contrast,Low Contrast,Medium Low Contrast,Medium Contrast,Medium High Contrast,High Contrast,Very High Contrast)
    -   crop_min_x - crop the scene along width till the value provided (Read cropping parameter section below)
    -   crop_max_x - crop the scene along width from the value provided
    -   crop_min_y - crop the scene along height till the value provided
    -   crop_max_y - crop the scene along height from the value provided
    -   resolution - resolution of the scene
    -   resolution_percentage - Reduce the dimensions of scene by X percentage. e.g resolution is 1980 X 2048 and resolution_percentage is 50, the rendered image is (1980*.50 X 2048*.50). 
        -   Note: The final rendered image dimensions depend on resolution of scene, resolution percentage and the cropping values defined above. If the crop_min_x is 0.1 and crop_max_x is 0.9, then width of final rendered image is 1980*.50*(0.9 - 0.1). 
    -   aspect_ratio - Aspect ratio of the scene e.g 1:1, 16:9, 4:3 
    -   color_modes - 3 type of color modes - RGB, BW, RGBA
    -   render_engine - Blender support 2 types of render engines - Eevee rendering and cycles rendering. Values to be used in configuration files are "BLENDER EEVEE" for eevee rendering and "CYCLES" for cycles rendering.

    **Cropping parameter** 
    -   The below two sections of images are examples of crop value parameters.
    -   The first section of examples are related to cropping along width direction (min_x/max_x) and second section of images are related to cropping along height direction (min_x/max_x)
    -    The first image is when no cropping parameters are used. The entire scene is rendered. The boundary with yellow line represents scene which will be rendered. 
    -   Second image is when crop min_x is used. The cropping is till the value (e.g 0.1 min_x used below. So the cropping is till 10% of the scene). 
    -   Third is when crop max_x is used. The croppping is from the value(e.g 0.9 min_x used below. So the cropping is from 90% of the scene). 
    -   Last image is the final rendered image after applying both min_x/min_y and max_x/max_y
    - The above points are valid for height direction  

    Width cropping 

    ![](images/crop_entire_scene.png?raw=true "Entire scene") ![](images/crop_min_x.png?raw=true "using min_x") ![](images/crop_max_x.png?raw=true "using max_x") ![](images/crop_both_min_x_max_x.png?raw=true "using both min_x and max_x")

    height cropping

    ![](images/crop_entire_scene.png?raw=true "Entire scene") ![](images/crop_min_y.png?raw=true "using min_y") ![](images/crop_max_y.png?raw=true "using max_y") ![](images/crop_both_min_y_max_y.png?raw=true "using both min_y and max_y")

    Example after using all cropping values (width and height cropping)

    ![](images/crop_using_all_values.png?raw=true "Entire scene")

-   **Light**

    -   light_x_location - X axis location of the light object (in meters)
    -   light_y_location -  Y axis location of the light object (in meters)
    -   light_z_location - Z axis location of the light object(in meters)
    -   light_energy -light intensity/energy value (in Watts). Refer [here](https://docs.blender.org/manual/en/latest/render/lights/light_object.html) for more information 
    -   light_types - blender support 4 different types of light (point, sun, spot and area). Recommended to use POINT or AREA
    -   hue - hue of light color. Value range from 0 to 1
    -   saturation - saturation of light color. Value range from 0 to 1
    -   value - value of light color. Value range from 0 to 1

-   **Image** 

    -   image_x_scale - Scaling the image object by a factor in width direction 
    -   image_y_scale - Scaling the image object by a factor in height direction
    -   image_x_rotation - Rotating the image object along x axis 
    -   image_y_rotation - Rotating the image object in y axis 
    -   image_z_rotation - Rotating the image object along z axis 

-   **Camera**
    -   camera_x_location_values - X axis location of camera object (in meters)
    -   camera_y_location_values - Y axis location of camera object (in meters)
    -   camera_z_location_values - Z axis location of camera object (in meters)
    -   camera_x_rotation_values - Rotating camera object along X axis. Value is in degrees 
    -   camera_y_rotation_values - Rotating camera object along Y axis. Value is in degrees  
    -   camera_z_rotation_values - Rotating camera object along Z axis. Value is in degrees
    -   camera_focal_length_values - Focal length of camera. Value is in mm  

    **Focal Length example**

    ![](images/focal_length.png?raw=true "Focal length image")
-   **Others**

    render_device_type - GPU/CPU.  


# Segmentation Images
-   Note: Currently, Sim2Real Docs only supports generating semantic segmentation images. To get segmentation images, **render engine should be set to CYCLES**.  

    ![](images/bb_original.png?raw=true "segmentation image") ![](images/segmentation_image.png?raw=true "segmentation image") 


# Run in a Docker container
- Clone the repo locally

        git clone <repository>

- Build a docker image
    - With CPU

          docker build -f Dockerfile_ubuntu18.04_cpu -t sim2real .

    - With GPU

          docker build -f Dockerfile_ubuntu18.04_gpu -t sim2real .

- Put your test images in test/input_images and run the container

        docker run -v <absolute path to local copy of the repo>/test:/src/test  -v <absolute path to local copy of the repo>/test/render_images/:/src/render_images --rm -it sim2real bash 

- In the bash, run 

        blender -b -P test/test.py

- In the path test/render_images/, you should get the rendered images and a json file containing the parameters.

# Original Implementation

[Nikhil Maddikunta](https://github.com/nmaddikunta21) [Huijun Zhao](https://github.com/huijunzhao-ds)









    




