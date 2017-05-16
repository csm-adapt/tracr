#!/usr/bin/env python
"""
Converts TIF format data to a Feature object.

INPUT:
    - List of either single/multi layer tif file, or list of individual files
    - pixelsize has been set as a **kwds argument as per tracr.io.read

OUTPUT:
    - Feature object

USAGE:
    e.g. feat = read(glob.glob()'path/to/dataFolder/*tif'), pixelsize=px_size)
    e.g. feat = read('path/to/tifFrame', pixelsize=px_size)
    * pixelsize has been set in general reading function.
"""

import sys, os, glob
import numpy as np
from PIL import Image, ImageSequence
from ..base import Feature

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
    File reader for single file, single layer TIF images (2D data). We also
    ensure that RGB images are greyscale before converting (ITU-R 601-2).
    e.g. 'frameX.tif'
    """
    im = Image.open(ifile)
    if im.mode in ('RGB', 'RGBA'):
        im = im.convert('L')
    return np.array(im)

def read(ifile, **kwds):
    """
    Root reading function:
        - Check if list is single file (multi/single layer), or list of frames
        - Call appropriate reader
		- Tranpose data for upwards-z indexing
        - Initiate Feature class using output numpy array and pixelsize kwd
    """
    # If only single file, either singlelayer or multilayer tif
    if len(ifile) == 1:
        im = Image.open(ifile[0])
        # Check if single or multilayer
        if im.n_frames == 1:
            arr = read_single(ifile[0])
            return Feature(arr, pixelsize=kwds['pixelsize'])
        else:
            arr = np.transpose(read_multilayer[ifile[0]], axes=(1,2,0))
            return Feature(arr, pixelsize=kwds['pixelsize'])
    # Must be list of multiple frames
    else:
        arr = np.transpose(np.array([read_single(frame) for frame in ifile]),
                            axes=(1,2,0))
        return Feature(arr, pixelsize=kwds['pixelsize'])


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
        np.save(path+'_'+ofile, intensity_array)
    except IndexError:
		sys.stderr.write('CL Usage: python {} [path/to/ifile] [ofile_name]'.format(sys.argv[0]))
		sys.exit(1)
