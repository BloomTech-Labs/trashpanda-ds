'''
Downloads multiple images from Bing. Uses the Bulk Bing Image Downloader from
https://github.com/ostrolucky/Bulk-Bing-Image-downloader

Arguments
items - The list of items to grab images from
transparent - True or False, if you want transparent backgrounds or not
limit - The higher the number, the more images you'll get. The number you insert is the MAXIMUM amount of images you might get per item.

Images will output to the downloads foler in their respective folder names, spaces replaced with underscores.

Bing search terms/filters are randomized each time the script runs in hope that it downloads unique images each subsequent run.

We download the Bulk Bing Image Downloader in this script to prevent copy/pasting someone else's code in our repo.
'''

import os
import sys
import urllib.request
from random import choice

'''
Items include:
'aerosol_cans_full', 'aluminium_foil', 'ammunition', 'auto_parts', 'batteries', 'bicycles', 'cables', 'cardboard', 'cartridge', 'cassette', 'cd_cases', 'cigarettes', 'cooking_oil', 'cookware', 'corks', 'crayons', 'digital_cameras', 'desktop_computers', 'discs', 'doors', 'eyeglasses', 'fabrics', 'fire_extinguishers', 'floppy_disks', 'furniture', 'game_consoles', 'generic_plastic', 'gift_bags', 'glass', 'glass_container', 'green_waste', 'hard_drives', 'hardware', 'hazardous_fluid', 'heaters', 'laptop_computers', 'large_appliance', 'lightbulb', 'medication_containers', 'medications', 'metal_cans', 'mixed_paper', 'mobile_device', 'monitors', 'nail_polish', 'oil_filters', 'paint', 'paint_thinner', 'pallets', 'paper_cups', 'pet_waste', 'plastic_cards', 'printers', 'propane_tanks', 'shoes', 'small_appliances', 'smoke_detectors', 'tires', 'tools', 'toothbrushes', 'toothpaste_tubes', 'toy', 'vehicles', 'water_filters', 'wood', 'wrapper'
'''
items = ['glass_container', 'paper_cups', 'shoes']
transparent = False
limit = 10

# Download the Bulk Bing Image Downloader if it doesn't exist in the system
if os.path.exists('./bbid.py'):
    pass
else:
    print('bbid.py not found. Downloading...')
    url = 'https://raw.githubusercontent.com/ostrolucky/Bulk-Bing-Image-downloader/6ab4c76b3f3c6bd9636ab547364765330eb48ad2/bbid.py'
    urllib.request.urlretrieve(url, './bbid.py')

# Create an array of all the item names (spaces instead of underscores)
itemNames = [item.replace("_", " ") for item in items]

# Create an array of all the item folder names (underscores instead of spaces)
itemFolderNames = [item.replace(" ", "_") for item in items]

# Create the folder names in the downloads folder
for itemFolderName in itemFolderNames:
    if not os.path.exists('./downloads/'+itemFolderName):
        os.makedirs('./downloads/'+itemFolderName)

# Initialize randomizer variables
randomSearchAppend = ['', '', '', '', 'image of ', 'picture of ', 'photo of ', 'photograph of ', 'snapshot of ', ' image', ' picture', ' photo', ' photograph', ' snapshot']
randomFilterAppend = ['', '', '', '+filterui:age-lt525600', '+filterui:license-L2_L3', '+filterui:aspect-square', '+filterui:aspect-wide', '+filterui:aspect-tall', '+filterui:imagesize-medium', '+filterui:imagesize-wallpaper']

# For all the items
for x in range(0, len(items)):
    randomizedFilter = '+filterui:photo-photo'
    randomizedSearch = ''

    # Select random search terms/fiilters
    randomSearchSeed = choice(randomSearchAppend)
    randomFilterSeed = choice(randomFilterAppend)

    # If the search append if a prefix, add it before the item name
    if 'of' in randomSearchSeed:
        randomizedSearch = randomSearchSeed + itemNames[x]
    # If the search append if a suffix, add it after the item name
    else:
        randomizedSearch = itemNames[x] + randomSearchSeed

    # Append the random filter to the filter list
    randomizedFilter += randomFilterSeed
    # Add the transparent filter if set
    if transparent:
        randomizedFilter += '+filterui:photo-transparent'

    # Run bbid.py, passing in appropriate arguments
    sys.argv = [
        "bbid.py",
        "-s",
        randomizedSearch,
        "-o",
        "downloads/"+itemFolderNames[x],
        "--limit",
        str(limit),
        "--filters",
        randomizedFilter
    ]
    exec(open("bbid.py").read())