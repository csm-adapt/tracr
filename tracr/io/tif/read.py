#!/usr/bin/env python
"""
Converts TIF format files/dirs into a numpy format intensity voxel array.
3D arrays are transposed such that the 'z'direction of the array is also 'up'
in the uXCT machine frame.

INPUT:
    - .tif file (either single or multilayer), or folder of .tif frames

OUTPUT:
    - Numpy array (either 2D or 3D) of intensity data

USAGE:
    e.g. intensity_array = read('path/to/data.tif')
    e.g. intensity_array = read('path/to/TIF_folder/')
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
								axes=(1,2,0))
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
        # Load inputs and read ifile normally
        ifile = sys.argv[1]
        path, base = os.path.split(ifile)
        intensity_array = read(ifile)
        try:
            ofile = sys.argv[2]
        except IndexError:
            # Extract path for saving array
            ofile, ext = os.path.splitext(base)
        np.save(path+ofile, intensity_array)
    except IndexError:
		sys.stderr.write('CL Usage: python {} [path/to/ifile] [ofile_name]'.format(sys.argv[0]))
		sys.exit(1)
