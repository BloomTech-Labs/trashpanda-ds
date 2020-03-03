# SageMaker Notes:


## Below is the step by step code, Alternatively, run the bash scripts as provided in the TLDR section
Following this guide:

https://github.com/AlexeyAB/darknet

1. Clone AlexyAB's version of Darknet (Keeps up to date compared to pjReddie's)

`git clone https://github.com/AlexeyAB/darknet.git`

2. download S3 bucket into sagemaker within darknet (this can take a little while as our dataset is now 15GB)

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

The following errors occur if you run `make`:
```c
/src/network.c: In function ‘fuse_conv_batchnorm’:
./src/network.c:1123:17: error: ‘for’ loop initial declarations are only allowed in C99 mode
                 for (int i = 0; i < l->nweights; ++i) printf(" w = %f,", l->weights[i]);
```

```c
./src/classifier.c: In function ‘try_classifier’:
./src/classifier.c:756:9: error: ‘for’ loop initial declarations are only allowed in C99 mode
         for(int i = 0; i < l.c; ++i){
```
in each you need to move the `int i` out of the for loop
eg:
```c
for(int i = 0; i < l.c; ++i){
```
becomes
```c
int i;
for(i = 0; i < l.c; ++i){
```

a few lines lower, twice in the same file in the try\_classifier function, change `int i = 0` to `i = 0`, no need to redeclare `int i` outside of the for loop, it has already been declared.

Once those changes occur (4 in total), `make` should run without error

Set GPU=1 and CUDNN=1 to speedup on GPU

Set CUDNN_HALF=1 to further speedup 3 x times (Mixed-precision on Tensor Cores) GPU: Volta, Xavier, Turing and higher

Set AVX=1 and OPENMP=1 to speedup on CPU (if error occurs then set AVX=0)


`cd darknet; make`


5. Do some precheck on the s3 bucket content:

`python manual_label_check.py dataset` 

3. Download pretrained weights
- From Untrained model (starting from scratch):
	`wget https://pjreddie.com/media/files/darknet53.conv.74`


NOTE: if you use transfer learning and continue training our pretrained model, you can now download the last weights from the S3 bucket saved-weights (file: yolo-obj_last.weights) and use them running the model, instead of `darknet53.conv.74`. 

------------------------------------------------------
Running the model
------------------------------------------------------

`./darknet detector train data/obj.data yolo-obj.cfg darknet53.conv.74`



## TLDR - preferentially this:

`cd; cp /home/ec2-user/SageMaker/trashpanda-ds/sagemaker/{step1.sh,step2.sh} . && chmod +x step1.sh; ./step1.sh`

Then change the C code as per step 4. 

`cd; chmod +x step2.sh; ./step2.sh`
