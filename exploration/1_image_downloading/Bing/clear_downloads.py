#!/usr/bin/env python3
"""
Deletes all files/folders in the downloads folder for testing purposes
"""

import os
import shutil

for r, d, f in os.walk('downloads'):
    for file in f:
        os.unlink(os.path.join(r, file))
    for dir in d:
        shutil.rmtree(os.path.join(r, dir))

print('All files in the downloads folder deleted')