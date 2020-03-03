# Discerning images

Used to discern file types. A sample directory of labeled images is provided

Where this fits into the data pipeline:

- images are resized and renamed

- *THIS* script will discern transparent images from opaque ones which will feed into...

- labeling bounding boxes (currently works with png, will work with jpeg with removing backgrounds)
