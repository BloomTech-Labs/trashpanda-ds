# Content


`view_boxes`
Contains scripts for double checking pipeline's output. Not terribly useful given the large amount of edits needing to be made


`manual_label_check.py`

Checks your images after manual labeling for:
- Unlabeled images
- Images with multiple bounding boxes
- Blank text files
- Mislabeled class categories in .txt files and changes them

Additionally, images which haven't been renamed to their md5sum, it will  prompt the user to opt-in to allow for the renaming

To use, edit hardcode, changing the variable `image\_dir` to the directory you want to check.

