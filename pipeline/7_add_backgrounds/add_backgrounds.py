#!/usr/bin/env python3

import os
import uuid
from random import randint
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

images_folder_name = 'input'

# Image category blacklist, currently used for testing
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
    # Save resulting image to output folder, named a random UUID (for now)
    bg.save('./output/'+infile, "PNG")


image_filepaths = []
image_folderpaths = []
bg_filepaths = []
bg_folderpaths = []

for r, d, f in os.walk('.', topdown=False):
    for file in f:
        if file != '.DS_Store': # macOS constantly adds this file we don't want
            if './'+images_folder_name+'/' in r:
                path = os.path.join(r.replace('./'+images_folder_name+'/', ''), file)
                folder = os.path.join(r.replace('./'+images_folder_name+'/', ''))
                image_filepaths.append(path)
                image_folderpaths.append(folder)
            elif './bg/' in r:
                path = os.path.join(r.replace('./bg/', ''), file)
                folder = os.path.join(r.replace('./bg/', ''))
                bg_filepaths.append(path)
                bg_folderpaths.append(folder)

'''
print(image_filepaths)
print()
print(image_folderpaths)
print()
print(bg_filepaths)
print()
print(bg_folderpaths)
print()
'''

unique_objects = list(set(image_folderpaths))
number_bg_folders = len(list(set(bg_folderpaths)))

for unique_object in unique_objects:
    if not os.path.exists('./output/'+unique_object):
        os.makedirs('./output/'+unique_object)

for x in range(0,len(image_filepaths)):
    print(image_filepaths[x])
    print(image_folderpaths[x])
    print(blacklist[image_folderpaths[x]])
    if (len(blacklist[image_folderpaths[x]]) >= number_bg_folders):
        print('You blacklisted all background types. Skipping image.')
    else:
        random_image = randint(0, len(bg_filepaths) - 1)
        while bg_folderpaths[random_image] in blacklist[image_folderpaths[x]]:
            random_image = randint(0, len(bg_filepaths) - 1)
        print(bg_filepaths[random_image])
        print()
        append_background(image_filepaths[x], bg_filepaths[random_image])