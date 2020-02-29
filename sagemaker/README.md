# SageMaker Notes:


## Below is the step by step code, Alternatively, run two bash scripts, skip to TLDR
Following this guide:

https://github.com/AlexeyAB/darknet

1. Clone AlexyAB's version of Darknet (Keeps up to date compared to pjReddie's)

`git clone https://github.com/AlexeyAB/darknet.git`

2. download s3 bucket into sagemaker within darknet (takes about 10 minutes for 20 Gb)

`cd darknet; aws s3 sync s3://the-trash-panda dataset`

fudge with directory structure (at the time of writing, we've written our scripts to conform to this directory structure)

`mv dataset/images/* dataset/ && rmdir dataset/images`

3. Move relevant files in from the trashpanda-ds github

`cp /home/ec2-user/SageMaker/trashpanda-ds/sagemaker/{manual_label_check.py,train_test_split.sh, yolo-obj.cfg} .`

`cp /home/ec2-user/SageMaker/trashpanda-ds/sagemaker/{obj.data,obj.names,yolo-obj.cfg} darknet/data && cp darknet/data/obj.names classes.txt`

Create a 9:1 train test split

`train_test_split.sh`

4. Make changes to C code


Change lines in src/network.c  fuse\_conv\_batchnorm and src/classifier try\_classifier

`cd darknet; make`


5. Do some precheck on the s3 bucket content:

`python manual_label_check.py dataset` 

3. Download pretrained weights
- From Untrained model (starting from scratch):
	`wget https://pjreddie.com/media/files/darknet53.conv.74`




------------------------------------------------------
Running the model
------------------------------------------------------

`./darknet detector train data/obj.data yolo-obj.cfg darknet53.conv.74`



## TLDR - preferentially this:

`cd; cp /home/ec2-user/SageMaker/trashpanda-ds/sagemaker/{step1.sh,step2.sh} . && chmod +x step1.sh; ./step1.sh`

Then change the C code as per step 4 then execute

`cd; chmod +x step2.sh; ./step2.sh`
