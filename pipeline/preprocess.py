import cv2
import hashlib
import imghdr
import numpy as np
import os
from PIL import Image, ImageDraw
from random import randint
import select, sys


def file_as_bytes(file):
    '''read image file as bytes'''
    with file:
        return file.read()


def hash_file(fpath):
    '''create hash file'''
    return hashlib.md5(file_as_bytes(open(fpath, 'rb'))).hexdigest()



def rename_files(fpath, unique_images):
    # separating the directory path (head) from the file (tail)
    head, tail = os.path.split(fpath)
    # separating the name of the file from its extension
    name, ext = os.path.splitext(tail)
    # find correct file extension 
    ext = '.' + imghdr.what(fpath)
    # getting md5sum for image file
    hash = hash_file(fpath)
    # joining file hash with file extension
    hash_name = hash + ext
    #checking for duplicate files
    if hash_name not in unique_images:
        unique_images.append(hash_name)
        # rename file as file hash + ext 
        os.rename(fpath, os.path.join(head, hash_name))
        print(os.path.join(head, hash_name))
    else:
        os.remove(fpath)                      # remove the duplicates

    return os.path.join(head, hash_name)


def image_resize(image_file):
    ''' Check image width and height. If width or/and height are bigger than 
    1080 pixels, image is resized. Biggest dimension will be 1080 pixels and 
    the other dimension is altered not affecting the aspect ratio'''

    img=Image.open(image_file)
    # img.size is a tuple (width,height)
    img_width = img.size[0]
    img_height = img.size[1]

    maxwidth = 1080    # desired max width
    maxheight = 1080   # desired max height

    # width is bigger than maxwidth and it is the biggest dimension on the image or it is a square image
    if img_width > maxwidth and img_width >= img_height:
        wratio = (maxwidth/float(img_width))
        hsize = int((float(img_height))*(float(wratio)))
        img = img.resize((maxwidth,hsize), Image.ANTIALIAS)
        img.save(image_file)

    # height is bigger than maxheight and it is the biggest dimension on the image
    elif img_height > maxheight and img_height > img_width:
        hratio = (maxheight/float(img_height))
        wsize = int((float(img_width))*(float(hratio)))
        img = img.resize((wsize,maxheight), Image.ANTIALIAS)
        img.save(image_file)


def is_transparent(image_filepath):
    img = Image.open(image_filepath)
    if img.mode == 'RGBA' or 'transparency' in img.info:
        return True
    elif imghdr.what(image_filepath) in ['png','gif']:
        return True
    else:
        return False




def append_background(infile, inbg):
    """ Function to paste background to an image and save it
    INPUT: original image, background image
    OUTPUT: image rendered
    """

    try:  # Check if the files are images
        print(infile)
        img = Image.open(infile).convert('RGBA')
        bg = Image.open(inbg).convert('RGBA')
        width, height = img.size
        bgWidth, bgHeight = bg.size
        print("background appended!")
    except:
        print("File is not an image.")
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
    # name as oriented in the input folder. Hardcode filename change so old extension
    # (e.g. gif) isn't retained
    new_pathname = f"{os.path.splitext(infile)[0]}.png" # Hard code filename change
    os.remove(infile)
    bg.save(new_pathname, "PNG")




blacklist = {
    'aerosol_cans': ['carpet'],
    'aluminium_foil': [],
    'ammunition': [],
    'auto_parts': ['greenery'],
    'batteries': ['abstract'],
    'bicycles': ['inside_car', 'tabletop'],
    'cables': [],
    'cardboard': [],
    'cartridge': [],
    'cassette': [],
    'cd_cases': [],
    'cigarettes': ['carpet'],
    'cooking_oil': ['greenery', 'carpet', 'inside_car', 'urban_outdoor'],
    'cookware': ['greenery', 'carpet', 'inside_car', 'garage', 'urban_outdoor'],
    'corks': ['inside_car'],
    'crayons': [],
    'desktop_computers': ['greenery'],
    'digital_cameras': [],
    'disks': ['abstract'],
    'doors': ['inside_car'],
    'electronic_waste': [],
    'eyeglasses': ['abstract'],
    'fabrics': ['urban_outdoor'],
    'fire_extinguishers': ['urban_outdoor', 'greenery', 'inside_car'],
    'floppy_disks': [],
    'food_waste': ['abstract'],
    'furniture': ['inside_car'],
    'game_consoles': [],
    'gift_bags': [],
    'glass': ['abstract', 'inside_car'],
    'glass_container': ['abstract'],
    'green_waste': ['abstract', 'inside_car', 'carpet'],
    'hardware': ['abstract'],
    'hazardous_fluid': ['carpet', 'abstract'],
    'heaters': ['inside_car'],
    'home_electronics': [],
    'laptop_computers': [],
    'large_appliance': ['inside_car', 'tabletop'],
    'lightbulb': ['abstract'],
    'medication_containers': ['abstract'],
    'medications': [],
    'metal_cans': [],
    'mixed_paper': ['abstract'],
    'mobile_device': [],
    'monitors': [],
    'musical_instruments': ['inside_car', 'tabletop'],
    'nail_polish': [],
    'office_supplies': [],
    'paint': ['abstract'],
    'pallets': ['carpet', 'tabletop', 'inside_car'],
    'paper_cups': [],
    'pet_waste': ['carpet', 'hardwood', 'tabletop', 'abstract'],
    'pizza_boxes': [],
    'plastic_bags': ['abstract'],
    'plastic_bottles': ['abstract'],
    'plastic_caps': [],
    'plastic_cards': [],
    'plastic_clamshells': ['abstract'],
    'plastic_containers': ['abstract'],
    'power_tools': [],
    'printers': [],
    'propane_tanks': [],
    'scrap_metal': [],
    'shoes': [],
    'small_appliances': ['abstract'],
    'smoke_detectors': [],
    'sporting_goods': [],
    'tires': ['tabletop', 'carpet', 'abstract'],
    'tools': ['abstract'],
    'toothbrushes': [],
    'toothpaste_tubes': [],
    'toy': [],
    'vehicles': ['inside_car', 'carpet', 'tabletop'],
    'water_filters': [],
    'wood': ['carpet'],
    'wrapper': ['abstract'],
    }

def update_classes(class_file, text_paths):
    # Add check to update classes. Check is skipped if no response is given in 10 seconds
    print(f"To check for updates in the {class_file} press enter...")
    i, o, e = select.select( [sys.stdin], [], [], 10 )
    if (i):

        classes_dict = {} # dictionary mapping items in classes.txt to line number
        with open(class_file,'r') as f:
            for i, line in enumerate(f):
                classes_dict.update({line.rstrip() : str(i)})

        # Check for changes in each line of each file
        changes = 0 # keep track of number of files changed
        for text_path in text_paths:
            current_class = os.path.normpath(text_path).split(os.sep)[1]
            try:
                new_class_num = classes_dict[current_class]
            except KeyError: # Stops operation if a class has been deleted
                print(f"{'-'*50}\nclass '{current_class}' doesn't exist in '{class_file}'\n manually remove or delete it from images directory and try again")
                exit(1)

            with open(text_path,'r+') as t:
                # convert each line into a list
                # modify the number if necessary
                lines = [line for line in t]
                for i, line in enumerate(lines):
                    #print(line.split(',')[0]) # first number
                    #print(new_class_num)
                    if line.split(' ')[0] != new_class_num:
                        changes += 1
                        print(f"changing class label for '{text_path}' \
                            \nfrom {line.split(' ')[0]} to {new_class_num}")
                        lines[i] =  f"{new_class_num} {' '.join(line.split(' ')[1:])}"

                t.seek(0) # go to zeroth byte in file, fully overwrite, truncate
                t.write(''.join(lines))
                t.truncate()


        if changes > 0:
            print(f"i\nnumber of files changes made: {changes}")
        else: 
            print("\nno changes made to class labels")
    else:
        print("No response, skipping class update")
