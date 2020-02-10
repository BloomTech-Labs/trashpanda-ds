"""ForeCut \\ Pipeline :: Remove background"""

import os
import sys

import cv2
import numpy as np

from forecut_pipeline.pipeline import Pipeline


class RemoveBg(Pipeline):
    def __init__(self, dst):
        self.dst = dst

        super().__init__()

    def map(self, data):
        self.remove_bg(data)

        return data

    def remove_bg(self, data):
        if "result" not in data:
            return

        result = data["result"]
        if "masks" not in result:
            return

        # Extract mask and image from data
        mask = result["masks"]
        image = data["image"]

        # We're treating all instances as one, so collapse the mask into one layer
        mask = np.sum(mask, -1, keepdims=True) >= 1

        # Create blank black background
        background = np.zeros(image.shape)

        # Copy color pixels from the original color image where mask is set
        dst_image = np.where(mask, image, background).astype(np.uint8)

        # Convert to 4-channel image
        tmp = cv2.cvtColor(dst_image.astype("uint8"), cv2.COLOR_BGR2GRAY)
        _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
        b, g, r = cv2.split(dst_image.astype("uint8"))
        rgba = [b, g, r, alpha]
        dst2 = cv2.merge(rgba, 4)

        data[self.dst] = dst2
