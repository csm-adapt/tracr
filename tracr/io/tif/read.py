#!/usr/bin/env python
"""
A script that converts TIF format files/dirs into a numpy format
intensity voxel array. 3D arrays are transposed such that the 'z'
direction of the array is also 'up' in the uXCT machine frame.
"""

import sys, os, glob
import numpy as np
from PIL import Image, ImageSequence

def read_multilayer(ifile):
    """
    File reader for single file, multilayer TIF images (3D data)
    e.g. 'sampleX_multilayer.tif'
    """
    im = Image.open(ifile)
    intensity_array = np.array([np.array(frame) for frame in ImageSequence.Iterator(im)])
    return intensity_array

def read_single(ifile):
    """
    File reader for single file, single layer TIF images (2D data)
    e.g. 'sampleX.tif'
    """
    return np.array(Image.open(ifile))

def read(ifile):
    """
    Root reading function:
        - Check if argument is single file (multi or single layer) or directory
        - Call appropriate reader
		- Tranpose data for upwards-z indexing
    """
    if os.path.isdir(ifile):
        # DIR: Iterate through each frame contained in directory
        all_frames = glob.glob(ifile+'*')
        return np.transpose(np.array([read_single(frame) for frame in all_frames]),
								axes=(1,2,0)
    else:
        # FILE: Check if file is single or multilayer, read accordingly
        im = Image.open(ifile)
        if im.n_frames == 1:
            arr = read_single(ifile)
            return arr
        else:
            arr = read_multilayer(ifile)
            return np.transpose(arr, axes=(1,2,0))

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
