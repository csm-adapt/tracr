#!/usr/bin/env python
"""
Converts .dcm format data to a Feature object.

INPUT:
	- List of single dcm frame, or list of multiple frames
	- * pixelsize set in tracr.io.read

OUTPUT:
	- Feature object (array (either 2D or 3D) of .dcm intensity data).

USAGE:
	e.g. intensity_array = read('path/to/frame.dcm')
	e.g. intensity_array = read('path/to/DCM_folder/')
"""

import sys, os, glob
import dicom
import numpy as np
from ..base import Feature

def read_single(ifile):
    return dicom.read_file(ifile).pixel_array

def read(ifile, **kwds):
	# ifile is a list, generate Feature object by iterating through list
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
