#!/usr/bin/env python3
"""
Deletes all files/folders in the output folder for testing purposes
"""

import os
import shutil

for r, d, f in os.walk('output'):
    for file in f:
        os.unlink(os.path.join(r, file))
    for dir in d:
        shutil.rmtree(os.path.join(r, dir))

print('All files in the output folder deleted')