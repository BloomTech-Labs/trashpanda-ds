# The Pipeline

## Instructions

TLDR: Run `make_images_folder.py`, clone and build detectron2, then execute `pipeline.py`.

### Test images

Sample images are provided in `downloads`, this can serve as a backup (of original, untouched images). For testing, `make_images_folder.py` will copy the downloads folder to a directory called `images`. A directory called `pipeline` exists that's unrelated to this data pipeline, it's built in to the architecture of the detectron2 library we're using.

### Background removal

Automated image background removal is done via an implementation of Facebook AI Research's [Detectron2](https://github.com/facebookresearch/detectron2). As the model is not formally serialized, it must be built from source every time this pipeline is set up on a new machine or in a new environment.

To build Detectron2 from source and install it into the working environment, follow the [installation instructions](https://github.com/facebookresearch/detectron2/blob/master/INSTALL.md).

## Pipeline in summary:

`images` is searched for the existance of new, unlabeled data,

Those images are resized, renamed (to their md5sum hash) and yolo labels are found

Any transparent images are now appended to backgrounds

images with opaque backgrounds: their backgrounds are removed and placed in an `output` directory as png files (blanks images if suggested by the model are removed). Yolo labels are found for these and paired with their original jpeg counterparts under `images`.

Despite some cleaning up and refactoring, this is a working pipeline to process and label images from start to finish

[x] TODO: add the yolo labeling back in

[ ] TODO: modularize/ refactor the pipeline

## Detectron2

Credit is given where credit is due. Removing backgrounds is done via an implementation of Facebook AI Research's very own [Detectron2](https://github.com/facebookresearch/detectron2). The configuration and pseudo-deployment of Detectron2 was heavily inspired by jagin's [detectron2-pipeline](https://github.com/jagin/detectron2-pipeline).
