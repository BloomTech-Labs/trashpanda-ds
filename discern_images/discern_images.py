#!/usr/bin/env python3

import imghdr
import os

image_filepaths = []
for r, d, f in os.walk('images', topdown=False):
    for file in f:
        path = os.path.join(r, file)
        image_filepaths.append(path)

for path in image_filepaths:
    print(path)
    print(imghdr.what(path))
    print()

# To be expanded. We don't want to print the outputs as much as we want to add our bounding box .txt scripts
