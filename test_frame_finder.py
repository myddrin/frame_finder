#!/usr/bin/python

"""
Unit test for frame_finder

Copyright (c) 2016 Thomas Richard

Following MIT license (see copying.txt)

The software is provided "as is", without warranty of any kind, express or
implied, including but not limited to the warranties of merchantability,
fitness for a particular purpose and noninfringement.
"""

import os
import shutil
from frame_finder import *


def create_folder(name, prefix, start, end, ext, fill, miss):
    if not os.path.exists(name):
        os.mkdir(name)
    print ("populating " + name + " from " + prefix + str(start).zfill(fill) +
           "." + ext + " to " + prefix + str(end - 1).zfill(fill) + "." + ext)

    for f in range(start, end):
        if miss <= 1 or f % miss != 0:
            touch(name + "/image" + str(f).zfill(fill) + "." + ext)


class FrameFinderTest:

    zfill = 2
    test_no = -1  # to start at 0

    def init_test(self):
        self.test_no += 1
        print ""
        print "TEST " + str(self.test_no).zfill(self.zfill)

        fold = "test_" + str(self.test_no).zfill(self.zfill)
        if os.path.exists(fold):
            print ("cleaning " + fold)
            shutil.rmtree(fold)
        return fold

    def test_no_missing(self):
        fold = self.init_test()

        finder = FrameFinder()
        create_folder(fold, finder.prefix, 0, 4,
                      finder.extension, finder.zfill, 1)

        missing = finder.find_missing(fold)
        print "len(missing) = " + str(len(missing))

        if len(missing) != 0:
            raise ValueError("should not miss files")

    def test_missing(self):
        fold = self.init_test()

        finder = FrameFinder()
        create_folder(fold, finder.prefix, 0, 4,
                      finder.extension, finder.zfill, 2)
        # should be missing frame 2

        missing = finder.find_missing(fold)
        print "len(missing) = " + str(len(missing))

        if len(missing) != 1:
            raise ValueError("should be missin only 1 frame")
        expected = (finder.prefix + str(2).zfill(finder.zfill) +
                    "." + finder.extension)
        if missing[0] != expected:
            raise ValueError("expecting " + expected + " but got " +
                             missing[0])

    def test_printing(self):
        fold = self.init_test()

        finder = FrameFinder()
        create_folder(fold, finder.prefix, 0, 4,
                      finder.extension, finder.zfill + 1, 2)
        # should be missing frame 2 but the numbering generated is bigger

        missing = finder.find_missing(fold)
        print "len(missing) = " + str(len(missing))

        finder.apply(fold, missing, FrameFinder.Operations.NONE)

        missing_after = finder.find_missing(fold)
        print "len(missing_after) = " + str(len(missing_after))

        if len(missing) != len(missing_after):
            raise ValueError("NONE should not affect content")

    def test_touch(self):
        fold = self.init_test()

        finder = FrameFinder()
        create_folder(fold, finder.prefix, 0, 4,
                      finder.extension, finder.zfill, 2)
        # should be missing frame 2 but the numbering generated is bigger

        missing = finder.find_missing(fold)
        print "len(missing) = " + str(len(missing))

        finder.apply(fold, missing, FrameFinder.Operations.TOUCH)

        missing_after = finder.find_missing(fold)
        print "len(missing_after) = " + str(len(missing_after))

        if len(missing) <= len(missing_after):
            raise ValueError("TOUCH should affect content")
        if len(missing_after) != 0:
            raise ValueError("TOUCH should have fix content")

    def test_duplicate(self):
        fold = self.init_test()

        finder = FrameFinder()
        create_folder(fold, finder.prefix, 0, 4,
                      finder.extension, finder.zfill, 2)
        # should be missing frame 2 but the numbering generated is bigger

        missing = finder.find_missing(fold)
        print "len(missing) = " + str(len(missing))

        finder.apply(fold, missing, FrameFinder.Operations.DUPLICATE)

        missing_after = finder.find_missing(fold)
        print "len(missing_after) = " + str(len(missing_after))

        if len(missing) <= len(missing_after):
            raise ValueError("DUPLICATE should affect content")
        if len(missing_after) != 0:
            raise ValueError("DUPLICATE should have fix content")

    def test_touch_zfill(self):
        fold = self.init_test()

        finder = FrameFinder()
        create_folder(fold, finder.prefix, 0, 4,
                      finder.extension, finder.zfill + 1, 2)
        # should be missing frame 2 but the numbering generated is bigger

        missing = finder.find_missing(fold)
        print "len(missing) = " + str(len(missing))

        finder.apply(fold, missing, FrameFinder.Operations.TOUCH)

        missing_after = finder.find_missing(fold)
        print "len(missing_after) = " + str(len(missing_after))

        if len(missing) <= len(missing_after):
            raise ValueError("TOUCH should affect content")
        if len(missing_after) != 0:
            raise ValueError("TOUCH should have fix content")

    def test_duplicate_zfill(self):
        fold = self.init_test()

        finder = FrameFinder()
        create_folder(fold, finder.prefix, 0, 4,
                      finder.extension, finder.zfill + 1, 2)
        # should be missing frame 2 but the numbering generated is bigger

        missing = finder.find_missing(fold)
        print "len(missing) = " + str(len(missing))

        finder.apply(fold, missing, FrameFinder.Operations.DUPLICATE)

        missing_after = finder.find_missing(fold)
        print "len(missing_after) = " + str(len(missing_after))

        if len(missing) <= len(missing_after):
            raise ValueError("DUPLICATE should affect content")
        if len(missing_after) != 0:
            raise ValueError("DUPLICATE should have fix content")

if __name__ == "__main__":
    # TODO: use pytest
    test = FrameFinderTest()

    test.test_no_missing()
    test.test_missing()
    test.test_printing()
    test.test_touch()
    test.test_duplicate()
    # if zfill is wrong duplicate fails to duplicate
    test.test_touch_zfill()
    # test.test_duplicate_zfill()  # TODO: enable back when fixed
