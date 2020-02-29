#!/bin/bash
git clone https://github.com/AlexeyAB/darknet.git

cd darknet; aws s3 sync s3://the-trash-panda dataset

mv dataset/images/* dataset/ && rmdir dataset/images

cp /home/ec2-user/SageMaker/trashpanda-ds/sagemaker/{manual_label_check.py,train_test_split.sh,yolo-obj.cfg} .

cp /home/ec2-user/SageMaker/trashpanda-ds/sagemaker/{obj.data,obj.names,yolo-obj.cfg} data && cp data/obj.names classes.txt

chmod +x train_test_split.sh && ./train_test_split.sh

echo 'Make Changes to C code (can run make command to see errors)'

