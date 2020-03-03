#!/bin/bash
cd darknet; make

python manual_label_check.py dataset

wget https://pjreddie.com/media/files/darknet53.conv.74

echo 'ready to run, from darknet folder, run: cd darknet && ./darknet detector train data/obj.data yolo-obj.cfg darknet53.conv.74'
