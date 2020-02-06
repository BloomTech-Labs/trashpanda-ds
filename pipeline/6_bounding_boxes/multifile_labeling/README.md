# multifile labeling

scenario: A directory `images` contains subdirectories with labels corresponding to the image clusters (eg. `batteries` contains images for alkaline batteries, car batteries, etc.)

The script `multifile_label.py` descends into them, finds bounding boxes, and saves that into the appropriate .txt file (e.g. photo1.png, coordinates are saved as photo1.txt)

## multifile\_labeling.py

 descends into the `images` directory, finds bounding boxes for each image, and saves that into the appropriate .txt file (e.g. photo1.png, coordinates are saved as photo1.txt)


## update\_classes.py

descends into the `images` directory and finds all unique directories, creates a "classes.txt" based on the directories present. This "classes.txt" file is used in conjunction with the `multifile_labeling.py`

## yolo\_label\_tools.py

Supporting functions for `multifile_labeling.py`



## TODO:
- Make `update_classes.py` only descend to the first directory in case sub categories are added. We don't want for example to have both "batteries" and "lithium ion batteries" listed in the "classes.txt" file

- Add functionality to `update_classes.py` to change the first column of each .txt file to update the number if new classes are added without needing to redo the calculations with bounding box. VERY IMPORTANT because some things are going to have to be added manually and we can't rely on the .png/transparent background trick

[x] Add functionality to preview bounding boxes. Maybe multithreading to "listen" to the user for sending flags when displaying. This can be entirely separate from the `multifile_labeling.py`. which can be run much like `find_borders.py` in `bounding-boxes` directory. NOTE: Created currently existing in ../post\_pipeline
