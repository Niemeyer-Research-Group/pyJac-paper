#! /usr/bin/env python
import os
import subprocess

script_dir = os.path.dirname(os.path.realpath(__file__))

#first, create the data file
from data_bin_writer import main
main(script_dir, cut=None)

#next call make
subprocess.check_call(['make', '-f', os.path.join(script_dir, 'makefile')])

#and finally run
subprocess.check_call([os.path.join(script_dir, 'tctest')])

#and cleanup
subprocess.check_call(['make', '-f', os.path.join(script_dir, 'makefile'), 'clean'])

