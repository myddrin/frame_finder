
import os
import shutil
from frame_finder import *

def create_folder(name, prefix, start, end, ext, fill, miss):

    if not os.path.exists(name):
        os.mkdir(name)
    print "poulating " + name + " from " + prefix + str(start).zfill(fill) + "." + ext + " to " + prefix + str(end).zfill(fill) + "." + ext

    for f in range(start, end):
        if f%miss != 0:
            touch(name + "/image" + str(f).zfill(fill) + "." + ext)


if __name__ == "__main__":

    if os.path.exists("example"):
        shutil.rmtree("example")
    if not os.path.exists("example"):
        os.mkdir("example")
    if not os.path.exists("example/empty_images"):
        os.mkdir("example/empty_images")

    create_folder("example/images", "image", 0, 14, "jpg", 2, 5)
    create_folder("example/other_images", "image", 0, 14, "jpg", 2, 6)
