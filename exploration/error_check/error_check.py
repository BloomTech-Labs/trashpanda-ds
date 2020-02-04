#!/usr/bin/env python3

import imghdr
import os
from PIL import Image

def error_check():
    """checks for the presence of unpaired images and text files
    (i.e. if no yolo boxes have been made)
    Currently only checks for presence of png and jpg files
    """
    image_types = ['png','jpeg']

    images = []
    texts = []
    others = []
    for r, d, f in os.walk('images', topdown=False):
        for file in f:
            path = os.path.join(r, file)
            if imghdr.what(path) in image_types:
                images.append(path)
            elif path.endswith('.txt'):
                texts.append(path)
            else:
                others.append(path)
    
    if others:
        print("non-conforming files:",others)
        print(f"{len(others)} in total")
        resp = ''
        while resp not in ['y','n']:
            resp = input ("Try and convert to jpeg? <y/n>")
            if resp == 'n':
                pass
            elif resp == 'y':
                for other in others:
                    convert_to_jpg(other)
    
    images = sorted(images)
    texts = sorted(texts)

    lonely_images = set(images) - set(texts)
    lonely_texts = set(texts) - set(images)
    if lonely_images:
        print(f"These images don't have text files:\n{lonely_images}\n")
    if lonely_texts:
        print(f"These text files don't belong to any images:\n{lonely_texts}\n")



def convert_to_jpg(other):
    """input: file path to image
    output: file path to new jpeg image"""
    extension = imghdr.what(other)
    if extension == None:
        print("Not an image file:{other}\nmanual handling required")
        return # Skip the rest if not an image file

    im = Image.open(file)
    im.save(file.replace(extension,'jpg'))
    os.remove(other)
    print(f'{other} removed, replaced by jpeg')


error_check()
