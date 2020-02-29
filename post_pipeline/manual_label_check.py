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
import select
import sys

# Run on a specific image dir (if no arg specified, it defaults to `image`
try:
    image_dir = image_dir = sys.argv[1]
except:
    image_dir = 'images'

print(f"checking directory '{image_dir}'")
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
lonely_texts = set(texts_basenames) - set(images_basenames)
unlabeled_images = [li + extensions_dict[li] for li in lonely_images]
unlabeled_texts = [f"{li}.txt" for li in lonely_texts]


# Find text files with multiples lines
for file in os.listdir(image_dir):
    if file.endswith(".txt"):
        with open(os.path.join(image_dir, file)) as f:
            text = f.readlines()
            size = len(text)
        if size != 1:
            print(os.path.join(image_dir, file) + " has "+str(size)+ " lines")



#### helper functions for finding poorly named images ####
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
        print(f"IMAGE RENAME: {head} --> {hash_name}")
        try:
            os.rename(old_text_name, new_text_name)
            print(f"TEXT RENAME: {old_text_name} --> {new_text_name}")
        except:
            print(f"No text rename, file doesn't exist")
    else:
        os.remove(fpath)                      # remove the duplicates
    
    return os.path.join(head, hash_name), os.path.join(head, hash)
###################################################################




# Display images that are not properly named as an md5sum
# Prompt user to change name (both image and text file)

poorly_named_images = [image for image in images
        if not re.match('^[a-f0-9]{32}$',os.path.splitext(os.path.split(image)[1])[0])]


if poorly_named_images:
    print("\n\nPOOR NAMES:")
    print(poorly_named_images)
    resp = input("Change all names? <y/n>")
    if resp == 'y':
        for poor_image in poorly_named_images:
            rename_files(poor_image, images)
    else:
        print("unkown or negative response, keeping names")


#### Check for textfile mislabels ######
def update_classes(class_file, text_paths):
    # Add check to update classes. Check is skipped if no response is given in 10 seconds
    print(f"To check for updates in the {class_file} press enter...")
    i, o, e = select.select( [sys.stdin], [], [], 10 )
    if (i):

        classes_dict = {} # dictionary mapping items in classes.txt to line number
        with open(class_file,'r') as f:
            for i, line in enumerate(f):
                classes_dict.update({line.rstrip() : str(i)})

        # Check for changes in each line of each file
        file_changes = 0 # keep track of number of files changed
        line_changes = 0 # keep track of number of lines changed
        for text_path in text_paths:
            current_class = os.path.normpath(text_path).split(os.sep)[1]
            try:
                new_class_num = classes_dict[current_class]
            except KeyError: # Stops operation if a class has been deleted
                print(f"{'-'*50}\nclass '{current_class}' doesn't exist in '{class_file}'\n manually remove or delete it from images directory and try again")
                exit(1)

            with open(text_path,'r+') as t:
                # convert each line into a list
                # modify the number if necessary
                lines = [line for line in t]
                file_change_occurred = False
                for i, line in enumerate(lines):
                    if ',' in line: # corrects past error (early on) if applicable
                        line = line.replace(',', ' ')
                        file_change_occurred = True
                        line_changes += 1
                    if line.split(' ')[0] != new_class_num:
                        file_change_occurred = True
                        line_changes += 1
                        print(f"changing class label for '{text_path}' \
                            \nfrom {line.split(' ')[0]} to {new_class_num}")
                        lines[i] =  f"{new_class_num} {' '.join(line.split(' ')[1:])}"
                if file_change_occurred: 
                    file_changes += 1

                t.seek(0) # go to zeroth byte in file, fully overwrite, truncate
                t.write(''.join(lines))
                t.truncate()


        if changes > 0:
            print(f"i\nnumber of files changes made: {changes}")
        else: 
            print("\nno changes made to class labels")
    else:
        print("No response, skipping class update")

class_file = 'classes.txt'
update_classes(class_file, texts)
print("DONE")

########### Display last errors ##############
print('\n'+str(len(unlabeled_images))+" unlabeled images")
for ui in unlabeled_images:
    print(ui)

print('\n'+str(len(unlabeled_texts))+" text files without images")
for ut in unlabeled_texts:
    print(ut)

print('\n'+str(len(errors))+" errors(unrecognized as text or image file)")
for e in errors:
    print(e)

