# Downloading Images

This hosts the google-images-download python program detailed from [here](https://github.com/hardikvasa/google-images-download)

## Current State

currently a `sample_download.py` exists which will return a single image of a tire with a transparent background (see hardcoded arguments therein). This is saved to the `downloads` directory in another subdirectory named "tire"

## Future TODO's

[x] Compile a sure list of items needed for downlad

[ ] Once a list of desired images are compiled, this list needs only to be added to the argument. This can be achieved with creating an external file, eg. `search_keys.txt` where each line is the search query. In the arguments of `sample_download.py` we swap `"keywords":"batteries"` for `"keywords_from_file":"search_keys.txt"`
