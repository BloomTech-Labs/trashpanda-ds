import cv2

from pipeline.pipeline import Pipeline


class CaptureImage(Pipeline):
    """Pipeline task to capture single image file"""

    def __init__(self, src):
        self.src = src

        super().__init__()

    def generator(self):
        """Yields the image content and metadata."""

        image = cv2.imread(self.src, cv2.IMREAD_UNCHANGED)

        data = {"image_id": self.src, "image": image}

        if self.filter(data):
            yield self.map(data)
