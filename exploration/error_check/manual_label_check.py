#!/usr/bin/env python3
"""
Checks your images after manual labeling for:
- Unlabeled images
- Images with two bounding boxes
- Blank text files

Change image_dir to the directory you want to check
"""

import os
import hashlib
import imghdr
import re

image_dir = "temp_test"
image_dir = 'paint'
images = []
texts = []
errors = []
for r, d, f in os.walk(image_dir, topdown=False):
    for file in f:
        path = os.path.join(r, file)
        if imghdr.what(path) != None:
            images.append(path)
        elif path.endswith(".txt"):
            texts.append(path)
        else:
            errors.append(path)

#### Find unlabeled (i.e. new) images
images_basenames = [os.path.splitext(image)[0] for image in images]
images_extensions = [os.path.splitext(image)[1] for image in images]
extensions_dict = dict(zip(images_basenames, images_extensions))
texts_basenames = [os.path.splitext(text)[0] for text in texts]
lonely_images = set(images_basenames) - set(texts_basenames)
unlabeled_images = [li + extensions_dict[li] for li in lonely_images]


print(str(len(unlabeled_images))+" unlabeled images")
for i in range(len(unlabeled_images)):
    print(unlabeled_images[i])

print()
# Find Files with multiples lines
for file in os.listdir(image_dir):
    if file.endswith(".txt"):
        with open(os.path.join(image_dir, file)) as f:
            text = f.readlines()
            size = len(text)
        if size != 1:
            print(os.path.join(image_dir, file) + " has "+str(size)+ " lines")



#### find poorly named images ####
def file_as_bytes(file):
    '''read image file as bytes'''
    with file:
        return file.read()


def hash_file(fpath):
    '''create hash file'''
    return hashlib.md5(file_as_bytes(open(fpath, 'rb'))).hexdigest()


def rename_files(fpath, unique_images):
    # separating the directory path (head) from the file (tail)
    head, tail = os.path.split(fpath)
    # separating the name of the file from its extension
    name, ext = os.path.splitext(tail)
    # find correct file extension
    ext = '.' + imghdr.what(fpath)
    # getting md5sum for image file
    hash = hash_file(fpath)
    # joining file hash with file extension
    hash_name = hash + ext
    # get old and new text names
    old_text_name = f'{os.path.join(head,name)}.txt'
    new_text_name = f'{os.path.join(head,hash)}.txt'
    #checking for duplicate files
    if hash_name not in unique_images:
        unique_images.append(hash_name)
        # rename file as file hash + ext
        os.rename(fpath, os.path.join(head, hash_name))
        #print(os.path.join(head, hash_name))
        print(f"IMAGE RENAME: {head} --> {hash_name}")
        try:
            os.rename(old_text_name, new_text_name)
            print(f"TEXT RENAME: {old_text_name} --> {new_text_name}")
        except:
            print(f"No text rename, file doesn't exist")
    else:
        os.remove(fpath)                      # remove the duplicates
    
    return os.path.join(head, hash_name), os.path.join(head, hash)




poorly_named_images = [image for image in images
        if not re.match('^[a-f0-9]{32}$',os.path.splitext(os.path.split(image)[1])[0])]



if poorly_named_images:
    print("\n\nPOOR NAMES:")
    print(poorly_named_images)
    resp = input("Change all names? <y/n>")
    if resp == 'y':
        for poor_image in poorly_named_images:
            #new_image_name, new_text_name = 
            rename_files(poor_image, images)
    else:
        print("unkown or negative response, keeping names")

