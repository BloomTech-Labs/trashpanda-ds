'''Python script to rename images to respective hash and extension (md5sum)'''


# importing libraries
import hashlib
import os


def file_as_bytes(file):
    '''read image file as bytes'''
    with file:
        return file.read()


def hash_file(fpath):
    '''create hash file'''
    return hashlib.md5(file_as_bytes(open(fpath, 'rb'))).hexdigest()


# get all the file_images locations from the images_to_rename folder
file_images = os.listdir('./images_to_rename')
fpaths = [f'./images_to_rename/{file_image}' for file_image in file_images]


dsts = []   # empty list
for fname in fpaths:   
    # separating the directory path (head) from the file (tail)
    head, tail = os.path.split(fname)
    # separating the name of the file from its extension
    name, ext = os.path.splitext(tail)
    # getting md5sum for image file
    hash = hash_file(fname)
    # joining file hash with file extension
    dst = hash + ext
    #checking for duplicate files
    if dst not in dsts:
        dsts.append(dst)
        # print(tail + " --> " + dst)
        os.rename(fname, head + "/" + dst)    # rename file as file hash + ext 
    else: 
        os.remove(fname)                      # remove the duplicates
