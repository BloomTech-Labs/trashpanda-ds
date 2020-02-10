"""ForeCut Pipeline :: Generate predictions"""


from forecut_pipeline.pipeline import Pipeline


class Predict(Pipeline):
    """Pipeline task for performing predictions."""

    def __init__(self, model):
        self.model = model

        super().__init__()

    def map(self, data):
        image = data["image"]
        results = self.model.detect([image], verbose=1)
        result = results[0]
        data["result"] = result

        return data

