import os
from tqdm import tqdm
import multiprocessing as mp

from pipeline.capture_images import CaptureImages
from pipeline.capture_image import CaptureImage
from pipeline.predict import Predict
from pipeline.async_predict import AsyncPredict
from pipeline.separate_background import SeparateBackground
from pipeline.annotate_image import AnnotateImage
from pipeline.save_image import SaveImage
from pipeline.utils import detectron


def process_images(
    input_path,
    output_path="output",
    config_file="configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml",
    weights_file=None,
    config_opts=[],
    confidence_threshold=0.5,
    gpus=1,
    cpus=0,
    single_process=True,
    queue_size=3,
    separate_background=True,
    progress=True,
):
    """
    :: Detectron2 image processing pipeline ::
    Functionized version of `process_images.py` command line utility.
    
    Parameters
    ----------
    input_path : str / path
        Path to input image file or directory.
    output_path : str / path, optional
        Path to output directory, default "output"
    config_file : str / path, optional
        Path to Detectron2 config file, default "configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
    weights_file : str / path, optional
        Path to custom Detectron2 weights file, default None
    config_opts : list, optional
        Modify model config options, default []
    confidence_threshold : float, optional
        Minimum score for instance predictions to be shown, by default 0.5
    gpus : int, optional
        Number of GPUs, default 1
    cpus : int, optional
        Number of CPUs, default 0
    single_process : bool, optional
        force the pipeline to run in a single process, default True
    queue_size : int, optional
        Queue size per process, default 3
    separate_background : bool, optional
        Make background transparent, default True
    progress : bool, optional
        Display progress, by default True
    """

    # Create output directory if needed
    os.makedirs(output_path, exist_ok=True)

    # Create pipeline steps
    capture_images = (
        CaptureImages(input_path)
        if os.path.isdir(input_path)
        else CaptureImage(input_path)
    )

    cfg = detectron.setup_cfg(
        config_file=config_file,
        weights_file=weights_file,
        config_opts=config_opts,
        confidence_threshold=confidence_threshold,
        cpu=False if gpus > 0 else True,
    )
    if not single_process:
        mp.set_start_method("spawn", force=True)
        predict = AsyncPredict(
            cfg, num_gpus=gpus, num_cpus=cpus, queue_size=queue_size, ordered=False
        )
    else:
        predict = Predict(cfg)

    if separate_background:
        separate_background = SeparateBackground("vis_image")
        annotate_image = None
    else:
        separate_background = None
        metadata_name = cfg.DATASETS.TEST[0] if len(cfg.DATASETS.TEST) else "__unused"
        annotate_image = AnnotateImage("vis_image", metadata_name)

    save_image = SaveImage("vis_image", output_path)

    # Create image processing pipeline
    pipeline = (
        capture_images | predict | separate_background | annotate_image | save_image
    )

    # Iterate through pipeline
    try:
        for _ in tqdm(pipeline, disable=not progress):
            pass
    except StopIteration:
        return
    except KeyboardInterrupt:
        return
    finally:
        # Pipeline cleanup
        if isinstance(predict, AsyncPredict):
            predict.cleanup()


if __name__ == "__main__":
    # Test it out on some trashpanda training images
    input_path = "assets/images/waste/glass-0001.png"

    process_images(input_path)
