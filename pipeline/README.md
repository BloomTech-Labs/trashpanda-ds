# The Pipeline

## Instructions

TLDR: Run `make_images_folder.py`, install dependencies listed in project root's Pipfile, then execute `pipeline.py`.

Note: when `pipeline.py` is run for the first time on a new machine, the COCO-trained weights used in the Mask R-CNN background removal will automatically download. This `.h5` file is around 250mb, so may take a little while to download, depending on your internet speed.

### Test images

Sample images are provided in `downloads`, this can serve as a backup (of original, untouched images). For testing, `make_images_folder.py` will copy the downloads folder to a directory called `images`. A directory called `pipeline` exists that's unrelated to this data pipeline, it's built in to the architecture of the detectron2 library we're using.

### Background removal

Automated image background removal is done via a Keras and Tensorflow implementation of [Mask R-CNN](https://github.com/matterport/Mask_RCNN/).

## Pipeline in summary:

`images` is searched for the existance of new, unlabeled data,

Those images are resized, renamed (to their md5sum hash) and yolo labels are found

Any transparent images are now appended to backgrounds

images with opaque backgrounds: their backgrounds are removed and placed in an `output` directory as png files (blanks images if suggested by the model are removed). Yolo labels are found for these and paired with their original jpeg counterparts under `images`.

Despite some cleaning up and refactoring, this is a working pipeline to process and label images from start to finish

[x] TODO: add the yolo labeling back in

[ ] TODO: modularize/ refactor the pipeline


## Detectron2

Credit is given where credit is due. Removing backgrounds is done via Matterport's implementation of [Mask R-CNN](https://github.com/matterport/Mask_RCNN/). The configuration of the Mask R-CNN pipeline was heavily inspired by jagin's [detectron2-pipeline](https://github.com/jagin/detectron2-pipeline).
