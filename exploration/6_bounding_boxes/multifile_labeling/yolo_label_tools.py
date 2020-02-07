import numpy as np
from PIL import Image, ImageDraw

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
    return y_top, y_bottom, x_left, x_right




def find_yolo_coordinates(infile):
    """ Finds the image centers, width and height of an image
    this is the format YOLOv3 uses for its bounding boxes
    INPUT: filepath
    OUTPUT: tuple of 4 ints: bounding box's: (x center, y center, width, height)
    """
    try: # If image is a png RGBA, this throws no error
        img = np.asarray(Image.open(infile))
        height, width, depth = img.shape
        if depth != 4:
            raise   # depth is likely 2 (grayscale, alpha)
                    # convert to RGBA to give depth 4

    except: # Convert to RGBA and continue
        img = np.asarray(Image.open(infile).convert('RGBA'))
        height, width, depth = img.shape

    y_top, y_bottom, x_left, x_right = find_pixel_edges(img)

    w = (width - x_left - x_right) / width      # width of bounding box
    h = (height - y_top - y_bottom) / height    # height of bounding box
    x = (1 - w / 2) - x_right / width           # x center of box (distance right from UL)
    y = (1 - h / 2) - y_bottom / height         # y center of box (distance down from UL)

    return x, y, w, h

