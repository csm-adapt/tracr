#!/usr/bin/env python
"""
A script that converts DCM formatted data into a numpy array of intensity
values. Iteratively processes each .dcm layer at a time (no multilayer).

INPUT:
	- Either a single .dcm file or folder of .dcm frames

OUTPUT:
	- Numpy array (either 2D or 3D) of .dcm intensity data.

USAGE:
	e.g. intensity_array = read('path/to/frame.dcm')
	e.g. intensity_array = read('path/to/DCM_folder/')
"""

import sys, os, glob
import dicom
import numpy as np

def read_single(ifile):
    return dicom.read_file(ifile).pixel_array

def read(ifile):
	# If input is folder, iterate through each frame and then transpose 3D array
    if os.path.isdir(ifile):
        all_frames = glob.glob(ifile+'*')
        return np.transpose(np.array([read_single(frame) for frame in all_frames]),
                                        axes=(1,2,0))
	else:
        return read_single(ifile)

if __name__ == '__main__':
	try:
		# generate array
		intensity_array = read(ifile)
		# read filename
		try:
			ofile = sys.argv[2]
		except IndexError:
			path, base = os.path.split(ifile)
			ofile, ext = os.path.splitext(base)
		# save the output
		np.save(path+ofile, intensity_array)
	except:
		sys.stderr.write('Usage: {} INPUT.tif [OUTPUT.npy]'.format(sys.argv[0]))
		sys.exit(1)
