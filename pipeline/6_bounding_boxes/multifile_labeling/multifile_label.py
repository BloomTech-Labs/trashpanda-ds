#!/usr/bin/env python3

import cv2
import numpy as np
import os
from PIL import Image, ImageDraw
import time
from yolo_label_tools import count_from_top, find_pixel_edges, find_yolo_coordinates

image_dir = 'downloads'

class_labels = []
with open('classes.txt') as f:
    for line in f:
        class_labels.append(line.strip('\n'))


dirs = []
png_filepaths = []
for r, d, f in os.walk(image_dir, topdown=False):
    for directory in d:
        dirs.append(directory)
    for file in f:
        if file.endswith('png'):
            path = os.path.join(r, file)
            png_filepaths.append(path)

dirs = sorted(dirs)


for png_path in png_filepaths:
    print(png_path)
    class_label = png_path.split('/')[-2] 
    class_label_number = str(class_labels.index(class_label) + 1) # yolo counts from 1
    coordinates = find_yolo_coordinates(png_path)
    if coordinates == None: # image is empty and ALL transparent
        print('blank image found:',png_path)
        os.remove(png_path)
        continue
    coordinates = [str(coordinate) for coordinate in coordinates]
    line = ','.join([class_label_number] +  coordinates)
    print(line)
    print()
    file_stem = png_path[:-4]
    with open(f'{file_stem}.txt','w') as f:
        f.write(line)
