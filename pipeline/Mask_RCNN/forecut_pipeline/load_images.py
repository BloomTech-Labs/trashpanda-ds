"""ForeCut Pipeline :: Load multiple images"""

import cv2

from forecut_pipeline.pipeline import Pipeline
import forecut_pipeline.utils.fs as fs


class LoadImages(Pipeline):
    """Pipeline task to load multiple images."""

    def __init__(
        self, path, valid_exts=(".jpg", ".jpeg", ".png"), level=None, contains=None
    ):
        self.path = path
        self.valid_exts = valid_exts
        self.level = level
        self.contains = contains

        super().__init__()

    def generator(self):
        """Yields the image content and metadata."""

        source = fs.list_files(self.path, self.valid_exts, self.level, self.contains)
        while self.has_next():
            try:
                image_file = next(source)
                image = cv2.imread(image_file)

                data = {"image_id": image_file, "image": image}

                if self.filter(data):
                    yield self.map(data)

            except StopIteration:
                return
