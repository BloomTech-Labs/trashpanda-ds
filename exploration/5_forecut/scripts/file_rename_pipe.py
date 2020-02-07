"""
Pipeline practice to rename image files.
"""

import os
import cv2


def walk_to_level(path, level=None):
    if level is None:
        yield from os.walk(path)
        return

    path = path.rstrip(os.path.sep)
    num_sep = path.count(os.path.sep)
    for root, dirs, files in os.walk(path):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            # When some directory on or below the desired level is found, all
            # of its subdirs are removed from the list of subdirs to search next.
            # So they won't be walked.
            del dirs[:]


def list_files(path, valid_exts=None, level=None, contains=None):
    """Loop over the input directory structure."""
    for (root_dir, dir_names, filenames) in walk_to_level(path, level):
        for filename in sorted(filenames):
            # ignore the file if not contains the string
            if contains is not None and contains not in filename:
                continue

            # Determine the file extension of the current file
            ext = filename[filename.rfind(".") :].lower()
            if valid_exts and ext.endswith(valid_exts):
                # Construct the path to the file and yield it
                file = os.path.join(root_dir, filename)
                yield file


class Pipeline:
    """Abstract base class for building pipelines."""

    def __init__(self):
        self.source = None

    def __iter__(self):
        return self.generator()

    def generator(self):
        while self.has_next():
            data = next(self.source) if self.source else {}
            if self.filter(data):
                yield self.map(data)

    def __or__(self, other):
        other.source = self.generator()
        return other

    def filter(self, data):
        return True

    def map(self, data):
        return data

    def has_next(self):
        return True


class RenameImages(Pipeline):
    def __init__(self, src, valid_exts=(".jpg", ".png")):
        self.src = src
        self.valid_exts = valid_exts

        super(RenameImages, self).__init__()

    def generator(self):
        source = list_files(self.src, self.valid_exts)

        while self.has_next():
            old = next(source)

            old_path, old_ext = os.path.splitext(old)
            old_name = old_path.split("/")[-1]

            class_name = old_name.split()[0]
            img_id = old_name.split()[2].zfill(4)
            new_name = f"{class_name}-{img_id}"

            new_path = os.path.join(self.src, new_name)
            new = f"{new_path}{old_ext}"

            print(f"{old}")
            print(f"{new}")
            data = new_path

            os.rename(old, new_path)

            if self.filter(data):
                yield self.map(data)


# class Printer(Pipeline):
#     def map(self, value):
#         print(value)
#         return value


def main(img_path):
    rename = RenameImages(img_path)
    # printer = Printer()

    pipeline = rename

    for i in pipeline:
        pass


if __name__ == "__main__":
    main("/Users/Tobias/workshop/buildbox/forecut/assets_/images")
