#!/usr/bin/env python3
"""
TODO
- Error handling if there are non-image files
- Clean up variable names
"""
import os
import uuid
from random import randint
from PIL import Image, ImageDraw, ImageFont, ImageEnhance


def append_background(infile, inbg):
    """ Function to paste background to an image and save it
    INPUT: original image, background image
    OUTPUT: image rendered
    """

    try: # Check if the files are images
        img = Image.open(infile).convert('RGBA')
        bg = Image.open(inbg).convert('RGBA')
        width, height = img.size
        bgwidth, bgheight = bg.size
    except:
        print("At least one of the files is not an image.") 

    print(width, height)
    print(bgwidth, bgheight)

    aspectRatio = width / height
    bgAspectRatio = bgwidth / bgheight

    if (aspectRatio > bgAspectRatio): # Original image is wider
        # Resize BG such that BG width = original image width
        new_bg_width  = width
        new_bg_height = int(new_bg_width * bgheight / bgwidth)
        print(new_bg_width, new_bg_height)
        bg = bg.resize((new_bg_width, new_bg_height), Image.ANTIALIAS)
        bg.paste(img, (0, int((new_bg_height / 2) - (height / 2))), img)
    else: # Background is wider
        # Resize BG such that BG width = original image width
        new_bg_height = height
        new_bg_width  = int(new_bg_height * bgwidth / bgheight)
        print(new_bg_width, new_bg_height)
        bg = bg.resize((new_bg_width, new_bg_height), Image.ANTIALIAS)
        bg.paste(img, (int((new_bg_width / 2) - (width / 2)), 0), img)

    bg.save('./output/'+str(uuid.uuid4())+'.png',"PNG")

# Get all original image locations in the tires folder
images = os.listdir('tires')
paths = [f'./tires/{image}' for image in images  if image != '.DS_Store']
# Get all background locations in the bg folder
bg = os.listdir('bg')
bgpath = [f'./bg/{image}' for image in bg  if image != '.DS_Store']
# Apply the background paste for all original images
for path in paths:
    print(path)
    append_background(path, bgpath[randint(0, len(bgpath))])

