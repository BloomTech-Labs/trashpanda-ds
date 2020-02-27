'''Post pipeline script for manual renamed images 

Python script to rename all images and .txt files to hash + extension (md5sum)

All image files should have a correspondent .txt file at this point

Attention: Change images dir to the directory you want to rename '''


# importing libraries
import hashlib
import os
import imghdr


def file_as_bytes(file):
    '''read image file as bytes'''
    with file:
        return file.read()


def hash_file(fpath):
    '''create hash file'''
    return hashlib.md5(file_as_bytes(open(fpath, 'rb'))).hexdigest()


# get all the file_images locations from the images_to_rename folder
all_files = os.listdir('./images')
fpaths = [f'./images/{current_file}' for current_file in all_files]


processed_images = {}   # dict that correspond each file name to its new md5sum name
txt_files = []          # list of .txt files to process using dict above

for fname in fpaths: 
    # print (fname)  
    # separating the directory path (head) from the image file (tail)
    head, tail = os.path.split(fname)
    # separating the name of the image file from its extension
    name, ext = os.path.splitext(tail)
    print("processing... ", tail)
    if ext != '.txt':
        # getting md5sum for image file
        hash = hash_file(fname)
        # joining file hash with file extension
        if name != hash:
            new_name = hash + ext
            os.rename(fname, os.path.join(head, new_name))    # rename image file as hash + ext 
            processed_images.update( {name : hash} )
            # print (name)
            # print (hash)
    else:
        txt_files.append(fname)  # adding .txt file name


#if the folder has already been processed, dict should be empty, no need for txt_files to be processed (already processed)
if len(processed_images) > 0:
    for txt_name in txt_files:
        # print (txt_name)
        # separating the directory path (head) from the .txt file (tail)
        head, tail = os.path.split(txt_name)
        print("processing... ", tail)
        # separating the name of the file from its extension
        name, ext = os.path.splitext(tail)

        if name in processed_images.keys():
            new_txt_name = processed_images[name] + ext
            os.rename(txt_name, os.path.join(head, new_txt_name))    # rename .txt file as hash + .txt

print ('All files processed!')
