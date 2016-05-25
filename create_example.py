#!/usr/bin/python

"""
Utility to create an example folder

Copyright (c) 2016 Thomas Richard

Following MIT license (see copying.txt)

The software is provided "as is", without warranty of any kind, express or
implied, including but not limited to the warranties of merchantability,
fitness for a particular purpose and noninfringement.
"""

import os
import shutil
from test_frame_finder import create_folder


if __name__ == "__main__":

    if os.path.exists("example"):
        shutil.rmtree("example")
    if not os.path.exists("example"):
        os.mkdir("example")
    if not os.path.exists("example/empty_images"):
        os.mkdir("example/empty_images")

    create_folder("example/images", "image", 0, 14, "jpg", 2, 5)
    create_folder("example/other_images", "image", 0, 14, "jpg", 2, 6)
