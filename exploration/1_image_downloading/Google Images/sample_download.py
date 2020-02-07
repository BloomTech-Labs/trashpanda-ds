#!/usr/bin/env python3

from google_images_download import google_images_download   #importing the library

# class instantiation
response = google_images_download.googleimagesdownload()  

# creating list of arguments
external_file = "search_keys.txt" # External file where each row is the search keyword
                                  # used with "keywords_from _file"
arguments = {"keywords":"tires","limit":5,"print_urls":False}   

paths = response.download(arguments)  
print(paths)   
