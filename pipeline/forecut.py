"""
ForeCut :: Pipeline execution module

To run the ForeCut pipeline, simply import and call
the `forecut.remove_bg()` function.
"""

# Std library
import os
import math
import multiprocessing as mp
import sys

# 3rd party
import numpy as np
import skimage.io
from tqdm import tqdm

# Root directory of the project
# To import local packages and modules
ROOT_DIR = os.path.abspath("./Mask_RCNN")
sys.path.append(ROOT_DIR)

# Import forecut pipeline
from forecut_pipeline.load_image import LoadImage
from forecut_pipeline.load_images import LoadImages
from forecut_pipeline.predict import Predict
from forecut_pipeline.pipeline import Pipeline
from forecut_pipeline.remove_bg import RemoveBg
from forecut_pipeline.save_image import SaveImage
from forecut_pipeline.utils.maskr import setup_model
from forecut_pipeline.utils.vars import coco_class_names

# Import Mask R-CNN
from mrcnn import utils
import mrcnn.model as modellib

# # Import COCO config
# sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))
# import coco

# # Directory to save logs and trained model
# MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# # Local path to trained weights file
# COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
# # Download COCO pre-trained weights if needed
# if not os.path.exists(COCO_MODEL_PATH):
#     utils.download_trained_weights(COCO_MODEL_PATH)

# Directory of input images
IMAGE_DIR = os.path.join(ROOT_DIR, "images")


def forecut(input_path=IMAGE_DIR, output_path="output", progress=True):
    """
    ForeCut :: Removes image background
    
    Parameters
    ----------
    input_path : str / path
        Path to input image file or directory.
    output_path : str / path, optional
        Path to output directory, default "output"
    progress : bool, optional
        Display progress, by default True
    """

    # Modify images directory if needed
    # IMAGE_DIR = os.path.join(ROOT_DIR, input_path)

    # Create output directory if needed
    os.makedirs(output_path, exist_ok=True)

    # === Define pipeline steps === #

    # 1. Load image(s)
    load_images = (
        LoadImages(input_path) if os.path.isdir(input_path) else LoadImage(input_path)
    )

    # 2. Create model instance + predict
    model = setup_model()

    # 2.1 Predict
    predict = Predict(model)

    # 4. Remove background
    vimg = "vimg"
    remove_bg = RemoveBg(vimg)

    # 5. Save image(s)
    save_image = SaveImage(vimg, output_path)

    # === Create the pipeline === #
    pipeline = load_images | predict | remove_bg | save_image

    # Iterate through pipeline
    try:
        for _ in tqdm(pipeline, disable=not progress):
            pass
    except StopIteration:
        return
    except KeyboardInterrupt:
        return


def forecut_multiple(input_paths, output_path="output", progress=True):
    """
    ForeCut :: Removes image background
    
    Parameters
    ----------
    input_path : str / path
        Path to input image file or directory.
    output_path : str / path, optional
        Path to output directory, default "output"
    progress : bool, optional
        Display progress, by default True
    """

    # Create output directory if needed
    os.makedirs(output_path, exist_ok=True)

    # === Define pipeline steps === #

    # Create model instance
    model = setup_model()

    total_input_paths = len(input_paths)
    path_counter = 1
    for path in input_paths:
        print("Removing background "+str(path_counter)+" out of "+str(total_input_paths))
        print(path)
        # Load image
        load_images = LoadImages(path) if os.path.isdir(path) else LoadImage(path)

        # Predict
        predict = Predict(model)

        # Remove background
        vimg = "vimg"
        remove_bg = RemoveBg(vimg)

        # Save image
        save_image = SaveImage(vimg, output_path)

        # === Create the pipeline === #
        pipeline = load_images | predict | remove_bg | save_image

        # Iterate through pipeline
        try:
            for _ in tqdm(pipeline, disable=not progress):
                path_counter += 1
                pass
        except StopIteration:
            return
        except KeyboardInterrupt:
            return
