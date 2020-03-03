#!/usr/bin/env python3

import cv2
import numpy as np
import os
from PIL import Image, ImageDraw
import time
from yolo_label_tools import count_from_top, find_pixel_edges, find_yolo_coordinates

class_labels = []
with open('classes.txt') as f:
    for line in f:
        class_labels.append(line.strip('\n'))


dirs = []
png_filepaths = []
for r, d, f in os.walk('images', topdown=False):
    for directory in d:
        dirs.append(directory)
    for file in f:
        if file.endswith('.png'):
            path = os.path.join(r, file)
            png_filepaths.append(path)

dirs = sorted(dirs)


for png_path in png_filepaths:
    print(png_path)
    class_label = png_path.split('/')[-2] 
    class_label_number = str(class_labels.index(class_label)) # yolo counts from 0
    coordinates = find_yolo_coordinates(png_path)
    coordinates = [str(coordinate) for coordinate in coordinates]
    line = ','.join([class_label_number] +  coordinates)
    print(line)
    print()
    file_stem = png_path[:-4]
    with open(f'{file_stem}.txt','w') as f:
        f.write(line)
