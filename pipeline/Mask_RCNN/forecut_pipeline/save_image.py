"""ForeCut \\ Pipeline :: Save image(s)"""

import os

import skimage.io

from forecut_pipeline.pipeline import Pipeline


class SaveImage(Pipeline):
    """Pipeline task to save images."""

    def __init__(self, src, path, image_ext="png"):
        self.src = src
        self.path = path
        self.image_ext = image_ext

        super().__init__()

    def map(self, data):
        image = data[self.src]
        image_id = data["image_id"]

        # Prepare output for image based on image_id
        output = image_id.split(os.path.sep)
        dirname = output[:-1]
        if len(dirname) > 0:
            dirname = os.path.join(*dirname)
            dirname = os.path.join(self.path, dirname)
            os.makedirs(dirname, exist_ok=True)
        else:
            dirname = self.path
        filename = f"{output[-1].rsplit('.', 1)[0]}.{self.image_ext}"
        path = os.path.join(dirname, filename)

        skimage.io.imsave(
            path, image,
        )

        return data
