#!/usr/bin/env python3

import cv2
import numpy as np
import os
from PIL import Image, ImageDraw
import time

def count_from_top(img):
    """ helper function for find_pixel_edges
    if a row is all zeros or "shaded", a pixel count is added
    INPUT numpy array
    OUTPUT int
    """
    pixel_count = 0
    for row in img:
        unique_pixel_vals = np.unique(row)
        if 255 not in unique_pixel_vals: # ignore shading (values between 0-255)
            pixel_count += 1
        else:
            return pixel_count

def find_pixel_edges(img):
    """Finds the counts of transparent pixels from each edge
    until a non-transparent pixel is found 
    INPUT numpy array
    OUTPUT tuple of 4 ints"""
    
    transparency_cells = img.T[3].T # Ignores rbg, returns only transparency. 
                                    # Values are either:
                                    # 0 (fully transparent) or 
                                    # 1 (not at all transparent)
    right_up = np.rot90(transparency_cells)
    bottom_up = np.rot90(right_up)
    left_up = np.rot90(bottom_up)

    y_top = count_from_top(transparency_cells)
    x_left = count_from_top(left_up)
    y_bottom = count_from_top(bottom_up)
    x_right = count_from_top(right_up)
    #print(f'\ty_top:{y_top}\nx_left:{x_left}\t\tx_right:{x_right}\n\ty_bottom:{y_bottom}')
    return y_top, y_bottom, x_left, x_right






def find_yolo_coordinates(y_top, y_bottom, x_left, x_right, width, height):
    """ Finds the image centers, width and height of an image
    this is the format YOLOv3 uses for its bounding boxes
    INPUT: 6 ints - number of pixels from top, bottom, left and right until
           transparent layer ends, image width and image height
    OUTPUT: tuple of 4 ints: bounding box center x, center y, box width and height
    """
    w = (width - x_left - x_right) / width      # width of bounding box
    h = (height - y_top - y_bottom) / height    # height of bounding box
    x = (1 - w / 2) - x_right / width           # x center of box (distance right from UL)
    y = (1 - h / 2) - y_bottom / height         # y center of box (distance down from UL)

    return x,y,w,h





def show_yolo_boxes(infile):
    """ A tool for visualizing the created bounding boxes
    INPUT: local file
    OUTPUT: image rendered
    """
    try: # If image is a png RGBA, this throws no error
        img = np.asarray(Image.open(infile))
        height, width, _ = img.shape
    except: # Convert to RGBA and continue
        img = np.asarray(Image.open(infile).convert('RGBA'))
        height, width, _ = img.shape

    y_top, y_bottom, x_left, x_right = find_pixel_edges(img)
    x,y,w,h = find_yolo_coordinates(y_top, y_bottom, x_left, x_right, width, height)
    
    # Reload image to draw box on
    image = cv2.imread(infile)

    start_point = (x_left, y_top) # Top Left
    end_point = (x_left + int(width * w), y_top + int(height * h))  # Bottom Right
    
    color = (0, 255, 0) # Bounding box is Green - Arbitrary choice
    thickness = 2 # Line thickness: 2 pixels
    
    # Using cv2.rectangle() method, draw green rectangle 
    image_with_box = cv2.rectangle(image, start_point, end_point, color, thickness)

    # Display the image  
    cv2.imshow(infile, image_with_box)     
    cv2.waitKey(200) # necessary otherwise the image doesn't render
    time.sleep(1)
    cv2.destroyAllWindows()

# An for loop useful for exploring multiple images
images = os.listdir('tires')
paths = [f'./tires/{image}' for image in images]

for path in paths:
    print(path)
    print(np.asarray(Image.open(path)).shape)
    show_yolo_boxes(path)

