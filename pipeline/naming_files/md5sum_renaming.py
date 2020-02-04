'''Python script to name images without .txt file and then rename these images
to hash and extension (md5sum)'''


# # rename all files inside folder called images_to_rename
# for fname in os.listdir('./images_to_rename'):
#     name, ext = os.path.splitext(fname)
#     hash = hash_file(fname)
#     dst = hash + ext
#     print(fname + " --> " + dst)
#     os.rename(fname, dst)

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


file_images = os.listdir('./images_to_rename')
fpaths = [f'./images_to_rename/{file_image}' for file_image in file_images]

dsts = []
for fname in fpaths:
    head, tail = os.path.split(fname)
    print(os.path.split(fname))
    name, ext = os.path.splitext(tail)
    print(os.path.splitext(tail))
    hash = hash_file(fname)
    print(hash_file(fname))
    dst = hash + ext
    if dst not in dsts:
        dsts.append(dst)
        print(tail + " --> " + dst)
        os.rename(fname, head + "/" + dst)
    else: 
        os.remove(fname)