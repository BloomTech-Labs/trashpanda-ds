# Data Pipeline

Collection of directories with scripts numbered in order of preprocessing.

## Tentative ordering

1. `1_image_downloading` - uses google image downloader to scrape images (currently defaults to those with transparent backgrounds)

2. `2_renaming` - renames images to their md5sum. Improves unique naming and serves as a check for duplicates

3. `3_resizing` - reduce dimensionality of images to 1080p on longest axis if necessary.

4. `4_discern_images` - differentiates png files from jpeg. png files go directly to bounding box script whereas jpeg must have background removed via `5_forecut`.

5. `5_forecut` (if applicable) - automates removing backgrounds (foreground extraction) from jpeg or other images using [OpenCV](https://github.com/opencv/opencv) and [Detectron2](https://github.com/facebookresearch/detectron2).

6. `6_bounding_boxes` - Finds bounding boxes for images. Saves class labels and coordinates in .txt file.

7. `7_add_backgrounds` (if applicable) - Add backgrounds to downloaded png files that had transparent backgrounds.
