#!/usr/bin/env python3

import cv2
import hashlib
import imghdr
import numpy as np
import os
from PIL import Image, ImageDraw
from preprocess import (
    image_resize,
    file_as_bytes,
    hash_file,
    rename_files,
    is_transparent,
    append_background,
    blacklist,
    update_classes
)
from random import randint
import sys
from yolo_label_tools import count_from_top, find_pixel_edges, find_yolo_coordinates

from forecut import forecut, forecut_multiple


image_dir = "images"
class_file = "classes.txt"


images = []
texts = []
errors = []
for r, d, f in os.walk(image_dir, topdown=False):
    for file in f:
        path = os.path.join(r, file)
        if imghdr.what(path) != None:
            images.append(path)
        elif path.endswith(".txt"):
            texts.append(path)
        else:
            errors.append(path)

# TODO: deal with errors

#### Prompt to perform updating of any text files (from an update to class_file)
update_classes(class_file, texts)

#### Find unlabeled (i.e. new) images
images_basenames = [os.path.splitext(image)[0] for image in images]
images_extensions = [os.path.splitext(image)[1] for image in images]
extensions_dict = dict(zip(images_basenames, images_extensions))
texts_basenames = [os.path.splitext(text)[0] for text in texts]
print(texts_basenames)
lonely_images = set(images_basenames) - set(texts_basenames)
print(lonely_images)
unlabeled_images = [li + extensions_dict[li] for li in lonely_images]

print("Unlabeled images: ", unlabeled_images)
print()
print("Renaming/resizing images...\n")
#### rename, resize and separate new images
transparent_filepaths = []
opaque_filepaths = []
unique_images = list(
    set(images) - set(unlabeled_images)
)  # labeled images (already preprocessed)
for unlabeled_image in unlabeled_images:
    new_name = rename_files(unlabeled_image, unique_images)
    try:
        image_resize(new_name)
        if is_transparent(new_name):
            transparent_filepaths.append(new_name) if new_name not in transparent_filepaths else None
        else:
            opaque_filepaths.append(new_name) if new_name not in opaque_filepaths else None
    except FileNotFoundError:
        print("File not found")
        continue

#### Take care of transparent images
print("Transparent images: ", transparent_filepaths)
print()
print("Opaque images: ", opaque_filepaths)
print()

# Add bounding boxes
print("Adding bounding boxes to transparent images...\n")
class_labels = []
with open("classes.txt") as f:
    for line in f:
        class_labels.append(line.strip("\n"))


for transparent_path in transparent_filepaths:
    class_label = os.path.normpath(transparent_path).split(os.sep)[1]
    class_label_number = str(class_labels.index(class_label))  # yolo counts from 0
    coordinates = find_yolo_coordinates(transparent_path)

    # remove blank image, (repeated below, consider during refactorization
    if coordinates == None:
        print("blank image:", transparent_path,'removing...')
        os.remove(transparent_path)
        transparent_filepaths.remove(transparent_path)
        continue

    coordinates = [str(coordinate) for coordinate in coordinates]
    line = " ".join([class_label_number] + coordinates)
    file_stem = os.path.splitext(transparent_path)[0]
    with open(f"{file_stem}.txt", "w") as f:
        f.write(line)


# Add background!!!

print("Adding backgrounds to transparent images...\n")

image_filepaths = transparent_filepaths  # Contains all the image filepaths
image_folderpaths = [
    os.path.normpath(transparent_filepath).split(os.sep)[1]
    for transparent_filepath in transparent_filepaths
]  # Contains the folder names of all the images
bg_filepaths = []  # Will contain all the background filepaths
bg_folderpaths = []  # Will contain all the folder names of all the backgrounds


for r, d, f in os.walk("bg", topdown=False):
    for file in f:
        # For all the background images
        path = os.path.join(r, file)
        folder = os.path.normpath(r).split(os.sep)[1]
        bg_filepaths.append(path)
        bg_folderpaths.append(folder)

# Get the number of background categories (to prevent infinite loop
# if all background categories are blacklisted)
number_bg_folders = len(list(set(bg_folderpaths)))


for x in range(0, len(image_filepaths)):
    try:
        if len(blacklist[image_folderpaths[x]]) >= number_bg_folders:
            print("You blacklisted all background types. Skipping image.")
            # continue
        else:
            # Pick a random background
            random_image = randint(0, len(bg_filepaths) - 1)
            # Reroll if selected background is in the blacklist
            while bg_folderpaths[random_image] in blacklist[image_folderpaths[x]]:
                random_image = randint(0, len(bg_filepaths) - 1)
            append_background(image_filepaths[x], bg_filepaths[random_image])
    except KeyError:  # Object has no blacklist
        print("Warning: Object not in blacklist")
        random_image = randint(0, len(bg_filepaths) - 1)
        append_background(image_filepaths[x], bg_filepaths[random_image])

print()

# === Background Removal === #
# TODO: Create (if not already existing) an `output` directory with the same
# file structure of subdirectories and images
# ====== ============ ====== #

if (len(opaque_filepaths) > 0):
    forecut_multiple(opaque_filepaths)  # creates file without background
else:
    print("No background removal needed")
blank_images = [] # If model removes everything, we must deal with it manually

for opaque_path in opaque_filepaths:  # e.g. opaque_path = images/tires/abc.jpg
    file_stem = os.path.splitext(opaque_path)[0]  # images/tires/abc
    output_file = os.path.join(
        "output", file_stem + ".png"
    )  # output/images/tires/abc.png
    class_label = os.path.normpath(opaque_path).split(os.sep)[1]  # tires
    class_label_number = str(class_labels.index(class_label))  # yolo counts from 0
    coordinates = find_yolo_coordinates(output_file)
    # remove blank images
    if coordinates == None:
        print("blank image:", output_file)
        blank_images.append(opaque_path) # keep images where background is removed
        opaque_filepaths.remove(opaque_path)
        continue

    coordinates = [str(coordinate) for coordinate in coordinates]
    line = " ".join([class_label_number] + coordinates)
    print("appending coordinates:", line)
    with open(f"{file_stem}.txt", "w") as f:
        f.write(line)

if blank_images:
    print("""\nThe background was removed entirely for the following images, \
        consider manual labeling""")
    for blank in blank_images:
        print("blank:", blank)

print("Pipeline complete!")
