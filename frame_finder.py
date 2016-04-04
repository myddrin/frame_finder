#!/usr/bin/python

import shutil
import os
import glob
import re
import argparse

def touch(path):
    open(path, 'w').close()

class FrameFinder:

    base_regexp = "([0-9]*)\." # to allow update in case prefix or extension changed

    prefix = "image"
    extension = "exr"
    reg_exp = prefix + base_regexp + extension
    verbose = False
    duplicate = False # duplicate last found
    createEmpty = True # create empty file
    zfill = 4 # number of digits
        
    def getFilename(self, number = 0):
        return self.prefix + str(number).zfill(self.zfill) + "." + self.extension

    def verify(self, basedir = "."):

        found_numbers = list()

        print "searching in " + basedir

        for filename in glob.glob(basedir + "/*." + self.extension):
            
            found = re.findall(self.reg_exp, filename)
            
            if self.verbose:
                print "found " + filename + " found: " + str(found)
            
            num = found[0]
            if num.isdigit():
                
                found_numbers.append(int(num))

        found_numbers = sorted(found_numbers)

        prev = found_numbers[0]

        for num in found_numbers:
            
            while prev+1 < num:
                
                missing = prev+1
                filename = self.getFilename(missing)
                
                if self.duplicate:
                    
                    prev_filename = self.getFilename(prev)
                    
                    print "copying " + prev_filename + " to " + filename
                        
                    shutil.copyfile(basedir + "/" + prev_filename, basedir + "/" + filename)
                
                elif self.createEmpty:
                    
                    print "touch " + filename
                        
                    touch(basedir + "/" + filename)
                
                else:
                    
                    print "missing file " + filename
                
                prev = missing
            
            prev = num

if __name__ == "__main__":
    
    finder = FrameFinder()
    parser = argparse.ArgumentParser("check that file with all numbers exist using a prefix and extension. If no option is given to replace file then only printing is done.")
    
    parser.add_argument("--prefix", type=str, dest="prefix", default=finder.prefix,
        help="filename prefix - default: " + finder.prefix)
    parser.add_argument("--extension", type=str, dest="extension", default=finder.extension,
        help="file extension without the dot - default: " + finder.extension)
    parser.add_argument("--regexp", type=str, dest="reg_exp", default=finder.reg_exp,
        help="regular expression to find the file (updated if filename or extension is changed) - default " + finder.reg_exp)
    
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose",
        help="verbose printing")
    parser.add_argument("-d", "--duplicate", action="store_true", dest="duplicate",
        help="Duplicate the previous frame when not found (has priority over other options)")
    parser.add_argument("-t", "--touch", action="store_true", dest="touch",
        help="Create empty file when not found using prefix and extension")
    parser.add_argument("-z", "--zerofill", type=int, dest="zfill", default=finder.zfill,
        help="Number of digits to use with zero fill (with z=3 converts 40 to 040) - default " + str(finder.zfill))
    
    parser.add_argument("dir", nargs="+", type=str,
        help="Verify files in a given directory")
    
    args = parser.parse_args()
    
    updateReg = False
    
    if args.prefix != finder.prefix:
        updateReg = True
        finder.prefix = args.prefix
    if args.extension != finder.extension:
        updateReg = True
        finder.extension = args.extension
    if args.reg_exp != finder.reg_exp:
        updateReg = False
        finder.reg_exp = args.reg_exp
    
    if updateReg:
        finder.reg_exp = finder.prefix + finder.base_regexp + finder.extension
    
    finder.verbose = args.verbose
    finder.duplicate = args.duplicate
    finder.createEmpty = args.touch
    finder.zfill = args.zfill
    
    for directory in args.dir:
        
		if os.path.isdir(directory):
			finder.verify(directory)
		else:
			print directory + " is not a directory"
