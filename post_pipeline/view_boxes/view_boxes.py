#!/usr/bin/env python3

import cv2
import imghdr
import numpy as np
import os
from PIL import Image, ImageDraw
import time


# Show boxes
def show_boxes(image_file,text_file):
    """ A tool for visualizing the created bounding boxes
    NOTE: As written it will only show the first bounding box,
        if multiple lines exist, it will only show the first
    INPUT: local image file, local text file (formatted for yolo)
    OUTPUT: image rendered with bounding boxes
    """
    
    try: # If image is a png RGBA, this throws no error
        img = np.asarray(Image.open(image_file))
        height, width, _ = img.shape
    except: # Convert to RGBA and continue
        img = np.asarray(Image.open(image_file).convert('RGBA'))
        height, width, _ = img.shape


    with open(text_file,'r') as t:
        lines = [line for line in t]
        x,y,w,h = np.array(lines[0].split(',')[1:]).astype('float')

    X, Y = x * width, y * height # Center of box (in pixel count)
    x_left, y_top = X - .5 * w * width, Y - .5 * h * height
    x_right, y_bottom = (x_left + w*width, y_top + h*height)

    x_left, y_top = np.array([x_left, y_top]).astype('int')


    print(image_file)
    # Reload image to draw box on
    image = cv2.imread(image_file)


    start_point = (x_left, y_top) # Top Left
    end_point = (x_left + int(width * w), y_top + int(height * h))  # Bottom Right

    color = (0, 255, 0) # Bounding box is Green - Arbitrary choice
    thickness = 2 # Line thickness: 2 pixels
    
    # Using cv2.rectangle() method, draw green rectangle 
    image_with_box = cv2.rectangle(image, start_point, end_point, color, thickness)

    # Display the image  
    cv2.imshow(image_file, image_with_box)
    cv2.waitKey(200) # necessary otherwise the image doesn't render
    time.sleep(1)
    cv2.destroyAllWindows()


# uncomment below to view boxes on multiple files at once
# ASSUMPTION: There is a directory named "classes" containing sub directories of images
# with corresponding .txt files with yolo labels (i.e. the multifile_labeling.py 
# has been run

"""
# Pair image to .txt. Flag if missing
image_types = ['png','jpg']
image_dir = 'classes'

images = []
texts = []
errors = []
for r, d, f in os.walk(image_dir, topdown=False):
    for file in f:
        path = os.path.join(r, file)
        if imghdr.what(path) in image_types:
            images.append(path)
        elif path.endswith('.txt'):
            texts.append(path)
        else:
            print("non-conforming file:",path)
            print(imghdr.what(path))
            print()

images = sorted(images)
texts = sorted(texts)

if len(errors) > 0:
    print("file errors:",errors)

print(images)

flagged_images = []
for i,image in enumerate(images):
    current_image = os.path.splitext(image)[0]
    current_text = os.path.splitext(texts[i])[0]
    if current_image == current_text:
        show_boxes(image, texts[i])
        #pass # Success, stay silent
    else:
        print(f"Error pairing image: {current_image} with text {current_text}")
        resp = input("Flag image and Continue? <y/n>")
        if resp == 'n':
            pass
        elif resp == 'y':
            flagged_images.append(image)
        else:
            print("Response not understood, keeping image, continuing")
if flagged_images:
    print("Problems with these images:",flagged_images)
"""
# Test for single local image.
image = "10.cd4160_288fa06c8d6d4e47a61dfef1bd69ba2c~mv2.png"

text = "10.cd4160_288fa06c8d6d4e47a61dfef1bd69ba2c~mv2.txt"

show_boxes(image,text)

