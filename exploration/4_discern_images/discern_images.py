#!/usr/bin/env python3

import imghdr
import os
from PIL import Image


# Gather images (for the sake of demo)
image_filepaths = []
for r, d, f in os.walk('images', topdown=False):
    for file in f:
        path = os.path.join(r, file)
        image_filepaths.append(path)



def discern_images(image_filepaths):
    transparent = []
    opaque = []
    for path in image_filepaths:
        img = Image.open(path)
        if img.mode == 'RGBA' or 'transparency' in img.info:
            transparent.append(path)
        else:
            opaque.append(path)
    return transparent, opaque

transparent, opaque = discern_images(image_filepaths)


print('transparent images:')
for t in transparent:
    print(t)

print('\nopaque images:')
for o in opaque:
    print(o)
# To be expanded. We don't want to print the outputs as much as we want to add our bounding box .txt scripts
