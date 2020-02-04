# Data Pipeline

collection of directories with scripts numbered in order of preprocessing 


## Tenative ordering
1. `1_image\_downloading` - uses google image downloader to scrape images (currently defaults to those with transparent backgrounds)

2. `2_resizing` - reduce dimensionality of images to 1080p on longest axis if necessary

3. `3_renaming` - to be added - rename images to their md5sum. Improves unique naming and serves as a check for duplicates

4. `4_discern_images` - differentiates png files from jpeg. png files go directly to bounding box script whereas jpeg must have background removed

5. remove backgrounds (if applicable) - To be added - automate removing backgrounds from jpeg or other images with a foreground

6. `6_bounding_boxes` - Finds bounding boxes for images. Saves class labels and coordinates in .txt file 

7. `7_add_backgrounds` (if applicable) - Add backgrounds to downloaded png files that had transparent backgrounds.

