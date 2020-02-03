#!/usr/bin/env python3
"""
Deletes all files in the output folder for testing purposes
"""
import os

images = os.listdir('output')
paths = [f'./output/{image}' for image in images  if image != '.DS_Store']
for path in paths:
    os.remove(path)

