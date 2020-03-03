# The Pipeline

## Instructions

Place images to process in the `images` directory, install dependencies listed in project root's Pipfile, then execute `pipeline.py`.

If you encounter any problems installing the pipeline, take a look at the **Pipeline Install Troubleshooting** section below.

Note: when `pipeline.py` is run for the first time on a new machine, the COCO-trained weights used in the Mask R-CNN background removal will automatically download. This `.h5` file is around 250mb, so may take a little while to download, depending on your internet speed.

### Test images

Sample images are provided in `downloads`, this can serve as a backup (of original, untouched images). For testing, `make_images_folder.py` will copy the downloads folder to a directory called `images`. A directory called `pipeline` exists that's unrelated to this data pipeline, it's built in to the architecture of the Mask R-CNN library we're using.

### Background removal

Automated image background removal is done via a Keras and Tensorflow implementation of [Mask R-CNN](https://github.com/matterport/Mask_RCNN/).

## Pipeline in summary:

`images` is searched for the existance of new, unlabeled data.

Those images are resized, renamed (to their md5sum hash) and yolo labels are found.

Any transparent images are now appended to backgrounds.

images with opaque backgrounds: their backgrounds are removed and placed in an `output` directory as png files (blanks images if suggested by the model are removed). Yolo labels are found for these and paired with their original jpeg counterparts under `images`.

Despite some cleaning up and refactoring, this is a working pipeline to process and label images from start to finish.

[x] TODO: add the yolo labeling back in

[x] TODO: modularize/ refactor the pipeline


## Mask R-CNN

Credit is given where credit is due. Removing backgrounds is done via Matterport's implementation of [Mask R-CNN](https://github.com/matterport/Mask_RCNN/). The configuration of the Mask R-CNN pipeline was heavily inspired by jagin's [detectron2-pipeline](https://github.com/jagin/detectron2-pipeline).

## Pipeline Install Troubleshooting

### The pipeline may not work properly on Windows.
We strongly recommended Windows users to install Windows Subsystem for Linux (WSL) to get access to Linux terminal programs.

To install WSL:

1. Download Ubuntu 18.04 or Debian GNU/Linux [here](https://docs.microsoft.com/en-us/windows/wsl/install-manual). If you're not sure, pick Ubuntu 18.04. Debian GNU/Linux is lighter but contains older packages.

2. In Windows PowerShell (with admin privileges), `cd` to the directory the Linux appx file downloaded to, then run `Add-AppxPackage distro_name.appx`

3. In Control Panel, go to Programs -> Turn Windows features on or off

4. In the window that appears, check `Windows Subsystem for Linux`, then restart your computer.

5. Once rebooted, open your Linux distro from the Start menu.

6. You'll see WSL terminal (bash). Enter your root username/password.

7. Run `sudo apt update` and `sudo apt upgrade`, which will get your WSL up to date.

8. Download [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (Linux 64-bit).

9. In bash, `cd` to the directory the Miniconda installer downloaded to. To get to the Downloads folder, the directory is `/mnt/c/users/(your username)/Downloads`

10. Run `bash Miniconda3-latest-linux-x86_64.sh`. Press and hold the enter key until you see the yes or no to agree to license terms, in which you type `yes`. Use the default installation path. Type `yes` when asked to initialize conda.

11. Open a new bash window to get access to Conda base.

To use WSL in VSCode, open the integrated terminal, and in the dropdown menu, select `Change default shell` and then select `WSL`.

### When running pipenv install, you get TypeError: write() takes exactly one argument (3 given)

If you're using WSL on Windows 10 1903 or newer, [uncheck all Python app execution aliases](https://superuser.com/questions/1437590/typing-python-on-windows-10-version-1903-command-prompt-opens-microsoft-stor). Somehow, those pesky aliases mess up pipenv, even though WSL is supposed to be isolated from Windows.

### Errors with cv2 or pycocotools

Ensure the following dependencies are installed directly on your Linux environment:

* gcc
* g++
* libglib2.0-0
* libsm6
* libxext6
* libxrender1

The above package names apply to Ubuntu-based systems. Fedora/Arch users will need to search for corresponding names.

In pip, make sure these dependencies are installed:

* cython
* numpy

In conda, make sure these dependencies are installed:

* gcc_linux-64 (if on Linux or WSL)
* setuptools

Don't delete `Pipfile.lock`, and before running `pipenv install` after a failure, reset the trashpanda pipenv with `pipenv --rm` first.

## Running the Pipeline with GPU

By default, the pipeline uses the CPU to remove backgrounds from nontransparent images. If you have a GPU and are running Linux, you should enable your GPU to greatly improve processing speeds.

1. In `/pipeline/Mask_RCNN/forecut_pipeline/utils/maskr.py`, replace the line:
```
DEVICE = "/cpu:0"
```
with
```
DEVICE = "/gpu:0"
```

2. Comment the line
```
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
```

3. Uncomment the lines
```
# with tf.device(DEVICE):
#     # Create model object in inference mode.
#     model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
```
### Nvidia GPU

4. Ensure you're using the Nvidia proprietary drivers (not Nouveau).

5. Pip install `tensorflow-gpu`

6. The pipeline should now use your GPU.

### AMD GPU

4. Pip install `tensorflow-rocm`

5. Install ROCm as per [these instructions](https://github.com/RadeonOpenCompute/ROCm). Using Ubuntu is highly recommended.

6. The pipeline should now use your GPU.