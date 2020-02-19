# Error Checking

`error_check.py`

Checks for the presence of image files without corresponding text files and vice versa, as well as any other "random" filetypes present.

Can be implemented after new image files are downloaded (after resizing if applicable, but before re-naming or messing with the heavier background-editing scripts) 



`trevor_transform.sh`

A shell script used to correct an error in a previous iteration (where yolo coordinates were mistakenly comma separated instead of space separated). This shell script works on Linux and Mac on a folder called 'images' and changes all commas to spaces in .txt files. Included here for historical purposes I guess
