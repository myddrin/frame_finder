"""
This script is to setup frame_finder.py to compile with py2exe

run as:
python py2exe_setup.py py2exe
"""

from distutils.core import setup
import py2exe
import os

# data files are normally needed data to run the program but we copy all
other_files = [
    ('.', ['copying.txt', 'readme.txt'])
]
example_files = [
    ('.', ['run_example_dist.cmd'])
]

setup(
    console = ['frame_finder.py'],
    data_files = other_files
)

setup(
    console = ['create_example.py'],
    data_files = example_files
)