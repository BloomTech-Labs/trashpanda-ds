#!/usr/bin/env python3

from google_images_download import google_images_download   #importing the library

# class instantiation
response = google_images_download.googleimagesdownload()  

# creating list of arguments
arguments = {"keywords":"tire","limit":1,"print_urls":False,"color_type":"transparent"}   

paths = response.download(arguments)  
print(paths)   
