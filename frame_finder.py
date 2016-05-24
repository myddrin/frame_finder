#!/usr/bin/python

"""
This python script was created to find missing files in given folders.

Copyright (c) 2016 Thomas Richard

Following MIT license (see copying.txt)

The software is provided "as is", without warranty of any kind, express or
implied, including but not limited to the warranties of merchantability,
fitness for a particular purpose and noninfringement.
"""

import shutil
import os
import glob
import re
import argparse


def touch(path):
    """
    Create a file
    """
    open(path, 'w').close()


class FrameFinder:
    """
    Object to check that files following a sequence of numbers exist
    """

    class Operations:
        NONE, DUPLICATE, TOUCH = range(3)
        # NONE: do nothin besides printing when not finding a file
        # DUPLICATE: When not finding a file duplicate the last found one
        # TOUCH: When not finding a file create a new empty file

    def __init__(self, prefix="image", extension="exr",
                 zfill=4, duplicate=False):
        # local variable as not used after creation
        base_regexp = "([0-9]*)\."
        """base_regexp: to allow update in case prefix or extension changed"""

        self.prefix = prefix
        """filename prefix"""
        self.extension = extension
        """filename extension"""
        self.reg_exp = self.prefix + base_regexp + self.extension
        self.verbose = False

        self.zfill = 4
        """number of digits to use to create a name with leading 0s"""

    def getFilename(self, number=0):
        """
        Return filename based on prefix, number zfill and extension
        """
        return self.prefix + str(number).zfill(self.zfill) \
            + "." + self.extension

    def find_missing(self, basedir="."):
        """
        Return a list of missing files in basedir by checking the range from
        existing files
        """
        found_numbers = list()
        missing_files = list()

        print "searching in " + basedir

        for filename in glob.glob(basedir + "/*." + self.extension):
            found = re.findall(self.reg_exp, filename)
            if self.verbose:
                print "found " + filename + " found: " + str(found)

            if len(found) > 0:
                num = found[0]
            else:
                num = ""

            if num.isdigit():
                found_numbers.append(int(num))
            else:
                if self.verbose:
                    print ("Could not find a digit in filename '" + filename +
                           "' using '" + reg_exp + "'")
                continue  # next frame

        if len(found_numbers) == 0:
            print "Did not find any files!"
            return missing_files

        found_numbers = sorted(found_numbers)
        prev = found_numbers[0]

        for num in found_numbers:
            while prev+1 < num:
                missing = prev+1
                filename = self.getFilename(missing)
                missing_files.append(filename)
                prev = missing
            prev = num
        return missing_files

    def apply(self, basedir, missing_files, ope):
        """
        Given a list of missing file will apply the given option using
        duplicate and createEmpty options
        Default operation is NONE
        """
        for filename in missing_files:
            if ope == FrameFinder.Operations.DUPLICATE:
                found = re.findall(self.reg_exp, filename)
                if found.size() > 0:
                    num = found[0]
                else:
                    raise ValueError("regexp '" + reg_exp +
                                     "' failed to find 1 group in '" +
                                     str(filename) + "'")
                if num.isdigit():
                    prev = int(num) - 1
                else:
                    raise ValueError("could not find number in filename '" +
                                     str(filename) + "' given as input")
                prev_filename = self.getFilename(prev)
                print "copying " + prev_filename + " to " + filename
                shutil.copyfile(basedir + "/" + prev_filename,
                                basedir + "/" + filename)
            elif ope == FrameFinder.Operations.TOUCH:
                print "touch " + filename
                touch(basedir + "/" + filename)
            elif ope == FrameFinder.Operations.NONE:
                # operation has to be NONE
                print "missing file " + filename
            else:
                raise ValueError("Invalid operation '" + ope + "' given")

    def verify(self, basedir, ope=Operations.NONE):
        """
        Utility method to verify a directory
        """
        missing_files = self.find_missing(basedir)
        self.apply(basedir, missing_files, ope)


if __name__ == "__main__":
    """
    Verify that a folder contains all images
    """
    parser = argparse.ArgumentParser("frame_finder.py")
    finder = FrameFinder()  # to have default values
    # long options
    parser.add_argument("--prefix", type=str, dest="prefix",
                        default=finder.prefix,
                        help="filename prefix - default: " + finder.prefix)
    parser.add_argument("--extension", type=str, dest="extension",
                        default=finder.extension,
                        help=("file extension without the dot - default: " +
                              finder.extension))
    parser.add_argument("--regexp", type=str, dest="reg_exp",
                        default="",
                        help=("regular expression to find the file. The "
                              "regular expression is updated if filename "
                              "prefix or extension is changed or can be "
                              "specified here directly - default " +
                              finder.reg_exp))
    # short options
    parser.add_argument("-v", "--verbose", action="store_true",
                        dest="verbose",
                        help="verbose printing")
    parser.add_argument("-d", "--duplicate", action="store_true",
                        dest="duplicate",
                        help=("Duplicate the previous frame when not found "
                              "(has priority over other options)"))
    parser.add_argument("-t", "--touch", action="store_true", dest="touch",
                        help=("Create empty file when not found using prefix "
                              "and extension"))
    parser.add_argument("-z", "--zerofill", type=int, dest="zfill",
                        default=finder.zfill,
                        help=("Number of digits to use with zero fill (with "
                              "z=3 converts 40 to 040) - default " +
                              str(finder.zfill)))
    # remaining parameters are directories to search
    parser.add_argument("dir", nargs="+", type=str,
                        help="Verify files in a given directory")

    args = parser.parse_args()

    finder = FrameFinder(args.prefix, args.extension, args.zfill)

    if args.reg_exp != "":
        finder.reg_exp = args.reg_exp

    finder.verbose = args.verbose
    operation = FrameFinder.Operations.NONE
    if args.duplicate:
        operation = FrameFinder.operations.DUPLICATE
    elif args.touch:
        operation = FrameFinder.operations.TOUCH

    for directory in args.dir:
        if os.path.isdir(directory):
            finder.verify(directory, operation)
            print ""  # empty line between dirs
        else:
            print directory + " is not a directory"
