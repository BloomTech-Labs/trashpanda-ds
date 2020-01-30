#!/usr/bin/env python3

import os
import uuid
from random import randint
from PIL import Image, ImageDraw, ImageFont, ImageEnhance


def append_background(infile, inbg):
    """ Function to paste background to an image and save it
    INPUT: original image, background image
    OUTPUT: image rendered
    """

    try:  # Check if the files are images
        img = Image.open(infile).convert('RGBA')
        bg = Image.open(inbg).convert('RGBA')
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
    else:  # background is wider
        # Resize BG such that BG width = input image width
        newBgHeight = height
        newBgWidth = int(newBgHeight * bgWidth / bgHeight)
        bg = bg.resize((newBgWidth, newBgHeight), Image.ANTIALIAS)
        # Paste input image to BG, center-aligned
        bg.paste(img, (int((newBgWidth / 2) - (width / 2)), 0), img)
    # Save resulting image to output folder, named a random UUID
    bg.save('./output/'+str(uuid.uuid4())+'.png', "PNG")

# Get all input image locations in the input folder
inputImages = os.listdir('input')
inputPaths = [f'./input/{inputImage}' for inputImage in inputImages
              if inputImage != '.DS_Store']
# Get all background locations in the bg folder
bgs = os.listdir('bg')
bgPaths = [f'./bg/{bg}' for bg in bgs if bg != '.DS_Store']
# Apply the random background paste for all input images
for inputPath in inputPaths:
    print(inputPath)
    append_background(inputPath, bgPaths[randint(0, len(bgPaths) - 1)])
