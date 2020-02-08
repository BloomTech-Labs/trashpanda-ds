#!/usr/bin/env python3
"""
Copies all contents of the downloads folder to a new folder named images.
Will overwrite the images folder if it exists and will ask the user if
they're ok with that, if necessary,
"""

import sys
import os
import shutil
from distutils.dir_util import copy_tree

if os.path.exists('images') and len(os.listdir('images')) > 0:
    images_input = input("""\nFiles detected in the images folder.
Are you sure you want to overwrite the images folder? (y/n) """).upper()
    if images_input != "Y":
        print("Closing script...")
        sys.exit()
    else:
        for r, d, f in os.walk('images'):
            for file in f:
                os.unlink(os.path.join(r, file))
            for dir in d:
                shutil.rmtree(os.path.join(r, dir))
elif not os.path.exists('images'):
    os.makedirs('images')

copy_tree('downloads', 'images')
print("Copied contents of downloads folder to images folder")