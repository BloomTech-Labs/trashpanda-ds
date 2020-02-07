"""Generator-based script to build a dataset from a filesystem."""

import os


class FileReader:
    """Base class for reading through a file system."""

    def __init__(self, src, valid_exts=(".jpg", ".jpeg", ".png")):
        self.src = src
        self.valid_exts = valid_exts

    def file_printer(self):
        for filename in sorted(os.listdir(self.src)):
            yield filename


def main(src):
    reader = FileReader(src)
    for f in reader.file_printer():
        print(f)


if __name__ == "__main__":
    main("/Users/Tobias/workshop/buildbox/forecut/assets_/images")

