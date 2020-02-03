'''Python script to name images without .txt file and then rename these images
to hash and extension (md5sum)'''

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

# rename all files inside folder called images_to_rename
for fname in os.listdir('images_to_rename'):
    name, ext = os.path.splitext(fname)
    hash = hash_file(fname)
    dst = hash + ext
    # print(fname + " --> " + dst)
    os.rename(fname, dst)