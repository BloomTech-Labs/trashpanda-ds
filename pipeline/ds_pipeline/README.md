# The Pipeline

NOTE: sample images are provided in `downloads`, this can serve as a backup (of original, untouched images). For testing, it's advised to make a copy of this directory called `images`.


execute `pipeline.py`


## Pipeline in summary:

`images` is searched for the existance of new, unlabeled data,

Those images are resized, renamed (to their md5sum hash) and yolo labels are found

Any transparent images are now appended to backgrounds

images with opaque backgrounds: their backgrounds are removed and placed in an `output` directory. Right now, adding the bounding boxes to those isn't implemented, but commented out code in the bottom of the script suggests a way of doing this

[ ] TODO: add the yolo labeling back in

[ ] TODO: modularize/ refactor the pipeline
