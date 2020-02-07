#!/usr/bin/env python3

""" add_backgrounds adds a random background to every image in an input folder.
Based on the object in the image, it's possible to blacklist certain
backgrounds (ex: no tires on a carpet background).

The appended background will first scale to the size of the image, then crop
such that the background's dimensions are identical to the image. This is so
the bounding boxes remain accurate.

Parsed images will appear in an output folder, retaining the same directories
and file names.
"""

import os
from shutil import copyfile
from random import randint
from PIL import Image

images_folder_name = 'input'

# Image category blacklist, currently used for testing
# Background categories include:
# abstract
# carpet
# garage
# greenery
# hardwood
# inside_car
# tabletop
# urban_outdoor
blacklist = {
    'tires': ['tabletop', 'carpet', 'abstract'],
    'battery': ['greenery', 'urban_outdoor']
    }


def append_background(infile, inbg):
    """ Function to paste background to an image and save it
    INPUT: original image, background image
    OUTPUT: image rendered
    """

    try:  # Check if the files are images
        img = Image.open('./'+images_folder_name+'/'+infile).convert('RGBA')
        bg = Image.open('./bg/'+inbg).convert('RGBA')
        width, height = img.size
        bgWidth, bgHeight = bg.size
    except:
        print("At least one of the files is not an image.")
        return
    # Get aspect ratios of the input and background images
    aspectRatio = width / height
    bgAspectRatio = bgWidth / bgHeight
    if (aspectRatio > bgAspectRatio):  # input image is wider
        # Resize BG such that BG width = input image width
        newBgWidth = width
        newBgHeight = int(newBgWidth * bgHeight / bgWidth)
        bg = bg.resize((newBgWidth, newBgHeight), Image.ANTIALIAS)
        # Paste input image to BG, center-aligned
        bg.paste(img, (0, int((newBgHeight / 2) - (height / 2))), img)
        # Crop image to retain input image dimensions
        bg = bg.crop((0, int((newBgHeight / 2) - (height / 2)),
                     width, int((newBgHeight / 2) + (height / 2))))
    else:  # background is wider
        # Resize BG such that BG width = input image width
        newBgHeight = height
        newBgWidth = int(newBgHeight * bgWidth / bgHeight)
        bg = bg.resize((newBgWidth, newBgHeight), Image.ANTIALIAS)
        # Paste input image to BG, center-aligned
        bg.paste(img, (int((newBgWidth / 2) - (width / 2)), 0), img)
        # Crop image to retain input image dimensions
        bg = bg.crop((int((newBgWidth / 2) - (width / 2)), 0,
                     int((newBgWidth / 2) + (width / 2)), height))
    # Save resulting image to output folder, located in the same directory/file
    # name as oriented in the input folder
    bg.save('./output/'+infile, "PNG")


image_filepaths = []  # Will contain all the image filepaths
image_folderpaths = []  # Will contain the folder names of all the images
bg_filepaths = []  # Will contain all the background filepaths
bg_folderpaths = []  # Will contain all the folder names of all the backgrounds

for r, d, f in os.walk('.', topdown=False):
    for file in f:
        # Discard unwanted macOS file
        if file != '.DS_Store':
            # For all the input images
            if './'+images_folder_name+'/' in r:
                path = os.path.join(r.replace('./'+images_folder_name+'/',
                                              ''), file)
                folder = os.path.join(r.replace('./'+images_folder_name+'/',
                                                ''))
                image_filepaths.append(path)
                image_folderpaths.append(folder)
            # For all the background images
            elif './bg/' in r:
                path = os.path.join(r.replace('./bg/', ''), file)
                folder = os.path.join(r.replace('./bg/', ''))
                bg_filepaths.append(path)
                bg_folderpaths.append(folder)

# Get a list of all the unique objects (for directory creation)
unique_objects = list(set(image_folderpaths))
# Get the number of background categories (to prevent infinite loop
# if all background categories are blacklisted)
number_bg_folders = len(list(set(bg_folderpaths)))

# Create the directories of the object names in the output folder
for unique_object in unique_objects:
    if not os.path.exists('./output/'+unique_object):
        os.makedirs('./output/'+unique_object)

# For all the input images
for x in range(0, len(image_filepaths)):
    print(image_filepaths[x])
    try:
        if (len(blacklist[image_folderpaths[x]]) >= number_bg_folders):
            print('You blacklisted all background types. Skipping image.')
            copyfile('./'+images_folder_name+'/'+image_filepaths[x],
                     './output/'+image_filepaths[x])
            continue
        else:
            # Pick a random background
            random_image = randint(0, len(bg_filepaths) - 1)
            # Reroll if selected background is in the blacklist
            while bg_folderpaths[random_image] in \
                blacklist[image_folderpaths[x]]:
                random_image = randint(0, len(bg_filepaths) - 1)
            append_background(image_filepaths[x], bg_filepaths[random_image])
    except KeyError: # Object has no blacklist
        random_image = randint(0, len(bg_filepaths) - 1)
        append_background(image_filepaths[x], bg_filepaths[random_image])
