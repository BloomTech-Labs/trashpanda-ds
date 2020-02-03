#!/usr/bin/env python3

import os

dirs = []
for r, d, f in os.walk('images', topdown=False):
    for directory in d:
        dirs.append(directory)

dirs = sorted(dirs)
print("The following classes now exist in the file 'classes.txt':")
print(dirs)

with open('classes.txt','w') as outfile:
    for clas in dirs:
        outfile.write(f'{clas}\n')
