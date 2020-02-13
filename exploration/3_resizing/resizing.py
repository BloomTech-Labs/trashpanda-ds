'''Python Script to check image size and resize if any or both of the dimensions is bigger than 1080.
 This job will replace the old image by the new resized image'''

# importing libraries
import os
from PIL import Image

def image_resize(image_file):
  ''' Check image width and height. If width or/and height are bigger than 
  1080 pixels, image is resized. Biggest dimension will be 1080 pixels and 
  the other dimension is altered not affecting the aspect ratio'''

  img=Image.open(image_file)
  # img.size is a tuple (width,height)
  img_width = img.size[0]
  img_height = img.size[1]

  maxwidth = 1080    # desired max width
  maxheight = 1080   # desired max height

  # width is bigger than maxwidth and it is the biggest dimension on the image or it is a square image
  if img_width > maxwidth and img_width >= img_height:
    wratio = (maxwidth/float(img_width))
    hsize = int((float(img_height))*(float(wratio)))
    img = img.resize((maxwidth,hsize), Image.ANTIALIAS)
    img.save(image_file)

  # height is bigger than maxheight and it is the biggest dimension on the image
  elif img_height > maxheight and img_height > img_width:
    hratio = (maxheight/float(img_height))
    wsize = int((float(img_width))*(float(hratio)))
    img = img.resize((wsize,maxheight), Image.ANTIALIAS)
    img.save(image_file)

# get all the input images in the folder named input
InputImages = os.listdir('input')
InputPaths = [f'./input/{InputImage}' for InputImage in InputImages]

# apply function image_resize to all the images inside the input folder 
for InputPath in InputPaths:
  image_resize(InputPath) 
