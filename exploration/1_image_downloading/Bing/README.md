# Binger - Bing Downloader

Downloads multiple images from Bing. Uses the Bulk Bing Image Downloader from
https://github.com/ostrolucky/Bulk-Bing-Image-downloader

## Arguments (edit in script)
* `items` - The list of items to grab images from
* `transparent` - True or False, if you want transparent backgrounds or not
* `limit` - The higher the number, the more images you'll get. The number you insert is the MAXIMUM amount of images you might get per item.

Images will output to the downloads foler in their respective folder names, spaces replaced with underscores.

Bing search terms/filters are randomized each time the script runs in hope that it downloads unique images each subsequent run.

We download the Bulk Bing Image Downloader in this script to prevent copy/pasting someone else's code in our repo.