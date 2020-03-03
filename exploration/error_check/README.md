# Error Checking

`error_check.py`

Checks for the presence of image files without corresponding text files and vice versa, as well as any other "random" filetypes present.

Can be implemented after new image files are downloaded (after resizing if applicable, but before re-naming or messing with the heavier background-editing scripts) 



`trevor_transform.sh`

A shell script used to correct an error in a previous iteration (where yolo coordinates were mistakenly comma separated instead of space separated). This shell script works on Linux and Mac on a folder called 'images' and changes all commas to spaces in .txt files. Included here for historical purposes.


`manual_label_check.py`

Checks your images after manual labeling for:
- Unlabeled images
- Images with multiple bounding boxes
- Blank text files
- Mislabeled class categories in .txt files and changes them

Additionally, images which haven't been renamed to their md5sum, it will prompt the user to opt-in to allow for the renaming

To use, edit hardcode, changing the variable `image_dir` to the directory you want to check.


`multifile_label.py`

Portion of the pipeline that adds bounding boxes and makes yolo textfile labels. This file only considers the png images at this point.

